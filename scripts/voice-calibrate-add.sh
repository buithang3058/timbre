#!/usr/bin/env bash
set -euo pipefail

# shellcheck source=lib/voice-common.sh
source "$(dirname "${BASH_SOURCE[0]}")/lib/voice-common.sh"

VOICE="$(resolve_voice "${1:-}")"
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

# Use printf with explicit format to prevent shell expansion of user-supplied values
printf '\n## Entry %s: %s\nAI-ish: %s\nPreferred: %s\nWhy: %s\nPattern: %s\n' \
  "$ENTRY_NUMBER" "$TITLE" "$AI_ISH" "$PREFERRED" "$WHY" "$PATTERN" \
  >> "$CALIBRATION_FILE"

echo "Added Entry $ENTRY_NUMBER to $CALIBRATION_FILE"
