#!/usr/bin/env node
// list-capabilities.mjs — List all capabilities from the capability registry.

import { readFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const registryPath = join(root, 'agent-os', 'state', 'capability-registry.json');

if (!existsSync(registryPath)) {
  console.log('ERROR: capability-registry.json not found.');
  process.exit(1);
}

const registry = JSON.parse(readFileSync(registryPath, 'utf-8'));
const capabilities = registry.capabilities || {};

console.log('Capability Registry');
console.log('===================\n');

for (const [name, data] of Object.entries(capabilities)) {
  console.log(`## ${name}`);
  console.log(`  Description:      ${data.description}`);
  console.log(`  Preferred Workers: ${(data.preferred_workers || []).join(', ')}`);
  console.log(`  Common Roles:     ${(data.common_roles || []).join(', ')}`);
  console.log(`  Evidence Expected: ${data.evidence_expected}`);
  console.log('');
}

console.log(`Total capabilities: ${Object.keys(capabilities).length}`);
