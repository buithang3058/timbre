---
name: voice-dna-writer
description: >
  Converts a voice interview transcript into a compact Writing DNA file.
  Enforces the 500-word DNA limit by checking and compressing the output.
---

# DNA Writer

Use this when the user asks for `voice dna create <voice>`, `voice dna update <voice>`, or `voice dna test <voice>`.

The DNA is the small source-of-truth file used while writing. It must stay at 500 words or fewer.

## Inputs

Required:

```text
voices/<voice>/interview.md
templates/dna-template.md
```

Optional:

```text
voices/<voice>/calibration.md
voices/<voice>/dna.md
```

If `<voice>` is missing, use the first folder in `voices/`.

## Create or Update Workflow

1. Read `voices/<voice>/interview.md`.
2. Read the existing `voices/<voice>/dna.md` if present.
3. Read `templates/dna-template.md`.
4. Extract only durable voice rules:
   - how the voice frames problems
   - sentence rhythm and preferred structure
   - words, tones, and moves to avoid
   - example style
   - calibration patterns that should affect future writing
5. Write `voices/<voice>/dna.md`.
6. Run:

```bash
wc -w voices/<voice>/dna.md
```

7. If the count is over 500 words, compress and check again before finishing.

## DNA Quality Bar

Good DNA:

- Uses concrete rules, not vague adjectives.
- Includes "Always" and "Never" sections.
- Describes rhythm, openings, closings, and transitions.
- Keeps raw examples out unless they are short and reusable.
- Separates the main DNA from calibration history.

Bad DNA:

- Says only "clear, direct, human, natural."
- Copies the whole interview.
- Adds long philosophy that will drown out writing instructions.
- Uses generic brand voice language.

## Test Workflow

Use this when the user asks for `voice dna test <voice>`.

1. Read `voices/<voice>/dna.md`.
2. Write three short samples in different formats:
   - one explanatory paragraph
   - one direct social post
   - one correction of an AI-ish sentence
3. Ask the user which line feels wrong.
4. Convert corrections into calibration entries with `voice calibrate add`.

## Output

After create or update:

```text
DNA saved: voices/<voice>/dna.md
Word count: <N>/500
Next: voice dna test <voice>
```
