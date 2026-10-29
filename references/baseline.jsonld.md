# Baseline JSON-LD: va en TODO sitio

Estos tres tipos son el núcleo obligatorio de cualquier sitio que salga del estudio. Las plantillas por
vertical **extienden** este baseline, no lo reemplazan. Rellena solo con datos reales y visibles.

Placeholders: `{{ ... }}`. Elimina las propiedades que no apliquen, Google prefiere **pocas
propiedades completas y correctas** sobre muchas malformadas.

## Disciplina de `@id`: el grafo conectado (regla dura)

Cada entidad estable del sitio tiene un **`@id` canónico** que se **reusa idéntico en TODA página**.
Así Google entiende que todas las páginas hablan de la misma entidad (no es magia del contenedor
`@graph`, es la identidad consistente + las relaciones explícitas lo que conecta el grafo).

IDs canónicos por sitio (fíjalos una vez y no los cambies):
- `https://{{domain}}/#org` (o `#practice` para un negocio local), la organización/negocio
- `https://{{domain}}/#website`, el sitio
- `https://{{domain}}/#dr` / `#persona`, una persona clave (médico, fundador, agente)
- Por página: `.../#webpage`, `.../#breadcrumb`, `.../#service`, `.../#procedimiento`, etc.

Enlaza con `isPartOf`, `about`, `author`, `publisher`, `member`, `parentOrganization` apuntando al
`@id` correcto, **no** repitas el objeto completo de una entidad ya definida; referénciala por `@id`.

> `@graph` es **recomendado** (agrupa entidades relacionadas de una página), pero Google también
> acepta bloques anidados o múltiples `<script>`. Lo que importa es el `@id` consistente y las
> relaciones válidas, no el contenedor por sí mismo.

---

## 1. Organization (Home): identidad de marca

Va en la home. Habilita logo/marca en el knowledge panel. Si el negocio tiene ubicación física
y atiende clientes ahí, usa `LocalBusiness` (o un subtipo) en vez de `Organization`, ver
`local-seo.md`.

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://{{domain}}/#org",
  "name": "{{business_name}}",
  "url": "https://{{domain}}/",
  "logo": "https://{{domain}}/{{logo_path}}",
  "description": "{{one_line_description}}",
  "sameAs": [
    "{{instagram_url}}",
    "{{facebook_url}}",
    "{{linkedin_url}}"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "{{+52...}}",
    "contactType": "customer service",
    "areaServed": "MX",
    "availableLanguage": ["Spanish"]
  }
}
```

## 2. WebSite: nombre del sitio para búsqueda

Va en la home junto con Organization. Define el nombre canónico del sitio.

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "@id": "https://{{domain}}/#website",
  "name": "{{site_name}}",
  "url": "https://{{domain}}/",
  "inLanguage": "es-MX",
  "publisher": { "@id": "https://{{domain}}/#org" }
}
```

> Nota: `SearchAction` / Sitelinks Search Box **ya no da rich result** (retirado en 2026).
> No lo agregues esperando el buscador en el SERP.

## 3. BreadcrumbList: en cada página interior

Reemplaza la URL cruda por una ruta legible en resultados. Refleja la jerarquía real del sitemap.

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Inicio",
      "item": "https://{{domain}}/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "{{section_name}}",
      "item": "https://{{domain}}/{{section_slug}}"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "{{page_name}}"
    }
  ]
}
```

> El último item no lleva `item` (es la página actual).

---

## Cómo emitirlo

Un solo `<script>` por bloque, o combina varios en un array `@graph`:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization", "...": "..." },
    { "@type": "WebSite", "...": "..." }
  ]
}
</script>
```

En Webflow: pega en el campo Schema de Page Settings (home → Organization + WebSite; interiores
→ BreadcrumbList) o en un Code Embed. En CMS, bindea `{{ campos }}` dinámicos.
