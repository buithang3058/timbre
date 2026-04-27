#!/usr/bin/env bash
# Shared setup for voice scripts. Source this file at the top of each script:
#   source "$(dirname "${BASH_SOURCE[0]}")/lib/voice-common.sh"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[1]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VOICES_DIR="$REPO_ROOT/voices"

usage_voice() {
  local script_name
  script_name="$(basename "${BASH_SOURCE[1]}")"
  echo "Usage: $script_name [voice-name]"
}

default_voice() {
  find "$VOICES_DIR" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sort | while IFS= read -r voice_dir; do
    basename "$voice_dir"
    break
  done
}

resolve_voice() {
  local voice="${1:-$(default_voice)}"
  if [ -z "${voice:-}" ]; then
    usage_voice >&2
    echo "No voice found. Create voices/<name>/ first or pass a voice name." >&2
    exit 1
  fi
  echo "$voice"
}
