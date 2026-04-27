---
name: content-writer
description: >
  Writes content using a selected voice's compact DNA and calibration status.
  Runs voice status before drafting and keeps output aligned with the DNA.
---

# Content Writer

Use this when the user asks:

```text
content write "<topic>"
content write "<topic>" --voice <voice>
write this in <voice>'s voice
```

If no voice is specified, use the first folder in `voices/`.

## Required Context

Read:

```text
voices/<voice>/dna.md
```

Run:

```bash
scripts/voice-status.sh <voice>
```

If `voice-status.sh` reports 5+ calibration entries, tell the user the voice is ready for `voice calibrate merge`, but do not block writing unless the user asks to merge first.

## Optional Context

Read recent calibration entries when the user asks for a stricter voice match or when the topic is close to previous calibration examples:

```text
voices/<voice>/calibration.md
```

Prefer the DNA over raw calibration if they conflict.

## Drafting Workflow

1. Clarify the format only if missing and risky:
   - article
   - newsletter
   - LinkedIn post
   - tweet/thread
   - script
   - landing page copy
2. Load the DNA.
3. Run `voice-status.sh`.
4. Draft the content.
5. Self-review against the DNA:
   - Does the opening sound like the voice?
   - Did any sentence become slogan-like?
   - Are examples concrete enough?
   - Did the ending give a useful decision, pattern, or implication?
6. Revise once before showing the user.

## Output Contract

Return only the drafted content plus a short note if calibration status matters.

Do not explain every DNA rule you applied unless the user asks.

## When the User Corrects the Draft

If the user says a line sounds AI-ish or rewrites a sentence:

1. Ask for the preferred version if they did not provide it.
2. Convert the correction into:

```text
AI-ish:
Preferred:
Why:
Pattern:
```

3. Run `scripts/voice-calibrate-add.sh <voice>` when interactive shell is appropriate, or append the entry manually after confirming the fields.
