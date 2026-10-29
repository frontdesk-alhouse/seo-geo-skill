# Citation measurement in AI assistants (manual protocol)

> How to measure whether a client appears in ChatGPT, Gemini, Google AIO/AI Mode, Claude or
> Perplexity, so that the series stays comparable over time. No API, no paid tool: a browser, a
> template and a calculation script.
> Templates: `templates/prompt-battery.template.md`, `templates/run.template.md`.
> Scripts: `scripts/indice_citacion.py`, `scripts/verificar_fuentes.py`.

**What this is and what it isn't.** N=3 on non-deterministic systems, run from a real account, is a
**signal that is comparable over time**, not a clean measurement. It is reported as a range, never
as a position.

---

## 1. The query battery

Written once per client, before the first run.

| Family | What it measures | Fictional example (medical: Dr. Elena Ruiz, spine surgery, Monterrey) |
|---|---|---|
| **F1** Unbranded, by need | Whether the client exists in the channel | "Who is the best spine surgeon in Monterrey?" |
| **F2** Unbranded, by decision | The question before buying | "I have a herniated disc, do I really need surgery?" · "How much does spine surgery cost in Monterrey?" |
| **F3** Branded | What it says about them and whether it confuses them | "Who is Dr. Elena Ruiz?" · "Dr. Elena Ruiz, where does she practice?" · namesake test |
| **F4** The third party searching on their behalf | Family member, partner, buying committee | "My dad has lumbar stenosis, who should he see in Monterrey?" |
| F5 optional, specific case | A condition or specific case | "Who operates on adult scoliosis in Monterrey?" |
| F6 optional, technique | A nameable technique or method | "Who does endoscopic spine surgery in Nuevo León?" |

Equivalents in other verticals: SaaS (Nimbus CRM): F1 "best CRM for sales teams in Mexico", F2
"HubSpot or a local CRM for 10 reps?", F4 "my boss wants a CRM, which one should I propose?". B2B
(Aceros del Bajío): F1 "industrial building manufacturers in the Bajío", F4 "the committee wants
three structural steel suppliers in León". Real estate (Inmobiliaria Cantera): F1 "trustworthy real
estate agencies in Querétaro", F2 "is buying pre-construction in Juriquilla worth it?".

**`query_type` tag** on every query: `informational`, `local` or `transactional`. The mix of
sources the assistant cites depends on the type (Yext vs Muck Rack, see `geo-evidence.md` 2.3), so
the census is read by type.

**Immutability rule.** The set **is not modified** between runs: not the wording, not the order, not
the accents. A new query is added at the end with its date added and the mark "no history". A query
that no longer works is marked retired, not deleted.

Typical size: 12-20 queries. Fewer gives no reading; more can't be sustained by hand.

## 2. Instrument

**The consumer UI is the official instrument.** The API is a declared complement (`origin: api`),
never a substitute. Reasons:

- SparkToro/Gumshoe (Jan-Mar 2026) ⚠️ measured in consumer UIs, which is what users see [E].
- `oneglanse` (MIT repo): "the API is not the product". API answers use a different search system,
  a different system prompt and a different search frequency; API citations are not the UI's
  (the suganthan.com Gemini guide reports this too).
- 8ight.AI (2026-10) measured via API and says so; that's why its Claude figures are treated as
  pending replication.

**Assistants to prioritize in Mexico.** StatCounter Mexico (Aug 2026): ChatGPT 75.1%, Gemini 16.7%
of chatbot use [E]. Order: ChatGPT, Gemini, Google AIO and AI Mode (from a browser, with a normal
search), Claude. **Perplexity is optional**: it requires an account and its weight in Mexico is low.

**Session mode per assistant:**

| Assistant | Mode | What to check |
|---|---|---|
| ChatGPT | Temporary chat | That the header shows the session is unpersonalized |
| Gemini | Temporary chat | That it doesn't cite the account's location ("your current city") |
| Claude | Incognito chat with web search on | That it searched (if not, `searched: false`) |
| Google AIO / AI Mode | Browser, private window | If AIO doesn't show, record `appears: false` with `notes: "no-trigger"` |
| Perplexity | Account, new session | Optional |

**Session gotchas that contaminate the measurement** (seen in a real round, 2026):

- **Claude's incognito does not turn off connectors.** If the account has Drive, Notion, ClickUp or others connected, Claude can answer the branded query from private data. Turn off every connector in the composer before the round, note it, and turn them back on when done. A run that cited a connector is set aside, not counted.
- **The account profile leaks anyway**: user memory or skills can make the assistant "know" the brand. A mention that treats the brand as the addressee ("your team at X") is not an appearance.
- **AI Mode personalizes with the Google account** just as Gemini does with location. Same treatment: flag it in `notes` and report it separately.
- **Gemini switches models when quota runs out** (Pro → Flash → Flash-Lite). Check the selector on every run and note the model; runs on another model are not comparable and get repeated.
- An assistant may ask permission to read a URL ("Allow once"); granting it is part of the real user's flow, but note it.

**Uncontrolled variable, always declared.** Runs come from a real account and a real IP. Location
leaks (an assistant can inject the account's city), and memory may not be fully off. Declare it in
the report; don't hide it.

**Operating gotchas:**

- ChatGPT accepts URL prefill: `https://chatgpt.com/?temporary-chat=true&q=<urlencoded query>`
  and then click send. It is more reliable than typing, because typing via automation fails with
  accents and characters like "ñ".
- Gemini and Claude: type the query; check that the accents survived.
- If you automate the browser, keep batches to **40 seconds or less** per step; a long batch times
  out and loses the run.
- N=3 means three new conversations, not three "regenerate".

## 3. What gets recorded per run

One file per run using `templates/run.template.md`. Frontmatter:

| Field | Content |
|---|---|
| `query` | Exact text, same as in the battery |
| `family` | F1 to F6 |
| `query_type` | informational, local, transactional |
| `assistant` | chatgpt, gemini, aio, ai-mode, claude, perplexity, copilot |
| `origin` | `ui` or `api` |
| `run` | 1, 2 or 3 |
| `date` | ISO with time |
| `mode` | Session mode used |
| `searched` | `true` if the assistant showed a search or sources; `false` if it answered from memory |
| `appears` | true, false (if AIO didn't trigger: false and `notes: "no-trigger"`) |
| `position` | The client's place in the list (empty if it doesn't appear) |
| `names` | Every proper name, in order |
| `cited_urls` | Every URL the assistant shows as a source |
| `stuck_claim` | Any data the assistant attaches to the client (figure, credential, address), correct or not |
| `notes` | Selection criteria the assistant states, errors, confusions |

Below the frontmatter go two sections: `## Query` (the exact text from the battery, not reworded)
and `## Verbatim` (the full answer, unedited). No verbatim, no audit.

## 4. Source verification (mandatory)

Tow Center (Mar 2025): more than 60% of answers with an incorrect citation and invented URLs [E].
Every cited URL is opened and classified: **live / dead / doesn't say what the assistant said**,
and **own / third party**.

`python3 scripts/verificar_fuentes.py runs/` does the first pass (HTTP status, whether the page
names the client; `--name "<client name>"` is required and can be repeated for variants). After that, human review of anything doubtful.

Known trap: a directory listing that returns 404 or 403 to the script and 200 in the browser **is
not down, it's an anti-bot block**. Always verify with a browser UA before reporting "dead".

## 5. Metrics

- **Citation Index** = runs where the client is named / total runs, per query × assistant. It is
  **always reported with a 95% Wilson interval**, never as a bare number. With N=3 per cell the
  interval is huge; that's why it is aggregated by family and by assistant.
- **Unbranded subtotal** (F1, F2, F4 and the optional ones). F3 is reported separately: showing up
  when you're named is not visibility.
- **First place**: runs where the client is the first name.
- **Trigger rate**: % of runs with `searched: true`, per assistant. It explains differences: an
  assistant that rarely searches answers from training.
- **Narrow vs broad reading**: separate narrow-category queries (technique, case, niche) from broad
  ones. Normally the client appears far more on the narrow ones; that contrast tells you where to
  invest.
- **Source census**: which URL holds up the client's name in each run, whether it's live, whether
  it's own or third party. Mentions without a supporting citation are common (25% in ChatGPT, 31%
  in AI Mode, TJ Robertson 2026-10 [E]); they are counted separately.
- **Stuck claim**: wrong data the assistant attaches to the client. It is a risk KPI: trace its
  source and fix it there.
- Sentiment is not scored. Note the criterion the assistant used to choose (for example, "how many
  procedures of that type they do per year") because it tells you what to publish.

`python3 scripts/indice_citacion.py runs/ --expected-n 3` produces the Markdown
table per query × assistant with intervals, subtotals, first place, trigger rate and source census.
F3 queries always count as branded; `--brand Q-NN` marks extra query ids as branded.

**No composite "GEO score".** There are no evidence-backed weights for combining these metrics.

## 6. Placebo control (optional)

From the `danishashko/geo-aeo-tracker` repo (MIT): for each family, a rewording of the same question
in other words, run the same way. If the rewording moves the index as much as the change you made
to the site, the change can't be attributed. Useful before reporting an improvement.

## 7. Cadence

| When | What |
|---|---|
| Baseline | Before touching anything |
| +30 and +60 days | After publishing changes |
| Afterwards | Quarterly |
| ChatGPT and AI Mode | Monthly at minimum: they rotate 74% and 56% of citations per week (Sistrix, Apr 2026 [E]) |
| AIO | Can go quarterly: stable on ~half of queries |

## 8. The measurement that's worth the most

Ask the client to ask **their own customers how they found them**, with "AI assistant or ChatGPT"
as an explicit option on the form, at reception or in the CRM. It's free and it's the only thing
that turns the channel into attributable data. Pew and Reuters show that clicks from AI are rare
(~1-4%), so the channel won't show up in analytics even when it's working.

## 9. How it's reported

- Index by assistant and by family with its interval: "ChatGPT, unbranded: 7 of 12 runs (58%,
  95% CI 32-81%)". Never "we're in 2nd place on ChatGPT".
- Comparison against the baseline, with the same battery.
- Source census: the 5-10 URLs that most hold up the client and its competitors.
- Stuck claims detected and their origin.
- Uncontrolled variable declared.
- Next action per finding: quick wins, this month, this quarter (see `report-template.md`).
