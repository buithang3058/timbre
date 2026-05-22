---
name: content-seo
description: >
  4-stage perception-first SEO article workflow. Human captures insight before AI
  writes anything. Stages: Perception Dump → Research → Center of Gravity → Draft.
  Supports Pillar and Cluster content tiers for topic cluster architecture.
  Invoke as /content-seo [project] where project is diverfi | tokemist | simplize | motquacam.
---

# Content SEO — 4-Stage Workflow

## Project → DNA Path Mapping

| Project   | DNA Path                    |
|-----------|-----------------------------|
| diverfi   | `voices/bui-thang/dna.md`  |
| tokemist  | `voices/tokemist/dna.md`   |
| simplize  | `voices/simplize/dna.md`   |
| motquacam | `voices/motquacam/dna.md`  |

## Step 0 — Project Selection + DNA Check

If the user invoked `/content-seo [project]`, use that project. If no project argument, ask:

> "Which project is this content for? diverfi / tokemist / simplize / motquacam"

Wait for answer before proceeding.

Look up the DNA path from the mapping table above. Check if the file exists.

**If DNA file is missing — hard stop:**

```
DNA file not found: voices/[project]/dna.md

This skill requires a voice DNA file to draft in your style. Run:
  /dna-writer [project]
Then retry /content-seo [project].
```

Do NOT proceed to Stage 1. Do not offer to draft without DNA.

If DNA file exists — read it silently. If the DNA has a Content Hubs section, extract the hub names and hold them in context for Stage 1. If the DNA has no hub structure, note that HUB field is optional for this project.

Also read these files silently:

**Voice calibration (all projects):**
- `voices/bui-thang/calibration.md` — AI-ish vs. preferred sentence pairs; apply these patterns when drafting
- `voices/bui-thang/bad-almost-good.md` — 12 patterns that sound good but are generic; use the Global Detection Rules when evaluating every sentence in Stage 4

**Crypto jargon rules (diverfi and tokemist only):**
- `voices/bui-thang/crypto.md` — jargon hard rules; keep all crypto/DeFi terms in English, add short Vietnamese explanation on first use

**SEO and quality references:**
- `references/eeat-framework.md` — E-E-A-T signals and YMYL requirements
- `references/google-seo-reference.md` — Google quality signals and structured data
- `references/quality-gates.md` — minimum word counts, title/meta requirements, internal linking
- `skills/content-seo/references/instructions-detail.md` — CORE-EEAT 16 constraints and SEO self-check workflow; apply in Stage 4 quality check
- `skills/content-seo/references/title-formulas.md` — title formula matrix and CTR modifiers; use to generate 2-3 title options in quality snapshot
- `skills/content-seo/references/content-structure-templates.md` — format blueprints; confirm required sections match FORMAT before drafting

Do not summarize or confirm any of these to the user. Hold as context for Stage 4. Proceed to Stage 1.

---

## Stage 1 — Perception Dump (Human only, NO AI)

Output this template exactly and STOP. Do not write anything else. Do not fill in any field. Do not offer examples or suggestions:

```
TOPIC: [topic]
PROJECT: [project]
HUB: [hub name — use the hub list from this project's DNA; omit if project has no hub structure]
TARGET READER: [ai họ là, đang làm gì, đang nghĩ gì ngay lúc này]
CONTENT TIER: [Pillar | Cluster]
PILLAR URL: [URL của pillar page — bắt buộc nếu CONTENT TIER = Cluster; bỏ trống nếu Pillar]
CLUSTER PAGES: [danh sách cluster pages liên quan — bắt buộc nếu CONTENT TIER = Pillar; bỏ trống nếu Cluster]

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

HUB is **invalid** if blank AND the project's DNA has a hub structure. If blank but DNA has hubs, infer the hub from the topic and confirm with user. If the project's DNA has no hub structure, HUB field is optional — skip HUB validation entirely.

TARGET READER is **invalid** if fewer than 10 words or still template text.

CONTENT TIER is **invalid** if blank or not one of: Pillar, Cluster. If CONTENT TIER = Cluster, PILLAR URL must not be blank. If CONTENT TIER = Pillar, CLUSTER PAGES may be blank at this stage (can be filled in later). Hold the CONTENT TIER value — it drives word count target and linking rules in Stage 4.

A field is **invalid** if:
- It contains the literal template text unchanged (e.g., still says "What do people get wrong about this?" with no answer)
- It is fewer than 10 words

If any field fails — list the offending field numbers and re-present the gate:

> "Fields [X] and [Y] are too short or unchanged. Please fill these in and paste your full dump again."

Do not proceed until all 5 fields pass.

### Stage 1 Quality Reflection Gate

After all 5 fields pass validation, reflect Stage 1 back to the user as one sentence per field:

```
Here's what I heard from your Perception Dump:
1. [one-sentence summary of field 1]
2. [one-sentence summary of field 2]
3. [one-sentence summary of field 3]
4. [one-sentence summary of field 4]
5. [one-sentence summary of field 5]

Does this accurately reflect what you wrote? Reply 'yes' to continue to Stage 2,
or correct any field that was misread.
```

**STOP. Wait for confirmation before running Stage 2.**

---

## Stage 2 — Research

Goal: find real evidence for the human's perception dump. Pattern miner only — not author.

**If `/research` was run in this conversation:** Its `[RESEARCH OUTPUT]` block is Stage 2. Skip the AI-only analysis below. Go directly to the gate prompt.

**If `/research` was NOT run:** Run the AI-only analysis below. Recommend the user run `/research` after this session for the next article — it produces keyword intent data and primary source verification that AI inference cannot.

### AI-Only Fallback (when /research not run)

**Important:** Output must begin with:

> "[Context-only inference from training data — verify before publishing. Do not treat as retrieved fact, especially for DeFi claims, statistics, or specific case studies.]"

Run all 4 prompts automatically. Do not ask the user which ones to run.

**Field mapping:**
- Field 1 → Where is this misconception most visible? What specific behavior reveals it?
- Field 2 → What's the delayed consequence most people miss? What behavior correlates with failure?
- Field 3 → What evidence supports this? When does it break down?
- Fields 4-5 → What case challenges or sharpens this? What mechanism is underneath?

**Output format — raw bullets only. No prose paragraphs. No headers. No "here is the research summary" framing:**

```
FIELD 1:
- [bullet: misconception + where it appears]
- [bullet: mechanism or case]

FIELD 2:
- [bullet: delayed consequence]
- [bullet: correlated behavior]

FIELD 3:
- [bullet: supporting evidence]
- [bullet: breakdown condition]

FIELDS 4-5:
- [bullet: challenging case]
- [bullet: mechanism underneath]
```

**Gate prompt (Stage 2 → 3):**

> "Stage 2 done. Does anything here change or sharpen your perception dump? If the evidence is thin or generic, reply 'skip — proceed to center.' Otherwise, add corrections. Before continuing, save these research notes to your local note."

**STOP. Wait for: corrections / "proceed" / "skip — proceed to center".**

---

## Stage 3 — Center of Gravity Selection

Goal: identify what the article is REALLY about before any draft.

### Step 3a — Generate from Perception Dump only

Generate 4 options from Stage 1 Perception Dump only. Do not use research output at this step.

```
Given the Perception Dump fields 1-5, generate 4 versions of the center of gravity —
what this article is REALLY about. Go from obvious to mechanism-level:

1. Surface topic: restate the topic from Stage 1 verbatim
2. Weak center: the obvious angle any writer would take
3. Stronger center: a mechanism or tension visible in fields 3-4
4. Strongest center: the underlying insight that explains WHY — the thing
   that makes everything else make sense

Output as 4 labeled bullets. One sentence each. No explanation.
```

Then ask:

> "Which of these is closest to what you want to say? Or write your own. Don't lock yet."

**STOP. Wait for the human to indicate direction.**

**Fallback:** If the human says the generated center feels generic — skip the 4 options and ask directly:

> "Write your own center of gravity in one sentence — what is this article REALLY about at the mechanism level?"

### Step 3b — Research as challenger

Present the COVERAGE MAP and READER AWARENESS STAGE from Stage 2 research. Ask one question:

> "Research shows [awareness stage] readers and these uncovered questions: [coverage map NOT in dump items]. Does this sharpen, challenge, or confirm the center direction you indicated?"

**STOP. Wait for response. Human decides — research does not override center direction.**

**Gate prompt (Stage 3 → 4):**

The approved center is locked when the human completes: "This article is really about ___."

Say:

> "Center locked. Copy this sentence to your local note before we continue: '[approved center sentence]'"

Hold the approved center in conversation context. It is the constraint for Stage 4 — the draft must serve this center, not the surface topic.

---

## Stage 4 — Draft → Cut → Discovery Loop

### Draft

**Word count target — set before writing the first sentence:**
- **Pillar page:** 3,000–5,000 words. Broad topic coverage. All Tier 1 semantic entities must appear. All required sections for informational articles must be present.
- **Cluster page:** 1,000–2,000 words. Deep, focused on one sub-topic. Link back to the Pillar URL from PILLAR URL field.

Count as you go — if you reach the end of the main body before the lower bound of your tier target, expand existing sections (more mechanism, more examples, more concrete detail) before writing FAQ and conclusion. Do not pad with filler sentences — expand with real content that serves the center and covers Tier 1 semantic entities.

Draft from:
- The approved center from Stage 3
- Evidence and patterns from Stage 2
- The voice DNA loaded in Step 0
- Calibration pairs from `calibration.md` — prefer the "Preferred" sentence patterns

Write continuously. Do not pause to evaluate sentences against patterns while drafting.

The draft must serve the center. The center determines HOW to explain each entity — not WHICH entities to include. All Tier 1 semantic entities from the SEMANTIC ENTITY MAP must appear in the draft; frame each through the approved center's perspective. A Tier 1 entity that seems tangential to the center still gets 1-2 sentences — do not omit it.

**Semantic entity coverage:** Review the SEMANTIC ENTITY MAP from Stage 2 research. For each Tier 1 entity — confirm it is addressed in the draft. For Tier 2 — include if it fits the center's framing; skip only if genuinely unrelated. Tier 3 — optional; include only if center touches them naturally.

**Entity-section mapping (before writing, map each Tier 1 entity to one section type):**

| Entity type | Default section |
|---|---|
| Definitional concept (what X is) | Định nghĩa |
| Process / how it works | Cơ chế |
| Property / trait (immutability, decentralization…) | Đặc điểm |
| Benefit / value for reader | Lợi ích |
| Real-world use case | Ứng dụng thực tế |
| Risk / failure mode | Ưu và nhược điểm |
| Comparison vs incumbent | So sánh |

Map each Tier 1 entity to a section before drafting. If an entity maps to a section that is not in the required sections list — add that section. Do not leave Tier 1 entities unanchored. The approved center determines HOW to explain the entity within its assigned section — not whether to include it.

**Logical Chain Test (apply after entity-section mapping):** For each Tier 1 entity, ask: "Is this entity in the logical chain leading to the approved center?" If yes → explain fully in its section. If no → reduce to 1-2 sentences (mention-only); do not remove entirely.

**Coverage check (reader comprehension):** Review the COVERAGE MAP from Stage 2 research. For questions marked "NOT in dump" — include if they serve the approved center's framing. If a question is important but the center frames it differently, answer it from the center's angle rather than skipping it.

**Informational article required sections ("X là gì" format):** If the topic is definitional — "X là gì", "X hoạt động như thế nào", "X là gì và tại sao quan trọng" — these sections are ALL required before FAQ:
1. Định nghĩa (definition — what it is)
2. Cơ chế (mechanism — how it works, step by step)
3. Đặc điểm / Tính chất (properties / characteristics — the key traits that define it, e.g., immutability, decentralization, transparency, trustless)
4. Lợi ích (benefits — concrete advantages for the reader)
5. Ưu và nhược điểm (pros and cons — honest tradeoffs, not just benefits)
6. So sánh (comparison — vs the system readers already know: bank, centralized exchange, etc.)
7. Ứng dụng thực tế (use cases — 2-3 concrete examples, not exhaustive)

Do not skip sections 3, 4, or 5. These are the sections most missing when drafting from a 5-field Perception Dump, because the dump captures INSIGHTS about the topic, not the full topic scope a reader needs to understand it completely.

**Hook rule:** Hook must start from where the TARGET READER is right now — their current behavior, current assumption, current situation — not from the article's conclusion or the center. Read the hub audience profile in the DNA before writing the first sentence. A beginner reader on an exchange should not encounter a scenario that assumes they already have MetaMask.

**Key Takeaways block:** Immediately after the hook, add a Key Takeaways block with 3-5 bullet points. Each bullet = one concrete, specific insight — not a teaser or article summary. The block gives readers who skim the core of what they need to know. Takeaways must serve the approved center, not describe the article structure.

**Image suggestions:** After the draft, propose 3-5 image placements using this format: `[Section: name | Size: WxH | Subject: what to show | Alt: descriptive text]`. Place images where they reduce cognitive load or anchor an abstract concept. Do not embed HTML — comment block only.

  Standard sizes: Wide infographic/comparison = **1200×628px** (Open Graph compatible). Multi-row table = **800×600px**. Photo illustration = **1200×800px**. Format: WebP primary, JPEG fallback, max 200KB.

  **Image file naming rule:** Tên file phải bằng tiếng Việt không dấu, khoảng trắng thay bằng dấu `-`. Thứ tự ưu tiên: (1) phù hợp với section đặt ảnh, (2) từ khoá SEO. Ví dụ: `proof-of-work-va-co-che-bao-ve-bitcoin.webp`. Thêm tên file vào mỗi image prompt theo format: `Filename: [ten-file].webp`.

  **Brand alignment:** Before writing image prompts, check if a brand.md exists for the project. For tokemist: `/Users/buithang/tokemist/resouces/Context/brand.md`. Apply brand colors, typography, and visual style to all prompts — do not use generic white-background clean design unless brand specifies it.

### Quality Check (run after presenting draft)

Present the draft first. Then run this check and append results below the draft.

**Voice check (from calibration.md + bad-almost-good.md):**
- Apply the Global Detection Rules (10 questions) from bad-almost-good.md to the draft as a whole. Flag paragraphs that fail — do not self-correct.
- If a flag is ambiguous ("this smells AI but unclear why"), consult the pattern bank in bad-almost-good.md to identify which pattern it matches. Name the pattern.
- Check calibration pairs: flag instances of slogan closings, meta-narration, announce-importance setup sentences, theatrical bucket brigade at argument openings, symmetrical insight. Do not rewrite — list each flag with the offending sentence.

**E-E-A-T (from eeat-framework.md):**
- Crypto/finance content is YMYL — highest E-E-A-T standards apply
- Does the draft include Experience signals from Stage 1? (first-hand observations, specific details that couldn't be fabricated)
- Are claims accurate and sourced, or labeled as context-only inference?
- No generic AI phrasing — every paragraph should trace to Stage 1 perceptions or Stage 2 evidence

**Quality gates (from quality-gates.md):**
- Word count target is tier-dependent (set in Stage 1):
  - Pillar: 3,000–5,000 words minimum
  - Cluster: 1,000–2,000 words
- Note the word count and the CONTENT TIER.
- If below the lower bound: **hard flag** — do not present draft as complete. Identify which sections need expansion (more mechanism, more examples, deeper FAQ) and expand before presenting. Do not pad — expand with real content that serves the center.

**SEO structure (from content-structure-templates.md + instructions-detail.md):**
- Check that FORMAT matches a blueprint in content-structure-templates.md. Verify required sections are present (e.g., blog post needs: intro, definition block, why it matters, FAQ, conclusion).
- TOC: if draft has 3+ H2 sections, add a TOC after the hook (CORE-EEAT O08).
- Summary box: add a TL;DR or key takeaways block near the top if the article is 1,000+ words (CORE-EEAT O02).
- FAQ section: add at the end if the topic covers 3+ related query variants (CORE-EEAT C03). Use 40-60 word answers.

  **FAQ writing protocol — judgment questions (run before writing each Q&A):**
  Before keeping a question, ask:
  1. *Ai đang hỏi câu này — người chưa đọc bài hay người vừa đọc xong?* → Nếu người chưa đọc bài: reframe thành decision/edge case hoặc cắt. FAQ phục vụ người vừa đọc xong.
  2. *Câu trả lời có thể tìm nguyên văn trong bài không?* → Nếu có: cắt hoặc reframe thành một góc khác (decision, edge case, threshold, scenario).
  3. *Câu đầu tiên của câu trả lời có phải là direct answer không?* → Không được có setup sentence. Câu đầu = answer. Câu sau = context tối thiểu.
  4. *Câu hỏi này connect về center của bài không?* → Nếu tangential: cắt dù GEO value cao.
  5. *Câu trả lời có liên quan đến mất tài sản / rủi ro tài chính không?* → Nếu có: thêm YMYL nuance (custodial vs non-custodial distinction, "không có ngoại lệ", v.v.).

  Target: 5-7 questions, mỗi câu trả lời 60-100 từ. Questions = decision questions hoặc edge cases, không phải definition questions.
- Primary keyword placement: must appear in H1, within the first 150 words, in at least one H2, and in the conclusion (CORE-EEAT C01, C02).
- Definition blocks: inline term definitions should be 40-60 words on first use.
- Links — tier-aware:
  - **Cluster page:** propose 1 internal link back to the PILLAR URL (from Stage 1 dump) + 1-2 links to related cluster pages. Use 2-3 external authoritative sources from Stage 2.
  - **Pillar page:** propose 3-5 internal links to existing or planned cluster pages (use placeholder URLs if cluster pages don't exist yet). Use 2-3 external authoritative sources from Stage 2.
  - (CORE-EEAT R02)

**Semantic Coverage Audit (from SEMANTIC ENTITY MAP in Stage 2):**
- If /research was run: list all Tier 1 entities and check each — present in draft (✓) or missing (✗)?
- If any Tier 1 entity is missing: flag it and note which section it would fit in. Do not add it silently.
- If Semantic Entity Map had MEDIUM or LOW confidence: note this in the quality snapshot.
- If /research was NOT run (AI-only Stage 2): skip this audit — no Semantic Entity Map available.

**After presenting the draft, append this block:**

```
--- QUALITY SNAPSHOT ---
Content tier: [Pillar | Cluster]
Word count: [N] words ([meets target | below lower bound — flag for expansion])
  Target: Pillar 3,000–5,000 / Cluster 1,000–2,000
E-E-A-T signals present: [list 2-3 specific experience signals from Stage 1 found in draft]
YMYL flags: [any claims that need verification before publishing]

Semantic coverage:
- Tier 1 entities present: [list] ✓
- Tier 1 entities missing: [list] ← flag for redraft
- Confidence: [HIGH | MEDIUM | LOW | N/A — /research not run]

Title options (from title-formulas.md):
1. [formula type] — "[title]" ([N] chars)
2. [formula type] — "[title]" ([N] chars)
3. [formula type] — "[title]" ([N] chars)

Meta description (120-160 chars): [description with primary keyword + value prop + implicit CTA]

SEO structure check:
- TOC: [added / not needed — fewer than 3 H2s]
- Summary box: [added / flagged missing]
- FAQ section: [added / flagged missing]
- Primary keyword in H1: [yes / no]
- Primary keyword in first 150 words: [yes / no]
- Internal links:
  - Cluster → Pillar: [link to PILLAR URL included: yes / no]
  - Cluster → related clusters: [N links proposed]
  - Pillar → cluster pages: [N links proposed]
- External citations: [N included]

Image suggestions:
- [Section: [section name] | Subject: [what to show] | Alt: [descriptive text]]
- (3-5 suggestions; prioritize abstract concepts and comparisons that benefit from visual)
```

### Cut Sequence

After the quality snapshot, propose specific cuts labeled by anti-pattern. Do NOT self-apply cuts — list each one and wait for the human to approve, reject, or modify each cut individually.

Cut targets (label each proposed cut with the pattern name):

| Pattern | Description |
|---------|-------------|
| Meta-narration | "In this article...", "This post will..." |
| Setup sentences | Anything before the actual hook |
| Packaged wisdom | Generic insights that aren't specific to the human's perception |
| Explain-too-early | Conclusion appears before tension is built |
| Fake cadence | Rhythm added to feel deep, not to carry meaning |

### Discovery Check

After cuts, ask the human:

> "What is this article REALLY saying? Where is the actual gravity? Which insight might be fake-smart? Which paragraph is merely discourse?"

### Loop

After each cut-and-discover cycle, ask:

> "Is this draft done, or do you want another cut pass?"

- If **"done"**: present the final draft. Exit.
- If **"re-center"** (or any explicit signal that the center has shifted): re-present the Stage 3 sharpening sequence with the new center candidate. Stage 2 research output is preserved — do not re-run it.
- Otherwise: run another cut pass.

There is no iteration cap. Loop until the human exits.

---

## What This Skill Does NOT Do

- Does not write during Stage 1 under any circumstances
- Does not proceed to Stage 2 until quality reflection is confirmed
- Does not draft without an approved center from Stage 3
- Does not self-apply cuts — human confirms each one
- Does not draft generic output when DNA file is missing
