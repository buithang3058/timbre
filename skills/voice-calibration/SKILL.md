---
name: voice-calibration
description: >
  Calibration workflow for Timbre. Adds AI-ish -> Preferred -> Why ->
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

Ask the user for four fields (one message, all four): `AI-ish`, `Preferred`, `Why`, `Pattern`.

Compute the next entry number and append to `voices/<voice>/calibration.md` using the Canonical Entry Schema below:

```bash
N=$(( $(grep -c '^## Entry' voices/<voice>/calibration.md) + 1 ))
```

Show the appended entry back to the user.

## Status Workflow

Report three numbers:

```bash
wc -w voices/<voice>/dna.md
grep -c '^## Entry' voices/<voice>/calibration.md
cat voices/<voice>/.last-merge 2>/dev/null || echo "never merged"
```

Entries added since `.last-merge` line 2 = unmerged backlog. Use this before deciding whether to merge.

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
3. Run the Status Workflow above.
4. Extract repeated or high-confidence patterns.
5. Propose a concise replacement or addition to `voices/<voice>/dna.md`.
6. Show the proposed diff in chat.
7. Ask for approval.
8. Only after approval, edit `voices/<voice>/dna.md`.
9. Run `wc -w voices/<voice>/dna.md`.
10. If the DNA is over 500 words, compress before saving.
11. Write two lines to `voices/<voice>/.last-merge`:
    - Line 1: current ISO date (`date -u +%Y-%m-%d`)
    - Line 2: current total entry count from `calibration.md`

```bash
printf '%s\n%s\n' "$(date -u +%Y-%m-%d)" "$ENTRY_COUNT" > voices/<voice>/.last-merge
```

12. Validation: pick 3 random calibration entries, generate a sentence using the new DNA for each AI-ish prompt, and compare the output to the Preferred line. Warn the user if any generated output does not resemble the Preferred version — that entry may need a stronger rule in the DNA.

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
- Vague adjectives: never merge a pattern into a rule like "write naturally" or "be clear." If the merged rule cannot be tested against a sentence to produce a pass/fail, it is too abstract to promote.
