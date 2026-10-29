---
name: seo-geo
description: "Capa ejecutable de SEO técnico, schema y GEO para cualquier sitio (Webflow, Framer, WordPress, Shopify, Squarespace, Wix, frameworks de código o HTML propio): genera JSON-LD y metadata, robots.txt para bots de IA y llms.txt, corre el gate de lanzamiento y mide la citación del negocio en asistentes de IA (ChatGPT, Gemini, Claude, AI Overviews y AI Mode)."
argument-hint: "[vertical: medical|saas|product|real-estate|generic] [URL o ruta del sitio] [--medir | --gate | --solo-schema]"
---

# SEO + Schema + GEO

> Convierte una marca, un sitemap y su copy en **schema válido, metadata completa, una capa
> técnica limpia y una superficie citable por asistentes de IA**, y después **mide** si el negocio
> aparece en esos asistentes. No es teoría: produce el JSON-LD que se pega en tu plataforma, el
> `robots.txt`, el borrador de `llms.txt`, el gate que se corre antes de lanzar y la línea base de
> citación.

**Input**: $ARGUMENTS (vertical del cliente + URL en producción o ruta local del sitio + modo)

| Modo | Corre |
|---|---|
| sin bandera | Pasos 1 a 6 (construir y lanzar) |
| `--solo-schema` | Pasos 2 y 3 |
| `--gate` | Paso 6 sobre un sitio ya publicado |
| `--medir` | Paso 7 (batería de prompts, corridas, índice y censo) |

---

## Verdad de negocio (leer antes de prometerle nada al cliente)

Evidencia completa, con etiqueta y fecha, en `references/geo-evidencia.md`. Lo que no se negocia:

- **Schema = comprensión de entidad y elegibilidad para rich results, no citas.** Ahrefs (may-2026)
  agregó JSON-LD a 1,885 páginas contra 4,000 de control: sin lift significativo en AI Mode ni
  ChatGPT, y AIO ligeramente abajo [E]. Se hace porque ordena la entidad, no como interruptor.
- **AI Overviews y AI Mode no piden nada extra.** Google (2025-12-10): sin requisitos adicionales,
  sin schema especial, sin archivos de texto para IA; cuenta estar indexado y ser elegible a
  snippet [O]. AI Mode en español corre en México desde 2025-09-23 [O].
- **llms.txt es especulativo.** Ningún motor documenta usarlo; Google lo llamó "purely
  speculative" [M como palanca]. Se publica como cortesía barata, nunca se vende como GEO.
- **FAQ rich result terminó el 2026-05-07** y HowTo desde 2023 [O]. `FAQPage` no se agrega
  esperando resultado visual.
- **No hay ranking en asistentes.** SparkToro/Gumshoe (2026) ⚠️: menos de 1 en 100 corridas
  repite la misma lista de marcas [E]. Se reporta **% de corridas con mención, como rango**,
  nunca "posición en ChatGPT".
- **El KPI es cita y mención, no tráfico.** Pew (2025) y Reuters DNR (2026): ~1% a ~4% de clics a
  fuentes desde resúmenes y chatbots [E].
- El tráfico orgánico real lo mueven contenido, autoridad demostrable, técnica correcta e
  intención. El schema es acabado, no motor.

---

## Cuándo usarlo

- Un sitio sale del workflow de diseño y necesita su capa SEO, schema y GEO antes de publicar.
- Un sitio en producción necesita schema, metadata, `robots.txt` para bots de IA o `llms.txt`.
- Antes de apuntar dominio o publicar: corre el gate (`--gate`).
- El cliente pregunta "¿salgo en ChatGPT?": se responde con medición (`--medir`), no con opinión.
- 30 y 60 días después de publicar cambios, y luego trimestral: repetir la medición.

---

## Flujo (7 pasos)

### 1. SEO técnico base
Crawl, indexación, canonical, redirects (2 saltos máximo), sitemap, robots, hreflang, Core Web
Vitals, un H1 y jerarquía real. Checklist, tipos de página, fórmulas y taxonomía de severidad en
`references/seo-core.md`. Se arreglan bloqueos técnicos **antes** de optimizar contenido.

### 2. Schema por página
Baseline **siempre**; encima, la plantilla del vertical:

| Página | Schema | Referencia |
|---|---|---|
| Home (todo sitio) | `Organization` (o subtipo de `LocalBusiness`) + `WebSite` | `baseline.jsonld.md` |
| Cualquier interior | `BreadcrumbList` | `baseline.jsonld.md` |
| Negocio con ubicación | `LocalBusiness` + NAP idéntico al perfil de Google | `local-seo.md` |
| Médico | `Person` (médico) + `MedicalClinic` + `SurgicalProcedure` / `MedicalProcedure` | `medical.jsonld.md` |
| SaaS / software | `SoftwareApplication` (`Offer` solo con precio visible), `DefinedTerm`, `Person` fundador | `saas.jsonld.md` |
| Catálogo físico | `Product` + `Offer`, `Brand`, `AggregateRating` solo si es real | `product.jsonld.md` |
| Inmobiliaria | `RealEstateAgent`, `RealEstateListing`, `Residence`, `Offer` | `real-estate.jsonld.md` |
| Blog / editorial | `Article` / `BlogPosting` | `seo-core.md` |

- Rellena los placeholders (`{{business_name}}`, `{{price}}`, ...) con datos **reales** del
  brief. Un `@id` canónico por entidad, reusado idéntico en todo el sitio.
- **Regla dura:** solo se marca contenido **visible**. Reseñas o precios que no están en la página
  son la violación de política número uno y pueden costar una acción manual.
- JSON-LD únicamente, en `<script type="application/ld+json">`. Nunca Microdata ni RDFa, nunca la
  misma entidad dos veces.

### 3. Metadata y Open Graph
`references/metadata-og.md`: `<title>` de 50 a 60 caracteres con el concepto al frente, meta
description de 120 a 160 honesta, OG y Twitter card con imagen 1200×630. Únicos por página.

### 4. GEO on-site (superficie citable)
Palancas priorizadas y cómo escribirlas en `references/geo-aeo.md`; la evidencia de cada una en
`geo-evidencia.md`. En la página, no en un archivo aparte:

- **Respuesta directa** en el primer párrafo de cada página clave; la pregunta se contesta, no se
  rodea.
- **Tablas** para comparar, especificar o tabular precios; listas donde haya pasos.
- **Fecha visible de actualización** y revisión trimestral de las páginas que importan.
- **Precios o rangos** cuando existan; "desde" con condiciones vale más que "cotiza".
- **Experiencia de primera mano**: casos, cifras propias verificables, método explicado.
- **Postura nombrable**: una tesis con nombre propio es citable; "la mejor solución" no.
- **Decir lo que NO hace** el producto o servicio: reduce errores de atribución.
- Ciudad y servicio juntos en la misma URL cuando el negocio es local.

### 5. Bots de IA, llms.txt y entidad
- `robots.txt`: por defecto **permite todo**; la variante opt-out de entrenamiento bloquea solo
  bots de entrenamiento y nunca los de búsqueda. Tabla de bots, Cloudflare y JS en
  `references/ai-crawlers.md`; archivos listos en `templates/robots-ai-permitir.txt` y
  `templates/robots-ai-optout-entrenamiento.txt`.
- `llms.txt`: borrador con `scripts/generar_llms_txt.py` sobre el sitemap, se cura a mano con
  `templates/llms.txt.template` y `references/llms-txt.md`. Opcional y declarado como tal.
- Entidad: nombre, credenciales, dirección y perfiles idénticos en todas partes; `sameAs` solo a
  perfiles que existen y coinciden. Checklist por vertical en `references/entidad-sameas.md`.
- Ninguna cifra ni credencial sale a una superficie pública sin verificar: un dato falso se
  propaga y sobrevive a su fuente.

### 6. Gate de lanzamiento
`checklist-lanzamiento.md` completo (incluye el bloque **Gate GEO** y las notas de Webflow y Framer), más:

- `scripts/check_html_crudo.py URL`: el HTML que recibe cada bot contiene el copy clave y el
  JSON-LD; `robots.txt` no bloquea bots de búsqueda; `llms.txt` y sitemap responden.
- `scripts/verificar_metadata.py`: longitudes, duplicados, canonical y OG por página.
- **validator.schema.org** y **Google Rich Results Test**: 0 errores.
- Cliente verificado en **Bing Webmaster Tools** y canal de IA creado en **GA4**
  (`references/analytics-ia.md`).

### 7. Medición de citación
Protocolo completo en `references/medicion-citacion.md`:

1. Batería desde `templates/bateria-prompts.template.md` (familias sin marca, con marca y tercero
   que busca); el set no se modifica entre rondas.
2. N=3 corridas por consulta y asistente, en el modo de sesión que indica la referencia; la
   sesión se declara como variable no controlada.
3. Cada corrida en `templates/corrida.template.md`.
4. `scripts/indice_citacion.py`: Índice de Citación con intervalo, primer lugar, subtotal sin
   marca, tasa de búsqueda y censo de fuentes.
5. `scripts/verificar_fuentes.py`: cada URL citada se abre; viva, muerta o no dice lo que el
   asistente afirmó.
6. Entrega con `templates/reporte-geo.template.md`.

---

## Cómo aplicarlo

El skill no depende de la plataforma. Cualquiera sirve si permite estas cinco cosas:

1. **JSON-LD en el HTML**, global (Organization + WebSite) y por página.
2. **Title, meta description, OG y canonical** editables por página (y ligados a campos en
   contenido dinámico).
3. **`robots.txt` en la raíz** del dominio, editable.
4. **Archivos en la raíz** como `llms.txt` (opcional).
5. **El copy clave en el HTML que entrega el servidor**, no solo después de ejecutar JS;
   compruébalo con `scripts/check_html_crudo.py`.

Dónde se pone cada cosa en tu plataforma (WordPress, Shopify, Squarespace, Wix, Webflow, Framer,
frameworks de código y HTML propio), y qué hacer si alguna no lo permite:
`references/plataformas.md`. Los detalles de Webflow y Framer que se revisan en el gate están en
las notas por plataforma de `checklist-lanzamiento.md`.

---

## Referencias

| Archivo | Para qué |
|---|---|
| `references/seo-core.md` | Checklist técnico, tipo de página a schema, fórmulas, enlaces, mapa keyword a página, severidad |
| `references/baseline.jsonld.md` | Organization + WebSite + BreadcrumbList y disciplina de `@id` |
| `references/medical.jsonld.md` · `saas.jsonld.md` · `product.jsonld.md` · `real-estate.jsonld.md` | Plantillas por vertical |
| `references/metadata-og.md` | Title, meta, OG y Twitter cards |
| `references/local-seo.md` | LocalBusiness, perfil de Google y NAP |
| `references/backlinks.md` | Auditoría de enlaces entrantes |
| `references/geo-evidencia.md` | Base de evidencia GEO con etiquetas [E]/[O]/[S]/[M] y fechas |
| `references/geo-aeo.md` | Palancas on-site y cómo escribirlas |
| `references/ai-crawlers.md` | Bots de IA, robots.txt, Cloudflare y HTML crudo |
| `references/llms-txt.md` | Qué es, qué no, anatomía, hosting |
| `references/entidad-sameas.md` | Consistencia de entidad y `sameAs` por vertical |
| `references/medicion-citacion.md` | Batería, protocolo N=3, Índice de Citación, censo |
| `references/analytics-ia.md` | GA4 canal IA, Bing WMT AI Performance, Search Console |
| `references/report-template.md` | Forma del reporte SEO + GEO para cliente |
| `references/plataformas.md` | Dónde va cada cosa por plataforma: WordPress, Shopify, Squarespace, Wix, Webflow, Framer, frameworks y HTML propio |
| `checklist-lanzamiento.md` | Gate de lanzamiento para cualquier plataforma, con Gate GEO y notas de Webflow y Framer |
| `templates/` | Batería, corrida, reporte GEO, `llms.txt`, dos `robots.txt` |
| `examples/` | Corridas ficticias para probar los scripts |

## Scripts

Python 3, solo biblioteca estándar; cada uno trae `--help`.

| Script | Qué hace |
|---|---|
| `scripts/check_html_crudo.py` | Pide la URL con el user-agent de cada bot y revisa copy clave, JSON-LD, robots, llms.txt y sitemap |
| `scripts/verificar_metadata.py` | Revisa title, meta, canonical y OG por página: longitudes, duplicados y faltantes |
| `scripts/generar_llms_txt.py` | Sitemap + title y meta de cada página → borrador de `llms.txt` para curar |
| `scripts/indice_citacion.py` | Corridas → Índice de Citación por consulta y asistente con intervalo de Wilson y censo de fuentes |
| `scripts/verificar_fuentes.py` | URLs citadas → estado HTTP y si la página nombra al negocio |

## Agentes opcionales

Si tienes un agente de auditoría SEO (por ejemplo `seo-specialist`), úsalo para auditar en modo
lectura; si no, `references/seo-core.md` trae la taxonomía de severidad y el formato de hallazgo.

---

## Anti-patrones

| Anti-patrón | Fix |
|---|---|
| Marcar contenido no visible | El schema refleja lo que está en la página |
| Agregar `FAQPage` esperando rich result | Terminó el 2026-05-07; solo si la página de verdad es preguntas y respuestas |
| Vender schema como ranking o como citas en IA | Es comprensión de entidad y rich results |
| Vender llms.txt como GEO | Cortesía barata; nadie documenta usarlo |
| Prometer posición en ChatGPT | No existe; se reporta % de corridas con mención, como rango |
| Inventar un "score GEO" compuesto con pesos | Índice de Citación por asistente y censo de fuentes |
| Agregar byline o CTAs como palanca de cita | La evidencia los asocia a menos citas; se ponen por razones de negocio, no de GEO |
| Trocear el contenido en pedacitos para LLMs o hacer una versión "para IA" | Google lo desaconseja; una sola página bien escrita |
| Copiar reseñas de terceros al sitio o marcarlas como propias | Solo reseñas reales, propias y visibles |
| Pagar por aparecer en listas de "los mejores" | Se detecta, no dura y contamina la entidad |
| Publicar una cifra o credencial sin verificar | Se propaga entre asistentes y sobrevive a su fuente |
| Bloquear `OAI-SearchBot` o `PerplexityBot` para "no entrenar" | Esos son de búsqueda; el opt-out va contra bots de entrenamiento |
| Schema en dos lugares (campo o plugin + código a mano) | Elige uno |
| "Mejora el SEO" genérico | Cada recomendación atada a una página o asset |
