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
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import (BOT_UAS, UA_BROWSER, detect_challenge, fetch, html_to_text,  # noqa: E402
                    md_table, normalize_text, parse_frontmatter, read_url_list)

UA_CHOICES = {"browser": [("navegador", UA_BROWSER)],
              "gptbot": [("GPTBot", BOT_UAS["GPTBot"])],
              "ambos": [("navegador", UA_BROWSER), ("GPTBot", BOT_UAS["GPTBot"])]}
DEAD_STATUSES = {404, 410}
BLOCK_STATUSES = {401, 403, 429}


def urls_from_runs(folder: Path) -> tuple[list[str], list[str]]:
    """Junta urls_citadas de todas las corridas, sin duplicados y en orden de aparición."""
    urls, warnings = [], []
    for path in sorted(folder.glob("*.md")):
        try:
            fields, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        except (ValueError, UnicodeDecodeError) as exc:
            warnings.append(f"{path.name}: {exc}")
            continue
        value = fields.get("urls_citadas") or []
        urls += [str(u) for u in (value if isinstance(value, list) else [value]) if u]
    return list(dict.fromkeys(urls)), warnings


def load_urls(source: Path) -> tuple[list[str], list[str]]:
    if source.is_dir():
        return urls_from_runs(source)
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


def check_url(url: str, names: list[str], uas: list[tuple[str, str]], timeout: float) -> dict:
    results = []
    for label, ua in uas:
        resp = fetch(url, ua=ua, timeout=timeout)
        results.append({"ua": label, "status": resp["status"], "final_url": resp["final_url"],
                        "redirecciones": len(resp["redirects"]), "error": resp["error"],
                        "clase": classify(resp, names)})
    return {"url": url, "resultados": results}


def render_markdown(rows: list[dict], names: list[str], warnings: list[str]) -> str:
    table = []
    for row in rows:
        for res in row["resultados"]:
            final = res["final_url"] if res["final_url"] != row["url"] else ""
            status = res["status"] if res["status"] is not None else res["error"]
            table.append([row["url"], res["ua"], status, final, res["clase"]])
    counts: dict = {}
    for row in rows:
        clase = row["resultados"][0]["clase"]
        counts[clase] = counts.get(clase, 0) + 1
    summary = " · ".join(f"{k}: {v}" for k, v in sorted(counts.items()))
    out = [f"# Verificación de fuentes\n\nNombre buscado: {', '.join(names)} · {len(rows)} URLs únicas\n\n{summary}",
           md_table(["URL", "UA", "Status", "Redirige a", "Clase"], table),
           "`bloqueo-anti-bot` no es una fuente muerta: ábrela en un navegador real antes de concluir."]
    if warnings:
        out.append("## Advertencias\n\n" + "\n".join(f"- {w}" for w in warnings))
    return "\n\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check cited URLs: alive or dead, anti-bot block, and whether the page names the client.")
    parser.add_argument("source", type=Path, help="folder of run files (*.md) or a text file with one URL per line")
    parser.add_argument("--nombre", action="append", required=True,
                        help="text to look for (accent and case insensitive); repeat for variants")
    parser.add_argument("--ua", choices=sorted(UA_CHOICES), default="browser",
                        help="User-Agent: browser (default), gptbot, or ambos to compare both")
    parser.add_argument("--timeout", type=float, default=15.0, help="seconds per request (default 15)")
    parser.add_argument("--json", action="store_true", help="print JSON instead of Markdown")
    args = parser.parse_args(argv)
    if not args.source.exists():
        print(f"error: no existe {args.source}", file=sys.stderr)
        return 1
    urls, warnings = load_urls(args.source)
    if not urls:
        print("error: no se encontraron URLs para verificar", file=sys.stderr)
        return 1
    rows = [check_url(u, args.nombre, UA_CHOICES[args.ua], args.timeout) for u in urls]
    if args.json:
        print(json.dumps({"nombre": args.nombre, "urls": rows, "advertencias": warnings}, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(rows, args.nombre, warnings))
    unreachable = all(r["resultados"][0]["error"] not in (None, "demasiadas-redirecciones") for r in rows)
    if unreachable:
        print("error: ninguna URL respondió; revisa la conexión del entorno", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
