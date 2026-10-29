# Product catalog: JSON-LD (extends baseline)

Typical case: a large industrial catalog (more than a thousand variants, Systems + Variants
collections in Webflow; fictional example: Aceros del Bajío, a Mexican steel supplier). Use this
**on top of** the baseline.

> **This is where the MOST visual rich results are** (price, availability, stars). But a generic
> `Product` gives little advantage: populate price, availability, rating and concrete specs.

---

## 1. Product + Offer (per product/variant: CMS-bound)

One per product page. In Webflow, a Collection template with bound fields.

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{{ Product Name }}",
  "image": "{{ Main Image }}",
  "description": "{{ Description }}",
  "sku": "{{ SKU }}",
  "brand": {
    "@type": "Brand",
    "name": "{{ Brand }}"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://{{domain}}/systems/{{ Slug }}",
    "priceCurrency": "MXN",
    "price": "{{ Price }}",
    "availability": "https://schema.org/{{InStock|OutOfStock|PreOrder}}",
    "itemCondition": "https://schema.org/NewCondition"
  }
}
```

> `price` with no currency symbol and no thousands separator ("14500", not "$14,500"). `priceCurrency`
> goes separately. If the catalog shows no public price, **omit `offers.price`**; do not invent one.

## 2. AggregateRating + Review (only if they exist)

Add this inside `Product` **only** if there are real reviews visible on the page.

```json
{
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "{{ Average Rating }}",
    "reviewCount": "{{ Review Count }}"
  },
  "review": [
    {
      "@type": "Review",
      "author": { "@type": "Person", "name": "{{ Author }}" },
      "reviewRating": {
        "@type": "Rating",
        "ratingValue": "{{ Rating }}",
        "bestRating": "5"
      },
      "reviewBody": "{{ Review Text }}"
    }
  ]
}
```

## 3. System as a collection: ItemList (listing page)

For the page of a System that groups variants, an `ItemList` helps understanding.

```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "{{ System Name }}",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "url": "https://{{domain}}/systems/{{ Variant Slug }}"
    }
  ]
}
```

---

## Product-specific rules

- **Availability and price must match what is visible.** Marking "InStock" on something sold out, or a
  price different from the one shown, is a policy violation and can remove rich result eligibility.
- Also feed Merchant Center / Shopping if the client sells online (the same `Offer` works).
- Webflow fields that do **NOT** bind: Reference, Multi-reference, Multi-image. A catalog that
  already uses spreadsheet naming maps SKU/Brand/Price to Plain text/Number fields.
