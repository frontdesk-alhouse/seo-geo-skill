---
name: seo-geo
description: "Executable layer of technical SEO, schema and GEO for any site (Webflow, Framer, WordPress, Shopify, Squarespace, Wix, code frameworks or plain HTML): generates JSON-LD and metadata, robots.txt for AI bots and llms.txt, runs the launch gate and measures how often the business is cited in AI assistants (ChatGPT, Gemini, Claude, AI Overviews and AI Mode)."
argument-hint: "[vertical: medical|saas|product|real-estate|generic] [site URL or path] [--measure | --gate | --schema-only]"
---

# SEO + Schema + GEO

> Turns a brand, a sitemap and its copy into **valid schema, complete metadata, a clean technical
> layer and a surface AI assistants can cite**, and then **measures** whether the business shows
> up in those assistants. This is not theory: it produces the JSON-LD you paste into your
> platform, the `robots.txt`, the draft `llms.txt`, the gate you run before launch and the citation
> baseline.

**Input**: $ARGUMENTS (client vertical + production URL or local site path + mode)

| Mode | Runs |
|---|---|
| no flag | Steps 1 to 6 (build and launch) |
| `--schema-only` | Steps 2 and 3 |
| `--gate` | Step 6 on a site that is already live |
| `--measure` | Step 7 (prompt battery, runs, index and census) |

The Spanish flags `--solo-schema` and `--medir` are accepted too.

```text
/seo-geo medical https://example.com
/seo-geo generic https://example.com --gate
/seo-geo saas https://example.com --measure
```

---

## Business truth (read before promising the client anything)

Full evidence, tagged and dated, in `references/geo-evidence.md`. Non-negotiable:

- **Schema = entity understanding and rich-result eligibility, not citations.** Ahrefs (May 2026)
  added JSON-LD to 1,885 pages against 4,000 controls: no significant lift in AI Mode or ChatGPT,
  and AIO slightly down [E]. You do it because it organizes the entity, not as a switch.
- **AI Overviews and AI Mode ask for nothing extra.** Google (2025-12-10): no additional
  requirements, no special schema, no text files for AI; what counts is being indexed and
  snippet-eligible [O]. AI Mode in Spanish has been live in Mexico since 2025-09-23 [O].
- **llms.txt is speculative.** No engine documents using it; Google called it "purely
  speculative" [M as a lever]. Publish it as a cheap courtesy, never sell it as GEO.
- **The FAQ rich result ended on 2026-05-07**, and HowTo in 2023 [O]. Do not add `FAQPage`
  expecting a visual result.
- **There is no ranking in assistants.** SparkToro/Gumshoe (2026) ⚠️: fewer than 1 in 100 runs
  repeats the same list of brands [E]. Report **% of runs with a mention, as a range**, never
  "position in ChatGPT".
- **The KPI is citation and mention, not traffic.** Pew (2025) and Reuters DNR (2026): roughly 1%
  to 4% of clicks go to sources from summaries and chatbots [E].
- Real organic traffic is moved by content, demonstrable authority, correct technical work and
  intent. Schema is finish, not engine.

---

## When to use it

- A site comes out of the design workflow and needs its SEO, schema and GEO layer before going
  live.
- A production site needs schema, metadata, `robots.txt` for AI bots or `llms.txt`.
- Before pointing the domain or publishing: run the gate (`--gate`).
- The client asks "do I show up in ChatGPT?": answer with measurement (`--measure`), not opinion.
- 30 and 60 days after publishing changes, then quarterly: repeat the measurement.

---

## Flow (7 steps)

### 1. Technical SEO baseline
Crawling, indexing, canonical, redirects (2 hops max), sitemap, robots, hreflang, Core Web
Vitals, one H1 and a real hierarchy. Checklist, page types, formulas and severity taxonomy in
`references/seo-core.md`. Fix technical blockers **before** optimizing content.

### 2. Schema per page
Baseline **always**; on top of it, the vertical template:

| Page | Schema | Reference |
|---|---|---|
| Home (every site) | `Organization` (or a `LocalBusiness` subtype) + `WebSite` | `baseline.jsonld.md` |
| Any interior page | `BreadcrumbList` | `baseline.jsonld.md` |
| Business with a location | `LocalBusiness` + NAP identical to the Google profile | `local-seo.md` |
| Medical | `Person` (physician) + `MedicalClinic` + `SurgicalProcedure` / `MedicalProcedure` | `medical.jsonld.md` |
| SaaS / software | `SoftwareApplication` (`Offer` only with a visible price), `DefinedTerm`, founder `Person` | `saas.jsonld.md` |
| Physical catalog | `Product` + `Offer`, `Brand`, `AggregateRating` only if it is real | `product.jsonld.md` |
| Real estate | `RealEstateAgent`, `RealEstateListing`, `Residence`, `Offer` | `real-estate.jsonld.md` |
| Blog / editorial | `Article` / `BlogPosting` | `seo-core.md` |

- Fill the placeholders (`{{business_name}}`, `{{price}}`, ...) with **real** data from the
  brief. One canonical `@id` per entity, reused identically across the site.
- **Hard rule:** mark up only **visible** content. Reviews or prices that are not on the page are
  the number one policy violation and can cost a manual action.
- JSON-LD only, in `<script type="application/ld+json">`. Never Microdata or RDFa, never the same
  entity twice.

### 3. Metadata and Open Graph
`references/metadata-og.md`: `<title>` of 50 to 60 characters with the concept first, an honest
meta description of 120 to 160, OG and Twitter card with a 1200×630 image. Unique per page.

### 4. On-site GEO (citable surface)
Prioritized levers and how to write them in `references/geo-aeo.md`; the evidence for each one in
`geo-evidence.md`. On the page, not in a separate file:

- **Direct answer** in the first paragraph of every key page; answer the question, do not circle
  it.
- **Tables** to compare, specify or list prices; lists wherever there are steps.
- **Visible last-updated date** and a quarterly review of the pages that matter.
- **Prices or ranges** when they exist; "from" with conditions beats "request a quote".
- **First-hand experience**: cases, verifiable figures of your own, the method explained.
- **A nameable stance**: a thesis with its own name is citable; "the best solution" is not.
- **Say what the product or service does NOT do**: it reduces attribution errors.
- City and service together on the same URL when the business is local.

### 5. AI bots, llms.txt and entity
- `robots.txt`: by default it **allows everything**; the training opt-out variant blocks only
  training bots and never search bots. Bot table, Cloudflare and JS in
  `references/ai-crawlers.md`; ready-made files in `templates/robots-ai-allow.txt` and
  `templates/robots-ai-optout-training.txt`.
- `llms.txt`: draft it with `scripts/generar_llms_txt.py` from the sitemap, curate it by hand with
  `templates/llms.txt.template` and `references/llms-txt.md`. Optional, and stated as such.
- Entity: name, credentials, address and profiles identical everywhere; `sameAs` only to
  profiles that exist and match. Per-vertical checklist in `references/entity-sameas.md`.
- No figure or credential goes to a public surface unverified: a false fact spreads and outlives
  its source.

### 6. Launch gate
The full `launch-checklist.md` (includes the **GEO gate** block and the Webflow and Framer notes), plus:

- `scripts/check_html_crudo.py URL`: the HTML each bot receives contains the key copy and the
  JSON-LD; `robots.txt` does not block search bots; `llms.txt` and the sitemap respond.
- `scripts/verificar_metadata.py`: lengths, duplicates, canonical and OG per page.
- **validator.schema.org** and **Google Rich Results Test**: 0 errors.
- Client verified in **Bing Webmaster Tools** and an AI channel created in **GA4**
  (`references/analytics-ai.md`).

### 7. Citation measurement
Full protocol in `references/citation-measurement.md`:

1. Battery from `templates/prompt-battery.template.md` (unbranded, branded and third party
   searching families); the set does not change between rounds.
2. N=3 runs per query and assistant, in the session mode the reference specifies; the session
   is declared as an uncontrolled variable.
3. Each run in `templates/run.template.md`.
4. `scripts/indice_citacion.py`: Citation Index with interval, first place, unbranded subtotal,
   search rate and source census.
5. `scripts/verificar_fuentes.py`: every cited URL gets opened; live, dead, or does not say what
   the assistant claimed.
6. Deliver with `templates/geo-report.template.md`.

---

## How to apply it

The skill does not depend on the platform. Any platform works if it allows these five things:

1. **JSON-LD in the HTML**, site-wide (Organization + WebSite) and per page.
2. **Title, meta description, OG and canonical** editable per page (and bound to fields on
   dynamic content).
3. **`robots.txt` at the root** of the domain, editable.
4. **Files at the root** such as `llms.txt` (optional).
5. **The key copy in the server-rendered HTML**, not only after JS runs; check it with
   `scripts/check_html_crudo.py`.

Where each piece goes on your platform (WordPress, Shopify, Squarespace, Wix, Webflow, Framer,
code frameworks and plain HTML), and what to do if one of them is not allowed:
`references/platforms.md`. The Webflow and Framer details checked at the gate are in the platform
notes of `launch-checklist.md`.

---

## References

| File | Purpose |
|---|---|
| `references/seo-core.md` | Technical checklist, page type to schema, formulas, links, keyword to page map, severity |
| `references/baseline.jsonld.md` | Organization + WebSite + BreadcrumbList and `@id` discipline |
| `references/medical.jsonld.md` · `saas.jsonld.md` · `product.jsonld.md` · `real-estate.jsonld.md` | Per-vertical templates |
| `references/metadata-og.md` | Title, meta, OG and Twitter cards |
| `references/local-seo.md` | LocalBusiness, Google profile and NAP |
| `references/backlinks.md` | Inbound link audit |
| `references/geo-evidence.md` | GEO evidence base with [E]/[O]/[S]/[M] tags and dates |
| `references/geo-aeo.md` | On-site levers and how to write them |
| `references/ai-crawlers.md` | AI bots, robots.txt, Cloudflare and raw HTML |
| `references/llms-txt.md` | What it is, what it is not, anatomy, hosting |
| `references/entity-sameas.md` | Entity consistency and `sameAs` per vertical |
| `references/citation-measurement.md` | Battery, N=3 protocol, Citation Index, census |
| `references/analytics-ai.md` | GA4 AI channel, Bing WMT AI Performance, Search Console |
| `references/report-template.md` | Shape of the client SEO + GEO report |
| `references/platforms.md` | Where each piece goes per platform: WordPress, Shopify, Squarespace, Wix, Webflow, Framer, frameworks and plain HTML |
| `launch-checklist.md` | Launch gate for any platform, with GEO gate and Webflow and Framer notes |
| `templates/` | Battery, run, GEO report, `llms.txt`, two `robots.txt` files |
| `examples/` | Fictional runs for testing the scripts |

## Scripts

Python 3, standard library only; each one has `--help`.

| Script | What it does |
|---|---|
| `scripts/check_html_crudo.py` | Requests the URL with each bot's user agent and checks key copy, JSON-LD, robots, llms.txt and sitemap |
| `scripts/verificar_metadata.py` | Checks title, meta, canonical and OG per page: lengths, duplicates and gaps |
| `scripts/generar_llms_txt.py` | Sitemap + each page's title and meta → draft `llms.txt` to curate |
| `scripts/indice_citacion.py` | Runs → Citation Index per query and assistant with a Wilson interval and source census |
| `scripts/verificar_fuentes.py` | Cited URLs → HTTP status and whether the page names the business |

## Optional agents

If you have an SEO audit agent (for example `seo-specialist`), use it to audit in read-only mode;
if not, `references/seo-core.md` has the severity taxonomy and the finding format.

---

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Marking up content that is not visible | Schema reflects what is on the page |
| Adding `FAQPage` expecting a rich result | It ended on 2026-05-07; only if the page truly is questions and answers |
| Selling schema as ranking or as AI citations | It is entity understanding and rich results |
| Selling llms.txt as GEO | A cheap courtesy; nobody documents using it |
| Promising a position in ChatGPT | It does not exist; report % of runs with a mention, as a range |
| Inventing a weighted composite "GEO score" | Citation Index per assistant and source census |
| Adding bylines or CTAs as a citation lever | The evidence associates them with fewer citations; add them for business reasons, not GEO |
| Chopping content into little pieces for LLMs or making an "AI version" | Google advises against it; one well-written page |
| Copying third-party reviews onto the site or marking them as your own | Only real, first-party, visible reviews |
| Paying to appear in "best of" lists | It gets detected, does not last and contaminates the entity |
| Publishing an unverified figure or credential | It spreads across assistants and outlives its source |
| Blocking `OAI-SearchBot` or `PerplexityBot` to "avoid training" | Those are search bots; the opt-out targets training bots |
| Schema in two places (field or plugin + hand-written code) | Pick one |
| Generic "improve the SEO" | Every recommendation tied to a page or asset |
