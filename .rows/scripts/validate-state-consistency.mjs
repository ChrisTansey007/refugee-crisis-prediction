#!/usr/bin/env node
// validate-state-consistency.mjs — Cross-check paired JSON and Markdown state files.

import { readFileSync, existsSync, writeFileSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const reportDir = join(root, 'agent-os', 'reports', 'state-consistency');
const now = new Date().toISOString().split('T')[0];
const stamp = new Date().toISOString();

function readJson(path) {
  return JSON.parse(readFileSync(path, 'utf-8'));
}

function normalizeList(value) {
  return String(value || '')
    .split(',')
    .map(item => item.trim().toLowerCase())
    .map(item => (item === 'all workers' ? 'all' : item))
    .filter(Boolean)
    .sort();
}

function parseDecisionMarkdown(md) {
  const rows = [];
  for (const line of md.split(/\r?\n/)) {
    const match = line.match(/^\|\s*\[((?:ADR|BLOCKER)-[A-Z0-9-]+)\]\(([^)]+)\)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$/);
    if (!match) continue;
    const [, adr, file, title, status, date] = match;
    rows.push({ adr, file: file.trim(), title: title.trim(), status: status.trim(), date: date.trim() });
  }
  return rows;
}

function parseCapabilityMarkdown(md) {
  const rows = [];
  for (const line of md.split(/\r?\n/)) {
    if (!line.startsWith('| ')) continue;
    if (line.startsWith('|-----------') || line.startsWith('|---------') || line.includes('Capability | Description')) continue;
    const match = line.match(/^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$/);
    if (!match) continue;
    const [, capability, description, preferredWorkers, commonRoles] = match;
    const key = capability.trim();
    if (!key || key.toLowerCase() === 'capability') continue;
    rows.push({
      key,
      description: description.trim(),
      preferredWorkers: normalizeList(preferredWorkers),
      commonRoles: normalizeList(commonRoles),
    });
  }
  return rows;
}

const decisionJsonPath = join(root, 'agent-os', 'state', 'decision-register.json');
const decisionMdPath = join(root, 'docs', '05-decisions', 'decision-register.md');
const capabilityJsonPath = join(root, 'agent-os', 'state', 'capability-registry.json');
const capabilityMdPath = join(root, 'agent-os', 'role-capability-matrix.md');

const reportLines = [
  `# State Consistency Report — ${now}`,
  `> Generated: ${stamp}`,
  ''
];

let issues = 0;

// Decision register vs markdown index
if (existsSync(decisionJsonPath) && existsSync(decisionMdPath)) {
  const decisionJson = readJson(decisionJsonPath);
  const decisionMd = readFileSync(decisionMdPath, 'utf-8');
  const mdRows = parseDecisionMarkdown(decisionMd);
  const mdByAdr = new Map(mdRows.map(row => [row.adr, row]));
  const jsonDecisions = decisionJson.decisions || [];

  const missingInMd = [];
  const extraInMd = [];
  for (const decision of jsonDecisions) {
    if (!mdByAdr.has(decision.adr)) {
      missingInMd.push(decision.adr);
      continue;
    }
    const row = mdByAdr.get(decision.adr);
    if (row.title !== decision.title || row.status.toLowerCase() !== String(decision.status || '').toLowerCase()) {
      issues++;
      reportLines.push(`- Decision mismatch for ${decision.adr}: JSON title/status (${decision.title} / ${decision.status}) vs Markdown (${row.title} / ${row.status})`);
    }
  }
  for (const row of mdRows) {
    if (!jsonDecisions.some(decision => decision.adr === row.adr)) {
      extraInMd.push(row.adr);
    }
  }

  if (missingInMd.length > 0) {
    issues += missingInMd.length;
    reportLines.push(`- Missing decision rows in Markdown: ${missingInMd.join(', ')}`);
  }
  if (extraInMd.length > 0) {
    issues += extraInMd.length;
    reportLines.push(`- Extra Markdown decisions not found in JSON: ${extraInMd.join(', ')}`);
  }

  reportLines.push('', '## Decision Register', `- JSON decisions: ${jsonDecisions.length}`, `- Markdown rows: ${mdRows.length}`, `- Missing in Markdown: ${missingInMd.length}`, `- Extra in Markdown: ${extraInMd.length}`,'');
} else {
  reportLines.push('## Decision Register', '- Skipped (one or both files missing)', '');
}

// Capability registry vs role-capability matrix
if (existsSync(capabilityJsonPath) && existsSync(capabilityMdPath)) {
  const capabilityJson = readJson(capabilityJsonPath);
  const capabilityMd = readFileSync(capabilityMdPath, 'utf-8');
  const mdRows = parseCapabilityMarkdown(capabilityMd);
  const mdByKey = new Map(mdRows.map(row => [row.key, row]));
  const jsonCapabilities = capabilityJson.capabilities || {};
  const jsonKeys = Object.keys(jsonCapabilities);

  const missingInMd = [];
  const extraInMd = [];
  for (const key of jsonKeys) {
    const jsonCap = jsonCapabilities[key];
    const row = mdByKey.get(key);
    if (!row) {
      missingInMd.push(key);
      continue;
    }
    const jsonPreferred = normalizeList((jsonCap.preferred_workers || []).join(','));
    if (jsonPreferred.join(',') !== row.preferredWorkers.join(',')) {
      issues++;
      reportLines.push(`- Capability mismatch for ${key}: preferred workers JSON (${jsonPreferred.join(', ') || 'none'}) vs Markdown (${row.preferredWorkers.join(', ') || 'none'})`);
    }
  }
  for (const row of mdRows) {
    if (!jsonKeys.includes(row.key)) {
      extraInMd.push(row.key);
    }
  }

  if (missingInMd.length > 0) {
    issues += missingInMd.length;
    reportLines.push(`- Missing capability rows in Markdown: ${missingInMd.join(', ')}`);
  }
  if (extraInMd.length > 0) {
    issues += extraInMd.length;
    reportLines.push(`- Extra Markdown capabilities not found in JSON: ${extraInMd.join(', ')}`);
  }

  reportLines.push('## Capability Registry', `- JSON capabilities: ${jsonKeys.length}`, `- Markdown rows: ${mdRows.length}`, `- Missing in Markdown: ${missingInMd.length}`, `- Extra in Markdown: ${extraInMd.length}`,'');
} else {
  reportLines.push('## Capability Registry', '- Skipped (one or both files missing)', '');
}

if (!existsSync(reportDir)) {
  mkdirSync(reportDir, { recursive: true });
}
const reportPath = join(reportDir, `state-consistency-${now}.md`);
writeFileSync(reportPath, reportLines.join('\n'));

console.log(reportLines.join('\n'));
console.log(`State consistency report written to: agent-os/reports/state-consistency/state-consistency-${now}.md`);

if (issues > 0) {
  process.exit(1);
}
