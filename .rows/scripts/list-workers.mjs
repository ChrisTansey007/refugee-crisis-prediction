#!/usr/bin/env node
// list-workers.mjs — List worker statuses from worker-status.json.

import { readFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const wsPath = join(root, 'agent-os', 'state', 'worker-status.json');

if (!existsSync(wsPath)) {
  console.log('ERROR: worker-status.json not found.');
  process.exit(1);
}

const ws = JSON.parse(readFileSync(wsPath, 'utf-8'));
const workers = ws.workers || {};

console.log('Worker Status');
console.log('=============\n');
console.log('| Worker | Status | Current Task | Active Roles | Best For |');
console.log('|--------|--------|--------------|--------------|----------|');

for (const [name, data] of Object.entries(workers)) {
  const roles = (data.active_roles || []).join(', ') || '—';
  const task = data.current_task || '—';
  console.log(`| ${name} | ${data.status || '?'} | ${task} | ${roles} | ${data.best_for || '?'} |`);
}

console.log(`\nTotal workers: ${Object.keys(workers).length}`);
