#!/usr/bin/env node
// validate-assignments.mjs — Validate assignment-state.json and worker-status.json consistency.

import { readFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const stateDir = join(root, 'agent-os', 'state');

const VALID_MODES = ['solo', 'multi-worker', 'hybrid'];

let errors = 0;
let warnings = 0;

// Read assignment state
let assignmentState = null;
try {
  assignmentState = JSON.parse(readFileSync(join(stateDir, 'assignment-state.json'), 'utf-8'));
} catch (e) {
  console.log('ERROR: Failed to parse assignment-state.json:', e.message);
  process.exit(1);
}

// Validate mode
if (!VALID_MODES.includes(assignmentState.mode)) {
  console.log(`ERROR: Invalid mode "${assignmentState.mode}". Must be one of: ${VALID_MODES.join(', ')}`);
  errors++;
}

// Validate reassignment_policy
const policy = assignmentState.reassignment_policy || {};
if (typeof policy.allow_reassignment !== 'boolean') {
  console.log('WARN: reassignment_policy.allow_reassignment is missing or not boolean');
  warnings++;
}

// Read worker status
let workerStatus = null;
try {
  workerStatus = JSON.parse(readFileSync(join(stateDir, 'worker-status.json'), 'utf-8'));
} catch (e) {
  console.log('ERROR: Failed to parse worker-status.json:', e.message);
  process.exit(1);
}

const workers = workerStatus.workers || {};

// Check that active_workers in assignment state reference known workers
const activeWorkers = assignmentState.active_workers || [];
for (const w of activeWorkers) {
  if (!workers[w]) {
    console.log(`WARN: Active worker "${w}" not found in worker-status.json`);
    warnings++;
  }
}

// Check each worker has required fields
for (const [name, data] of Object.entries(workers)) {
  if (!data.status) {
    console.log(`WARN: Worker "${name}" has no status field`);
    warnings++;
  }
  if (!data.active_roles) {
    console.log(`WARN: Worker "${name}" has no active_roles field`);
    warnings++;
  }
  if (!data.best_for) {
    console.log(`WARN: Worker "${name}" has no best_for field`);
    warnings++;
  }
}

// Check assignments array
const assignments = assignmentState.assignments || [];
for (const a of assignments) {
  if (!a.task) {
    console.log('WARN: Assignment missing task field');
    warnings++;
  }
  if (!a.worker) {
    console.log('WARN: Assignment missing worker field');
    warnings++;
  }
}

console.log(`\nAssignment Validation Results:`);
console.log(`  Errors:   ${errors}`);
console.log(`  Warnings: ${warnings}`);

if (errors > 0) {
  process.exit(1);
}
