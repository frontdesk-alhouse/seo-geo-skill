---
# Query id in the battery (Q-01, Q-02...). An id is never reused.
query: Q-01
# Family: F1 unbranded by need, F2 unbranded by decision, F3 branded, F4 third party, F5 specific case, F6 technique.
family: F1
# Query type: informational | local | transactional (copied from the battery, not decided per run).
query_type: local
# Assistant: chatgpt | gemini | claude | perplexity | aio | aimode | copilot
assistant: chatgpt
# Origin: ui (consumer interface, official instrument) | api (only as a declared complement).
origin: ui
# Run number for this query and assistant: 1..N (N=3 by default).
run: 1
# Run date in ISO (YYYY-MM-DD). If you want the time, put it in notes.
date: 2026-01-15
# Session mode, free text: temporary-unpersonalized, temporary-chat, incognito, signed-in...
mode: temporary-unpersonalized
# searched: true if the assistant ran a web search (shows sources or "searching"); false if it answered from memory.
searched: true
# appears: true if the client is named in the answer (even in passing).
appears: false
# position: the client's place in the order of names (1 = first). null if it doesn't appear or there is no order.
position: null
# names: every business or person named, in the order they appear. A [a, b] list or with dashes.
names: []
# cited_urls: every URL the assistant showed as a source, as is. Verify them later with verificar_fuentes.py.
cited_urls: []
# stuck_claim: wrong or unpublished data the assistant attaches to the client (in quotes). null if none.
stuck_claim: null
# notes: selection criteria the assistant stated, errors, location leaks, incidents. In quotes.
notes: ""
---

## Query

Exact text of the query, copied from the battery. Not reworded.

## Verbatim

Paste the full answer here, unedited, including the lists and the text of the sources.
