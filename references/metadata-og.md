# Metadata + Open Graph: por página

Uno por página, todos únicos. El `<title>` y la meta description son lo que el usuario ve en el
SERP; OG/Twitter cards son lo que se ve al compartir en redes/WhatsApp. Las fórmulas base de title y meta viven en `seo-core.md`; aquí está la aplicación por página.

---

## Title tag (50-60 caracteres)

```text
Concepto Principal: Modificador Específico | Marca
```

- Concepto/keyword al frente, legible para humanos (no stuffing).
- Único por página. Nada de que todos colapsen al mismo default.

Ejemplos:
- `Departamentos en Polanco con Amenidades | Inmobiliaria Cantera`
- `Cirugía de Columna Endoscópica: Neurocirugía Monterrey | Dra. Elena Ruiz`

## Meta description (120-160 caracteres)

```text
Acción + tema + propuesta de valor + un detalle de soporte.
```

- Honesta, describe la página real, tema principal de forma natural.
- No es factor de ranking, pero mueve el CTR.

---

## Open Graph (Facebook, LinkedIn, WhatsApp)

```html
<meta property="og:type" content="website">
<meta property="og:title" content="{{title}}">
<meta property="og:description" content="{{description}}">
<meta property="og:url" content="https://{{domain}}/{{slug}}">
<meta property="og:image" content="https://{{domain}}/{{og_image_1200x630}}">
<meta property="og:locale" content="es_MX">
<meta property="og:site_name" content="{{site_name}}">
```

- `og:image`: **1200×630 px**, < 1 MB, con URL absoluta. Es lo que decide si el link se ve bien
  al compartir.

## Twitter / X card

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{title}}">
<meta name="twitter:description" content="{{description}}">
<meta name="twitter:image" content="https://{{domain}}/{{og_image_1200x630}}">
```

---

## Canonical

```html
<link rel="canonical" href="https://{{domain}}/{{slug}}">
```

- URL absoluta, formato consistente con el dominio primario (si es `www`, inclúyelo; sin trailing
  slash extra). Debe apuntar a **producción**, nunca a staging `.webflow.io`.

## En Webflow

Title, meta description, OG image y canonical se llenan en **Page Settings** (y en el template de
Collection para páginas CMS, bindeando `{{ campos }}`). No dupliques en custom code lo que ya pones
en Page Settings.
