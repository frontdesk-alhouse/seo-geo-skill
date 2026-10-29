#!/usr/bin/env python3
"""Lo que ve un bot que NO ejecuta JavaScript: HTML crudo, JSON-LD, robots.txt, llms.txt.

Varios crawlers de IA no ejecutan JavaScript (ver references/ai-crawlers.md).
Si el copy clave, una lista CMS o el JSON-LD se inyectan con JS, para ellos no
existen. Este script, para cada User-Agent de la tabla de bots:

  - hace GET del HTML crudo y reporta status, tamaño y si los textos clave
    aparecen literalmente (sin acentos ni mayúsculas de por medio);
  - lista los @type de cada <script type="application/ld+json">;
  - evalúa /robots.txt con un parser propio (grupos User-agent, Allow/Disallow,
    gana el patrón más largo; empate gana Allow) para la ruta de la URL;
  - reporta /llms.txt y /sitemap.xml (status y tamaño);
  - detecta Cloudflare (cf-ray), challenges anti-bot y Content-Signal.

Severidad: ERROR si se bloquea un bot de búsqueda (Googlebot, Bingbot,
OAI-SearchBot, PerplexityBot, Claude-SearchBot) en robots o por firewall; AVISO
si se bloquea un fetch de usuario (ChatGPT-User, Claude-User, Perplexity-User);
INFO si se bloquea un bot de entrenamiento (decisión del cliente).

Limitación: el UA se imita desde tu IP. Cloudflare y otros verifican por IP, así
que un 403 aquí sugiere bloqueo pero el bot real puede pasar (o al revés).

Uso:
    python3 check_html_crudo.py https://www.ejemplo.mx --textos "cirujano de columna" "Monterrey"
    python3 check_html_crudo.py https://www.ejemplo.mx --bots GPTBot,OAI-SearchBot --json
    python3 check_html_crudo.py https://www.example.com --texts "spine surgeon" --lang en
Con --lang en la salida sale en inglés (AVISO pasa a WARN); las claves del JSON no cambian.
Sale con código 1 si hay algún ERROR (sirve como gate de lanzamiento).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import (BOT_UAS, UA_BROWSER, add_lang_arg, detect_challenge, error_label,  # noqa: E402
                    fetch, header, jsonld_types, make_translator, md_table, normalize_text,
                    parse_html, resolve_lang)

SEARCH_BOTS = ("Googlebot", "Bingbot", "OAI-SearchBot", "PerplexityBot", "Claude-SearchBot")
USER_FETCH_BOTS = ("ChatGPT-User", "Claude-User", "Perplexity-User")
TRAINING_TOKENS = ("GPTBot", "ClaudeBot", "Google-Extended", "Applebot-Extended",
                   "CCBot", "Bytespider", "meta-externalagent")
SEVERITY_EN = {"AVISO": "WARN"}

MESSAGES = {
    "es": {
        "i_get": "{bot}: GET respondió {status}", "i_challenge": " con challenge anti-bot",
        "i_robots": "robots.txt bloquea a {bot} ({rule}, grupo '{group}')",
        "i_missing_text": "texto clave ausente del HTML crudo: '{text}'",
        "i_no_jsonld": "ningún bloque JSON-LD en el HTML crudo (¿se inyecta con JS o no existe?)",
        "i_faq": "FAQPage presente: ya no produce rich result en Google (desde 2026-05-07); no es error",
        "i_robots_status": "/robots.txt respondió {status}",
        "i_sitemap": "/sitemap.xml no responde 200 (revisa la directiva Sitemap: de robots.txt)",
        "i_noindex": "cabecera X-Robots-Tag con noindex",
        "title": "# HTML crudo por bot\n\nURL: {url}",
        "none_types": "(ninguno)", "NO": "NO",
        "col_bot": "Bot", "col_status": "Status", "col_bytes": "Bytes", "col_challenge": "Challenge",
        "col_jsonld": "JSON-LD @type",
        "h_robots": "## robots.txt (ruta {path})",
        "col_token": "Token", "col_group": "Grupo", "col_allowed": "Permitido", "col_rule": "Regla",
        "col_severity": "Severidad",
        "h_aux": "## Archivos auxiliares", "col_file": "Archivo",
        "edge": ("## Borde\n\n- Cloudflare (cf-ray): {cf} · server: {server}\n"
                 "- Content-Signal en cabecera: {cs_header}\n"
                 "- Content-Signal en robots.txt: {cs_robots}\n"
                 "- X-Robots-Tag: {xrt} · challenge con UA de navegador: {challenge}"),
        "no_findings": "Sin hallazgos.",
        "h_findings": "## Hallazgos",
        "ip_note": "El UA se imita desde tu IP; un bloqueo por IP verificada no se ve aquí.",
        "bad_url": "error: la URL debe empezar con http:// o https://",
        "no_response": "error: el sitio no respondió a ningún bot ({error})",
        "rule_none": "(sin regla)",
    },
    "en": {
        "i_get": "{bot}: GET returned {status}", "i_challenge": " with an anti-bot challenge",
        "i_robots": "robots.txt blocks {bot} ({rule}, group '{group}')",
        "i_missing_text": "key text missing from the raw HTML: '{text}'",
        "i_no_jsonld": "no JSON-LD block in the raw HTML (injected with JS, or missing?)",
        "i_faq": "FAQPage present: it no longer produces a rich result in Google (since 2026-05-07); not an error",
        "i_robots_status": "/robots.txt returned {status}",
        "i_sitemap": "/sitemap.xml does not return 200 (check the Sitemap: directive in robots.txt)",
        "i_noindex": "X-Robots-Tag header with noindex",
        "title": "# Raw HTML by bot\n\nURL: {url}",
        "none_types": "(none)", "NO": "NO",
        "col_bot": "Bot", "col_status": "Status", "col_bytes": "Bytes", "col_challenge": "Challenge",
        "col_jsonld": "JSON-LD @type",
        "h_robots": "## robots.txt (path {path})",
        "col_token": "Token", "col_group": "Group", "col_allowed": "Allowed", "col_rule": "Rule",
        "col_severity": "Severity",
        "h_aux": "## Auxiliary files", "col_file": "File",
        "edge": ("## Edge\n\n- Cloudflare (cf-ray): {cf} · server: {server}\n"
                 "- Content-Signal header: {cs_header}\n"
                 "- Content-Signal in robots.txt: {cs_robots}\n"
                 "- X-Robots-Tag: {xrt} · challenge with a browser UA: {challenge}"),
        "no_findings": "No findings.",
        "h_findings": "## Findings",
        "ip_note": "The UA is spoofed from your IP; a block based on verified IPs does not show up here.",
        "bad_url": "error: the URL must start with http:// or https://",
        "no_response": "error: the site did not respond to any bot ({error})",
        "rule_none": "(no rule)",
    },
}


def _sev(severity: str | None, lang: str) -> str | None:
    """Severidad en el idioma de salida (AVISO es WARN en inglés)."""
    return SEVERITY_EN.get(severity, severity) if lang == "en" and severity else severity


# ---------------------------------------------------------------- robots.txt

def parse_robots(text: str) -> list[dict]:
    """Grupos [{'agents': [...], 'rules': [(allow:bool, patrón)]}]. Une grupos consecutivos de User-agent."""
    groups: list[dict] = []
    current = None
    expecting_agents = False
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        key, value = (part.strip() for part in line.split(":", 1))
        key = key.lower()
        if key == "user-agent":
            if not expecting_agents:
                current = {"agents": [], "rules": []}
                groups.append(current)
            current["agents"].append(value.lower())
            expecting_agents = True
        elif key in ("allow", "disallow") and current is not None:
            expecting_agents = False
            if value:  # 'Disallow:' vacío no bloquea nada
                current["rules"].append((key == "allow", value))
    return groups


def rules_for(groups: list[dict], token: str) -> tuple[list, str]:
    """Reglas del grupo que aplica al token (se unen grupos repetidos); si no hay, las de '*'."""
    token = token.lower()
    specific = [r for g in groups if token in g["agents"] for r in g["rules"]]
    if any(token in g["agents"] for g in groups):
        return specific, token
    return [r for g in groups if "*" in g["agents"] for r in g["rules"]], "*"


def _pattern_regex(pattern: str) -> re.Pattern:
    anchored = pattern.endswith("$")
    body = re.escape(pattern.rstrip("$")).replace(r"\*", ".*")
    return re.compile("^" + body + ("$" if anchored else ""))


def is_allowed(rules: list, path: str) -> tuple[bool, str]:
    """Gana el patrón más largo que coincide; en empate gana Allow. Sin coincidencias: permitido."""
    matches = [(len(p), allow, p) for allow, p in rules if _pattern_regex(p).match(path)]
    if not matches:
        return True, "(sin regla)"
    length, allow, pattern = max(matches, key=lambda m: (m[0], m[1]))
    return allow, ("Allow: " if allow else "Disallow: ") + pattern


def robots_verdicts(robots_text: str, path: str) -> list[dict]:
    groups = parse_robots(robots_text)
    verdicts = []
    for token in [*SEARCH_BOTS, *USER_FETCH_BOTS, *TRAINING_TOKENS]:
        rules, group = rules_for(groups, token)
        allowed, rule = is_allowed(rules, path)
        verdicts.append({"bot": token, "grupo": group, "permitido": allowed, "regla": rule,
                         "severidad": None if allowed else _severity(token)})
    return verdicts


def _severity(token: str) -> str:
    if token in SEARCH_BOTS:
        return "ERROR"
    return "AVISO" if token in USER_FETCH_BOTS else "INFO"


# ---------------------------------------------------------------- HTML por bot

def check_bot(url: str, bot: str, textos: list[str], timeout: float) -> dict:
    resp = fetch(url, ua=BOT_UAS[bot], timeout=timeout)
    parsed = parse_html(resp["body"])
    types, broken = jsonld_types(parsed.jsonld)
    plain = normalize_text(resp["body"])
    blocked = bool(resp["error"]) or (resp["status"] or 0) >= 400 or detect_challenge(resp)
    return {"bot": bot, "status": resp["status"], "error": resp["error"], "bytes": len(resp["body"]),
            "challenge": detect_challenge(resp), "bloqueado": blocked,
            "textos": {t: normalize_text(t) in plain for t in textos},
            "jsonld_tipos": sorted(set(types)), "jsonld_rotos": broken,
            "severidad": _severity(bot) if blocked else None}


def check_aux(base: str, timeout: float) -> dict:
    out = {}
    for name in ("robots.txt", "llms.txt", "sitemap.xml"):
        resp = fetch(urllib.parse.urljoin(base, "/" + name), ua=UA_BROWSER, timeout=timeout)
        out[name] = {"status": resp["status"], "error": resp["error"], "bytes": len(resp["body"]),
                     "body": resp["body"] if name == "robots.txt" and resp["status"] == 200 else ""}
    return out


def edge_signals(url: str, timeout: float, robots_text: str) -> dict:
    resp = fetch(url, ua=UA_BROWSER, timeout=timeout)
    signals = [ln.strip() for ln in robots_text.splitlines() if ln.lower().startswith("content-signal")]
    return {"cloudflare": header(resp["headers"], "cf-ray") is not None,
            "server": header(resp["headers"], "server"),
            "content_signal_header": header(resp["headers"], "content-signal"),
            "content_signal_robots": signals,
            "x_robots_tag": header(resp["headers"], "x-robots-tag"),
            "challenge_navegador": detect_challenge(resp)}


# ---------------------------------------------------------------- salida

def _status(item: dict, lang: str):
    return item["status"] or error_label(item["error"], lang)


def _rule(rule: str, lang: str) -> str:
    return make_translator(MESSAGES, lang)("rule_none") if rule == "(sin regla)" else rule


def collect_issues(rep: dict, lang: str = "es") -> list[tuple[str, str]]:
    """Hallazgos (severidad interna ERROR/AVISO/INFO, mensaje en el idioma pedido)."""
    t = make_translator(MESSAGES, lang)
    issues = [(b["severidad"], t("i_get", bot=b["bot"], status=_status(b, lang))
               + (t("i_challenge") if b["challenge"] else "")) for b in rep["bots"] if b["severidad"]]
    issues += [(v["severidad"], t("i_robots", bot=v["bot"], rule=_rule(v["regla"], lang), group=v["grupo"]))
               for v in rep["robots"] if v["severidad"]]
    missing = [x for b in rep["bots"] if not b["bloqueado"] for x, ok in b["textos"].items() if not ok]
    issues += [("ERROR", t("i_missing_text", text=x)) for x in sorted(set(missing))]
    if not any(b["jsonld_tipos"] for b in rep["bots"]):
        issues.append(("AVISO", t("i_no_jsonld")))
    if any("FAQPage" in b["jsonld_tipos"] for b in rep["bots"]):
        issues.append(("INFO", t("i_faq")))
    if rep["aux"]["robots.txt"]["status"] != 200:
        issues.append(("AVISO", t("i_robots_status", status=_status(rep["aux"]["robots.txt"], lang))))
    if rep["aux"]["sitemap.xml"]["status"] != 200:
        issues.append(("AVISO", t("i_sitemap")))
    if (rep["edge"]["x_robots_tag"] or "").lower().find("noindex") >= 0:
        issues.append(("ERROR", t("i_noindex")))
    return issues


def _render_robots(rep: dict, t, lang: str) -> str:
    yes = t("yes")
    rows = [[v["bot"], v["grupo"], yes if v["permitido"] else t("NO"), _rule(v["regla"], lang),
             _sev(v["severidad"], lang) or ""] for v in rep["robots"]]
    head = [t("col_token"), t("col_group"), t("col_allowed"), t("col_rule"), t("col_severity")]
    return t("h_robots", path=rep["ruta"]) + "\n\n" + md_table(head, rows)


def _render_edge(edge: dict, t) -> str:
    def yes_no(flag) -> str:
        return t("yes") if flag else t("no")
    return t("edge", cf=yes_no(edge["cloudflare"]), server=edge["server"],
             cs_header=edge["content_signal_header"] or t("no"),
             cs_robots="; ".join(edge["content_signal_robots"]) or t("no"),
             xrt=edge["x_robots_tag"] or t("no"), challenge=yes_no(edge["challenge_navegador"]))


def render_markdown(rep: dict, lang: str = "es") -> str:
    t = make_translator(MESSAGES, lang)
    textos = rep["textos"]
    yes, no = t("yes"), t("no")
    rows = [[b["bot"], _status(b, lang), b["bytes"], yes if b["challenge"] else no,
             *[yes if b["textos"][x] else t("NO") for x in textos], ", ".join(b["jsonld_tipos"]) or t("none_types")]
            for b in rep["bots"]]
    head = [t("col_bot"), t("col_status"), t("col_bytes"), t("col_challenge"), *[f"'{x}'" for x in textos],
            t("col_jsonld")]
    out = [t("title", url=rep["url"]), md_table(head, rows), _render_robots(rep, t, lang)]
    aux = [[k, _status(v, lang), v["bytes"]] for k, v in rep["aux"].items()]
    out.append(t("h_aux") + "\n\n" + md_table([t("col_file"), t("col_status"), t("col_bytes")], aux))
    out.append(_render_edge(rep["edge"], t))
    issues = "\n".join(f"- **{_sev(sev, lang)}** {msg}" for sev, msg in rep["hallazgos"]) or t("no_findings")
    out.append(t("h_findings") + "\n\n" + issues + "\n\n" + t("ip_note"))
    return "\n\n".join(out) + "\n"


def localize_json(rep: dict, lang: str) -> dict:
    """Copia del reporte para --json: sin cuerpos de archivos y con severidades en el idioma pedido."""
    aux = {k: {kk: vv for kk, vv in v.items() if kk != "body"} for k, v in rep["aux"].items()}
    if lang != "en":
        return {**rep, "aux": aux}
    return {**rep, "aux": aux,
            "bots": [{**b, "severidad": _sev(b["severidad"], lang)} for b in rep["bots"]],
            "robots": [{**v, "severidad": _sev(v["severidad"], lang), "regla": _rule(v["regla"], lang)}
                       for v in rep["robots"]],
            "hallazgos": [(_sev(sev, lang), msg) for sev, msg in rep["hallazgos"]]}


def parse_bots(value: str) -> list[str]:
    if value == "all":
        return list(BOT_UAS)
    wanted = [b.strip() for b in value.split(",") if b.strip()]
    unknown = [b for b in wanted if b not in BOT_UAS]
    if unknown:
        raise argparse.ArgumentTypeError(f"unknown bot(s): {', '.join(unknown)}; valid: {', '.join(BOT_UAS)}")
    return wanted


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fetch raw HTML as each AI/search bot (no JavaScript), check key texts, JSON-LD, robots.txt, llms.txt.")
    parser.add_argument("url", help="page URL (http/https)")
    parser.add_argument("--textos", "--texts", dest="textos", nargs="*", default=[],
                        help="key phrases that must appear in raw HTML")
    parser.add_argument("--bots", type=parse_bots, default=list(BOT_UAS), help="'all' or comma list, e.g. GPTBot,OAI-SearchBot")
    parser.add_argument("--timeout", type=float, default=15.0, help="seconds per request (default 15)")
    parser.add_argument("--json", action="store_true", help="print JSON instead of Markdown (keys stay in Spanish)")
    add_lang_arg(parser)
    args = parser.parse_args(argv)
    lang = resolve_lang(args.lang)
    t = make_translator(MESSAGES, lang)
    if not re.match(r"^https?://", args.url):
        print(t("bad_url"), file=sys.stderr)
        return 1
    parts = urllib.parse.urlparse(args.url)
    path = parts.path or "/"
    aux = check_aux(f"{parts.scheme}://{parts.netloc}/", args.timeout)
    rep = {"url": args.url, "ruta": path, "textos": args.textos,
           "bots": [check_bot(args.url, b, args.textos, args.timeout) for b in args.bots],
           "robots": robots_verdicts(aux["robots.txt"]["body"], path),
           "aux": aux, "edge": edge_signals(args.url, args.timeout, aux["robots.txt"]["body"])}
    rep = {**rep, "hallazgos": collect_issues(rep, lang)}
    if all(b["error"] and b["error"] != "demasiadas-redirecciones" for b in rep["bots"]):
        print(t("no_response", error=rep["bots"][0]["error"]), file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(localize_json(rep, lang), ensure_ascii=False, indent=2))
    else:
        print(render_markdown(rep, lang))
    return 1 if any(sev == "ERROR" for sev, _ in rep["hallazgos"]) else 0


if __name__ == "__main__":
    sys.exit(main())
