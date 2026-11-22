# From census to action (step 8)

> Step 7 says where the client shows up and which sources the assistants cite. This step turns that
> census into a **short list of third-party pages** worth working on: the ones the assistants
> already use to answer the buyer's questions and where the client is missing.
> Script: `scripts/objetivos_terceros.py`. Methods for each target: `asset-led-links.md`.

**What this is and what it isn't.** It is prospecting guided by real citations, not a campaign.
On its own it produces not a single mention: it produces who to write to, with what and why. There
is no guarantee that a corrected page moves the index; it is measured in the next cycle with the
same battery.

---

## 1. Input

- The cycle's runs (`templates/run.template.md`), in the same folder `indice_citacion.py` reads.
- Only **unbranded** queries: F1, F2, F4 and the optional F5, F6 and F7. F3 stays out: if they
  name you, the page citing you already knows you.
- The JSON output of `verificar_fuentes.py` on that folder. A URL nobody opened is not a target:
  assistants invent URLs (Tow Center, Mar 2025: more than 60% of answers with a wrong citation
  [E], see `geo-evidence.md` 2.5).

```bash
python3 scripts/verificar_fuentes.py runs/ --name "Elena Ruiz" --json > verif.json
python3 scripts/objetivos_terceros.py runs/ --own-domain draelenaruiz.example.com \
    --competitors competidor-uno.example.com --name "Elena Ruiz" --verification verif.json --lang en
```

The script excludes own and competitor domains (subdomains included), groups by URL and domain,
and sorts by **runs without the client** that cite that URL, then by total runs. The type, angle,
contact and priority columns come out empty: they are curated by hand.

## 2. The target table

One row per URL. What the script provides is marked (s); the rest is filled in with the page open.

| Column | Content |
|---|---|
| URL and domain (s) | The URL as the assistant cited it, and its domain |
| Type | `listicle`, `directory`, `comparison`, `forum`, `media`, `profile`, `guide`. Decided with the page open, not from the URL |
| Queries and assistants (s) | Where it weighs: battery ids and the assistants that cited it |
| Runs citing it (s) | How many unbranded runs use it |
| Without client (s) | In how many of those the client did not appear |
| Named (s) | Names the assistant gave in those runs. **Not** what the page lists |
| Competitors on the page | Those the page actually names, checked by opening it |
| Is the client there? | `yes`, `no`, `in passing`, with the verbatim quote if present |
| Verification (s) | Status from `verificar_fuentes.py`; `not opened` does not move forward |
| Angle | One concrete, verifiable sentence: what that page lacks that the client can bring |
| Method | Correction sheet, Tombstone, Missing visual or profile (see `asset-led-links.md`) |
| Contact | Contact page, author or form **found on the site itself**; otherwise `unverified` |
| Priority | High, medium or low with the criteria in §4 |

## 3. Why the tail and not domain authority

- Domain authority explains little of who shows up: in AIO, web brand mentions correlate 0.664
  with visibility and DR only 0.326 (Ahrefs, 2025-05-26, 75,000 brands [E]).
- Assistants cite a lot outside Google's top 10: only 2-5% of cited pages come from the top 10 (TJ
  Robertson, 2026-10-25 [E]); only 38% of AIO citations rank top 10 (Ahrefs, 2026-03-02 [E]).
- 93% of the domains cited in local searches are individual business sites (BrightLocal,
  2026-08-26 [E]).
- Our reading [S]: at the head (Wikipedia, Reddit, YouTube, LinkedIn, big media) DR and citation
  agree and nobody gets in this quarter with an email. The difference is in the tail: niche blogs,
  vertical directories, associations, small comparison pages. There an editor replies, and there
  sorting by DR hides what the assistants actually read.

The head is not deleted from the census: it is reported. It only leaves the outreach list.
Reddit, YouTube or LinkedIn are worked with the client's real participation, never with paid
campaigns.

## 4. Priority

| Priority | Criteria |
|---|---|
| High | Cited in 2 or more queries without the client, or by 2 or more assistants; alive; verifiable angle; verified contact |
| Medium | One query or one assistant; verifiable angle; verified contact or public form |
| Low | Weak angle or no verified contact. It stays in the census and is reviewed next cycle |

A useful list has 5 to 20 rows. If 80 come out, the angle was not written with the page open.

## 5. Rules

1. **Nothing invented.** No URLs, no competitors on the page, no contacts, no figures. If it could
   not be opened or checked, the cell says `unverified` and the row does not rise above low.
2. **The source was opened.** `verificar_fuentes.py` first; `anti-bot-block` is opened in a real
   browser before discarding it.
3. **The client sends; the agent only drafts.** A paste-ready draft, from the client's email.
   Never claim something was sent if the client did not send it.
4. **A mention without a link counts too.** Mentions correlate more than backlinks (Ahrefs
   2025-05-26 [E]); an editor adding the name without a link is not a failure.
5. **No payment.** Paying to get into a "best of" list is in the anti-patterns; if an editor asks
   for money, the row is closed.

## 6. Closing the cycle

In the report (`templates/geo-report.template.md`, targets section): the curated table, what was
sent and what came back. In the next cycle the same battery is run: if a worked page starts naming
the client, the census shows it with the URL. No causality is claimed: the coincidence and the
date of the change are reported.
