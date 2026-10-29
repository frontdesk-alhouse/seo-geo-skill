# AI bots: robots.txt, Cloudflare and raw HTML

> Which bot does what, what is allowed by default, how to apply it on any platform, and how
> to check that what the bot receives is what the client thinks they published.
> Tags as in `geo-evidence.md`: [E] study · [O] official · [S] inference or vendor.

---

## 1. The three roles

Every AI company has (or should have) one bot per role. Mixing them up is the most common mistake:
blocking "OpenAI" to avoid training and, along the way, dropping out of ChatGPT Search.

| Role | What it does | If you block it |
|---|---|---|
| **Training** | Collects a corpus to train models | You don't drop out of search-backed answers; you stop contributing to the model's base knowledge |
| **Search index** | Builds the index the assistant queries when answering | **You drop out of that assistant's search-backed answers** |
| **User fetch** | Opens a URL because a user asked for it in the chat | The assistant can't read your page when someone shares it; several state that robots.txt may not apply |

## 2. Official token table

| Token | Company | Role | Tag and source |
|---|---|---|---|
| `GPTBot` | OpenAI | Training | [O] https://developers.openai.com/api/docs/bots |
| `OAI-SearchBot` | OpenAI | ChatGPT search index; blocking it removes you from search answers; changes reflected in ~24 h | [O] same page |
| `ChatGPT-User` | OpenAI | User fetch; "robots.txt rules may not apply" | [O] same page |
| `OAI-AdsBot` | OpenAI | Review of ad landing pages | [O] same page |
| `ClaudeBot` | Anthropic | Training | [O] https://support.claude.com/en/articles/8896518 |
| `Claude-SearchBot` | Anthropic | Search index | [O] same page |
| `Claude-User` | Anthropic | User fetch | [O] same page |
| `PerplexityBot` | Perplexity | Search index; "not used to crawl content for AI foundation models" | [O] https://docs.perplexity.ai/guides/bots |
| `Perplexity-User` | Perplexity | User fetch; "generally ignores robots.txt" | [O] same page |
| `Googlebot` | Google | Search, AIO and AI Mode | [O] |
| `Google-Extended` | Google | Token (not a separate crawler) for Gemini training and grounding; does not affect inclusion or ranking in Search, AIO or AI Mode | [O] https://developers.google.com/search/docs/appearance/ai-features |
| `Bingbot` | Microsoft | Bing search and Copilot | [O] |
| `Applebot-Extended` | Apple | Apple training opt-out; does not affect ranking | [O] https://support.apple.com/en-us/119829 |
| `meta-externalagent` | Meta | Meta AI | [O] |
| `CCBot` | Common Crawl | Open corpus used by many training runs | [S] |
| `Bytespider` | ByteDance | Training | [S] |

**Errors that circulate and that we don't repeat:** "GPTBot feeds ChatGPT Search" (false: it's
OAI-SearchBot); `anthropic-ai` as a current token (retired); calling Meta AI's bot "FacebookBot";
describing `GoogleOther` as an AI bot; leaving out `Claude-SearchBot`, `Claude-User` and
`Perplexity-User`.

About Claude: its search uses Brave Search as the backend (declared subprocessor since 2025-03-19)
[O]. Being in Brave's index matters for Claude even though Brave isn't in your robots.txt.

## 3. Default policy: allow everything

**Skill default: no AI bot is blocked.** Template: `templates/robots-ai-allow.txt`.

Reason: for a medical practice, an industrial company or a SaaS in Mexico, the problem is not being known,
not being copied. Blocking training removes the client from the model's base knowledge, which is
where answers come from when the assistant does **not** search (Claude searched in only 36.6% of
prompts in 8ight.AI, 2026-10 [E, small sample]). The cost of allowing is low: the content is already
public and made to circulate.

## 4. Variant: training opt-out

Template: `templates/robots-ai-optout-training.txt`. For clients with proprietary content
(research, courses, paid data) or who explicitly ask for it.

```
# Search and user fetch: ALLOW
User-agent: Googlebot
User-agent: Bingbot
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Perplexity-User
Allow: /

# Training: BLOCK (client's decision)
User-agent: GPTBot
User-agent: ClaudeBot
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: CCBot
User-agent: Bytespider
Disallow: /
```

**Declared cost, and the client is told in writing:** the model stops learning from the site in
future training runs. Answers without search will depend only on what third parties say about it.
It does not remove it from AIO or AI Mode (only blocking Googlebot would) [O].

**Content-Signals** (contentsignals.org) lets you declare intent in the same robots.txt, for
example `Content-Signal: ai-train=no, search=yes`. It is a declaration, not a technical block; whether it's
respected depends on each company [S]. It can be added to both templates without risk.

## 5. Cloudflare: the risk is in the client's zone

Hosted platforms (for example Webflow and Framer) serve the site from their own infrastructure. The problem appears when the
client (or their IT provider) puts **their own Cloudflare zone with the orange-cloud proxy** in front of the
domain. Then that zone's configuration rules, not robots.txt.

| Date | Change | Tag |
|---|---|---|
| 2025-07-01 | New zones block AI bots by default; pay-per-crawl (HTTP 402) in beta | [O] |
| 2025-08-04 | Cloudflare accuses Perplexity of stealth crawlers and removes it as a verified bot | [O] |
| 2026-09-15 | "Disallow AI Training" control: in Block mode it can also stop Googlebot, Bingbot and Applebot, including search | [O] ⚠️ secondary coverage |

Audit (ask the client for access or a screenshot):

1. `dig +short domain.com` and check whether a Cloudflare IP answers.
2. In the dashboard: Security → Bots and AI Crawl Control. Look for blocks on AI search bots and
   the status of "Disallow AI Training".
3. Check whether Cloudflare is **rewriting** robots.txt (managed robots): the served file doesn't
   match the one written in the platform.
4. Confirm with `scripts/check_html_crudo.py` that each search bot gets 200, not 403 or 402.

## 6. How to apply it

Where robots.txt is edited on each platform (WordPress, Shopify, Squarespace, Wix, Webflow,
Framer, frameworks and plain HTML): `platforms.md`. Below, the Webflow and Framer details.

**Webflow.** Site Settings → SEO → robots.txt. Paste the full template content and
publish. Add `Sitemap: https://domain.com/sitemap.xml` at the end. The `.webflow.io` staging
carries its own noindex (see `launch-checklist.md`), not touched from here. There are reports
of Content-Signal support ⚠️; verify in the served file.

**Framer.** Custom robots.txt via **Static Files**, available on Pro and Enterprise plans
[O] https://www.framer.com/help/articles/how-can-i-access-the-robots-txt-file . On lower plans
the robots.txt generated by Framer stays; verify that it doesn't block anything and document it as a
limitation.

**Always:** after publishing, `curl -s https://domain.com/robots.txt` and compare against the
template. What matters is what's served.

## 7. The raw HTML check

AI bots **do not execute JavaScript**: GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Meta's bots
and Bytespider only read the HTML the server returns [E] Vercel/MERJ, Dec 2024,
https://vercel.com/blog/the-rise-of-the-ai-crawler . Googlebot does render, which is why a site can
look perfect in Search Console and empty to ChatGPT.

What breaks, with Webflow and Framer examples (the pattern applies to any site that renders content with JS):

| Pattern | Platform | Risk |
|---|---|---|
| Embeds that render content client-side (review widgets, calendars, pricing) | Both | The text doesn't exist for the bot |
| Tabs and accordions whose content is injected by JS | Both (in native Webflow it's usually in the HTML; in external libraries it isn't) | Invisible FAQ answers |
| Code components that `fetch` | Framer | Dynamic content empty in the HTML |
| CMS lists loaded or filtered by JS (Finsweet and similar) | Webflow | Only the first page, or nothing |
| JSON-LD injected by a script or by GTM | Both | The schema doesn't exist for bots without JS |
| Key copy inside images, SVG or Lottie | Both | It isn't text |

Manual test:

```bash
curl -s -A "OAI-SearchBot" https://domain.com/service | grep -c "key phrase from the copy"
curl -s -A "GPTBot" https://domain.com/ | grep -c 'application/ld+json'
```

The packaged version is `scripts/check_html_crudo.py`: it walks a list of URLs with each bot's
UA, confirms status, presence of key texts and of JSON-LD, that robots.txt doesn't block search
bots, and that `llms.txt` and `sitemap.xml` respond.

Watch out: a 403 or a "404" with a bot UA and 200 with a browser UA is **anti-bot blocking**, not a page
that's down. Report it as such.

## 8. Gate before publishing

- [ ] Served robots.txt = chosen template (allow or opt-out), with `Sitemap:`.
- [ ] No search bot (Googlebot, Bingbot, OAI-SearchBot, Claude-SearchBot, PerplexityBot)
      gets 403, 402 or Disallow.
- [ ] If the client has their own Cloudflare: reviewed and documented.
- [ ] Key copy and JSON-LD present in the raw HTML of every key page.
- [ ] The opt-out decision, if taken, is in writing with its cost.
