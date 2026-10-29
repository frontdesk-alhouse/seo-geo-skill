"""Utilidades compartidas por los scripts de seo-geo (solo biblioteca estándar).

No se ejecuta solo. Lo importan indice_citacion.py, verificar_fuentes.py,
check_html_crudo.py, verificar_metadata.py y generar_llms_txt.py.

Contiene:
- parse_frontmatter(): lector mínimo de frontmatter YAML (escalares y listas).
- fetch(): GET con User-Agent propio, tope de 5 redirecciones y timeout.
- HeadParser / extract_page_meta(): title, meta, canonical, h1, JSON-LD.
- read_sitemap(): sitemap.xml y sitemap index.
- md_table(), normalize_text(), wilson_interval().
"""
from __future__ import annotations

import gzip
import html
import json
import math
import re
import socket
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

MAX_REDIRECTS = 5
MAX_BYTES = 4_000_000

UA_BROWSER = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
)

# Cadenas aproximadas a las publicadas por cada operador. El token que decide
# en robots.txt es el nombre corto; varios operadores verifican además por IP,
# así que un GET desde tu máquina con este UA no es idéntico al bot real.
BOT_UAS = {
    "Googlebot": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Bingbot": "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "OAI-SearchBot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot",
    "ChatGPT-User": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ChatGPT-User/1.0; +https://openai.com/bot",
    "Claude-SearchBot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Claude-SearchBot/1.0; +https://www.anthropic.com)",
    "Claude-User": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Claude-User/1.0; +https://www.anthropic.com)",
    "PerplexityBot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)",
    "Perplexity-User": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Perplexity-User/1.0; +https://perplexity.ai/perplexity-user)",
    "GPTBot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.1; +https://openai.com/gptbot",
    "ClaudeBot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; ClaudeBot/1.0; +claudebot@anthropic.com)",
}

CHALLENGE_MARKERS = (
    "cf-chl", "challenge-platform", "just a moment...", "attention required! | cloudflare",
    "cf_chl_opt", "checking your browser", "verify you are human", "ddos-guard",
    "px-captcha", "captcha-delivery", "_incapsula_resource",
)


# ---------------------------------------------------------------- texto

def normalize_text(text: str) -> str:
    """Minúsculas, sin acentos y con espacios colapsados (para buscar nombres)."""
    decomposed = unicodedata.normalize("NFKD", text or "")
    plain = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", plain).strip().lower()


def html_to_text(raw: str) -> str:
    """Quita scripts, estilos y etiquetas; resuelve entidades."""
    no_code = re.sub(r"(?is)<(script|style|noscript)\b.*?</\1>", " ", raw or "")
    return html.unescape(re.sub(r"(?s)<[^>]+>", " ", no_code))


def md_table(headers: list[str], rows: list[list]) -> str:
    """Tabla Markdown; escapa barras verticales en las celdas."""
    def cell(value) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")
    lines = ["| " + " | ".join(cell(h) for h in headers) + " |",
             "|" + "|".join("---" for _ in headers) + "|"]
    lines += ["| " + " | ".join(cell(v) for v in row) + " |" for row in rows]
    return "\n".join(lines)


def wilson_interval(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Intervalo de Wilson para una proporción k/n (95 % por defecto)."""
    if n <= 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, center - half), min(1.0, center + half))


def fmt_prop(k: int, n: int) -> str:
    """'k/n · p % [lo-hi %]' con intervalo de Wilson."""
    if n == 0:
        return "0/0"
    lo, hi = wilson_interval(k, n)
    return f"{k}/{n} · {100 * k / n:.0f} % [{100 * lo:.0f}-{100 * hi:.0f} %]"


# ---------------------------------------------------------------- frontmatter

def _strip_inline_comment(value: str) -> str:
    """Quita ' # comentario' al final, respetando comillas y corchetes de lista."""
    quote = ""
    for i, ch in enumerate(value):
        if quote:
            quote = "" if ch == quote else quote
        elif ch in ("'", '"'):
            quote = ch
        elif ch == "#" and i > 0 and value[i - 1].isspace():
            return value[:i]
    return value


def _split_inline_list(body: str) -> list[str]:
    items, current, quote = [], "", ""
    for ch in body:
        if quote:
            current += ch
            quote = "" if ch == quote else quote
        elif ch in ("'", '"'):
            current += ch
            quote = ch
        elif ch == ",":
            items.append(current)
            current = ""
        else:
            current += ch
    items.append(current)
    return [i.strip() for i in items if i.strip()]


def parse_scalar(raw: str):
    """Convierte un escalar YAML simple: bool, null, int, cadena con o sin comillas."""
    value = raw.strip()
    if value == "" or value.lower() in ("null", "~"):
        return None
    if value.lower() in ("true", "false"):
        return value.lower() == "true"
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def _parse_value(raw: str):
    value = _strip_inline_comment(raw).strip()
    if value.startswith("[") and value.endswith("]"):
        return [parse_scalar(v) for v in _split_inline_list(value[1:-1])]
    return parse_scalar(value)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Devuelve (campos, cuerpo). Soporta 'clave: valor', listas [a, b] y listas con guiones."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("el archivo no abre con '---'")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration as exc:
        raise ValueError("frontmatter sin cierre '---'") from exc
    fields: dict = {}
    last_key = None
    for line in lines[1:end]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- ") and last_key is not None:
            previous = fields.get(last_key) or []
            fields[last_key] = [*previous, _parse_value(stripped[2:])]
            continue
        match = re.match(r"^([A-Za-z_][\w-]*)\s*:(.*)$", stripped)
        if not match:
            raise ValueError(f"línea no reconocida en frontmatter: {stripped!r}")
        last_key = match.group(1)
        fields[last_key] = _parse_value(match.group(2))
    return fields, "\n".join(lines[end + 1:])


# ---------------------------------------------------------------- red

class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D401
        return None


_OPENER = urllib.request.build_opener(_NoRedirect)


def _decode(raw: bytes, headers) -> str:
    if (headers.get("Content-Encoding") or "").lower() == "gzip":
        try:
            raw = gzip.decompress(raw)
        except OSError:
            pass
    charset = headers.get_content_charset() if hasattr(headers, "get_content_charset") else None
    return raw.decode(charset or "utf-8", errors="replace")


def _single_get(url: str, ua: str, timeout: float) -> dict:
    req = urllib.request.Request(url, headers={
        "User-Agent": ua, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "es-MX,es;q=0.9,en;q=0.8"})
    try:
        resp = _OPENER.open(req, timeout=timeout)
    except urllib.error.HTTPError as err:
        resp = err
    raw = resp.read(MAX_BYTES) if resp.fp is not None else b""
    return {"status": getattr(resp, "status", None) or getattr(resp, "code", None),
            "headers": dict(resp.headers.items()), "body": _decode(raw, resp.headers),
            "location": resp.headers.get("Location")}


def fetch(url: str, ua: str = UA_BROWSER, timeout: float = 15.0) -> dict:
    """GET siguiendo como máximo 5 redirecciones. Nunca reintenta.

    Devuelve dict con: url, final_url, status (int o None), headers, body,
    redirects (lista), error (None, 'timeout', 'demasiadas-redirecciones' o texto).
    """
    result = {"url": url, "final_url": url, "status": None, "headers": {},
              "body": "", "redirects": [], "error": None}
    current = url
    for _ in range(MAX_REDIRECTS + 1):
        try:
            resp = _single_get(current, ua, timeout)
        except (socket.timeout, TimeoutError):
            return {**result, "final_url": current, "error": "timeout"}
        except urllib.error.URLError as err:
            reason = err.reason
            kind = "timeout" if isinstance(reason, (socket.timeout, TimeoutError)) else str(reason)
            return {**result, "final_url": current, "error": kind}
        except (ValueError, OSError) as err:
            return {**result, "final_url": current, "error": str(err)}
        result = {**result, "final_url": current, "status": resp["status"],
                  "headers": resp["headers"], "body": resp["body"]}
        if resp["status"] in (301, 302, 303, 307, 308) and resp["location"]:
            nxt = urllib.parse.urljoin(current, resp["location"])
            result = {**result, "redirects": [*result["redirects"], nxt]}
            current = nxt
            continue
        return result
    return {**result, "error": "demasiadas-redirecciones"}


def header(headers: dict, name: str) -> str | None:
    """Lee una cabecera sin importar mayúsculas."""
    lowered = name.lower()
    return next((v for k, v in headers.items() if k.lower() == lowered), None)


def detect_challenge(resp: dict) -> bool:
    """True si la respuesta parece un challenge anti-bot (Cloudflare u otros)."""
    if (header(resp["headers"], "cf-mitigated") or "").lower() == "challenge":
        return True
    head = (resp.get("body") or "")[:20000].lower()
    return any(marker in head for marker in CHALLENGE_MARKERS)


# ---------------------------------------------------------------- HTML

class HeadParser(HTMLParser):
    """Extrae title, meta, link rel, h1, lang, primer <p> y bloques JSON-LD."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title, self.lang, self.first_p = "", None, ""
        self.metas: list[dict] = []
        self.links: list[dict] = []
        self.h1: list[str] = []
        self.jsonld: list[str] = []
        self._stack: list[str] = []
        self._buffer = ""

    def handle_starttag(self, tag, attrs):
        attr = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html" and self.lang is None:
            self.lang = attr.get("lang") or None
        elif tag == "meta":
            self.metas.append(attr)
        elif tag == "link":
            self.links.append(attr)
        is_ld = tag == "script" and "ld+json" in attr.get("type", "").lower()
        if tag in ("title", "h1", "p") or is_ld:
            self._stack.append("ld" if is_ld else tag)
            self._buffer = ""

    def handle_data(self, data):
        if self._stack:
            self._buffer += data

    def handle_endtag(self, tag):
        if not self._stack:
            return
        kind = self._stack[-1]
        if tag != ("script" if kind == "ld" else kind):
            return
        self._stack.pop()
        text = self._buffer if kind == "ld" else re.sub(r"\s+", " ", self._buffer).strip()
        self._store(kind, text)
        self._buffer = ""

    def _store(self, kind: str, text: str) -> None:
        if kind == "title" and not self.title:
            self.title = text
        elif kind == "h1":
            self.h1.append(text)
        elif kind == "p" and not self.first_p and len(text) > 40:
            self.first_p = text
        elif kind == "ld":
            self.jsonld.append(text)


def parse_html(raw: str) -> HeadParser:
    parser = HeadParser()
    try:
        parser.feed(raw or "")
        parser.close()
    except Exception:  # HTML roto: devolvemos lo que se alcanzó a leer
        pass
    return parser


def meta_content(parser: HeadParser, key: str) -> str | None:
    """Busca <meta name|property=key content=...>."""
    key = key.lower()
    for meta in parser.metas:
        if (meta.get("name") or meta.get("property") or "").lower() == key:
            return meta.get("content", "")
    return None


def jsonld_types(blocks: list[str]) -> tuple[list[str], int]:
    """Lista de @type encontrados y número de bloques que no parsean como JSON."""
    types: list[str] = []
    broken = 0

    def walk(node) -> None:
        if isinstance(node, dict):
            t = node.get("@type")
            types.extend(t if isinstance(t, list) else [t] if t else [])
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    for block in blocks:
        try:
            walk(json.loads(block))
        except json.JSONDecodeError:
            broken += 1
    return [str(t) for t in types], broken


# ---------------------------------------------------------------- sitemap y listas

def parse_sitemap_xml(body: str) -> tuple[list[str], list[str]]:
    """Devuelve (urls, sitemaps_hijos) de un sitemap o sitemap index."""
    root = ET.fromstring(body.strip().encode("utf-8"))
    tag = root.tag.split("}")[-1]
    locs = [el.text.strip() for el in root.iter() if el.tag.split("}")[-1] == "loc" and el.text]
    return ([], locs) if tag == "sitemapindex" else (locs, [])


def read_sitemap(url: str, timeout: float = 15.0, limit: int = 500, depth: int = 0) -> list[str]:
    """Lee un sitemap (y sus hijos si es index, hasta 2 niveles). Lanza RuntimeError si falla."""
    resp = fetch(url, timeout=timeout)
    if resp["error"] or resp["status"] != 200:
        raise RuntimeError(f"no se pudo leer {url}: {resp['error'] or resp['status']}")
    try:
        urls, children = parse_sitemap_xml(resp["body"])
    except ET.ParseError as exc:
        raise RuntimeError(f"{url} no es XML válido: {exc}") from exc
    for child in children:
        if len(urls) >= limit or depth >= 2:
            break
        urls = [*urls, *read_sitemap(child, timeout, limit - len(urls), depth + 1)]
    return list(dict.fromkeys(urls))[:limit]


def read_url_list(path: Path) -> list[str]:
    """Una URL por línea; ignora vacías y comentarios con '#'."""
    lines = path.read_text(encoding="utf-8").splitlines()
    return [ln.strip() for ln in lines if ln.strip() and not ln.strip().startswith("#")]


def resolve_targets(target: str, timeout: float, limit: int) -> list[str]:
    """Acepta URL de sitemap, archivo con URLs o una URL suelta."""
    path = Path(target)
    if path.is_file():
        return read_url_list(path)[:limit]
    if not re.match(r"^https?://", target):
        raise RuntimeError(f"'{target}' no es archivo ni URL http(s)")
    if urllib.parse.urlparse(target).path.lower().endswith(".xml"):
        return read_sitemap(target, timeout, limit)
    return [target]
