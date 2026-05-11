#!/usr/bin/env node
// claim-task.mjs — Validate and assist with task claiming.
// Usage: node scripts/claim-task.mjs TASK-XXXX [worker-name]

import { readFileSync, existsSync, readdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const readyDir = join(root, 'agent-os', 'tasks', 'ready');
const locksDir = join(root, 'agent-os', 'locks');

const taskId = process.argv[2];
const worker = process.argv[3] || 'unknown';

if (!taskId) {
  console.log('Usage: node scripts/claim-task.mjs <TASK-XXXX> [worker-name]');
  console.log('Example: node scripts/claim-task.mjs TASK-0002 codex');
  process.exit(1);
}

// Check if task exists in ready/
const taskFile = join(readyDir, `${taskId}.md`);
if (!existsSync(taskFile)) {
  // Also check if it might be in another folder
  const LIFECYCLE = ['backlog', 'ready', 'claimed', 'in-progress', 'review', 'blocked', 'done'];
  for (const folder of LIFECYCLE) {
    const altFile = join(root, 'agent-os', 'tasks', folder, `${taskId}.md`);
    if (existsSync(altFile)) {
      console.log(`ERROR: Task ${taskId} is in ${folder}/, not ready/.`);
      console.log('Tasks must be in ready/ before they can be claimed.');
      process.exit(1);
    }
  }
  console.log(`ERROR: Task ${taskId} not found in agent-os/tasks/ready/`);
  console.log('Tasks must be in ready/ before they can be claimed.');
  console.log('Available tasks in ready/:');
  const readyTasks = readdirSync(readyDir).filter(f => f.endsWith('.md') && f !== 'README.md');
  if (readyTasks.length === 0) {
    console.log('  (none)');
  } else {
    readyTasks.forEach(t => console.log(`  ${t}`));
  }
  process.exit(1);
}

// Read task content and check for assignment fields
const taskContent = readFileSync(taskFile, 'utf-8');
const warnings = [];

if (!taskContent.includes('Required Capabilities') && !taskContent.includes('Required capabilities')) {
  warnings.push('WARNING: Task has no Required Capabilities section. Capability-based routing requires this.');
}
if (!taskContent.includes('Context Snapshot')) {
  warnings.push('WARNING: Task has no Context Snapshot section. Enrich it before claiming.');
}
if (!taskContent.includes('Preferred Workers') && !taskContent.includes('Preferred workers')) {
  warnings.push('WARNING: Task has no Preferred Workers section.');
}
if (!taskContent.includes('Current Claimed Worker') && !taskContent.includes('Current claimed worker')) {
  warnings.push('WARNING: Task has no Current Claimed Worker section.');
}
if (!taskContent.includes('Reassignment Allowed') && !taskContent.includes('Reassignment allowed')) {
  warnings.push('WARNING: Task has no Reassignment Allowed section.');
}

// Check if already claimed
const currentClaimedMatch = taskContent.match(/Current [Cc]laimed [Ww]orker[\s\S]*?\n([^\n]+)/);
if (currentClaimedMatch && currentClaimedMatch[1].trim().toLowerCase() !== 'none') {
  warnings.push(`WARNING: Task appears to already be claimed by: ${currentClaimedMatch[1].trim()}`);
}

if (warnings.length > 0) {
  console.log('Pre-claim warnings:');
  warnings.forEach(w => console.log(`  ${w}`));
  console.log('');
}

// Check for conflicting locks
const lockFiles = readdirSync(locksDir).filter(f => f.endsWith('.json') && f !== 'lock-template.json');
if (lockFiles.length > 0) {
  console.log('Existing locks found:');
  for (const lf of lockFiles) {
    const lock = JSON.parse(readFileSync(join(locksDir, lf), 'utf-8'));
    console.log(`  ${lf}: task=${lock.task_id}, worker=${lock.claimed_by}, expires=${lock.expires_at}`);
  }
  console.log('\nCheck for conflicts before proceeding.');
}

console.log(`Task ${taskId} is available in ready/.`);
console.log('To claim this task:');
console.log(`1. Verify capability fit against agent-os/state/capability-registry.json`);
console.log(`2. Move agent-os/tasks/ready/${taskId}.md → agent-os/tasks/claimed/`);
console.log(`3. Create a lock file in agent-os/locks/ using lock-template.json`);
console.log(`4. Update agent-os/state/worker-status.json with your status and active_roles`);
console.log(`5. Refresh the task's Context Snapshot if it is stale or missing`);
console.log(`6. Update the task file's Current claimed worker field`);
console.log(`7. Create a branch: agent/${worker}/${taskId.toLowerCase()}-short-description`);
console.log(`8. Move task from claimed/ to in-progress/ and begin work`);
