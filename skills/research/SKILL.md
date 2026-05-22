---
name: research
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
2. **SEMrush phrase_related + WebFetch English** — semantic entity signal (identifies Tier 1/2/3 entities Google NLP expects for this topic)
3. **Web search** — primary source verification for claims in the Perception Dump

## Input

Read the Stage 1 Perception Dump from the current conversation context.

Required fields: TOPIC, TARGET READER, and the 5 filled fields.

HUB is optional — use it to narrow keyword targeting if present.

If no Stage 1 dump is found in context, ask:
> "Paste your Stage 1 Perception Dump so I can run research against it."

## Step 1 — SEMrush Keyword Intent

Read the API key (run from `/Users/buithang/agentic-content/` — where `.env` lives):
```bash
source /Users/buithang/agentic-content/.env && echo "Key loaded: ${SEMRUSH_API_KEY:0:8}..."
```

Derive 4-6 keyword candidates from TOPIC + TARGET READER:
- Main topic (as stated in TOPIC field)
- "What is [topic]" variant (informational intent)
- Specific sub-topic from field 3 or 4 (the hidden/mechanism insight)
- Tool or protocol names mentioned in the dump (navigational/commercial)
- Vietnamese and English variants for crypto projects

For each keyword, URL-encode it first (required for Vietnamese characters), then run:
```bash
source /Users/buithang/agentic-content/.env
KEYWORD=$(python3 -c "import urllib.parse; print(urllib.parse.quote('KEYWORD_HERE'))")
curl -s "https://api.semrush.com/?type=phrase_this&phrase=$KEYWORD&export_columns=Ph,Nq,In&database=vn&key=$SEMRUSH_API_KEY"
```

Run one curl per keyword. Output format: `Keyword;Search Volume;Intent`

Parse the response: Ph = keyword phrase, Nq = monthly search volume, In = intent bitmask (1=informational, 2=navigational, 4=commercial, 8=transactional; can combine, e.g., 5 = informational + commercial).

If volume is 0 or API returns no data — note it as "no data" and continue.

After all queries, determine: **which awareness stage is the TARGET READER at?**
- Volume high on "what is X" → Unaware or Problem-aware
- Volume high on brand/product names → Solution-aware or Most-aware
- Mix → segment exists at multiple stages

## Step 1b — Semantic Entity Signal (phrase_related)

For the primary keyword (main topic), run phrase_related to get semantically associated terms:
```bash
source /Users/buithang/agentic-content/.env
KEYWORD=$(python3 -c "import urllib.parse; print(urllib.parse.quote('KEYWORD_HERE'))")
curl -s "https://api.semrush.com/?type=phrase_related&phrase=$KEYWORD&export_columns=Ph,Nq,Rr&database=vn&key=$SEMRUSH_API_KEY&display_limit=20"
```

Parse: Ph = phrase, Nq = volume, Rr = relevance score (0–1).

If phrase_related returns no data: flag `[SEMrush no data — WebFetch-only, LOW confidence]` and proceed to Step 1c.

## Step 1c — Semantic Structure Signal (WebFetch English)

Fetch English authoritative sources to extract H2 headings. Try in order — stop on first success:
1. `https://en.wikipedia.org/wiki/[Topic_in_English]`
2. `https://www.investopedia.com/terms/[letter]/[topic].asp`
3. `https://www.coinbase.com/learn/crypto-basics/what-is-[topic]`

Extract H2 headings from the fetched page. These represent the semantic sub-topics the source considers part of this topic.

If 0/3 URLs succeed: flag `[WebFetch all failed — phrase_related only, MEDIUM confidence]` and proceed to Step 1d with phrase_related data only.

## Step 1d — Cross-reference → Semantic Entity Map

Cross-reference phrase_related Rr scores × English H2 headings:

| Condition | Tier |
|-----------|------|
| Rr ≥ 0.5 AND in English H2s | Tier 1 [HIGH] — must appear in draft |
| Rr ≥ 0.3 AND in English H2s | Tier 1 [MEDIUM] — must appear |
| Rr ≥ 0.5 OR in English H2s (not both) | Tier 2 — should appear |
| Rr ≥ 0.3 only, not in H2s | Tier 2 [MEDIUM] |
| Low Rr, not in H2s | Tier 3 — optional |

Note: When the approved center is known (Stage 3 of /content-seo), apply the Logical Chain Test to each Tier 1 candidate — "Is this entity in the logical chain leading to the center?" If no → downgrade to Tier 2 (mention-only, 1-2 sentences). In /research output, classify by data signal alone and flag candidates that may need downgrade after center is locked.

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

Minimum 7 questions. 8 if the topic has significant mechanism complexity. Fewer than 7 means the topic is under-scoped for a 1,500-word article.

Also identify SERP format gap: given the primary keyword intent, what content format or angle is likely underrepresented in top results? (e.g., top results are all definitions → gap is mechanism explanation; all how-tos → gap is why-it-matters)

## Output Format

Output MUST be raw research notes. No intro sentence. No "Here is the research summary." No prose paragraphs. No headers that introduce sections with narrative.

Format exactly as follows:

```
[RESEARCH OUTPUT — paste into Stage 2 of /content-seo]

KEYWORD DEMAND (VN market):
- "[keyword]": [volume]/month — [intent: informational|commercial|navigational|transactional]
- "[keyword]": [volume]/month — [intent]
- (repeat for all queried keywords)

READER AWARENESS STAGE: [Unaware | Problem-aware | Solution-aware | Most-aware]
→ Implication: [one sentence on what this means for hook and content depth]

SEMANTIC ENTITY MAP (Google ranking signal — entities Google NLP expects for this topic):
- Tier 1 [HIGH]: [entity], [entity] — must appear in draft
- Tier 1 [MEDIUM]: [entity] — must appear (lower confidence signal)
- Tier 2: [entity], [entity] — should appear; frame through approved center
- Tier 3: [entity] — optional; only if center touches them naturally
- Confidence: [HIGH | MEDIUM | LOW] — [note if any data source failed]
- Logical Chain Test pending: [entities that may need downgrade after center is locked, if any]

CLAIM VERIFICATION:
- "[exact claim from dump field N]"
  → CONFIRMED: [URL]
- "[exact claim from dump field N]"
  → UNVERIFIABLE: no primary source found — verify before publishing
- "[exact claim from dump field N]"
  → CONTRADICTED: [URL] — [what the source actually says]

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
- (5-8 questions total; omit evidence section for covered questions)

SERP FORMAT GAP:
- [what format or angle top results are likely missing for this keyword]
```

## After Output

Say:
> "Research done. Use this as your Stage 2 results in /content-seo. Does anything here change or sharpen your Perception Dump? If not, reply 'proceed to Stage 3' and I'll generate the center of gravity options."

**STOP. Wait for user response.**

This skill does NOT run Stage 3 or 4. Control returns to /content-seo after user confirms.

## What This Skill Does NOT Do

- Does not infer facts from AI training data
- Does not cite aggregator sites, news, social media
- Does not produce prose paragraphs or summary essays
- Does not run Stage 3 or 4 — it only covers Stage 2
