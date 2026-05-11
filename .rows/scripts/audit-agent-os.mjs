#!/usr/bin/env node
// audit-agent-os.mjs — Run comprehensive audit of agent-os.

import { execSync } from 'child_process';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { existsSync, writeFileSync, mkdirSync } from 'fs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');

const scripts = [
  { name: 'JSON Validation', cmd: 'node scripts/validate-json.mjs' },
  { name: 'Task Validation', cmd: 'node scripts/validate-task.mjs' },
  { name: 'Handoff Validation', cmd: 'node scripts/validate-handoff.mjs' },
  { name: 'Assignment Validation', cmd: 'node scripts/validate-assignments.mjs' },
  { name: 'Decision Validation', cmd: 'node scripts/validate-decisions.mjs' },
  { name: 'Knowledge Graph Validation', cmd: 'node scripts/validate-knowledge-graph.mjs' },
  { name: 'Link Validation', cmd: 'node scripts/validate-links.mjs' },
  { name: 'Placeholder Validation', cmd: 'node scripts/validate-placeholders.mjs' },
  { name: 'Lock Validation', cmd: 'node scripts/validate-locks.mjs' },
  { name: 'MCP Validation', cmd: 'node scripts/validate-mcp.mjs' },
  { name: 'Provider Tier Validation', cmd: 'node scripts/validate-provider-tiers.mjs' },
  { name: 'Secret Scan', cmd: 'node scripts/validate-secrets.mjs' },
  { name: 'Scope Check', cmd: 'node scripts/check-scope.mjs' },
  { name: 'Markdown Lint', cmd: 'node scripts/lint-markdown.mjs' },
  { name: 'State Consistency Validation', cmd: 'node scripts/validate-state-consistency.mjs' },
  { name: 'Startup Consistency Validation', cmd: 'node scripts/validate-startup-consistency.mjs' },
  { name: 'Template Readiness', cmd: 'node scripts/validate-template-readiness.mjs' },
  { name: 'Definition of Done', cmd: 'node scripts/check-definition-of-done.mjs' }
];

console.log('========================================');
console.log('  ROWS — Agent OS Audit');
console.log('========================================\n');

let passed = 0;
let failed = 0;
const results = [];

for (const { name, cmd } of scripts) {
  process.stdout.write(`${name}... `);
  try {
    execSync(cmd, { cwd: root, stdio: 'pipe', timeout: 30000 });
    console.log('PASS');
    passed++;
    results.push({ name, status: 'PASS' });
  } catch (e) {
    console.log('FAIL');
    failed++;
    results.push({ name, status: 'FAIL', error: e.stderr?.toString().slice(0, 200) || e.message });
  }
}

console.log('\n========================================');
console.log('  Audit Summary');
console.log('========================================');
console.log(`  Passed: ${passed}`);
console.log(`  Failed: ${failed}`);
console.log(`  Total:  ${passed + failed}`);

// Write audit report
const reportsDir = join(root, 'agent-os', 'reports', 'audits');
if (!existsSync(reportsDir)) mkdirSync(reportsDir, { recursive: true });

const now = new Date().toISOString().split('T')[0];
const report = [
  `# Audit Report — ${now}`,
  `> Generated: ${new Date().toISOString()}`,
  '',
  '| Check | Result |',
  '|-------|--------|',
  ...results.map(r => `| ${r.name} | ${r.status} |`),
  '',
  `- **Passed:** ${passed}`,
  `- **Failed:** ${failed}`,
  ''
].join('\n');

writeFileSync(join(reportsDir, `audit-${now}.md`), report);

if (failed > 0) {
  process.exit(1);
}
