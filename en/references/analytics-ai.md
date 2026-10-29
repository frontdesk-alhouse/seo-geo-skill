# AI analytics: what you can see for free and what you can't

> GA4, Bing Webmaster Tools, Search Console, IndexNow and Webflow AEO. Tags as in
> `geo-evidence.md`.

**Before setting anything up, set the expectation.** Clicks from AI are rare: ~1% on links in
Google's summaries (Pew, 2025-07-22) and ~4% from chatbots (Reuters DNR 2026) [E]. Analytics sees
the tip of the channel, not the channel. The KPI is still citation and mention
(`citation-measurement.md`); analytics is secondary evidence that those citations send visits.

---

## 1. GA4: AI referral channel

By default GA4 puts chatgpt.com, perplexity.ai and the like into **Referral**, mixed in with
everything else. Create a custom channel group.

**Steps:**

1. Admin → Data display → Channel groups → Create new channel group (a copy of the default).
2. Add new channel → name it `AI Assistants`.
3. Condition: **Source** · matches regex · paste:

```
(^|\.)(chatgpt\.com|chat\.openai\.com|perplexity\.ai|gemini\.google\.com|bard\.google\.com|copilot\.microsoft\.com|edgeservices\.bing\.com|claude\.ai|deepseek\.com|grok\.com|meta\.ai)$
```

4. **Reorder: `AI Assistants` above Referral.** GA4 assigns the first channel that matches; if it
   sits below, it never receives anything.
5. Save it and use it as the primary dimension in Acquisition → Traffic acquisition. It also
   applies to historical data (custom groups reprocess).

**Notes:**

- GA4 reportedly launched a native "AI Assistant" channel (2026-05-13) that excludes Perplexity ⚠️
  secondary coverage. If it shows up in the property, keep the custom one anyway: it covers more
  sources and is comparable with previous months.
- ChatGPT adds `utm_source=chatgpt.com` to many links it puts in its answers. Also check
  Session source / medium with that value.
- **A lot of AI traffic arrives as Direct**: desktop and mobile apps, copy-pasting the URL,
  AI browsers. There is no way to recover it; declare it.
- Clicks from AIO and AI Mode land in **Organic Search**, indistinguishable from normal organic.
- Create an exploration with landing page × `AI Assistants` channel to see which pages receive that
  traffic. It usually matches the URLs in the source census.
- If the client has a CRM, store the first visit's `source` on the lead to tie AI to real
  conversions.

## 2. Bing Webmaster Tools: AI Performance

**The only free first-party citation report** [O]. Public preview since Feb 2026 at
bing.com/webmasters/aiperformance: it shows how many times Copilot and Bing's AI answers cited each
page of the site and with which grounding queries. No clicks.
https://searchengineland.com/bing-webmaster-tools-testing-new-ai-performance-report-468039

**How to turn it on:**

1. Sign in to Bing Webmaster Tools with a Microsoft account.
2. Add the site. Fastest: **import from Google Search Console** (brings ownership and sitemaps).
   Alternative: meta tag verification (Webflow: Site Settings → Custom code → Head; Framer: Site
   Settings → General → Custom Code) or a DNS record.
3. Submit the sitemap if it wasn't imported.
4. AI Performance fills in over time; check it after 2-4 weeks.

Reading it: grounding queries tell you which questions Copilot is answering with your pages. Use
them to feed the measurement battery (as new queries at the end, with their date added).

**Bing as cheap insurance.** Bing and Copilot share an index [O]. The ChatGPT and Bing relationship
is disputed: OpenAI has its own index (OAI-SearchBot), Seer reported that 87% of ChatGPT citations
matched Bing's top results, and 2026 tests suggest a shift toward Google [S]. Being well indexed in
Bing takes an hour and covers that scenario.

## 3. Search Console: Generative AI report

Beta since 2026-06-03 [O]: **impressions only**, AIO + AI Mode + Discover combined, no clicks and no
breakdown by surface. AIO and AI Mode traffic also counts inside the "Web" search type of the normal
performance report.

Good for: seeing whether key pages appear on Google's AI surfaces and their trend. Not good for:
attributing clicks or separating AIO from AI Mode. Don't report it as "citations".

## 4. IndexNow

A protocol to tell Bing (and Yandex, Seznam, Naver) that a URL changed [O]. Bing reports that ~50%
of new URLs clicked in its search engine arrive via IndexNow. Google doesn't participate.

- Webflow and Framer: no confirmed native support. Options: submit manually from Bing Webmaster
  Tools (URL Submission) when publishing key pages, or a Webflow publish webhook that calls the
  IndexNow API (requires an intermediate service and the key at the root).
- For most studio sites, a manual submission at each launch or major change is enough.

## 5. Webflow AEO

Announced 2026-04-13, available for Enterprise since 2026-05-21 [O via press]. It includes
analytics of AI bot visits, brand citations, conversions attributed to AI and Prompt Insights
(ChatGPT first); content agents since 2026-07-28; it consumes AI credits since 2026-06-29. Requires
Analyze for Enterprise. In the Webflow MCP its surface is `data_aeo_tool`.

When it applies: only if the client is already on Enterprise. Most studio clients aren't; for them,
the manual stack in this file. If it is available, its prompt data is treated as [S vendor] until
checked against your own measurement, and the AI bots it logs are useful to confirm that robots.txt
and Cloudflare aren't blocking them.

## 6. Paid tools

| Tool | What it does | For whom |
|---|---|---|
| Profound | Citation monitoring at scale, multi-assistant | Enterprise |
| Peec AI | Prompt and citation tracking by brand | Agencies, mid-size |
| Otterly | Low-cost prompt tracking | Small business, small agency |
| Semrush AI Toolkit | AI visibility inside Semrush | If they already pay for Semrush |
| Ahrefs Brand Radar | Brand mentions in AI, with YouTube and Reddit since Jan 2026 | If they already pay for Ahrefs |

They mostly measure via API or with their own sampling; their figures are not comparable with the
manual UI measurement. If the client pays for one, it is used as a declared complement, not as a
replacement for the protocol. None of them turns its "score" into evidence of cause.

## 7. The monthly report

| Block | Source | What gets written |
|---|---|---|
| Measured citations | Manual runs + `scripts/indice_citacion.py` | Index by assistant and family with interval; only in measurement months |
| Citations in Bing/Copilot | Bing WMT AI Performance | Most-cited pages and new grounding queries |
| Presence in Google AI | Search Console Generative AI | Impression trend for key pages |
| Visits from AI | GA4 `AI Assistants` channel | Sessions, landing pages, conversions; compare with the previous month |
| Declared attribution | "How did you hear about us?" question | Count of "AI assistant" answers |
| Technical health | `scripts/check_html_crudo.py` | Bots not blocked, correct raw HTML, llms.txt and sitemap live |

Rules: don't add these sources into a single number; each one measures something different. Always
declare that Direct hides part of the channel. See `report-template.md` for the client-facing
format.
