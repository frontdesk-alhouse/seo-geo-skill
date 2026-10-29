# Technical SEO baseline: checklist, page types, formulas and severity

> The floor of any site before talking about schema or GEO. If this is broken, nothing else
> matters: an AI assistant does not cite what the search engine cannot crawl or index.

Principles:
1. Technical blockers first, content second.
2. One page, one primary search intent.
3. Long-term quality signals; no tricks.
4. Mobile-first indexing: review on mobile.
5. Every recommendation points to a specific page or asset and can be implemented.

---

## 1. Technical checklist

### Crawling
- [ ] `robots.txt` lets important pages through and blocks only low-value surfaces
      (internal search, parameters, carts).
- [ ] `robots.txt` does not block AI search bots (see `ai-crawlers.md`).
- [ ] No key page sits more than 3 clicks from the home page.
- [ ] Redirects: **2 hops max** from the old URL to the final one; no loops.
- [ ] No broken internal links on key paths.

### Indexing
- [ ] No important page set to `noindex` by accident (meta robots and `X-Robots-Tag` header).
- [ ] One consistent URL format (with or without `www`, with or without trailing slash, always
      the same).
- [ ] Canonical present, absolute, pointing to production, self-consistent and loop-free.
- [ ] No duplicate URLs competing without canonical control.
- [ ] XML sitemap reflects the real public surface and is submitted in Search Console and Bing.
- [ ] Multilingual site: reciprocal `hreflang` on every version, with `x-default`.
- [ ] Staging not indexed.

### Performance (Core Web Vitals, 75th percentile field data)
| Metric | Good | Typical fixes |
|---|---|---|
| LCP | < 2.5 s | Preload the hero image, remove render-blocking work |
| INP | < 200 ms | Trim heavy JS, break up long tasks |
| CLS | < 0.1 | Explicit dimensions on images and embeds, reserve space |

Field data (Search Console, CrUX) outranks local Lighthouse, which varies a lot between runs.

### On-page structure
- [ ] A single `H1` that says what the page is about.
- [ ] `H2` and `H3` reflect the real content hierarchy, not the visual size someone wanted.
- [ ] Descriptive alt text on images that carry content.
- [ ] Key copy is in the served HTML, not injected by JS (see `ai-crawlers.md`).

---

## 2. Page type → schema.org

| Page type | Schema | Note |
|---|---|---|
| Home | `Organization` or a `LocalBusiness` subtype + `WebSite` | A single organization `@id` across the whole site |
| Interior | `BreadcrumbList` | Reflects the real navigation path |
| Service | `Service` with `provider` pointing to the organization `@id` | |
| Physical product | `Product` + `Offer` | Price and availability only if visible |
| Software | `SoftwareApplication` | `Offer` only with a published price |
| Article, blog | `Article` / `BlogPosting` with `datePublished` and `dateModified` | Dates equal to the visible ones |
| Person (physician, founder, author) | `Person` with verified `sameAs` | See `entity-sameas.md` |
| Contact, location | `LocalBusiness` with NAP identical to the Google profile | See `local-seo.md` |
| FAQ | `FAQPage` only if the page **is** visible questions and answers | No rich result since 2026-05-07 |
| Coined term | `DefinedTerm` | Useful to give a nameable stance its own entity |

---

## 3. Title and meta formulas

**Title** (50 to 60 characters, concept first, readable by a person):

```text
Main topic + concrete modifier | Brand
```
Examples: `Minimally Invasive Spine Surgery in Austin | Example Clinic` ·
`Inventory Software for Hardware Stores | Example App`.

**Meta description** (120 to 160 characters, honest, no promises):

```text
What you do + for whom + one concrete fact that backs it + next step
```

Rules: unique per page; no brand name repeated as the title; no keyword lists; in CMS templates,
bound to the item's fields.

---

## 4. Internal links and anchors

- Link from strong pages (home, main services) to the ones you want to rank.
- Descriptive anchor: "herniated disc surgery", not "see more" or "click here".
- Every new page gets at least 2 links from relevant existing pages and gives at least one back.
- Orphan pages (no inbound links) get linked or retired.

---

## 5. Keyword → page map

1. Define the intent: informational, commercial or transactional.
2. Gather real variants (autocomplete, Search Console, customer questions).
3. Prioritize by intent match, likely value and competition.
4. **One cluster per page**: a primary keyword and its close variants live on a single URL.
5. Detect cannibalization: if two URLs fight over the same cluster, consolidate or differentiate.

| Cluster | Intent | URL | Primary keyword | Variants |
|---|---|---|---|---|

---

## 6. Severity taxonomy

| Level | What it is | Examples |
|---|---|---|
| **Critical** | Prevents important pages from being crawled, indexed or cited. Fixed before launch | `noindex` on the home page; `robots.txt` blocks `/` or blocks `OAI-SearchBot`; looping canonical or one pointing to staging; chain of 3 or more redirects; staging indexed; key copy exists only after JS runs |
| **High** | Hurts relevance or eligibility on key pages | Missing or duplicate titles or metas; multiple `H1`s; invalid or missing JSON-LD on key types; schema marking up content that is not visible; CWV in the red on important pages; `sameAs` pointing to profiles that do not exist |
| **Medium** | Weakens, but does not block | Thin content; missing alt; generic anchors; orphan pages; cannibalization; no visible last-updated date on key pages |
| **Low** | Polish | Title a bit long; OG without its own image on secondary pages; descriptions that could be better |

## 7. Finding format

```text
[HIGH] Duplicate titles on service pages
Page: /services/* (12 URLs)
Evidence: all 12 return "Services | Brand" in the served HTML (verificar_metadata.py, 2026-10-28)
Why it matters: the search engine cannot tell which page answers which intent
Fix: template title = "{{service name}} in {{city}} | Brand"
```

Finding rules: always a specific page or URL, reproducible evidence (command, screenshot or
snippet of the served HTML, with date) and a fix the recipient can implement without asking.
No SEO folklore and no manipulative patterns.
