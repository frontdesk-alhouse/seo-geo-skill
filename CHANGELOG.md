# Changelog

## v1.3.0 (2026-11-22)

Del censo a la acción, auditoría con Search Console y enlaces por activo. / From census to action,
Search Console audit and asset-led links.

- Paso 8, del censo a la acción: `references/censo-a-accion.md` /
  `en/references/citation-census-to-action.md` y `scripts/objetivos_terceros.py`. De las corridas
  sin marca donde el cliente faltó, la tabla de páginas de terceros citadas, ordenada por corridas
  sin el cliente y no por autoridad de dominio; reutiliza el lector de `indice_citacion.py` y
  acepta el JSON de `verificar_fuentes.py`. `--medir` / `--measure` corre ahora los pasos 7 y 8;
  el reporte GEO trae una sección de objetivos.
- Modo `--auditar` / `--audit`: `references/auditoria-gsc.md` / `en/references/gsc-audit.md` y
  `scripts/auditoria_gsc.py`. Lee CSV de Search Console con encabezados en español o inglés y hace
  seis análisis: CTR bajo contra la curva del propio sitio (no una tabla fija previa a AI
  Overviews), distancia de ataque, pérdida entre periodos con diagnóstico, canibalización, páginas
  muertas y proporción con marca y sin marca. CSV ficticios en `examples/gsc-ejemplo/` y
  `en/examples/gsc-sample/`.
- `references/enlaces-por-activo.md` / `en/references/asset-led-links.md`: hoja de correcciones,
  lápida y visual faltante, con reglas comunes (nada sin verificar, pocos envíos, el cliente
  envía). `backlinks.md` resume y apunta ahí.
- Familia opcional F7 en la batería (alternativas a X, X vs Y, con marca de competidor): suma al
  subtotal sin marca y se lee también sola; documentado en `medicion-citacion.md`.
  `indice_citacion.py` acepta F7; su salida sobre los ejemplos no cambia.
- `geo-aeo.md`: la página de datos como activo citable, con seis filtros por cifra y las fuentes
  enlazadas.
- Anti-patrones nuevos: intercambio de enlaces, campañas pagadas en Reddit, Quora o YouTube,
  directorios gubernamentales solo por el enlace, medir asistentes con búsqueda web del agente,
  scores compuestos de visibilidad, H2 en pregunta como palanca de cita, página de datos sin
  enlazar sus fuentes.
- `install.sh` no copia `_briefs/`.
- Ideas tomadas de la revisión de un skill público de SEO (Distribb), reescritas y ajustadas a la
  evidencia de este skill; no es dependencia. / Ideas taken from reviewing a public SEO skill
  (Distribb), rewritten and adjusted to this skill's evidence; it is not a dependency.

## v1.2.0 (2026-10-29)

Cualquier plataforma, no solo Webflow y Framer. / Any platform, not only Webflow and Framer.

- Guía nueva por plataforma: `references/plataformas.md` / `en/references/platforms.md`. HTML
  estático, Next.js, Astro, Nuxt, SvelteKit, Gatsby, SPA sin SSR, WordPress (Yoast, Rank Math),
  Shopify, Squarespace, Wix, Webflow, Framer, Ghost y HubSpot CMS: dónde va el JSON-LD, la
  metadata, robots.txt, llms.txt y qué bloquea cada una, con fuente oficial y fecha.
- El checklist pasa a `checklist-lanzamiento.md` / `en/launch-checklist.md`, genérico, con las
  notas de Webflow y Framer al final. `install.sh` limpia el nombre viejo.
- SKILL y README: los 5 requisitos que cualquier plataforma debe permitir y el puntero a la guía.
- Corrección: Webflow sirve `llms.txt` nativo desde el 2025-07-23 (Site Settings → SEO).

## v1.1.0 (2026-10-29)

Edición completa en inglés. / Full English edition.

- `en/`: SKILL, referencias, plantillas, checklist y ejemplos en inglés, con nombres de archivo en
  inglés (`geo-evidence.md`, `citation-measurement.md`, `run.template.md`...). Fuentes de entidad
  de México conservadas y equivalentes de EE. UU. agregados (NPI, juntas médicas estatales,
  Healthgrades, Zocdoc, Yelp, BBB).
- `install.sh --lang en|es`: instala una u otra edición en `~/.claude/skills/seo-geo/`; cambiar de
  idioma limpia los archivos de la edición anterior.
- Scripts bilingües: `--lang es|en` (por defecto, el idioma instalado), alias de opciones en
  inglés (`--brand`, `--name`, `--texts`, `--sections`, `--output`...) y lectura de corridas con
  campos en español o en inglés. La salida en español no cambia.
- Corrección en ambas ediciones: el campo `aparece` / `appears` es `true` o `false`; si AI
  Overviews no se dispara se registra `false` con la nota `no-disparo` / `no-trigger`.

## v1.0.0 (2026-10-29)

Primera versión pública. Evolución de un skill interno de SEO y schema a uno autocontenido de
SEO + Schema + GEO.

### Incluye
- `SKILL.md` con flujo de 7 pasos: SEO técnico, schema por página, metadata, GEO on-site, bots de
  IA y entidad, gate de lanzamiento y medición de citación.
- `references/seo-core.md`: checklist técnico, tipo de página a schema, fórmulas, mapa keyword a
  página y taxonomía de severidad. El skill ya no depende de skills ni agentes externos.
- Plantillas JSON-LD: baseline y verticales médico, SaaS, catálogo físico e inmobiliario.
- Referencias GEO nuevas: `geo-evidencia.md` (evidencia etiquetada [E]/[O]/[S]/[M] con fecha),
  `ai-crawlers.md`, `llms-txt.md`, `entidad-sameas.md`, `medicion-citacion.md`,
  `analytics-ia.md`; `geo-aeo.md` actualizado.
- Gate de lanzamiento para Webflow y Framer con bloque Gate GEO.
- Plantillas: batería de prompts, corrida, reporte GEO, `llms.txt` y dos `robots.txt` (permitir
  todo y opt-out de entrenamiento).
- Scripts en Python 3 sin dependencias: `check_html_crudo.py`, `verificar_metadata.py`,
  `generar_llms_txt.py`, `indice_citacion.py`, `verificar_fuentes.py`.
- Corridas de ejemplo ficticias en `examples/`.
- `install.sh` standalone, `README.md` y `README.en.md`, licencia MIT.

### Probado en campo
- Gate y ronda 0 de medición corridos sobre un sitio real en Framer antes de publicar.
- `verificar_metadata.py` reporta como INFO (no error) los `<h1>` idénticos que Framer repite
  por breakpoint.
- Notas de Framer en el checklist: `llms.txt` en Hosting → Files con ruta `/`, el custom code no
  se localiza, filtro "New" en Localization.

### Decisiones de encuadre
- Sin "score GEO" compuesto: se reporta Índice de Citación con intervalo y censo de fuentes.
- `robots.txt` por defecto permite todo; el opt-out solo toca bots de entrenamiento.
- Medición manual en la UI de consumo de cada asistente, con script de cálculo; sin API de pago.
