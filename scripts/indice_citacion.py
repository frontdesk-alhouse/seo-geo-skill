#!/usr/bin/env python3
"""Índice de Citación a partir de corridas manuales en asistentes de IA.

Lee una carpeta de corridas (*.md) escritas con templates/corrida.template.md
y produce, en Markdown (o JSON con --json):

  1. Índice de Citación por consulta x asistente: k/n (posiciones) y total.
  2. Subtotal sin marca por asistente y global, con intervalo de Wilson al 95 %.
  3. Primer lugar por asistente (consultas sin marca).
  4. Tasa de disparo: proporción de corridas en que el asistente buscó en la web.
  5. Lectura por tipo de consulta y por familia.
  6. Censo de fuentes: dominio, corridas que lo citan, en cuántas aparece el cliente.
  7. Cifras pegadas al nombre (dato erróneo que el asistente asocia al cliente).
  8. Advertencias: corridas faltantes, campos inválidos, consultas sin histórico.

Las consultas de marca (familia F3 o las listadas en --marca) se reportan
aparte y nunca entran al subtotal sin marca.

Método completo: references/medicion-citacion.md

Acepta corridas con frontmatter en español o en inglés (query, family,
query_type, assistant...; ver _comun.RUN_KEYS_EN). La salida sale en el idioma
de --lang; el JSON conserva sus claves en español en los dos idiomas.

Uso:
    python3 indice_citacion.py examples/corridas-ejemplo
    python3 indice_citacion.py corridas/ --marca Q-07 Q-08 --n-esperado 3
    python3 indice_citacion.py corridas/ --json > indice.json
    python3 indice_citacion.py runs/ --brand Q-07 --expected-n 3 --lang en
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import (QUERY_TYPES_ES_TO_EN, RUN_KEYS_ES_TO_EN, add_lang_arg, fmt_prop,  # noqa: E402
                    make_translator, md_table, normalize_run_fields, parse_frontmatter,
                    resolve_lang, wilson_interval)

ASISTENTES = ("chatgpt", "gemini", "claude", "perplexity", "aio", "aimode", "copilot")
ORIGENES = ("ui", "api")
TIPOS = ("informacional", "local", "transaccional")
FAMILIAS = ("F1", "F2", "F3", "F4", "F5", "F6")
REQUIRED = ("consulta", "familia", "tipo_consulta", "asistente", "origen", "corrida",
            "fecha", "modo", "busco", "aparece", "posicion", "nombres", "urls_citadas",
            "cifra_pegada", "notas")

MESSAGES = {
    "es": {
        "missing_field": "falta el campo '{field}'",
        "bad_query": "consulta debe ser un id tipo Q-NN o A-NN",
        "bad_family": "familia debe ser una de {opts}",
        "bad_type": "tipo_consulta debe ser una de {opts}",
        "bad_assistant": "asistente debe ser uno de {opts}",
        "bad_origin": "origen debe ser ui o api",
        "bad_run": "corrida debe ser entero >= 1",
        "bad_date": "fecha debe ser ISO (AAAA-MM-DD)",
        "bad_searched": "busco debe ser true o false",
        "bad_appears": "aparece debe ser true o false",
        "bad_position": "posicion debe ser entero o null",
        "appears_false_pos": "aparece es false pero posicion tiene valor",
        "fm_unreadable": "{file}: no se pudo leer el frontmatter ({exc})",
        "run_discarded": "{file}: corrida descartada; {problems}",
        "repeated_run": "{query} / {assistant}: número de corrida repetido {numbers}",
        "few_runs": "{query} / {assistant}: {got} de {expected} corridas esperadas",
        "missing_combos": "combinaciones sin ninguna corrida (si fue deliberado, ignora): {combos}",
        "no_history": "{query}: sin histórico (alta {start}, posterior a la primera corrida)",
        "appears_no_pos": "{file}: aparece sin posicion (¿respuesta en prosa sin orden?)",
        "searched_no_urls": "{file}: busco=true pero sin urls_citadas",
        "no_verbatim": "{file}: falta la sección '## Verbatim'",
        "title": ("# Índice de Citación\n\n{runs} corridas · {first} a {last} · "
                  "celdas `k/n (posiciones)`; proporciones con intervalo de Wilson al 95 %.\n"),
        "branded_suffix": " (marca)",
        "h_by_query": "## 1. Por consulta y asistente",
        "col_query": "Consulta", "col_family_short": "Fam.", "col_type": "Tipo", "col_total": "Total",
        "h_unbranded": "## 2. Subtotal sin marca",
        "col_assistant": "Asistente", "col_appears": "Aparece",
        "branded_note": "Consultas de marca (aparte, no suman al subtotal):",
        "h_first": "## 3. Primer lugar (sin marca)", "col_first": "Primer lugar",
        "h_trigger": "## 4. Tasa de disparo (buscó en la web)", "col_searched": "Buscó",
        "h_breakdown": "## 5. Lectura por tipo de consulta (sin marca) y por familia", "col_family": "Familia",
        "h_census": "## 6. Censo de fuentes", "census_empty": "Ninguna corrida citó URLs.",
        "col_domain": "Dominio", "col_cited": "Corridas que lo citan", "col_with_client": "Con cliente",
        "col_urls": "URLs",
        "census_note": ("Viva/muerta y si nombra al cliente: corre `verificar_fuentes.py` sobre la misma carpeta. "
                        "Propia/tercero: márcalo a mano en el reporte."),
        "h_figures": "## 7. Cifras pegadas", "figures_empty": "Ninguna registrada.",
        "col_run": "Corrida", "col_date": "Fecha", "col_claim": "Cifra",
        "h_warnings": "## 8. Advertencias", "none": "Ninguna.",
        "overall": "global",
        "not_dir": "error: {path} no es una carpeta",
        "no_valid": "error: ninguna corrida válida.",
    },
    "en": {
        "missing_field": "missing field '{field}'",
        "bad_query": "query must be an id like Q-NN or A-NN",
        "bad_family": "family must be one of {opts}",
        "bad_type": "query_type must be one of {opts}",
        "bad_assistant": "assistant must be one of {opts}",
        "bad_origin": "origin must be ui or api",
        "bad_run": "run must be an integer >= 1",
        "bad_date": "date must be ISO (YYYY-MM-DD)",
        "bad_searched": "searched must be true or false",
        "bad_appears": "appears must be true or false",
        "bad_position": "position must be an integer or null",
        "appears_false_pos": "appears is false but position has a value",
        "fm_unreadable": "{file}: could not read the frontmatter ({exc})",
        "run_discarded": "{file}: run discarded; {problems}",
        "repeated_run": "{query} / {assistant}: repeated run number {numbers}",
        "few_runs": "{query} / {assistant}: {got} of {expected} expected runs",
        "missing_combos": "combinations with no runs at all (ignore if deliberate): {combos}",
        "no_history": "{query}: no history (added {start}, after the first run)",
        "appears_no_pos": "{file}: appears without position (prose answer with no order?)",
        "searched_no_urls": "{file}: searched=true but no cited_urls",
        "no_verbatim": "{file}: missing the '## Verbatim' section",
        "title": ("# Citation Index\n\n{runs} runs · {first} to {last} · "
                  "cells `k/n (positions)`; proportions with a 95% Wilson interval.\n"),
        "branded_suffix": " (branded)",
        "h_by_query": "## 1. By query and assistant",
        "col_query": "Query", "col_family_short": "Fam.", "col_type": "Type", "col_total": "Total",
        "h_unbranded": "## 2. Unbranded subtotal",
        "col_assistant": "Assistant", "col_appears": "Appears",
        "branded_note": "Branded queries (reported separately, not added to the subtotal):",
        "h_first": "## 3. First place (unbranded)", "col_first": "First place",
        "h_trigger": "## 4. Trigger rate (searched the web)", "col_searched": "Searched",
        "h_breakdown": "## 5. Reading by query type (unbranded) and by family", "col_family": "Family",
        "h_census": "## 6. Source census", "census_empty": "No run cited URLs.",
        "col_domain": "Domain", "col_cited": "Runs citing it", "col_with_client": "With client",
        "col_urls": "URLs",
        "census_note": ("Alive/dead and whether it names the client: run `verificar_fuentes.py` on the same folder. "
                        "Owned/third party: mark it by hand in the report."),
        "h_figures": "## 7. Stuck claims", "figures_empty": "None recorded.",
        "col_run": "Run", "col_date": "Date", "col_claim": "Claim",
        "h_warnings": "## 8. Warnings", "none": "None.",
        "overall": "overall",
        "not_dir": "error: {path} is not a folder",
        "no_valid": "error: no valid runs.",
    },
}


def _tr(lang: str):
    return make_translator(MESSAGES, lang)


def _field(key: str, lang: str) -> str:
    """Nombre del campo como lo escribe el usuario en ese idioma."""
    return RUN_KEYS_ES_TO_EN.get(key, key) if lang == "en" else key


def _qtype(value: str, lang: str) -> str:
    return QUERY_TYPES_ES_TO_EN.get(value, value) if lang == "en" else value


# ---------------------------------------------------------------- lectura y validación

def _parse_fecha(value) -> date | None:
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).date()
    except ValueError:
        try:
            return date.fromisoformat(str(value))
        except ValueError:
            return None


def _as_list(value) -> list:
    if value is None:
        return []
    return list(value) if isinstance(value, list) else [value]


def validate_run(fields: dict, lang: str = "es") -> list[str]:
    """Devuelve la lista de problemas del frontmatter (vacía si es válido). Espera claves internas."""
    t = _tr(lang)
    types = tuple(_qtype(x, lang) for x in TIPOS)
    errors = [t("missing_field", field=_field(k, lang)) for k in REQUIRED if k not in fields]
    checks = [
        (re.fullmatch(r"[A-Za-z]{1,4}-\d+", str(fields.get("consulta", ""))), t("bad_query")),
        (fields.get("familia") in FAMILIAS, t("bad_family", opts=FAMILIAS)),
        (fields.get("tipo_consulta") in TIPOS, t("bad_type", opts=types)),
        (fields.get("asistente") in ASISTENTES, t("bad_assistant", opts=ASISTENTES)),
        (fields.get("origen") in ORIGENES, t("bad_origin")),
        (isinstance(fields.get("corrida"), int) and fields["corrida"] >= 1, t("bad_run")),
        (_parse_fecha(fields.get("fecha")) is not None, t("bad_date")),
        (isinstance(fields.get("busco"), bool), t("bad_searched")),
        (isinstance(fields.get("aparece"), bool), t("bad_appears")),
        (fields.get("posicion") is None or isinstance(fields.get("posicion"), int), t("bad_position")),
    ]
    errors += [msg for ok, msg in checks if not ok]
    if fields.get("aparece") is False and isinstance(fields.get("posicion"), int):
        errors.append(t("appears_false_pos"))
    return errors


def load_runs(folder: Path, lang: str = "es") -> tuple[list[dict], list[str]]:
    """Lee *.md de la carpeta (frontmatter en español o inglés). Devuelve (corridas válidas, advertencias)."""
    t = _tr(lang)
    runs, warnings = [], []
    for path in sorted(folder.glob("*.md")):
        try:
            raw_fields, body = parse_frontmatter(path.read_text(encoding="utf-8"), lang)
        except (ValueError, UnicodeDecodeError) as exc:
            warnings.append(t("fm_unreadable", file=path.name, exc=exc))
            continue
        fields = normalize_run_fields(raw_fields)
        problems = validate_run(fields, lang)
        if problems:
            warnings.append(t("run_discarded", file=path.name, problems="; ".join(problems)))
            continue
        runs.append({**fields, "archivo": path.name, "fecha": _parse_fecha(fields["fecha"]),
                     "nombres": _as_list(fields["nombres"]),
                     "urls_citadas": [u for u in _as_list(fields["urls_citadas"]) if u],
                     "tiene_verbatim": "## Verbatim" in body})
    return runs, warnings


# ---------------------------------------------------------------- cálculo

def is_brand(run: dict, brand_ids: set[str]) -> bool:
    return run["familia"] == "F3" or run["consulta"] in brand_ids


def group_by(runs: list[dict], *keys: str) -> dict:
    groups: dict = defaultdict(list)
    for run in runs:
        groups[tuple(run[k] for k in keys)].append(run)
    return dict(groups)


def proportion(runs: list[dict], predicate) -> dict:
    k, n = sum(1 for r in runs if predicate(r)), len(runs)
    lo, hi = wilson_interval(k, n)
    return {"k": k, "n": n, "p": round(k / n, 4) if n else None,
            "wilson95": [round(lo, 4), round(hi, 4)], "texto": fmt_prop(k, n)}


def index_matrix(runs: list[dict], assistants: list[str], brand_ids: set[str]) -> list[dict]:
    """Fila por consulta con celdas k/n (posiciones) por asistente."""
    rows = []
    for (consulta,), qruns in sorted(group_by(runs, "consulta").items(), key=lambda kv: _qnum(kv[0][0])):
        cells = {}
        for name in assistants:
            aruns = [r for r in qruns if r["asistente"] == name]
            hits = [r for r in aruns if r["aparece"]]
            cells[name] = {"k": len(hits), "n": len(aruns),
                           "posiciones": sorted(r["posicion"] for r in hits if r["posicion"] is not None)}
        first = qruns[0]
        rows.append({"consulta": consulta, "familia": first["familia"], "tipo_consulta": first["tipo_consulta"],
                     "marca": is_brand(first, brand_ids), "celdas": cells,
                     "total": proportion(qruns, lambda r: r["aparece"])})
    return rows


def _qnum(consulta: str) -> int:
    return int(consulta.split("-")[1])


def per_assistant(runs: list[dict], assistants: list[str], predicate) -> dict:
    result = {a: proportion([r for r in runs if r["asistente"] == a], predicate) for a in assistants}
    return {**result, "global": proportion(runs, predicate)}


def breakdown(runs: list[dict], key: str) -> dict:
    return {value: proportion(rs, lambda r: r["aparece"])
            for (value,), rs in sorted(group_by(runs, key).items())}


def _domain(url: str) -> str:
    host = urllib.parse.urlparse(str(url)).netloc.lower()
    return host[4:] if host.startswith("www.") else host or str(url)


def source_census(runs: list[dict]) -> list[dict]:
    """Dominio → corridas que lo citan, en cuántas aparece el cliente, URLs."""
    census: dict = {}
    for run in runs:
        for dom in sorted({_domain(u) for u in run["urls_citadas"]}):
            entry = census.get(dom, {"dominio": dom, "corridas": 0, "con_cliente": 0, "urls": []})
            urls = [u for u in run["urls_citadas"] if _domain(u) == dom]
            census[dom] = {**entry, "corridas": entry["corridas"] + 1,
                           "con_cliente": entry["con_cliente"] + int(run["aparece"]),
                           "urls": sorted(set(entry["urls"]) | set(urls))}
    return sorted(census.values(), key=lambda e: (-e["corridas"], e["dominio"]))


def stuck_figures(runs: list[dict]) -> list[dict]:
    return [{"consulta": r["consulta"], "asistente": r["asistente"], "corrida": r["corrida"],
             "fecha": r["fecha"].isoformat(), "cifra": r["cifra_pegada"], "archivo": r["archivo"]}
            for r in sorted(runs, key=lambda r: (_qnum(r["consulta"]), r["asistente"], r["corrida"]))
            if r.get("cifra_pegada")]


# ---------------------------------------------------------------- advertencias

def coverage_warnings(runs: list[dict], n_expected: int, assistants: list[str], lang: str = "es") -> list[str]:
    t = _tr(lang)
    warnings = []
    for (consulta, asistente), rs in sorted(group_by(runs, "consulta", "asistente").items()):
        numbers = [r["corrida"] for r in rs]
        if len(set(numbers)) != len(numbers):
            warnings.append(t("repeated_run", query=consulta, assistant=asistente, numbers=sorted(numbers)))
        if len(rs) < n_expected:
            warnings.append(t("few_runs", query=consulta, assistant=asistente, got=len(rs), expected=n_expected))
    present = {(r["consulta"], r["asistente"]) for r in runs}
    missing = [f"{q}/{a}" for q in sorted({r["consulta"] for r in runs}, key=_qnum)
               for a in assistants if (q, a) not in present]
    if missing:
        warnings.append(t("missing_combos", combos=", ".join(missing)))
    return warnings


def quality_warnings(runs: list[dict], lang: str = "es") -> list[str]:
    t = _tr(lang)
    warnings = []
    first_date = min(r["fecha"] for r in runs)
    for (consulta,), rs in sorted(group_by(runs, "consulta").items(), key=lambda kv: _qnum(kv[0][0])):
        start = min(r["fecha"] for r in rs)
        if start > first_date:
            warnings.append(t("no_history", query=consulta, start=start.isoformat()))
    for r in runs:
        if r["aparece"] and r["posicion"] is None:
            warnings.append(t("appears_no_pos", file=r["archivo"]))
        if r["busco"] and not r["urls_citadas"]:
            warnings.append(t("searched_no_urls", file=r["archivo"]))
        if not r["tiene_verbatim"]:
            warnings.append(t("no_verbatim", file=r["archivo"]))
    return warnings


# ---------------------------------------------------------------- salida

def build_report(runs: list[dict], warnings: list[str], brand_ids: set[str], n_expected: int,
                 lang: str = "es") -> dict:
    assistants = [a for a in ASISTENTES if any(r["asistente"] == a for r in runs)]
    unbranded = [r for r in runs if not is_brand(r, brand_ids)]
    branded = [r for r in runs if is_brand(r, brand_ids)]
    return {
        "corridas": len(runs), "asistentes": assistants,
        "fechas": [min(r["fecha"] for r in runs).isoformat(), max(r["fecha"] for r in runs).isoformat()],
        "indice": index_matrix(runs, assistants, brand_ids),
        "sin_marca": per_assistant(unbranded, assistants, lambda r: r["aparece"]),
        "marca": per_assistant(branded, assistants, lambda r: r["aparece"]),
        "primer_lugar": per_assistant(unbranded, assistants, lambda r: r["aparece"] and r["posicion"] == 1),
        "tasa_disparo": per_assistant(runs, assistants, lambda r: r["busco"]),
        "por_tipo_consulta": breakdown(unbranded, "tipo_consulta"),
        "por_familia": breakdown(runs, "familia"),
        "censo_fuentes": source_census(runs),
        "cifras_pegadas": stuck_figures(runs),
        "advertencias": [*warnings, *coverage_warnings(runs, n_expected, assistants, lang),
                         *quality_warnings(runs, lang)],
    }


def _cell(cell: dict) -> str:
    if cell["n"] == 0:
        return "·"
    pos = f" ({', '.join(map(str, cell['posiciones']))})" if cell["posiciones"] else ""
    return f"{cell['k']}/{cell['n']}{pos}"


def _prop_rows(block: dict, assistants: list[str], overall: str) -> list[list[str]]:
    return [[overall if a == "global" else a, block[a]["texto"]]
            for a in [*assistants, "global"] if block[a]["n"]]


def _section(heading: str, body: str) -> str:
    return f"{heading}\n\n{body}"


def render_markdown(rep: dict, lang: str = "es") -> str:
    t = _tr(lang)
    a = rep["asistentes"]
    ov = t("overall")
    out = [t("title", runs=rep["corridas"], first=rep["fechas"][0], last=rep["fechas"][1])]
    rows = [[r["consulta"] + (t("branded_suffix") if r["marca"] else ""), r["familia"], _qtype(r["tipo_consulta"], lang),
             *[_cell(r["celdas"][x]) for x in a], r["total"]["texto"]] for r in rep["indice"]]
    head = [t("col_query"), t("col_family_short"), t("col_type"), *a, t("col_total")]
    out.append(_section(t("h_by_query"), md_table(head, rows)))
    appears = [t("col_assistant"), t("col_appears")]
    out.append(_section(t("h_unbranded"), md_table(appears, _prop_rows(rep["sin_marca"], a, ov))))
    if rep["marca"]["global"]["n"]:
        out.append(_section(t("branded_note"), md_table(appears, _prop_rows(rep["marca"], a, ov))))
    out.append(_section(t("h_first"), md_table([t("col_assistant"), t("col_first")],
                                               _prop_rows(rep["primer_lugar"], a, ov))))
    out.append(_section(t("h_trigger"), md_table([t("col_assistant"), t("col_searched")],
                                                 _prop_rows(rep["tasa_disparo"], a, ov))))
    by_type = [[_qtype(k, lang), v["texto"]] for k, v in rep["por_tipo_consulta"].items()]
    by_family = [[k, v["texto"]] for k, v in rep["por_familia"].items()]
    out.append(_section(t("h_breakdown"), md_table([t("col_type"), t("col_appears")], by_type)
                        + "\n\n" + md_table([t("col_family"), t("col_appears")], by_family)))
    out.append(_render_census(rep["censo_fuentes"], t))
    out.append(_render_figures(rep["cifras_pegadas"], t))
    out.append(_section(t("h_warnings"), "\n".join(f"- {w}" for w in rep["advertencias"]) or t("none")))
    return "\n\n".join(out) + "\n"


def _render_census(census: list[dict], t) -> str:
    if not census:
        return _section(t("h_census"), t("census_empty"))
    rows = [[e["dominio"], e["corridas"], e["con_cliente"], "<br>".join(e["urls"])] for e in census]
    head = [t("col_domain"), t("col_cited"), t("col_with_client"), t("col_urls")]
    return _section(t("h_census"), md_table(head, rows) + "\n\n" + t("census_note"))


def _render_figures(figs: list[dict], t) -> str:
    if not figs:
        return _section(t("h_figures"), t("figures_empty"))
    rows = [[f["consulta"], f["asistente"], f["corrida"], f["fecha"], f["cifra"]] for f in figs]
    head = [t("col_query"), t("col_assistant"), t("col_run"), t("col_date"), t("col_claim")]
    return _section(t("h_figures"), md_table(head, rows))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Citation Index from manual AI-assistant runs (Markdown files with YAML frontmatter).")
    parser.add_argument("dir_corridas", type=Path,
                        help="folder with run files (*.md) based on the run template (Spanish or English keys)")
    parser.add_argument("--marca", "--brand", dest="marca", nargs="*", default=[], metavar="ID-NN",
                        help="extra query ids to treat as branded (F3 is always branded)")
    parser.add_argument("--n-esperado", "--expected-n", dest="n_esperado", type=int, default=3,
                        help="expected runs per query x assistant (default 3)")
    parser.add_argument("--json", action="store_true", help="print JSON instead of Markdown (keys stay in Spanish)")
    add_lang_arg(parser)
    args = parser.parse_args(argv)
    lang = resolve_lang(args.lang)
    t = _tr(lang)
    if not args.dir_corridas.is_dir():
        print(t("not_dir", path=args.dir_corridas), file=sys.stderr)
        return 1
    runs, warnings = load_runs(args.dir_corridas, lang)
    if not runs:
        print(t("no_valid") + "\n" + "\n".join(warnings), file=sys.stderr)
        return 1
    report = build_report(runs, warnings, set(args.marca), args.n_esperado, lang)
    print(json.dumps(report, ensure_ascii=False, indent=2, default=str) if args.json else render_markdown(report, lang))
    return 0


if __name__ == "__main__":
    sys.exit(main())
