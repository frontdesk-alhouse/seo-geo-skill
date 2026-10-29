# Baseline JSON-LD: goes on EVERY site

These three types are the mandatory core of any site the studio ships. The per-vertical templates
**extend** this baseline, they do not replace it. Fill in only real, visible data.

Placeholders: `{{ ... }}`. Remove any property that does not apply: Google prefers **a few
complete, correct properties** over many malformed ones.

## `@id` discipline: the connected graph (hard rule)

Every stable entity on the site has a **canonical `@id`** that is **reused verbatim on EVERY page**.
That is how Google understands that all pages talk about the same entity (it is not the magic of the
`@graph` container; consistent identity plus explicit relationships is what connects the graph).

Canonical IDs per site (set them once and never change them):
- `https://{{domain}}/#org` (or `#practice` for a local business), the organization/business
- `https://{{domain}}/#website`, the site
- `https://{{domain}}/#dr` / `#person`, a key person (physician, founder, agent)
- Per page: `.../#webpage`, `.../#breadcrumb`, `.../#service`, `.../#procedure`, etc.

Link with `isPartOf`, `about`, `author`, `publisher`, `member`, `parentOrganization` pointing to the
correct `@id`. Do **not** repeat the full object of an entity that is already defined; reference it by `@id`.

> `@graph` is **recommended** (it groups related entities on a page), but Google also accepts
> nested blocks or multiple `<script>` tags. What matters is the consistent `@id` and valid
> relationships, not the container itself.

---

## 1. Organization (Home): brand identity

Goes on the home page. Enables the logo/brand in the knowledge panel. If the business has a physical
location and serves customers there, use `LocalBusiness` (or a subtype) instead of `Organization`, see
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
    "telephone": "{{phone_e164}}",
    "contactType": "customer service",
    "areaServed": "US",
    "availableLanguage": ["English"]
  }
}
```

## 2. WebSite: the site name for search

Goes on the home page alongside Organization. Defines the canonical site name.

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "@id": "https://{{domain}}/#website",
  "name": "{{site_name}}",
  "url": "https://{{domain}}/",
  "inLanguage": "en-US",
  "publisher": { "@id": "https://{{domain}}/#org" }
}
```

> `inLanguage` must match the language of the site (for example `en-US`, `es-MX`).

> Note: `SearchAction` / Sitelinks Search Box **no longer produces a rich result** (retired in 2026).
> Do not add it expecting the search box in the SERP.

## 3. BreadcrumbList: on every interior page

Replaces the raw URL with a readable path in results. Mirrors the real hierarchy of the sitemap.

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
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

> The last item has no `item` (it is the current page).

---

## How to emit it

One `<script>` per block, or combine several in a `@graph` array:

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

In Webflow: paste into the Schema field of Page Settings (home: Organization + WebSite; interior pages:
BreadcrumbList) or into a Code Embed. In the CMS, bind dynamic `{{ fields }}`.
