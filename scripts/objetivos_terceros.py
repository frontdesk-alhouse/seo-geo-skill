#!/usr/bin/env python3
"""Del censo de fuentes a una lista de objetivos de terceros (paso 8).

Lee la misma carpeta de corridas que indice_citacion.py (usa su lector y su
validación, no los duplica) y arma la tabla de candidatos: páginas de terceros
que los asistentes citan cuando responden consultas SIN marca y el cliente
falta o aparece poco.

Por URL citada:
  - dominio, URL, consultas y asistentes donde pesa;
  - corridas sin marca que la citan y, de ellas, en cuántas faltó el cliente;
  - nombres que dio el asistente en esas corridas (no son los de la página:
    lo que la página lista se comprueba abriéndola);
  - estado de verificación si pasas el JSON de verificar_fuentes.py;
  - columnas vacías para curar a mano: tipo, ángulo, contacto, prioridad.

Orden: corridas sin cliente (desc), corridas que la citan (desc), dominio.
Las consultas de marca (F3 o --marca) no entran. Los dominios propios
(--dominio-propio) y de competidores (--competidores) se excluyen, con sus
subdominios.

Método completo: references/censo-a-accion.md

Uso:
    python3 objetivos_terceros.py examples/corridas-ejemplo
    python3 objetivos_terceros.py corridas/ --dominio-propio draelenaruiz.example.com \\
        --competidores competidor-uno.example.com --nombre "Elena Ruiz"
    python3 verificar_fuentes.py corridas/ --nombre "Elena Ruiz" --json > verif.json
    python3 objetivos_terceros.py corridas/ --verificacion verif.json --json
    python3 objetivos_terceros.py runs/ --own-domain example.com --competitors rival.com --lang en
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import add_lang_arg, make_translator, md_table, normalize_text, resolve_lang  # noqa: E402
from indice_citacion import _domain, _qnum, is_brand, load_runs  # noqa: E402

CLASS_EN = {"viva-y-nombra": "alive-names", "viva-no-nombra": "alive-no-name",
            "bloqueo-anti-bot": "anti-bot-block", "muerta": "dead", "timeout": "timeout"}
CLASS_ES = {en: es for es, en in CLASS_EN.items()}

MESSAGES = {
    "es": {
        "title": ("# Objetivos de terceros\n\n{runs} corridas sin marca leídas · {absent} sin el cliente · "
                  "{targets} URLs de terceros candidatas en {domains} dominios.\n"),
        "h_targets": "## 1. Candidatos (una fila por URL)",
        "col_domain": "Dominio", "col_url": "URL", "col_type": "Tipo", "col_queries": "Consultas",
        "col_assistants": "Asistentes", "col_cited": "Corridas que la citan", "col_absent": "Sin cliente",
        "col_names": "Nombrados en esas respuestas", "col_state": "Verificación", "col_angle": "Ángulo",
        "col_contact": "Contacto", "col_priority": "Prioridad",
        "h_domains": "## 2. Resumen por dominio",
        "col_urls": "URLs", "col_client_in": "Con cliente",
        "empty": "Ninguna URL de tercero citada en consultas sin marca.",
        "not_opened": "sin abrir",
        "curate_note": ("Tipo, ángulo, contacto y prioridad se curan a mano (ver `references/censo-a-accion.md`). "
                        "Contacto: solo verificado en la página del sitio; si no, `sin verificar`. "
                        "\"Nombrados\" es lo que dijo el asistente, no lo que lista la página: ábrela."),
        "h_warnings": "## 3. Advertencias", "none": "Ninguna.",
        "no_verification": "sin --verificacion: ninguna URL consta como abierta; corre verificar_fuentes.py antes de curar",
        "not_in_verification": "{count} URLs candidatas no están en el JSON de verificación",
        "verif_unreadable": "error: no se pudo leer {path} ({exc})",
        "not_dir": "error: {path} no es una carpeta",
        "no_valid": "error: ninguna corrida válida.",
        "no_unbranded": "error: no hay corridas sin marca; el paso 8 parte de F1, F2, F4 y opcionales.",
    },
    "en": {
        "title": ("# Third-party targets\n\n{runs} unbranded runs read · {absent} without the client · "
                  "{targets} third-party candidate URLs on {domains} domains.\n"),
        "h_targets": "## 1. Candidates (one row per URL)",
        "col_domain": "Domain", "col_url": "URL", "col_type": "Type", "col_queries": "Queries",
        "col_assistants": "Assistants", "col_cited": "Runs citing it", "col_absent": "Without client",
        "col_names": "Named in those answers", "col_state": "Verification", "col_angle": "Angle",
        "col_contact": "Contact", "col_priority": "Priority",
        "h_domains": "## 2. Summary by domain",
        "col_urls": "URLs", "col_client_in": "With client",
        "empty": "No third-party URL cited in unbranded queries.",
        "not_opened": "not opened",
        "curate_note": ("Type, angle, contact and priority are curated by hand (see "
                        "`references/citation-census-to-action.md`). Contact: only verified on the site itself; "
                        "otherwise `unverified`. \"Named\" is what the assistant said, not what the page lists: open it."),
        "h_warnings": "## 3. Warnings", "none": "None.",
        "no_verification": "no --verification: no URL is recorded as opened; run verificar_fuentes.py before curating",
        "not_in_verification": "{count} candidate URLs are not in the verification JSON",
        "verif_unreadable": "error: could not read {path} ({exc})",
        "not_dir": "error: {path} is not a folder",
        "no_valid": "error: no valid runs.",
        "no_unbranded": "error: no unbranded runs; step 8 starts from F1, F2, F4 and the optional families.",
    },
}


def _tr(lang: str):
    return make_translator(MESSAGES, lang)


def _clean_domain(value: str) -> str:
    """Acepta 'https://www.x.com/ruta' o 'x.com' y devuelve 'x.com'."""
    text = value.strip().lower()
    return _domain(text if "://" in text else f"https://{text}")


def is_excluded(domain: str, excluded: set[str]) -> bool:
    return any(domain == d or domain.endswith("." + d) for d in excluded)


def load_verification(path: Path) -> dict[str, str]:
    """URL → clase (en español) a partir del JSON de verificar_fuentes.py."""
    data = json.loads(path.read_text(encoding="utf-8"))
    states = {}
    for row in data.get("urls", []):
        results = row.get("resultados") or []
        if results:
            clase = str(results[0].get("clase", ""))
            states[row["url"]] = CLASS_ES.get(clase, clase)
    return states


def _names_without_client(names: list, client_names: list[str]) -> list[str]:
    keys = [normalize_text(n) for n in client_names if n]
    return [str(n) for n in names if not any(k in normalize_text(str(n)) for k in keys)]


def build_targets(runs: list[dict], brand_ids: set[str], excluded: set[str],
                  client_names: list[str]) -> tuple[list[dict], list[dict]]:
    """Devuelve (filas por URL, resumen por dominio) sobre corridas sin marca."""
    by_url: dict[str, dict] = {}
    for run in (r for r in runs if not is_brand(r, brand_ids)):
        for url in sorted(set(map(str, run["urls_citadas"]))):
            dom = _domain(url)
            if is_excluded(dom, excluded):
                continue
            entry = by_url.get(url, {"url": url, "dominio": dom, "consultas": set(), "asistentes": set(),
                                     "corridas": 0, "sin_cliente": 0, "nombrados": {}})
            named = {**entry["nombrados"]}
            for name in _names_without_client(run["nombres"], client_names):
                named[name] = named.get(name, 0) + 1
            by_url[url] = {**entry, "consultas": entry["consultas"] | {run["consulta"]},
                           "asistentes": entry["asistentes"] | {run["asistente"]},
                           "corridas": entry["corridas"] + 1,
                           "sin_cliente": entry["sin_cliente"] + int(not run["aparece"]),
                           "nombrados": named}
    rows = [{**e, "consultas": sorted(e["consultas"], key=_qnum), "asistentes": sorted(e["asistentes"]),
             "nombrados": [n for n, _ in sorted(e["nombrados"].items(), key=lambda kv: (-kv[1], kv[0]))],
             "tipo": "", "angulo": "", "contacto": "", "prioridad": ""}
            for e in by_url.values()]
    rows.sort(key=lambda e: (-e["sin_cliente"], -e["corridas"], e["dominio"], e["url"]))
    return rows, _domain_summary(rows)


def _domain_summary(rows: list[dict]) -> list[dict]:
    summary: dict[str, dict] = {}
    for row in rows:
        entry = summary.get(row["dominio"], {"dominio": row["dominio"], "urls": 0, "corridas": 0, "sin_cliente": 0})
        summary[row["dominio"]] = {**entry, "urls": entry["urls"] + 1, "corridas": entry["corridas"] + row["corridas"],
                                   "sin_cliente": entry["sin_cliente"] + row["sin_cliente"]}
    return sorted(summary.values(), key=lambda e: (-e["sin_cliente"], -e["corridas"], e["dominio"]))


def attach_verification(rows: list[dict], states: dict[str, str] | None) -> tuple[list[dict], int]:
    if states is None:
        return [{**r, "verificacion": None} for r in rows], 0
    missing = sum(1 for r in rows if r["url"] not in states)
    return [{**r, "verificacion": states.get(r["url"])} for r in rows], missing


def render_markdown(rep: dict, lang: str = "es") -> str:
    t = _tr(lang)
    out = [t("title", runs=rep["corridas_sin_marca"], absent=rep["corridas_sin_cliente"],
             targets=len(rep["objetivos"]), domains=len(rep["dominios"]))]
    if not rep["objetivos"]:
        return "\n\n".join([*out, t("empty")]) + "\n"

    def state(value: str | None) -> str:
        if value is None:
            return t("not_opened")
        return CLASS_EN.get(value, value) if lang == "en" else value

    head = [t("col_domain"), t("col_url"), t("col_type"), t("col_queries"), t("col_assistants"), t("col_cited"),
            t("col_absent"), t("col_names"), t("col_state"), t("col_angle"), t("col_contact"), t("col_priority")]
    rows = [[r["dominio"], r["url"], "", ", ".join(r["consultas"]), ", ".join(r["asistentes"]), r["corridas"],
             r["sin_cliente"], ", ".join(r["nombrados"][:5]), state(r["verificacion"]), "", "", ""]
            for r in rep["objetivos"]]
    out.append(f"{t('h_targets')}\n\n{md_table(head, rows)}\n\n{t('curate_note')}")
    dom_head = [t("col_domain"), t("col_urls"), t("col_cited"), t("col_absent")]
    dom_rows = [[d["dominio"], d["urls"], d["corridas"], d["sin_cliente"]] for d in rep["dominios"]]
    out.append(f"{t('h_domains')}\n\n{md_table(dom_head, dom_rows)}")
    warnings = "\n".join(f"- {w}" for w in rep["advertencias"]) or t("none")
    out.append(f"{t('h_warnings')}\n\n{warnings}")
    return "\n\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Third-party target list from AI-assistant runs: pages cited in unbranded queries where the "
                    "client is missing (step 8).")
    parser.add_argument("dir_corridas", type=Path, help="folder with run files (*.md), same as indice_citacion.py")
    parser.add_argument("--dominio-propio", "--own-domain", dest="propios", nargs="*", default=[], metavar="DOMAIN",
                        help="client domains to exclude (subdomains included)")
    parser.add_argument("--competidores", "--competitors", dest="competidores", nargs="*", default=[],
                        metavar="DOMAIN", help="competitor domains to exclude (subdomains included)")
    parser.add_argument("--nombre", "--name", dest="nombre", action="append", default=[],
                        help="client name, to drop it from the 'named in those answers' column; repeatable")
    parser.add_argument("--marca", "--brand", dest="marca", nargs="*", default=[], metavar="ID-NN",
                        help="extra query ids to treat as branded (F3 is always branded)")
    parser.add_argument("--verificacion", "--verification", dest="verificacion", type=Path, default=None,
                        help="JSON from `verificar_fuentes.py --json` to fill the verification column")
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
    brand_ids = set(args.marca)
    unbranded = [r for r in runs if not is_brand(r, brand_ids)]
    if not unbranded:
        print(t("no_unbranded"), file=sys.stderr)
        return 1
    states = None
    if args.verificacion is not None:
        try:
            states = load_verification(args.verificacion)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            print(t("verif_unreadable", path=args.verificacion, exc=exc), file=sys.stderr)
            return 1
    excluded = {_clean_domain(d) for d in [*args.propios, *args.competidores] if d.strip()}
    rows, domains = build_targets(runs, brand_ids, excluded, args.nombre)
    rows, missing = attach_verification(rows, states)
    notes = [t("no_verification")] if states is None else (
        [t("not_in_verification", count=missing)] if missing else [])
    report = {"corridas_sin_marca": len(unbranded),
              "corridas_sin_cliente": sum(1 for r in unbranded if not r["aparece"]),
              "excluidos": sorted(excluded), "objetivos": rows, "dominios": domains,
              "advertencias": [*warnings, *notes]}
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.json else render_markdown(report, lang))
    return 0


if __name__ == "__main__":
    sys.exit(main())
