#!/usr/bin/env node
// agentctl.mjs — ROWS Agent Control Script
// Prints available commands and system information.

import { readFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');

console.log('========================================');
console.log('  ROWS — Repo-Orchestrated Worker System');
console.log('  Agent Control (agentctl)');
console.log('========================================\n');

// System state
const statePath = join(root, 'agent-os', 'state', 'system-state.json');
if (existsSync(statePath)) {
  const state = JSON.parse(readFileSync(statePath, 'utf-8'));
  console.log('System State:');
  console.log(`  Repo:        ${state.repo_name}`);
  console.log(`  Phase:       ${state.current_phase}`);
  console.log(`  Tasks:       ${state.active_task_count} active`);
  console.log(`  Updated:     ${state.last_updated}`);
  console.log(`  Notes:       ${state.notes}\n`);
}

// Assignment state
const assignmentPath = join(root, 'agent-os', 'state', 'assignment-state.json');
if (existsSync(assignmentPath)) {
  const assignment = JSON.parse(readFileSync(assignmentPath, 'utf-8'));
  console.log('Execution Mode:');
  console.log(`  Mode:        ${assignment.mode}`);
  console.log(`  Workers:     ${(assignment.active_workers || []).join(', ') || 'none'}`);
  console.log(`  Assignments: ${(assignment.assignments || []).length} active\n`);
}

console.log('Available Commands:');
console.log('  npm run audit                  Full audit of all checks');
console.log('  npm run validate:json          Validate all JSON files');
console.log('  npm run validate:tasks         Validate task files');
console.log('  npm run validate:handoffs      Validate handoff files');
console.log('  npm run validate:assignments   Validate assignment state');
console.log('  npm run validate:decisions     Validate ADR/decision files');
console.log('  npm run validate:links         Check for broken links');
console.log('  npm run validate:placeholders  Audit placeholder usage');
console.log('  npm run validate:locks         Validate lock files');
console.log('  npm run validate:template      Check template readiness');
console.log('  npm run validate:agent-os      Run all validations');
console.log('  npm run status:generate        Generate status report');
console.log('  npm run assignments:report     Generate assignment report');
console.log('  npm run check:dod              Check definition of done');
console.log('  npm run list:tasks             List tasks by state');
console.log('  npm run list:workers           List worker statuses');
console.log('  npm run list:capabilities      List all capabilities');
console.log('  npm run list:modes             Show current execution mode');
console.log('');
console.log('Direct Scripts:');
console.log('  node scripts/claim-task.mjs                Claim a task from ready/');
console.log('  node scripts/move-task.mjs                 Move a task between folders');
console.log('  node scripts/validate-task.mjs             Validate task structure');
console.log('  node scripts/validate-handoff.mjs          Validate handoff structure');
console.log('  node scripts/validate-assignments.mjs      Validate assignment state');
console.log('  node scripts/validate-decisions.mjs        Validate ADR/decision files');
console.log('  node scripts/validate-links.mjs            Check broken links');
console.log('  node scripts/validate-placeholders.mjs     Audit placeholders');
console.log('  node scripts/validate-locks.mjs            Validate lock files');
console.log('  node scripts/validate-template-readiness.mjs Check template readiness');
console.log('  node scripts/list-capabilities.mjs         List all capabilities');
console.log('  node scripts/list-tasks.mjs                List tasks');
console.log('  node scripts/list-workers.mjs              List workers');
console.log('  node scripts/list-modes.mjs                Show execution mode');
console.log('  node scripts/audit-agent-os.mjs            Run comprehensive audit');
console.log('  node scripts/generate-assignment-report.mjs Generate assignment report');
console.log('');
console.log('Execution Modes: solo | multi-worker | hybrid');
console.log('Assignment: capability → role → preferred worker → active worker');
console.log('Task Lifecycle: backlog → ready → claimed → in-progress → review → done');
console.log('For full documentation, see AGENTS.md and agent-os/README.md');
console.log('');
console.log('New in v0.3.0: prompt-library/, examples/, template readiness checks');
