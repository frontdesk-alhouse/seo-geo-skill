# GEO / AEO: on-site readiness and citation levers in AI assistants

> Ported and adapted from concepts in `AgriciDaniel/claude-seo` (v2.2.4, MIT).
> Updated in 2026 with operational criteria from a SaaS case and the measurement procedure
> from a medical case; updated 2026-10-28 with the evidence base in
> `geo-evidence.md` (tags [E] study · [O] official · [S] inference · [M] myth).

GEO (Generative Engine Optimization) / AEO (Answer Engine Optimization) is the evolution of SEO
for a SERP where many queries show an AI-generated answer, and for a world where
many people no longer even go through the SERP: they ask an assistant directly.
Risk: zero-click. Opportunity: being the cited source.

**Honest framing, and it is non-negotiable.** In an assistant **there is no ranking, no position and no
determinism**. The same question repeats the same list of brands less than 1 time in 100
(SparkToro/Gumshoe, 2026 [E] ⚠️). What you can offer is citable surface, a consistent
entity and **honest measurement**. The KPI is citation and mention, not traffic. Promising "I'll rank you
in ChatGPT" is the 2026 version of promising rankings from schema.

---

## What actually moves the needle

Twelve levers in two blocks, each with its tag. The full evidence and the priority order
(Tier 1-4) are in `geo-evidence.md` §7.

### Content structure

1. **Direct answer at the top** [E]. Cited pages open by answering 20% of the time vs
   5% of ignored pages; 23% of cited pages never answer the question vs 50% of ignored ones (TJ
   Robertson, 2026-10-25). No filler intro before the answer.
2. **Self-contained passages** [S]. Each key block must make sense without the rest of the page:
   implicit question, answer, context. There is no magic length: the "134-167 words" rule
   that circulates is **not** in the Princeton paper [M]. And you don't chunk the page for LLMs:
   Google advises against it (Sullivan, Jan 2026 [O]).
3. **Concrete data with a source**, not adjectives [E]. Statistics +30.6%, quotations +40.9%,
   citing sources +27.5% (Princeton, KDD 2024, simulated engines). *"erecting a 5,000 m² industrial
   building in 10 weeks"* gets cited; *"incredible results"* doesn't.
4. **Tables and comparative structure** [E]. Tables +69% in citation odds (ChatGPT +88%), lists
   +22% (TJ Robertson). Tables of tiers, criteria and limits: that's what the model reuses as is.
5. **Visible freshness** [E]. Content updated in the last 12 months +88%; year in the title
   ×2 (TJ Robertson); cited URLs 25.7% fresher than organic ones (Ahrefs). A visible update date
   and a real quarterly review, not changing the date without changing the content.
6. **Visible prices** [E] +28% (TJ Robertson). If there is a price or range, publish it; if it
   isn't published, say so.
7. **First-hand experience and methodology** [E]. First-hand +45%; on "best X" pages,
   explaining how the picks were made +51% (TJ Robertson). Your own cases, your own photos, the real process.
8. **A clear, nameable position** [S, our own case]. *"the CRM that fills itself in from WhatsApp"* is citable; *"the best
   platform"* isn't.
9. **Saying what the product or the doctor does NOT do** [S, our own case]. Models reuse
   content that sets boundaries, and it is the only thing that truly differentiates in a saturated category.

**Caveats from the same study** [E, association]: the **author byline** is associated with −28% and
**CTAs** with −12%. In YMYL authorship stays (E-E-A-T rules), but you don't load the page you want
cited with CTAs. Schema only +13%, and in Ahrefs' controlled test (May 2026) no
significant effect.

### Entity and authority

10. **Entity clarity and `sameAs`** [S]. Schema (`Organization`, `Person`, `Product`,
    `MedicalClinic`) and `sameAs` declare what each thing is and which profiles are the same entity. It is the
    cheapest disambiguation, and critical with namesakes. Its value is entity understanding, not a
    citation switch. Detail in `entity-sameas.md`.
11. **Third-party surfaces and demonstrable E-E-A-T** [E]. Branded web mentions are the best
    correlate of AIO visibility (Spearman 0.664, Ahrefs 2025); GBP receives 36% of AI
    Mode citations (SE Ranking, Feb 2026); for doctors, ChatGPT cites hospital rosters and specialty
    boards, not GBP (Medical Economics, 2026-08). Author with credentials, date and sources;
    for a person, a real author anchor (ORCID, Google Scholar) lasts longer than a commercial
    directory.
12. **Narrow category** [S, our own case]. An assistant answers with a proper name when the
    set of defensible answers is small. In a crowded category it picks aggregators; in a
    narrow one it picks people. **If the client is in a saturated category, narrowing the category
    is cheaper than winning it.**

---

## What this channel does differently (findings from measuring real cases)

These came from measuring a medical case (dozens of runs across three assistants, 2026) and a SaaS case. They are principles, not
promises; they change how you plan.

1. **It feeds on what third parties say, not just on the site.** In the measured case, the client's own site
   did not resolve and the assistant still described the client accurately, with the literal language
   of a directory profile. **A live third-party surface is worth more, and sooner, than a site that
   doesn't exist yet.** Rewriting the directory profile can pay off more than waiting for the build.
2. **The identity splits into entities the assistant doesn't join** (person, clinic, site). Each
   one accumulates a fraction of the signal. Fix it with `sameAs`, the exact name everywhere and
   301 redirects from old domains and pages.
3. **A false figure spreads and outlives its source.** A figure the client wrote on a
   profile, unvalidated and contradicted by another of their own figures, appeared in 7 runs even though the profile
   no longer resolved. **You don't fix it by talking to the model: you fix the source**, and even then it takes time.
   Hard rule: no credential or figure goes onto a public surface without being verified.
4. **The competitors who win get in through their own site with name + technique + city on the same
   URL.** ChatGPT adds a location in 30% of questions with no city (TJ Robertson [E]): the page
   has to name service and city together.
5. **The assistant states its criterion, and you have to publish it.** In the medical case, all three
   assistants chose by "how many surgeries of that type they perform per year". If the verifiable figure
   exists, publish it with its backing and date; if not, don't invent it.
6. **Claude ≠ ChatGPT ≠ Gemini.** Different indexes, different sources, different search rates
   (Claude searched in 36.6% of prompts in 8ight.AI 2026 [E, small sample]). Measure and report per
   assistant, never an average.
7. **The source that holds you up can disappear in weeks** (in the measured case, 13 days). That's why
   measurement is repeated and the source census is audited every cycle.

And one verification trap: a directory listing that seemed to return 404 was **anti-bot blocking**.
Before reporting a source as dead, verify with a browser UA.

**Entity consistency is hygiene, not an engine.** In the measured case the entity was
fragmented and contradictory, and it still got cited: what made it appear was the narrow category plus the
distinctive claim. Consistency makes what gets cited **correct and durable**. Don't sell it
as a lever for appearing. And if the assistant sends the patient to the wrong hospital, the harm is
real.

---

## How it's measured (summary)

Full protocol in `citation-measurement.md`; calculation with `scripts/indice_citacion.py`.

- Fixed battery in families F1-F4 (+F5/F6 optional), tagged by `query_type`. **It is not
  changed between runs**; new queries go at the end with their date added.
- N=3 per query and assistant, in the **consumer UI** with a temporary session; the session is a declared
  uncontrolled variable.
- Priority in Mexico: ChatGPT, Gemini, AIO/AI Mode, Claude; Perplexity optional.
- Record names, position, cited URLs, whether it searched, and the stuck claim attached to the name; every URL is
  verified (`scripts/verificar_fuentes.py`).
- Citation Index with a 95% Wilson interval, unbranded subtotal, first place, trigger
  rate and source census. Never a composite "GEO score".
- Cadence: baseline, +30 and +60 days after changes, then quarterly; ChatGPT and AI Mode monthly
  at minimum because they rotate 74% and 56% of citations per week (Sistrix, Apr 2026 [E]).
- And what's worth more: asking the client's customers **how they found them**, with "AI assistant"
  as an explicit option.

---

## How to apply it in the build

- At least one **direct-answer block** per key page: a real audience question,
  a self-contained one-paragraph answer at the top, a figure with source and date.
- Headings phrased as questions when it fits the intent (*"How long is recovery from
  spine surgery?"*).
- A table wherever there is a real comparison (options, criteria, price ranges, limits).
- Visible update date; year in the title when the content is seasonal or about price.
- Key copy and JSON-LD in the **raw HTML**, not injected by JS (see `ai-crawlers.md`).
- Schema aligned with that content, **with `sameAs` populated** to real, verified profiles.
- Author anchor where real material exists.
- robots.txt not blocking AI search bots (`ai-crawlers.md`); llms.txt optional as a
  courtesy (`llms-txt.md`); AI channel in GA4 and Bing Webmaster Tools (`analytics-ai.md`).

## What NOT to do

- **Don't promise position or ranking in any assistant.** They don't exist.
- **Don't confuse AEO with putting `FAQPage` back** hoping for a visual rich result: it died on
  2026-05-07. A visible FAQ does help answer; the schema is not the cause.
- **Don't "write for the robot"** or chunk the page into fragments. Clear passages get cited.
- **Don't sell llms.txt or schema as a citation lever** [M].
- **Don't fabricate the distinctive claim.** If the narrow, verifiable fact doesn't exist, it doesn't exist.
- **Don't buy mentions in "best of" lists** presented as editorial. Having a third party say it
  doesn't exempt you from advertising regulation if you paid for it, and in healthcare it's a violation.
- **Don't copy third-party reviews onto your site** to look more citable: Google prohibits adding
  other sites' ratings.
