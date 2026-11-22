#!/usr/bin/env python3
"""Auditoría de un sitio en producción con exportaciones de Search Console (modo --auditar).

Entrada: uno o más CSV exportados de Search Console (Rendimiento → Exportar), o
carpetas que los contengan. Reconoce encabezados en español y en inglés:

  consulta   "Consultas principales" / "Top queries" / "Consulta" / "Query"
  página     "Páginas principales" / "Top pages" / "Página" / "Page"
  clics      "Clics" / "Clicks"
  impres.    "Impresiones" / "Impressions"
  CTR        "CTR" (acepta "12.5%", "12,5 %" o 0.125)
  posición   "Posición" / "Position"

Un CSV con consulta y página a la vez es la vista consulta × página (API,
Looker Studio o filtros). Si no hay tabla de consultas o de páginas, se derivan
de la vista consulta × página.

Análisis (cada hallazgo con una acción y una página):
  a. CTR bajo para su posición (1 a 10), contra la curva del PROPIO sitio:
     mediana de CTR por banda de posición, sin consultas de marca, con mínimo de
     impresiones.
     No se usa una tabla fija de CTR esperado (es previa a AI Overviews).
  b. Distancia de ataque: posiciones 5 a 20 con impresiones.
  c. Pérdida de 5 clics o más entre dos periodos (--periodo-previo), con
     diagnóstico: posición, CTR o demanda.
  d. Canibalización: una consulta sin marca repartida entre varias páginas.
  e. Páginas muertas: tenían clics en el periodo previo y ahora cero.
  f. Proporción de clics con marca y sin marca (>60 % sano, 40-60 % medio,
     <40 % dependiente; umbral orientativo).

Método completo: references/auditoria-gsc.md

Uso:
    python3 auditoria_gsc.py examples/gsc-ejemplo/actual --marca "elena ruiz" ruiz
    python3 auditoria_gsc.py actual/*.csv --periodo-previo previo/ --marca nimbus --json
    python3 auditoria_gsc.py current/ --previous-period previous/ --brand nimbus --lang en
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import add_lang_arg, make_translator, md_table, normalize_text, resolve_lang  # noqa: E402

HEADERS = {
    "consulta": ("consultas principales", "top queries", "consulta", "consultas", "query", "queries"),
    "pagina": ("paginas principales", "top pages", "pagina", "paginas", "page", "pages", "url", "landing page"),
    "clics": ("clics", "clicks"),
    "impresiones": ("impresiones", "impressions"),
    "ctr": ("ctr",),
    "posicion": ("posicion", "position", "posicion media", "average position"),
}
BANDS = (("1", 0, 1.5), ("2", 1.5, 2.5), ("3", 2.5, 3.5), ("4-5", 3.5, 5.5), ("6-10", 5.5, 10.5),
         ("11-20", 10.5, 20.5), ("21+", 20.5, 10_000))
CTR_FACTOR = 0.7          # CTR por debajo del 70 % de la mediana de su banda
CTR_MAX_POSITION = 10.5   # en página 2 el arreglo es subir, no el snippet: eso lo cubre la distancia de ataque
MIN_LOSS_CLICKS = 5       # una pérdida menor es ruido
MIN_ROWS_PER_BAND = 3     # sin 3 filas en la banda no hay curva para esa banda
ATTACK_RANGE = (5.0, 20.0)
TARGET_BAND = "3"         # la ganancia de la distancia de ataque se estima contra la mediana de la banda 3
POSITION_DROP = 2.0       # caída de posición que se lee como problema de contenido
CTR_DROP = 0.2            # caída relativa de CTR que se lee como problema de SERP o snippet
IMPR_DROP = 0.2           # caída relativa de impresiones que se lee como demanda
CANNIBAL_SHARE = 0.15     # una página cuenta si tiene al menos 15 % de las impresiones de la consulta
TOP_ROWS = 15

MESSAGES = {
    "es": {
        "title": "# Auditoría de Search Console\n\n{summary}\n",
        "summary": ("{queries} consultas · {pages} páginas · {pairs} filas consulta × página · "
                    "periodo previo: {prev} · mínimo de impresiones: {min_impr}"),
        "yes": "sí", "no": "no",
        "h_exec": "## Resumen ejecutivo",
        "exec_one": "**Acción número uno:** {action} ({page}). Clics en juego, estimados con la curva del sitio: {clicks}.",
        "exec_none": "Sin hallazgos con clics en juego sobre el mínimo de impresiones.",
        "exec_counts": "Hallazgos: CTR bajo {a} · distancia de ataque {b} · pérdida {c} · canibalización {d} · páginas muertas {e}.",
        "exec_brand": "Clics sin marca: {ratio} ({label}).",
        "h_curve": "## Curva de CTR del sitio (sin marca)",
        "col_band": "Banda de posición", "col_rows": "Filas", "col_median": "CTR mediano",
        "curve_note": ("Mediana de CTR por banda, con filas de al menos {min_impr} impresiones. Una banda con "
                       "menos de {min_rows} filas no tiene curva y no se usa. Referencia de contexto, no tabla fija: "
                       "el CTR orgánico en consultas con AI Overviews cayó 61 % desde mid-2024 (Seer Interactive, "
                       "sep 2025 [E] ⚠️, ver `geo-evidencia.md` 2.5)."),
        "h_a": "## a. CTR bajo para su posición (1 a 10)",
        "h_b": "## b. Distancia de ataque (posiciones 5 a 20)",
        "h_c": "## c. Pérdida entre periodos",
        "h_d": "## d. Canibalización",
        "h_e": "## e. Páginas muertas",
        "h_f": "## f. Marca y sin marca",
        "col_query": "Consulta", "col_page": "Página", "col_pos": "Posición", "col_impr": "Impresiones",
        "col_clicks": "Clics", "col_ctr": "CTR", "col_expected": "CTR mediano de su banda", "col_gain": "Clics en juego",
        "col_action": "Acción", "col_key": "Clave", "col_prev_clicks": "Clics antes", "col_delta": "Cambio de clics",
        "col_prev_pos": "Posición antes", "col_diag": "Diagnóstico", "col_pages": "Páginas que compiten",
        "col_kind": "Tipo", "col_share": "Proporción de clics",
        "no_page": "(exporta consulta × página)",
        "act_ctr": "reescribir title y meta description; revisar si la SERP muestra AI Overview",
        "act_attack_top": "subir al top 3: respuesta directa al abrir, tabla o dato propio, enlaces internos",
        "act_attack_p2": "llevar a página 1: refrescar el contenido y sumar enlaces internos desde páginas fuertes",
        "diag_position": "perdió posición: refrescar contenido y revisar quién entró arriba",
        "diag_ctr": "misma posición, menos CTR: snippet o SERP cambió (AI Overview, title); reescribir title y meta",
        "diag_demand": "misma posición, menos impresiones: bajó la demanda o la estacionalidad; no se toca la página",
        "diag_mixed": "caída mixta: revisar a mano",
        "act_cannibal": "{winner} se queda la consulta; las demás se consolidan con 301 o se diferencian de intención",
        "act_dead": "abrir la URL: si da 404 o noindex, restaurar o redirigir; si está viva, buscar la página que le quitó la consulta",
        "kind_brand": "con marca", "kind_unbranded": "sin marca",
        "ratio_healthy": "sano", "ratio_medium": "medio", "ratio_dependent": "dependiente de la marca",
        "ratio_note": "Umbral orientativo: >60 % sin marca sano, 40-60 % medio, <40 % dependiente.",
        "top_unbranded": "Consultas sin marca con más clics:",
        "empty": "Sin hallazgos.",
        "needs_prev": "Requiere --periodo-previo.",
        "needs_pairs": "Requiere la vista consulta × página.",
        "needs_brand": "Requiere --marca.",
        "needs_pages": "Requiere tabla de páginas en los dos periodos.",
        "h_warnings": "## Advertencias", "none": "Ninguna.",
        "w_no_brand": "sin --marca: la curva y la canibalización incluyen consultas de marca, que inflan el CTR",
        "w_band": "banda {band}: {rows} filas, menos de {min_rows}; sin curva para esa banda",
        "w_unknown_csv": "{file}: no reconozco las columnas ({cols}); se omite",
        "w_bad_row": "{file}: {count} filas con números ilegibles; se omiten",
        "w_derived": "tabla de {kind} derivada de la vista consulta × página",
        "kind_queries": "consultas", "kind_pages": "páginas",
        "not_found": "error: no existe {path}",
        "no_csv": "error: no encontré CSV en {paths}",
        "no_rows": "error: ningún CSV con columnas de Search Console reconocibles",
    },
    "en": {
        "title": "# Search Console audit\n\n{summary}\n",
        "summary": ("{queries} queries · {pages} pages · {pairs} query × page rows · "
                    "previous period: {prev} · minimum impressions: {min_impr}"),
        "yes": "yes", "no": "no",
        "h_exec": "## Executive summary",
        "exec_one": "**Action number one:** {action} ({page}). Clicks at stake, estimated with the site's own curve: {clicks}.",
        "exec_none": "No findings with clicks at stake above the impression minimum.",
        "exec_counts": "Findings: low CTR {a} · striking distance {b} · loss {c} · cannibalization {d} · dead pages {e}.",
        "exec_brand": "Unbranded clicks: {ratio} ({label}).",
        "h_curve": "## Site CTR curve (unbranded)",
        "col_band": "Position band", "col_rows": "Rows", "col_median": "Median CTR",
        "curve_note": ("Median CTR per band, from rows with at least {min_impr} impressions. A band with fewer than "
                       "{min_rows} rows has no curve and is not used. Context, not a fixed table: organic CTR on "
                       "queries with AI Overviews fell 61% since mid-2024 (Seer Interactive, Sep 2025 [E] ⚠️, see "
                       "`geo-evidence.md` 2.5)."),
        "h_a": "## a. Low CTR for its position (1 to 10)",
        "h_b": "## b. Striking distance (positions 5 to 20)",
        "h_c": "## c. Loss between periods",
        "h_d": "## d. Cannibalization",
        "h_e": "## e. Dead pages",
        "h_f": "## f. Branded and unbranded",
        "col_query": "Query", "col_page": "Page", "col_pos": "Position", "col_impr": "Impressions",
        "col_clicks": "Clicks", "col_ctr": "CTR", "col_expected": "Median CTR of its band", "col_gain": "Clicks at stake",
        "col_action": "Action", "col_key": "Key", "col_prev_clicks": "Clicks before", "col_delta": "Click change",
        "col_prev_pos": "Position before", "col_diag": "Diagnosis", "col_pages": "Competing pages",
        "col_kind": "Kind", "col_share": "Share of clicks",
        "no_page": "(export query × page)",
        "act_ctr": "rewrite title and meta description; check whether the SERP shows an AI Overview",
        "act_attack_top": "move into the top 3: direct answer up front, a table or own data, internal links",
        "act_attack_p2": "reach page 1: refresh the content and add internal links from strong pages",
        "diag_position": "lost position: refresh the content and check who moved above",
        "diag_ctr": "same position, lower CTR: the snippet or SERP changed (AI Overview, title); rewrite title and meta",
        "diag_demand": "same position, fewer impressions: demand or seasonality dropped; leave the page alone",
        "diag_mixed": "mixed drop: review by hand",
        "act_cannibal": "{winner} keeps the query; the others get consolidated with a 301 or split by intent",
        "act_dead": "open the URL: if it returns 404 or noindex, restore or redirect; if it is live, find the page that took the query",
        "kind_brand": "branded", "kind_unbranded": "unbranded",
        "ratio_healthy": "healthy", "ratio_medium": "medium", "ratio_dependent": "brand-dependent",
        "ratio_note": "Rough threshold: >60% unbranded healthy, 40-60% medium, <40% dependent.",
        "top_unbranded": "Unbranded queries with the most clicks:",
        "empty": "No findings.",
        "needs_prev": "Needs --previous-period.",
        "needs_pairs": "Needs the query × page view.",
        "needs_brand": "Needs --brand.",
        "needs_pages": "Needs a pages table in both periods.",
        "h_warnings": "## Warnings", "none": "None.",
        "w_no_brand": "no --brand: the curve and cannibalization include branded queries, which inflate CTR",
        "w_band": "band {band}: {rows} rows, fewer than {min_rows}; no curve for that band",
        "w_unknown_csv": "{file}: unrecognized columns ({cols}); skipped",
        "w_bad_row": "{file}: {count} rows with unreadable numbers; skipped",
        "w_derived": "{kind} table derived from the query × page view",
        "kind_queries": "queries", "kind_pages": "pages",
        "not_found": "error: {path} does not exist",
        "no_csv": "error: no CSV found in {paths}",
        "no_rows": "error: no CSV with recognizable Search Console columns",
    },
}


def _tr(lang: str):
    return make_translator(MESSAGES, lang)


# ---------------------------------------------------------------- lectura

def parse_number(raw: str, integer: bool = False) -> float:
    """'1,234' '1.234' '12,5 %' '12.5%' '3,4' → número. Lanza ValueError si no se puede."""
    text = re.sub(r"[\s% ]", "", str(raw))
    if not text:
        raise ValueError(raw)
    if integer:
        return float(re.sub(r"[.,]", "", text))
    if "," in text and "." in text:
        decimal = "," if text.rfind(",") > text.rfind(".") else "."
        thousands = "." if decimal == "," else ","
        text = text.replace(thousands, "").replace(decimal, ".")
    else:
        text = text.replace(",", ".")
    return float(text)


def parse_ctr(raw: str) -> float:
    """Devuelve CTR como proporción (0-1). '12,5 %' → 0.125; '0.125' → 0.125."""
    value = parse_number(raw)
    return value / 100 if "%" in str(raw) or value > 1 else value


def _map_columns(header: list[str]) -> dict[str, int]:
    mapping = {}
    for idx, name in enumerate(header):
        key = normalize_text(name)
        for field, aliases in HEADERS.items():
            if key in aliases and field not in mapping:
                mapping[field] = idx
    return mapping


def _sniff_rows(text: str) -> list[list[str]]:
    try:
        dialect = csv.Sniffer().sniff(text[:4096], delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel
    return [row for row in csv.reader(io.StringIO(text), dialect) if any(c.strip() for c in row)]


def read_csv(path: Path, t) -> tuple[str | None, list[dict], list[str]]:
    """Devuelve (tipo, filas, advertencias). Tipo: consultas, paginas, pares o None."""
    rows = _sniff_rows(path.read_text(encoding="utf-8-sig"))
    if not rows:
        return None, [], []
    cols = _map_columns(rows[0])
    metrics = {"clics", "impresiones", "ctr", "posicion"}
    has_q, has_p = "consulta" in cols, "pagina" in cols
    if not metrics <= cols.keys() or not (has_q or has_p):
        return None, [], [t("w_unknown_csv", file=path.name, cols=", ".join(rows[0]))]
    kind = "pares" if has_q and has_p else ("consultas" if has_q else "paginas")
    parsed, bad = [], 0
    for row in rows[1:]:
        try:
            parsed.append({"consulta": row[cols["consulta"]].strip() if has_q else None,
                           "pagina": row[cols["pagina"]].strip() if has_p else None,
                           "clics": parse_number(row[cols["clics"]], integer=True),
                           "impresiones": parse_number(row[cols["impresiones"]], integer=True),
                           "ctr": parse_ctr(row[cols["ctr"]]),
                           "posicion": parse_number(row[cols["posicion"]])})
        except (ValueError, IndexError):
            bad += 1
    warnings = [t("w_bad_row", file=path.name, count=bad)] if bad else []
    return kind, parsed, warnings


def collect_csvs(paths: list[Path]) -> list[Path]:
    files = []
    for path in paths:
        files += sorted(path.glob("*.csv")) if path.is_dir() else [path]
    return files


def aggregate(pairs: list[dict], key: str) -> list[dict]:
    """Deriva la tabla de consultas o de páginas desde consulta × página."""
    groups: dict[str, list[dict]] = {}
    for row in pairs:
        groups.setdefault(row[key], []).append(row)
    out = []
    for name, rows in groups.items():
        clicks = sum(r["clics"] for r in rows)
        impr = sum(r["impresiones"] for r in rows)
        pos = sum(r["posicion"] * r["impresiones"] for r in rows) / impr if impr else 0.0
        out.append({"consulta": name if key == "consulta" else None, "pagina": name if key == "pagina" else None,
                    "clics": clicks, "impresiones": impr, "ctr": clicks / impr if impr else 0.0, "posicion": pos})
    return out


def load_period(paths: list[Path], t) -> tuple[dict, list[str]]:
    tables: dict[str, list[dict]] = {"consultas": [], "paginas": [], "pares": []}
    warnings = []
    for path in collect_csvs(paths):
        kind, rows, notes = read_csv(path, t)
        warnings += notes
        if kind:
            tables = {**tables, kind: [*tables[kind], *rows]}
    for kind, key, label in (("consultas", "consulta", "kind_queries"), ("paginas", "pagina", "kind_pages")):
        if not tables[kind] and tables["pares"]:
            tables = {**tables, kind: aggregate(tables["pares"], key)}
            warnings.append(t("w_derived", kind=t(label)))
    return tables, warnings


# ---------------------------------------------------------------- análisis

def is_brand_query(query: str | None, brand_terms: list[str]) -> bool:
    text = normalize_text(query or "")
    return any(term and term in text for term in brand_terms)


def band_of(position: float) -> str:
    return next(name for name, lo, hi in BANDS if lo <= position < hi)


def ctr_curve(rows: list[dict], min_impr: int) -> dict[str, dict]:
    curve = {}
    for name, _, _ in BANDS:
        ctrs = [r["ctr"] for r in rows if r["impresiones"] >= min_impr and band_of(r["posicion"]) == name]
        curve[name] = {"filas": len(ctrs), "mediana": statistics.median(ctrs) if len(ctrs) >= MIN_ROWS_PER_BAND else None}
    return curve


def _best_page(query: str, pairs: list[dict]) -> str | None:
    candidates = [p for p in pairs if p["consulta"] == query]
    return max(candidates, key=lambda p: (p["clics"], p["impresiones"]))["pagina"] if candidates else None


def low_ctr(rows: list[dict], curve: dict, pairs: list[dict], min_impr: int) -> list[dict]:
    found = []
    for r in rows:
        median = curve[band_of(r["posicion"])]["mediana"]
        if r["impresiones"] < min_impr or r["posicion"] > CTR_MAX_POSITION or median is None or r["ctr"] >= median * CTR_FACTOR:
            continue
        page = r["pagina"] or _best_page(r["consulta"], pairs)
        found.append({**r, "pagina": page, "ctr_banda": median,
                      "clics_en_juego": round(r["impresiones"] * (median - r["ctr"]))})
    return sorted(found, key=lambda f: -f["clics_en_juego"])


def striking_distance(rows: list[dict], curve: dict, pairs: list[dict], min_impr: int) -> list[dict]:
    target = curve[TARGET_BAND]["mediana"]
    found = []
    for r in rows:
        if r["impresiones"] < min_impr or not ATTACK_RANGE[0] <= r["posicion"] <= ATTACK_RANGE[1]:
            continue
        gain = round(r["impresiones"] * max(0.0, target - r["ctr"])) if target is not None else None
        found.append({**r, "pagina": r["pagina"] or _best_page(r["consulta"], pairs), "clics_en_juego": gain,
                      "accion": "act_attack_top" if r["posicion"] <= 10 else "act_attack_p2"})
    return sorted(found, key=lambda f: -f["impresiones"])


def _diagnose(now: dict, before: dict) -> str:
    if now["posicion"] - before["posicion"] >= POSITION_DROP:
        return "diag_position"
    if before["ctr"] and (before["ctr"] - now["ctr"]) / before["ctr"] >= CTR_DROP:
        return "diag_ctr"
    if before["impresiones"] and (before["impresiones"] - now["impresiones"]) / before["impresiones"] >= IMPR_DROP:
        return "diag_demand"
    return "diag_mixed"


def period_loss(now_rows: list[dict], prev_rows: list[dict], key: str) -> list[dict]:
    now_by = {r[key]: r for r in now_rows}
    found = []
    for before in prev_rows:
        now = now_by.get(before[key])
        if now is None or before["clics"] - now["clics"] < MIN_LOSS_CLICKS:
            continue
        found.append({"clave": before[key], "tipo": key, "pagina": now.get("pagina"), "clics_antes": before["clics"],
                      "clics": now["clics"], "cambio": now["clics"] - before["clics"],
                      "posicion_antes": before["posicion"], "posicion": now["posicion"],
                      "diagnostico": _diagnose(now, before), "clics_en_juego": round(before["clics"] - now["clics"])})
    return sorted(found, key=lambda f: f["cambio"])


def cannibalization(pairs: list[dict], brand_terms: list[str], min_impr: int) -> list[dict]:
    groups: dict[str, list[dict]] = {}
    for p in pairs:
        if not is_brand_query(p["consulta"], brand_terms):
            groups.setdefault(p["consulta"], []).append(p)
    found = []
    for query, rows in groups.items():
        total = sum(r["impresiones"] for r in rows)
        if total < min_impr:
            continue
        competing = sorted((r for r in rows if r["impresiones"] / total >= CANNIBAL_SHARE),
                           key=lambda r: (-r["clics"], r["posicion"]))
        if len(competing) >= 2:
            found.append({"consulta": query, "impresiones": total, "paginas": competing,
                          "ganadora": competing[0]["pagina"]})
    return sorted(found, key=lambda f: -f["impresiones"])


def dead_pages(now_pages: list[dict], prev_pages: list[dict], min_prev_clicks: int) -> list[dict]:
    now_clicks = {r["pagina"]: r["clics"] for r in now_pages}
    found = [{"pagina": r["pagina"], "clics_antes": r["clics"], "clics": now_clicks.get(r["pagina"], 0),
              "clics_en_juego": round(r["clics"])}
             for r in prev_pages if r["clics"] >= min_prev_clicks and now_clicks.get(r["pagina"], 0) == 0]
    return sorted(found, key=lambda f: -f["clics_antes"])


def brand_split(queries: list[dict], brand_terms: list[str]) -> dict | None:
    if not brand_terms:
        return None
    branded = [q for q in queries if is_brand_query(q["consulta"], brand_terms)]
    unbranded = [q for q in queries if not is_brand_query(q["consulta"], brand_terms)]
    b_clicks, u_clicks = sum(q["clics"] for q in branded), sum(q["clics"] for q in unbranded)
    total = b_clicks + u_clicks
    ratio = u_clicks / total if total else None
    label = None if ratio is None else ("ratio_healthy" if ratio > 0.6 else
                                        "ratio_medium" if ratio >= 0.4 else "ratio_dependent")
    top = sorted(unbranded, key=lambda q: -q["clics"])[:10]
    return {"clics_marca": b_clicks, "clics_sin_marca": u_clicks,
            "impresiones_marca": sum(q["impresiones"] for q in branded),
            "impresiones_sin_marca": sum(q["impresiones"] for q in unbranded),
            "proporcion_sin_marca": round(ratio, 4) if ratio is not None else None, "lectura": label,
            "top_sin_marca": [{"consulta": q["consulta"], "clics": q["clics"], "posicion": q["posicion"]} for q in top]}


def number_one(rep: dict) -> dict | None:
    """El hallazgo con más clics en juego entre a, b, c y e."""
    pool = [("act_ctr", f) for f in rep["ctr_bajo"]]
    pool += [(f["accion"], f) for f in rep["distancia_ataque"] if f["clics_en_juego"]]
    pool += [(f["diagnostico"], f) for f in (rep["perdida"] or [])]
    pool += [("act_dead", f) for f in (rep["paginas_muertas"] or [])]
    pool = [(action, f) for action, f in pool if f.get("clics_en_juego")]
    if not pool:
        return None
    action, best = max(pool, key=lambda item: item[1]["clics_en_juego"])
    return {"accion": action, "pagina": best.get("pagina") or best.get("clave"),
            "consulta": best.get("consulta"), "clics_en_juego": best["clics_en_juego"]}


def build_report(now: dict, prev: dict | None, brand_terms: list[str], min_impr: int,
                 min_prev_clicks: int, warnings: list[str], t) -> dict:
    queries, pages, pairs = now["consultas"], now["paginas"], now["pares"]
    unbranded_q = [q for q in queries if not is_brand_query(q["consulta"], brand_terms)]
    curve_rows = unbranded_q or pages
    curve = ctr_curve(curve_rows, min_impr)
    notes = [] if brand_terms else [t("w_no_brand")]
    notes += [t("w_band", band=b, rows=c["filas"], min_rows=MIN_ROWS_PER_BAND)
              for b, c in curve.items() if c["mediana"] is None and c["filas"]]
    loss = None
    dead = None
    if prev is not None:
        key_rows = (("pagina", pages, prev["paginas"]) if pages and prev["paginas"]
                    else ("consulta", unbranded_q, prev["consultas"]))
        loss = period_loss(key_rows[1], key_rows[2], key_rows[0])
        dead = dead_pages(pages, prev["paginas"], min_prev_clicks) if pages and prev["paginas"] else None
    rep = {"resumen": {"consultas": len(queries), "paginas": len(pages), "pares": len(pairs),
                       "periodo_previo": prev is not None, "min_impresiones": min_impr},
           "curva_ctr": curve,
           "ctr_bajo": low_ctr(unbranded_q or pages, curve, pairs, min_impr),
           "distancia_ataque": striking_distance(unbranded_q or pages, curve, pairs, min_impr),
           "perdida": loss,
           "canibalizacion": cannibalization(pairs, brand_terms, min_impr) if pairs else None,
           "paginas_muertas": dead,
           "marca": brand_split(queries, brand_terms) if queries else None,
           "advertencias": [*warnings, *notes]}
    return {**rep, "accion_uno": number_one(rep)}


# ---------------------------------------------------------------- salida

def _pct(value: float | None) -> str:
    return "·" if value is None else f"{100 * value:.1f} %"


def _pos(value: float) -> str:
    return f"{value:.1f}"


def _n(value: float | None) -> str:
    return "·" if value is None else f"{value:,.0f}"


def _section(heading: str, body: str) -> str:
    return f"{heading}\n\n{body}"


def _render_exec(rep: dict, t) -> str:
    lines = []
    one = rep["accion_uno"]
    if one:
        page = one["pagina"] or t("no_page")
        target = f"{one['consulta']} → {page}" if one.get("consulta") else page
        lines.append(t("exec_one", action=t(one["accion"]), page=target, clicks=_n(one["clics_en_juego"])))
    else:
        lines.append(t("exec_none"))
    count = lambda v: "·" if v is None else len(v)  # noqa: E731
    lines.append(t("exec_counts", a=len(rep["ctr_bajo"]), b=len(rep["distancia_ataque"]), c=count(rep["perdida"]),
                   d=count(rep["canibalizacion"]), e=count(rep["paginas_muertas"])))
    brand = rep["marca"]
    if brand and brand["proporcion_sin_marca"] is not None:
        lines.append(t("exec_brand", ratio=_pct(brand["proporcion_sin_marca"]), label=t(brand["lectura"])))
    return _section(t("h_exec"), "\n\n".join(lines))


def _render_findings(rep: dict, t) -> list[str]:
    no_page = t("no_page")
    out = []
    head_a = [t("col_query"), t("col_page"), t("col_pos"), t("col_impr"), t("col_ctr"), t("col_expected"),
              t("col_gain"), t("col_action")]
    rows_a = [[f["consulta"] or "·", f["pagina"] or no_page, _pos(f["posicion"]), _n(f["impresiones"]), _pct(f["ctr"]),
               _pct(f["ctr_banda"]), _n(f["clics_en_juego"]), t("act_ctr")] for f in rep["ctr_bajo"][:TOP_ROWS]]
    out.append(_section(t("h_a"), md_table(head_a, rows_a) if rows_a else t("empty")))
    head_b = [t("col_query"), t("col_page"), t("col_pos"), t("col_impr"), t("col_clicks"), t("col_gain"), t("col_action")]
    rows_b = [[f["consulta"] or "·", f["pagina"] or no_page, _pos(f["posicion"]), _n(f["impresiones"]), _n(f["clics"]),
               _n(f["clics_en_juego"]), t(f["accion"])] for f in rep["distancia_ataque"][:TOP_ROWS]]
    out.append(_section(t("h_b"), md_table(head_b, rows_b) if rows_b else t("empty")))
    if rep["perdida"] is None:
        out.append(_section(t("h_c"), t("needs_prev")))
    else:
        head_c = [t("col_key"), t("col_prev_clicks"), t("col_clicks"), t("col_delta"), t("col_prev_pos"), t("col_pos"),
                  t("col_diag")]
        rows_c = [[f["clave"], _n(f["clics_antes"]), _n(f["clics"]), _n(f["cambio"]), _pos(f["posicion_antes"]),
                   _pos(f["posicion"]), t(f["diagnostico"])] for f in rep["perdida"][:TOP_ROWS]]
        out.append(_section(t("h_c"), md_table(head_c, rows_c) if rows_c else t("empty")))
    out.append(_render_cannibal(rep["canibalizacion"], t))
    if rep["paginas_muertas"] is None:
        out.append(_section(t("h_e"), t("needs_pages")))
    else:
        rows_e = [[f["pagina"], _n(f["clics_antes"]), _n(f["clics"]), t("act_dead")] for f in rep["paginas_muertas"]]
        head_e = [t("col_page"), t("col_prev_clicks"), t("col_clicks"), t("col_action")]
        out.append(_section(t("h_e"), md_table(head_e, rows_e) if rows_e else t("empty")))
    out.append(_render_brand(rep["marca"], t))
    return out


def _render_cannibal(found: list[dict] | None, t) -> str:
    if found is None:
        return _section(t("h_d"), t("needs_pairs"))
    if not found:
        return _section(t("h_d"), t("empty"))
    rows = [[f["consulta"], _n(f["impresiones"]),
             "<br>".join(f"{p['pagina']} ({_pos(p['posicion'])}, {_n(p['clics'])} {t('col_clicks').lower()})"
                         for p in f["paginas"]),
             t("act_cannibal", winner=f["ganadora"])] for f in found[:TOP_ROWS]]
    return _section(t("h_d"), md_table([t("col_query"), t("col_impr"), t("col_pages"), t("col_action")], rows))


def _render_brand(brand: dict | None, t) -> str:
    if brand is None:
        return _section(t("h_f"), t("needs_brand"))
    total = brand["clics_marca"] + brand["clics_sin_marca"]
    share = lambda v: _pct(v / total) if total else "·"  # noqa: E731
    rows = [[t("kind_brand"), _n(brand["clics_marca"]), _n(brand["impresiones_marca"]), share(brand["clics_marca"])],
            [t("kind_unbranded"), _n(brand["clics_sin_marca"]), _n(brand["impresiones_sin_marca"]),
             share(brand["clics_sin_marca"])]]
    body = md_table([t("col_kind"), t("col_clicks"), t("col_impr"), t("col_share")], rows)
    if brand["lectura"]:
        body += f"\n\n**{t(brand['lectura'])}.** {t('ratio_note')}"
    top = [[q["consulta"], _n(q["clics"]), _pos(q["posicion"])] for q in brand["top_sin_marca"]]
    if top:
        body += f"\n\n{t('top_unbranded')}\n\n" + md_table([t("col_query"), t("col_clicks"), t("col_pos")], top)
    return _section(t("h_f"), body)


def render_markdown(rep: dict, lang: str = "es") -> str:
    t = _tr(lang)
    s = rep["resumen"]
    out = [t("title", summary=t("summary", queries=s["consultas"], pages=s["paginas"], pairs=s["pares"],
                                 prev=t("yes") if s["periodo_previo"] else t("no"), min_impr=s["min_impresiones"]))]
    out.append(_render_exec(rep, t))
    curve_rows = [[b, c["filas"], _pct(c["mediana"])] for b, c in rep["curva_ctr"].items()]
    out.append(_section(t("h_curve"), md_table([t("col_band"), t("col_rows"), t("col_median")], curve_rows) + "\n\n"
                        + t("curve_note", min_impr=s["min_impresiones"], min_rows=MIN_ROWS_PER_BAND)))
    out += _render_findings(rep, t)
    out.append(_section(t("h_warnings"), "\n".join(f"- {w}" for w in rep["advertencias"]) or t("none")))
    return "\n\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit a live site from Search Console CSV exports (Spanish or English headers): low CTR "
                    "against the site's own curve, striking distance, period loss, cannibalization, dead pages "
                    "and branded vs unbranded split.")
    parser.add_argument("csv", type=Path, nargs="+", help="Search Console CSV files or folders containing them")
    parser.add_argument("--marca", "--brand", dest="marca", nargs="*", default=[], metavar="TERM",
                        help="brand terms (accent and case insensitive); a query containing one is branded")
    parser.add_argument("--periodo-previo", "--previous-period", dest="previo", type=Path, nargs="*", default=None,
                        help="CSV files or folders of the previous period, for loss and dead pages")
    parser.add_argument("--min-impresiones", "--min-impressions", dest="min_impr", type=int, default=50,
                        help="minimum impressions for a row to count (default 50)")
    parser.add_argument("--min-clics-previos", "--min-previous-clicks", dest="min_prev", type=int, default=5,
                        help="previous-period clicks for a page to count as dead when it drops to zero (default 5)")
    parser.add_argument("--json", action="store_true", help="print JSON instead of Markdown (keys stay in Spanish)")
    add_lang_arg(parser)
    args = parser.parse_args(argv)
    lang = resolve_lang(args.lang)
    t = _tr(lang)
    for path in [*args.csv, *(args.previo or [])]:
        if not path.exists():
            print(t("not_found", path=path), file=sys.stderr)
            return 1
    if not collect_csvs(args.csv):
        print(t("no_csv", paths=", ".join(map(str, args.csv))), file=sys.stderr)
        return 1
    now, warnings = load_period(args.csv, t)
    if not any(now.values()):
        print(t("no_rows") + "\n" + "\n".join(warnings), file=sys.stderr)
        return 1
    prev = None
    if args.previo:
        prev, prev_warnings = load_period(args.previo, t)
        warnings = [*warnings, *prev_warnings]
    brand_terms = [normalize_text(term) for term in args.marca if term.strip()]
    report = build_report(now, prev, brand_terms, args.min_impr, args.min_prev, warnings, t)
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.json else render_markdown(report, lang))
    return 0


if __name__ == "__main__":
    sys.exit(main())
