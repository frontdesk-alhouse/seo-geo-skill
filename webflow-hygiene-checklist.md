# Checklist de higiene y gate de lanzamiento (Webflow y Framer)

Gate obligatorio antes de publicar cualquier sitio de cliente. Estos son los errores que rompen el
SEO de sitios en Webflow y Framer y que se ven una y otra vez. Correr **antes** de apuntar el
dominio y **antes** de publicar. Severidad de cada falla según `references/seo-core.md`.

---

## 1. Indexación y staging

- [ ] **Desactivar indexación del subdominio `.webflow.io`** (Site Settings → SEO → subdomain
      indexing OFF). Si no, Google indexa el staging y parte la señal con duplicados.
- [ ] Ninguna página importante en `noindex` por accidente (Page Settings de cada página clave).
- [ ] `robots.txt` permite las páginas importantes, bloquea lo de bajo valor.

## 2. Dominio y sitemap

- [ ] **Fijar el dominio primario ANTES de generar el sitemap** (Site Settings → Publishing). Si
      generas el sitemap con el dominio equivocado, las URLs quedan con 301 y confunden al crawler.
- [ ] Sitemap XML habilitado (Webflow lo genera solo) y refleja la superficie pública real.
- [ ] Ojo: **no se puede borrar `/sitemap.xml`** una vez creado; hazlo bien la primera vez.

## 3. Canonicals

- [ ] Canonical global con el formato del dominio primario: si es `www`, incluir el prefijo `www`
      y sin barra final extra. (Un canonical mal armado genera URLs tipo `//contacto`.)
- [ ] Canonicals de páginas CMS apuntan a **producción**, no a staging.

## 4. Metadata (Page Settings)

- [ ] `<title>` único y descriptivo por página (50 a 60 car.).
- [ ] Meta description única por página (120 a 160 car.).
- [ ] OG title / description / image (1200×630) por página.
- [ ] En templates de Collection, todo lo anterior bindeado a campos CMS para que cada item sea
      único.
- [ ] `scripts/verificar_metadata.py` sin faltantes ni duplicados.

## 5. Schema markup

- [ ] Baseline aplicado: Organization + WebSite (home), BreadcrumbList (interiores).
- [ ] Vertical aplicado donde corresponde (medical / saas / product / real-estate).
- [ ] Schema en **un solo lugar** (campo Schema de Page Settings **o** Code Embed, no ambos).
- [ ] CMS: campos dinámicos bindeados; recuerda que **Reference, Multi-reference y Multi-image NO
      bindean**; reestructura a Plain text, Option o Number si hace falta.
- [ ] Validado en **validator.schema.org** y **Google Rich Results Test** → 0 errores.
- [ ] Solo se marca contenido **visible** en la página.

## 6. Assets y links (skills del MCP de Webflow, si los tienes)

- [ ] `asset-audit`: todas las imágenes con alt descriptivo y nombres legibles.
- [ ] `link-checker`: sin links rotos ni inseguros (HTTP en sitio HTTPS).
- [ ] `accessibility-audit`: jerarquía de headings y focus states (se traslapa con SEO).

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
      embeds y code components.
- [ ] `llms.txt` publicado y responde 200. **Opcional**; si se publica, se le dice al cliente que
      es cortesía, no palanca.
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

## Notas Framer

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
