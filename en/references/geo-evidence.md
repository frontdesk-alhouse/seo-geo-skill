# GEO: evidence base (cutoff 2026-10-28)

> What moves citations and mentions in ChatGPT, Google AI Overviews (AIO), AI Mode, Gemini, Perplexity,
> Claude and Copilot, separated by strength of evidence. Everything else in the skill points here when
> it needs to justify a lever.

**Tags.** [E] evidenced by a study (almost always correlational: association, not cause) ·
[O] official from the platform · [S] speculative, unaudited vendor or our own inference ·
[M] myth or contradicted by the evidence · ⚠️ the data came through secondary coverage, not the
original study; it is cited with that caveat.

---

## 1. Honest framing (non-negotiable)

- **There is no ranking, no position and no determinism.** SparkToro/Gumshoe (Jan-Mar 2026) ⚠️:
  ~600 volunteers, 12 prompts, ~3,000 runs in consumer UIs; less than 1 in 100 chance of getting the
  same list of brands and less than 1 in 1,000 of the same order [E]. The only metric that holds up is
  **% visibility over many runs**.
  https://searchengineland.com/ai-recommendation-lists-rarely-repeat-study-468076
- **The KPI is citation and mention, not traffic.** Pew (2025-07-22, 900 US adults): with an AI summary,
  clicks on a regular result drop from 15% to 8%, and links inside the summary get ~1% of clicks
  [E]. Reuters Digital News Report 2026 (97,520 respondents, 48 markets): ~4% click through to sources
  from chatbots [E].
- **Nothing is a switch.** No lever (schema, llms.txt, paragraph length) guarantees showing up.
  What you sell is citable surface, a consistent entity and honest measurement.

## 2. What is evidenced

### 2.1 Page content

| Finding | Tag | Source |
|---|---|---|
| Adding quotations +40.9%, statistics +30.6%, fluency +28.0%, citing sources +27.5%, technical terms +17.6%, authoritative tone +10.4%; keyword stuffing −8.3% (position-adjusted visibility) | [E] simulated engines 2023 | Princeton, Aggarwal et al., arXiv 2311.09735, KDD 2024. https://arxiv.org/html/2311.09735v3 |
| Gains are large for the page in 5th place (citing sources +115%) and **negative** for the 1st (−30/−23/−21%); on real Perplexity: quotations +22%, statistics +37% | [E] | Princeton, same paper |
| The paper does **not** contain any "134-167 words per passage" rule | [M] | False attribution circulating in GEO repos |
| Odds of being cited vs ignored (controlling for DR and page type): freshness ≤12 months +88%, year in the title ×2, tables +69% (ChatGPT +88%), methodology explained in "best of" pages +51%, first-hand experience +45%, visible prices +28%, FAQ +26%, lists +22%, schema +13% | [E] association | TJ Robertson / TJ Digital, 2026-10-25. https://tjrobertson.com/ai-citation-study/ |
| Negatives in the same study: **author byline −28%**, CTAs −12%; many images, hard reading and long sentences, slight | [E] association | TJ Robertson 2026-10-25 |
| Cited pages open with a direct answer 20% vs 5%; 23% of cited pages never answer the question vs 50% of ignored ones; promotional tone the same (3.8 vs 3.7) | [E] | TJ Robertson 2026-10-25 |
| URLs cited by AI average 1,064 days old vs 1,432 in organic (25.7% fresher); ChatGPT prefers the newest, AIO barely | [E] ~17M citations | Ahrefs. https://ahrefs.com/blog/do-ai-assistants-prefer-to-cite-fresh-content/ |

TJ Robertson in detail: 78 businesses, 4,167 unbranded questions, 193,507 answers (ChatGPT,
AI Mode, AIO), 943,673 citations, 8 weekly snapshots (Aug 27 to Oct 21, 2026). Limitations it
declares: association is not cause, keywords as a proxy, sample of Peec AI clients, no
downloadable dataset. Use it to prioritize, not to promise percentages.

### 2.2 What kind of page and what site gets cited

- Company sites get 67% of citations (52% consumer/ecommerce, **87% industrial B2B**);
  product page 28%, home 12%, category 10%, profile 9%, articles ~25%; comparisons 2.5%,
  "alternatives to" 0.2% [E] (TJ Robertson 2026-10-25).
- Only 2-5% of cited pages come from Google's top 10; AIO cites 24% from the top 10, AI Mode
  17%, ChatGPT 7% [E] (TJ Robertson). Ahrefs (2026-03-02, 863k keywords): only 38% of AIO citations
  rank top 10, versus 76% in Jul 2025 [E].
  https://ahrefs.com/blog/ai-overview-citations-top-10/
- SE Ranking (Feb 2026, 10k US keywords): 59% of AI Mode citations go to organic results and **36% to
  Google Business Profile listings** [E]. https://seranking.com/blog/ai-mode-research/

### 2.3 Third-party mentions and entity

- Ahrefs (2025-05-26, 75,000 brands, AIO), Spearman with visibility: branded web mentions 0.664,
  branded anchors 0.527, branded search volume 0.392, DR 0.326, backlinks 0.218 [E].
  https://ahrefs.com/blog/ai-overview-brand-correlation/
- Ahrefs (2025-12-12, ChatGPT + AI Mode + AIO): YouTube mentions ~0.737, web mentions
  0.66-0.71 [E]. Ahrefs itself warns: correlation is not causation.
  https://ahrefs.com/blog/ai-brand-visibility-correlations
- Profound (Aug 2024-Jun 2025, 680M citations): ChatGPT cites Wikipedia first (7.8%), Perplexity
  Reddit (6.6%); AIO spreads across Reddit 2.2%, YouTube 1.9%, Quora 1.5%, LinkedIn 1.3% [E].
  https://www.tryprofound.com/blog/ai-platform-citation-patterns
- Semrush (Jan-Feb 2026, 325k prompts): LinkedIn cited in 14.3% of ChatGPT Search answers and
  13.5% of AI Mode answers [E]. https://www.semrush.com/blog/most-cited-domains-ai/
- Yext (2025-10-09, 6.8M citations) [S vendor, sells listings]: 86% of citations from sources the brand
  manages (site 44%, listings 42%); in healthcare, listings 52.6%. **Muck Rack (2025)** ⚠️ says the
  opposite: ~84-94% non-owned sources. Reading: the mix depends on the query type
  (informational cites third parties; local and transactional cite listings and the site). That is why
  the battery tags each query with `query_type`.

### 2.4 Local, reviews and verticals

- BrightLocal (2026-08-26, 1,355 locations US/UK/AU, ~2M citations): GBP is the main source for
  Google's AIs (~28.6%); Yelp appears in 80% of ChatGPT answers; 93% of cited domains
  are individual business sites [E].
  https://www.brightlocal.com/resources/ai-directory-sources/
- 8ight.AI (2026-10-05, search-enabled APIs, 39 trades × 49 cities): businesses with <25 reviews
  named 3.4% vs 22.2% with 1,000+; **star ratings don't matter**; Claude cited Yelp in 92.7% vs
  ChatGPT 0%; Claude searched in only 36.6% of prompts [E, small Claude sample: n=218, API,
  pending replication]. https://ppc.land/chatgpt-names-3-4-of-tested-local-firms-with-under-25-reviews-8ight-finds/
- Medical Economics (2026-08-25, ChatGPT, US, ~33k citations, 1,200 patient prompts): hospital and
  academic rosters 27.5%, specialty boards and associations 22.1%, national directories
  8.3%, state licensing 5.1%, reviews 3.8%; **zero citations to GBP URLs**; practice sites
  with detailed procedure, candidacy and training pages produced more specific
  descriptions [E].
  https://www.medicaleconomics.com/view/before-you-pay-for-ai-visibility-for-your-practice-audit-these-five-sources
- Real estate: Local Falcon (37,500 searches, 100 US cities) only 21.2% of top agents with a
  site were cited; portals and directories dominate [E vendor].

### 2.5 Volatility, accuracy and traffic

- Sistrix (Apr 2026): AI Mode rotates 56% of its citations per week, ChatGPT 74%; AIO stable in a little
  over half of queries [E]. TJ Robertson: week-over-week retention 24-28%, at 7 weeks
  11-16% [E]. Consequence: N=3 per query and a fixed cadence.
- Columbia Tow Center / CJR (Mar 2025, 8 engines, 1,600 queries): >60% of answers with an incorrect
  citation; they invent URLs; ChatGPT Search fully correct only 28% [E]. Consequence: every cited URL
  gets opened and verified.
- Seer Interactive (Sep 2025): organic CTR on queries with AIO fell 61% since mid-2024; brands
  cited in the AIO +35% organic clicks [E correlational ⚠️].
  https://www.seerinteractive.com/insights/aio-impact-on-google-ctr-september-2025-update
- Mention without a supporting citation: 31% in AI Mode, 25% in ChatGPT, 13% in AIO [E] (TJ Robertson).
  ChatGPT runs ~1.8 searches per answer and adds a location in 30% of questions with no city [E].

### 2.6 Schema: the null test

- Ahrefs (May 2026): 1,885 pages that added JSON-LD vs 4,000 controls. AI Mode +2.4% and
  ChatGPT +2.2% (not significant), AIO −4.6% [E]. Only pages already cited.
  https://www.searchenginejournal.com/schema-markup-didnt-move-ai-citations-in-ahrefs-test/574568/
- searchVIU: five AI systems read only the visible HTML and ignore JSON-LD [E ⚠️].
- Bing did state (Mar 2025) that it uses schema for its LLMs [O].
- Reading: schema is **entity understanding and hygiene**, not a citation switch. Do it anyway,
  because it is cheap and feeds classic rich results, but don't sell it as a GEO lever.

## 3. What Google says officially [O]

"AI features and your website" (2025-12-10)
https://developers.google.com/search/docs/appearance/ai-features

- There are no additional requirements or special optimizations to appear in AIO or AI Mode; no
  special schema or AI text files are needed. What counts is being indexed and eligible for a
  snippet.
- Structured data must be consistent with the visible text.
- Controls: `nosnippet`, `data-nosnippet`, `max-snippet`, `noindex`.
- AIO and AI Mode use **query fan-out** (several searches per question).
- AIO/AI Mode traffic counts in Search Console under the "Web" type.
- **Google-Extended** controls only Gemini training and grounding; blocking it does **not** remove you
  from AIO or AI Mode (only blocking Googlebot does that).
- Danny Sullivan (Jan 2026): don't break content into "bite-sized chunks" for LLMs or make
  two versions of the page.
- FAQ rich results stopped showing on 2026-05-07; HowTo deprecated since 2023.
- AI Mode in Spanish, including Mexico, since 2025-09-23.
  https://blog.google/company-news/inside-google/around-the-globe/google-latin-america/google-mexico-20-years/
- Search Console "Generative AI" (beta since 2026-06-03): impressions only, AIO + AI Mode + Discover
  combined, no clicks.

## 4. Myths and pitches we don't make

| Claim | Tag | Why |
|---|---|---|
| "llms.txt gets you into ChatGPT" | [M] | John Mueller (Jun 2025): no AI system uses it; later "purely speculative". No engine documents using it. See `llms-txt.md` |
| "Add FAQPage for the rich result" | [M] | The rich result died on 2026-05-07. A visible FAQ is associated with citations (+26%, TJ Robertson); the schema is not the cause |
| "Schema = more AI citations" | [M] | Ahrefs test May 2026 with no significant effect; Google says it isn't needed |
| "I'll rank you in ChatGPT" | [M] | There is no position; the same list repeats <1% of the time |
| "Chunk your content for LLMs" | [M] | Google (Sullivan, Jan 2026) says no; what is associated with citations is answering directly, not fragmenting |
| "134-167 word passages" | [M] | Not in the Princeton paper |
| "0 to 100 GEO score" with weights | [M] | The weights are made up; no study backs them. The skill reports a Citation Index with an interval and a source census |
| "GPTBot feeds ChatGPT Search" | [M] | The search index is OAI-SearchBot; GPTBot is training. See `ai-crawlers.md` |

**Outdated third-party materials.** The `marketing:seo-audit` plugin skill and any
guide, template or auditor that recommends `FAQPage` or `HowTo` to get rich results is
outdated since 2026-05-07 (FAQ) and 2023 (HowTo). Same for repos that attribute length rules
to Princeton or publish "GEO score" weights. If a tool suggests it, ignore that
recommendation and note it in the report.

## 5. The Spanish-language and LatAm gap

- There is **no** public study of citations in AIO or AI Mode in Spanish. Everything above is US/UK or
  global in English. Applying it to Mexico is inference [S].
- URBAN (2026-09-02, 276 answers to 46 ES/EN prompts) ⚠️: on questions about Mexico, the most
  cited outlet was El País (13); the first Mexican outlet, El Financiero (7). It suggests assistants
  pull from Spain's Spanish-language sources when they don't find a solid Mexican source [S].
- StatCounter Mexico (Aug 2026): ChatGPT 75.1% of chatbot usage, Gemini 16.7% [E]. That is why
  measurement prioritizes ChatGPT and Gemini, plus AIO/AI Mode; Perplexity is optional.
- Practical consequence: your own measurement (`citation-measurement.md`) **is** the local evidence.
  Keep the runs; over time they are the only Spanish-language dataset you will have.

## 6. Timeline of changes (mid-2025 to Oct 2026)

| Date | Change | Tag |
|---|---|---|
| 2025-03 | Bing confirms it uses schema for its LLMs; Claude declares Brave Search as a subprocessor (2025-03-19) | [O] |
| 2025-03 | Tow Center: >60% incorrect citations | [E] |
| 2025-05-26 | Ahrefs: brand mentions, best correlate of AIO visibility | [E] |
| 2025-06 | Mueller: no system uses llms.txt | [O] |
| 2025-07-01 | Cloudflare blocks AI bots by default on new zones; pay-per-crawl in beta | [O] |
| 2025-07-22 | Pew: ~1% of clicks on summary links | [E] |
| 2025-08-04 | Cloudflare accuses Perplexity of stealth crawlers | [O] |
| 2025-09-23 | AI Mode in Spanish in Mexico | [O] |
| 2025-10-09 | Yext 6.8M citations (vendor) | [S] |
| 2025-12-10 | Google publishes "AI features and your website" | [O] |
| 2026-01 | Sullivan: don't chunk content for LLMs | [O] |
| 2026-01 to 03 | SparkToro/Gumshoe: lists almost never repeat | [E] ⚠️ |
| 2026-02 | Bing Webmaster Tools AI Performance in preview; SE Ranking: 36% of AI Mode citations to GBP | [O] / [E] |
| 2026-03-02 | Ahrefs: only 38% of AIO citations in the top 10 | [E] |
| 2026-04 | Sistrix: AI Mode rotates 56%/week, ChatGPT 74% | [E] |
| 2026-05 | Ahrefs: schema with no lift in citations; Webflow AEO GA for Enterprise (2026-05-21); GA4 "AI Assistant" channel (2026-05-13) | [E] / [O] / ⚠️ |
| 2026-05-07 | FAQ rich results die | [O] |
| 2026-06-03 | Search Console "Generative AI" in beta | [O] |
| 2026-08 | BrightLocal (08-26) and Medical Economics (08-25) | [E] |
| 2026-09-15 | Cloudflare: "Disallow AI Training" control that in Block mode can stop Googlebot/Bingbot | [O] ⚠️ |
| 2026-10 | 8ight.AI (10-05) and TJ Robertson (10-25) | [E] |

## 7. Prioritized levers

Ordered by strength of evidence and then by effort. The operational detail lives in `geo-aeo.md`.

| Tier | Lever | Evidence | Effort |
|---|---|---|---|
| 1 | Don't block search bots (OAI-SearchBot, Claude-SearchBot, PerplexityBot, Googlebot, Bingbot) and review the client's Cloudflare | [O] | Low |
| 1 | Key copy and JSON-LD in the raw HTML (no JS dependency) | [E] Vercel/MERJ Dec 2024 | Low-medium |
| 1 | Direct answer at the top of every key page | [E] TJ Robertson | Low |
| 1 | Visible date, year in the title where it applies, quarterly update | [E] TJ Robertson, Ahrefs | Low |
| 1 | Measure with a protocol (N=3, Index with interval, census) before promising anything | [E] SparkToro, Sistrix | Medium |
| 2 | Comparison tables, visible prices, figures with a source, quotations | [E] TJ Robertson, Princeton | Medium |
| 2 | Live, correct third-party surfaces: GBP, vertical directories, rosters, reviews (count and pace) | [E] BrightLocal, SE Ranking, Medical Economics, 8ight | Medium |
| 2 | First-hand experience and explained methodology | [E] TJ Robertson | Medium |
| 2 | A dedicated page that brings together name + service + city on the same URL | [E] TJ Robertson (location in 30% of searches) + our own case | Low |
| 3 | Brand mentions on the web, YouTube, LinkedIn, Reddit (without buying them) | [E] correlational Ahrefs, Semrush | High |
| 3 | Entity consistency and verified `sameAs` | [S] reasonable mechanism, no direct test | Low |
| 3 | Bing Webmaster Tools + IndexNow as insurance | [O] / [S] | Low |
| 4 | Schema beyond the baseline | [E] null on citations | Low, done for classic SEO |
| 4 | llms.txt | [M] as a lever | Low, courtesy |

Caveats from the same study that carries the most weight: the author byline is associated with −28% and CTAs with
−12%. That is no reason to remove authorship in YMYL (E-E-A-T rules there), but it is a reason not to load
the page you want cited with CTAs.
