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

Uso:
    python3 indice_citacion.py examples/corridas-ejemplo
    python3 indice_citacion.py corridas/ --marca Q-07 Q-08 --n-esperado 3
    python3 indice_citacion.py corridas/ --json > indice.json
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
from _comun import fmt_prop, md_table, parse_frontmatter, wilson_interval  # noqa: E402

ASISTENTES = ("chatgpt", "gemini", "claude", "perplexity", "aio", "aimode", "copilot")
ORIGENES = ("ui", "api")
TIPOS = ("informacional", "local", "transaccional")
FAMILIAS = ("F1", "F2", "F3", "F4", "F5", "F6")
REQUIRED = ("consulta", "familia", "tipo_consulta", "asistente", "origen", "corrida",
            "fecha", "modo", "busco", "aparece", "posicion", "nombres", "urls_citadas",
            "cifra_pegada", "notas")


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


def validate_run(fields: dict) -> list[str]:
    """Devuelve la lista de problemas del frontmatter (vacía si es válido)."""
    errors = [f"falta el campo '{k}'" for k in REQUIRED if k not in fields]
    checks = [
        (re.fullmatch(r"[A-Za-z]{1,4}-\d+", str(fields.get("consulta", ""))), "consulta debe ser un id tipo Q-NN o A-NN"),
        (fields.get("familia") in FAMILIAS, f"familia debe ser una de {FAMILIAS}"),
        (fields.get("tipo_consulta") in TIPOS, f"tipo_consulta debe ser una de {TIPOS}"),
        (fields.get("asistente") in ASISTENTES, f"asistente debe ser uno de {ASISTENTES}"),
        (fields.get("origen") in ORIGENES, "origen debe ser ui o api"),
        (isinstance(fields.get("corrida"), int) and fields["corrida"] >= 1, "corrida debe ser entero >= 1"),
        (_parse_fecha(fields.get("fecha")) is not None, "fecha debe ser ISO (AAAA-MM-DD)"),
        (isinstance(fields.get("busco"), bool), "busco debe ser true o false"),
        (isinstance(fields.get("aparece"), bool), "aparece debe ser true o false"),
        (fields.get("posicion") is None or isinstance(fields.get("posicion"), int),
         "posicion debe ser entero o null"),
    ]
    errors += [msg for ok, msg in checks if not ok]
    if fields.get("aparece") is False and isinstance(fields.get("posicion"), int):
        errors.append("aparece es false pero posicion tiene valor")
    return errors


def load_runs(folder: Path) -> tuple[list[dict], list[str]]:
    """Lee *.md de la carpeta. Devuelve (corridas válidas, advertencias)."""
    runs, warnings = [], []
    for path in sorted(folder.glob("*.md")):
        try:
            fields, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        except (ValueError, UnicodeDecodeError) as exc:
            warnings.append(f"{path.name}: no se pudo leer el frontmatter ({exc})")
            continue
        problems = validate_run(fields)
        if problems:
            warnings.append(f"{path.name}: corrida descartada; " + "; ".join(problems))
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

def coverage_warnings(runs: list[dict], n_expected: int, assistants: list[str]) -> list[str]:
    warnings = []
    for (consulta, asistente), rs in sorted(group_by(runs, "consulta", "asistente").items()):
        numbers = [r["corrida"] for r in rs]
        if len(set(numbers)) != len(numbers):
            warnings.append(f"{consulta} / {asistente}: número de corrida repetido {sorted(numbers)}")
        if len(rs) < n_expected:
            warnings.append(f"{consulta} / {asistente}: {len(rs)} de {n_expected} corridas esperadas")
    present = {(r["consulta"], r["asistente"]) for r in runs}
    missing = [f"{q}/{a}" for q in sorted({r["consulta"] for r in runs}, key=_qnum)
               for a in assistants if (q, a) not in present]
    if missing:
        warnings.append("combinaciones sin ninguna corrida (si fue deliberado, ignora): " + ", ".join(missing))
    return warnings


def quality_warnings(runs: list[dict]) -> list[str]:
    warnings = []
    first_date = min(r["fecha"] for r in runs)
    for (consulta,), rs in sorted(group_by(runs, "consulta").items(), key=lambda kv: _qnum(kv[0][0])):
        start = min(r["fecha"] for r in rs)
        if start > first_date:
            warnings.append(f"{consulta}: sin histórico (alta {start.isoformat()}, posterior a la primera corrida)")
    for r in runs:
        if r["aparece"] and r["posicion"] is None:
            warnings.append(f"{r['archivo']}: aparece sin posicion (¿respuesta en prosa sin orden?)")
        if r["busco"] and not r["urls_citadas"]:
            warnings.append(f"{r['archivo']}: busco=true pero sin urls_citadas")
        if not r["tiene_verbatim"]:
            warnings.append(f"{r['archivo']}: falta la sección '## Verbatim'")
    return warnings


# ---------------------------------------------------------------- salida

def build_report(runs: list[dict], warnings: list[str], brand_ids: set[str], n_expected: int) -> dict:
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
        "advertencias": [*warnings, *coverage_warnings(runs, n_expected, assistants), *quality_warnings(runs)],
    }


def _cell(cell: dict) -> str:
    if cell["n"] == 0:
        return "·"
    pos = f" ({', '.join(map(str, cell['posiciones']))})" if cell["posiciones"] else ""
    return f"{cell['k']}/{cell['n']}{pos}"


def _prop_rows(block: dict, assistants: list[str]) -> list[list[str]]:
    return [[a, block[a]["texto"]] for a in [*assistants, "global"] if block[a]["n"]]


def render_markdown(rep: dict) -> str:
    a = rep["asistentes"]
    out = [f"# Índice de Citación\n\n{rep['corridas']} corridas · {rep['fechas'][0]} a {rep['fechas'][1]} · "
           "celdas `k/n (posiciones)`; proporciones con intervalo de Wilson al 95 %.\n"]
    rows = [[r["consulta"] + (" (marca)" if r["marca"] else ""), r["familia"], r["tipo_consulta"],
             *[_cell(r["celdas"][x]) for x in a], r["total"]["texto"]] for r in rep["indice"]]
    out.append("## 1. Por consulta y asistente\n\n" + md_table(["Consulta", "Fam.", "Tipo", *a, "Total"], rows))
    out.append("## 2. Subtotal sin marca\n\n" + md_table(["Asistente", "Aparece"], _prop_rows(rep["sin_marca"], a)))
    if rep["marca"]["global"]["n"]:
        out.append("Consultas de marca (aparte, no suman al subtotal):\n\n"
                   + md_table(["Asistente", "Aparece"], _prop_rows(rep["marca"], a)))
    out.append("## 3. Primer lugar (sin marca)\n\n" + md_table(["Asistente", "Primer lugar"], _prop_rows(rep["primer_lugar"], a)))
    out.append("## 4. Tasa de disparo (buscó en la web)\n\n" + md_table(["Asistente", "Buscó"], _prop_rows(rep["tasa_disparo"], a)))
    out.append("## 5. Lectura por tipo de consulta (sin marca) y por familia\n\n"
               + md_table(["Tipo", "Aparece"], [[k, v["texto"]] for k, v in rep["por_tipo_consulta"].items()])
               + "\n\n" + md_table(["Familia", "Aparece"], [[k, v["texto"]] for k, v in rep["por_familia"].items()]))
    out.append(_render_census(rep["censo_fuentes"]))
    out.append(_render_figures(rep["cifras_pegadas"]))
    out.append("## 8. Advertencias\n\n" + ("\n".join(f"- {w}" for w in rep["advertencias"]) or "Ninguna."))
    return "\n\n".join(out) + "\n"


def _render_census(census: list[dict]) -> str:
    if not census:
        return "## 6. Censo de fuentes\n\nNinguna corrida citó URLs."
    rows = [[e["dominio"], e["corridas"], e["con_cliente"], "<br>".join(e["urls"])] for e in census]
    note = ("\n\nViva/muerta y si nombra al cliente: corre `verificar_fuentes.py` sobre la misma carpeta. "
            "Propia/tercero: márcalo a mano en el reporte.")
    return "## 6. Censo de fuentes\n\n" + md_table(["Dominio", "Corridas que lo citan", "Con cliente", "URLs"], rows) + note


def _render_figures(figs: list[dict]) -> str:
    if not figs:
        return "## 7. Cifras pegadas\n\nNinguna registrada."
    rows = [[f["consulta"], f["asistente"], f["corrida"], f["fecha"], f["cifra"]] for f in figs]
    return "## 7. Cifras pegadas\n\n" + md_table(["Consulta", "Asistente", "Corrida", "Fecha", "Cifra"], rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Citation Index from manual AI-assistant runs (Markdown files with YAML frontmatter).")
    parser.add_argument("dir_corridas", type=Path, help="folder with run files (*.md) based on corrida.template.md")
    parser.add_argument("--marca", nargs="*", default=[], metavar="ID-NN",
                        help="extra query ids to treat as branded (F3 is always branded)")
    parser.add_argument("--n-esperado", type=int, default=3, help="expected runs per query x assistant (default 3)")
    parser.add_argument("--json", action="store_true", help="print JSON instead of Markdown")
    args = parser.parse_args(argv)
    if not args.dir_corridas.is_dir():
        print(f"error: {args.dir_corridas} no es una carpeta", file=sys.stderr)
        return 1
    runs, warnings = load_runs(args.dir_corridas)
    if not runs:
        print("error: ninguna corrida válida.\n" + "\n".join(warnings), file=sys.stderr)
        return 1
    report = build_report(runs, warnings, set(args.marca), args.n_esperado)
    print(json.dumps(report, ensure_ascii=False, indent=2, default=str) if args.json else render_markdown(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
