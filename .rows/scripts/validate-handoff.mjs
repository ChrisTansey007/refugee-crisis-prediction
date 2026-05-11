#!/usr/bin/env node
// validate-handoff.mjs — Validate that handoff files contain required headings.

import { readFileSync, readdirSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const handoffsDir = join(root, 'agent-os', 'handoffs', 'active');

const REQUIRED_HEADINGS = ['Summary of Work', 'Files Changed', 'Evidence Produced', 'Known Issues', 'Next Steps'];

if (!existsSync(handoffsDir)) {
  console.log('No active handoffs directory found.');
  console.log('Handoff Validation: 0 total, 0 valid, 0 invalid');
  process.exit(0);
}

const files = readdirSync(handoffsDir).filter(f => f.endsWith('.md') && f !== 'README.md');

let total = 0;
let valid = 0;
let invalid = 0;

for (const file of files) {
  total++;
  const content = readFileSync(join(handoffsDir, file), 'utf-8');
  const missing = REQUIRED_HEADINGS.filter(h => !content.includes(`# ${h}`) && !content.includes(`## ${h}`));

  if (missing.length > 0) {
    console.log(`INVALID: ${file} — missing headings: ${missing.join(', ')}`);
    invalid++;
  } else {
    valid++;
  }
}

console.log(`\nHandoff Validation Results:`);
console.log(`  Total:   ${total}`);
console.log(`  Valid:   ${valid}`);
console.log(`  Invalid: ${invalid}`);

if (invalid > 0) {
  process.exit(1);
}
