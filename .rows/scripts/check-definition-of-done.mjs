#!/usr/bin/env node
// check-definition-of-done.mjs — Check that tasks in review/ or a specific task have handoff and verification references.

import { readFileSync, readdirSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const taskDirs = ['review', 'claimed', 'in-progress', 'blocked', 'ready', 'backlog', 'done'];
const handoffsDir = join(root, 'agent-os', 'handoffs', 'active');
const verificationDir = join(root, 'agent-os', 'reports', 'verification');

function findTask(taskId) {
  for (const dir of taskDirs) {
    const taskDir = join(root, 'agent-os', 'tasks', dir);
    if (!existsSync(taskDir)) continue;
    const exact = join(taskDir, `${taskId}.md`);
    if (existsSync(exact)) return exact;
    for (const file of readdirSync(taskDir)) {
      if (file.startsWith(taskId) && file.endsWith('.md')) return join(taskDir, file);
    }
  }
  return null;
}

const taskArg = process.argv.slice(2).find(arg => !arg.startsWith('-'));
const reviewDir = join(root, 'agent-os', 'tasks', 'review');

let taskFiles = [];
if (taskArg) {
  const found = findTask(taskArg);
  if (!found) {
    console.log(`DoD Check: task ${taskArg} not found.`);
    process.exit(1);
  }
  taskFiles = [found];
} else {
  if (!existsSync(reviewDir)) {
    console.log('No review directory found.');
    console.log('DoD Check: 0 tasks in review');
    process.exit(0);
  }
  taskFiles = readdirSync(reviewDir)
    .filter(f => f.endsWith('.md') && f !== 'README.md')
    .map(f => join(reviewDir, f));
}

if (taskFiles.length === 0) {
  console.log('DoD Check: No tasks in review.');
  process.exit(0);
}

const handoffFiles = existsSync(handoffsDir) ? readdirSync(handoffsDir).filter(f => f.endsWith('.md') && f !== 'README.md') : [];
const verificationFiles = existsSync(verificationDir) ? readdirSync(verificationDir).filter(f => f.endsWith('.md') && f !== 'README.md') : [];

let passed = 0;
let failed = 0;

for (const taskPath of taskFiles) {
  const content = readFileSync(taskPath, 'utf-8');
  const taskFile = taskPath.split('/').pop();
  const taskId = taskFile.replace('.md', '');
  const issues = [];

  const hasHandoffRef = handoffFiles.some(h => h.startsWith(taskId));
  if (!hasHandoffRef) {
    issues.push('No handoff found in handoffs/active/');
  }

  const hasVerificationRef = verificationFiles.some(v => v.includes(taskId));
  if (!hasVerificationRef) {
    issues.push('No verification report found in reports/verification/');
  }

  if (!content.includes('Acceptance Criteria')) {
    issues.push('Missing Acceptance Criteria section');
  }

  if (!content.includes('Handoff Required')) {
    issues.push('Missing Handoff Required section');
  }

  const claimedMatch = content.match(/Current [Cc]laimed [Ww]orker[\s\S]*?\n([^\n]+)/);
  if (claimedMatch) {
    const claimedWorker = claimedMatch[1].trim();
    if (claimedWorker.toLowerCase() !== 'none') {
      console.log(`WARN: ${taskId} — Task in review but claimed by ${claimedWorker}. Ensure reviewer is different.`);
    }
  }

  if (issues.length > 0) {
    console.log(`FAIL: ${taskId} — ${issues.join('; ')}`);
    failed++;
  } else {
    console.log(`PASS: ${taskId}`);
    passed++;
  }
}

console.log(`\nDefinition of Done Check:`);
console.log(`  Tasks checked: ${taskFiles.length}`);
console.log(`  Passed: ${passed}`);
console.log(`  Failed: ${failed}`);

if (failed > 0) {
  process.exit(1);
}
