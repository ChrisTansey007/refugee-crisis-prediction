#!/usr/bin/env node
// generate-assignment-report.mjs — Generate assignment summary report.

import { readFileSync, existsSync, writeFileSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const stateDir = join(root, 'agent-os', 'state');

let assignmentState = {};
let workerStatus = {};
let capabilityRegistry = {};

try { assignmentState = JSON.parse(readFileSync(join(stateDir, 'assignment-state.json'), 'utf-8')); } catch {}
try { workerStatus = JSON.parse(readFileSync(join(stateDir, 'worker-status.json'), 'utf-8')); } catch {}
try { capabilityRegistry = JSON.parse(readFileSync(join(stateDir, 'capability-registry.json'), 'utf-8')); } catch {}

const now = new Date().toISOString().split('T')[0];
const timestamp = new Date().toISOString();

const lines = [];
lines.push(`# Assignment Report — ${now}`);
lines.push(`> Generated: ${timestamp}`);
lines.push('');

// Execution mode
lines.push('## Execution Mode');
lines.push(`- **Mode:** ${assignmentState.mode || 'N/A'}`);
lines.push(`- **Assignment model:** capability → role → preferred worker → active worker`);
lines.push('');

// Active workers
lines.push('## Active Workers');
const workers = workerStatus.workers || {};
const activeWorkers = Object.entries(workers).filter(([, d]) => d.status === 'active' || d.current_task);
if (activeWorkers.length === 0) {
  lines.push('- No active workers.');
} else {
  lines.push('| Worker | Status | Current Task | Roles |');
  lines.push('|--------|--------|--------------|-------|');
  for (const [name, data] of activeWorkers) {
    const roles = (data.active_roles || []).join(', ') || '—';
    lines.push(`| ${name} | ${data.status} | ${data.current_task || '—'} | ${roles} |`);
  }
}
lines.push('');

// Current assignments
lines.push('## Current Assignments');
const assignments = assignmentState.assignments || [];
if (assignments.length === 0) {
  lines.push('- No active assignments.');
} else {
  for (const a of assignments) {
    lines.push(`- **${a.task || '?'}** → ${a.worker || '?'} (${a.role || '?'})`);
  }
}
lines.push('');

// Reassignment policy
lines.push('## Reassignment Policy');
const policy = assignmentState.reassignment_policy || {};
lines.push(`- Allow reassignment: ${policy.allow_reassignment ? 'Yes' : 'No'}`);
lines.push(`- Require handoff before reassignment: ${policy.require_handoff_before_reassignment ? 'Yes' : 'No'}`);
lines.push(`- Allow human override: ${policy.allow_human_override ? 'Yes' : 'No'}`);
lines.push(`- Allow stale lock recovery: ${policy.allow_stale_lock_recovery ? 'Yes' : 'No'}`);
lines.push(`- Require new lock after reassignment: ${policy.require_new_lock_after_reassignment ? 'Yes' : 'No'}`);
lines.push('');

// Capability summary
lines.push('## Capability Summary');
const caps = capabilityRegistry.capabilities || {};
lines.push(`- Total capabilities: ${Object.keys(caps).length}`);
lines.push('');

// Worker availability
lines.push('## Worker Availability');
lines.push('| Worker | Status | Best For |');
lines.push('|--------|--------|----------|');
for (const [name, data] of Object.entries(workers)) {
  lines.push(`| ${name} | ${data.status || '?'} | ${data.best_for || '?'} |`);
}
lines.push('');

const report = lines.join('\n');

const reportsDir = join(root, 'agent-os', 'reports', 'assignments');
if (!existsSync(reportsDir)) mkdirSync(reportsDir, { recursive: true });

const outPath = join(reportsDir, `assignment-report-${now}.md`);
writeFileSync(outPath, report);
console.log(`Assignment report written to: agent-os/reports/assignments/assignment-report-${now}.md`);
console.log(report);
