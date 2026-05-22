# agentic-content

> **ARCHIVED** — Voice calibration has been merged into [seo-agentic](../seo-agentic/).
> Calibration data lives at `seo-agentic/resources/context/voices/bui-thang/calibration.md`.
> Scripts live at `seo-agentic/scripts/voice/`. Git history preserved here.

Voice engine for AI-assisted writing.

The repo stores a compact Writing DNA for each voice plus raw calibration cases:

```text
AI-ish -> Preferred -> Why -> Pattern
```

The calibration file is intentionally concrete. It stores examples where AI output sounded wrong, the preferred rewrite, the reason, and the reusable writing pattern.

## Structure

```text
skills/
  interviewer.md          # Interview workflow for extracting voice source material
  dna-writer.md           # Convert interview output into a <=500 word DNA file
  voice-calibration.md    # Add, review, and merge calibration entries
  content-writer.md       # Write content using DNA plus calibration status
scripts/
  voice-calibrate-add.sh  # Interactive append helper
  voice-status.sh         # Entry count, recent patterns, merge reminder
templates/
  dna-template.md
  calibration-entry.md
voices/
  bui-thang/
    dna.md
    calibration.md
```

## Requirements

- Bash and standard Unix tools.
- In Claude Code or Codex-style agents, grant shell permission when asked so skills can run `scripts/voice-calibrate-add.sh` and `scripts/voice-status.sh`.

No package manager or external dependencies are required.

## Commands

Add a calibration entry:

```bash
scripts/voice-calibrate-add.sh bui-thang
```

Check voice status:

```bash
scripts/voice-status.sh bui-thang
```

If no voice is passed, scripts use the first folder in `voices/`.

## Voice Workflow

1. Run the interview workflow from [skills/interviewer.md](skills/interviewer.md).
2. Use [skills/dna-writer.md](skills/dna-writer.md) to create `voices/<name>/dna.md`.
3. Use [skills/voice-calibration.md](skills/voice-calibration.md) whenever AI output sounds wrong.
4. Use [skills/content-writer.md](skills/content-writer.md) before drafting content.
5. When `voice-status.sh` shows 5+ entries, run the merge workflow in `voice-calibration.md`.

## Default Voice

If a command or skill does not receive a voice name, use the first folder in `voices/`.

You can record a project default in `CLAUDE.md` or `AGENTS.md`:

```text
VOICE=bui-thang
```
