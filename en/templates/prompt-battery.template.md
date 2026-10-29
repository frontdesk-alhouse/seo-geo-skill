# Prompt battery: {{NAME}}

Template for measuring whether AI assistants name a business when someone asks about what it sells, both without mentioning it and mentioning it. Full method, the rationale for N and cadence: `references/citation-measurement.md`. Bots and search: `references/ai-crawlers.md`.

- Client: {{NAME}}
- Service or category: {{SERVICE}}
- City or market: {{CITY}} (e.g., Columbus, Ohio)
- Vertical: {{medical | SaaS | B2B industrial | real estate | other}}
- Date the set was created: {{YYYY-MM-DD}}
- Person responsible for the runs: {{person}}

## Protocol

| Aspect | Rule |
|---|---|
| Assistants | ChatGPT and Gemini always. Claude recommended. Google AI Overviews and AI Mode in the browser when the query triggers them. Perplexity and Copilot optional (Perplexity requires an account). Each assistant is reported separately: they are not averaged together. |
| N | 3 runs per query and assistant, within the same date window. Answers don't repeat between runs; that's why a single one is never reported. |
| Session | ChatGPT: temporary chat, with "Unpersonalized" visible in the header. Gemini: temporary chat. Claude: incognito with web search on. AI Overviews and AI Mode: private window. Record the exact mode in every run (`mode`). |
| Language | The language and variant the person would actually write in (for a US market, US English). Don't fix typos if the battery includes them on purpose. |
| What gets recorded | One file per run using `templates/run.template.md`: full verbatim, order of names, the client's position, cited URLs, whether it searched the web, stuck claims attached to the name, mode, date and notes. |
| Verification | Every cited URL is opened with `scripts/verificar_fuentes.py` and, if it comes back `bloqueo-anti-bot` (anti-bot block), in a real browser. A source can be dead or not say what the assistant said. |

**Immutability rule.** The set is not modified between runs: no rewording, no fixing accents or spelling, no removing queries that "come out badly". A new query is added at the end with a new id, its date added and the mark "no history" until it has two cycles. A retired query keeps its id and is marked "retired (date)"; its id is never reused.

**Uncontrolled variable (declare it in every report).** Runs are done with real sessions, from a specific country and IP. Even when the mode is temporary or incognito, the assistant can use your approximate location (typical example: "based on your current location..."). N=3 on non-deterministic systems is a signal that is comparable over time, not a clean measurement.

**Query type.** Each query is tagged once as `informational` (wants to understand), `local` (looking for someone in a place) or `transactional` (wants to buy, get a quote or book). The mix of sources assistants cite changes with the type, so the index is also read by type.

## Families

| Family | What it measures | Required |
|---|---|---|
| F1 | Unbranded, by need or condition: do they name you when someone looks for what you do? | Yes |
| F2 | Unbranded, by decision: do you show up while the person is still deciding whether they need it or how much it costs? | Yes |
| F3 | Branded: does the assistant know who you are, without confusing you? Includes the namesake test. Reported separately, never added to the unbranded subtotal. | Yes |
| F4 | The third party searching on their behalf: family member, boss, purchasing department. | Yes |
| F5 | Specific case: a narrow condition, problem or scenario where the client is strong. | Optional |
| F6 | Technique, method or product with a proper name. | Optional |

How many: 2 to 4 queries per required family and 1 to 3 per optional one. More queries don't make up for fewer runs.

## Examples by vertical (fictional, to adapt)

Replace the placeholders. Don't copy examples from another vertical without rewriting them in the audience's real language.

### F1: unbranded, by need or condition

| Vertical | Query | query_type |
|---|---|---|
| Medical | Who is the best {{SERVICE}} in {{CITY}}? | local |
| Medical | My lower back has hurt for months and the pain goes down my leg, what kind of specialist should I see in {{CITY}}? | local |
| SaaS | Which {{SERVICE}} would you recommend for a 50-person company in the US? | transactional |
| SaaS | I need to stop running payroll in Excel, what tools are out there? | informational |
| B2B industrial | What {{SERVICE}} suppliers are there in {{CITY}}? | local |
| B2B industrial | I need a {{SERVICE}} manufacturer certified for the automotive industry in the Midwest | transactional |
| Real estate | What {{SERVICE}} developments are there in {{CITY}}? | local |
| Real estate | I'm looking for a two-bedroom apartment close to work in {{CITY}}, which area makes sense? | local |

### F2: unbranded, by decision

| Vertical | Query | query_type |
|---|---|---|
| Medical | I have a herniated disc, do I really need surgery? | informational |
| Medical | How much does {{SERVICE}} surgery cost in {{CITY}}? | transactional |
| Medical | How do I know if a surgeon is board certified? | informational |
| SaaS | Is it worth paying for a {{SERVICE}} or should I just use spreadsheets? | informational |
| SaaS | How much does a {{SERVICE}} cost for a small business? | transactional |
| B2B industrial | What should I ask a {{SERVICE}} supplier for before onboarding them as a vendor? | informational |
| B2B industrial | Should I import {{SERVICE}} or buy from a domestic manufacturer? | informational |
| Real estate | Is it better to buy pre-construction or a finished apartment in {{CITY}}? | informational |
| Real estate | What's the price per square foot in {{CITY}} this year? | transactional |

### F3: branded (includes the namesake test)

| Vertical | Query | query_type |
|---|---|---|
| All | Who is {{NAME}}? (no city or context: namesake test, does it confuse you with another person or company with the same name?) | informational |
| All | {{NAME}} {{CITY}}, what are the reviews like? | informational |
| Medical | Where does {{NAME}} practice and how do I book an appointment? | transactional |
| SaaS | What does {{NAME}} do and how is it different from the alternatives? | informational |
| B2B industrial | Does {{NAME}} have certifications and which industries does it supply? | informational |
| Real estate | Is {{NAME}} a reliable developer? Has it delivered on time? | informational |

When recording F3: if the assistant mixes in data from a namesake, note it in `notes` and put any false data in `stuck_claim`.

### F4: the third party searching on their behalf

| Vertical | Query | query_type |
|---|---|---|
| Medical | My dad has lumbar stenosis, who should I take him to in {{CITY}}? | local |
| Medical | How do I choose a good {{SERVICE}} for my mom? | informational |
| SaaS | My boss asked me to compare {{SERVICE}} options, which ones should I look at? | transactional |
| SaaS | I'm an outside accountant for several small businesses, which {{SERVICE}} should I recommend to them? | transactional |
| B2B industrial | Purchasing asked me for three quotes on {{SERVICE}} in {{CITY}}, who should I ask? | transactional |
| B2B industrial | I'm a plant engineer, which {{SERVICE}} supplier responds fast when the line goes down? | local |
| Real estate | My parents want to buy a place to retire in {{CITY}}, which developments are good? | local |
| Real estate | I'm relocating to {{CITY}} for work, which area should I look in and who should I work with? | local |

### F5 (optional): specific case

| Vertical | Query | query_type |
|---|---|---|
| Medical | I had spine surgery two years ago and the pain came back, who does revision surgery in {{CITY}}? | local |
| Medical | I have adult scoliosis, who treats it in {{CITY}}? | local |
| SaaS | Which {{SERVICE}} handles employees in several states with different benefits well? | transactional |
| SaaS | Is there a {{SERVICE}} that integrates with my accounting software without any coding? | informational |
| B2B industrial | Who manufactures high-temperature {{SERVICE}} in the US? | transactional |
| B2B industrial | Who services European-brand {{SERVICE}} in {{CITY}}? | local |
| Real estate | Which developments in {{CITY}} accept FHA loans? | transactional |
| Real estate | Where can I find apartments that allow large pets in {{CITY}}? | local |

### F6 (optional): technique, method or product with a proper name

| Vertical | Query | query_type |
|---|---|---|
| Medical | Who does endoscopic spine surgery in {{CITY}}? | local |
| Medical | What is minimally invasive lumbar fusion and who does it in the US? | informational |
| SaaS | What is {{PRODUCT'S OWN TERM}} and which tools do it? | informational |
| SaaS | Which {{SERVICE}} has automatic bank reconciliation? | transactional |
| B2B industrial | Who in the US does {{PROCESS}} coating for {{MATERIAL}} parts? | transactional |
| B2B industrial | What's the difference between {{PROCESS A}} and {{PROCESS B}} and who offers them in {{CITY}}? | informational |
| Real estate | Which developments in {{CITY}} have a green building certification? | local |
| Real estate | What is fractional ownership and who offers it in {{CITY}}? | informational |

## Client set (immutable)

| id | family | query_type | query | added | status |
|---|---|---|---|---|---|
| Q-01 | F1 | | | {{YYYY-MM-DD}} | active |
| Q-02 | F1 | | | {{YYYY-MM-DD}} | active |
| Q-03 | F2 | | | {{YYYY-MM-DD}} | active |
| Q-04 | F2 | | | {{YYYY-MM-DD}} | active |
| Q-05 | F3 | | Who is {{NAME}}? | {{YYYY-MM-DD}} | active |
| Q-06 | F3 | | | {{YYYY-MM-DD}} | active |
| Q-07 | F4 | | | {{YYYY-MM-DD}} | active |
| Q-08 | F4 | | | {{YYYY-MM-DD}} | active |

Statuses: `active`, `no history (added YYYY-MM-DD)`, `retired (YYYY-MM-DD)`.

## Run log

One row per run. The detail lives in the run file; this table is the index so none gets lost.

| Date | id | Assistant | Run | Mode | Searched | Appears | Position | File | Incidents |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

Suggested file name: `Q-01_chatgpt_r1.md`. When the cycle closes: `python3 scripts/indice_citacion.py <folder> --expected-n 3`.

## Execution gotchas

- **URL prefill in ChatGPT.** Open `https://chatgpt.com/?temporary-chat=true&q=<urlencoded query>` and click send. Typing with browser automation (`type`) fails with accents and special characters. In Gemini and Claude, type or paste.
- **Short batches.** If you automate with a browser extension, keep each batch of actions to 40 seconds or less. A batch that times out loses the run silently: confirm the file was written before moving to the next one.
- **Check the mode before sending.** If you don't see "temporary chat" or "Unpersonalized", the run doesn't count: repeat it and log the incident.
- **Location.** If the answer mentions your location ("near you", "in your city"), note it in `notes`: that's the uncontrolled variable in action.
- **One tab at a time.** Some interfaces don't generate the answer if the tab is hidden; work with the tab visible.
- **Don't reword by hand.** If a query looks badly written, it stays that way this cycle and the new version goes in at the end with a new id.
