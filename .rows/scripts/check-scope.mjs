#!/usr/bin/env node
// check-scope.mjs — Compare task file scope to git diff.

import { execSync } from 'child_process';
import { readFileSync, existsSync, readdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const taskDirs = ['review', 'claimed', 'in-progress', 'blocked', 'ready', 'backlog', 'done'];
const activeTaskDirs = ['review', 'claimed', 'in-progress', 'blocked'];

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--task') out.taskId = argv[++i];
    else if (!arg.startsWith('-') && !out.taskId) out.taskId = arg;
  }
  return out;
}

function findTaskFile(taskId) {
  for (const dir of taskDirs) {
    const fullDir = join(root, 'agent-os', 'tasks', dir);
    if (!existsSync(fullDir)) continue;
    const exact = join(fullDir, `${taskId}.md`);
    if (existsSync(exact)) return exact;
    for (const file of readdirSync(fullDir)) {
      if (file.startsWith(taskId) && file.endsWith('.md')) return join(fullDir, file);
    }
  }
  return null;
}

function readTaskScope(taskPath) {
  const lines = readFileSync(taskPath, 'utf8').split(/\r?\n/);
  const start = lines.findIndex(line => line.trim() === '## Files Likely Affected');
  if (start === -1) return [];
  const scope = [];
  for (let i = start + 1; i < lines.length; i += 1) {
    const line = lines[i].trim();
    if (line.startsWith('## ')) break;
    const match = line.match(/^[-*]\s+`?([^`]+)`?/);
    if (match) scope.push(match[1].trim());
  }
  return scope;
}

function gitDiffFiles() {
  const staged = execSync('git diff --name-only --cached', { cwd: root, encoding: 'utf8' }).trim();
  const unstaged = execSync('git diff --name-only', { cwd: root, encoding: 'utf8' }).trim();
  return [...new Set([...staged.split(/\r?\n/), ...unstaged.split(/\r?\n/)].filter(Boolean))];
}

function matchesScope(file, expected) {
  const normalizedFile = file.replace(/\\/g, '/');
  const normalizedExpected = expected.replace(/\\/g, '/').replace(/\*.*$/, '');
  return normalizedFile === normalizedExpected || normalizedFile.startsWith(`${normalizedExpected}/`);
}

const args = parseArgs(process.argv.slice(2));
const taskId = args.taskId;

const taskIds = taskId ? [taskId] : activeTaskDirs.flatMap(dir => {
  const fullDir = join(root, 'agent-os', 'tasks', dir);
  if (!existsSync(fullDir)) return [];
  return readdirSync(fullDir)
    .filter(file => file.endsWith('.md') && file !== 'README.md')
    .map(file => file.replace(/\.md$/, ''));
}).filter(Boolean);

if (taskIds.length === 0) {
  console.log('Scope check: no tasks found.');
  process.exit(0);
}

const diffFiles = gitDiffFiles();
let failed = 0;

for (const id of taskIds) {
  const taskPath = findTaskFile(id);
  if (!taskPath) {
    console.log(`WARN: ${id} — task file not found; skipping scope check.`);
    continue;
  }
  const scope = readTaskScope(taskPath);
  if (scope.length === 0) {
    console.log(`WARN: ${id} — no Files Likely Affected entries found.`);
    continue;
  }

  const outOfScope = diffFiles.filter(file => !scope.some(expected => matchesScope(file, expected)));
  if (outOfScope.length > 0) {
    console.log(`FAIL: ${id} — out-of-scope files:`);
    for (const file of outOfScope) console.log(`- ${file}`);
    failed += 1;
  } else {
    console.log(`PASS: ${id}`);
  }
}

if (failed > 0) process.exit(1);
console.log('Scope check passed.');
