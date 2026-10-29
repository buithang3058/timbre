---
name: seo-research
description: >
  SEMrush keyword intent analysis + primary source verification.
  Invoked after Stage 1 of /content-seo to replace AI-only Stage 2.
  Input: Stage 1 dump (TOPIC, HUB, TARGET READER, fields 1-5).
  Output: raw research bullets with sources — not prose, not essay.
---

# Research Agent

## Purpose

This skill runs real research so Stage 2 of /content-seo is grounded in actual data, not AI inference from training.

Three tools:
1. **SEMrush phrase_this** — keyword volume + search intent (reads demand signal and reader awareness stage)
2. **SEMrush phrase_related + WebFetch English** — candidate sub-topics (Semrush relevance × H2 headings of one English reference page; advisory, not a Google ranking signal)
3. **Web search** — primary source verification for claims in the Perception Dump

## Input

Read the Stage 1 Perception Dump from the current conversation context.

Required fields: TOPIC, TARGET READER, and the 5 filled fields.

HUB is optional — use it to narrow keyword targeting if present.

If no Stage 1 dump is found in context, ask:
> "Paste your Stage 1 Perception Dump so I can run research against it."

## Step 1 — SEMrush Keyword Intent

Load the API key (run from `${CLAUDE_PLUGIN_ROOT}/` — where `.env` lives). Never print any part of the key:
```bash
source ${CLAUDE_PLUGIN_ROOT}/.env && [ -n "$SEMRUSH_API_KEY" ] && echo "Key loaded" || echo "Key missing"
```

Derive 4-6 keyword candidates from TOPIC + TARGET READER:
- Main topic (as stated in TOPIC field)
- "What is [topic]" variant (informational intent)
- Specific sub-topic from field 3 or 4 (the hidden/mechanism insight)
- Tool or protocol names mentioned in the dump (navigational/commercial)
- Vietnamese and English variants for crypto projects

For each keyword, URL-encode it first (required for Vietnamese characters), then run:
```bash
source ${CLAUDE_PLUGIN_ROOT}/.env
KEYWORD=$(python3 -c "import urllib.parse; print(urllib.parse.quote('KEYWORD_HERE'))")
curl -s "https://api.semrush.com/?type=phrase_this&phrase=$KEYWORD&export_columns=Ph,Nq,In&database=vn&key=$SEMRUSH_API_KEY"
```

Run one curl per keyword. Output format: `Keyword;Search Volume;Intent`

Parse the response: Ph = keyword phrase, Nq = monthly search volume, In = intent code(s): `0` = commercial, `1` = informational, `2` = navigational, `3` = transactional. Multiple intents are comma-separated (e.g. `1,0` = informational + commercial). Not a bitmask.

**Read the response before interpreting it.** Semrush returns HTTP 200 with a body of `ERROR 50 :: NOTHING FOUND` when the database has no row for that phrase — that, and only that, is "no data": record `no data (ERROR 50)` for the keyword and continue. Any other `ERROR <n> :: <text>` (e.g. `ERROR 122 :: WRONG FORMAT OR EMPTY KEY`, HTTP 400; wrong key, units exhausted, rate limit) is an **API failure, not an absence of demand**: stop the Semrush steps, report the exact error line to the user, and do not proceed as if the keyword had no data. A returned row with volume `0` is **not** "no data": keep the row as returned (`0/month — [intent]`); the intent code is still information.

If the main topic keyword itself returns `ERROR 50`, try at most two broader variants (drop the qualifier, e.g. "pruned node là gì" → "node là gì" → "node blockchain") before concluding the VN database has no demand data for this topic. Data found on a broader variant is a signal about the **parent topic**: report it under that keyword, do not attribute it to the original long-tail, and do not derive the long-tail's awareness stage from it. If the topic keyword and its variants all return `ERROR 50`, write `READER AWARENESS STAGE: UNKNOWN — no Semrush demand data`; do not infer a stage from training data.

After all queries, determine: **which awareness stage is the TARGET READER at?**
- Volume high on "what is X" → Unaware or Problem-aware
- Volume high on brand/product names → Solution-aware or Most-aware
- Mix → segment exists at multiple stages

## Step 1b — Semantic Entity Signal (phrase_related)

For the primary keyword (main topic), run phrase_related to get semantically associated terms:
```bash
source ${CLAUDE_PLUGIN_ROOT}/.env
KEYWORD=$(python3 -c "import urllib.parse; print(urllib.parse.quote('KEYWORD_HERE'))")
curl -s "https://api.semrush.com/?type=phrase_related&phrase=$KEYWORD&export_columns=Ph,Nq,Rr&database=vn&key=$SEMRUSH_API_KEY&display_limit=20"
```

Parse: Ph = phrase, Nq = volume, Rr = relevance score (0–1).

If phrase_related returns `ERROR 50` (after the same broader-variant retry as Step 1): flag `[SEMrush no data — WebFetch-only, LOW confidence]` and proceed to Step 1c. Any other error → API failure, same handling as Step 1.

## Step 1c — Semantic Structure Signal (WebFetch English)

Fetch English authoritative sources to extract H2 headings. Try in order — stop on first success:
1. `https://en.wikipedia.org/wiki/[Topic_in_English]`
2. `https://www.investopedia.com/terms/[letter]/[topic].asp`
3. `https://www.coinbase.com/learn/crypto-basics/what-is-[topic]`

Extract H2 headings from the fetched page. These represent the semantic sub-topics the source considers part of this topic.

If none of the three exact-title URLs resolve (Wikipedia 404 for a sub-topic title is common; Coinbase Learn may return 403), fall back once to the **parent topic's** Wikipedia article (e.g. "Pruned node" → `Bitcoin_Core` or `Blockchain`, found via `https://en.wikipedia.org/w/index.php?search=<topic>&ns0=1`) and take its H2s, noting that they describe the parent, not the sub-topic. From any page, keep only content headings related to the topic; drop navigation and boilerplate (References, Further reading, See also, External links). Two related headings are usable; ten unrelated ones are not. No related heading → this signal is empty. Only if that also fails: flag `[WebFetch all failed — phrase_related only, MEDIUM confidence]` and proceed to Step 1d with phrase_related data only. If both Semrush and WebFetch produced nothing, the CANDIDATE SUB-TOPICS block is `none — no data`, confidence `NONE`; Steps 2 and 3 still run, because claim verification and the coverage map do not depend on Semrush.

## Step 1d — Cross-reference → Candidate Sub-topics

Cross-reference phrase_related Rr scores × English H2 headings. This is a signal from one keyword database and one reference page, not what Google "expects". Output is advisory: the approved center (Stage 3) decides what the article covers.

| Condition | Tier |
|-----------|------|
| Rr ≥ 0.5 AND in English H2s | Strong candidate — readers of this topic usually expect it |
| Rr ≥ 0.3 AND in English H2s | Candidate |
| Rr ≥ 0.5 OR in English H2s (not both) | Weak candidate |
| Rr ≥ 0.3 only, not in H2s | Weak candidate |
| Low Rr, not in H2s | Note only |

Classify by data signal alone. The writer decides in Stage 4 which candidates the center needs; a candidate outside the center's logical chain may be a link to another article instead of a section.

## Step 2 — Primary Source Verification

For each claim in the Perception Dump that is a fact, statistic, or protocol behavior — not an opinion — run a web search.

**Primary sources only:** official documentation, protocol whitepapers, GitHub repos, BIP standards, on-chain explorers, academic papers, Chainanalysis reports. Never cite: Medium articles, YouTube, news aggregators, Twitter threads, Reddit.

For each verifiable claim, search for it and report:
- **CONFIRMED** — found in primary source (include URL)
- **CONTRADICTED** — primary source says something different (include URL + what it says)
- **UNVERIFIABLE** — no primary source found; flag for user to verify before publishing

## Step 3 — Coverage Map

From the topic, keyword data, and Perception Dump fields 1-5, identify 5-8 questions a reader needs answered to fully understand this topic. Prioritize questions that appear in related keyword patterns or common search variants — not AI inference about what "should" matter.

For each question:
- State it as a reader would ask it
- Note whether a Perception Dump field already addresses it (field N) or it is NOT in dump
- For questions NOT in dump: run a web search and provide 1-3 evidence bullets from primary sources. Same source rules as Step 2 — no Medium, YouTube, Reddit, Twitter

Aim for 5-8 questions. Fewer is acceptable for a narrow topic; do not pad.

Also identify SERP format gap **only from an observed SERP** (a fetched results page or the Semrush organic report for the keyword): what content format or angle is underrepresented in top results? (e.g., top results are all definitions → gap is mechanism explanation). If you did not observe the SERP, write "chưa xác định — chưa khảo sát SERP"; do not infer a gap from intent codes or training data.

## Output Format

Output MUST be raw research notes. No intro sentence. No "Here is the research summary." No prose paragraphs. No headers that introduce sections with narrative.

Format exactly as follows:

```
[RESEARCH OUTPUT — paste into Stage 2 of /content-seo]

KEYWORD DEMAND (VN market):
- "[keyword]": [volume]/month — [intent: informational|commercial|navigational|transactional]   (volume 0 stays "0/month — [intent]")
- "[keyword]": no data (ERROR 50)
- (repeat for all queried keywords; a broader variant that has data is listed as "[parent keyword] (parent topic, not the long-tail)")

READER AWARENESS STAGE: [Unaware | Problem-aware | Solution-aware | Most-aware | UNKNOWN — no Semrush demand data]
→ Implication: [one sentence on what this means for hook and content depth; if UNKNOWN: "not inferred — use TARGET READER from the dump"]

CANDIDATE SUB-TOPICS (advisory — Semrush relevance × English H2s; the center decides coverage):
- Strong: [topic], [topic]
- Candidate: [topic]
- Weak: [topic], [topic]
- Confidence: [HIGH | MEDIUM | LOW | NONE] — [which data source failed and how: ERROR 50 / WebFetch 404-403 / parent page only]
- (when both signals are empty, this block is exactly: "none — no data" + Confidence: NONE; do not fill topics from training data)

CLAIM VERIFICATION (fixed table — /content-review reads this by machine; keep the columns exactly):
| Claim (exact wording from dump, field N) | Status | Source |
|---|---|---|
| "[claim]" | CONFIRMED | [URL] |
| "[claim]" | UNVERIFIABLE | no primary source found — author to verify |
| "[claim]" | CONTRADICTED | [URL] — [what the source actually says] |

RAW EVIDENCE BULLETS (verifiable facts with source):
- [fact] — source: [URL]
- [fact] — source: [URL]
- (only include if found; omit section if nothing verifiable)

GAPS (claims that need user to provide source):
- [claim from dump that has no verifiable primary source]

COVERAGE MAP (reader comprehension — questions reader needs answered to understand this topic):
- [question] — covered: dump field N
- [question] — NOT in dump
  → [evidence bullet] — source: [URL]
  → [evidence bullet] — source: [URL]
- (5-8 questions total; omit evidence section for covered questions. When keyword data is empty, questions come only from the dump and from sources actually found; do not add questions to reach a count)

SERP FORMAT GAP:
- [what format or angle top results are missing for this keyword — only if you fetched or otherwise observed the SERP; otherwise write exactly: "chưa xác định — chưa khảo sát SERP"]
```

## After Output

Return control to /content-seo immediately. Do not ask the user a question here — /content-seo presents the research as a challenger during center selection (Stage 3), which is the author's single decision point for research.

This skill does NOT run Stage 3 or 4.

## What This Skill Does NOT Do

- Does not infer facts from AI training data
- Does not cite aggregator sites, news, social media
- Does not produce prose paragraphs or summary essays
- Does not run Stage 3 or 4 — it only covers Stage 2
