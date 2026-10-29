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
    python3 verificar_metadata.py https://www.example.com/sitemap.xml --lang en
Sale con código 1 si hay algún ERROR (sirve como gate antes de publicar).
Con --lang en la salida sale en inglés (AVISO pasa a WARN); las claves del JSON no cambian.
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
from _comun import (add_lang_arg, error_label, fetch, header, make_translator, md_table,  # noqa: E402
                    meta_content, parse_html, resolve_lang, resolve_targets)

TITLE_RANGE = (50, 60)
DESC_RANGE = (120, 160)
SEVERITIES = ("ERROR", "AVISO", "INFO")
SEVERITY_EN = {"AVISO": "WARN"}

MESSAGES = {
    "es": {
        "absent": "{label} ausente",
        "length": "{label} de {n} caracteres (ideal {lo}-{hi})",
        "no_canonical": "sin canonical",
        "canonical_relative": "canonical relativo: {value}",
        "canonical_http": "canonical en http:// sobre una página https",
        "canonical_other": "canonical apunta a otra URL: {value}",
        "canonical_host": "canonical con otro formato de host (www): {value}",
        "status": "la página respondió {status}",
        "missing": "falta {name}",
        "h1_framer": "{n} <h1> con el mismo texto: copia por breakpoint (Framer), no es error",
        "h1_count": "{n} elementos <h1> (debe haber 1)",
        "no_lang": "<html> sin atributo lang",
        "noindex": "noindex en meta robots o X-Robots-Tag",
        "duplicate": "{label} duplicado con: {others}",
        "title": "# Metadata publicada\n\n{n} páginas · {counts}",
        "col_url": "URL", "col_status": "Status", "col_title": "Title", "col_desc": "Desc.", "col_h1": "H1",
        "col_lang": "lang", "col_canonical": "Canonical", "col_og_image": "og:image", "col_issues": "Problemas",
        "h_detail": "## Detalle", "no_issues": "Sin problemas.",
        "no_urls": "error: no hay URLs que revisar",
    },
    "en": {
        "absent": "{label} missing",
        "length": "{label} is {n} characters (ideal {lo}-{hi})",
        "no_canonical": "no canonical",
        "canonical_relative": "relative canonical: {value}",
        "canonical_http": "http:// canonical on an https page",
        "canonical_other": "canonical points to another URL: {value}",
        "canonical_host": "canonical uses another host format (www): {value}",
        "status": "the page returned {status}",
        "missing": "missing {name}",
        "h1_framer": "{n} <h1> with the same text: one copy per breakpoint (Framer), not an error",
        "h1_count": "{n} <h1> elements (there must be 1)",
        "no_lang": "<html> without a lang attribute",
        "noindex": "noindex in meta robots or X-Robots-Tag",
        "duplicate": "{label} duplicated with: {others}",
        "title": "# Published metadata\n\n{n} pages · {counts}",
        "col_url": "URL", "col_status": "Status", "col_title": "Title", "col_desc": "Desc.", "col_h1": "H1",
        "col_lang": "lang", "col_canonical": "Canonical", "col_og_image": "og:image", "col_issues": "Issues",
        "h_detail": "## Detail", "no_issues": "No issues.",
        "no_urls": "error: no URLs to check",
    },
}


def _sev(severity: str, lang: str) -> str:
    return SEVERITY_EN.get(severity, severity) if lang == "en" else severity


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


def _length_issue(label: str, value: str | None, bounds: tuple[int, int], t) -> list[tuple[str, str]]:
    if not value:
        return [("ERROR", t("absent", label=label))]
    lo, hi = bounds
    if not lo <= len(value) <= hi:
        return [("AVISO", t("length", label=label, n=len(value), lo=lo, hi=hi))]
    return []


def _canonical_issues(page: dict, t) -> list[tuple[str, str]]:
    canonical = page["canonical"]
    if not canonical:
        return [("AVISO", t("no_canonical"))]
    issues = []
    if not canonical.startswith(("http://", "https://")):
        issues.append(("AVISO", t("canonical_relative", value=canonical)))
    if canonical.startswith("http://") and page["final_url"].startswith("https://"):
        issues.append(("ERROR", t("canonical_http")))
    absolute = urllib.parse.urljoin(page["final_url"], canonical)
    if _norm_url(absolute) != _norm_url(page["final_url"]):
        issues.append(("AVISO", t("canonical_other", value=absolute)))
    elif urllib.parse.urlparse(absolute).netloc != urllib.parse.urlparse(page["final_url"]).netloc:
        issues.append(("INFO", t("canonical_host", value=absolute)))
    return issues


def _h1_issues(h1: list[str], t) -> list[tuple[str, str]]:
    unique_h1 = {h.strip().lower() for h in h1}
    if len(h1) > 1 and len(unique_h1) == 1:
        # Framer serves one copy of the page per breakpoint group (ssr-variant); only one is visible.
        return [("INFO", t("h1_framer", n=len(h1)))]
    if len(h1) != 1:
        return [("ERROR" if not h1 else "AVISO", t("h1_count", n=len(h1)))]
    return []


def page_issues(page: dict, lang: str = "es") -> list[tuple[str, str]]:
    """Problemas de una página (severidad interna ERROR/AVISO/INFO, mensaje en el idioma pedido)."""
    t = make_translator(MESSAGES, lang)
    if page["error"] or page["status"] != 200:
        return [("ERROR", t("status", status=page["status"] or error_label(page["error"], lang)))]
    issues = _length_issue("title", page["title"], TITLE_RANGE, t)
    issues += _length_issue("meta description", page["description"], DESC_RANGE, t)
    issues += _canonical_issues(page, t)
    issues += [("AVISO", t("missing", name=k.replace("_", ":")))
               for k in ("og_title", "og_description", "og_image") if not page[k]]
    if not page["twitter_card"]:
        issues.append(("INFO", t("missing", name="twitter:card")))
    issues += _h1_issues(page["h1"], t)
    if not page["lang"]:
        issues.append(("AVISO", t("no_lang")))
    noindex = "noindex" in (page["robots"] or "").lower() or "noindex" in (page["x_robots_tag"] or "").lower()
    if noindex:
        issues.append(("ERROR", t("noindex")))
    return issues


def duplicate_issues(pages: list[dict], lang: str = "es") -> dict[str, list[tuple[str, str]]]:
    """Por URL, avisos de title/description repetidos en otras páginas."""
    t = make_translator(MESSAGES, lang)
    extra: dict = defaultdict(list)
    for field, label in (("title", "title"), ("description", "meta description")):
        seen: dict = defaultdict(list)
        for page in pages:
            if page.get(field):
                seen[page[field].strip().lower()].append(page["url"])
        for urls in (u for u in seen.values() if len(u) > 1):
            for url in urls:
                others = ", ".join(x for x in urls if x != url)
                extra[url].append(("AVISO", t("duplicate", label=label, others=others)))
    return extra


def render_markdown(pages: list[dict], issues: dict, lang: str = "es") -> str:
    t = make_translator(MESSAGES, lang)
    yes, no = t("yes"), t("no")
    rows = [[p["url"], p["status"] or error_label(p["error"], lang), len(p["title"] or ""),
             len(p["description"] or ""), len(p["h1"]), p["lang"] or "", yes if p["canonical"] else no,
             yes if p["og_image"] else no, len(issues[p["url"]])] for p in pages]
    counts = {s: sum(1 for p in pages for sev, _ in issues[p["url"]] if sev == s) for s in SEVERITIES}
    head = [t(k) for k in ("col_url", "col_status", "col_title", "col_desc", "col_h1", "col_lang",
                           "col_canonical", "col_og_image", "col_issues")]
    summary = " · ".join(f"{_sev(s, lang)}: {n}" for s, n in counts.items())
    out = [t("title", n=len(pages), counts=summary), md_table(head, rows)]
    detail = []
    for page in pages:
        for sev, msg in sorted(issues[page["url"]], key=lambda i: SEVERITIES.index(i[0])):
            detail.append(f"- **{_sev(sev, lang)}** {page['url']}: {msg}")
    out.append(t("h_detail") + "\n\n" + ("\n".join(detail) or t("no_issues")))
    return "\n\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit published SEO metadata per page (title, description, canonical, OG, h1, lang, hreflang, noindex).")
    parser.add_argument("target", help="sitemap.xml URL, text file with one URL per line, or a single page URL")
    parser.add_argument("--max", type=int, default=200, help="maximum pages to check (default 200)")
    parser.add_argument("--workers", type=int, default=6, help="parallel requests (default 6)")
    parser.add_argument("--timeout", type=float, default=15.0, help="seconds per request (default 15)")
    parser.add_argument("--json", action="store_true", help="print JSON instead of Markdown (keys stay in Spanish)")
    add_lang_arg(parser)
    args = parser.parse_args(argv)
    lang = resolve_lang(args.lang)
    t = make_translator(MESSAGES, lang)
    try:
        urls = resolve_targets(args.target, args.timeout, args.max, lang)
    except (RuntimeError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if not urls:
        print(t("no_urls"), file=sys.stderr)
        return 1
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        pages = list(pool.map(lambda u: extract(u, args.timeout), urls))
    dups = duplicate_issues(pages, lang)
    issues = {p["url"]: [*page_issues(p, lang), *dups.get(p["url"], [])] for p in pages}
    if args.json:
        print(json.dumps([{**p, "problemas": [{"severidad": _sev(s, lang), "mensaje": m} for s, m in issues[p["url"]]]}
                          for p in pages], ensure_ascii=False, indent=2))
    else:
        print(render_markdown(pages, issues, lang))
    return 1 if any(sev == "ERROR" for v in issues.values() for sev, _ in v) else 0


if __name__ == "__main__":
    sys.exit(main())
