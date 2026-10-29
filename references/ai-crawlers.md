# Bots de IA: robots.txt, Cloudflare y HTML crudo

> Qué bot hace qué, qué se permite por defecto, cómo se aplica en cualquier plataforma, y cómo
> comprobar que lo que el bot recibe es lo que el cliente cree que publicó.
> Etiquetas como en `geo-evidencia.md`: [E] estudio · [O] oficial · [S] inferencia o vendor.

---

## 1. Los tres roles

Cada empresa de IA tiene (o debería tener) un bot por rol. Confundirlos es el error más común:
bloquear "a OpenAI" para no entrenar y, de paso, salir de ChatGPT Search.

| Rol | Qué hace | Si lo bloqueas |
|---|---|---|
| **Entrenamiento** | Junta corpus para entrenar modelos | No sales de las respuestas con búsqueda; dejas de aportar al conocimiento base del modelo |
| **Índice de búsqueda** | Construye el índice que el asistente consulta al responder | **Sales de las respuestas con búsqueda** de ese asistente |
| **Fetch de usuario** | Abre una URL porque un usuario lo pidió en el chat | El asistente no puede leer tu página cuando alguien se la pasa; varios declaran que robots.txt puede no aplicar |

## 2. Tabla oficial de tokens

| Token | Empresa | Rol | Etiqueta y fuente |
|---|---|---|---|
| `GPTBot` | OpenAI | Entrenamiento | [O] https://developers.openai.com/api/docs/bots |
| `OAI-SearchBot` | OpenAI | Índice de ChatGPT search; bloquearlo te saca de respuestas de búsqueda; cambios se reflejan en ~24 h | [O] misma página |
| `ChatGPT-User` | OpenAI | Fetch de usuario; "robots.txt rules may not apply" | [O] misma página |
| `OAI-AdsBot` | OpenAI | Revisión de landing pages de anuncios | [O] misma página |
| `ClaudeBot` | Anthropic | Entrenamiento | [O] https://support.claude.com/en/articles/8896518 |
| `Claude-SearchBot` | Anthropic | Índice de búsqueda | [O] misma página |
| `Claude-User` | Anthropic | Fetch de usuario | [O] misma página |
| `PerplexityBot` | Perplexity | Índice de búsqueda; "not used to crawl content for AI foundation models" | [O] https://docs.perplexity.ai/guides/bots |
| `Perplexity-User` | Perplexity | Fetch de usuario; "generally ignores robots.txt" | [O] misma página |
| `Googlebot` | Google | Búsqueda, AIO y AI Mode | [O] |
| `Google-Extended` | Google | Token (no es crawler aparte) para entrenamiento y grounding de Gemini; no afecta inclusión ni ranking en Search, AIO ni AI Mode | [O] https://developers.google.com/search/docs/appearance/ai-features |
| `Bingbot` | Microsoft | Búsqueda Bing y Copilot | [O] |
| `Applebot-Extended` | Apple | Opt-out de entrenamiento de Apple; no afecta ranking | [O] https://support.apple.com/en-us/119829 |
| `meta-externalagent` | Meta | Meta AI | [O] |
| `CCBot` | Common Crawl | Corpus abierto que usan muchos entrenamientos | [S] |
| `Bytespider` | ByteDance | Entrenamiento | [S] |

**Errores que circulan y no se repiten:** "GPTBot alimenta ChatGPT Search" (falso: es
OAI-SearchBot); `anthropic-ai` como token vigente (retirado); llamar "FacebookBot" al bot de Meta
AI; describir `GoogleOther` como bot de IA; omitir `Claude-SearchBot`, `Claude-User` y
`Perplexity-User`.

Sobre Claude: su búsqueda usa Brave Search como backend (subprocesador declarado desde 2025-03-19)
[O]. Estar en el índice de Brave importa para Claude aunque no esté en tu robots.txt.

## 3. Política por defecto: permitir todo

**Default del skill: no se bloquea ningún bot de IA.** Plantilla: `templates/robots-ai-permitir.txt`.

Razón: para un consultorio, una industria o un SaaS en México, el problema es que no los conozcan,
no que los copien. Bloquear entrenamiento quita al cliente del conocimiento base del modelo, que es
de donde salen las respuestas cuando el asistente **no** busca (Claude buscó solo en 36.6% de los
prompts en 8ight.AI, 2026-10 [E, muestra chica]). El costo de permitir es bajo: el contenido ya es
público y está hecho para circular.

## 4. Variante: opt-out de entrenamiento

Plantilla: `templates/robots-ai-optout-entrenamiento.txt`. Para clientes con contenido propietario
(investigación, cursos, datos de pago) o que lo piden explícitamente.

```
# Búsqueda y fetch de usuario: PERMITIR
User-agent: Googlebot
User-agent: Bingbot
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Perplexity-User
Allow: /

# Entrenamiento: BLOQUEAR (decisión del cliente)
User-agent: GPTBot
User-agent: ClaudeBot
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: CCBot
User-agent: Bytespider
Disallow: /
```

**Costo declarado, y se le dice al cliente por escrito:** el modelo deja de aprender del sitio en
entrenamientos futuros. Las respuestas sin búsqueda dependerán solo de lo que terceros digan de él.
No lo saca de AIO ni AI Mode (eso solo lo haría bloquear Googlebot) [O].

**Content-Signals** (contentsignals.org) permite declarar intención en el mismo robots.txt, por
ejemplo `Content-Signal: ai-train=no, search=yes`. Es una declaración, no un bloqueo técnico; su
respeto depende de cada empresa [S]. Se puede agregar en ambas plantillas sin riesgo.

## 5. Cloudflare: el riesgo está en la zona del cliente

Las plataformas alojadas (por ejemplo Webflow y Framer) sirven el sitio desde su propia infraestructura. El problema aparece cuando el
cliente (o su proveedor de TI) pone **su propia zona de Cloudflare con proxy naranja** delante del
dominio. Entonces manda la configuración de esa zona, no la de robots.txt.

| Fecha | Cambio | Etiqueta |
|---|---|---|
| 2025-07-01 | Zonas nuevas bloquean bots de IA por defecto; pay-per-crawl (HTTP 402) en beta | [O] |
| 2025-08-04 | Cloudflare acusa a Perplexity de crawlers encubiertos y lo retira como bot verificado | [O] |
| 2026-09-15 | Control "Disallow AI Training": en modo Block puede frenar también Googlebot, Bingbot y Applebot, incluida búsqueda | [O] ⚠️ cobertura secundaria |

Auditoría (pedir acceso o captura al cliente):

1. `dig +short dominio.com` y revisar si responde una IP de Cloudflare.
2. En el dashboard: Security → Bots y AI Crawl Control. Buscar bloqueos a bots de búsqueda de IA y
   el estado de "Disallow AI Training".
3. Ver si Cloudflare está **reescribiendo** robots.txt (robots gestionado): el archivo servido no
   coincide con el que se escribió en la plataforma.
4. Confirmar con `scripts/check_html_crudo.py` que cada bot de búsqueda recibe 200, no 403 ni 402.

## 6. Cómo aplicarlo

Dónde se edita robots.txt en cada plataforma (WordPress, Shopify, Squarespace, Wix, Webflow,
Framer, frameworks y HTML propio): `plataformas.md`. Abajo, el detalle de Webflow y Framer.

**Webflow.** Site Settings → SEO → robots.txt. Se pega el contenido completo de la plantilla y se
publica. Agregar al final `Sitemap: https://dominio.com/sitemap.xml`. El staging `.webflow.io`
lleva su propio noindex (ver `checklist-lanzamiento.md`), no se toca desde aquí. Hay reportes
de soporte de Content-Signal ⚠️; verificar en el archivo servido.

**Framer.** robots.txt personalizado vía **Static Files**, disponible en planes Pro y Enterprise
[O] https://www.framer.com/help/articles/how-can-i-access-the-robots-txt-file . En planes menores
se queda el robots.txt generado por Framer; verificar que no bloquee nada y documentarlo como
limitación.

**Siempre:** después de publicar, `curl -s https://dominio.com/robots.txt` y comparar con la
plantilla. Lo que importa es lo servido.

## 7. El check de HTML crudo

Los bots de IA **no ejecutan JavaScript**: GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, los de
Meta y Bytespider solo leen el HTML que devuelve el servidor [E] Vercel/MERJ, dic 2024,
https://vercel.com/blog/the-rise-of-the-ai-crawler . Googlebot sí renderiza, por eso un sitio puede
verse perfecto en Search Console y vacío para ChatGPT.

Qué se rompe, con ejemplos de Webflow y Framer (el patrón aplica a cualquier sitio que pinte contenido con JS):

| Patrón | Plataforma | Riesgo |
|---|---|---|
| Embeds que pintan contenido del lado del cliente (widgets de reseñas, calendarios, precios) | Ambas | El texto no existe para el bot |
| Tabs y acordeones cuyo contenido se inyecta por JS | Ambas (en Webflow nativo suele estar en el HTML; en librerías externas no) | Respuestas FAQ invisibles |
| Code components que hacen `fetch` | Framer | Contenido dinámico vacío en el HTML |
| Listas CMS cargadas o filtradas por JS (Finsweet y similares) | Webflow | Solo la primera página o nada |
| JSON-LD inyectado por un script o por GTM | Ambas | El schema no existe para bots sin JS |
| Copy clave dentro de imágenes, SVG o Lottie | Ambas | No es texto |

Prueba manual:

```bash
curl -s -A "OAI-SearchBot" https://dominio.com/servicio | grep -c "frase clave del copy"
curl -s -A "GPTBot" https://dominio.com/ | grep -c 'application/ld+json'
```

La versión empaquetada es `scripts/check_html_crudo.py`: recorre una lista de URLs con el UA de
cada bot, confirma status, presencia de textos clave y de JSON-LD, que robots.txt no bloquee bots
de búsqueda, y que `llms.txt` y `sitemap.xml` respondan.

Ojo: un 403 o un "404" con UA de bot y 200 con UA de navegador es **bloqueo anti-bot**, no página
caída. Se reporta como tal.

## 8. Gate antes de publicar

- [ ] robots.txt servido = plantilla elegida (permitir u opt-out), con `Sitemap:`.
- [ ] Ningún bot de búsqueda (Googlebot, Bingbot, OAI-SearchBot, Claude-SearchBot, PerplexityBot)
      recibe 403, 402 ni Disallow.
- [ ] Si hay Cloudflare propio del cliente: revisado y documentado.
- [ ] Copy clave y JSON-LD presentes en el HTML crudo de cada página clave.
- [ ] La decisión de opt-out, si se tomó, está por escrito con su costo.
