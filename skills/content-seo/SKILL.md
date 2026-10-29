---
name: content-seo
description: >
  Writing, SEO: turn the author's insights and research into an article built around
  an approved central argument, in the author's voice. Cover the reader's search
  intent, preserve clear structure, and carry the draft through checks, review,
  author approval, and image prompts. Use for new SEO articles or revisions.
---

# Content SEO — Writer Workflow

## Project and Voice Routing

Read `../project/SKILL.md` relative to this skill and use its resolution rules with the
optional project argument. Do not maintain a fixed list of projects or use legacy
Claude memory as a competing default. Pin the resolved config to this conversation.

Set `TIMBRE` to the actual installation root containing this `skills/` directory,
not a hard-coded user path. `DRAFTS_ROOT` is the resolved `content.drafts` from the
selected config. `D` is the article dossier under that folder; `ARTICLE` remains
the exact selected working file. Resolve paths before commands and handoffs.

Read `voice.dna` in order, then configured calibration, structural rules, jargon and
content policy. Missing DNA blocks drafting. Optional null resources are skipped;
declared missing files are configuration errors. No voice fallback across projects.
Use any content hubs/audience profiles in the configured DNA. Preserve the existing
voice precedence below. Use project policy without inventing one if none is configured.
Keep `visual.brand` for image-prompt after approval. Before lint, set `LINT` to the resolved `tools.lint` and `TERMS` to resolved `voice.jargon` (unset TERMS when absent). Do not reuse shell values from another project.

**Precedence when voice guidance conflicts (shared with `bui-thang/dna.md` and `structural-rules.md`):**
Facts and safety override every voice rule. Within the voice layer, follow the author's explicit instructions for the current task first. Author-designated voice samples guide expression and the flow of ideas in matching situations; calibration, structural rules and DNA support that reference rather than mechanically removing an expression because a general rule bans its form. Samples do not require copying wording, do not make every retained sentence an intentional author decision, and do not verify claims or authorize borrowing experiences. Where no relevant author instruction or sample applies, a calibration entry matching the exact situation wins; otherwise configured structural rules apply to Mode B and DNA is the default. If structural rules are absent or null, use DNA, calibration and samples without loading an unconfigured structural-rules file. A sample or calibration entry is not a blanket exception for the whole article. Templates in `references/` remain layout suggestions.

Do not summarize or confirm any of these to the user. Proceed to Stage 1.

**Resume rule.** Before Stage 1, check `$DRAFTS_ROOT/` for a folder whose `dump.md` topic matches the request. If found, do not ask for the dump again — read `dump.md` and `sources.md`, determine the working copy as described below, then read `stage` and `center` from that working copy and continue from the first missing step. Do not take `stage` or `center` from `draft.md` before the working copy is fixed. If the request or handoff hands over a specific revision (a path plus its `sha256[:12]`), that named file is the version to continue from: confirm the file's current hash matches the handed-over hash — the hash fixes which content is the chosen revision, it does not establish which copy is newer. Do not use `date`/`stage` frontmatter (or the hash) to infer that one copy supersedes another; version order is not something to deduce here. With no handed-over revision, do not assume `draft.md`, a published copy, or any other copy is the current text. Fix the chosen revision only from a clear basis — the handoff, an explicit author instruction, or a hash matching the handed-over one — and once fixed, that path is the one every later step reads, edits, snapshots (4.2), lints (4.3), hashes, and hands to the reviewer (4.5): carry it through explicitly and never silently fall back to a different `draft.md`. Set `ARTICLE` to that chosen file: for a new piece it defaults to `$D/draft.md`; a resume revision keeps its own path. `ARTICLE` is the working copy for every later step. If `ARTICLE` is not `$D/draft.md`, leave the old `draft.md` untouched — do not archive it or copy the revision into it; edit `ARTICLE` in place instead. If there is no clear basis for which copy is the chosen revision — a handed-over hash matches no file, a named path is missing, or two copies differ with nothing to say which is intended — stop and report the conflicting paths and hashes to the author instead of copying, overwriting, or choosing one. If `center` was never saved, propose one from the existing text and mark it `[CHỜ TÁC GIẢ]` — the author confirms or rewrites it (Decision 1). A `[CHỜ TÁC GIẢ]` center is a question to the author, not a constraint: never draft or re-argue the piece against it, and never record it as approved or write it into frontmatter as the locked `center` without the author's explicit approval. Fact and claim fixes that do not depend on a center may proceed and do not block the lint/review steps; any change to the thesis, framing, causal chain, or conclusion waits for Decision 1. `stage: center-locked` means the center is already approved but drafting/revision is pending: use the saved center and continue at 4.1 without asking Stage 3 again. If the user asks only to review an existing article, do not draft: run Stage 4's review step on the file they name.

---

## Stage 1 — Perception Dump (Human only, NO AI)

Output this template exactly and STOP. Do not write anything else. Do not fill in any field. Do not offer examples or suggestions:

```
TOPIC: [topic]
PROJECT: [project]
HUB: [hub name — use the hub list from this project's DNA; omit if project has no hub structure]
TARGET READER: [who are they, what are they doing, what are they thinking about this]
CONTENT TIER: [Pillar | Cluster]
PILLAR URL: [URL của pillar page — required if CONTENT TIER = Cluster; blank if is Pillar]
CLUSTER PAGES: [listing cluster pages related — required if CONTENT TIER = Pillar; blank if Cluster]

1. What do people get wrong about this?
2. What predicts failure that most people don't track?
3. What secretly matters but nobody talks about?
4. What changed my mind about this?
5. What still bothers me / feels unresolved?
```

Then say:

> "Fill this in offline — paper, notes app, anywhere without Claude open. When done, paste it back here. All 5 fields must be filled. Before pasting, copy your dump to a local note so you don't lose it if this session resets."

**STOP. Wait for the user to paste their completed dump.**

### Stage 1 Validation

When the user pastes their dump, check HUB, TARGET READER, CONTENT TIER, and all 5 fields:

- HUB is invalid if blank AND the project's DNA has a hub structure. If blank but DNA has hubs, infer the hub from the topic and state the inference in one line (no separate confirmation step). If the DNA has no hub structure, skip HUB validation.
- TARGET READER is invalid if fewer than 10 words or still template text.
- CONTENT TIER is invalid if blank or not one of: Pillar, Cluster. If Cluster, PILLAR URL must not be blank. If Pillar, CLUSTER PAGES may be filled later.
- A field 1–5 is invalid if it still contains the unchanged template text, has fewer than 10 words, or is only a topic label with no observation or claim in it (e.g. a bolded heading such as "Mining centralization and miner hedging" names a subject but says nothing about it — ask for the sentence behind it).

If any field fails — list the offending fields and re-present the gate:

> "Fields [X] and [Y] are too short or unchanged. Please fill these in and paste your full dump again."

Do not proceed until all fields pass.

**When validation passes:** save the dump verbatim to `$DRAFTS_ROOT/[slug]/dump.md` (create the folder; slug = TOPIC in Vietnamese no-diacritics, hyphenated). Then immediately invoke `/seo-research [project] [topic]`. No reflection gate: the dump is the author's words; the author will see how they were read when the centers are proposed in Stage 3.

---

## Stage 2 — Research

Goal: real evidence for the human's perception dump. Pattern miner only — not author.

`/seo-research` runs automatically after Stage 1. When it returns its `[RESEARCH OUTPUT]` block, save the full output to `$DRAFTS_ROOT/[slug]/sources.md`. Do not ask the user anything here; go straight to Stage 3, where the research is presented as a challenger to the center options. That is the author's one decision point for research.

**AI-only fallback — last resort only.** Run it ONLY if `/seo-research` fails completely (no keyword data, no claims verified, no coverage map). Never as a default, never to supplement partial data. Semrush returning `ERROR 50 :: NOTHING FOUND` is not a failure — research continues with claim verification and the coverage map, and the output carries `no data` / confidence `NONE` where Semrush was empty. A Semrush API error (any other `ERROR <n>`) is a failure to fix (key, units, rate limit), not a reason to fall back to AI-only. Output must begin with:

> "[Context-only inference from training data — verify before publishing. Do not treat as retrieved fact, especially for YMYL niche (Example DeFi claims, statistics, or specific case studies.)]"

Field mapping for the fallback:
- Field 1 → Where is this misconception most visible? What specific behavior reveals it?
- Field 2 → What's the delayed consequence most people miss? What behavior correlates with failure?
- Field 3 → What evidence supports this? When does it break down?
- Fields 4–5 → What case challenges or sharpens this? What mechanism is underneath?

Output raw bullets grouped by field. No prose, no headers, no framing sentence. Save to `sources.md` with the inference label at the top.

---

## Stage 3 — Center of Gravity (Decision 1)

Goal: identify what the article is REALLY about before any draft. One message, one stop.

**Part A — four centers, from the Perception Dump only** (do not use research output for this part):

```
1. Surface topic: restate the topic from Stage 1 verbatim
2. Weak center: the obvious angle any writer would take
3. Stronger center: a mechanism or tension visible in fields 3-4
4. Strongest center: the underlying insight that explains WHY — the thing
   that makes everything else make sense. If fields 1, 4 or 5 contain a
   specific author observation, change of mind or tension, make this a
   position: name the familiar reading, the author's different view, and
   what the article must explain. It must come from the dump, not be
   invented for drama. Otherwise keep this as the strongest insight.
```

Four labeled bullets. One sentence each. No explanation.

**Part B — research as challenger**, in the same message, directly below:

> "Research: readers are [awareness stage]. Questions the coverage map found that your dump does not address: [list]. Strong candidate sub-topics: [list]. Claims from your dump marked UNVERIFIABLE or CONTRADICTED: [list, or 'none']. Does any of this sharpen, challenge, or confirm a center above?"

If the strongest center is a position, add one final line:

> "Limit on the strongest center: [one material factual condition, counterexample or scope boundary from research; or 'none material found']."

Do not add this line for a direct definition, how-to or announcement. It is
not a new author decision or a balance exercise: it prevents a position from
claiming more than its factual premises support.

Then ask:

> "Which center is closest to what you want to say? Write your own if none fits. Complete the sentence: 'This article is really about ___.'"

**STOP. Wait for the author.** Research does not override the author's direction. If a proposed position depends on a CONTRADICTED factual premise, state that plainly and do not draft it as fact; the author can choose a narrower or revised center. If the author says the options feel generic, skip them and ask only for the sentence.

**Lock and save.** As soon as the author approves the center sentence, set `D="$DRAFTS_ROOT/[slug]"` (the dossier folder) and `ARTICLE="$D/draft.md"` for a new piece (on resume, `ARTICLE` is the working copy already fixed by the resume rule), and save that exact sentence as `center` in `$ARTICLE` frontmatter, before starting Stage 4. Use valid YAML quoting so punctuation and quotes preserve the original value.

- If the file does not exist, create it with frontmatter only: `stage: center-locked`, `project`, `slug`, `tier`, `center`, and `date`. Do not write article prose yet.
- If the file exists (including re-centering), update only `center` and `stage: center-locked`; preserve the body and all other frontmatter. Existing prose is pending revision against the new center, not an approved draft.
- Read back the frontmatter to confirm it saved correctly, then say: "Center locked and saved: '[sentence]'." Do not claim it is saved if the write failed.

The saved center is the constraint for Stage 4 — the draft serves this center, not the surface topic. Change it only when the author approves a new center.

---

## Stage 4 — Draft → Humanizer → Guard/Lint → Review → Approval

Use three passes within the existing writer workflow: prepare, write, then check. No extra agent, report or author approval is needed between these passes. For scoped edits, apply them only to changed passages and their dependencies.

### 4.1 Prepare → Write

**Prepare.** Use the locked center, target reader, `dump.md`, `sources.md` and configured voice resources. In the existing coverage map, arrange essential reader questions into H2/H3 sections and note the answer each section must deliver. Explain unfamiliar foundations before relying on them. Supporting topics may use a brief answer and link; essential answers must appear in the article. Candidates are advisory, not quotas. If essential coverage conflicts with the center, ask the author to decide the scope.

For a rewrite, compare with the selected original and preserve useful answers, conditions and author edits; omit repetition or obsolete facts with a reason. Smoother narration alone is not a reason to cut information. Keep headings useful for scanning.

Choose 2–3 relevant author-approved passages from configured `voice.samples`, the author's edits, or calibration entries marked "từ bài thật". Use them to understand expression and reasoning, not to borrow scenarios, wording or experience. Apply calibration by the passage's purpose and situation, under the existing voice precedence. If suitable samples are unavailable, use the configured DNA/calibration and report the limitation; do not invent approval or add a mandatory sample gate. Identify the author's supplied observations and changes of mind so they survive drafting as the author's perspective.

Read [article criteria](references/instructions-detail.md) for the required reader-facing elements before writing; use the same reference for the final check. Consult [title formulas](references/title-formulas.md) when choosing the title and [structure templates](references/content-structure-templates.md) only when a layout is needed. Templates do not override voice. General website SEO/EEAT assessment belongs to `seo-audit`.

**Write.** Write continuously from the prepared outline, evidence and author material. Grounding means the reader has enough information to understand the next idea; it does not require visible transition questions or narration about the writing process. Keep natural rhetorical questions where useful. Do not force "I", short sentences or dramatic pauses as signs of personality.

Preserve the author's confirmed interpretation and first-person perspective. Use `dump.md` or `author-notes.md` for personal experience; append new author confirmations from chat verbatim to `$D/author-notes.md` with the date before using them. Do not invent beliefs or experiences. For beginner/intermediate articles, everyday explanations and rounded numbers are welcome, but cannot distort the mechanism, argument or money/safety implications.

Mode A utility blocks (takeaways, FAQ, TOC, definitions, tables) prioritize direct answers without voice rules. Mode B prose (hook, body, mechanisms, consequences, conclusion) follows the voice precedence above; structural rules apply only when configured. 

**Hook.** Choose an opening from the article's material: a question to answer, an observation, an author experience, or a concrete situation that helps explain the problem. TARGET READER determines assumed knowledge and what needs explaining; it need not become a character in the hook. Use the hub profile as context, not as a substitute for that reader. Learn why a sample's opening leads to its next idea, rather than repeating its opening structure. When no useful situation is available, address the problem directly.

Source claims as you write. Every number with a unit needs an inline source or an MDX provenance comment after the sentence (`{/* hằng số giao thức */}`, `{/* tự tính: công thức */}`). Keep these labels out of visible prose; derived figures read "theo ước tính". Link the protocol specification at the first constant.

**Facts and reasoning.** Source factual premises and keep the reader able to distinguish measured facts from interpretation in context, following project disclosure rules. An inference may be the author's own: check the premises and reasoning, not whether a source states the exact conclusion. Do not force every inference into "có thể", "nếu… thì…", or "tôi"; use a short attribution or condition only where needed to avoid confusion. Preserve the author's approved position and never invent first-person experience or a personal belief absent from the dump/author confirmations. Opinion labels do not excuse false premises, unsupported causal claims or safety guarantees. Claims of absence still need support or an honestly bounded scope.

**Evidence fit.** Follow content-review Step 5 and project policy: prefer primary evidence, allow an adequately supported secondary source for suitable claims, and require authoritative evidence for direct money/safety instructions. Do not delete a useful historical fact merely because its source is secondary. Before writing a derived figure, compare input definitions, population/denominator, units, data dates and method, then calculate. A shared fetch date does not prove compatibility. Keep input sources, formula and material limitations in existing sources/notes or the provenance annotation; prose can be short and rounded. If inputs are not comparable, record the uncertainty rather than presenting arithmetic as a verified measurement or trend.

**Save the draft immediately.** Use the absolute `$D` and `$ARTICLE` established at center lock. Save the article to `$ARTICLE`, preserving the saved `center` verbatim and unrelated frontmatter; set `stage: draft` and add the title/description. The draft frontmatter includes:

```yaml
---
stage: draft
project: [project]
slug: [slug]
tier: [Pillar | Cluster]
center: "[locked center sentence]"
title: "[the title you intend to use — pick from title-formulas now]"
description: "[meta description 120–160 chars you intend to use]"
date: [YYYY-MM-DD]
---
```

`title` and `description` are claims readers see in the SERP; they must be in the file the reviewer reads. Alternatives can be listed in the self-check, but only the ones in the frontmatter count as reviewed.

Update `stage` as the draft moves: `center-locked` → `draft` → `humanized` (if used) → `reviewed` → `approved`.

### 4.2 Humanizer (local, optional)

Only for Mode B passages that read AI-ish after drafting. Not for Key Takeaways, FAQ, definitions, tables (Mode A — fix those by hand).

1. Copy the draft to a temporary snapshot first: `cp "$ARTICLE" /tmp/[slug].pre-humanizer.md`.
2. Invoke `/humanizer` on the selected passages only. Give it: the passage plus surrounding context; 2–3 paragraphs the author has approved as voice samples (from configured `voice.samples` if present, otherwise the calibration entries marked "từ bài thật"; never pick paragraphs and call them "approved"); the project exceptions: no em dash, en dash only between numbers, H1 Title Case is intentional. State explicitly: **do not remove any claim, do not add opinions or facts, do not borrow experiences from the samples; flag doubtful claims instead of deleting them.**
3. Only the writer applies the result into `$ARTICLE`. Set `stage: humanized`.

### 4.3 Guard and lint

If `tools.lint` is null, skip to 4.4; report lint unavailable and count words directly for self-check.

```bash
: "${LINT:?Set LINT from the resolved project config}"
: "${D:?Set D to the resolved article dossier}"
: "${ARTICLE:?Set ARTICLE to the absolute working-copy path selected above}"
term_args=()
[ -n "${TERMS:-}" ] && term_args=(--terms "$TERMS")  # TERMS = configured jargon, or unset
[ -f /tmp/[slug].pre-humanizer.md ] && python3 "$LINT" --diff /tmp/[slug].pre-humanizer.md "$ARTICLE" "${term_args[@]}"
python3 "$LINT" --all "$ARTICLE" > "$D/lint.txt"; cat "$D/lint.txt"
shasum -a 256 "$ARTICLE" | cut -c1-12      # draft_hash for review.md and the handoff
```

- `--diff` is advisory: it lists quantities (number + unit, incl. counts like "12 từ", durations, storage), years, URLs, and allowlist terms that appeared or disappeared. It does not catch reversed relations or negation. Every difference is a line to read in both versions; a clean diff does not prove meaning was kept. Do not accept a humanizer result that lost a number, URL, or term without a reason.
- `lint.txt` is a candidate list for the reviewer, not a verdict. Em-dash FAILs are yours to fix now. Allowlist compliance (allowed terms in English, everything else Vietnamese) is not machine-checked: read the draft against the Jargon file yourself. Number-provenance items go to the reviewer.

For revisions using the configured content-check interface, check the starting version with `--check-hash FILE EXPECTED_SHA` (recorded SHA-256, 12 or 64 characters). Reuse a snapshot matching that version, or create one; record its path/hash in existing notes. At batch end, run `--diff BEFORE AFTER`, checking the snapshot and any in-scope website source required to stay unchanged via repeated `--check-hash`. Do not repeat per sentence. Hash mismatch/unreadable file: stop and resolve, never silently refresh the expected hash or overwrite author edits. Review frontmatter warnings against author decisions; harmless formatting or already-authorized changes need no separate warning acknowledgement or approval step. Without that lint interface, keep file hash checks without adding a lint dependency.

### 4.4 Writer self-check → `review.md`

Read [article criteria](references/instructions-detail.md) and check the actual draft in three groups: content/SEO, voice/reasoning, and evidence/presentation. Correct specific local gaps before delivery; do not rewrite the whole article to make a checklist pass. Author edits and the locked argument remain constraints.

Write the self-check in `$D/review.md`; preserve existing records when resuming. The reviewer appends below it. Use the same file rather than creating another report:

```markdown
# Review — [slug]
draft_hash: [first 12 chars of SHA-256 of ARTICLE]
stage: writer-self-check

## Writer self-check
- Tier / word count: [tier / count from lint, or direct count with method]
- Content / SEO: [essential question or concept → answer location; gaps and their basis; skipped candidates or rewrite omissions → reason]
- Voice / reasoning: [sample references used; specific mismatch or missing reasoning step → local fix; unresolved limitations]
- CORE-EEAT / presentation: [Warn/Fail IDs and locations, or all pass after checking; metadata, structure and link issues]
- Lint: [path or unavailable; FAIL/WARN counts and unresolved items]
- Reviewed metadata: [actual frontmatter title and description; character counts; title formula if used]
```

Distinguish a missing term from a missing explanation: another accurate name may already answer the question. Compare concepts and relationships against available research, not keyword quotas. If the research cannot establish a gap, report that limitation; do not label this check "NLP analysis" without a corresponding method and data. Put material research gaps back into `sources.md` for research follow-up rather than inventing coverage evidence.

Record unresolved claim issues for the independent reviewer. A clean self-check does not establish author acceptance or publication approval. For scoped revisions, check affected passages and dependencies without reopening completed work.

### 4.5 Review (subagent)

Spawn `/content-review` as a **separate agent with a fresh context** (Agent tool). Do not pass conversation history. Pass paths and the task only. Include one scope line in the existing handoff, not a new file or approval step. Use known author/voice and article type; do not invent a center. An explicit user assignment of writer/reviewer takes precedence over automatic dispatch; prepare the same handoff for that reviewer instead of launching another agent.

```
Skill: [absolute `$TIMBRE/skills/content-review/SKILL.md`]
Project: [project]
Project policy: [configured content.policy, absolute]   (or: none)
Scope: [article type] · preserve [author/voice] and the existing/approved argument · [initial review: consequential claims across the article | re-check: changed claims/IDs + dependent passages] · no style editing
Draft (fixed, do not edit): [absolute `$ARTICLE` — e.g. [absolute `$D`]/draft.md, or the resume revision's own path]   sha256[:12]=[hash]
Sources: [absolute `$D`]/sources.md   (or: none)
Author dump: [absolute `$D`]/dump.md   (or: none — legacy article)
Author confirmation: [absolute `$D`]/author-notes.md   (or: none)
Lint output: [absolute `$D`]/lint.txt   (or: none)
Output: append to [absolute `$D`]/review.md
Task: review claims per the skill; write findings; do not modify the draft.
```

All paths absolute. Compute the hash yourself before dispatch and compare with the reviewer's `draft_hash` on return. Set the subagent's model explicitly to Opus (`model: opus`): a subagent inherits the parent session's model, and a credit-gated model (Fable) can terminate the review mid-run on a spend limit.

While the reviewer runs, you may prepare alternative titles. Image prompts wait until the author approves the final content under 4.7. Do not touch `$ARTICLE` until the reviewer returns; anything you later move into it or its frontmatter (a different title, a new description) is a change and goes through 4.6.

### 4.6 Process findings

Read the reviewer's `## Findings`. **First classify each "Cần sửa trước khi đăng" item before touching the draft** — this classification decides whether "apply yourself" applies:
- *Local fix* — the smallest change makes the claim accurate or the scope honest without altering the point, the causal chain, or the conclusion. Apply it yourself (only the writer edits `$ARTICLE`).
- *Touches thesis / framing / center* — correcting the fact forces the argument, angle, or conclusion to change, or the sentence to be corrected is itself an unproven thesis claim. Do NOT apply it. Keep the verbatim before/after proposal, evidence and reason in existing notes/review only; leave the article unchanged at those locations until the author decides. A "temporary safer version" is still an applied change, not a proposal. Pause that item, not unrelated local fixes; group pending decisions for the author instead of repeatedly rewriting the unresolved item.

Adding a hedge ("ước tính", "thường", "một số") does not discharge an UNVERIFIED figure or claim. Either attach a source that supports that exact sentence, or handle the whole claim: dropping only the number and keeping the sentence is allowed **only if the remaining assertion is itself sourced or self-evident**; otherwise remove or narrow the claim, and if doing so touches the thesis/framing, put it to the author instead of deciding it yourself. Do not defer sourcing to publish — wire the sources you already have into the right claim groups now.

**One before/after check per batch.** Read all scoped findings, group repeated claims with dependent premises/conclusions, and apply local fixes together. Search every occurrence in Key Takeaways, body, tables, FAQ and title/description. At batch end, compare the changed passages with their originals:

- Is the original error resolved, including any completion conditions, without adding unsupported claims?
- Are the author's point, voice, causal chain and conclusion preserved, without invented experience or repeated warnings?
- Are repeated claims and dependent passages consistent with the fix?

Report unresolved points together in existing notes, describing the actual text, not the intended edit. Lint/guard PASS proves neither meaning nor voice preservation. Use the closure/re-check routes below; self-check alone does not close findings.

- An exact replacement explicitly permitted for writer-only closure by the reviewer → apply the content-review Re-check contract: same checked evidence, all affected occurrences/dependencies handled, nothing beyond the checked correction or any unresolved conflict, and any required author approval obtained. Verify the actual diff, run applicable lint, and append an application receipt with IDs, before/after hashes, locations and the reviewer instruction/evidence in existing notes/review. Do not alter the reviewer's old labels, status or reviewed hash, or claim another review occurred.
- Other changes to claims, sources, conditions or operational steps → send one batch to the assigned reviewer, with changed IDs/passages, dependencies and evidence; no full review or automatic fetch of unchanged evidence.
- Wording only, meaning intact → re-run applicable lint; no re-review.

Stop when the scoped findings are resolved and remaining author decisions or evidence gaps are explicit. Do not start another polishing/research pass merely because the writer returned a revision. When measuring a test, record before/after hashes, changed scope, actual start/end times (separate waits), tool/fetch counts and token usage if exposed in the existing notes; otherwise report unavailable. Keep writer/reviewer measurements separate and do not substitute conversation-wide usage or claim voice preservation without author comparison.

The minimal fix follows the author's DNA. Do not mechanically add hedges, disclaimers, or repeated warnings; add a condition only when omitting it would materially mislead the reader or when project policy requires it. Do not rewrite rhythm, emotion, rhetorical questions, metaphor, or recognisable interpretation merely to make prose sound "safer". Ask: **if this claim is wrong, could the reader act harmfully or misunderstand a core mechanism or the main argument?** If yes, check and handle it; otherwise investigate only when something looks off, while still reporting clear errors already found. Judge the claim's use in context, not its topic or the presence of a number. Use the project policy for domain-specific risks. This is a selection criterion, not a new scoring system, table column, or approval gate; it does not waive the project's sourcing rules. An unchecked claim is never written as verified.

For a full drafting/approval pass, propose only cuts that remove redundancy or improve understanding, without applying them. Judge the sentence's function in context under the existing voice precedence, not its opening phrase or position. Skip this style-polish step during scoped revisions/re-checks unless the author explicitly requests it:

| Pattern | Description |
|---------|-------------|
| Redundant narration | Announces the writing process or repeats a promise without orienting the reader; keep framing and transitions that help the reader follow |
| Unnecessary setup | Background that neither explains why the question matters nor supports the next idea; keep useful context |
| Packaged wisdom | Generic insights not specific to the author's perception |
| Redundant explanation | Restates what the context already makes clear; keep explanations needed to understand the reasoning, and do not delay an answer merely to manufacture tension |
| Fake cadence | Rhythm added to feel deep, not to carry meaning |

### 4.7 Author approval (Decision 2)

Present in one message: the draft; the reviewer's "Bạn quyết định" items; open UNVERIFIED / UNATTRIBUTED claims; the proposed cuts; title options and meta. Ask:

> "Approve as is, approve with these cuts [list], request another pass, or re-center?"

- **Approve** (with or without cuts) → apply approved cuts and title/description choices under 4.6. A cut removing a condition, source or step, or a title/description changing a checkable claim, needs scoped re-check unless it meets the explicitly permitted exact-fix closure rule. Process new findings under 4.6; any new thesis decision returns to the author. Set `stage: approved` only with author approval of the final changes, lint resolved (defined below), no unresolved "Cần sửa" items and no required evidence gaps. Coverage must come from the reviewer plus any valid application receipts under the Re-check contract; receipts do not turn unchecked claims into verified ones. **Lint resolved** does not mean an empty `lint.txt`, and never edit the draft just to silence a line or rewrite the tool's FAIL/WARN output — keep that output as the tool emitted it. Each FAIL is either fixed in the draft or a justified exception — recorded in `review.md`/notes with the check/location, the reason, and its basis (project policy or the reviewer's conclusion) — such as the intentional H1 Title Case. A FAIL that is neither is an open finding and blocks approval. A justified exception never waives verification of a content claim: it covers a tool FAIL the author has grounds to accept, not the writer declaring a claim checked. WARN-level items and "Có thể cải thiện" must be read, not auto-dismissed, and do not block once noted. Do not reclassify a real error as a warning to wave it through. In `review.md` record `approved: [date]`, `approved_hash: [final sha256[:12]]`, `reviewed_hash: [actual last reviewer-covered hash]`, and reference any intervening application receipts/wording-only diffs linking that hash to the approved version. Preserve the historical review status; do not imply the reviewer read the final version if they did not. For every new article, continue to 4.8 before ending the workflow, unless the author explicitly declines image prompts. Publishing is separate; nothing here publishes.
- **Another pass** → apply requested changes (4.6 rules), return here.
- **Re-center** → Stage 3 with the new candidate. `sources.md` is preserved; do not re-run research.

### 4.8 Image prompts (after final author approval)

For every new article, automatically continue after final author approval under 4.7, unless the author explicitly declines prompts. Do not run at draft delivery, during review, or while requested edits await approval. For existing-article revisions, update affected prompts after the relevant changes are approved, or create prompts when requested.

Read and execute `$TIMBRE/skills/image-prompt/SKILL.md` in this writer session; no separate agent or dispatch. Pass the absolute `$ARTICLE`, `approved_hash` and approval reference from `review.md`, channel `SEO article`, the resolved `visual.brand` path (if any), and output `$D/image-prompts.md`. The skill checks the approved version and owns the visual selection, prompt format and output checks. If it is unavailable, report the missing path; do not claim prompts were produced.

Return the link to `$D/image-prompts.md` before ending. This creates prompts only; publishing remains separate.

---

## What This Skill Does NOT Do

- Does not write during Stage 1 under any circumstances
- Does not draft without a locked center from Stage 3
- Does not write first-person experience found in neither `dump.md` nor `author-notes.md`
- Does not let the reviewer or the humanizer edit `$ARTICLE` (the working copy) — only the writer edits
- Does not apply cuts or publish without the author's approval
- Does not draft generic output when the DNA file is missing
