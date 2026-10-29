# Hygiene checklist and launch gate (Webflow and Framer)

Mandatory gate before publishing any client site. These are the mistakes that break SEO on
Webflow and Framer sites and that show up again and again. Run it **before** pointing the domain
and **before** publishing. Severity of each failure per `references/seo-core.md`.

---

## 1. Indexing and staging

- [ ] **Disable indexing of the `.webflow.io` subdomain** (Site Settings → SEO → subdomain
      indexing OFF). Otherwise Google indexes staging and splits the signal with duplicates.
- [ ] No important page set to `noindex` by accident (Page Settings of every key page).
- [ ] `robots.txt` allows the important pages and blocks low-value ones.

## 2. Domain and sitemap

- [ ] **Set the primary domain BEFORE generating the sitemap** (Site Settings → Publishing). If
      you generate the sitemap with the wrong domain, the URLs end up as 301s and confuse the
      crawler.
- [ ] XML sitemap enabled (Webflow generates it automatically) and reflecting the real public
      surface.
- [ ] Watch out: **`/sitemap.xml` cannot be deleted** once created; get it right the first time.

## 3. Canonicals

- [ ] Global canonical in the primary domain format: if it is `www`, include the `www` prefix
      and no extra trailing slash. (A malformed canonical produces URLs like `//contact`.)
- [ ] Canonicals on CMS pages point to **production**, not staging.

## 4. Metadata (Page Settings)

- [ ] Unique, descriptive `<title>` per page (50 to 60 chars).
- [ ] Unique meta description per page (120 to 160 chars).
- [ ] OG title / description / image (1200×630) per page.
- [ ] In Collection templates, everything above bound to CMS fields so each item is unique.
- [ ] `scripts/verificar_metadata.py` reports no gaps or duplicates.

## 5. Schema markup

- [ ] Baseline applied: Organization + WebSite (home), BreadcrumbList (interior pages).
- [ ] Vertical applied where it fits (medical / saas / product / real-estate).
- [ ] Schema in **one place only** (Page Settings Schema field **or** Code Embed, not both).
- [ ] CMS: dynamic fields bound; remember that **Reference, Multi-reference and Multi-image do
      NOT bind**; restructure to Plain text, Option or Number if needed.
- [ ] Validated in **validator.schema.org** and **Google Rich Results Test** → 0 errors.
- [ ] Only **visible** content on the page is marked up.

## 6. Assets and links (Webflow MCP skills, if you have them)

- [ ] `asset-audit`: every image with descriptive alt text and readable file names.
- [ ] `link-checker`: no broken or insecure links (HTTP on an HTTPS site).
- [ ] `accessibility-audit`: heading hierarchy and focus states (overlaps with SEO).

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
      embeds and code components.
- [ ] `llms.txt` published and returning 200. **Optional**; if it is published, tell the client
      it is a courtesy, not a lever.
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

## Framer notes

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
