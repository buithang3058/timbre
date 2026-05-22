'use strict';

const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execSync } = require('child_process');
const { countEntries, parseEntries, formatEntry } = require('../scripts/lib/extract-lib');

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`  ✓ ${name}`);
    passed++;
  } catch (err) {
    console.error(`  ✗ ${name}`);
    console.error(`    ${err.message}`);
    failed++;
  }
}

function withTempDir(fn) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'extract-test-'));
  try {
    fn(dir);
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

// ---------------------------------------------------------------------------
// countEntries
// ---------------------------------------------------------------------------

console.log('\ncountEntries');

test('returns 0 when file does not exist', () => {
  assert.strictEqual(countEntries('/nonexistent/calibration.md'), 0);
});

test('returns 0 for empty file', () => {
  withTempDir(dir => {
    const f = path.join(dir, 'calibration.md');
    fs.writeFileSync(f, '# Calibration: test\n');
    assert.strictEqual(countEntries(f), 0);
  });
});

test('counts existing entries correctly', () => {
  withTempDir(dir => {
    const f = path.join(dir, 'calibration.md');
    fs.writeFileSync(f, '# Calibration\n\n## Entry 1: A\nAI-ish: x\n\n## Entry 2: B\nAI-ish: y\n');
    assert.strictEqual(countEntries(f), 2);
  });
});

// ---------------------------------------------------------------------------
// parseEntries
// ---------------------------------------------------------------------------

console.log('\nparseEntries');

const VALID_EXTRACTION = `AI-ish: So DeFi does not make you safer. Understanding the order does.
Preferred: DeFi thuc su hap dan khi ban hieu dung.
Why: The AI version ends on a compressed slogan. The preferred is natural and positive.
Pattern: Avoid sentence-final slogans. End on a fact or natural observation instead.

AI-ish: This is a game-changer for your workflow.
Preferred: This cuts the correction loop in half.
Why: "Game-changer" is vague. The preferred gives a specific, measurable claim.
Pattern: Replace vague superlatives with a specific outcome or number.`;

test('parses two valid entries', () => {
  const entries = parseEntries(VALID_EXTRACTION);
  assert.strictEqual(entries.length, 2);
});

test('entry fields are correctly extracted', () => {
  const entries = parseEntries(VALID_EXTRACTION);
  assert.ok(entries[0].aiIsh.includes('Understanding the order'));
  assert.ok(entries[0].preferred.includes('hap dan'));
  assert.ok(entries[0].why.includes('slogan'));
  assert.ok(entries[0].pattern.includes('sentence-final'));
});

test('returns empty array for too-similar message', () => {
  const entries = parseEntries('Input pair too similar for meaningful extraction.');
  assert.strictEqual(entries.length, 0);
});

test('skips malformed blocks missing a field', () => {
  const incomplete = `AI-ish: Something
Preferred: Better thing
Why: Because reasons
`;
  const entries = parseEntries(incomplete);
  assert.strictEqual(entries.length, 0);
});

// ---------------------------------------------------------------------------
// formatEntry
// ---------------------------------------------------------------------------

console.log('\nformatEntry');

test('formats with correct fields', () => {
  const entry = { aiIsh: 'Old', preferred: 'New', why: 'Because', pattern: 'Do X instead.' };
  const out = formatEntry(3, 'My title', entry);
  assert.ok(out.includes('## Entry 3: My title'));
  assert.ok(out.includes('AI-ish: Old'));
  assert.ok(out.includes('Preferred: New'));
  assert.ok(out.includes('Why: Because'));
  assert.ok(out.includes('Pattern: Do X instead.'));
});

test('entry number sequence is sequential from prior total', () => {
  withTempDir(dir => {
    const f = path.join(dir, 'calibration.md');
    fs.writeFileSync(f, '# Calibration\n\n## Entry 1: First\nAI-ish: a\nPreferred: b\nWhy: c\nPattern: d\n');
    const startN = countEntries(f) + 1;
    assert.strictEqual(startN, 2);

    const entry = { aiIsh: 'a2', preferred: 'b2', why: 'c2', pattern: 'd2' };
    const formatted = formatEntry(startN, 'Second', entry);
    fs.appendFileSync(f, formatted + '\n');

    assert.strictEqual(countEntries(f), 2);
    assert.ok(fs.readFileSync(f, 'utf-8').includes('## Entry 2: Second'));
  });
});

// ---------------------------------------------------------------------------
// CLI error paths (subprocess)
// ---------------------------------------------------------------------------

console.log('\nCLI error paths');

const scriptPath = path.join(__dirname, '..', 'scripts', 'extract-pairs.js');

test('missing args → usage message, exit 1', () => {
  try {
    execSync(`node ${scriptPath}`, { encoding: 'utf-8', env: { ...process.env, ANTHROPIC_API_KEY: 'x' } });
    assert.fail('should have exited with code 1');
  } catch (err) {
    assert.ok(err.stderr.includes('Usage:') || err.stdout.includes('Usage:'));
  }
});

test('missing API key → clear error, exit 1', () => {
  const env = { ...process.env };
  delete env.ANTHROPIC_API_KEY;
  try {
    execSync(
      `node ${scriptPath} --voice bui-thang --ai-draft /dev/null --preferred /dev/null --next-draft /dev/null`,
      { encoding: 'utf-8', env }
    );
    assert.fail('should have exited with code 1');
  } catch (err) {
    assert.ok((err.stderr + err.stdout).includes('ANTHROPIC_API_KEY'));
  }
});

test('unknown voice → clear error, exit 1', () => {
  try {
    execSync(
      `node ${scriptPath} --voice no-such-voice --ai-draft /dev/null --preferred /dev/null --next-draft /dev/null`,
      { encoding: 'utf-8', env: { ...process.env, ANTHROPIC_API_KEY: 'x' } }
    );
    assert.fail('should have exited with code 1');
  } catch (err) {
    assert.ok((err.stderr + err.stdout).includes('Voice directory not found'));
  }
});

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------

console.log(`\n${passed} passed, ${failed} failed`);
if (failed > 0) process.exit(1);
