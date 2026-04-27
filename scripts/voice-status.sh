#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VOICES_DIR="$REPO_ROOT/voices"
THRESHOLD="${VOICE_MERGE_THRESHOLD:-5}"

usage() {
  echo "Usage: $0 [voice-name]"
}

default_voice() {
  find "$VOICES_DIR" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sort | while IFS= read -r voice_dir; do
    basename "$voice_dir"
    break
  done
}

VOICE="${1:-$(default_voice)}"
if [ -z "${VOICE:-}" ]; then
  usage >&2
  echo "No voice found. Create voices/<name>/ first or pass a voice name." >&2
  exit 1
fi

VOICE_DIR="$VOICES_DIR/$VOICE"
CALIBRATION_FILE="$VOICE_DIR/calibration.md"
LAST_MERGE_FILE="$VOICE_DIR/.last-merge"
DNA_FILE="$VOICE_DIR/dna.md"

echo "Voice: $VOICE"

if [ ! -f "$CALIBRATION_FILE" ]; then
  echo "Calibration entries: 0"
  echo "Calibration file: missing ($CALIBRATION_FILE)"
else
  ENTRY_COUNT="$(grep -c '^## Entry' "$CALIBRATION_FILE" 2>/dev/null || true)"
  echo "Calibration entries: $ENTRY_COUNT"
fi

if [ -f "$LAST_MERGE_FILE" ]; then
  LAST_MERGE="$(sed -n '1p' "$LAST_MERGE_FILE")"
  echo "Last merge: $LAST_MERGE"
else
  echo "Last merge: First run - no prior merge"
fi

if [ -f "$DNA_FILE" ]; then
  DNA_WORDS="$(wc -w < "$DNA_FILE" | tr -d ' ')"
  echo "DNA words: $DNA_WORDS/500"
  if [ "$DNA_WORDS" -gt 500 ]; then
    echo "DNA warning: over 500 words. Compress before using for generation."
  fi
else
  echo "DNA words: missing ($DNA_FILE)"
fi

if [ -f "$CALIBRATION_FILE" ]; then
  echo
  echo "Recent patterns:"
  grep '^Pattern:' "$CALIBRATION_FILE" | tail -5 | sed 's/^Pattern:[[:space:]]*/- /' || true
fi

ENTRY_COUNT="${ENTRY_COUNT:-0}"
if [ "$ENTRY_COUNT" -ge "$THRESHOLD" ]; then
  echo
  echo "Merge reminder: $ENTRY_COUNT entries found. Run voice calibrate merge for $VOICE."
fi
