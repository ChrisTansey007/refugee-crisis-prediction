#!/usr/bin/env node
// enrich-task.mjs — Add or refresh Context Snapshot for a task.

import { existsSync, readFileSync, writeFileSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');

const taskPathArg = process.argv[2];
if (!taskPathArg) {
  console.error('Usage: node scripts/enrich-task.mjs <relative-task-path>');
  process.exit(1);
}

const taskPath = join(root, taskPathArg);
if (!existsSync(taskPath)) {
  console.error(`Task file not found: ${taskPathArg}`);
  process.exit(1);
}

const projectContextPath = join(root, 'PROJECT_CONTEXT.md');
const taskContent = readFileSync(taskPath, 'utf-8');
const projectContext = existsSync(projectContextPath) ? readFileSync(projectContextPath, 'utf-8') : '';

function getSection(content, heading) {
  const escaped = heading.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const pattern = new RegExp(`^## ${escaped}\\s*$([\\s\\S]*?)(?=^## |\\Z)`, 'm');
  const match = content.match(pattern);
  return match ? match[1].trim() : '';
}

function bullets(text) {
  return text
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line.startsWith('- '))
    .map((line) => line.slice(2).trim())
    .filter(Boolean);
}

const objective = getSection(taskContent, 'Objective').replace(/\s+/g, ' ').trim();
const dependencies = bullets(getSection(taskContent, 'Dependencies'));
const requiredReading = bullets(getSection(taskContent, 'Required Reading'));
const relatedAdrs = bullets(getSection(taskContent, 'Related ADRs'));
const relatedDecisions = bullets(getSection(taskContent, 'Related Decisions'));

const firstProjectConstraint = bullets(getSection(projectContext, 'Active Constraints'))[0] || 'No distilled project constraints recorded yet.';
const why = objective || 'Task objective not yet filled.';
const timestamp = new Date().toISOString();

const snapshot = [
  '## Context Snapshot',
  '',
  '> Fill this before moving the task to `ready/`. Keep it short enough for a worker to load quickly.',
  '',
  '### Why This Task Exists',
  '',
  why,
  '',
  '### Key Decisions',
  '',
  ...(relatedAdrs.length || relatedDecisions.length ? [...relatedAdrs, ...relatedDecisions].map((line) => `- ${line}`) : ['- None recorded yet.']),
  '',
  '### Key Constraints',
  '',
  `- ${firstProjectConstraint}`,
  '',
  '### Upstream Facts',
  '',
  ...(dependencies.length ? dependencies.map((line) => `- ${line}`) : ['- No upstream task dependencies recorded.']),
  '',
  '### Required Context Links',
  '',
  ...(requiredReading.length ? requiredReading.map((line) => `- ${line}`) : ['- [PROJECT_GOAL.md](../../PROJECT_GOAL.md) — baseline project intent']),
  '',
  '### Snapshot Freshness',
  '',
  `- **Generated/updated:** ${timestamp}`,
  '- **Source versions:** manual',
  '- **Needs refresh if:** related ADRs, decisions, dependencies, or project context change',
  ''
].join('\n');

let next = taskContent;
if (/^## Context Snapshot$/m.test(taskContent)) {
  next = taskContent.replace(/^## Context Snapshot[\s\S]*?(?=^## |\Z)/m, snapshot);
} else {
  next = taskContent.replace(/^## Objective/m, `${snapshot}\n## Objective`);
}

writeFileSync(taskPath, next);
console.log(`Enriched ${taskPathArg}`);
