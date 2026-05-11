#!/usr/bin/env node
// validate-task.mjs — Validate that task files contain required headings.
// Checks all task files in agent-os/tasks/ (excluding README files).

import { readFileSync, readdirSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const tasksDir = join(root, 'agent-os', 'tasks');

const REQUIRED_HEADINGS = ['Objective', 'Acceptance Criteria', 'Verification Required', 'Handoff Required'];
const READY_STATE_REQUIRED_HEADINGS = ['Related ADRs', 'Related Decisions', 'Context Snapshot'];

const RECOMMENDED_HEADINGS = ['Status', 'Execution Mode Compatibility', 'Responsible Role', 'Required Capabilities', 'Preferred Workers', 'Current Claimed Worker', 'Reassignment Allowed'];

const VALID_STATUSES = ['backlog', 'ready', 'claimed', 'in-progress', 'review', 'blocked', 'done'];

const LIFECYCLE_FOLDERS = ['backlog', 'ready', 'claimed', 'in-progress', 'review', 'blocked', 'done'];

let totalTasks = 0;
let validTasks = 0;
let invalidTasks = 0;

for (const folder of LIFECYCLE_FOLDERS) {
  const folderPath = join(tasksDir, folder);
  if (!existsSync(folderPath)) continue;

  const files = readdirSync(folderPath).filter(f => f.endsWith('.md') && f !== 'README.md');
  for (const file of files) {
    totalTasks++;
    const filePath = join(folderPath, file);
    const content = readFileSync(filePath, 'utf-8');
    const missing = REQUIRED_HEADINGS.filter(h => !content.includes(`# ${h}`) && !content.includes(`## ${h}`));
    const missingRecommended = RECOMMENDED_HEADINGS.filter(h => !content.includes(`# ${h}`) && !content.includes(`## ${h}`));
    const readyStateMissing = (folder === 'ready' || folder === 'claimed' || folder === 'in-progress' || folder === 'review' || folder === 'done')
      ? READY_STATE_REQUIRED_HEADINGS.filter(h => !content.includes(`# ${h}`) && !content.includes(`## ${h}`))
      : [];

    if (missing.length > 0 || readyStateMissing.length > 0) {
      const allMissing = [...missing, ...readyStateMissing];
      console.log(`INVALID: ${folder}/${file} — missing required headings: ${allMissing.join(', ')}`);
      invalidTasks++;
    } else {
      if (missingRecommended.length > 0) {
        console.log(`WARN: ${folder}/${file} — missing recommended headings: ${missingRecommended.join(', ')}`);
      }
      validTasks++;
    }
  }
}

console.log(`\nTask Validation Results:`);
console.log(`  Total:  ${totalTasks}`);
console.log(`  Valid:  ${validTasks}`);
console.log(`  Invalid: ${invalidTasks}`);

if (invalidTasks > 0) {
  process.exit(1);
}
