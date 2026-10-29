#!/usr/bin/env python3
"""Verifica las URLs que citaron los asistentes: ¿siguen vivas y de verdad nombran al cliente?

Los asistentes inventan URLs y atribuyen a una página cosas que no dice
(ver references/medicion-citacion.md). Este script abre cada URL citada una
sola vez y la clasifica:

  viva-y-nombra     2xx y el HTML contiene el nombre buscado
  viva-no-nombra    2xx pero el nombre no está en el HTML servido
  bloqueo-anti-bot  403/429 o challenge (Cloudflare y similares); NO es un 404:
                    ábrela a mano en un navegador antes de darla por muerta
  muerta            404/410/5xx, DNS, conexión rechazada, más de 5 redirecciones
  timeout           no respondió dentro del --timeout

La búsqueda del nombre ignora acentos y mayúsculas. Ojo: si la página pinta el
nombre con JavaScript, aquí saldrá viva-no-nombra (eso mismo ve un bot que no
ejecuta JS). Nunca reintenta ni sigue más de 5 redirecciones.

Uso:
    python3 verificar_fuentes.py examples/corridas-ejemplo --nombre "Elena Ruiz"
    python3 verificar_fuentes.py examples/urls-ejemplo.txt --nombre "Example"
    python3 verificar_fuentes.py corridas/ --nombre "Elena Ruiz" --nombre "Dra. Ruiz" --ua ambos
    python3 verificar_fuentes.py runs/ --name "Elena Ruiz" --lang en

Lee corridas con frontmatter en español (urls_citadas) o en inglés (cited_urls).
Con --lang en las clases salen en inglés (alive-names, alive-no-name,
anti-bot-block, dead, timeout), también en el JSON; las claves del JSON no cambian.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import (BOT_UAS, UA_BROWSER, add_lang_arg, detect_challenge, error_label,  # noqa: E402
                    fetch, html_to_text, make_translator, md_table, normalize_run_fields,
                    normalize_text, parse_frontmatter, read_url_list, resolve_lang)

UA_CHOICES = {"browser": [("navegador", UA_BROWSER)],
              "gptbot": [("GPTBot", BOT_UAS["GPTBot"])],
              "ambos": [("navegador", UA_BROWSER), ("GPTBot", BOT_UAS["GPTBot"])],
              "both": [("navegador", UA_BROWSER), ("GPTBot", BOT_UAS["GPTBot"])]}
DEAD_STATUSES = {404, 410}
BLOCK_STATUSES = {401, 403, 429}
CLASS_EN = {"viva-y-nombra": "alive-names", "viva-no-nombra": "alive-no-name",
            "bloqueo-anti-bot": "anti-bot-block", "muerta": "dead", "timeout": "timeout"}

MESSAGES = {
    "es": {
        "ua_browser": "navegador",
        "title": "# Verificación de fuentes\n\nNombre buscado: {names} · {count} URLs únicas\n\n{summary}",
        "col_url": "URL", "col_ua": "UA", "col_status": "Status", "col_redirect": "Redirige a", "col_class": "Clase",
        "block_note": "`bloqueo-anti-bot` no es una fuente muerta: ábrela en un navegador real antes de concluir.",
        "h_warnings": "## Advertencias",
        "not_found": "error: no existe {path}",
        "no_urls": "error: no se encontraron URLs para verificar",
        "unreachable": "error: ninguna URL respondió; revisa la conexión del entorno",
    },
    "en": {
        "ua_browser": "browser",
        "title": "# Source check\n\nName searched: {names} · {count} unique URLs\n\n{summary}",
        "col_url": "URL", "col_ua": "UA", "col_status": "Status", "col_redirect": "Redirects to", "col_class": "Class",
        "block_note": "`anti-bot-block` is not a dead source: open it in a real browser before concluding.",
        "h_warnings": "## Warnings",
        "not_found": "error: {path} does not exist",
        "no_urls": "error: no URLs found to check",
        "unreachable": "error: no URL responded; check the network connection of this environment",
    },
}


def urls_from_runs(folder: Path, lang: str = "es") -> tuple[list[str], list[str]]:
    """Junta urls_citadas (o cited_urls) de todas las corridas, sin duplicados y en orden de aparición."""
    urls, warnings = [], []
    for path in sorted(folder.glob("*.md")):
        try:
            raw_fields, _ = parse_frontmatter(path.read_text(encoding="utf-8"), lang)
        except (ValueError, UnicodeDecodeError) as exc:
            warnings.append(f"{path.name}: {exc}")
            continue
        value = normalize_run_fields(raw_fields).get("urls_citadas") or []
        urls += [str(u) for u in (value if isinstance(value, list) else [value]) if u]
    return list(dict.fromkeys(urls)), warnings


def load_urls(source: Path, lang: str = "es") -> tuple[list[str], list[str]]:
    if source.is_dir():
        return urls_from_runs(source, lang)
    return list(dict.fromkeys(read_url_list(source))), []


def name_found(resp: dict, names: list[str]) -> bool:
    body = resp.get("body") or ""
    haystacks = (normalize_text(html_to_text(body)), normalize_text(body))
    return any(normalize_text(n) in hay for n in names for hay in haystacks)


def classify(resp: dict, names: list[str]) -> str:
    if resp["error"] == "timeout":
        return "timeout"
    if resp["error"]:
        return "muerta"
    status = resp["status"] or 0
    if status in BLOCK_STATUSES or detect_challenge(resp):
        return "bloqueo-anti-bot"
    if status in DEAD_STATUSES or status >= 400:
        return "muerta"
    if 200 <= status < 300:
        return "viva-y-nombra" if name_found(resp, names) else "viva-no-nombra"
    return "muerta"


def _class_label(clase: str, lang: str) -> str:
    return CLASS_EN.get(clase, clase) if lang == "en" else clase


def check_url(url: str, names: list[str], uas: list[tuple[str, str]], timeout: float, lang: str = "es") -> dict:
    t = make_translator(MESSAGES, lang)
    results = []
    for label, ua in uas:
        resp = fetch(url, ua=ua, timeout=timeout)
        results.append({"ua": t("ua_browser") if label == "navegador" else label, "status": resp["status"],
                        "final_url": resp["final_url"], "redirecciones": len(resp["redirects"]),
                        "error": resp["error"], "clase": _class_label(classify(resp, names), lang)})
    return {"url": url, "resultados": results}


def render_markdown(rows: list[dict], names: list[str], warnings: list[str], lang: str = "es") -> str:
    t = make_translator(MESSAGES, lang)
    table = []
    for row in rows:
        for res in row["resultados"]:
            final = res["final_url"] if res["final_url"] != row["url"] else ""
            status = res["status"] if res["status"] is not None else error_label(res["error"], lang)
            table.append([row["url"], res["ua"], status, final, res["clase"]])
    counts: dict = {}
    for row in rows:
        clase = row["resultados"][0]["clase"]
        counts[clase] = counts.get(clase, 0) + 1
    summary = " · ".join(f"{k}: {v}" for k, v in sorted(counts.items()))
    head = [t("col_url"), t("col_ua"), t("col_status"), t("col_redirect"), t("col_class")]
    out = [t("title", names=", ".join(names), count=len(rows), summary=summary),
           md_table(head, table), t("block_note")]
    if warnings:
        out.append(t("h_warnings") + "\n\n" + "\n".join(f"- {w}" for w in warnings))
    return "\n\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check cited URLs: alive or dead, anti-bot block, and whether the page names the client.")
    parser.add_argument("source", type=Path, help="folder of run files (*.md) or a text file with one URL per line")
    parser.add_argument("--nombre", "--name", dest="nombre", action="append", required=True,
                        help="text to look for (accent and case insensitive); repeat for variants")
    parser.add_argument("--ua", choices=sorted(UA_CHOICES), default="browser",
                        help="User-Agent: browser (default), gptbot, or both (alias ambos) to compare both")
    parser.add_argument("--timeout", type=float, default=15.0, help="seconds per request (default 15)")
    parser.add_argument("--json", action="store_true", help="print JSON instead of Markdown (keys stay in Spanish)")
    add_lang_arg(parser)
    args = parser.parse_args(argv)
    lang = resolve_lang(args.lang)
    t = make_translator(MESSAGES, lang)
    if not args.source.exists():
        print(t("not_found", path=args.source), file=sys.stderr)
        return 1
    urls, warnings = load_urls(args.source, lang)
    if not urls:
        print(t("no_urls"), file=sys.stderr)
        return 1
    rows = [check_url(u, args.nombre, UA_CHOICES[args.ua], args.timeout, lang) for u in urls]
    if args.json:
        print(json.dumps({"nombre": args.nombre, "urls": rows, "advertencias": warnings}, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(rows, args.nombre, warnings, lang))
    unreachable = all(r["resultados"][0]["error"] not in (None, "demasiadas-redirecciones") for r in rows)
    if unreachable:
        print(t("unreachable"), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
