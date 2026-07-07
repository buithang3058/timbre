#!/usr/bin/env bash
# Remove the manual Timbre skill symlinks from ~/.claude/skills/.
# Run this AFTER installing the Timbre plugin, so skills load from the
# plugin instead of the symlinks (otherwise they'd double-load).
#
# Only removes symlinks whose target points into /Users/buithang/timbre/.
# gstack skills, .agents skills, and real directories are left untouched.
#
# Usage:
#   scripts/unlink-timbre-skills.sh          # dry run (default, shows what it would do)
#   scripts/unlink-timbre-skills.sh --apply  # actually remove the symlinks

set -euo pipefail

SKILLS_DIR="$HOME/.claude/skills"
TIMBRE_ROOT="/Users/buithang/timbre/"
APPLY=0
[[ "${1:-}" == "--apply" ]] && APPLY=1

[[ -d "$SKILLS_DIR" ]] || { echo "No $SKILLS_DIR — nothing to do."; exit 0; }

found=0
for link in "$SKILLS_DIR"/*; do
  [[ -L "$link" ]] || continue                       # symlinks only
  target=$(readlink "$link")
  case "$target" in
    "$TIMBRE_ROOT"*)
      found=$((found+1))
      if [[ $APPLY -eq 1 ]]; then
        rm "$link"
        echo "removed:  $(basename "$link")  ->  $target"
      else
        echo "would rm: $(basename "$link")  ->  $target"
      fi
      ;;
  esac
done

echo "---"
if [[ $found -eq 0 ]]; then
  echo "No Timbre symlinks found."
elif [[ $APPLY -eq 1 ]]; then
  echo "Removed $found Timbre symlink(s)."
else
  echo "$found Timbre symlink(s) would be removed. Re-run with --apply to do it."
fi
