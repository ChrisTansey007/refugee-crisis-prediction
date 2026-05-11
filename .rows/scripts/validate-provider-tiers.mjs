#!/usr/bin/env node
// validate-provider-tiers.mjs — Validate starter provider tier routing data.

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const tiersPath = join(root, 'agent-os', 'state', 'provider-tiers.json');

if (!existsSync(tiersPath)) {
  console.log('Provider tier validation: no provider-tiers.json found.');
  process.exit(0);
}

let data;
try {
  data = JSON.parse(readFileSync(tiersPath, 'utf-8'));
} catch (error) {
  console.error(`Invalid JSON in provider-tiers.json: ${error.message}`);
  process.exit(1);
}

const issues = [];
if (!data || typeof data !== 'object') issues.push('Root must be an object.');
if (!Number.isInteger(data.version) || data.version < 1) issues.push('version must be a positive integer.');
if (typeof data.default_tier !== 'string' || !data.default_tier) issues.push('default_tier must be a non-empty string.');
if (!data.tiers || typeof data.tiers !== 'object' || Array.isArray(data.tiers)) issues.push('tiers must be an object.');

const tierNames = ['frontier', 'mid', 'fast', 'local'];
for (const name of tierNames) {
  const tier = data.tiers?.[name];
  if (!tier || typeof tier !== 'object' || Array.isArray(tier)) {
    issues.push(`Missing tier object: ${name}`);
    continue;
  }
  if (typeof tier.description !== 'string' || !tier.description.trim()) issues.push(`${name}.description must be a non-empty string.`);
  if (!Array.isArray(tier.use_for) || tier.use_for.length === 0) issues.push(`${name}.use_for must be a non-empty array.`);
  if (!Array.isArray(tier.fallback)) issues.push(`${name}.fallback must be an array.`);
  if (typeof tier.cost_ceiling !== 'string' || !tier.cost_ceiling.trim()) issues.push(`${name}.cost_ceiling must be a non-empty string.`);
}

if (data.default_tier && !tierNames.includes(data.default_tier)) {
  issues.push(`default_tier must be one of: ${tierNames.join(', ')}`);
}

const reportsDir = join(root, 'agent-os', 'reports', 'provider-routing');
if (!existsSync(reportsDir)) mkdirSync(reportsDir, { recursive: true });
const now = new Date().toISOString().split('T')[0];
const report = [
  `# Provider Tier Validation — ${now}`,
  `> Generated: ${new Date().toISOString()}`,
  '',
  `- Default tier: ${data.default_tier || 'N/A'}`,
  `- Tiers defined: ${Object.keys(data.tiers || {}).length}`,
  '',
  issues.length > 0 ? '## Issues' : '## No issues found.',
  ...issues.map(issue => `- ${issue}`),
  ''
].join('\n');
writeFileSync(join(reportsDir, `provider-tiers-${now}.md`), report);

console.log('Provider Tier Validation Results:');
console.log(`  Tiers: ${Object.keys(data.tiers || {}).length}`);
console.log(`  Issues: ${issues.length}`);

if (issues.length > 0) {
  process.exit(1);
}
