# Asset-led links: earning mentions with something made by hand

> How to get a third-party page to name or link to the client without buying anything: bring the
> editor something that improves their page and would cost them work to make. Few sends, each with
> a real asset. The list of who to write to comes from step 8 (`citation-census-to-action.md`).

**Framing.** A link or a mention on a page the assistants already cite is a live third-party
surface, the Tier 2-3 lever in `geo-evidence.md` §7. Brand mentions correlate with AIO visibility
more than backlinks do (0.664 against 0.218, Ahrefs 2025-05-26 [E]): a mention without a link
counts as a result. None of this is a switch; it is measured in the next cycle.

---

## Common rules (they apply to all three methods)

1. **No claim about someone else's page without verifying it.** All three methods work by telling
   the editor something about their own content. Their first move is to check it; one mistake and
   the client looks like spam. Whatever could not be confirmed against a primary source leaves the
   list; it is not softened with "it seems".
2. **Few, worked sends.** 5 to 20 per cycle, each with its asset. The method stops working at
   volume because what convinces is that it is obviously handmade. If asked to scale it to
   hundreds, say no.
3. **The client sends.** The agent prepares the asset and the draft; the client sends it from
   their own email, under their own name. Never claim something was sent.
4. **No payment and no exchanges.** No money, no "I'll link to you if you link to me". Excessive
   link exchanges and partner pages made only to cross-link are link spam according to Google
   ("Spam policies for Google web search", checked 2026-11-22 [O]).
5. **Honesty about the replacement.** If the client is not the best alternative for a slot, say
   who is. An editor who catches you overselling once won't open the next email.

## The list generator: step 8

`scripts/objetivos_terceros.py` ranks the pages the assistants cite when the client is missing.
Each curated row gets one of the methods below depending on what the page is:

| The page is | Method |
|---|---|
| A list or comparison that includes someone who no longer exists or changed business | Tombstone |
| A guide or article with figures, prices, dates or "currently" | Correction sheet |
| A long guide describing a process, a comparison or a hierarchy without a diagram | Missing visual |
| A directory or profile in the vertical | Create or fix the profile (`entity-sameas.md`) |

## 1. Correction sheet (Fact Decay)

Idea: review a good page that went stale and give the editor a dated sheet of what is no longer
true, each item with its primary source.

1. Pick pages that matter: the ones from step 8 or the ones ranking for money queries.
2. Pull out every checkable claim: figures, prices, dates, names, "the latest", "today".
3. Verify each one against the **primary source** (the maker's pricing page, the original study,
   the announcement, the official rule). Not against another blog.
4. Classify: still true, changed, superseded, could not verify. The unverified is marked as such
   and is not sent as a correction.
5. Build the sheet: claim, status, source with URL, replacement sentence written in the page's
   voice so it can be pasted.
6. **First email without asking for a link.** The sheet is the whole message. The link comes when
   the corrected sentence needs a source and the client is that source, or on the second exchange.

Deliverable: one sheet per page, dated, each row sourced. Email skeleton: which page, how many
facts changed, two concrete examples, the sheet attached, no ask.

Real cost: verification is human work. Being fast here is worth nothing; being wrong is expensive.

## 2. Tombstone

Idea: "best of" lists and comparisons that still recommend a product or firm that closed, merged
or left the segment. The URL resolves fine, so no broken-link tool flags it.

1. A death list in the client's category: shutdown notices, acquisitions, discontinued products,
   pricing that moved to "contact sales", segment changes.
2. **A receipt for each one:** notice URL, date, screenshot. No receipt, no email.
3. Find who still lists it: the step 8 census first (a dead entry on a page the assistants cite is
   worth more than any other); then a search of the name with list patterns.
4. Per page: which entry went stale, the receipt, and replacement text for that slot written in
   the page's voice. If the closest alternative is not the client, say which one it is.

Deliverable per page: URL, stale entry, receipt, replacement text and verified contact. Email
skeleton: which entry, since when and with what proof, and the paste-ready text.

## 3. Missing visual

Idea: a page that already ranks describes a process, a comparison or a timeline in prose and has
no diagram at all. Make that diagram **from its own text**.

1. Candidates: pages that rank or that step 8 found, with zero or one image in the body.
2. Check that the prose has a shape: numbered steps, comparable options, dates, a hierarchy or a
   set of figures. If it doesn't, drop it; forcing a diagram onto shapeless prose shows.
3. Build it from code (SVG or HTML to PNG), not with an image generator, which mangles text. If
   the client has a design system, use it with restraint: the diagram belongs to the editor.
4. **Not one figure that isn't in their text.** The whole argument is that the visual is their
   article.
5. Two versions: one with a small credit to the client and a clean one. The clean one is offered
   with no strings.

Deliverable per page: the visual in two versions and the draft. Email skeleton: which section
describes what, the diagram made with their words, attached, credit optional.

## What we don't do

| No | Why |
|---|---|
| Link exchanges or "link for link" networks | Link spam under Google's policy [O] |
| Paying to get into "best of" lists | It gets detected, doesn't last, pollutes the entity; in health it breaks advertising rules |
| Paid campaigns on Reddit, Quora or YouTube presented as user opinion | Astroturfing; same problem as paying to appear |
| Signing up for government or institutional directories just to get a link | Not a surface the buyer consults; the link is not the goal |
| A template sent to hundreds of sites | The method depends on being obviously handmade |
| Claiming something about someone else's page without a primary source | One wrong correction ends the relationship |

## And on your own site

The asset that gets cited the most is the one with sourced data: a **data page** of your own that
passes the filter in `geo-aeo.md` (named source, year, exact figure, opened URL, faithful quote,
live link and linked sources). It is what gives the editor something to link to when they correct
their page.
