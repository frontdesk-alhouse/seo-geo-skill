# SaaS / producto de software: JSON-LD

> Extiende `baseline.jsonld.md`. Para clientes cuyo producto **es** el software: plataformas B2B,
> herramientas, apps web. Ejemplo ficticio usado abajo: Nimbus CRM.
>
> No confundir con `product.jsonld.md`, que es para **catálogo de productos físicos**.

## Lo primero, porque casi siempre se sobrevende

`SoftwareApplication` **solo es elegible al rich result de aplicación si lleva `offers` o
`aggregateRating`**. Sin uno de los dos, el bloque sirve para comprensión de entidad y para la capa
de respuestas de IA, pero **no produce ningún resultado visual en el SERP**.

Un SaaS pre-lanzamiento normalmente no tiene ninguno de los dos: no publica precio todavía y no
tiene reseñas. **No se inventan.** Se marca el bloque por comprensión de entidad y se le dice al
cliente exactamente eso.

---

## 1. SoftwareApplication (Home)

Va en la home, junto al `Organization` + `WebSite` del baseline. `@id` canónico: `#app`.

```json
{
  "@type": "SoftwareApplication",
  "@id": "https://{{domain}}/#app",
  "name": "{{product_name}}",
  "url": "https://{{domain}}/",
  "applicationCategory": "BusinessApplication",
  "applicationSubCategory": "{{categoría en lenguaje llano}}",
  "operatingSystem": "Web browser",
  "publisher": { "@id": "https://{{domain}}/#org" },
  "featureList": [
    "{{capacidad 1, redactada como la ve el usuario en la página}}",
    "{{capacidad 2}}"
  ]
}
```

### Valores de `applicationCategory`

Usa el enum de schema.org, no texto libre. Para B2B casi siempre es `BusinessApplication`.
Otros válidos: `DeveloperApplication`, `FinanceApplication`, `SecurityApplication`,
`CommunicationApplication`, `DesignApplication`. La especificidad va en
`applicationSubCategory`, que sí es texto libre.

### Regla de `featureList`

Cada entrada corresponde a **algo visible en la home**, redactado como está en la página. No es el
roadmap, no es el catálogo interno de features y no es lo que dice el pitch deck al inversionista.

Cuando el copy de la home cambie, `featureList` cambia el mismo día. Un `featureList` que promete
lo que la página ya no dice es la desalineación más fácil de detectar y la más difícil de
justificar.

---

## 2. Offer: solo con precio visible

**Condición dura, las tres a la vez:**

1. El precio está **visible en la página**, no solo en el schema.
2. El precio del schema es **idéntico** al de la página, sin redondeos.
3. La moneda es la que se cobra de verdad.

```json
{
  "@type": "Offer",
  "@id": "https://{{domain}}/pricing#plan-{{slug}}",
  "name": "{{nombre del plan}}",
  "price": "{{número, sin símbolo de moneda}}",
  "priceCurrency": "{{USD|MXN}}",
  "url": "https://{{domain}}/pricing",
  "availability": "https://schema.org/InStock",
  "itemOffered": { "@id": "https://{{domain}}/#app" }
}
```

Un `Offer` por plan. Para pricing por consumo sin plan fijo, usa `PriceSpecification` en vez de
`price` plano, o **no marques precio en absoluto**, que suele ser lo correcto.

---

## 3. DefinedTerm: la jugada de citación por LLM

Para el SaaS que está creando una categoría, o disputando el nombre de una. La página de
definición se estructura para ser **extraída**, y `DefinedTerm` la etiqueta como tal.

```json
{
  "@type": "DefinedTerm",
  "@id": "https://{{domain}}/#term-{{slug}}",
  "name": "{{el término}}",
  "description": "{{copia LITERAL del primer párrafo de la página}}",
  "inDefinedTermSet": {
    "@type": "DefinedTermSet",
    "name": "{{marca}} glossary",
    "url": "https://{{domain}}/{{ruta de la página de definición}}"
  }
}
```

`description` es **copia literal**, no una versión resumida. Es el bloque que los modelos extraen,
así que si difiere de lo visible se está marcando contenido que no existe.

Antes de reclamar un término, verifica que no lo ocupe ya un incumbente. Es research, no schema, y
se hace antes.

---

## 4. Personas fundadoras (About)

En SaaS pre-Series A los fundadores suelen ser el activo de credibilidad más fuerte. Se definen una
sola vez, en `/about`, con `@id` canónico reusable.

```json
{
  "@type": "Person",
  "@id": "https://{{domain}}/#{{nombre}}",
  "name": "{{nombre completo}}",
  "jobTitle": "{{título formal}}",
  "worksFor": { "@id": "https://{{domain}}/#org" },
  "sameAs": ["{{URL real de LinkedIn}}"]
}
```

`sameAs` es la propiedad que más aporta a resolución de entidad de persona. **Pídela, no la
adivines**: un perfil equivocado es peor que ninguno.

---

## Qué NO marcar nunca en un SaaS

| Prohibido | Por qué |
|---|---|
| `aggregateRating` sin reseñas públicas verificables | Violación de política. Es la tentación #1 de un SaaS nuevo |
| `Review` sobre un competidor en páginas `/vs/` o `/compare/` | Puede disparar acción manual |
| `offers` con "desde $X" cuando la página no muestra precio | Violación de política #1 |
| Logos de cliente sin autorización escrita | Riesgo legal antes que de SEO |
| `featureList` con capacidades del roadmap | Se marca lo que la página dice hoy |
| `sameAs` adivinado | Ensucia la resolución de entidad |

---

## Mapa por página, sitio SaaS típico

| Página | Schema |
|---|---|
| Home | `Organization` + `WebSite` + `SoftwareApplication` + `WebPage` (+ `FAQPage` si hay FAQ visible) |
| Producto y sus hijas | `BreadcrumbList` + `WebPage` |
| Páginas de audiencia | `BreadcrumbList` + `WebPage`. Nada más |
| Pricing | `BreadcrumbList` + `WebPage` + `Offer` **condicional** |
| Comparativas | `BreadcrumbList` + `WebPage`. **Cero `Review`** |
| Definición de categoría | `Article` + `DefinedTerm` |
| Blog | `Blog` / `BlogPosting` con autor persona real |
| About | `AboutPage` + `Person` por fundador |
| Legal | ninguno |

## Implementación en Webflow

El campo **Schema de Page Settings** es nativo y se puede escribir por API con
`data_pages_tool > bulk_update_pages_schema_markup`. Úsalo en vez de un Code Embed: cumple la regla
de schema en un solo lugar y queda releíble con `query_pages_schema_markup`.

Dos límites de la API que conviene conocer antes de planear:

- **No existe `create_folder`.** `create_page` acepta `parentFolderId`, pero la carpeta se crea a
  mano en el Designer. Las URL anidadas dependen de ese paso manual.
- **No existe `delete_page`.** Una página creada con el slug equivocado solo se borra en el
  Designer. Crea únicamente páginas cuyo slug esté cerrado.

## Cómo documentar el caso

Guarda en la carpeta del cliente un `SCHEMA_JSONLD.md` con la plantilla aplicada página por página e
incluye las decisiones de qué se dejó fuera y por qué (precio no visible, sin reseñas, sin logos).
