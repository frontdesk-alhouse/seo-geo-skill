# Launch checklist (any platform)

Mandatory gate before publishing any client site, whether it runs on WordPress, Shopify,
Squarespace, Wix, Webflow, Framer, a code framework or plain HTML. These are the mistakes that
break SEO and that show up again and again. Run it **before** pointing the domain and **before**
publishing. Severity of each failure per `references/seo-core.md`.

Every item is generic; the **How** says what to check, and where it lives on your platform is in
`references/platforms.md`. Webflow and Framer specifics are at the end, under **Platform notes**.

---

## 1. Indexing and staging

- [ ] **The staging or preview domain is not indexable.** If Google indexes staging, it splits
      the signal with duplicates. How: `noindex` or password protection on staging; the exact
      setting is in `references/platforms.md`.
- [ ] No important page set to `noindex` by accident. How: check the indexing setting of every
      key page and confirm the served HTML has no `<meta name="robots" content="noindex">`.
- [ ] `robots.txt` allows the important pages and blocks low-value ones. How: open the served
      `https://domain.com/robots.txt`, not the one you think you wrote.

## 2. Domain and sitemap

- [ ] **The primary domain is set before the sitemap is generated.** If the sitemap goes out with
      the wrong domain, the URLs end up as 301s and confuse the crawler. How: the platform's
      domain setting (see `references/platforms.md`), then regenerate the sitemap.
- [ ] XML sitemap enabled and reflecting the real public surface (no staging, no `noindex`
      pages, no drafts). How: open `/sitemap.xml` and compare it with the design sitemap.

## 3. Canonicals

- [ ] Canonical in the primary domain format: if it is `www`, include `www`, and no extra
      trailing slash. (A malformed canonical produces URLs like `//contact`.) How:
      `scripts/verificar_metadata.py`.
- [ ] Canonicals on dynamic pages (CMS items, collections, products, posts) point to
      **production**, not staging.

## 4. Metadata

- [ ] Unique, descriptive `<title>` per page (50 to 60 chars).
- [ ] Unique meta description per page (120 to 160 chars).
- [ ] OG title / description / image (1200×630) per page.
- [ ] In dynamic content templates (CMS, collections, products), everything above bound to fields
      so each item is unique.
- [ ] `scripts/verificar_metadata.py` reports no gaps or duplicates.

How: where each per-page field is edited is in `references/platforms.md`; formulas in
`references/metadata-og.md`.

## 5. Schema markup

- [ ] Baseline applied: Organization + WebSite (home), BreadcrumbList (interior pages).
- [ ] Vertical applied where it fits (medical / saas / product / real-estate).
- [ ] **Schema in one place only.** Never the same entity twice (for example, a plugin or theme
      that already outputs schema plus a block pasted by hand). How: count the
      `<script type="application/ld+json">` blocks in the served HTML; see
      `references/platforms.md`.
- [ ] Dynamic content: the fields that fill the JSON-LD are bound and come out with a value on
      every item. How: open two or three items and read the served JSON-LD.
- [ ] Validated in **validator.schema.org** and **Google Rich Results Test** → 0 errors.
- [ ] Only **visible** content on the page is marked up.

## 6. Assets and links

- [ ] Every image with descriptive alt text and readable file names.
- [ ] No broken or insecure links (HTTP on an HTTPS site).
- [ ] Heading hierarchy and focus states checked (overlaps with SEO).

How: any crawler or accessibility auditor; if the platform ships its own tools, see
`references/platforms.md`.

## 7. Performance

- [ ] LCP < 2.5 s · INP < 200 ms · CLS < 0.1.
- [ ] Images with explicit dimensions, AVIF/WebP formats, lazy loading below the fold.

## 8. GEO gate

References: `ai-crawlers.md`, `llms-txt.md`, `entity-sameas.md`, `analytics-ai.md`,
`citation-measurement.md`.

- [ ] `robots.txt` **does not block** `OAI-SearchBot`, `PerplexityBot`, `Claude-SearchBot`,
      `Googlebot` or `Bingbot` (`scripts/check_html_crudo.py`). If the client asked for a
      training opt-out, only training bots are blocked
      (`templates/robots-ai-optout-training.txt`).
- [ ] The **key copy and the JSON-LD are in the raw HTML**, not only after JS runs
      (`check_html_crudo.py` with a bot user agent). Check tabs, accordions, filtered lists,
      embeds and components that fetch data.
- [ ] `llms.txt` published at the root and returning 200. **Optional**; if it is published, tell
      the client it is a courtesy, not a lever. Where to upload it: `references/platforms.md`.
- [ ] Every `sameAs` URL **was opened** and the profile matches (name, credentials, address).
- [ ] Site verified in **Bing Webmaster Tools**, sitemap submitted.
- [ ] **AI channel in GA4** created (custom channel group placed above Referral).
- [ ] **Visible last-updated date** on key pages (services, pricing, guides).
- [ ] If the client has their own **Cloudflare** zone in front of the site: check that AI bot
      blocking and the training control do not stop search bots.
- [ ] **Prompt battery set up** (`templates/prompt-battery.template.md`) and **baseline run**
      before publishing content changes, so there is something to compare against.

## 9. Post-launch

- [ ] Submit the sitemap in **Search Console** and in **Bing Webmaster Tools**.
- [ ] **URL Inspection** on 2 or 3 key pages → confirm Google detects the schema.
- [ ] Check the Enhancements report (valid rich results or errors) a few days later.
- [ ] Schedule citation measurement at 30 and 60 days.

---

## Platform notes: Webflow and Framer

The other platforms (WordPress, Shopify, Squarespace, Wix, code frameworks, plain HTML) are in
`references/platforms.md`.

### Webflow

- **Staging:** disable indexing of the `.webflow.io` subdomain (Site Settings → SEO → subdomain
  indexing OFF).
- **Per-page noindex:** checked in the Page Settings of every key page.
- **Domain and sitemap:** set the primary domain in Site Settings → Publishing **before**
  generating the sitemap. Webflow generates the XML sitemap automatically. Watch out:
  **`/sitemap.xml` cannot be deleted** once created; get it right the first time.
- **Canonical:** the global canonical follows the primary domain format (with `www` if that is
  the primary, no extra trailing slash); canonicals on CMS pages point to production.
- **Metadata:** title, description and OG in Page Settings; in Collection templates, bound to CMS
  fields so each item is unique.
- **Schema in one place only:** Page Settings Schema field **or** Code Embed, never both.
- **CMS:** bind fields inside the JSON-LD (`"headline": "{{ Post Title }}"`). **Reference,
  Multi-reference and Multi-image do NOT bind**; restructure to Plain text, Option or Number if
  needed.
- **robots.txt** in Site Settings → SEO. **llms.txt** natively, also in Site Settings → SEO
  (since Jul 2025; see `references/llms-txt.md`).
- **Assets and links:** if you have the Webflow MCP skills, `asset-audit` (alt text and readable
  names), `link-checker` (broken links or HTTP on HTTPS) and `accessibility-audit` (headings and
  focus states).
- **JS-loaded content:** copy placed by JS (tabs, accordions, filtered lists, embeds that fetch)
  is invisible to most AI bots; confirm with `check_html_crudo.py`.

### Framer

- **Meta per page:** title, description, OG and JSON-LD in each page's **Page Settings** (the
  JSON-LD in that page's `<head>` custom code). On CMS pages, bind to fields.
- **robots.txt:** your own only via **Static Files**, available on Pro plans or higher. On lower
  plans Framer's default stays; check that it does not block search bots.
- **llms.txt:** upload it in Site Settings → Hosting → Files (robots.txt, llms.txt or any file at a fixed URL).
- **Duplicate H1 that is not an error:** Framer serves a full copy of the page per breakpoint group (`div.ssr-variant` with `hidden-*` classes) when desktop and mobile differ in structure. The raw HTML carries two `<h1>` with the same text and only one is shown. `verificar_metadata.py` reports it as INFO; do not fix it.
- **Translations:** every new layer is born untranslated in the Localization view; the `/en/` page shows the Spanish text until it is filled in. Check the locale's "New" filter before publishing.
- **Per-page custom code is not localized:** the JSON-LD in Site Settings → Code ships unchanged on `/en/` (with `inLanguage: es-MX`).
- **Staging:** the `.framer.app`/`.framer.website` subdomain must not compete with the primary
  domain; confirm the canonical points to production.
- **JS-loaded content:** code components that fetch data do not appear in the raw HTML; run
  `check_html_crudo.py`.
