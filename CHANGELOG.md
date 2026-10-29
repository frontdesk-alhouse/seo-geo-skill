# Changelog

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
