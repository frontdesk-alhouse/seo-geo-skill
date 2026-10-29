#!/usr/bin/env python3
"""Audita la metadata publicada de un sitio, página por página, sobre el HTML servido.

Por URL revisa: <title> (ideal 50-60 caracteres), meta description (120-160),
canonical (presente, absoluto, apunta a sí misma, https), og:title,
og:description, og:image, twitter:card, número de <h1> (debe ser 1), lang del
<html>, hreflang y noindex (meta robots o cabecera X-Robots-Tag). Al final
detecta títulos y descripciones duplicados entre páginas y resume los problemas
por severidad.

Mide el HTML que sirve el servidor, no el que se ve en el Designer: si se editó
en vivo, lo publicado manda.

Uso:
    python3 verificar_metadata.py https://www.ejemplo.mx/sitemap.xml
    python3 verificar_metadata.py urls.txt --json
    python3 verificar_metadata.py https://www.ejemplo.mx/servicios --max 1
Sale con código 1 si hay algún ERROR (sirve como gate antes de publicar).
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import fetch, header, md_table, meta_content, parse_html, resolve_targets  # noqa: E402

TITLE_RANGE = (50, 60)
DESC_RANGE = (120, 160)
SEVERITIES = ("ERROR", "AVISO", "INFO")


def _norm_url(url: str) -> str:
    parts = urllib.parse.urlparse(url)
    path = parts.path.rstrip("/") or "/"
    return f"{parts.netloc.lower().removeprefix('www.')}{path}"


def extract(url: str, timeout: float) -> dict:
    """Descarga la página y extrae los campos de metadata."""
    resp = fetch(url, timeout=timeout)
    page = parse_html(resp["body"])
    canonical = next((ln.get("href") for ln in page.links if "canonical" in ln.get("rel", "").lower()), None)
    hreflang = [ln.get("hreflang") for ln in page.links
                if "alternate" in ln.get("rel", "").lower() and ln.get("hreflang")]
    return {"url": url, "final_url": resp["final_url"], "status": resp["status"], "error": resp["error"],
            "title": page.title or None, "description": meta_content(page, "description"),
            "canonical": canonical, "og_title": meta_content(page, "og:title"),
            "og_description": meta_content(page, "og:description"), "og_image": meta_content(page, "og:image"),
            "twitter_card": meta_content(page, "twitter:card"), "h1": page.h1, "lang": page.lang,
            "hreflang": hreflang, "robots": meta_content(page, "robots"),
            "x_robots_tag": header(resp["headers"], "x-robots-tag")}


def _length_issue(label: str, value: str | None, bounds: tuple[int, int]) -> list[tuple[str, str]]:
    if not value:
        return [("ERROR", f"{label} ausente")]
    lo, hi = bounds
    if not lo <= len(value) <= hi:
        return [("AVISO", f"{label} de {len(value)} caracteres (ideal {lo}-{hi})")]
    return []


def _canonical_issues(page: dict) -> list[tuple[str, str]]:
    canonical = page["canonical"]
    if not canonical:
        return [("AVISO", "sin canonical")]
    issues = []
    if not canonical.startswith(("http://", "https://")):
        issues.append(("AVISO", f"canonical relativo: {canonical}"))
    if canonical.startswith("http://") and page["final_url"].startswith("https://"):
        issues.append(("ERROR", "canonical en http:// sobre una página https"))
    absolute = urllib.parse.urljoin(page["final_url"], canonical)
    if _norm_url(absolute) != _norm_url(page["final_url"]):
        issues.append(("AVISO", f"canonical apunta a otra URL: {absolute}"))
    elif urllib.parse.urlparse(absolute).netloc != urllib.parse.urlparse(page["final_url"]).netloc:
        issues.append(("INFO", f"canonical con otro formato de host (www): {absolute}"))
    return issues


def page_issues(page: dict) -> list[tuple[str, str]]:
    if page["error"] or page["status"] != 200:
        return [("ERROR", f"la página respondió {page['status'] or page['error']}")]
    issues = _length_issue("title", page["title"], TITLE_RANGE)
    issues += _length_issue("meta description", page["description"], DESC_RANGE)
    issues += _canonical_issues(page)
    issues += [("AVISO", f"falta {k.replace('_', ':')}") for k in ("og_title", "og_description", "og_image") if not page[k]]
    if not page["twitter_card"]:
        issues.append(("INFO", "falta twitter:card"))
    unique_h1 = {h.strip().lower() for h in page["h1"]}
    if len(page["h1"]) > 1 and len(unique_h1) == 1:
        # Framer serves one copy of the page per breakpoint group (ssr-variant); only one is visible.
        issues.append(("INFO", f"{len(page['h1'])} <h1> con el mismo texto: copia por breakpoint (Framer), no es error"))
    elif len(page["h1"]) != 1:
        issues.append(("ERROR" if not page["h1"] else "AVISO", f"{len(page['h1'])} elementos <h1> (debe haber 1)"))
    if not page["lang"]:
        issues.append(("AVISO", "<html> sin atributo lang"))
    noindex = "noindex" in (page["robots"] or "").lower() or "noindex" in (page["x_robots_tag"] or "").lower()
    if noindex:
        issues.append(("ERROR", "noindex en meta robots o X-Robots-Tag"))
    return issues


def duplicate_issues(pages: list[dict]) -> dict[str, list[tuple[str, str]]]:
    """Por URL, avisos de title/description repetidos en otras páginas."""
    extra: dict = defaultdict(list)
    for field, label in (("title", "title"), ("description", "meta description")):
        seen: dict = defaultdict(list)
        for page in pages:
            if page.get(field):
                seen[page[field].strip().lower()].append(page["url"])
        for urls in (u for u in seen.values() if len(u) > 1):
            for url in urls:
                others = ", ".join(x for x in urls if x != url)
                extra[url].append(("AVISO", f"{label} duplicado con: {others}"))
    return extra


def render_markdown(pages: list[dict], issues: dict) -> str:
    rows = [[p["url"], p["status"] or p["error"], len(p["title"] or ""), len(p["description"] or ""),
             len(p["h1"]), p["lang"] or "", "sí" if p["canonical"] else "no",
             "sí" if p["og_image"] else "no", len(issues[p["url"]])] for p in pages]
    counts = {s: sum(1 for p in pages for sev, _ in issues[p["url"]] if sev == s) for s in SEVERITIES}
    out = [f"# Metadata publicada\n\n{len(pages)} páginas · " + " · ".join(f"{s}: {n}" for s, n in counts.items()),
           md_table(["URL", "Status", "Title", "Desc.", "H1", "lang", "Canonical", "og:image", "Problemas"], rows)]
    detail = []
    for page in pages:
        for sev, msg in sorted(issues[page["url"]], key=lambda i: SEVERITIES.index(i[0])):
            detail.append(f"- **{sev}** {page['url']}: {msg}")
    out.append("## Detalle\n\n" + ("\n".join(detail) or "Sin problemas."))
    return "\n\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit published SEO metadata per page (title, description, canonical, OG, h1, lang, hreflang, noindex).")
    parser.add_argument("target", help="sitemap.xml URL, text file with one URL per line, or a single page URL")
    parser.add_argument("--max", type=int, default=200, help="maximum pages to check (default 200)")
    parser.add_argument("--workers", type=int, default=6, help="parallel requests (default 6)")
    parser.add_argument("--timeout", type=float, default=15.0, help="seconds per request (default 15)")
    parser.add_argument("--json", action="store_true", help="print JSON instead of Markdown")
    args = parser.parse_args(argv)
    try:
        urls = resolve_targets(args.target, args.timeout, args.max)
    except (RuntimeError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if not urls:
        print("error: no hay URLs que revisar", file=sys.stderr)
        return 1
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        pages = list(pool.map(lambda u: extract(u, args.timeout), urls))
    dups = duplicate_issues(pages)
    issues = {p["url"]: [*page_issues(p), *dups.get(p["url"], [])] for p in pages}
    if args.json:
        print(json.dumps([{**p, "problemas": [{"severidad": s, "mensaje": m} for s, m in issues[p["url"]]]}
                          for p in pages], ensure_ascii=False, indent=2))
    else:
        print(render_markdown(pages, issues))
    return 1 if any(sev == "ERROR" for v in issues.values() for sev, _ in v) else 0


if __name__ == "__main__":
    sys.exit(main())
