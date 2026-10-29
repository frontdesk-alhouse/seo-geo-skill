# Entity and sameAs: making the assistant know all those profiles are one

> Entity consistency, `sameAs` by vertical (Mexican sources plus US equivalents), reviews and GBP as
> citation sources, and a third-party surface audit. Tags as in `geo-evidence.md`.

---

## 1. Why it matters

Assistants feed on what third parties say about the client, not just on its site. When the
surfaces don't match, two things happen, both seen while measuring real cases:

1. **The identity splits.** The person, their practice or company, and their site show up as
   separate entities the assistant never joins. Each one collects a fraction of the signal, and on
   the branded query the assistant mixes data or confuses the client with a namesake.
2. **A false figure spreads.** A claim the client wrote on a profile (case volume, years of
   experience, a certification) is repeated in runs across several assistants and **outlives its
   source**: it keeps showing up even after the profile is gone. You don't fix it by talking to the
   model; you fix the source, and even then it takes time.

Honest framing: consistency is **hygiene**, not what drives appearance. What makes you appear is a
narrow category and a distinctive claim; consistency makes what appears correct and durable [S,
reasonable mechanism without a direct test]. But if the assistant sends a patient to the wrong
hospital, the harm is real.

## 2. Consistency checklist

Fill in a table with one row per surface and one column per data point. Any difference is fixed on
the surface, not in the table.

| Data point | Rule |
|---|---|
| Exact name | One single form, identical on site, schema, GBP and directories. With or without "Dr." and second surname, but always the same |
| Registration | Medical: professional license and specialty license (Mexico: cédula profesional, SEP; US: NPI number and state medical license). Company: legal name and tax ID (Mexico: razón social and RFC) where applicable. Real estate: AMPI or state registration in Mexico, state real estate license in the US, if it exists |
| Education | Same institutions and years. A course is not a fellowship; don't inflate |
| Institutions | Current hospitals, clinics, chambers or associations. Remove the ones that no longer apply |
| NAP | Name, address and phone identical (see `local-seo.md`) |
| Category | The same primary category in GBP, directories and schema |
| Figures | Only verifiable figures, published on the site with a date |

**Hard rule:** no credential or figure goes onto a public surface without being verified. In
classic SEO you fix a mistake by editing the page; here it gets replicated.

## 3. sameAs by vertical

`sameAs` in the `Person` or `Organization` schema declares which profiles are the same entity. It
is the cheapest disambiguation, and critical when a namesake exists. List only profiles that are
**owned by or verified for the entity**, live, and say the same thing as the site.

| Vertical | Candidate surfaces (Mexico) | Equivalents (US / global) |
|---|---|---|
| **Medical** | Doctoralia, Topdoctors.mx, doktor.mx, profile on the specialty's certification council (see CONACEM), SEP professional license registry, rosters of the hospitals where they operate (the physician's page on the hospital site), specialty association or college, ORCID, Google Scholar (PubMed has no author profile: its articles are anchored via ORCID, not with a search URL), the practice's GBP, LinkedIn | NPI Registry, state medical board license lookup, Healthgrades, Zocdoc, hospital rosters, Google Business Profile, LinkedIn, ORCID, Google Scholar |
| **SaaS** | Company LinkedIn, Crunchbase, G2, Capterra, Product Hunt, the organization's GitHub, founders' profiles (as a separate `Person`) | Same set (these are global) |
| **B2B industrial** | LinkedIn, GBP for plant and offices, chambers (CANACINTRA, COPARMEX, the sector chamber), industrial directories for the sector and for industrial parks, supplier registrations on large customers' procurement portals when they are public | LinkedIn, Google Business Profile, BBB |
| **Real estate** | Portals where they list (agency profile, not individual listings), AMPI (local chapter), GBP, LinkedIn, Instagram if it is the real channel | Google Business Profile, LinkedIn, Yelp, BBB |

Notes by vertical:

- **Medical.** Medical Economics (2026-08-25, ChatGPT, US) found that hospital and academic rosters
  (27.5%) and board or association profiles (22.1%) are the sources ChatGPT cites most for
  physicians, and **zero citations to GBP URLs** [E, US]. Priority: make sure the hospital has a
  page for the physician with correct name, specialty and training. A real author anchor (ORCID,
  PubMed, Scholar) lasts longer than a commercial directory.
- **B2B industrial.** TJ Robertson (2026-10-25): 87% of citations in B2B industrial go to company
  sites [E]. The lever is the company's own site; directories are entity backup.
- **Real estate.** Local Falcon: portals and directories dominate, only 21.2% of top agents with a
  site were cited [E vendor, US]. The agency profile on portals matters as much as the site.
- **SaaS.** Semrush (Jan-Feb 2026): LinkedIn cited in 14.3% of ChatGPT Search answers [E]. G2 and
  Capterra come in on comparison queries.

**Wikidata only if the entity is notable** (independent press, publications, verifiable awards).
Creating an item for a practice or a small business without secondary sources is spam: it gets
deleted, and it leaves a trace.

**Every `sameAs` URL gets opened and must say the same thing.** Before publishing the schema and on
every quarterly run. A `sameAs` pointing to a dead or contradictory profile makes the entity worse.
Never guess a URL (see `saas.jsonld.md`).

## 4. Reviews as a source

- 8ight.AI (2026-10-05, APIs with search): businesses with fewer than 25 reviews were named in 3.4%
  of answers, versus 22.2% for those with 1,000 or more; **star rating didn't matter** [E, pending
  replication].
- In subscription medical directories, ordering is driven by the **pace of new reviews**, not the
  star average (our own observation, [S]).
- Takeaway: what counts is **count and pace**, not the rating. The plan is to ask for a review
  systematically after every service, on the surface the vertical uses.

## 5. Google Business Profile as a citation source

| Study | Finding | For whom |
|---|---|---|
| SE Ranking, Feb 2026 | 36% of AI Mode citations point to GBP [E] | Local on Google |
| BrightLocal, 2026-08-26 | GBP is the main source for Google's AIs (~28.6%) [E] | Local on Google |
| Medical Economics, 2026-08-25 | 0 citations to GBP in ChatGPT for physicians [E] | Physicians on ChatGPT |

Takeaway: audit GBP as a citation source for AIO and AI Mode (category, description, services,
hours, photos, review replies), but don't sell it as the lever for ChatGPT in healthcare. There,
rosters, boards and the client's own site with detailed pages carry the weight.

## 6. Third-party surface audit

Once per client at the start, and then with the source census of every measurement
(`citation-measurement.md`).

1. Search the exact name and variants on Google, Bing and inside the vertical's directories.
2. List every surface: URL, owner (own, managed, third party), status (live, dead, anti-bot
   block), date of last edit if visible.
3. Compare against the checklist in section 2.
4. Cross-check with the source census: which surfaces do the assistants actually cite? Those go
   first.
5. Plan: fix the live ones that get cited, claim the ones that can be claimed, request removal or
   correction of the ones with false data, and redirect (301) the client's old domains or pages to
   the canonical URL.

Status check: with a browser, not just a script. A 404 or 403 with a bot UA may be an anti-bot
block. And a surface that holds the client up today can disappear within weeks; that's why it is
audited every cycle.

Planning: **a live, correct third-party surface is worth more, and sooner, than a site that doesn't
exist yet.** Fixing a directory profile can pay off while the site is being built.

## 7. What NOT to do

- **Don't buy mentions in "best of" lists** presented as editorial. If you paid for it, advertising
  regulation applies all the same, and in healthcare it is a violation.
- **Don't copy third-party reviews** onto the site or mark them up in schema: Google prohibits
  aggregating ratings from other sites.
- **Healthcare (COFEPRIS, Mexico):** profiles, bios and directory descriptions must not carry the
  prohibited claims ("the most advanced technique", "shorter recovery time", "guaranteed results",
  "the safest surgery", "the best treatment", "risk-free"). What is repeated in a directory gets
  repeated in the assistant.
- Don't create duplicate profiles to "have more presence": they split the entity.
- Don't fill profiles with figures that aren't published and backed up on the site.
- Don't put in `sameAs` profiles of another person, the clinic when the `Person` is the physician,
  or search pages.
