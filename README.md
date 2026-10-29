# seo-geo

Skill de Claude Code para **SEO técnico, schema y GEO** (visibilidad en asistentes de IA) en
sitios hechos en cualquier plataforma; guías detalladas para WordPress, Shopify, Squarespace, Wix, Webflow, Framer, frameworks de código y HTML propio. Genera el JSON-LD, la metadata, el `robots.txt`
para bots de IA y el borrador de `llms.txt`; corre un gate de lanzamiento; y **mide** si el
negocio aparece en ChatGPT, Gemini, Claude, AI Overviews y AI Mode, con un protocolo repetible.

[English version](README.en.md) (edición completa en inglés: `bash install.sh --lang en`) · Hecho por [Alto House](https://altohouse.mx/), estudio de brand management y posicionamiento en Guadalajara.

## Para quién

- Estudios, freelancers y equipos internos que entregan sitios en cualquier plataforma (WordPress,
  Shopify, Squarespace, Wix, Webflow, Framer, frameworks de código o HTML propio) y quieren una
  capa SEO + schema + GEO que no dependa de herramientas de pago.
- Equipos en México y LatAm que trabajan en español y necesitan medir citación en asistentes sin
  pagar una plataforma enterprise.
- Negocios en verticales donde la entidad pesa: médicos y clínicas, SaaS B2B, industria,
  inmobiliario, catálogo físico.

## Qué NO promete

- **No hay "posición en ChatGPT".** Las respuestas casi nunca se repiten; se reporta el % de
  corridas en que el negocio aparece, como rango.
- **El schema no da citas.** Ordena la entidad y habilita rich results; el test de Ahrefs de
  mayo de 2026 no encontró lift en citas.
- **llms.txt no es GEO.** Ningún motor documenta usarlo; se publica como cortesía barata.
- **El KPI es cita y mención, no tráfico.** Los clics desde resúmenes y chatbots son de 1% a 4%.
- **Nada es un interruptor.** Ninguna palanca garantiza aparecer; el skill trabaja superficie
  citable, entidad consistente y medición honesta.

## Instalación

Standalone:

```bash
git clone https://github.com/frontdesk-alhouse/seo-geo-skill.git
cd seo-geo-skill
bash install.sh              # edición en español (por defecto)
# bash install.sh --lang en  # edición en inglés
```

`install.sh` copia la edición elegida a `~/.claude/skills/seo-geo/`, verifica `python3` e imprime cómo
invocarlo. Es idempotente y no descarga nada. Alternativa manual: copia la carpeta tal cual a
`~/.claude/skills/seo-geo/`.

## Uso

```text
/seo-geo medical https://ejemplo.com            construir y lanzar (pasos 1 a 6)
/seo-geo saas https://ejemplo.com --solo-schema schema y metadata
/seo-geo generic https://ejemplo.com --gate     gate de lanzamiento sobre un sitio publicado
/seo-geo real-estate https://ejemplo.com --medir medición de citación en asistentes
```

Verticales: `medical`, `saas`, `product`, `real-estate`, `generic`.

## Mapa de archivos

| Ruta | Contenido |
|---|---|
| `SKILL.md` | Flujo de 7 pasos y reglas del skill |
| `references/seo-core.md` | SEO técnico base, tipo de página a schema, fórmulas, severidad |
| `references/*.jsonld.md` | Baseline y plantillas por vertical |
| `references/metadata-og.md` · `local-seo.md` · `backlinks.md` | Metadata, SEO local, enlaces |
| `references/geo-evidencia.md` | Evidencia GEO etiquetada y fechada |
| `references/geo-aeo.md` | Palancas on-site |
| `references/ai-crawlers.md` · `llms-txt.md` | Bots de IA, robots.txt, Cloudflare, llms.txt |
| `references/entidad-sameas.md` | Consistencia de entidad y `sameAs` |
| `references/medicion-citacion.md` · `analytics-ia.md` | Protocolo de medición y analítica |
| `references/report-template.md` | Reporte para cliente |
| `references/plataformas.md` | Dónde va cada cosa por plataforma: WordPress, Shopify, Squarespace, Wix, Webflow, Framer, frameworks y HTML propio |
| `checklist-lanzamiento.md` | Gate de lanzamiento para cualquier plataforma, con Gate GEO y notas de Webflow y Framer |
| `templates/` | Batería de prompts, corrida, reporte GEO, `llms.txt`, `robots.txt` |
| `scripts/` | Utilidades en Python |
| `examples/` | Corridas ficticias para probar los scripts |
| `en/` | Edición completa en inglés (comparte `scripts/`) |

## Scripts

Python 3, **solo biblioteca estándar** (sin `pip install`). Todos traen `--help`.

| Script | Qué hace |
|---|---|
| `check_html_crudo.py` | Pide la URL como cada bot y confirma copy clave, JSON-LD, robots, llms.txt y sitemap en el HTML crudo |
| `verificar_metadata.py` | Title, meta, canonical y OG por página: longitudes, duplicados, faltantes |
| `generar_llms_txt.py` | Del sitemap a un borrador de `llms.txt` para curar a mano |
| `indice_citacion.py` | De las corridas al Índice de Citación con intervalo de Wilson y censo de fuentes |
| `verificar_fuentes.py` | Abre cada URL citada: estado HTTP y si de verdad nombra al negocio |

## Método de medición

1. Batería fija de prompts en familias: sin marca por necesidad, sin marca por decisión, con
   marca y el tercero que busca por alguien.
2. El set no se modifica entre rondas; las consultas nuevas entran al final con fecha.
3. Tres corridas por consulta y asistente, en la interfaz de consumo, no en la API.
4. La sesión (chat temporal, incógnito, cuenta) se declara como variable no controlada.
5. Cada corrida se guarda con su texto, nombres en orden, URLs citadas y si el asistente buscó.
6. Índice de Citación = corridas con mención / corridas totales, con intervalo; marca aparte.
7. Cada URL citada se abre: muchas están muertas o no dicen lo que el asistente afirmó.
8. Se repite a 30 y 60 días de publicar cambios y luego cada trimestre; se lee la tendencia.

## Evidencia

Todo el skill se apoya en `references/geo-evidencia.md`, donde cada afirmación lleva etiqueta
([E] estudio, [O] oficial, [S] especulativo, [M] mito) y fuente con fecha. Estudios clave:

- Princeton, Aggarwal et al., "GEO: Generative Engine Optimization", KDD 2024.
- Ahrefs, test de schema y citas en IA, mayo de 2026.
- TJ Robertson / TJ Digital, estudio de citación en ChatGPT, AI Mode y AI Overviews, octubre de 2026.
- SparkToro / Gumshoe, repetibilidad de listas de recomendación en asistentes, 2026.
- Columbia Tow Center (CJR), exactitud de citas en buscadores de IA, marzo de 2025.
- Pew Research Center, clics con resúmenes de IA en Google, julio de 2025.

## De dónde sale

El método lo desarrolló [Alto House](https://altohouse.mx/), estudio de Guadalajara, México,
en casos reales entre 2025 y 2026: sitios médicos, SaaS B2B, industria e inmobiliario. Los casos están
anonimizados: el repo no contiene nombres de clientes, URLs, cifras ni transcripciones reales.
Las corridas de `examples/` son ficticias. El skill se probó de punta a punta en el sitio del
propio estudio (Framer): gate, ronda 0 de medición y aplicación de cambios.

## Créditos

- [`AgriciDaniel/claude-seo`](https://github.com/AgriciDaniel/claude-seo) (MIT): estructura de
  auditoría de backlinks, SEO local, reporte para cliente y el primer encuadre de GEO/AEO. Se
  reescribió en español y se ajustó a la evidencia de 2026.
- [`zubair-trabzada/geo-seo-claude`](https://github.com/zubair-trabzada/geo-seo-claude) (MIT):
  niveles de bots y Content-Signals, detección de robots gestionado por Cloudflare, el chequeo
  HTML crudo contra DOM, la lógica del generador de `llms.txt`, la estrategia `sameAs` y el
  formato quick wins / mes / trimestre. **Se corrigió:** GPTBot no alimenta ChatGPT Search (eso
  es OAI-SearchBot); `anthropic-ai` es un token retirado; faltaban Claude-SearchBot, Claude-User y
  Perplexity-User; la regla de "134-167 palabras" no está en el paper de Princeton; se quitaron
  los pesos compuestos, las cifras sin fuente y el instalador `curl | bash`.

## Frente a `Auriti-Labs/geo-optimizer-skill`

Es el proyecto más cercano y vale la pena conocerlo. Lo que este hace distinto:

- Español y mercado LatAm primero, con fuentes de entidad mexicanas por vertical.
- Mide en la **interfaz de consumo** de cada asistente, sin costo de API; la API queda como
  complemento declarado.
- Evidencia etiquetada y fechada; ninguna cifra sin fuente.
- Funciona en cualquier plataforma; guías detalladas para WordPress, Shopify, Squarespace, Wix, Webflow, Framer, frameworks de código y HTML propio.

## Licencia

MIT. Ver [LICENSE](LICENSE).

## Cómo contribuir

- **Estudios:** abre un PR a `references/geo-evidencia.md` con fuente, URL, fecha, tamaño de
  muestra y etiqueta. Si llegó por cobertura secundaria, márcalo con ⚠️.
- **Corridas de ejemplo:** agrega corridas ficticias a `examples/` con la plantilla de
  `templates/corrida.template.md`; nunca datos reales de un cliente.
- **Verticales:** plantillas JSON-LD nuevas con validación en validator.schema.org.
- Los scripts siguen sin dependencias externas.
