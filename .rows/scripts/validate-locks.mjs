#!/usr/bin/env node
// validate-locks.mjs — Validate lock JSON files in agent-os/locks/.

import { readFileSync, readdirSync, existsSync, writeFileSync, mkdirSync } from 'fs';
import { join, dirname, relative } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const locksDir = join(root, 'agent-os', 'locks');

const REQUIRED_FIELDS = ['task_id', 'worker', 'created_at'];

if (!existsSync(locksDir)) {
  console.log('No locks directory found.');
  process.exit(0);
}

const lockFiles = readdirSync(locksDir).filter(f => f.endsWith('.json') && f !== 'lock-template.json');

if (lockFiles.length === 0) {
  console.log('Lock Validation: No active locks.');
  process.exit(0);
}

let valid = 0;
let invalid = 0;
let expired = 0;
const issues = [];

for (const file of lockFiles) {
  const filePath = join(locksDir, file);
  let lock;
  try {
    lock = JSON.parse(readFileSync(filePath, 'utf-8'));
  } catch (e) {
    issues.push({ file, issue: `Invalid JSON: ${e.message}` });
    invalid++;
    continue;
  }

  const missing = REQUIRED_FIELDS.filter(f => !lock[f]);
  if (missing.length > 0) {
    issues.push({ file, issue: `Missing fields: ${missing.join(', ')}` });
    invalid++;
    continue;
  }

  // Check expiration
  if (lock.expires_at) {
    const expires = new Date(lock.expires_at);
    if (expires < new Date()) {
      issues.push({ file, issue: `Expired at ${lock.expires_at}` });
      expired++;
    }
  }

  valid++;
}

// Write report
const reportsDir = join(root, 'agent-os', 'reports', 'locks');
if (!existsSync(reportsDir)) mkdirSync(reportsDir, { recursive: true });

const now = new Date().toISOString().split('T')[0];
const report = [
  `# Lock Validation Report — ${now}`,
  `> Generated: ${new Date().toISOString()}`,
  '',
  `- Total locks: ${lockFiles.length}`,
  `- Valid: ${valid}`,
  `- Invalid: ${invalid}`,
  `- Expired: ${expired}`,
  '',
  issues.length > 0 ? '## Issues' : '## No issues found.',
  ...issues.map(i => `- \`${i.file}\`: ${i.issue}`),
  ''
].join('\n');

writeFileSync(join(reportsDir, `locks-${now}.md`), report);

console.log(`\nLock Validation Results:`);
console.log(`  Total:   ${lockFiles.length}`);
console.log(`  Valid:   ${valid}`);
console.log(`  Invalid: ${invalid}`);
console.log(`  Expired: ${expired}`);

if (invalid > 0) {
  process.exit(1);
}
