#!/usr/bin/env node
// validate-decisions.mjs — Validate ADR/decision file consistency.

import { readFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');

const REQUIRED_ADRS = [
  'docs/02-architecture/decisions/ADR-0001-repo-orchestrated-worker-system.md',
  'docs/02-architecture/decisions/ADR-0002-template-fork-workflow.md',
  'docs/02-architecture/decisions/ADR-0003-flexible-worker-assignment.md'
];

let errors = 0;

// Check required ADR files exist
for (const adr of REQUIRED_ADRS) {
  if (!existsSync(join(root, adr))) {
    console.log(`ERROR: Required ADR file missing: ${adr}`);
    errors++;
  }
}

// Read decision register
const registerPath = join(root, 'agent-os', 'state', 'decision-register.json');
if (!existsSync(registerPath)) {
  console.log('ERROR: decision-register.json not found');
  process.exit(1);
}

let register;
try {
  register = JSON.parse(readFileSync(registerPath, 'utf-8'));
} catch (e) {
  console.log(`ERROR: Invalid JSON in decision-register.json: ${e.message}`);
  process.exit(1);
}

const decisions = register.decisions || [];

// Check each decision's file reference exists
for (const d of decisions) {
  if (!d.file) {
    console.log(`ERROR: Decision ${d.adr || '?'} has no file reference`);
    errors++;
    continue;
  }
  if (!existsSync(join(root, d.file))) {
    console.log(`ERROR: Decision ${d.adr} references missing file: ${d.file}`);
    errors++;
  }
}

// Check all required ADRs are in the register
const registeredAdrs = decisions.map(d => d.adr);
for (const adr of REQUIRED_ADRS) {
  const adrId = adr.match(/ADR-\d+/)?.[0];
  if (adrId && !registeredAdrs.includes(adrId)) {
    console.log(`WARN: ${adrId} exists but is not in decision-register.json`);
  }
}

// Check blocker-sourced decisions point to blocker files.
for (const decision of decisions.filter((d) => String(d.adr || '').startsWith('BLOCKER-'))) {
  if (!String(decision.file || '').startsWith('agent-os/blockers/')) {
    console.log(`ERROR: Blocker decision ${decision.adr} must point to agent-os/blockers/, got ${decision.file}`);
    errors++;
  }
}

console.log(`\nDecision Validation Results:`);
console.log(`  Errors: ${errors}`);

if (errors > 0) {
  process.exit(1);
}
