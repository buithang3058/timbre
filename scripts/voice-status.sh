#!/usr/bin/env bash
set -euo pipefail

# shellcheck source=lib/voice-common.sh
source "$(dirname "${BASH_SOURCE[0]}")/lib/voice-common.sh"

THRESHOLD="${VOICE_MERGE_THRESHOLD:-5}"

VOICE="$(resolve_voice "${1:-}")"
VOICE_DIR="$VOICES_DIR/$VOICE"
CALIBRATION_FILE="$VOICE_DIR/calibration.md"
LAST_MERGE_FILE="$VOICE_DIR/.last-merge"
DNA_FILE="$VOICE_DIR/dna.md"

echo "Voice: $VOICE"

ENTRY_COUNT=0
if [ ! -f "$CALIBRATION_FILE" ]; then
  echo "Calibration entries: 0"
  echo "Calibration file: missing ($CALIBRATION_FILE)"
else
  ENTRY_COUNT="$(grep -c '^## Entry' "$CALIBRATION_FILE" 2>/dev/null || true)"
  echo "Calibration entries: $ENTRY_COUNT (total)"
fi

# .last-merge format: line 1 = ISO date, line 2 = entry count at time of merge
COUNT_AT_MERGE=0
if [ -f "$LAST_MERGE_FILE" ]; then
  LAST_MERGE_DATE="$(sed -n '1p' "$LAST_MERGE_FILE")"
  COUNT_AT_MERGE="$(sed -n '2p' "$LAST_MERGE_FILE" | tr -d '[:space:]')"
  COUNT_AT_MERGE="${COUNT_AT_MERGE:-0}"
  echo "Last merge: $LAST_MERGE_DATE (entries at merge: $COUNT_AT_MERGE)"
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

ENTRIES_SINCE_MERGE=$(( ENTRY_COUNT - COUNT_AT_MERGE ))
if [ "$ENTRIES_SINCE_MERGE" -ge "$THRESHOLD" ]; then
  echo
  echo "Merge reminder: $ENTRIES_SINCE_MERGE new entries since last merge. Run voice calibrate merge for $VOICE."
fi
