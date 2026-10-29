# SaaS / software product: JSON-LD

> Extends `baseline.jsonld.md`. For clients whose product **is** the software: B2B platforms,
> tools, web apps. Fictional example used below: Nimbus CRM.
>
> Not to be confused with `product.jsonld.md`, which is for **physical product catalogs**.

## First things first, because it is almost always oversold

`SoftwareApplication` **is only eligible for the app rich result if it carries `offers` or
`aggregateRating`**. Without one of the two, the block serves entity understanding and the AI answer
layer, but **it produces no visual result in the SERP**.

A pre-launch SaaS usually has neither: it does not publish pricing yet and it has no reviews.
**They are not invented.** Mark up the block for entity understanding and tell the client exactly that.

---

## 1. SoftwareApplication (Home)

Goes on the home page, next to the baseline `Organization` + `WebSite`. Canonical `@id`: `#app`.

```json
{
  "@type": "SoftwareApplication",
  "@id": "https://{{domain}}/#app",
  "name": "{{product_name}}",
  "url": "https://{{domain}}/",
  "applicationCategory": "BusinessApplication",
  "applicationSubCategory": "{{category in plain language}}",
  "operatingSystem": "Web browser",
  "publisher": { "@id": "https://{{domain}}/#org" },
  "featureList": [
    "{{capability 1, worded as the user sees it on the page}}",
    "{{capability 2}}"
  ]
}
```

### `applicationCategory` values

Use the schema.org enum, not free text. For B2B it is almost always `BusinessApplication`.
Other valid values: `DeveloperApplication`, `FinanceApplication`, `SecurityApplication`,
`CommunicationApplication`, `DesignApplication`. The specificity goes in
`applicationSubCategory`, which is free text.

### `featureList` rule

Each entry corresponds to **something visible on the home page**, worded as it is on the page. It is
not the roadmap, not the internal feature catalog and not what the investor pitch deck says.

When the home page copy changes, `featureList` changes the same day. A `featureList` that promises
what the page no longer says is the easiest misalignment to spot and the hardest to justify.

---

## 2. Offer: only with visible pricing

**Hard condition, all three at once:**

1. The price is **visible on the page**, not only in the schema.
2. The schema price is **identical** to the page price, with no rounding.
3. The currency is the one actually charged.

```json
{
  "@type": "Offer",
  "@id": "https://{{domain}}/pricing#plan-{{slug}}",
  "name": "{{plan name}}",
  "price": "{{number, no currency symbol}}",
  "priceCurrency": "{{USD|MXN}}",
  "url": "https://{{domain}}/pricing",
  "availability": "https://schema.org/InStock",
  "itemOffered": { "@id": "https://{{domain}}/#app" }
}
```

One `Offer` per plan. For usage-based pricing with no fixed plan, use `PriceSpecification` instead of
a flat `price`, or **do not mark up a price at all**, which is usually the right call.

---

## 3. DefinedTerm: the LLM citation play

For the SaaS that is creating a category, or contesting the name of one. The definition page is
structured to be **extracted**, and `DefinedTerm` labels it as such.

```json
{
  "@type": "DefinedTerm",
  "@id": "https://{{domain}}/#term-{{slug}}",
  "name": "{{the term}}",
  "description": "{{VERBATIM copy of the page's first paragraph}}",
  "inDefinedTermSet": {
    "@type": "DefinedTermSet",
    "name": "{{brand}} glossary",
    "url": "https://{{domain}}/{{definition page path}}"
  }
}
```

`description` is a **verbatim copy**, not a summarized version. It is the block that models extract,
so if it differs from what is visible you are marking up content that does not exist.

Before claiming a term, check that an incumbent does not already own it. That is research, not schema,
and it happens first.

---

## 4. Founders (About)

In pre-Series A SaaS, the founders are often the strongest credibility asset. Define them once,
on `/about`, with a reusable canonical `@id`.

```json
{
  "@type": "Person",
  "@id": "https://{{domain}}/#{{name}}",
  "name": "{{full name}}",
  "jobTitle": "{{formal title}}",
  "worksFor": { "@id": "https://{{domain}}/#org" },
  "sameAs": ["{{real LinkedIn URL}}"]
}
```

`sameAs` is the property that contributes most to person entity resolution. **Ask for it, do not
guess it**: a wrong profile is worse than none.

---

## What NEVER to mark up on a SaaS site

| Prohibited | Why |
|---|---|
| `aggregateRating` without verifiable public reviews | Policy violation. The #1 temptation for a new SaaS |
| `Review` about a competitor on `/vs/` or `/compare/` pages | Can trigger a manual action |
| `offers` with "from $X" when the page shows no price | Policy violation #1 |
| Client logos without written authorization | Legal risk before SEO risk |
| `featureList` with roadmap capabilities | Mark up what the page says today |
| Guessed `sameAs` | Pollutes entity resolution |

---

## Map by page, typical SaaS site

| Page | Schema |
|---|---|
| Home | `Organization` + `WebSite` + `SoftwareApplication` + `WebPage` (+ `FAQPage` if there is a visible FAQ) |
| Product and its child pages | `BreadcrumbList` + `WebPage` |
| Audience pages | `BreadcrumbList` + `WebPage`. Nothing else |
| Pricing | `BreadcrumbList` + `WebPage` + **conditional** `Offer` |
| Comparisons | `BreadcrumbList` + `WebPage`. **Zero `Review`** |
| Category definition | `Article` + `DefinedTerm` |
| Blog | `Blog` / `BlogPosting` with a real person as author |
| About | `AboutPage` + `Person` per founder |
| Legal | none |

## Implementation in Webflow

The **Schema field in Page Settings** is native and can be written via API with
`data_pages_tool > bulk_update_pages_schema_markup`. Use it instead of a Code Embed: it satisfies the
schema-in-one-place rule and stays readable with `query_pages_schema_markup`.

Two API limits worth knowing before planning:

- **There is no `create_folder`.** `create_page` accepts `parentFolderId`, but the folder is created
  by hand in the Designer. Nested URLs depend on that manual step.
- **There is no `delete_page`.** A page created with the wrong slug can only be deleted in the
  Designer. Only create pages whose slug is final.

## How to document the case

Save a `SCHEMA_JSONLD.md` in the client folder with the template applied page by page and
include the decisions about what was left out and why (price not visible, no reviews, no logos).
