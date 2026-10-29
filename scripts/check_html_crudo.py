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
from _comun import (BOT_UAS, UA_BROWSER, detect_challenge, fetch, header,  # noqa: E402
                    jsonld_types, md_table, normalize_text, parse_html)

SEARCH_BOTS = ("Googlebot", "Bingbot", "OAI-SearchBot", "PerplexityBot", "Claude-SearchBot")
USER_FETCH_BOTS = ("ChatGPT-User", "Claude-User", "Perplexity-User")
TRAINING_TOKENS = ("GPTBot", "ClaudeBot", "Google-Extended", "Applebot-Extended",
                   "CCBot", "Bytespider", "meta-externalagent")


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

def collect_issues(rep: dict) -> list[tuple[str, str]]:
    issues = [(b["severidad"], f"{b['bot']}: GET respondió {b['status'] or b['error']}"
               + (" con challenge anti-bot" if b["challenge"] else "")) for b in rep["bots"] if b["severidad"]]
    issues += [(v["severidad"], f"robots.txt bloquea a {v['bot']} ({v['regla']}, grupo '{v['grupo']}')")
               for v in rep["robots"] if v["severidad"]]
    missing = [t for b in rep["bots"] if not b["bloqueado"] for t, ok in b["textos"].items() if not ok]
    issues += [("ERROR", f"texto clave ausente del HTML crudo: '{t}'") for t in sorted(set(missing))]
    if not any(b["jsonld_tipos"] for b in rep["bots"]):
        issues.append(("AVISO", "ningún bloque JSON-LD en el HTML crudo (¿se inyecta con JS o no existe?)"))
    if any("FAQPage" in b["jsonld_tipos"] for b in rep["bots"]):
        issues.append(("INFO", "FAQPage presente: ya no produce rich result en Google (desde 2026-05-07); no es error"))
    if rep["aux"]["robots.txt"]["status"] != 200:
        issues.append(("AVISO", f"/robots.txt respondió {rep['aux']['robots.txt']['status'] or rep['aux']['robots.txt']['error']}"))
    if rep["aux"]["sitemap.xml"]["status"] != 200:
        issues.append(("AVISO", "/sitemap.xml no responde 200 (revisa la directiva Sitemap: de robots.txt)"))
    if (rep["edge"]["x_robots_tag"] or "").lower().find("noindex") >= 0:
        issues.append(("ERROR", "cabecera X-Robots-Tag con noindex"))
    return issues


def render_markdown(rep: dict) -> str:
    textos = rep["textos"]
    rows = [[b["bot"], b["status"] or b["error"], b["bytes"], "sí" if b["challenge"] else "no",
             *["sí" if b["textos"][t] else "NO" for t in textos], ", ".join(b["jsonld_tipos"]) or "(ninguno)"]
            for b in rep["bots"]]
    out = [f"# HTML crudo por bot\n\nURL: {rep['url']}",
           md_table(["Bot", "Status", "Bytes", "Challenge", *[f"'{t}'" for t in textos], "JSON-LD @type"], rows)]
    rrows = [[v["bot"], v["grupo"], "sí" if v["permitido"] else "NO", v["regla"], v["severidad"] or ""]
             for v in rep["robots"]]
    out.append(f"## robots.txt (ruta {rep['ruta']})\n\n" + md_table(["Token", "Grupo", "Permitido", "Regla", "Severidad"], rrows))
    aux = [[k, v["status"] or v["error"], v["bytes"]] for k, v in rep["aux"].items()]
    out.append("## Archivos auxiliares\n\n" + md_table(["Archivo", "Status", "Bytes"], aux))
    edge = rep["edge"]
    out.append(f"## Borde\n\n- Cloudflare (cf-ray): {'sí' if edge['cloudflare'] else 'no'} · server: {edge['server']}\n"
               f"- Content-Signal en cabecera: {edge['content_signal_header'] or 'no'}\n"
               f"- Content-Signal en robots.txt: {'; '.join(edge['content_signal_robots']) or 'no'}\n"
               f"- X-Robots-Tag: {edge['x_robots_tag'] or 'no'} · challenge con UA de navegador: "
               f"{'sí' if edge['challenge_navegador'] else 'no'}")
    issues = "\n".join(f"- **{sev}** {msg}" for sev, msg in rep["hallazgos"]) or "Sin hallazgos."
    out.append("## Hallazgos\n\n" + issues + "\n\nEl UA se imita desde tu IP; un bloqueo por IP verificada no se ve aquí.")
    return "\n\n".join(out) + "\n"


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
    parser.add_argument("--textos", nargs="*", default=[], help="key phrases that must appear in raw HTML")
    parser.add_argument("--bots", type=parse_bots, default=list(BOT_UAS), help="'all' or comma list, e.g. GPTBot,OAI-SearchBot")
    parser.add_argument("--timeout", type=float, default=15.0, help="seconds per request (default 15)")
    parser.add_argument("--json", action="store_true", help="print JSON instead of Markdown")
    args = parser.parse_args(argv)
    if not re.match(r"^https?://", args.url):
        print("error: la URL debe empezar con http:// o https://", file=sys.stderr)
        return 1
    parts = urllib.parse.urlparse(args.url)
    path = parts.path or "/"
    aux = check_aux(f"{parts.scheme}://{parts.netloc}/", args.timeout)
    rep = {"url": args.url, "ruta": path, "textos": args.textos,
           "bots": [check_bot(args.url, b, args.textos, args.timeout) for b in args.bots],
           "robots": robots_verdicts(aux["robots.txt"]["body"], path),
           "aux": aux, "edge": edge_signals(args.url, args.timeout, aux["robots.txt"]["body"])}
    rep = {**rep, "hallazgos": collect_issues(rep)}
    if all(b["error"] and b["error"] != "demasiadas-redirecciones" for b in rep["bots"]):
        print(f"error: el sitio no respondió a ningún bot ({rep['bots'][0]['error']})", file=sys.stderr)
        return 1
    if args.json:
        slim = {**rep, "aux": {k: {kk: vv for kk, vv in v.items() if kk != "body"} for k, v in aux.items()}}
        print(json.dumps(slim, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(rep))
    return 1 if any(sev == "ERROR" for sev, _ in rep["hallazgos"]) else 0


if __name__ == "__main__":
    sys.exit(main())
