# Examples

Fictional material for testing the scripts without touching real client data. Run every command from the skill root (the folder that contains `scripts/`). Requirement: Python 3.10 or later, no external dependencies.

The English installer writes `.lang` with `en` in the skill root, so the scripts print English without `--lang en`. If you run them from a clone of the repo instead of an install, add `--lang en` (or set `SEO_GEO_LANG=en`).

## What is here

- `sample-runs/`: 12 runs for a fictional client, Dr. Elena Ruiz (spine surgery, Monterrey), written with `templates/run.template.md`.
  - Q-01 (F1, local): 3 runs in ChatGPT and 3 in Gemini.
  - Q-02 (F2, informational): 3 runs in ChatGPT; one with `searched: false` (it answered without searching).
  - Q-03 (F3, branded): 3 runs in ChatGPT; one with a `stuck_claim`.
  - Competitors and URLs are made up and live on `example.com` and `example.org`.
- `sample-urls.txt`: 5 public, stable URLs (one forces a 404) for testing `verificar_fuentes.py`.

## How to run each script

**Citation Index** (no network):

```bash
python3 scripts/indice_citacion.py examples/sample-runs
python3 scripts/indice_citacion.py examples/sample-runs --json | python3 -m json.tool | head -40
```

What to expect: Q-01 at 4/6, Q-02 at 1/3, Q-03 (branded) reported separately at 3/3; unbranded subtotal 5/9 with a Wilson interval of [27-81 %]; ChatGPT trigger rate 8/9; one stuck claim; one warning because Gemini only ran Q-01.

**Source check** (network):

```bash
python3 scripts/verificar_fuentes.py examples/sample-urls.txt --name "Example"
python3 scripts/verificar_fuentes.py examples/sample-urls.txt --name "Example" --ua both
```

The URLs in `sample-runs/` are fictional: if you run the script on that folder, almost all of them come out `dead`, which is exactly what you would see with a URL an assistant made up.

**Raw HTML by bot, robots.txt and llms.txt** (network; use your own site or a client's with permission):

```bash
python3 scripts/check_html_crudo.py https://www.your-site.com --texts "key phrase from the hero" "{{CITY}}"
python3 scripts/check_html_crudo.py https://www.your-site.com --bots GPTBot,OAI-SearchBot --json
```

**Published metadata** (network):

```bash
python3 scripts/verificar_metadata.py https://www.your-site.com/sitemap.xml
python3 scripts/verificar_metadata.py https://www.your-site.com/contact
```

**llms.txt draft** (network):

```bash
python3 scripts/generar_llms_txt.py https://www.your-site.com/sitemap.xml --max 30
python3 scripts/generar_llms_txt.py your-site.com --sections "Services:/services,/pricing" "About:/about,/contact" --output llms-draft.txt
```

The draft comes out with `TODO` in the summary, the context and the Notes for language models. Curate it by hand, using `templates/llms.txt.template` as a guide, before publishing it.

## Output language

Every script takes `--lang es|en`. Without it, the language comes from the `SEO_GEO_LANG` environment variable, then from the `.lang` file in the skill root, then defaults to `es`. Spanish option names (`--marca`, `--n-esperado`, `--textos`, `--nombre`, `--secciones`, `--incluir-idiomas`, `--salida`) still work. With `--json`, keys stay in Spanish in both languages so that tooling built on them does not break; messages, warnings and labels follow the chosen language.

## Exit codes

| Script | 0 | 1 |
|---|---|---|
| `indice_citacion.py` | report generated | folder does not exist or no valid runs |
| `verificar_fuentes.py` | report generated | no URLs, file does not exist, or no URL responded |
| `check_html_crudo.py` | no ERROR findings | any ERROR (search bot blocked, key text missing, noindex) or site not responding |
| `verificar_metadata.py` | no ERROR issues | any ERROR (title or description missing, no h1, noindex, status other than 200) |
| `generar_llms_txt.py` | draft generated | sitemap unreadable or with no URLs |
