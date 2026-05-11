#!/usr/bin/env node
// validate-placeholders.mjs — Scan for vague placeholders in the repo.

import { readFileSync, readdirSync, existsSync, statSync, writeFileSync, mkdirSync } from 'fs';
import { join, dirname, relative, extname, sep } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');

const TEXT_EXTS = ['.md', '.json', '.yml', '.yaml', '.mjs', '.js', '.ts', '.tsx', '.jsx'];

const INTENTIONAL = [
  '[PROJECT_NAME]', '[PROJECT_GOAL]', '[PRIMARY_USER]', '[TECH_STACK]',
  '[DEPLOYMENT_TARGET]', '[OWNER_USERNAME]', '[WORKER_NAME]', '[ROLE_NAME]',
  '[CAPABILITY]', '[TASK_ID]', '[ONE_SENTENCE_GOAL]', '[LONG_FORM_GOAL]',
  '[OUTCOME_1]', '[OUTCOME_2]', '[OUTCOME_3]', '[NON_GOAL_1]', '[NON_GOAL_2]', '[NON_GOAL_3]',
  '[BUDGET_CONSTRAINT]', '[TIMELINE_CONSTRAINT]', '[TEAM_SIZE]', '[PLATFORM_CONSTRAINT]',
  '[COMPLIANCE_REQUIREMENTS]', '[OTHER_CONSTRAINTS]', '[FRONTEND_FRAMEWORK]',
  '[BACKEND_FRAMEWORK]', '[DATABASE]', '[CI_CD]', '[OTHER_TECH]',
  '[CRITERION_1]', '[CRITERION_2]', '[CRITERION_3]', '[FIRST_MILESTONE]',
  '[RISK_1]', '[RISK_2]', '[RISK_3]', '[PREFERRED_EXECUTION_MODE]',
  '[PREFERRED_WORKERS]', '[WORKERS_NOT_AVAILABLE]', '[HUMAN_REVIEW_PREFERENCE]',
  '[WORKER_AUTONOMY]', '[HUMAN_OWNER_NOTES]'
];

const VAGUE = ['TODO', 'TBD', 'FIXME', 'fill this in later', 'coming soon', 'placeholder text'];

function walk(dir, files = [], excludeDirs = ['reports']) {
  if (!existsSync(dir)) return files;
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) {
      if (!entry.startsWith('.git') && entry !== 'node_modules' && !excludeDirs.includes(entry)) {
        walk(full, files, []);
      }
    } else if (TEXT_EXTS.includes(extname(entry))) {
      files.push(full);
    }
  }
  return files;
}

// Exclude agent-os/reports/ from scan (contains generated reports that may reference vague terms)
// Also exclude this script itself
function shouldSkip(file) {
  const rel = relative(root, file);
  return rel.includes('reports' + sep) || rel.includes('validate-placeholders.mjs');
}

const allFiles = walk(root);
let vagueCount = 0;
let intentionalCount = 0;
const vagueFound = [];
const intentionalFound = [];

for (const file of allFiles) {
  if (shouldSkip(file)) continue;
  const content = readFileSync(file, 'utf-8');
  const relFile = relative(root, file);

  for (const v of VAGUE) {
    if (content.includes(v)) {
      vagueCount++;
      vagueFound.push({ file: relFile, placeholder: v });
    }
  }

  for (const i of INTENTIONAL) {
    if (content.includes(i)) {
      intentionalCount++;
      intentionalFound.push({ file: relFile, placeholder: i });
    }
  }
}

// Write report
const reportsDir = join(root, 'agent-os', 'reports', 'placeholders');
if (!existsSync(reportsDir)) mkdirSync(reportsDir, { recursive: true });

const now = new Date().toISOString().split('T')[0];
const report = [
  `# Placeholder Audit Report — ${now}`,
  `> Generated: ${new Date().toISOString()}`,
  '',
  `## Summary`,
  `- Intentional placeholders found: ${intentionalCount}`,
  `- Vague placeholders found: ${vagueCount}`,
  '',
  vagueFound.length > 0 ? '## Vague Placeholders (Action Required)' : '## No vague placeholders found.',
  ...vagueFound.map(v => `- \`${v.file}\`: "${v.placeholder}"`),
  '',
  '## Intentional Placeholders (Allowed)',
  ...intentionalFound.slice(0, 20).map(i => `- \`${i.file}\`: ${i.placeholder}`),
  intentionalFound.length > 20 ? `- ... and ${intentionalFound.length - 20} more` : '',
  ''
].join('\n');

writeFileSync(join(reportsDir, `placeholders-${now}.md`), report);

console.log(`Placeholder Audit Results:`);
console.log(`  Intentional: ${intentionalCount}`);
console.log(`  Vague:       ${vagueCount}`);
console.log(`  Report:      agent-os/reports/placeholders/placeholders-${now}.md`);

if (vagueCount > 0) {
  console.log('\nWARNING: Vague placeholders found. Replace with intentional markers or remove.');
  process.exit(1);
}
