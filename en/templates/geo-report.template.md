## Visibility in AI assistants: {{MONTH YYYY}}

Cycle {{n}} · runs from {{YYYY-MM-DD}} to {{YYYY-MM-DD}} · {{N}} runs on {{assistants}} · compared against the cycle of {{YYYY-MM-DD}}.

The figures come from `scripts/indice_citacion.py` and `scripts/verificar_fuentes.py`; the method is in `references/citation-measurement.md`.

### What matters, in three lines

1. {{Where we stand: unbranded subtotal and its interval, in one sentence.}}
2. {{What changed against the previous cycle and whether the change falls outside the interval or not.}}
3. {{The highest-impact action for the coming month.}}

### Citation Index by query and assistant

Cells `k/n (positions)`: in how many of n runs you were named and in what place. The branded query goes separately.

| Query | Family | Type | ChatGPT | Gemini | Claude | AI Overviews | AI Mode | Total |
|---|---|---|---|---|---|---|---|---|
| Q-01 {{short text}} | F1 | local | {{2/3 (2, 3)}} | | | | | {{k/n · % [lo-hi %]}} |
| Q-02 {{short text}} | F2 | informational | | | | | | |
| Q-05 {{short text}} (branded) | F3 | informational | | | | | | |

**Unbranded subtotal**

| Assistant | Names you | First place | Searched the web (trigger rate) |
|---|---|---|---|
| ChatGPT | {{k/n · % [lo-hi %]}} | {{k/n}} | {{k/n}} |
| Gemini | | | |
| Claude | | | |
| Overall | | | |

The brackets hold the 95% Wilson interval. Two cycles whose intervals overlap don't show a real change, even if the percentage moves.

**Reading by query type (unbranded):** informational {{k/n}}, local {{k/n}}, transactional {{k/n}}. {{One sentence: where you win and where you don't.}}

### Source census

Which pages hold up what the assistants say about you and your competitors.

| URL | Runs that cite it | Names you? | Status | Own or third party | What it says about you |
|---|---|---|---|---|---|
| {{https://...}} | {{n}} | {{yes/no}} | {{live / dead / anti-bot block}} | {{own / third party}} | {{one-line summary, or "doesn't mention you"}} |

{{One sentence: which third-party source is most worth keeping alive and which one should be corrected or replaced.}}

### Stuck claims

Wrong or unpublished data that some assistant attaches to you. They are a reputation risk: trace them to their source and fix them at the origin.

| Claim or data | Query | Assistant | Runs | Likely source | Action |
|---|---|---|---|---|---|
| {{"more than N ..."}} | {{Q-05}} | {{chatgpt}} | {{1/3}} | {{directory profile}} | {{fix the profile; measure again}} |

### Changes against the previous cycle

| Metric | Previous cycle | This cycle | Outside the interval? |
|---|---|---|---|
| Unbranded, overall | | | {{yes/no}} |
| Unbranded, ChatGPT | | | |
| Unbranded, Gemini | | | |
| First place, overall | | | |
| Own sources cited | | | |
| Active stuck claims | | | |

{{What was published or changed between cycles: new pages, corrected profiles, reviews, mentions. Without claiming causation.}}

### Plan

**Quick wins (this week)**

- [ ] {{Concrete action, owner, date.}}
- [ ] {{Concrete action, owner, date.}}

**This month**

- [ ] {{Action, owner, date.}}

**This quarter**

- [ ] {{Action, owner, date.}}

Next measurement: {{YYYY-MM-DD}} (30 and 60 days after publishing changes; after that, quarterly).

### How to read these figures (method)

AI assistants don't have a fixed ranking: the same question asked twice returns different lists. That's why we don't report a position but a proportion: in how many of several runs you are named, with its confidence interval. We ran {{N}} runs per query and assistant with real sessions in temporary or incognito mode, from {{country}}; location and account are variables we don't control, so these figures are for comparing against our own previous measurements, not as absolute truth. The query set doesn't change between cycles. There is no way to guarantee that an assistant will cite you: what we can do is improve what sources say about you and measure whether that shows up. The indicator is mention and citation, not traffic: very few people click on the sources of an answer.
