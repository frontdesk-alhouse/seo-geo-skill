# Metadata + Open Graph: per page

One per page, all unique. The `<title>` and meta description are what the user sees in the
SERP; OG/Twitter cards are what shows up when the link is shared on social or WhatsApp. The base title and meta formulas live in `seo-core.md`; this file covers applying them per page.

---

## Title tag (50-60 characters)

```text
Main Concept: Specific Modifier | Brand
```

- Concept/keyword first, readable by humans (no stuffing).
- Unique per page. Do not let them all collapse to the same default.

Examples:
- `Apartments in Brooklyn with Amenities | Example Realty`
- `Endoscopic Spine Surgery: Neurosurgery Austin | Dr. Elena Ruiz`

## Meta description (120-160 characters)

```text
Action + topic + value proposition + one supporting detail.
```

- Honest, describes the actual page, main topic worked in naturally.
- Not a ranking factor, but it moves CTR.

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

- `og:locale`: use the site's locale (`es_MX` for Mexican Spanish, `en_US` for US English).
- `og:image`: **1200×630 px**, < 1 MB, absolute URL. It decides whether the link looks good when
  shared.

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

- Absolute URL, format consistent with the primary domain (if it is `www`, include it; no extra
  trailing slash). It must point to **production**, never to `.webflow.io` staging.

## In Webflow

Title, meta description, OG image and canonical are filled in **Page Settings** (and in the
Collection template for CMS pages, binding `{{ fields }}`). Do not duplicate in custom code what
you already set in Page Settings.
