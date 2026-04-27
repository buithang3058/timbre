#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VOICES_DIR="$REPO_ROOT/voices"

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
mkdir -p "$VOICE_DIR"

if [ ! -f "$CALIBRATION_FILE" ]; then
  printf '# Calibration: %s\n' "$VOICE" > "$CALIBRATION_FILE"
fi

read -r -p "AI-ish: " AI_ISH
read -r -p "Preferred: " PREFERRED
read -r -p "Why: " WHY
read -r -p "Pattern: " PATTERN

ENTRY_COUNT="$(grep -c '^## Entry' "$CALIBRATION_FILE" 2>/dev/null || true)"
ENTRY_NUMBER=$((ENTRY_COUNT + 1))
TITLE="$(printf '%s' "$PREFERRED" | tr '\n' ' ' | sed 's/^[[:space:]]*//; s/[[:space:]]*$//; s/[#*_`\\[\\]]//g' | cut -c 1-60)"
[ -n "$TITLE" ] || TITLE="Untitled"

cat >> "$CALIBRATION_FILE" <<EOF

## Entry $ENTRY_NUMBER: $TITLE
AI-ish: $AI_ISH
Preferred: $PREFERRED
Why: $WHY
Pattern: $PATTERN
EOF

echo "Added Entry $ENTRY_NUMBER to $CALIBRATION_FILE"
