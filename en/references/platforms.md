# Platforms: applying technical SEO, schema and GEO on any stack

> What each platform allows, where you do it, and what to do when the platform blocks it.
> Tags: [O] official documentation (URL + "checked Oct 2026") · ⚠️ community or secondary source
> only · "not verified" when no source was found. Plans and menus change: confirm in the client's
> dashboard before promising anything. What counts is what gets **served**: always verify with
> `scripts/check_html_crudo.py` and `curl`.

---

## 1. The 5 capabilities every platform must allow

| # | Capability | Why | Reference |
|---|---|---|---|
| 1 | **JSON-LD in the page HTML**, global (Organization, WebSite) and per page or CMS template | Entity and rich-result eligibility | `references/baseline.jsonld.md` |
| 2 | **Title, meta, OG and canonical per page** (and per CMS item) | Snippet, social preview, canonical signal | `references/metadata-og.md` |
| 3 | **robots.txt at the root**, editable | Don't block AI search bots; declare the sitemap | `references/ai-crawlers.md` |
| 4 | **A file at the root** such as `/llms.txt` (and verification files) | Courtesy for agents; domain verification | `references/llms-txt.md` |
| 5 | **Key copy in the raw HTML** (server-rendered), not only injected by JS | Most AI bots don't execute JS | `scripts/check_html_crudo.py` |

If a platform fails on 1, 2 or 5, that is a real SEO problem. If it fails on 3 or 4, there is
almost always a way out (section 2).

## 2. Universal fallback when the platform blocks something

**A. Edge proxy (CDN or edge).** If the domain runs through a proxy you control (Cloudflare with
the orange cloud, Fastly, a reverse proxy), you can serve `/llms.txt` or `/robots.txt` from there
without touching the platform. On Cloudflare, a Worker on the route `domain.com/llms.txt` returns
the file with `Content-Type: text/plain; charset=utf-8` [O]
https://developers.cloudflare.com/workers/configuration/routing/routes/ (checked Oct 2026).

Caveats:
- Changing DNS to put a proxy in front of Shopify, Wix, Squarespace or HubSpot can break SSL or
  the platform's support. Check their domain rules first; not verified per platform.
- A robots.txt served from the edge **overrides** the platform's file. Document which one wins,
  or the next person who edits the dashboard won't see any effect.
- Check that Cloudflare itself isn't rewriting robots.txt (managed robots) or blocking AI search
  bots (`references/ai-crawlers.md`, section 5).

**B. 301 redirect from `/llms.txt` to a hosted file** (a CDN asset or a text page). It works for
people and for most HTTP clients, but the file is no longer "at the root": declare it as a
limitation. **Not valid for robots.txt**: each bot handles a redirected robots.txt by its own
rules, so it is unreliable.

**C. HTML page at `/llms-txt`** with the content as text. Last resort: it is served as HTML.

**D. JS-injected copy the platform can't fix:** there is no sensible edge fallback. Move the copy
into a native, server-rendered block, or use prerender/SSR. Run `check_html_crudo.py` afterward.

---

## 3. Platform by platform

Fixed fields: JSON-LD · Metadata/OG/canonical · robots.txt · llms.txt and root files · sitemap ·
staging · JS risk · gotchas.

### 3.1 Plain HTML and static hosting (Netlify, Vercel, Cloudflare Pages, GitHub Pages)

- **JSON-LD:** `<script type="application/ld+json">` in each file's `<head>`. Global = in the
  shared include or partial; per page = in its file. No binding limits.
- **Metadata:** all by hand in the `<head>`: `<title>`, meta description, OG, Twitter and an
  absolute canonical pointing to production.
- **robots.txt:** a `robots.txt` file at the root of the published directory. Full control.
- **llms.txt:** same, a file at the root. No plan limits.
- **Sitemap:** by hand or from the build's generator; declare it in robots.txt.
- **Staging:**
  - Vercel sets `X-Robots-Tag: noindex` on every Preview Deployment, except when you assign a
    custom domain to a non-production branch [O]
    https://vercel.com/kb/guide/are-vercel-preview-deployment-indexed-by-search-engines
    (checked Oct 2026).
  - Cloudflare Pages sets `X-Robots-Tag: noindex` on every preview deployment by default; the
    production `*.pages.dev` does not get it [O]
    https://developers.cloudflare.com/pages/configuration/preview-deployments/ (checked Oct 2026).
  - Netlify: deploy previews carry `noindex` and it can't be removed ⚠️ (answers.netlify.com
    forum); official docs did not confirm it in this check.
  - GitHub Pages: no custom headers; not verified whether any automatic noindex exists. Use a
    canonical to production.
  - Everywhere: the platform subdomain (`*.vercel.app`, `*.netlify.app`, `*.pages.dev`) stays live
    in production. Canonical to the primary domain, or redirect.
- **JS risk:** low when the HTML is hand-written.
- **Gotchas:** per-file headers (`_headers`, `vercel.json`) handle `X-Robots-Tag` and the
  `Content-Type` of `llms.txt`. Don't block previews with robots.txt: a blocked bot can't read
  the noindex.

### 3.2 JS frameworks (Next.js, Astro, Nuxt, SvelteKit, Gatsby)

General rule: **server rendering or static generation = complete raw HTML**. Anything fetched in
the browser after load does not exist for most AI bots.

**Next.js (App Router)**
- **JSON-LD:** a native `<script type="application/ld+json">` in `layout.js` (global) or `page.js`
  (per page), with `JSON.stringify(data).replace(/</g, '\\u003c')` to avoid XSS; don't use
  `next/script` [O] https://nextjs.org/docs/app/guides/json-ld (checked Oct 2026).
- **Metadata:** a `metadata` object or `generateMetadata()` per route (title, description,
  openGraph, alternates.canonical, robots) [O]
  https://nextjs.org/docs/app/api-reference/functions/generate-metadata (checked Oct 2026).
- **robots.txt and sitemap:** `app/robots.ts` and `app/sitemap.ts` files (or static ones) [O]
  https://nextjs.org/docs/app/api-reference/file-conventions/metadata/robots (checked Oct 2026).
- **llms.txt:** a file in `public/` or a Route Handler at `app/llms.txt/route.ts`.
- **JS risk:** `'use client'` components that load data in `useEffect` leave copy out of the raw
  HTML. Server Components don't.

**Astro**
- Static by default. JSON-LD and meta in the `<head>` of the layout or each page; root files in
  `public/` [O] https://docs.astro.build/en/basics/project-structure/ (checked Oct 2026). Sitemap
  via the official `@astrojs/sitemap` integration [O]
  https://docs.astro.build/en/guides/integrations-guide/sitemap/ (checked Oct 2026).
- Risk: `client:only` islands are not server-rendered.

**Nuxt**
- SSR by default. Meta with `useSeoMeta` / `useHead` per page [O]
  https://nuxt.com/docs/api/composables/use-seo-meta (checked Oct 2026). JSON-LD with `useHead`
  and an `application/ld+json` script. Root files in `public/` [O]
  https://nuxt.com/docs/guide/directory-structure/public (checked Oct 2026).
- Risk: `ssr: false` or `<ClientOnly>` turn the page into an SPA.

**SvelteKit**
- SSR by default. Meta and JSON-LD in `<svelte:head>` [O]
  https://svelte.dev/docs/svelte/svelte-head (checked Oct 2026). Root files in `static/` [O]
  https://svelte.dev/docs/kit/project-structure (checked Oct 2026).
- Risk: `export const ssr = false` on a route.

**Gatsby**
- Static. Meta and JSON-LD with the Head API (`export const Head`) [O]
  https://www.gatsbyjs.com/docs/reference/built-in-components/gatsby-head/ (checked Oct 2026).
  Root files in `static/` [O]
  https://www.gatsbyjs.com/docs/how-to/images-and-media/static-folder/ (checked Oct 2026).

**SPA without SSR (Vite + React, Create React App and similar)**
- The raw HTML is an empty `<div id="root">`. Google can render JS in a second pass [O]
  https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
  (checked Oct 2026), but most AI bots don't execute JS (`references/ai-crawlers.md`).
- Meta and JSON-LD injected by JS (react-helmet and similar) are not in the raw HTML either.
- Way out: prerender the public routes at build time, or move to a framework with SSR/SSG. This is
  a **blocker** in the launch gate if the site wants AI visibility.

**Framework staging:** depends on the host (section 3.1).

### 3.3 WordPress

- **JSON-LD:** without a plugin, core emits no schema; not verified whether any theme does. With
  Yoast or Rank Math, the plugin emits a graph (Organization, WebSite, WebPage, Article,
  BreadcrumbList) configurable per content type. For custom schema: extend the plugin's graph
  through its filters; don't paste a second block that duplicates the entity.
- **Metadata:** title, meta, OG and canonical per post and per content type from the SEO plugin.
- **robots.txt:** WordPress serves a **virtual** robots.txt generated by `do_robots()` and
  modifiable with the `robots_txt` filter [O]
  https://developer.wordpress.org/reference/hooks/robots_txt/ (checked Oct 2026). Yoast and Rank
  Math include an editor. A **physical** `robots.txt` at the server root is served by the web
  server before WordPress runs, so the virtual file and the editors stop applying ⚠️ (common
  behavior, not documented as such in the reference). If the editor "does nothing", look for the
  physical file.
- **llms.txt:**
  - Yoast SEO (free version, since 25.3) generates it at the root, refreshes it weekly and lets you
    supply your own [O] https://developer.yoast.com/features/llms-txt/functional-specification/
    · https://yoast.com/help/enable-llmstxt/ (checked Oct 2026).
  - Rank Math: "LLMS Txt" module in the dashboard; you pick content types and noindex is excluded
    [O] https://rankmath.com/kb/llms-txt/ (checked Oct 2026).
  - No plugin: a physical file at the root via FTP or the host's file manager.
- **Sitemap:** core generates `/wp-sitemap.xml` since 5.5 and declares it in robots.txt [O]
  https://make.wordpress.org/core/2020/07/22/new-xml-sitemaps-functionality-in-wordpress-5-5/
  (checked Oct 2026). Yoast and Rank Math replace it with their own.
- **Staging:** Settings → Reading → "Discourage search engines" on staging, and **turn it off at
  launch** (the classic cause of a new site that never gets indexed).
- **JS risk:** low with classic themes and blocks. High with page builders that load sections via
  AJAX, sliders and plugin tabs.
- **Gotchas:** two active SEO plugins = duplicated schema and meta. Cache or security plugins can
  block AI bot user agents; test with `check_html_crudo.py`.

### 3.4 Shopify

- **JSON-LD:** in the theme (`theme.liquid` for global, product or article templates per page).
  The Liquid `structured_data` filter emits JSON-LD for `product` and `article` [O]
  https://shopify.dev/docs/api/liquid/filters/structured_data (checked Oct 2026). Many themes
  already include it: **check the theme before adding** to avoid duplicates. Review and SEO apps
  often inject their own Product ⚠️, which is where duplicates come from.
- **Metadata:** title and meta per product, collection, page and article under "Search engine
  listing". OG and canonical are emitted by the theme; edit them in Liquid if needed.
- **robots.txt:** editable with the theme's `robots.txt.liquid` template, which replaces the
  default output; Shopify recommends modifying through Liquid to keep the rules it maintains, and
  support won't help with those edits [O]
  https://shopify.dev/docs/storefronts/themes/seo/robots-txt (checked Oct 2026).
- **llms.txt:** every store serves `/agents.md` by default, and `/llms.txt` and `/llms-full.txt`
  mirror that content. To customize: `agents.md.liquid` (changes all three) or `llms.txt.liquid`
  (only `/llms.txt`). Restricted Liquid context (only `request` and `agents`), primary domain
  only, no per-locale version [O]
  https://shopify.dev/docs/storefronts/themes/architecture/templates/llms-txt-liquid ·
  https://shopify.dev/changelog/customize-llmstxt-llms-fulltxt-and-agentsmd (checked Oct 2026).
  Other arbitrary root files: no; the redirect to Files remains ⚠️.
- **Sitemap:** automatic at `/sitemap.xml`.
- **Staging:** a password-protected store is not indexed; the `*.myshopify.com` domain redirects to
  the primary ⚠️ (verify with `curl -I`).
- **JS risk:** low on Liquid themes. High on headless storefronts (Hydrogen or others) if they
  don't server-render; see section 3.2.
- **Gotchas:** updating the theme can overwrite your Liquid edits. Collection filters and JS "load
  more" hide products from the raw HTML.

### 3.5 Squarespace

- **JSON-LD:** global Code Injection (header) or per page (Page Settings → Advanced → Page Header
  Code Injection). Available on Core, Plus, Advanced and some legacy plans; after a downgrade the
  code stops applying [O]
  https://support.squarespace.com/hc/en-us/articles/205815908-Using-code-injection (checked Oct
  2026). Squarespace emits its own schema; exact types not verified: check the raw HTML before
  adding to avoid duplicates.
- **Metadata:** SEO title and description per page and item in its SEO panel; OG via the social
  image. Canonical is emitted by the platform; not verified whether it is editable.
- **robots.txt:** **not editable**. All sites share the same file [O]
  https://support.squarespace.com/hc/en-us/articles/206543207-Understanding-Google-SEO-emails-and-console-errors
  (checked Oct 2026). There are only two checkboxes under Crawlers: block search engines and
  "Block known artificial intelligence crawlers" (unchecked by default) [O]
  https://support.squarespace.com/hc/en-us/articles/360022347072-Request-that-AI-models-exclude-your-site
  (checked Oct 2026). Confirm the AI box is **unchecked** if the client wants citations.
- **llms.txt:** native on 7.1 sites: SEO/AI Visibility panel → SEO Settings → LLMS.txt tab, off
  by default [O]
  https://support.squarespace.com/hc/en-us/articles/47434125611277-Create-an-llms-txt-file
  (checked Oct 2026). On 7.0: not verified.
- **Sitemap:** automatic at `/sitemap.xml`.
- **Staging:** a trial or password-protected site is not indexed; behavior of the
  `*.squarespace.com` subdomain after connecting a domain not verified.
- **JS risk:** not verified; run `check_html_crudo.py` on pages with collection or summary blocks.
- **Gotchas:** robots.txt can't be touched; if you need fine-grained rules, only the edge is left
  (section 2A), with the DNS caveats.

### 3.6 Wix and Wix Studio

- **JSON-LD:** per page in the Structured Data Markup section of the page's SEO panel. JSON-LD
  only, under 7,000 characters per block, up to 5 per page, and **static pages only** [O]
  https://support.wix.com/en/article/add-structured-data-markup-to-your-sites-pages (checked Oct
  2026). Products, Bookings services, blog posts, events and forum are edited in SEO Settings per
  page type. Dynamic CMS pages: official support says no; there are reports that Wix Studio lets
  you connect fields ⚠️. Validate in the served HTML.
- **Metadata:** title, description, OG and canonical per page and per page-type pattern in SEO
  Settings.
- **robots.txt:** editable under SEO & GEO → Tools and settings → Robots.txt Editor, with a reset to
  default; support won't help with changes [O]
  https://support.wix.com/en/article/editing-your-sites-robotstxt-file (checked Oct 2026).
- **llms.txt:** Wix **generates and maintains it automatically**; edit it under SEO & GEO → Go to
  llms.txt, and turn it off with "Use your llms.txt file". Requires a paid plan, a custom domain
  and indexing enabled [O] https://support.wix.com/en/article/understanding-your-sites-llmstxt-file
  (checked Oct 2026). Review the generated file: it describes the business in Wix's words, not
  yours.
- **Sitemap:** automatic.
- **Staging:** free sites live on `*.wixsite.com`; not verified whether they get indexed. Launch
  with the domain connected and check the canonical.
- **JS risk:** not verified. Velo code that fills text in the browser stays out of the raw HTML ⚠️.
  Run `check_html_crudo.py`.
- **Gotchas:** JSON-LD injected with Velo on dynamic pages sometimes isn't detected by Google ⚠️
  (forum).

### 3.7 Webflow

- **JSON-LD:** the **Schema** field in Page Settings or a **Code Embed**, never both. In CMS
  templates, bind fields inside the JSON-LD (`"headline": "{{ Post Title }}"`). Reference,
  Multi-reference and Multi-image **don't bind**: restructure to Plain text, Option or Number.
  Custom code requires a paid Site plan or paid Workspace [O]
  https://help.webflow.com/hc/en-us/articles/33961357265299-Custom-code-in-head-and-body-tags
  (checked Oct 2026).
- **Metadata:** Page Settings per page; in Collection templates, bound to fields. Global canonical
  in the primary-domain format (with `www` if that's the primary, no extra trailing slash).
- **robots.txt:** Site Settings → SEO → robots.txt. Paste the full template and add `Sitemap:` at
  the end.
- **llms.txt:** **native** since July 2025: Site Settings → SEO → LLMs.txt, upload a UTF-8 file
  under 100 KB; it is served at the root and kept out of the index [O]
  https://help.webflow.com/hc/en-us/articles/43240104183315 ·
  https://webflow.com/updates/introducing-llmstxt (checked Oct 2026; size and date from the search
  result, the page returned 403 when opened). Plan required: not verified. One file only. The old
  methods (redirect to an asset) remain as a fallback.
- **Sitemap:** automatic. Set the primary domain **before** generating it; `/sitemap.xml` can't be
  deleted afterward.
- **Staging:** disable indexing of the `.webflow.io` subdomain (Site Settings → SEO).
- **JS risk:** native tabs, accordions and sliders are usually in the HTML. CMS lists filtered or
  paginated by JS (Finsweet and similar) and embeds that fetch are not.
- **Gotchas:** a badly formed canonical produces URLs like `//contact`. See `launch-checklist.md`.

### 3.8 Framer

- **JSON-LD:** per page in Page Settings (custom `<head>` code); global in Site Settings → Code. On
  CMS pages, bind to fields. Site Settings custom code is **not localized**: it ships unchanged on
  `/en/`.
- **Metadata:** title, description and OG per page in Page Settings; bound on CMS pages.
- **robots.txt:** Framer generates one; for your own, upload it as a Static File, which replaces
  the default [O] https://www.framer.com/help/articles/how-can-i-access-the-robots-txt-file
  (checked Oct 2026).
- **llms.txt:** Static Files / Well-known files; served at `/llms.txt` [O]
  https://www.framer.com/help/articles/llms-txt-framer/ ·
  https://www.framer.com/help/articles/well-known-files (checked Oct 2026). Plan: the articles
  disagree (Pro and Enterprise in one; Pro, Scale and Enterprise in another, up to 30 files per
  project). Confirm on the client's plan.
- **Sitemap:** automatic.
- **Staging:** the `.framer.app` / `.framer.website` subdomain must not compete with the primary;
  confirm the canonical points to production.
- **JS risk:** code components that fetch data don't appear in the raw HTML.
- **Gotchas:** duplicate H1 from `div.ssr-variant` when desktop and mobile differ in structure;
  not an error (`verificar_metadata.py` flags it as INFO). New layers start untranslated in
  Localization.

### 3.9 Ghost

- **JSON-LD:** the theme's `{{ghost_head}}` helper already emits meta and schema.org JSON-LD [O]
  https://ghost.org/docs/themes/helpers/ghost_head_foot (checked Oct 2026). To add more: Settings
  → Code Injection → Site Header (global) or code injection in each post's settings (per page).
  Exact default types not verified; check before duplicating.
- **Metadata:** meta, OG and Twitter per post and page from their settings; per-post canonical is
  editable.
- **robots.txt:** a `robots.txt` at the theme root replaces Ghost's default [O]
  https://ghost.org/help/modifying-robots-txt/ (checked Oct 2026). On Ghost(Pro), uploading a
  custom theme requires the Creator plan or higher ⚠️ (forum). One report of a theme breaking
  after the upload ⚠️.
- **llms.txt:** same theme-root file mechanism ⚠️; not verified in official docs.
- **Sitemap:** automatic at `/sitemap.xml`.
- **Staging:** private mode switches robots.txt to restrictive ⚠️ (forum).
- **JS risk:** low (server-rendered Handlebars). Headless mode: depends on the front end.

### 3.10 HubSpot CMS

- **JSON-LD:** in each page's **Head HTML** field (Settings → Advanced → Additional code
  snippets) or in the site head HTML per domain [O]
  https://knowledge.hubspot.com/website-and-landing-pages/create-and-customize-pages (checked Oct
  2026). In templates, with HubL in the theme. Official schema-specific guidance: not verified.
- **Metadata:** title and meta description per page in its settings; OG and canonical are emitted
  by the theme.
- **robots.txt:** editable under Settings → Content → Pages → SEO & Crawlers, as a default for all
  domains or per domain (the specific one wins); applies only to HubSpot-connected domains [O]
  https://knowledge.hubspot.com/seo/prevent-content-from-appearing-in-search-results (checked Oct
  2026).
- **llms.txt:** **no verified native support**; an uploaded file lives under `/hubfs/...`, not at
  the root (open community idea) ⚠️
  https://community.hubspot.com/t5/HubSpot-Ideas/Support-LLMs-txt-in-HubSpot-CMS/idi-p/1136969 .
  Marketplace apps serve it via redirect. Fallback: section 2B or 2A.
- **Sitemap:** HubSpot generates the sitemap per domain and lets you edit it [O]
  https://knowledge.hubspot.com/domains-and-urls/view-and-edit-a-hubspot-hosted-domain-sitemap
  (checked Oct 2026).
- **Staging:** system domains containing `hs-sites` are always noindex [O] (same search-results
  article).
- **JS risk:** low on standard modules; not verified for custom modules that fetch.

---

## 4. Summary table

Yes = native · Partial = with a condition or plan · No = blocked. After the `/`, the fallback.

| Platform | 1. JSON-LD | 2. Meta/OG/canonical | 3. robots.txt | 4. llms.txt at root | 5. Raw HTML |
|---|---|---|---|---|---|
| Static HTML | Yes | Yes | Yes | Yes | Yes |
| Next.js / Astro / Nuxt / SvelteKit / Gatsby | Yes | Yes | Yes | Yes | Yes with SSR/SSG / Partial with client islands |
| SPA without SSR | Partial (via JS) / prerender | Partial / prerender | Yes | Yes | **No** / prerender or SSR |
| WordPress | Yes (plugin) | Yes (plugin) | Yes (virtual or physical) | Yes (Yoast, Rank Math or file) | Yes / check page builders |
| Shopify | Yes (theme) / watch duplicates | Yes | Yes (`robots.txt.liquid`) | Yes (default + `llms.txt.liquid`) | Yes on Liquid / Partial headless |
| Squarespace | Partial (plan with Code Injection) | Yes | **No** (checkboxes only) / edge | Yes (7.1) | Not verified / `check_html_crudo.py` |
| Wix / Wix Studio | Partial (static; dynamic limited) | Yes | Yes | Yes (auto-generated, paid plan) | Not verified / `check_html_crudo.py` |
| Webflow | Yes (paid plan; limited binding) | Yes | Yes | Yes (native) | Yes / watch JS lists |
| Framer | Yes | Yes | Partial (plan with Static Files) | Partial (plan with Static Files) | Yes / watch code components |
| Ghost | Yes | Yes | Partial (custom theme) | Partial ⚠️ (theme) / edge | Yes |
| HubSpot CMS | Yes (Head HTML) | Yes | Yes | **No** / redirect or edge | Yes / not verified for fetch modules |

---

## 5. Closing out on any platform

1. Fill in the section 4 table for the client's site using what is **served**, not what the
   dashboard says: `scripts/check_html_crudo.py URL`, `curl -s domain.com/robots.txt`,
   `curl -sI domain.com/llms.txt`.
2. Every "No" or "Partial" goes into the launch gate (`launch-checklist.md`) with its fallback, or
   as a limitation declared to the client.
3. Never two sources for the same entity: if the platform already emits schema, extend or replace
   it; don't add another block.
