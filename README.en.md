# seo-geo (English summary)

A Claude Code skill for **technical SEO, schema and GEO** (visibility in AI assistants) on sites
built with Webflow, Framer or plain HTML. It generates JSON-LD, metadata, an AI-bot-aware
`robots.txt` and a draft `llms.txt`; runs a pre-launch gate; and **measures** whether a business
shows up in ChatGPT, Gemini, Claude, AI Overviews and AI Mode with a repeatable protocol.

The skill content is written in Spanish (Mexico). Script `--help` output is in English.

## What it does not promise

- **There is no "rank in ChatGPT".** Answers rarely repeat; we report the share of runs where
  the business is mentioned, as a range.
- **Schema does not earn citations.** It clarifies the entity and enables rich results; Ahrefs'
  May 2026 test found no citation lift.
- **llms.txt is not GEO.** No engine documents using it; ship it as a cheap courtesy.
- **The KPI is citation and mention, not traffic.** Click-through from AI summaries and chatbots
  sits around 1% to 4%.
- **Nothing is a switch.** The skill works on citable surface, entity consistency and honest
  measurement.

## Install

```bash
git clone https://github.com/frontdesk-alhouse/seo-geo-skill.git
cd seo-geo-skill
bash install.sh
```

Copies the folder to `~/.claude/skills/seo-geo/`, checks for `python3`, prints usage. Idempotent,
no downloads, no `curl | bash`.

## Use

```text
/seo-geo medical https://example.com            build and launch (steps 1 to 6)
/seo-geo saas https://example.com --solo-schema schema and metadata only
/seo-geo generic https://example.com --gate     pre-launch gate on a live site
/seo-geo real-estate https://example.com --medir citation measurement in AI assistants
```

## Scripts (Python 3, standard library only)

| Script | Purpose |
|---|---|
| `check_html_crudo.py` | Fetches a URL as each bot; checks key copy, JSON-LD, robots, llms.txt, sitemap in raw HTML |
| `verificar_metadata.py` | Title, meta, canonical and OG per page: lengths, duplicates, gaps |
| `generar_llms_txt.py` | Sitemap to a draft `llms.txt` for manual curation |
| `indice_citacion.py` | Run logs to a Citation Index with Wilson intervals and a source census |
| `verificar_fuentes.py` | Opens every cited URL: HTTP status and whether it names the business |

## Measurement in short

Fixed prompt battery by family (unbranded need, unbranded decision, branded, third party
searching on someone's behalf); three runs per prompt and assistant in the consumer UI; session
mode declared as an uncontrolled variable; every cited URL opened and verified; Citation Index
with a confidence interval, branded queries reported separately; repeat at 30 and 60 days, then
quarterly.

## Evidence

`references/geo-evidencia.md` tags every claim as [E] study, [O] official, [S] speculative or
[M] myth, with source and date: Princeton GEO (KDD 2024), Ahrefs schema test (May 2026),
TJ Robertson citation study (Oct 2026), SparkToro/Gumshoe (2026), Columbia Tow Center (Mar 2025),
Pew (Jul 2025), and more.

## Origin and credits

Built by [Alto House](https://altohouse.mx/), a brand management and positioning studio in
Guadalajara, Mexico, on anonymized client work from 2025 to 2026, and tested end to end on the
studio's own Framer site. No client names, URLs or real data in this repo. Concepts adapted from
`AgriciDaniel/claude-seo` and `zubair-trabzada/geo-seo-claude` (both MIT), with corrections
listed in the Spanish README.

## License

MIT. See [LICENSE](LICENSE).
