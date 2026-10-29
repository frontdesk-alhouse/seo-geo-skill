# Checklist de lanzamiento (cualquier plataforma)

Gate obligatorio antes de publicar cualquier sitio de cliente, esté hecho en WordPress, Shopify,
Squarespace, Wix, Webflow, Framer, un framework de código o HTML propio. Son los errores que
rompen el SEO y que se ven una y otra vez. Correr **antes** de apuntar el dominio y **antes** de
publicar. Severidad de cada falla según `references/seo-core.md`.

Cada punto es genérico; el **Cómo** dice qué comprobar y dónde se hace en tu plataforma está en
`references/plataformas.md`. Lo específico de Webflow y Framer está al final, en
**Notas por plataforma**.

---

## 1. Indexación y staging

- [ ] **El dominio de staging o vista previa no es indexable.** Si Google indexa el staging, parte
      la señal con duplicados. Cómo: `noindex` o protección por contraseña en el staging;
      el ajuste concreto en `references/plataformas.md`.
- [ ] Ninguna página importante en `noindex` por accidente. Cómo: revisar el ajuste de indexación
      de cada página clave y confirmar en el HTML servido que no hay `<meta name="robots"
      content="noindex">`.
- [ ] `robots.txt` permite las páginas importantes y bloquea lo de bajo valor. Cómo: abrir
      `https://dominio.com/robots.txt` servido, no el que se cree haber escrito.

## 2. Dominio y sitemap

- [ ] **El dominio primario está fijado antes de generar el sitemap.** Si el sitemap sale con el
      dominio equivocado, las URLs quedan con 301 y confunden al crawler. Cómo: ajuste de dominio
      de la plataforma (ver `references/plataformas.md`), luego regenerar el sitemap.
- [ ] Sitemap XML habilitado y refleja la superficie pública real (ni staging, ni páginas en
      `noindex`, ni borradores). Cómo: abrir `/sitemap.xml` y contrastar con el sitemap de diseño.

## 3. Canonicals

- [ ] Canonical con el formato del dominio primario: si es `www`, con `www`, y sin barra final
      extra. (Un canonical mal armado genera URLs tipo `//contacto`.) Cómo:
      `scripts/verificar_metadata.py`.
- [ ] Canonicals de páginas dinámicas (CMS, colecciones, productos, entradas) apuntan a
      **producción**, no a staging.

## 4. Metadata

- [ ] `<title>` único y descriptivo por página (50 a 60 car.).
- [ ] Meta description única por página (120 a 160 car.).
- [ ] OG title / description / image (1200×630) por página.
- [ ] En plantillas de contenido dinámico (CMS, colecciones, productos), todo lo anterior ligado a
      campos para que cada item sea único.
- [ ] `scripts/verificar_metadata.py` sin faltantes ni duplicados.

Cómo: dónde se edita cada campo por página en `references/plataformas.md`; fórmulas en
`references/metadata-og.md`.

## 5. Schema markup

- [ ] Baseline aplicado: Organization + WebSite (home), BreadcrumbList (interiores).
- [ ] Vertical aplicado donde corresponde (medical / saas / product / real-estate).
- [ ] **Schema en un solo lugar.** Nunca la misma entidad dos veces (por ejemplo, un plugin o tema
      que ya emite schema más un bloque pegado a mano). Cómo: contar los
      `<script type="application/ld+json">` en el HTML servido; ver `references/plataformas.md`.
- [ ] Contenido dinámico: los campos que llenan el JSON-LD están ligados y salen con valor en cada
      item. Cómo: abrir dos o tres items y leer el JSON-LD servido.
- [ ] Validado en **validator.schema.org** y **Google Rich Results Test** → 0 errores.
- [ ] Solo se marca contenido **visible** en la página.

## 6. Assets y links

- [ ] Todas las imágenes con alt descriptivo y nombres de archivo legibles.
- [ ] Sin links rotos ni inseguros (HTTP en sitio HTTPS).
- [ ] Jerarquía de headings y focus states revisados (se traslapa con SEO).

Cómo: cualquier crawler o auditor de accesibilidad; si la plataforma trae herramientas propias,
ver `references/plataformas.md`.

## 7. Performance

- [ ] LCP < 2.5 s · INP < 200 ms · CLS < 0.1.
- [ ] Imágenes con dimensiones explícitas, formatos AVIF/WebP, lazy en lo que está bajo el pliegue.

## 8. Gate GEO

Referencias: `ai-crawlers.md`, `llms-txt.md`, `entidad-sameas.md`, `analytics-ia.md`,
`medicion-citacion.md`.

- [ ] `robots.txt` **no bloquea** `OAI-SearchBot`, `PerplexityBot`, `Claude-SearchBot`,
      `Googlebot` ni `Bingbot` (`scripts/check_html_crudo.py`). Si el cliente pidió opt-out de
      entrenamiento, solo se bloquean bots de entrenamiento (`templates/robots-ai-optout-entrenamiento.txt`).
- [ ] El **copy clave y el JSON-LD están en el HTML crudo**, no solo después de ejecutar JS
      (`check_html_crudo.py` con user-agent de bot). Revisar tabs, acordeones, listas filtradas,
      embeds y componentes que traen datos con fetch.
- [ ] `llms.txt` publicado en la raíz y responde 200. **Opcional**; si se publica, se le dice al
      cliente que es cortesía, no palanca. Dónde se sube: `references/plataformas.md`.
- [ ] Cada URL de `sameAs` **se abrió** y el perfil coincide (nombre, credenciales, dirección).
- [ ] Sitio verificado en **Bing Webmaster Tools**, sitemap enviado.
- [ ] **Canal de IA en GA4** creado (grupo de canales personalizado por encima de Referral).
- [ ] **Fecha visible de actualización** en las páginas clave (servicios, precios, guías).
- [ ] Si el cliente tiene su propia zona de **Cloudflare** delante del sitio: revisar que el
      bloqueo de bots de IA y el control de entrenamiento no frenen bots de búsqueda.
- [ ] **Batería de prompts dada de alta** (`templates/bateria-prompts.template.md`) y **línea base
      corrida** antes de publicar cambios de contenido, para tener contra qué comparar.

## 9. Post-publicación

- [ ] Enviar sitemap en **Search Console** y en **Bing Webmaster Tools**.
- [ ] **URL Inspection** en 2 o 3 páginas clave → confirmar que Google detecta el schema.
- [ ] Revisar el reporte de Enhancements (rich results válidos o con error) unos días después.
- [ ] Agendar la medición de citación a 30 y 60 días.

---

## Notas por plataforma: Webflow y Framer

Las demás plataformas (WordPress, Shopify, Squarespace, Wix, frameworks de código, HTML propio)
están en `references/plataformas.md`.

### Webflow

- **Staging:** desactivar la indexación del subdominio `.webflow.io` (Site Settings → SEO →
  subdomain indexing OFF).
- **noindex por página:** se revisa en Page Settings de cada página clave.
- **Dominio y sitemap:** fijar el dominio primario en Site Settings → Publishing **antes** de
  generar el sitemap. Webflow genera el sitemap XML solo. Ojo: **no se puede borrar
  `/sitemap.xml`** una vez creado; hazlo bien la primera vez.
- **Canonical:** el canonical global va con el formato del dominio primario (con `www` si es el
  primario, sin barra final extra); los canonicals de páginas CMS apuntan a producción.
- **Metadata:** title, description y OG en Page Settings; en templates de Collection, bindeados a
  campos CMS para que cada item sea único.
- **Schema en un solo lugar:** campo Schema de Page Settings **o** Code Embed, nunca los dos.
- **CMS:** se bindean campos dentro del JSON-LD (`"headline": "{{ Post Title }}"`).
  **Reference, Multi-reference y Multi-image NO bindean**; reestructura a Plain text, Option o
  Number si hace falta.
- **robots.txt** en Site Settings → SEO. **llms.txt** nativo, también en Site Settings → SEO
  (desde 2025-07; ver `references/llms-txt.md`).
- **Assets y links:** si tienes los skills del MCP de Webflow, `asset-audit` (alt y nombres
  legibles), `link-checker` (links rotos o HTTP en HTTPS) y `accessibility-audit` (headings y
  focus states).
- **Contenido por JS:** copy colocado por JS (tabs, acordeones, listas filtradas, embeds que hacen
  fetch) no lo ven la mayoría de los bots de IA; confírmalo con `check_html_crudo.py`.

### Framer

- **Meta por página:** title, description, OG y JSON-LD en **Page Settings** de cada página (el
  JSON-LD en el custom code del `<head>` de esa página). En páginas CMS, bindear a campos.
- **robots.txt:** propio solo vía **Static Files**, disponible en planes Pro o superiores. En
  planes menores queda el de Framer; verifica que no bloquee bots de búsqueda.
- **llms.txt:** se sube en Site Settings → Hosting → Files (robots.txt, llms.txt o cualquier archivo en URL fija).
- **H1 duplicado que no es error:** Framer sirve una copia completa de la página por grupo de breakpoints (`div.ssr-variant` con clases `hidden-*`) cuando escritorio y móvil difieren en estructura. El HTML crudo trae dos `<h1>` con el mismo texto y solo uno se muestra. `verificar_metadata.py` lo reporta como INFO; no se arregla.
- **Traducciones:** cada capa nueva nace sin traducir en la vista Localization; el `/en/` muestra el texto en español hasta que se llena. Revisar el filtro "New" del locale antes de publicar.
- **Custom code por página no se localiza:** el JSON-LD de Site Settings → Code sale igual en `/en/` (con `inLanguage: es-MX`).
- **Staging:** el subdominio `.framer.app`/`.framer.website` no debe competir con el dominio
  primario; confirma el canonical hacia producción.
- **Contenido por JS:** code components que traen datos con fetch no aparecen en el HTML crudo;
  pasa `check_html_crudo.py`.
