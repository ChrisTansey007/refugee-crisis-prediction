#!/usr/bin/env node
// validate-startup-consistency.mjs — Check startup-sequence doc references and adapter drift.

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const startupDoc = join(root, 'agent-os', 'startup-sequence.md');
const agentsPath = join(root, 'AGENTS.md');
const adapterPaths = [
  join(root, 'CLAUDE.md'),
  join(root, 'GEMINI.md'),
  join(root, 'HERMES.md')
];

const failures = [];

if (!existsSync(startupDoc)) {
  failures.push('Missing canonical doc: agent-os/startup-sequence.md');
}

function read(file) {
  try {
    return readFileSync(file, 'utf-8');
  } catch {
    return '';
  }
}

const agents = read(agentsPath);
if (!agents.includes('startup-sequence.md')) {
  failures.push('AGENTS.md does not reference agent-os/startup-sequence.md');
}
if (!agents.includes('knowledge-model.md')) {
  failures.push('AGENTS.md does not reference agent-os/knowledge-model.md');
}

for (const file of adapterPaths) {
  const text = read(file);
  if (!text.includes('startup-sequence.md')) {
    failures.push(`${file.replace(root + '/', '')} does not reference agent-os/startup-sequence.md`);
  }
  if (text.includes('Read these files in order before taking any action:') && !text.includes('startup-sequence.md')) {
    failures.push(`${file.replace(root + '/', '')} still restates startup steps instead of linking to the canonical doc`);
  }
}

const reportsDir = join(root, 'agent-os', 'reports', 'startup-consistency');
if (!existsSync(reportsDir)) mkdirSync(reportsDir, { recursive: true });
const now = new Date().toISOString().split('T')[0];
const report = [
  `# Startup Consistency Report — ${now}`,
  `> Generated: ${new Date().toISOString()}`,
  '',
  `- Canonical doc present: ${existsSync(startupDoc) ? 'yes' : 'no'}`,
  `- AGENTS reference present: ${agents.includes('startup-sequence.md') ? 'yes' : 'no'}`,
  ...adapterPaths.map((file) => {
    const text = read(file);
    const name = file.replace(root + '/', '');
    return `- ${name}: ${text.includes('startup-sequence.md') ? 'linked' : 'missing link'}`;
  }),
  '',
  failures.length > 0 ? '## Failures' : '## All startup checks passed.',
  ...failures.map((f) => `- ${f}`),
  ''
].join('\n');

writeFileSync(join(reportsDir, `startup-consistency-${now}.md`), report);
console.log(report);
if (failures.length > 0) process.exit(1);
