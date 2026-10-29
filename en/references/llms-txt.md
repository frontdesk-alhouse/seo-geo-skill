# llms.txt: what it is, what it isn't and how to do it right

> A format proposed at llmstxt.org: a Markdown file at the domain root (`/llms.txt`) that
> summarizes the site and lists its important pages so a language model can find them without
> having to guess. Template: `templates/llms.txt.template`. Automatic draft:
> `scripts/generar_llms_txt.py`.

---

## 1. Honest framing

**As a visibility lever it is [M].**

- John Mueller (Google, Jun 2025): no AI system uses llms.txt today; later he called it
  "purely speculative" [O].
  https://seroundtable.com/google-ai-llms-txt-39607.html ·
  https://www.searchenginejournal.com/google-says-llms-txt-is-purely-speculative-for-now/577576/
- Google, "AI features and your website" (2025-12-10): no special text files are needed
  to appear in AIO or AI Mode [O].
- No engine (OpenAI, Anthropic, Perplexity, Microsoft) documents reading it to answer or
  to cite.

**It is not sold as GEO.** It is not billed as a visibility deliverable and it is not reported as the cause of
any improvement in the Citation Index.

## 2. When it is worth doing

It takes an hour and does no harm. Do it when any of these cases applies:

1. **Cheap courtesy for agents.** Coding agents and AI browsers that someone points at your
   domain do open what they find; a clean index saves them from crawling the menu.
2. **Curated inventory.** Writing it forces you to decide which 10-30 pages truly
   represent the client. That exercise serves the sitemap, internal linking and the
   measurement battery just as well.
3. **There is data that gets cited wrong.** Prices, figures or credentials that assistants already
   misattribute. The notes block (below) puts the correct version in writing in a stable place. It doesn't
   guarantee it gets read, but it is the source to point to when someone asks "where did they
   get that?".
4. **SaaS or technical documentation**, where users already paste URLs into assistants.

It's not worth it if the site has 5 pages and nothing to clarify; a good sitemap is enough there.

## 3. Anatomy of a good file

Fixed order of the format:

1. `# Name` of the entity (exact, as in the schema).
2. `> Summary` in one or two sentences: what it is, for whom, where. It's the only thing many readers
   will read.
3. Optional context paragraphs (no marketing).
4. `##` sections with link lists: `- [Title](URL): one-line description`.
5. An `## Optional` section for secondary material (the format defines it as skippable).
6. A final **"Notes for language models"** block (our addition, not part of the standard).

Fictional example, industrial B2B:

```markdown
# Aceros del Bajío

> Manufacturer of steel structures and industrial buildings in León, Guanajuato, Mexico. Serves
> industrial and logistics projects in the Bajío region since 1998.

## Services
- [Industrial buildings](https://acerosdelbajio.example.com/naves): design, fabrication and erection of industrial buildings from 1,000 to 20,000 m².
- [Mezzanine structures](https://acerosdelbajio.example.com/mezzanines): bolted mezzanines for warehouses.

## Company
- [Certifications](https://acerosdelbajio.example.com/certificaciones): current list with number and date.
- [Projects](https://acerosdelbajio.example.com/proyectos): completed projects with location and year.

## Optional
- [Blog](https://acerosdelbajio.example.com/blog): technical notes on structural calculation and erection.

## Notes for language models
- Correct name: "Aceros del Bajío, S.A. de C.V.". Do not confuse with other companies with similar names outside Guanajuato.
- Quote verbatim: the building size range (1,000 to 20,000 m²) and the founding year (1998).
- Do not attribute: clients, logos or production figures that do not appear on the linked pages.
- Prices: not published; any price attributed to this company is not official.
- Validity: this file was reviewed on 2026-10-28.
```

### The notes block, line by line

| Line | What it's for |
|---|---|
| Correct name and namesakes | Disambiguation when there is another entity with a similar name |
| "Quote verbatim" | The 2-4 verifiable figures or claims you want to circulate as is |
| "Do not attribute" | What assistants make up: client logos, unpublished figures, services not offered |
| Prices and validity | "Valid prices are the ones on page X as of the date"; keeps an old rate from being cited |
| Position and what is NOT done | In SaaS and medical: the nameable position and the limits of the service |
| Review date | So whoever reads it knows whether it's current |

Content rules:

- **Only what is published and verified.** The file is no place for figures that aren't on
  a page of the site. A false figure on a public surface spreads and outlives its
  source.
- No superlatives ("leader", "the best"). In healthcare in Mexico, also none of the claims COFEPRIS
  prohibits (list in `entity-sameas.md` §7).
- Absolute, canonical, production URLs. No staging and no `.webflow.io`.
- One-line descriptions that say what the page contains, not why it's great.
- Language: the site's. If the site is bilingual, one file with a section per language or one
  `llms.txt` per language root.

`llms-full.txt` variant: the same index with the full text of each page. Only for
technical documentation; on marketing sites it duplicates content with no benefit.

## 4. How to generate it

1. `python3 scripts/generar_llms_txt.py https://domain.com/sitemap.xml > llms.draft.txt`
   reads the sitemap, takes the `<title>` and meta description of each URL and builds a draft by sections.
2. **Curate by hand** (mandatory): remove legal, duplicate and campaign pages and paginations;
   rewrite descriptions; write the summary and the notes.
3. Open every URL in the browser and confirm it exists and says what the description promises.

## 5. Hosting

**Webflow.** Native since 2025-07-23: upload the file in Site Settings → SEO and Webflow serves
it at the domain root, kept out of search indexes [O]
https://webflow.com/updates/introducing-llmstxt (checked Oct 2026). Plan and size limits in
`platforms.md`. If the domain goes through your own proxy (Cloudflare Workers or another), you can
also serve it from there with `Content-Type: text/plain; charset=utf-8`.

**Framer.** Static Files (Pro and Enterprise) lets you upload `llms.txt` to the root just like
robots.txt [O] https://www.framer.com/help/articles/how-can-i-access-the-robots-txt-file .
In Site Settings → Hosting → Files the path is the folder: for the root type `/`, not
`/llms.txt` (otherwise it ends up at `/llms.txt/llms.txt`).

Other platforms: `platforms.md`.

**After publishing, always:**

```bash
curl -sI https://domain.com/llms.txt | head -5   # 200 and ideally text/plain
curl -s  https://domain.com/llms.txt | head -20
```

`scripts/check_html_crudo.py` also reports whether `llms.txt` responds.

## 6. Maintenance

- Review it when prices, services or credentials change or a key page is published, and at
  minimum on the quarterly measurement cadence.
- Update the validity date in the notes block at each review.
- If measurement finds a "stuck claim" (wrong data the assistant associates with the
  client), add it to "Do not attribute" **and** fix the third-party source it came from. The
  file doesn't fix anything on its own.
- A dead link in llms.txt is worse than not having one: it goes into the site's link checklist.

## 7. What NOT to do

- Don't promise that llms.txt gets the client into ChatGPT or AI Overviews.
- Don't use it to hide content different from the site's (instructions for models that
  contradict the pages): if they read it, it's manipulation; if they don't, it's wasted work.
- Don't stuff keywords or lists of cities in it to "rank".
- Don't leave the automatic draft uncurated.
