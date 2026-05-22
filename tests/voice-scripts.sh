#!/usr/bin/env bash
# Plain-shell tests for voice-calibrate-add.sh and voice-status.sh.
# Runs each case in an isolated temp VOICES_DIR.
set -euo pipefail

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../scripts" && pwd)"
PASSED=0
FAILED=0

pass() { echo "  ✓ $1"; PASSED=$((PASSED + 1)); }
fail() { echo "  ✗ $1"; echo "    $2"; FAILED=$((FAILED + 1)); }

with_voice_dir() {
  # Usage: with_voice_dir <voice> <fn>
  local voice="$1"
  local fn="$2"
  local tmpdir
  tmpdir="$(mktemp -d)"
  export VOICES_DIR="$tmpdir"
  mkdir -p "$tmpdir/$voice"
  "$fn" "$tmpdir" "$voice"
  rm -rf "$tmpdir"
  unset VOICES_DIR
}

# ---------------------------------------------------------------------------
# voice-calibrate-add.sh
# ---------------------------------------------------------------------------

echo ""
echo "voice-calibrate-add.sh"

test_creates_header_when_no_calibration_file() {
  local tmpdir="$1" voice="$2"
  local cal="$tmpdir/$voice/calibration.md"

  printf 'ai draft line\npreferred line\nbecause reasons\ndo X instead\n' \
    | bash "$SCRIPTS_DIR/voice-calibrate-add.sh" "$voice" >/dev/null 2>&1

  if [ -f "$cal" ] && grep -q "^# Calibration:" "$cal"; then
    pass "creates calibration.md with header when file missing"
  else
    fail "creates calibration.md with header when file missing" "header not found in $cal"
  fi
}
with_voice_dir testvoice test_creates_header_when_no_calibration_file

test_entry_count_increments_correctly() {
  local tmpdir="$1" voice="$2"
  local cal="$tmpdir/$voice/calibration.md"

  printf 'ai1\npref1\nwhy1\npattern1\n' \
    | bash "$SCRIPTS_DIR/voice-calibrate-add.sh" "$voice" >/dev/null 2>&1
  printf 'ai2\npref2\nwhy2\npattern2\n' \
    | bash "$SCRIPTS_DIR/voice-calibrate-add.sh" "$voice" >/dev/null 2>&1

  local count
  count="$(grep -c '^## Entry' "$cal" 2>/dev/null || echo 0)"
  if [ "$count" -eq 2 ]; then
    pass "entry count increments correctly after multiple adds"
  else
    fail "entry count increments correctly after multiple adds" "expected 2, got $count"
  fi
}
with_voice_dir testvoice test_entry_count_increments_correctly

# ---------------------------------------------------------------------------
# voice-status.sh
# ---------------------------------------------------------------------------

echo ""
echo "voice-status.sh"

test_status_no_calibration_file() {
  local tmpdir="$1" voice="$2"

  local output
  output="$(bash "$SCRIPTS_DIR/voice-status.sh" "$voice" 2>&1)"

  if echo "$output" | grep -q "missing"; then
    pass "shows 'missing' when no calibration file"
  else
    fail "shows 'missing' when no calibration file" "output was: $output"
  fi
}
with_voice_dir testvoice test_status_no_calibration_file

test_status_no_last_merge_file() {
  local tmpdir="$1" voice="$2"
  local cal="$tmpdir/$voice/calibration.md"
  printf '# Calibration: %s\n' "$voice" > "$cal"

  local output
  output="$(bash "$SCRIPTS_DIR/voice-status.sh" "$voice" 2>&1)"

  if echo "$output" | grep -q "First run"; then
    pass "shows 'First run' when no .last-merge file"
  else
    fail "shows 'First run' when no .last-merge file" "output was: $output"
  fi
}
with_voice_dir testvoice test_status_no_last_merge_file

test_status_below_threshold_no_reminder() {
  local tmpdir="$1" voice="$2"
  local cal="$tmpdir/$voice/calibration.md"
  local merge="$tmpdir/$voice/.last-merge"

  # 3 entries total, merge at 2 → 1 since merge, threshold default 5
  {
    printf '# Calibration: %s\n' "$voice"
    printf '\n## Entry 1: a\nAI-ish: x\nPreferred: y\nWhy: z\nPattern: w\n'
    printf '\n## Entry 2: b\nAI-ish: x\nPreferred: y\nWhy: z\nPattern: w\n'
    printf '\n## Entry 3: c\nAI-ish: x\nPreferred: y\nWhy: z\nPattern: w\n'
  } > "$cal"
  printf '2026-01-01\n2\n' > "$merge"

  local output
  output="$(bash "$SCRIPTS_DIR/voice-status.sh" "$voice" 2>&1)"

  if ! echo "$output" | grep -q "Merge reminder"; then
    pass "no merge reminder when entries since merge below threshold"
  else
    fail "no merge reminder when entries since merge below threshold" "unexpected reminder in: $output"
  fi
}
with_voice_dir testvoice test_status_below_threshold_no_reminder

test_status_at_threshold_shows_reminder() {
  local tmpdir="$1" voice="$2"
  local cal="$tmpdir/$voice/calibration.md"
  local merge="$tmpdir/$voice/.last-merge"

  # 5 entries total, merge at 0 → 5 since merge = at threshold (default 5)
  {
    printf '# Calibration: %s\n' "$voice"
    for i in 1 2 3 4 5; do
      printf '\n## Entry %s: x\nAI-ish: a\nPreferred: b\nWhy: c\nPattern: d\n' "$i"
    done
  } > "$cal"
  printf '2026-01-01\n0\n' > "$merge"

  local output
  output="$(bash "$SCRIPTS_DIR/voice-status.sh" "$voice" 2>&1)"

  if echo "$output" | grep -q "Merge reminder"; then
    pass "shows merge reminder when entries since merge at threshold"
  else
    fail "shows merge reminder when entries since merge at threshold" "output was: $output"
  fi
}
with_voice_dir testvoice test_status_at_threshold_shows_reminder

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

echo ""
echo "$PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ]
