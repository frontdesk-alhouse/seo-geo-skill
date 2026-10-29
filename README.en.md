# seo-geo

A Claude Code skill for **technical SEO, schema and GEO** (visibility in AI assistants) on sites
built on any platform; detailed guides for WordPress, Shopify, Squarespace, Wix, Webflow, Framer, code frameworks and plain HTML. It generates the JSON-LD, the metadata, an AI-bot-aware
`robots.txt` and a draft `llms.txt`; runs a launch gate; and **measures** whether a business shows
up in ChatGPT, Gemini, Claude, AI Overviews and AI Mode, with a repeatable protocol.

Full English and Spanish editions: you pick the language at install time.
[Versión en español](README.md) · Made by [Alto House](https://altohouse.mx/), a brand management
and positioning studio in Guadalajara, Mexico.

## Who it is for

- Studios, freelancers and in-house teams who ship sites on any platform (WordPress, Shopify,
  Squarespace, Wix, Webflow, Framer, code frameworks or plain HTML) and want an SEO + schema + GEO
  layer that does not depend on paid tools.
- Teams that want to measure citation in AI assistants without paying for an enterprise platform.
- Businesses in verticals where the entity matters: doctors and clinics, B2B SaaS, industrial,
  real estate, physical catalogs.

## What it does not promise

- **There is no "rank in ChatGPT".** Answers rarely repeat; we report the share of runs where the
  business is mentioned, as a range.
- **Schema does not earn citations.** It clarifies the entity and enables rich results; Ahrefs'
  May 2026 test found no citation lift.
- **llms.txt is not GEO.** No engine documents using it; ship it as a cheap courtesy.
- **The KPI is citation and mention, not traffic.** Click-through from AI summaries and chatbots
  sits around 1% to 4%.
- **Nothing is a switch.** No lever guarantees an appearance; the skill works on citable surface,
  entity consistency and honest measurement.

## Install

```bash
git clone https://github.com/frontdesk-alhouse/seo-geo-skill.git
cd seo-geo-skill
bash install.sh --lang en      # English edition
# bash install.sh              # Spanish edition (default)
```

`install.sh` copies the chosen edition to `~/.claude/skills/seo-geo/`, checks for `python3` and
prints usage. Idempotent, no downloads, no `curl | bash`. Run it again with the other `--lang` to
switch editions.

## Use

```text
/seo-geo medical https://example.com               build and launch (steps 1 to 6)
/seo-geo saas https://example.com --schema-only    schema and metadata
/seo-geo generic https://example.com --gate        launch gate on a live site
/seo-geo real-estate https://example.com --measure citation measurement in AI assistants
```

Verticals: `medical`, `saas`, `product`, `real-estate`, `generic`.

## File map (English edition, as installed)

| Path | Contents |
|---|---|
| `SKILL.md` | The 7-step flow and the skill's rules |
| `references/seo-core.md` | Technical SEO baseline, page type to schema, formulas, severity |
| `references/*.jsonld.md` | Baseline and per-vertical templates |
| `references/metadata-og.md` · `local-seo.md` · `backlinks.md` | Metadata, local SEO, links |
| `references/geo-evidence.md` | GEO evidence, tagged and dated |
| `references/geo-aeo.md` | On-page levers |
| `references/ai-crawlers.md` · `llms-txt.md` | AI bots, robots.txt, Cloudflare, llms.txt |
| `references/entity-sameas.md` | Entity consistency and `sameAs` |
| `references/citation-measurement.md` · `analytics-ai.md` | Measurement protocol and analytics |
| `references/report-template.md` | Client report |
| `references/platforms.md` | Where each piece goes per platform: WordPress, Shopify, Squarespace, Wix, Webflow, Framer, frameworks and plain HTML |
| `launch-checklist.md` | Launch gate for any platform, with GEO gate and Webflow and Framer notes |
| `templates/` | Prompt battery, run log, GEO report, `llms.txt`, two `robots.txt` |
| `scripts/` | Python utilities (shared by both editions) |
| `examples/` | Fictional runs to try the scripts |

In this repo the Spanish edition sits at the root and the English one under `en/`; `scripts/` is
shared.

## Scripts

Python 3, **standard library only** (no `pip install`). All have `--help`. Output follows the
installed edition; override with `--lang en|es`.

| Script | What it does |
|---|---|
| `check_html_crudo.py` | Fetches a URL as each bot and checks key copy, JSON-LD, robots, llms.txt and sitemap in the raw HTML |
| `verificar_metadata.py` | Title, meta, canonical and OG per page: lengths, duplicates, gaps |
| `generar_llms_txt.py` | Sitemap to a draft `llms.txt` for manual curation |
| `indice_citacion.py` | Run logs to a Citation Index with Wilson intervals and a source census |
| `verificar_fuentes.py` | Opens every cited URL: HTTP status and whether it really names the business |

Script file names stay in Spanish so both editions share one codebase.

## Measurement method

1. A fixed prompt battery in families: unbranded by need, unbranded by decision, branded, and a
   third party searching on someone's behalf.
2. The set does not change between rounds; new queries are appended with a date.
3. Three runs per query and assistant, in the consumer interface, not the API.
4. The session (temporary chat, incognito, signed in) is declared as an uncontrolled variable.
5. Each run is saved with its text, names in order, cited URLs and whether the assistant searched.
6. Citation Index = runs with a mention / total runs, with an interval; branded queries apart.
7. Every cited URL is opened: many are dead or do not say what the assistant claimed.
8. Repeat at 30 and 60 days after shipping changes, then quarterly; read the trend.

## Evidence

The whole skill rests on `references/geo-evidence.md`, where every claim carries a tag ([E] study,
[O] official, [S] speculative, [M] myth) plus source and date. Key studies:

- Princeton, Aggarwal et al., "GEO: Generative Engine Optimization", KDD 2024.
- Ahrefs, schema and AI citations test, May 2026.
- TJ Robertson / TJ Digital, citation study across ChatGPT, AI Mode and AI Overviews, October 2026.
- SparkToro / Gumshoe, repeatability of recommendation lists in assistants, 2026.
- Columbia Tow Center (CJR), citation accuracy in AI search, March 2025.
- Pew Research Center, clicks with Google AI summaries, July 2025.

## Where it comes from

[Alto House](https://altohouse.mx/), a studio in Guadalajara, Mexico, developed the method on real
client work from 2025 to 2026: medical sites, B2B SaaS, industrial and real estate. The cases are
anonymized: the repo holds no client names, URLs, figures or real transcripts. The runs in
`examples/` are fictional. The skill was tested end to end on the studio's own Framer site: gate,
round 0 of measurement and applied changes.

## Credits

- [`AgriciDaniel/claude-seo`](https://github.com/AgriciDaniel/claude-seo) (MIT): structure for the
  backlink audit, local SEO, client report and the first GEO/AEO framing. Rewritten and adjusted to
  the 2026 evidence.
- [`zubair-trabzada/geo-seo-claude`](https://github.com/zubair-trabzada/geo-seo-claude) (MIT): bot
  tiers and Content-Signals, Cloudflare-managed robots detection, the raw HTML vs DOM check, the
  `llms.txt` generator logic, the `sameAs` strategy and the quick wins / month / quarter format.
  **Corrected:** GPTBot does not feed ChatGPT Search (that is OAI-SearchBot); `anthropic-ai` is a
  retired token; Claude-SearchBot, Claude-User and Perplexity-User were missing; the "134-167
  words" rule is not in the Princeton paper; composite weights, unsourced figures and the
  `curl | bash` installer were removed.

## Compared with `Auriti-Labs/geo-optimizer-skill`

The closest project, and worth knowing. What this one does differently:

- Spanish and the LatAm market first, with an English edition, and entity sources per vertical
  for Mexico and the US.
- Measures in each assistant's **consumer interface**, at no API cost; the API is a declared
  complement.
- Evidence tagged and dated; no figure without a source.
- Works on any platform; detailed guides for WordPress, Shopify, Squarespace, Wix, Webflow, Framer, code frameworks and plain HTML.

## License

MIT. See [LICENSE](LICENSE).

## Contributing

- **Studies:** open a PR to `references/geo-evidencia.md` and `en/references/geo-evidence.md` with
  source, URL, date, sample size and tag. Mark it with ⚠️ if it came through secondary coverage.
- **Sample runs:** add fictional runs to `examples/` (or `en/examples/`) using the run template;
  never real client data.
- **Verticals:** new JSON-LD templates validated on validator.schema.org.
- Scripts stay free of external dependencies.
