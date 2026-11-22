# Search Console audit (`--audit` mode)

> For a site that is already live and has data: which pages are losing clicks, which are one push
> away from page 1, where two URLs fight over the same query and how much the site depends on its
> brand. Every finding comes tied to a page and an action.
> Script: `scripts/auditoria_gsc.py`. Finding format and severity: `seo-core.md` §6 and §7.

**Requirement.** A verified Search Console property with at least 3 months of data. With less, the
CTR curve does not have enough rows and the period comparison says nothing.

---

## 1. Export

In Search Console: **Performance → Search results**, search type **Web** (AI Overviews and AI
Mode traffic counts there too, Google 2025-12-10 [O]).

| What | How |
|---|---|
| Current period | Date: last 3 months (or a fixed range). **Export → Download CSV**. The zip holds several tables; use `Queries.csv` and `Pages.csv` (`Consultas.csv` and `Páginas.csv` if the interface is in Spanish) |
| Previous period | Same length, right before, or the same period last year if there is seasonality. Export it **separately**, not in "Compare" mode: the script reads one period per folder |
| Query × page | The interface does not export both dimensions together. Options: the Search Analytics API with dimensions `query` and `page`, a spreadsheet connector, or Looker Studio with a page and query table, exported to CSV with query, page, clicks, impressions, CTR and position columns. Without this view there is no cannibalization analysis |

Notes on the data:
- The interface exports a limited number of rows per table; for large sites, use the API.
- Search Console omits anonymized queries: the sum of clicks by query stays below the total by
  page. That is normal; don't try to reconcile it.
- The script accepts Spanish or English headers, CTR with `%` and decimal comma, and comma,
  semicolon or tab separators.

```bash
python3 scripts/auditoria_gsc.py export-current/ --previous-period export-previous/ \
    --brand "elena ruiz" "dra ruiz" --min-impressions 50 --lang en
```

`--brand` takes the brand terms (accents and case don't matter). Without them, the curve and the
cannibalization check mix in branded queries, which have very high CTR, and analysis (f) does not
run.

## 2. Expected CTR comes from the site itself

The fixed "expected CTR by position" tables that circulate (position 1 near 28%, and so on) predate
AI Overviews and do not work as a yardstick. Organic CTR on queries with AIO fell 61% since
mid-2024 (Seer Interactive, Sep 2025 [E] ⚠️); with an AI summary, clicks on a regular result drop
from 15% to 8% (Pew, 2025-07-22 [E]). See `geo-evidence.md` 2.5 and §1.

That is why the script computes the **site's own curve**: median CTR per position band (1, 2, 3,
4-5, 6-10, 11-20, 21+), only with unbranded queries and with at least `--min-impressions`. A band
with fewer than 3 rows has no curve and is not used. The curve compares the site against itself:
if the whole SERP lost CTR, that is not a finding about the page.

## 3. The six analyses

| | Analysis | Script rule | Typical action |
|---|---|---|---|
| a | **Low CTR for its position** | Position 1 to 10, CTR below 70% of its band's median. Clicks at stake = impressions × (median − CTR) | Rewrite title and meta description; check whether the SERP shows an AI Overview (if it does, the path is making the page citable, `geo-aeo.md`) |
| b | **Striking distance** | Position 5 to 20 with impressions. Clicks at stake estimated against the median of band 3 | 5-10: direct answer up front, a table or own data, internal links. 11-20: content refresh and internal links from strong pages |
| c | **Loss between periods** | Same page (or query) down 5 clicks or more | Diagnosis: lost 2 positions or more → content; same position and CTR −20% or more → snippet or SERP; same position and impressions −20% → demand, leave the page alone |
| d | **Cannibalization** | Unbranded query where 2 or more URLs have at least 15% of its impressions | The URL with the most clicks keeps the query; the others are consolidated with a 301 or rewritten for another intent (`seo-core.md` §5) |
| e | **Dead pages** | Had 5 clicks or more in the previous period and now zero | Open the URL: 404 or `noindex` → restore or redirect; alive → find which page took the query (back to d) |
| f | **Branded and unbranded** | Share of unbranded clicks | Rough threshold: >60% healthy, 40-60% medium, <40% brand-dependent. Dependent: the work is content for unbranded queries, not more schema |

The threshold in (f) is a rule of thumb to read the site, not a published standard: do not present
it to the client as a benchmark.

The **executive summary** picks action number one: the finding from a, b, c or e with the most
clicks at stake. It is an estimate made with the site's own curve, not a traffic promise.

## 4. From output to report

- Each row becomes a finding in the `seo-core.md` §7 format: severity, page, evidence (the table's
  figures), action and owner.
- Cannibalization and dead pages are **medium** severity unless they hit a money page; a position
  loss on a main service page is **high**.
- Report 10 actions at most; the rest goes in the appendix.
- Queries from (b) phrased as questions are also candidates for the measurement battery
  (`citation-measurement.md`), as new queries at the end of the set.

## 5. Limits

- Search Console gives averages per row: a position of 7.8 can be 3 on mobile and 12 on desktop.
- A CTR drop at a stable position can be a new AI Overview on the SERP: open the query in a private
  window before rewriting anything.
- The script's thresholds are constants at the top of `auditoria_gsc.py`; if you change them, say
  so in the report.
