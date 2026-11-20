---
name: seo-research
description: >
  Web-based search intent and topic discovery + claim verification.
  Invoked after Stage 1 of /content-seo to replace AI-only Stage 2.
  Input: Stage 1 dump (TOPIC, HUB, TARGET READER, fields 1-5).
  Output: raw research bullets with sources — not prose, not essay.
---

# Research Agent

## Purpose

This skill runs real research so Stage 2 of /content-seo is grounded in actual data, not AI inference from training.

The dump supplies the author's material and perspective, not the boundary of research. Use the article request, target reader, and available project context to discover important information beyond the dump. Propose additions when evidence shows that omitting them would leave a reader's need unanswered, cause misunderstanding, or leave an argument unsupported. Do not impose a fixed, mechanical checklist by article type. A content standard an author or project has explicitly designated for a topic type (such as a project/token overview baseline) is applied where it fits — cover each required element, or record with its basis why an element is confirmed absent or not applicable — while the specific questions, depth, and structure stay flexible to this reader and center.

Research combines observed search suggestions/results, reference material, and claim-appropriate evidence. Available GSC/Bing data or user-provided exports may supplement research; no paid provider is required. The center guides emphasis and depth, but does not automatically exclude information needed to understand the article. Surface findings that would change an approved center or scope for the author's decision; do not make that change yourself.

## Input

Read the Stage 1 Perception Dump from the current conversation context.

Required fields: TOPIC, TARGET READER, and the 5 filled fields.

HUB is optional — use it to narrow keyword targeting if present. Use the project context and content policy supplied by the calling workflow; consult the configured policy when needed to judge evidence requirements.

If no Stage 1 dump is found in context, ask:
> "Paste your Stage 1 Perception Dump so I can run research against it."

## Step 1 — Keyword Intent and Candidate Sub-topics

Start the coverage map with questions this reader needs answered. Use TOPIC, TARGET READER, the article request, project context, and the dump. Consult [reader-task lenses](references/reader-task-lenses.md) to identify the reading task and turn each applicable author- or project-designated content requirement into a question or part of a question — applying only what fits this article, and marking a requirement confirmed not-applicable with its basis rather than forcing it; these are the reader's needs, not a fixed list to complete for every article. Choose the questions and depth to fit the reader and center. Use unanswered questions and missing parts of answers to formulate research queries.

Use Google Suggest (Autocomplete) to expand query variants, questions, and topic branches when exploring search needs. Record the seed query, observed suggestions, language/region settings, retrieval date, and source URL or retrieval method. Suggestions are discovery signals, not evidence for a factual claim, search volume, difficulty, or importance rankings. Their order does not establish priority; absence does not show absence of demand. If Suggest is unavailable, report that and continue with other sources. Do not fabricate suggestions or label ordinary search results as Autocomplete observations.

Search the web for relevant candidates and inspect results. Record URLs and distinguish observed search intent from interpretation. Use available first-party data or supplied exports only with source, market, date range, and metric labels. GSC impressions/clicks are not monthly search volume. Without a volume source, write `unavailable — no volume source`; do not invent numbers or treat missing data as zero demand.

Reader awareness is a hypothesis only when supported by observed queries and results. Otherwise write `UNKNOWN — insufficient observed evidence` and use TARGET READER from the dump.

Use the main query to find a suitable overview, official document, or specialist source for the target reader. Where organic rankings for the target market are observable, use the leading relevant results as a starting point. Otherwise select from the available results by relevance and quality. If the results lack context the reader needs, broaden the query.

Use search results to select relevant pages. Frame extraction requests around the coverage questions and the explanation still needed, including relevant relationships or conditions and the passages that support them. Reuse original passages already returned by a tool and use a passage for multiple questions where it supports them. Treat snippets and generated syntheses as leads.

As you read, add concise answers and their supporting sources to the corresponding questions and carry supported findings into RAW EVIDENCE. If a source reveals a question or dependency the reader needs to understand the topic, add or revise the relevant question, record why it matters, and use any unresolved part to guide further research. Continue to consider relevant leads from search and sources even when the initial questions have answers. Apply the relevance criteria below, discard navigation and boilerplate, and label parent-topic sources as such. Record when a passage is inaccessible or leaves a question unanswered.

For each proposed sub-topic, explain its value to this reader or argument and cite the observed basis. Keep editorial relevance separate from evidence confidence:
- Strong: omitting it would leave an essential question unanswered, cause misunderstanding, or leave a material argument unsupported; explain why.
- Candidate: useful additional context whose depth depends on the article's purpose and scope.
- Weak: peripheral or indirect relevance; usually better deferred or linked elsewhere.

These labels are editorial judgments, not measured search demand. Source counts alone do not determine importance or certainty, and repeated copies of one source are not independent evidence. Record evidence confidence and limitations separately for each candidate. If no useful sources are retrieved, output `none — no data`, confidence `NONE`; Steps 2 and 3 still run. Missing keyword metrics do not mean research failed.

## Step 2 — Claim Verification

Verify factual claims in the dump and new factual findings proposed for the article. An opinion or the author's personal experience is not an external fact; distinguish it from factual premises that can be checked.

Discovery sources and verification sources have different roles. Use quality overviews and secondary sources to understand context and find leads. For verification, choose evidence that supports the specific claim: prefer original documentation, data, research, or firsthand records for specifications, mechanisms, and directly recorded facts; use credible independent specialist sources for analysis, context, and comparison where appropriate. Evaluate relevance, supporting evidence, authorship, date/version, and independence rather than relying on a site's reputation alone. Apply the project's evidence policy, especially for claims affecting money or safety. A discovery lead is not automatically verified evidence.

For each verifiable claim, search for it and report:
- **CONFIRMED** — supported by suitable evidence (include URL and any material scope limits)
- **CONTRADICTED** — suitable evidence says something different (include URL + what it says)
- **UNVERIFIABLE** — adequate evidence not found; flag the gap before publishing

Keep the existing dump-claim table columns unchanged. Record new findings with their supporting evidence and limitations in RAW EVIDENCE BULLETS and the COVERAGE MAP; do not invent a dump field for them. A claim appearing in the dump is not itself verification.

## Step 3 — Coverage Map

Finalize the coverage map started in Step 1 using the findings from claim verification. Update answers and evidence limits where verification changes what the sources support. Do not impose a fixed question count, add filler, or omit essential questions to meet a limit.

Before finalizing the coverage map, reconcile the explicit comprehension needs in the article request and TARGET READER, together with any applicable author- or project-designated content standard, against the actual answers in the map. A combined answer may satisfy several needs; a related topic or keyword mention alone does not establish that a need is answered. Where retrieved material already contains a missing explanation, carry that explanation and its supporting source into the map. For needs still lacking adequate evidence, make one focused supplementary research pass across those gaps, then record any remaining missing answers or evidence explicitly rather than omitting the needs. This check does not limit discovery to stated needs.

For each question:
- State it as the reader would ask it.
- Note whether a dump field addresses it (field N) or it is NOT in dump. This marks origin, not completeness or verification.
- Give a concise answer or evidence bullets with suitable sources; refer to an existing verified claim when that avoids repetition. Mark missing evidence honestly.
- For questions outside the dump, explain why the addition matters to the reader or argument.
- Note material conditions, uncertainty, conflicting evidence, or a scope decision needed from the author.

The center sets emphasis and depth, not an automatic veto on necessary context. Surface any conflict with approved scope for the author without changing the center or adding a new approval step here.

Also identify SERP format gap **only from an observed SERP** (a fetched results page for the keyword): what content format or angle is underrepresented in top results? (e.g., top results are all definitions → gap is mechanism explanation). If you did not observe the SERP, write "chưa xác định — chưa khảo sát SERP"; do not infer a gap from intent codes or training data.

## Output Format

Output MUST be raw research notes. No intro sentence. No "Here is the research summary." No prose paragraphs. No headers that introduce sections with narrative.

Format exactly as follows:

```
[RESEARCH OUTPUT — paste into Stage 2 of /content-seo]

KEYWORD DEMAND (VN market):
- "[keyword]": [sourced volume/month, or unavailable — no volume source] — [observed intent or UNKNOWN] — [source URL/date or unavailable]
- (first-party impressions/clicks, if available, are separate metrics with their date range; never label them search volume)

READER AWARENESS STAGE: [Unaware | Problem-aware | Solution-aware | Most-aware | UNKNOWN — insufficient observed evidence]
→ Implication: [evidence-backed hypothesis for hook/depth; if UNKNOWN: "not inferred — use TARGET READER from the dump"]

SEARCH DISCOVERY:
- Google Suggest: [seed → observed suggestions; language/region; date; source URL or retrieval method; or unavailable + reason]
- [relevant search/source observation] — [URL/date; distinguish observation from interpretation]

CANDIDATE SUB-TOPICS (advisory — reader relevance; center guides emphasis and depth):
- [Strong | Candidate | Weak]: [topic] — [why relevant] — [source URLs]
  → Evidence confidence: [HIGH | MEDIUM | LOW | NONE] — [basis and limitations, separate from importance]
- (when no useful sources were retrieved: "none — no data" + Confidence: NONE; do not fill topics from training data)

CLAIM VERIFICATION (fixed table — /content-review reads this by machine; keep the columns exactly):
| Claim (exact wording from dump, field N) | Status | Source |
|---|---|---|
| "[claim]" | CONFIRMED | [URL] |
| "[claim]" | UNVERIFIABLE | adequate evidence not found — author to verify |
| "[claim]" | CONTRADICTED | [URL] — [what the source actually says] |

RAW EVIDENCE BULLETS (verifiable facts with source):
- [fact] — source: [URL]
- [fact] — source: [URL]
- (only include if found; omit section if nothing verifiable)

GAPS (claims that need user to provide source):
- [claim or proposed finding lacking adequate evidence; identify what remains unresolved]

COVERAGE MAP (reader comprehension — questions reader needs answered to understand this topic):
- [question] — addressed in dump: field N / NOT in dump
  → [concise answer/evidence] — source: [URL or reference to verified claim above]
  → Why add: [reader need, misunderstanding avoided, or argument supported; required for questions outside dump]
  → Limits: [material conditions, uncertainty, missing evidence, or author scope decision; omit if none]
- (no fixed count; ground additions in observed material and relevance, not training-data assertions or a quota)

SERP FORMAT GAP:
- [what format or angle top results are missing for this keyword — only if you fetched or otherwise observed the SERP; otherwise write exactly: "chưa xác định — chưa khảo sát SERP"]
```

## After Output

Return control to /content-seo immediately. Do not ask the user a question here — /content-seo presents the research as a challenger during center selection (Stage 3), which is the author's single decision point for research.

This skill does NOT run Stage 3 or 4.

## What This Skill Does NOT Do

- Does not infer facts from AI training data
- Does not treat suggestions, source reputation, or repeated mentions as proof of a claim
- Does not produce prose paragraphs or summary essays
- Does not run Stage 3 or 4 — it only covers Stage 2
