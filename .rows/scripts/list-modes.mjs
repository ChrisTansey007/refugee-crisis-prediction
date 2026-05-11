#!/usr/bin/env node
// list-modes.mjs — Show current execution mode and valid modes.

import { readFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const asPath = join(root, 'agent-os', 'state', 'assignment-state.json');

const VALID_MODES = {
  'solo': 'One worker does everything. Must use human approval or automated validation for closure.',
  'multi-worker': 'Multiple workers divide work. Different worker must review.',
  'hybrid': 'One primary worker + specialized support workers. Support workers or human must review.'
};

if (!existsSync(asPath)) {
  console.log('ERROR: assignment-state.json not found.');
  process.exit(1);
}

const as = JSON.parse(readFileSync(asPath, 'utf-8'));

console.log('Execution Modes');
console.log('===============\n');
console.log(`Current mode: ${as.mode}`);
console.log(`Description: ${VALID_MODES[as.mode] || 'Unknown mode'}`);
console.log('');

console.log('Valid modes:');
for (const [mode, desc] of Object.entries(VALID_MODES)) {
  console.log(`  ${mode}: ${desc}`);
}

if (as.notes && as.notes.length > 0) {
  console.log('\nNotes:');
  as.notes.forEach(n => console.log(`  - ${n}`));
}
