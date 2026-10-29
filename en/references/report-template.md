# Client SEO + GEO report: template

> Structure concept adapted from `AgriciDaniel/claude-seo` (MIT). The shape of the deliverable
> presented to the client. Honest, actionable, no empty jargon.

---

## Structure

### 1. Executive summary (half a page)
- Overall status in one sentence.
- The 3 most important findings.
- What was done / what is left.
- Honest reminder: schema and technical SEO = visibility, CTR and entity understanding; traffic
  is moved by content, authority and intent; in AI assistants, citation is measured, not
  promised.

### 2. Technical SEO
| Item | Status | Action |
|---|---|---|
| Crawling / robots.txt | ✅/⚠️/❌ | |
| Indexing (accidental noindex, staging) | | |
| Canonicals | | |
| XML sitemap | | |
| Core Web Vitals (LCP/INP/CLS) | | |
| HTTPS / redirects | | |

### 3. Schema markup
| Page / type | Schema applied | Validated (Rich Results / validator) | Detected in Search Console |
|---|---|---|---|
| Home: Organization/WebSite | | | |
| Interior pages: BreadcrumbList | | | |
| {{vertical}} | | | |

### 4. On-page
- Unique titles and metas within range.
- Heading hierarchy.
- Image alt text.
- Internal links.

### 5. Content / E-E-A-T
- Authorship and verifiable authority signals (critical for medical).
- Citable surface: direct answer, tables, visible dates, prices (see `geo-aeo.md`).

### 6. Local (if it applies)
- Consistent NAP, verified Google profile, reviews.

### 7. Visibility in AI assistants
The detail goes in `templates/geo-report.template.md`; here it is summarized:

- Unbranded Citation Index per assistant, **as a range** (with interval), against the baseline.
- Branded queries separately: do they describe the business correctly? Is there a wrong figure
  or fact stuck to the name?
- Source census: which URLs back the mention, which are first-party and which third-party,
  which are live.
- GEO technical status: search bots allowed, copy in raw HTML, live `sameAs`.
- Never "position in ChatGPT"; never a composite score.

### 8. Prioritized plan
| Horizon | Actions (each tied to a page, profile or asset) |
|---|---|
| **Quick wins** (this week) | Critical blockers, robots, missing metadata, broken `sameAs`, visible dates |
| **This month** | Direct answer and tables on key pages, third-party profiles corrected, vertical schema |
| **This quarter** | First-hand experience content, earned mentions in sources the census surfaced, new measurement |

---

## Metrics to report (with an honest source)

| Metric | Source |
|---|---|
| Impressions, clicks, CTR, average position | **Search Console** (hard data from Google) |
| Impressions in AI features (AIO, AI Mode and Discover combined; no clicks) | **Search Console**, Generative AI report |
| Citations in Copilot and Bing per page and query | **Bing Webmaster Tools**, AI Performance |
| Sessions referred by assistants | **GA4**, custom AI channel (see `analytics-ai.md`) |
| Citation Index and source census | In-house measurement (`citation-measurement.md`, `scripts/indice_citacion.py`) |
| Indexed pages, valid rich results or errors | Search Console |
| Core Web Vitals | Search Console / PageSpeed Insights |

> Industry figures (for example, lifts from adding tables) are presented as **estimates from
> correlational studies**, with source and date, never as a guarantee. The client's own numbers
> are the truth.
