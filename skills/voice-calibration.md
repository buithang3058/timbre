---
name: voice-calibration
description: >
  Calibration workflow for agentic-content. Adds AI-ish -> Preferred -> Why ->
  Pattern entries, reviews accumulated entries, and merges durable patterns into DNA.
---

# Voice Calibration

Use this for:

```text
voice calibrate add <voice>
voice calibrate review <voice>
voice calibrate merge <voice>
voice status <voice>
```

If `<voice>` is missing, use the first folder in `voices/`.

## Add Workflow

Run:

```bash
scripts/voice-calibrate-add.sh <voice>
```

The script prompts for four fields:

1. `AI-ish`
2. `Preferred`
3. `Why`
4. `Pattern`

It appends to:

```text
voices/<voice>/calibration.md
```

If shell access is unavailable, tell the user to run the command manually and paste the result.

## Status Workflow

Run:

```bash
scripts/voice-status.sh <voice>
```

Use the output before content writing and before deciding whether to merge.

## Review Workflow

1. Read `voices/<voice>/calibration.md`.
2. Group entries by repeated or related `Pattern:` lines.
3. Identify:
   - patterns that appear more than once
   - one-off corrections that are still strong
   - contradictions that need the user's judgment
4. Show a short review:

```text
Strong patterns:
- <pattern> [entries: 1, 4, 6]

Possible contradictions:
- <pattern A> vs <pattern B>

Not ready to merge:
- <pattern>
```

Do not modify files during review.

## Merge Workflow

Merge means converting raw calibration cases into durable DNA rules. The AI proposes the diff. The user approves before the file changes.

1. Read `voices/<voice>/dna.md`.
2. Read `voices/<voice>/calibration.md`.
3. Run `scripts/voice-status.sh <voice>`.
4. Extract repeated or high-confidence patterns.
5. Propose a concise replacement or addition to `voices/<voice>/dna.md`.
6. Show the proposed diff in chat.
7. Ask for approval.
8. Only after approval, edit `voices/<voice>/dna.md`.
9. Run `wc -w voices/<voice>/dna.md`.
10. If the DNA is over 500 words, compress before saving.
11. Write the current ISO date to:

```text
voices/<voice>/.last-merge
```

## Canonical Entry Schema

```markdown
## Entry {N}: {short title}
AI-ish: {sentence AI wrote}
Preferred: {sentence user prefers}
Why: {short explanation}
Pattern: {reusable rule}
```

## Merge Judgment

Promote a pattern into DNA when:

- It appears in multiple calibration entries.
- It explains a correction the user clearly cares about.
- It changes generation behavior, not just wording.
- It is short enough to survive in the 500-word DNA.

Do not promote:

- Topic-specific one-offs.
- Rules that contradict the existing DNA without asking.
- Long examples that belong in `calibration.md`.
