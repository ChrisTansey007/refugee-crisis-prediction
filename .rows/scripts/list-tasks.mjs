#!/usr/bin/env node
// list-tasks.mjs — List task files by lifecycle state.

import { readFileSync, readdirSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const tasksDir = join(root, 'agent-os', 'tasks');

const LIFECYCLE = ['backlog', 'ready', 'claimed', 'in-progress', 'review', 'blocked', 'done'];

console.log('Task Listing');
console.log('============\n');

let total = 0;

for (const folder of LIFECYCLE) {
  const fp = join(tasksDir, folder);
  if (!existsSync(fp)) continue;
  const files = readdirSync(fp).filter(f => f.endsWith('.md') && f !== 'README.md');
  if (files.length === 0) continue;

  console.log(`## ${folder} (${files.length})`);
  for (const file of files) {
    total++;
    const content = readFileSync(join(fp, file), 'utf-8');
    const titleMatch = content.match(/^#\s+(.+)$/m);
    const roleMatch = content.match(/Responsible Role\s*\n\s*(\S+)/);
    const workerMatch = content.match(/Current Claimed Worker\s*\n\s*(\S+)/);
    const title = titleMatch ? titleMatch[1].trim() : file;
    const role = roleMatch ? roleMatch[1].trim() : '?';
    const worker = workerMatch ? workerMatch[1].trim() : 'none';
    console.log(`  - ${title}`);
    console.log(`    Role: ${role} | Worker: ${worker}`);
  }
  console.log('');
}

console.log(`Total tasks: ${total}`);
