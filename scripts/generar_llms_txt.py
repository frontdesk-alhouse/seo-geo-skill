#!/usr/bin/env python3
"""Borrador de llms.txt a partir del sitemap: para curar a mano, no para publicar tal cual.

Lee sitemap.xml (y sitemap index), toma de cada URL el <title> y la meta
description (o el primer párrafo si falta), agrupa por primer segmento de ruta
o por --secciones, y emite un borrador con la forma de
templates/llms.txt.template. El resumen, el contexto y las Notas para modelos
salen con TODO: eso lo escribe una persona que conoce la marca.

Encuadre honesto: ningún motor confirma usar llms.txt (references/llms-txt.md).
Es una cortesía barata, no una palanca de citación.

Uso:
    python3 generar_llms_txt.py https://www.ejemplo.mx/sitemap.xml --max 40
    python3 generar_llms_txt.py ejemplo.mx --secciones "servicios:/servicios,/precios" "empresa:/nosotros,/contacto"
    python3 generar_llms_txt.py https://www.ejemplo.mx/sitemap.xml --salida llms-borrador.txt
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import fetch, meta_content, parse_html, read_sitemap  # noqa: E402

ORG_TYPES = {"Organization", "Corporation", "LocalBusiness", "MedicalBusiness", "Physician",
             "MedicalClinic", "RealEstateAgent", "ProfessionalService", "WebSite"}

OPTIONAL_SEGMENTS = {"blog", "news", "noticias", "articulos", "recursos", "resources", "careers",
                     "empleo", "vacantes", "legal", "privacy", "privacidad", "terms", "terminos",
                     "aviso-de-privacidad", "cookies", "changelog", "press", "prensa"}
LOCALE_RE = re.compile(r"^[a-z]{2}(-[a-z]{2})?$", re.IGNORECASE)
TITLE_SEPARATORS = (" | ", " - ", " · ", " \u2013 ", " \u2014 ")  # barra, guion, punto medio, guiones tipográficos


def sitemap_url(target: str) -> str:
    if re.match(r"^https?://", target):
        return target
    return f"https://{target.strip('/')}/sitemap.xml"


def parse_sections(specs: list[str]) -> list[tuple[str, list[str]]]:
    """'nombre:/a,/b' → [('nombre', ['/a', '/b'])]."""
    sections = []
    for spec in specs:
        if ":" not in spec:
            raise ValueError(f"--secciones espera 'nombre:/ruta1,/ruta2', recibí {spec!r}")
        name, paths = spec.split(":", 1)
        sections.append((name.strip(), [p.strip().rstrip("/") or "/" for p in paths.split(",") if p.strip()]))
    return sections


def clean_title(title: str, brand: str | None) -> str:
    for sep in TITLE_SEPARATORS:
        parts = [p.strip() for p in title.split(sep) if p.strip()]
        if len(parts) > 1:
            useful = [p for p in parts if not brand or p.lower() != brand.lower()]
            return useful[0] if useful else parts[0]
    return title.strip()


def page_info(url: str, timeout: float) -> dict:
    resp = fetch(url, timeout=timeout)
    page = parse_html(resp["body"])
    desc = meta_content(page, "description") or page.first_p
    return {"url": url, "status": resp["status"], "title": page.title,
            "site_name": meta_content(page, "og:site_name"), "description": (desc or "").strip(),
            "lang": page.lang, "org_name": org_name(page.jsonld)}


def org_name(blocks: list[str]) -> str | None:
    """Primer 'name' de un nodo Organization (o similar) en el JSON-LD de la página."""
    def walk(node):
        if isinstance(node, list):
            return next((n for n in map(walk, node) if n), None)
        if not isinstance(node, dict):
            return None
        types = node.get("@type")
        types = set(types) if isinstance(types, list) else {types}
        if types & ORG_TYPES and isinstance(node.get("name"), str):
            return node["name"]
        return walk(node.get("@graph", []))
    for block in blocks:
        try:
            found = walk(json.loads(block))
        except json.JSONDecodeError:
            continue
        if found:
            return found
    return None


def brand_name(home: dict | None, source: str) -> str:
    """Organization del JSON-LD, luego og:site_name, luego la parte corta del title, luego el dominio."""
    home = home or {}
    if home.get("org_name") or home.get("site_name"):
        return home.get("org_name") or home["site_name"]
    title = home.get("title") or ""
    for sep in TITLE_SEPARATORS:
        if sep in title:
            return min((p.strip() for p in title.split(sep) if p.strip()), key=len)
    host = urllib.parse.urlparse(source).netloc.lower().removeprefix("www.")
    return host.split(".")[0].capitalize() or "TODO: marca"


def section_for(path: str, sections: list[tuple[str, list[str]]]) -> str:
    for name, prefixes in sections:
        if any(path == p or (p != "/" and path.startswith(p + "/")) for p in prefixes):
            return name
    segments = [s for s in path.split("/") if s]
    first = segments[0].lower() if segments else ""
    if first in OPTIONAL_SEGMENTS:
        return "Opcional"
    return first.replace("-", " ").capitalize() if first else "Inicio"


def group_pages(pages: list[dict], sections: list[tuple[str, list[str]]]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {}
    for page in pages:
        path = urllib.parse.urlparse(page["url"]).path.rstrip("/") or "/"
        name = section_for(path, sections)
        groups[name] = [*groups.get(name, []), page]
    ordered = [n for n, _ in sections if n in groups]
    rest = sorted(n for n in groups if n not in ordered and n not in ("Inicio", "Opcional"))
    tail = ["Opcional"] if "Opcional" in groups else []
    return {n: groups[n] for n in [*ordered, *rest, *tail]}


def _one_line(text: str, limit: int = 180) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text if len(text) <= limit else text[: limit - 3].rsplit(" ", 1)[0] + "..."


def render(home: dict | None, groups: dict[str, list[dict]], brand: str, source: str) -> str:
    lang = (home or {}).get("lang") or "TODO"
    lines = [f"<!-- BORRADOR generado por generar_llms_txt.py desde {source}.",
             "     Cúralo a mano antes de publicar: reescribe resumen y contexto, quita páginas",
             "     que no ayudan a entender la marca, revisa cada descripción y llena las Notas. -->",
             "", f"# {brand}", "",
             "> TODO: resumen de 2-3 frases. Qué hace, para quién y el resultado concreto.", "",
             "TODO: contexto. Qué es, para quién, qué NO es, categoría, fundadores o responsable. "
             f"Idioma del sitio: {lang}.", ""]
    for name, pages in groups.items():
        if name == "Inicio":
            continue
        lines += [f"## {name}", ""]
        lines += [f"- [{p['titulo']}]({p['url']}): {_one_line(p['description']) or 'TODO: descripción de una línea.'}"
                  for p in pages]
        lines.append("")
    lines += ["## Notas para modelos de lenguaje", "",
              "- TODO: cómo citar la postura de la marca (la frase exacta que debe repetirse).",
              "- TODO: qué NO atribuir (logos de clientes, cifras o resultados que el sitio no publica).",
              "- TODO: vigencia de precios (válidos solo como aparecen en la página de precios al momento de leerla).", ""]
    return "\n".join(lines)


def filter_urls(urls: list[str], keep_locales: bool) -> list[str]:
    if keep_locales:
        return urls
    def first_segment(u: str) -> str:
        segs = [s for s in urllib.parse.urlparse(u).path.split("/") if s]
        return segs[0] if segs else ""
    return [u for u in urls if not LOCALE_RE.match(first_segment(u))]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Draft an llms.txt from sitemap.xml (titles + meta descriptions) for manual curation.")
    parser.add_argument("target", help="sitemap.xml URL or bare domain (https://<domain>/sitemap.xml is assumed)")
    parser.add_argument("--max", type=int, default=60, help="maximum pages to include (default 60)")
    parser.add_argument("--secciones", nargs="*", default=[], metavar="NAME:/path1,/path2",
                        help="explicit sections by path prefix; the rest groups by first path segment")
    parser.add_argument("--incluir-idiomas", action="store_true", help="keep locale-prefixed URLs such as /es/ or /en-us/")
    parser.add_argument("--timeout", type=float, default=15.0, help="seconds per request (default 15)")
    parser.add_argument("--salida", type=Path, help="write the draft to this file instead of stdout")
    parser.add_argument("--json", action="store_true", help="print the collected pages as JSON")
    args = parser.parse_args(argv)
    try:
        sections = parse_sections(args.secciones)
        source = sitemap_url(args.target)
        urls = filter_urls(read_sitemap(source, args.timeout, limit=1000), args.incluir_idiomas)[: args.max]
    except (ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if not urls:
        print("error: el sitemap no tiene URLs utilizables", file=sys.stderr)
        return 1
    with ThreadPoolExecutor(max_workers=6) as pool:
        infos = [i for i in pool.map(lambda u: page_info(u, args.timeout), urls) if i["status"] == 200]
    home = next((i for i in infos if (urllib.parse.urlparse(i["url"]).path.rstrip("/") or "/") == "/"), None)
    brand = brand_name(home, source)
    pages = [{**i, "titulo": clean_title(i["title"] or i["url"], brand)} for i in infos]
    if args.json:
        print(json.dumps({"fuente": source, "marca": brand, "paginas": pages}, ensure_ascii=False, indent=2))
        return 0
    draft = render(home, group_pages(pages, sections), brand, source)
    if args.salida:
        args.salida.write_text(draft, encoding="utf-8")
        print(f"borrador escrito en {args.salida} ({len(pages)} páginas)")
    else:
        print(draft)
    return 0


if __name__ == "__main__":
    sys.exit(main())
