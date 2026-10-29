# Plataformas: cómo aplicar SEO técnico, schema y GEO en cualquier stack

> Qué permite cada plataforma, dónde se hace y qué hacer cuando la plataforma lo bloquea.
> Etiquetas: [O] documentación oficial (URL + "consultado 2026-10") · ⚠️ solo fuente comunitaria o
> secundaria · "no verificado" cuando no hubo fuente. Los planes y menús cambian: confirma en el
> panel del cliente antes de prometer algo. Lo que manda es lo **servido**: verifica siempre con
> `scripts/check_html_crudo.py` y `curl`.

---

## 1. Las 5 capacidades que toda plataforma debe permitir

| # | Capacidad | Por qué | Referencia |
|---|---|---|---|
| 1 | **JSON-LD en el HTML** de la página, global (Organization, WebSite) y por página o plantilla CMS | Entidad y elegibilidad a rich results | `references/baseline.jsonld.md` |
| 2 | **Title, meta, OG y canonical por página** (y por item de CMS) | Snippet, preview social, señal canónica | `references/metadata-og.md` |
| 3 | **robots.txt en la raíz**, editable | No bloquear bots de búsqueda de IA; declarar sitemap | `references/ai-crawlers.md` |
| 4 | **Un archivo en la raíz** tipo `/llms.txt` (y verificaciones) | Cortesía para agentes; verificación de dominios | `references/llms-txt.md` |
| 5 | **Copy clave en el HTML crudo** (render de servidor), no solo inyectado por JS | La mayoría de los bots de IA no ejecutan JS | `scripts/check_html_crudo.py` |

Si una plataforma falla en 1, 2 o 5, es un problema de SEO real. Si falla en 3 o 4, casi siempre
hay salida (sección 2).

## 2. Respaldo universal cuando la plataforma bloquea algo

**A. Proxy en el borde (CDN o edge).** Si el dominio pasa por un proxy que controlas (Cloudflare
con nube naranja, Fastly, un reverse proxy), puedes servir `/llms.txt` o `/robots.txt` desde ahí
sin tocar la plataforma. En Cloudflare, un Worker con una ruta `dominio.com/llms.txt` responde el
archivo con `Content-Type: text/plain; charset=utf-8` [O]
https://developers.cloudflare.com/workers/configuration/routing/routes/ (consultado 2026-10).

Cuidados:
- Cambiar los DNS para poner un proxy delante de Shopify, Wix, Squarespace o HubSpot puede romper
  el SSL o el soporte de la plataforma. Revisa sus reglas de dominio antes; no verificado por
  plataforma.
- Un robots.txt servido desde el borde **pisa** al de la plataforma. Documenta cuál manda, o el
  siguiente que edite el panel no verá el efecto.
- Revisa que el propio Cloudflare no reescriba robots.txt (robots gestionado) ni bloquee bots de
  búsqueda de IA (`references/ai-crawlers.md`, sección 5).

**B. Redirect 301 de `/llms.txt` a un archivo alojado** (asset del CDN o página de texto). Funciona
para personas y para la mayoría de los clientes HTTP, pero el archivo deja de estar "en la raíz":
declararlo como limitación. **No sirve para robots.txt**: un robots.txt redirigido se sigue con
reglas propias de cada bot y no es confiable.

**C. Página HTML en `/llms-txt`** con el contenido en texto. Último recurso: se sirve como HTML.

**D. Copy por JS sin arreglo en la plataforma:** no hay respaldo de borde razonable. Hay que mover
el copy a un bloque nativo renderizado en servidor, o usar prerender/SSR. Pasa
`check_html_crudo.py` después.

---

## 3. Plataforma por plataforma

Campos fijos: JSON-LD · Metadata/OG/canonical · robots.txt · llms.txt y archivos raíz · sitemap ·
staging · riesgo de JS · trampas.

### 3.1 HTML plano y hosting estático (Netlify, Vercel, Cloudflare Pages, GitHub Pages)

- **JSON-LD:** `<script type="application/ld+json">` en el `<head>` de cada archivo. Global = en el
  include o parcial compartido; por página = en su archivo. Sin límites de binding.
- **Metadata:** todo a mano en el `<head>`: `<title>`, meta description, OG, Twitter y canonical
  absoluto a producción.
- **robots.txt:** archivo `robots.txt` en la raíz del directorio publicado. Control total.
- **llms.txt:** igual, archivo en la raíz. Sin límites de plan.
- **Sitemap:** a mano o con el generador del build; declararlo en robots.txt.
- **Staging:**
  - Vercel pone `X-Robots-Tag: noindex` en todos los Preview Deployments, salvo si asignas un
    dominio propio a una rama que no es producción [O]
    https://vercel.com/kb/guide/are-vercel-preview-deployment-indexed-by-search-engines
    (consultado 2026-10).
  - Cloudflare Pages pone `X-Robots-Tag: noindex` en cada preview deployment por defecto; el
    `*.pages.dev` de producción no [O]
    https://developers.cloudflare.com/pages/configuration/preview-deployments/ (consultado 2026-10).
  - Netlify: deploy previews con `noindex` y sin forma de quitarlo ⚠️ (foro
    answers.netlify.com); la documentación oficial no lo confirmó en esta consulta.
  - GitHub Pages: no permite headers propios; no verificado si existe noindex automático. Usa
    canonical a producción.
  - En todos: el subdominio de la plataforma (`*.vercel.app`, `*.netlify.app`, `*.pages.dev`)
    sigue vivo en producción. Canonical al dominio primario o redirect.
- **Riesgo de JS:** bajo si el HTML se escribe a mano.
- **Trampas:** headers por archivo (`_headers`, `vercel.json`) sirven para `X-Robots-Tag` y para el
  `Content-Type` de `llms.txt`. No bloquees previews con robots.txt: un bot bloqueado no lee el
  noindex.

### 3.2 Frameworks de JS (Next.js, Astro, Nuxt, SvelteKit, Gatsby)

Regla general: **render de servidor o generación estática = HTML crudo completo**. Lo que se pida
con `fetch` en el navegador después de cargar no existe para la mayoría de los bots de IA.

**Next.js (App Router)**
- **JSON-LD:** `<script type="application/ld+json">` nativo en `layout.js` (global) o `page.js`
  (por página), con `JSON.stringify(data).replace(/</g, '\\u003c')` para no abrir XSS; no usar
  `next/script` [O] https://nextjs.org/docs/app/guides/json-ld (consultado 2026-10).
- **Metadata:** objeto `metadata` o `generateMetadata()` por ruta (title, description, openGraph,
  alternates.canonical, robots) [O]
  https://nextjs.org/docs/app/api-reference/functions/generate-metadata (consultado 2026-10).
- **robots.txt y sitemap:** archivos `app/robots.ts` y `app/sitemap.ts` (o estáticos) [O]
  https://nextjs.org/docs/app/api-reference/file-conventions/metadata/robots (consultado 2026-10).
- **llms.txt:** archivo en `public/` o un Route Handler en `app/llms.txt/route.ts`.
- **Riesgo de JS:** componentes con `'use client'` que cargan datos con `useEffect` dejan el copy
  fuera del HTML crudo. Los Server Components no.

**Astro**
- Genera estático por defecto. JSON-LD y meta en el `<head>` del layout o de cada página; archivos
  de raíz en `public/` [O] https://docs.astro.build/en/basics/project-structure/ (consultado
  2026-10). Sitemap con la integración oficial `@astrojs/sitemap` [O]
  https://docs.astro.build/en/guides/integrations-guide/sitemap/ (consultado 2026-10).
- Riesgo: islas `client:only` no se renderizan en servidor.

**Nuxt**
- SSR por defecto. Meta con `useSeoMeta` / `useHead` por página [O]
  https://nuxt.com/docs/api/composables/use-seo-meta (consultado 2026-10). JSON-LD con `useHead`
  y un script `application/ld+json`. Archivos de raíz en `public/` [O]
  https://nuxt.com/docs/guide/directory-structure/public (consultado 2026-10).
- Riesgo: `ssr: false` o `<ClientOnly>` convierten la página en SPA.

**SvelteKit**
- SSR por defecto. Meta y JSON-LD en `<svelte:head>` [O]
  https://svelte.dev/docs/svelte/svelte-head (consultado 2026-10). Archivos de raíz en `static/`
  [O] https://svelte.dev/docs/kit/project-structure (consultado 2026-10).
- Riesgo: `export const ssr = false` en una ruta.

**Gatsby**
- Estático. Meta y JSON-LD con la Head API (`export const Head`) [O]
  https://www.gatsbyjs.com/docs/reference/built-in-components/gatsby-head/ (consultado 2026-10).
  Archivos de raíz en `static/` [O]
  https://www.gatsbyjs.com/docs/how-to/images-and-media/static-folder/ (consultado 2026-10).

**SPA sin SSR (Vite + React, Create React App y similares)**
- El HTML crudo es un `<div id="root">` vacío. Google puede renderizar JS en una segunda pasada
  [O] https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
  (consultado 2026-10), pero la mayoría de los bots de IA no ejecutan JS
  (`references/ai-crawlers.md`).
- Meta y JSON-LD inyectados por JS (react-helmet y similares) tampoco están en el HTML crudo.
- Salida: prerender de las rutas públicas en build, o migrar a un framework con SSR/SSG. Esto es
  **bloqueante** en el gate de lanzamiento si el sitio quiere visibilidad en IA.

**Staging de frameworks:** depende del host (sección 3.1).

### 3.3 WordPress

- **JSON-LD:** sin plugin, el core no emite schema; no verificado si algún tema lo hace. Con Yoast
  o Rank Math, el plugin emite un grafo (Organization, WebSite, WebPage, Article, BreadcrumbList)
  configurable por tipo de contenido. Para schema propio: extender el grafo del plugin con sus
  filtros, no pegar un segundo bloque que duplique la entidad.
- **Metadata:** title, meta, OG y canonical por entrada y por tipo de contenido desde el plugin SEO.
- **robots.txt:** WordPress sirve un robots.txt **virtual** generado por `do_robots()` y
  modificable con el filtro `robots_txt` [O]
  https://developer.wordpress.org/reference/hooks/robots_txt/ (consultado 2026-10). Yoast y Rank
  Math traen editor. Un `robots.txt` **físico** en la raíz del servidor lo sirve el servidor web
  antes que WordPress, y el virtual y los editores dejan de aplicar ⚠️ (comportamiento habitual,
  no documentado como tal en la referencia). Si el editor "no hace nada", busca el archivo físico.
- **llms.txt:**
  - Yoast SEO (versión gratuita, desde 25.3) lo genera en la raíz, lo refresca semanalmente y
    permite usar uno propio [O] https://developer.yoast.com/features/llms-txt/functional-specification/
    · https://yoast.com/help/enable-llmstxt/ (consultado 2026-10).
  - Rank Math: módulo "LLMS Txt" en el dashboard; eliges tipos de contenido y excluye noindex [O]
    https://rankmath.com/kb/llms-txt/ (consultado 2026-10).
  - Sin plugin: archivo físico en la raíz por FTP o el gestor del hosting.
- **Sitemap:** el core genera `/wp-sitemap.xml` desde 5.5 y lo declara en robots.txt [O]
  https://make.wordpress.org/core/2020/07/22/new-xml-sitemaps-functionality-in-wordpress-5-5/
  (consultado 2026-10). Yoast y Rank Math lo sustituyen por el suyo.
- **Staging:** Ajustes → Lectura → "Disuadir a los motores de búsqueda" en staging, y **quitarlo al
  lanzar** (es la causa clásica de un sitio nuevo sin indexar).
- **Riesgo de JS:** bajo con temas clásicos y bloques. Alto con constructores que cargan secciones
  por AJAX, sliders y tabs de plugins.
- **Trampas:** dos plugins SEO activos = schema y meta duplicados. Plugins de caché o seguridad
  pueden bloquear user-agents de bots de IA; prueba con `check_html_crudo.py`.

### 3.4 Shopify

- **JSON-LD:** en el tema (`theme.liquid` para global, plantillas de producto o artículo para
  página). El filtro Liquid `structured_data` emite el JSON-LD de `product` y `article` [O]
  https://shopify.dev/docs/api/liquid/filters/structured_data (consultado 2026-10). Muchos temas
  ya lo traen: **revisa el tema antes de agregar** para no duplicar. Las apps de reseñas y SEO
  suelen inyectar su propio Product ⚠️, y ahí aparecen duplicados.
- **Metadata:** title y meta por producto, colección, página y artículo en "Search engine
  listing". OG y canonical los emite el tema; edítalos en Liquid si hace falta.
- **robots.txt:** editable con la plantilla `robots.txt.liquid` del tema, que reemplaza la salida
  por defecto; Shopify recomienda modificar con Liquid para conservar las reglas que mantiene, y
  soporte no ayuda con esas ediciones [O]
  https://shopify.dev/docs/storefronts/themes/seo/robots-txt (consultado 2026-10).
- **llms.txt:** cada tienda sirve por defecto `/agents.md`, y `/llms.txt` y `/llms-full.txt`
  reflejan ese contenido. Para personalizar: `agents.md.liquid` (cambia los tres) o
  `llms.txt.liquid` (solo `/llms.txt`). Contexto Liquid restringido (solo `request` y `agents`),
  solo en el dominio primario, sin versión por idioma [O]
  https://shopify.dev/docs/storefronts/themes/architecture/templates/llms-txt-liquid ·
  https://shopify.dev/changelog/customize-llmstxt-llms-fulltxt-and-agentsmd (consultado 2026-10).
  Otros archivos arbitrarios en la raíz: no; queda el redirect a Files ⚠️.
- **Sitemap:** automático en `/sitemap.xml`.
- **Staging:** la tienda con contraseña no se indexa; el dominio `*.myshopify.com` redirige al
  primario ⚠️ (verificar con `curl -I`).
- **Riesgo de JS:** bajo en temas Liquid. Alto en storefronts headless (Hydrogen u otros) si no
  renderizan en servidor; aplica la sección 3.2.
- **Trampas:** actualizar el tema puede pisar tus ediciones de Liquid. Los filtros de colección y
  "cargar más" por JS esconden productos al HTML crudo.

### 3.5 Squarespace

- **JSON-LD:** Code Injection global (header) o por página (Page Settings → Advanced → Page Header
  Code Injection). Disponible en Core, Plus, Advanced y algunos planes legacy; al bajar de plan el
  código deja de aplicarse [O]
  https://support.squarespace.com/hc/en-us/articles/205815908-Using-code-injection (consultado
  2026-10). Squarespace emite schema propio; qué tipos exactos, no verificado: revisa el HTML
  crudo antes de agregar para no duplicar.
- **Metadata:** SEO title y description por página e item en su panel de SEO; OG con la imagen
  social. Canonical lo emite la plataforma; no verificado si se edita.
- **robots.txt:** **no editable**. Todos los sitios usan el mismo archivo [O]
  https://support.squarespace.com/hc/en-us/articles/206543207-Understanding-Google-SEO-emails-and-console-errors
  (consultado 2026-10). Solo hay dos casillas en Crawlers: bloquear buscadores y "Block known
  artificial intelligence crawlers" (desmarcada por defecto) [O]
  https://support.squarespace.com/hc/en-us/articles/360022347072-Request-that-AI-models-exclude-your-site
  (consultado 2026-10). Confirma que la casilla de IA esté **desmarcada** si el cliente quiere
  citación.
- **llms.txt:** nativo en sitios 7.1: panel SEO/AI Visibility → SEO Settings → pestaña LLMS.txt,
  apagado por defecto [O]
  https://support.squarespace.com/hc/en-us/articles/47434125611277-Create-an-llms-txt-file
  (consultado 2026-10). En 7.0: no verificado.
- **Sitemap:** automático en `/sitemap.xml`.
- **Staging:** el sitio en prueba o con contraseña no se indexa; no verificado el comportamiento del
  subdominio `*.squarespace.com` tras conectar dominio.
- **Riesgo de JS:** no verificado; corre `check_html_crudo.py` en páginas con bloques de
  colecciones o sumarios.
- **Trampas:** robots.txt no se puede tocar; si necesitas reglas finas, solo queda el borde
  (sección 2A) con los cuidados de DNS.

### 3.6 Wix y Wix Studio

- **JSON-LD:** por página en la sección Structured Data Markup del panel SEO de la página. Solo
  JSON-LD, menos de 7,000 caracteres por bloque, hasta 5 por página, y **solo en páginas
  estáticas** [O] https://support.wix.com/en/article/add-structured-data-markup-to-your-sites-pages
  (consultado 2026-10). Para productos, servicios de Bookings, posts, eventos y foro se edita en
  SEO Settings por tipo de página. Páginas dinámicas de CMS: el soporte oficial dice que no; hay
  reportes de que Wix Studio permite conectar campos ⚠️. Validar en el HTML servido.
- **Metadata:** title, description, OG y canonical por página y por patrón de tipo de página en SEO
  Settings.
- **robots.txt:** editable en SEO & GEO → Tools and settings → Robots.txt Editor, con reset al
  default; soporte no ayuda con cambios [O]
  https://support.wix.com/en/article/editing-your-sites-robotstxt-file (consultado 2026-10).
- **llms.txt:** Wix lo **genera y mantiene solo**; se edita en SEO & GEO → Go to llms.txt, y se
  apaga con "Use your llms.txt file". Requiere plan pagado, dominio propio e indexación activa [O]
  https://support.wix.com/en/article/understanding-your-sites-llmstxt-file (consultado 2026-10).
  Revisa el autogenerado: describe al negocio con las palabras de Wix, no las tuyas.
- **Sitemap:** automático.
- **Staging:** sitios gratuitos en `*.wixsite.com`; no verificado si se indexan. Lanzar con dominio
  conectado y revisar canonical.
- **Riesgo de JS:** no verificado. Velo que llena texto en el navegador queda fuera del HTML
  crudo ⚠️. Corre `check_html_crudo.py`.
- **Trampas:** JSON-LD inyectado con Velo en páginas dinámicas a veces no lo detecta Google ⚠️ (foro).

### 3.7 Webflow

- **JSON-LD:** campo **Schema** de Page Settings o un **Code Embed**, nunca los dos. En plantillas
  CMS se bindean campos dentro del JSON-LD (`"headline": "{{ Post Title }}"`). Reference,
  Multi-reference y Multi-image **no bindean**: reestructurar a Plain text, Option o Number.
  Custom code requiere Site plan pagado o Workspace pagado [O]
  https://help.webflow.com/hc/en-us/articles/33961357265299-Custom-code-in-head-and-body-tags
  (consultado 2026-10).
- **Metadata:** Page Settings por página; en Collection templates, bindeado a campos. Canonical
  global en el formato del dominio primario (con `www` si aplica, sin barra extra).
- **robots.txt:** Site Settings → SEO → robots.txt. Pegar la plantilla completa y agregar
  `Sitemap:` al final.
- **llms.txt:** **nativo** desde julio 2025: Site Settings → SEO → LLMs.txt, subir archivo UTF-8
  de menos de 100 KB; se sirve en la raíz y queda fuera del índice [O]
  https://help.webflow.com/hc/en-us/articles/43240104183315 ·
  https://webflow.com/updates/introducing-llmstxt (consultado 2026-10; datos de tamaño y fecha
  vía resultado de búsqueda, la página dio 403 al abrirla). Plan requerido: no verificado. Un
  solo archivo. Los métodos viejos (redirect a asset) quedan como respaldo.
- **Sitemap:** automático. Fijar el dominio primario **antes** de generarlo; `/sitemap.xml` no se
  puede borrar después.
- **Staging:** desactivar la indexación del subdominio `.webflow.io` (Site Settings → SEO).
- **Riesgo de JS:** tabs, acordeones y sliders nativos suelen estar en el HTML. Listas CMS
  filtradas o paginadas por JS (Finsweet y similares) y embeds que hacen fetch, no.
- **Trampas:** canonical mal armado genera URLs tipo `//contacto`. Ver `checklist-lanzamiento.md`.

### 3.8 Framer

- **JSON-LD:** por página en Page Settings (custom code del `<head>`); global en Site Settings →
  Code. En páginas CMS, bindear a campos. El custom code de Site Settings **no se localiza**: sale
  igual en `/en/`.
- **Metadata:** title, description y OG por página en Page Settings; en CMS, bindeados.
- **robots.txt:** Framer genera uno; para uno propio, subirlo como Static File, que reemplaza al
  default [O] https://www.framer.com/help/articles/how-can-i-access-the-robots-txt-file
  (consultado 2026-10).
- **llms.txt:** Static Files / Well-known files; se sirve en `/llms.txt` [O]
  https://www.framer.com/help/articles/llms-txt-framer/ ·
  https://www.framer.com/help/articles/well-known-files (consultado 2026-10). Plan: los artículos
  no coinciden (Pro y Enterprise en uno; Pro, Scale y Enterprise en otro, hasta 30 archivos por
  proyecto). Confirma en el plan del cliente.
- **Sitemap:** automático.
- **Staging:** el subdominio `.framer.app` / `.framer.website` no debe competir con el primario;
  confirma canonical a producción.
- **Riesgo de JS:** code components que traen datos con fetch no aparecen en el HTML crudo.
- **Trampas:** H1 duplicado por `div.ssr-variant` cuando escritorio y móvil difieren en estructura;
  no es error (`verificar_metadata.py` lo marca INFO). Capas nuevas nacen sin traducir en
  Localization.

### 3.9 Ghost

- **JSON-LD:** el helper `{{ghost_head}}` del tema ya emite meta y JSON-LD de schema.org [O]
  https://ghost.org/docs/themes/helpers/ghost_head_foot (consultado 2026-10). Para agregar:
  Settings → Code Injection → Site Header (global) o code injection en los ajustes de cada post
  (por página). Tipos exactos que emite por defecto: no verificado; revisa antes de duplicar.
- **Metadata:** meta, OG y Twitter por post y página desde sus ajustes; canonical por post
  editable.
- **robots.txt:** un `robots.txt` en la raíz del tema reemplaza el default de Ghost [O]
  https://ghost.org/help/modifying-robots-txt/ (consultado 2026-10). En Ghost(Pro), subir un tema
  propio requiere plan Creator o superior ⚠️ (foro). Hay un reporte de un tema roto tras subirlo ⚠️.
- **llms.txt:** mismo mecanismo de archivos en la raíz del tema ⚠️; no verificado en documentación
  oficial.
- **Sitemap:** automático en `/sitemap.xml`.
- **Staging:** el modo privado cambia robots.txt a restrictivo ⚠️ (foro).
- **Riesgo de JS:** bajo (render de servidor con Handlebars). Modo headless: depende del front.

### 3.10 HubSpot CMS

- **JSON-LD:** en el campo **Head HTML** de cada página (Settings → Advanced → Additional code
  snippets) o en el head HTML del sitio por dominio [O]
  https://knowledge.hubspot.com/website-and-landing-pages/create-and-customize-pages (consultado
  2026-10). En plantillas, con HubL en el tema. Guía oficial específica de schema: no verificada.
- **Metadata:** title y meta description por página en sus ajustes; OG y canonical los emite el
  tema.
- **robots.txt:** editable en Settings → Content → Pages → SEO & Crawlers, por defecto para todos
  los dominios o por dominio (el específico gana); solo aplica a dominios conectados a HubSpot [O]
  https://knowledge.hubspot.com/seo/prevent-content-from-appearing-in-search-results (consultado
  2026-10).
- **llms.txt:** **sin soporte nativo** verificado; un archivo subido queda en `/hubfs/...`, no en la
  raíz (idea abierta en la comunidad) ⚠️
  https://community.hubspot.com/t5/HubSpot-Ideas/Support-LLMs-txt-in-HubSpot-CMS/idi-p/1136969 .
  Hay apps del marketplace que lo sirven con redirect. Respaldo: sección 2B o 2A.
- **Sitemap:** HubSpot genera y deja editar el sitemap por dominio [O]
  https://knowledge.hubspot.com/domains-and-urls/view-and-edit-a-hubspot-hosted-domain-sitemap
  (consultado 2026-10).
- **Staging:** los dominios de sistema con `hs-sites` siempre van en noindex [O] (mismo artículo de
  search results).
- **Riesgo de JS:** bajo en módulos estándar; no verificado para módulos personalizados con fetch.

---

## 4. Tabla resumen

Sí = nativo · Parcial = con condición o plan · No = bloqueado. Después del `/`, el respaldo.

| Plataforma | 1. JSON-LD | 2. Meta/OG/canonical | 3. robots.txt | 4. llms.txt en raíz | 5. HTML crudo |
|---|---|---|---|---|---|
| HTML estático | Sí | Sí | Sí | Sí | Sí |
| Next.js / Astro / Nuxt / SvelteKit / Gatsby | Sí | Sí | Sí | Sí | Sí con SSR/SSG / Parcial si hay islas de cliente |
| SPA sin SSR | Parcial (por JS) / prerender | Parcial / prerender | Sí | Sí | **No** / prerender o SSR |
| WordPress | Sí (plugin) | Sí (plugin) | Sí (virtual o físico) | Sí (Yoast, Rank Math o archivo) | Sí / revisar constructores |
| Shopify | Sí (tema) / cuidar duplicados | Sí | Sí (`robots.txt.liquid`) | Sí (default + `llms.txt.liquid`) | Sí en Liquid / Parcial en headless |
| Squarespace | Parcial (plan con Code Injection) | Sí | **No** (solo casillas) / borde | Sí (7.1) | No verificado / `check_html_crudo.py` |
| Wix / Wix Studio | Parcial (estáticas; dinámicas limitadas) | Sí | Sí | Sí (autogenerado, plan pagado) | No verificado / `check_html_crudo.py` |
| Webflow | Sí (plan pagado; binding limitado) | Sí | Sí | Sí (nativo) | Sí / cuidado con listas por JS |
| Framer | Sí | Sí | Parcial (plan con Static Files) | Parcial (plan con Static Files) | Sí / cuidado con code components |
| Ghost | Sí | Sí | Parcial (tema propio) | Parcial ⚠️ (tema) / borde | Sí |
| HubSpot CMS | Sí (Head HTML) | Sí | Sí | **No** / redirect o borde | Sí / no verificado en módulos con fetch |

---

## 5. Cómo cerrar en cualquier plataforma

1. Llenar la tabla de la sección 4 para el sitio del cliente con lo **servido**, no con lo que dice
   el panel: `scripts/check_html_crudo.py URL` y `curl -s dominio.com/robots.txt`,
   `curl -sI dominio.com/llms.txt`.
2. Cada "No" o "Parcial" va al gate de lanzamiento (`checklist-lanzamiento.md`) con su respaldo o
   como limitación declarada al cliente.
3. Nunca dos fuentes de la misma entidad: si la plataforma ya emite schema, se extiende o se
   reemplaza, no se suma otro bloque.
