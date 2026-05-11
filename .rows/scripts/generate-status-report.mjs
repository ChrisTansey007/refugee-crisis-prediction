#!/usr/bin/env node
// generate-status-report.mjs — Generate a Markdown status report from state files.

import { readFileSync, readdirSync, existsSync, writeFileSync, mkdirSync, statSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const stateDir = join(root, 'agent-os', 'state');
const tasksDir = join(root, 'agent-os', 'tasks');
const handoffsDir = join(root, 'agent-os', 'handoffs', 'active');
const blockedDir = join(root, 'agent-os', 'tasks', 'blocked');
const reportsDir = join(root, 'agent-os', 'reports', 'status');

const now = new Date().toISOString().split('T')[0];
const timestamp = new Date().toISOString();

// Read state
let systemState = {};
try { systemState = JSON.parse(readFileSync(join(stateDir, 'system-state.json'), 'utf-8')); } catch {}

let workerStatus = {};
try { workerStatus = JSON.parse(readFileSync(join(stateDir, 'worker-status.json'), 'utf-8')); } catch {}

let assignmentState = {};
try { assignmentState = JSON.parse(readFileSync(join(stateDir, 'assignment-state.json'), 'utf-8')); } catch {}

let riskRegister = {};
try { riskRegister = JSON.parse(readFileSync(join(stateDir, 'risk-register.json'), 'utf-8')); } catch {}

let milestoneState = {};
try { milestoneState = JSON.parse(readFileSync(join(stateDir, 'milestones.json'), 'utf-8')); } catch {}

// Count tasks by state
const LIFECYCLE = ['backlog', 'ready', 'claimed', 'in-progress', 'review', 'blocked', 'done'];
const taskCounts = {};
for (const folder of LIFECYCLE) {
  const fp = join(tasksDir, folder);
  taskCounts[folder] = existsSync(fp) ? readdirSync(fp).filter(f => f.endsWith('.md') && f !== 'README.md').length : 0;
}

// Count handoffs
const handoffFiles = existsSync(handoffsDir)
  ? readdirSync(handoffsDir).filter(f => f.endsWith('.md') && f !== 'README.md')
  : [];
const handoffCount = handoffFiles.length;

// Count blocked tasks
const blockedTasks = existsSync(blockedDir)
  ? readdirSync(blockedDir).filter(f => f.endsWith('.md') && f !== 'README.md')
  : [];

// Pick most recent handoffs for a quick human scan
const recentHandoffs = handoffFiles
  .map(file => ({ file, mtime: statSync(join(handoffsDir, file)).mtimeMs }))
  .sort((a, b) => b.mtime - a.mtime)
  .slice(0, 5);

// Build report
const lines = [];
lines.push(`# STATUS.md — ${now}`);
lines.push(`> Generated: ${timestamp}`);
lines.push('');
lines.push('## System');
lines.push(`- **Repo:** ${systemState.repo_name || 'N/A'}`);
lines.push(`- **Phase:** ${systemState.current_phase || 'N/A'}`);
lines.push(`- **Execution Mode:** ${assignmentState.mode || 'N/A'}`);
lines.push(`- **Last updated:** ${systemState.last_updated || 'N/A'}`);
lines.push('');
lines.push('## Task Queue');
lines.push('| State | Count |');
lines.push('|-------|-------|');
for (const folder of LIFECYCLE) {
  lines.push(`| ${folder} | ${taskCounts[folder]} |`);
}
const totalTasks = Object.values(taskCounts).reduce((a, b) => a + b, 0);
lines.push(`| **Total** | **${totalTasks}** |`);
lines.push('');
lines.push('## Workers');
lines.push('| Worker | Status | Current Task | Active Roles |');
lines.push('|--------|--------|--------------|--------------|');
const workers = workerStatus.workers || {};
for (const [name, data] of Object.entries(workers)) {
  const roles = (data.active_roles || []).join(', ') || '—';
  lines.push(`| ${name} | ${data.status || 'unknown'} | ${data.current_task || '—'} | ${roles} |`);
}
lines.push('');
lines.push('## Assignments');
const assignments = assignmentState.assignments || [];
lines.push(`- Active assignments: ${assignments.length}`);
if (assignments.length > 0) {
  for (const a of assignments) {
    lines.push(`  - ${a.task || '?'} → ${a.worker || '?'} (${a.role || '?'})`);
  }
}
lines.push('');
lines.push('## Recent Handoffs');
lines.push(`- Active handoffs: ${handoffCount}`);
if (recentHandoffs.length === 0) {
  lines.push('- None');
} else {
  for (const handoff of recentHandoffs) {
    lines.push(`- ${handoff.file}`);
  }
}
lines.push('');
lines.push('## Blocked Tasks');
lines.push(`- Blocked tasks: ${blockedTasks.length}`);
if (blockedTasks.length === 0) {
  lines.push('- None');
} else {
  for (const task of blockedTasks) {
    lines.push(`- ${task}`);
  }
}
lines.push('');
lines.push('## Risks');
const risks = riskRegister.risks || [];
lines.push(`- Total risks tracked: ${risks.length}`);
const activeRisks = risks.filter(r => r.status !== 'resolved');
if (activeRisks.length > 0) {
  for (const r of activeRisks) {
    lines.push(`  - **${r.id}:** ${r.title} (${r.likelihood}/${r.impact}) — ${r.status}`);
  }
}
lines.push('');

lines.push('## Milestones');
const milestones = milestoneState.milestones || [];
lines.push(`- Total milestones tracked: ${milestones.length}`);
if (milestones.length === 0) {
  lines.push('- None');
} else {
  for (const milestone of milestones) {
    lines.push(`  - **${milestone.id}:** ${milestone.title} — ${milestone.status}`);
  }
}
lines.push('');

const report = lines.join('\n');

// Ensure directory exists
if (!existsSync(reportsDir)) {
  mkdirSync(reportsDir, { recursive: true });
}

const outPath = join(reportsDir, `status-${now}.md`);
writeFileSync(outPath, report);
writeFileSync(join(root, 'STATUS.md'), report);
console.log(`Status report written to: STATUS.md`);
console.log(`Status report written to: agent-os/reports/status/status-${now}.md`);
console.log(report);
