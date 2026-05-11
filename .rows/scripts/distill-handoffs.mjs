#!/usr/bin/env node
// distill-handoffs.mjs — Draft updates to PROJECT_CONTEXT.md from active handoffs.

import { existsSync, readFileSync, readdirSync, writeFileSync, mkdirSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const activeDir = join(root, 'agent-os', 'handoffs', 'active');
const projectContextPath = join(root, 'PROJECT_CONTEXT.md');

function read(file) {
  return readFileSync(file, 'utf-8');
}

function getSection(content, heading) {
  const escaped = heading.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const pattern = new RegExp(`^## ${escaped}\\s*$([\\s\\S]*?)(?=^## |\\Z)`, 'm');
  const match = content.match(pattern);
  return match ? match[1].trim() : '';
}

function bullets(text) {
  return text
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line.startsWith('- '))
    .map((line) => line.slice(2).trim())
    .filter(Boolean);
}

const handoffs = existsSync(activeDir)
  ? readdirSync(activeDir)
      .filter((name) => name.endsWith('.md') && name !== 'README.md' && !name.startsWith('EXAMPLE'))
      .map((name) => {
        const fullPath = join(activeDir, name);
        const content = read(fullPath);
        return {
          name,
          taskId: content.match(/TASK-\d+/)?.[0] || 'unknown-task',
          knownIssues: bullets(getSection(content, 'Known Issues')),
          risks: bullets(getSection(content, 'Risks')),
          continuity: getSection(content, 'Continuity Notes'),
          changes: getSection(content, 'What Changed'),
          nextSteps: getSection(content, 'Next Steps')
        };
      })
  : [];

if (!existsSync(projectContextPath)) {
  console.error('PROJECT_CONTEXT.md not found. Create it before running distillation.');
  process.exit(1);
}

const current = read(projectContextPath);
const durableFacts = [];
const activeConstraints = [];
const watchItems = [];
const recentlyDistilled = [];

for (const handoff of handoffs) {
  if (handoff.continuity) durableFacts.push(`- ${handoff.taskId}: ${handoff.continuity.replace(/\n+/g, ' ').trim()}`);
  for (const issue of handoff.knownIssues) {
    activeConstraints.push(`- ${handoff.taskId}: ${issue}`);
  }
  for (const risk of handoff.risks) {
    watchItems.push(`- ${handoff.taskId}: ${risk}`);
  }
  recentlyDistilled.push(`- ${handoff.taskId} from \`agent-os/handoffs/active/${handoff.name}\``);
}

const stamp = new Date().toISOString();
const draft = [
  '<!-- rows:distillation:draft:start -->',
  `Last distilled: ${stamp}`,
  '',
  '### Suggested Durable Facts',
  durableFacts.length ? durableFacts.join('\n') : '- none',
  '',
  '### Suggested Active Constraints',
  activeConstraints.length ? activeConstraints.join('\n') : '- none',
  '',
  '### Suggested Watch Items',
  watchItems.length ? watchItems.join('\n') : '- none',
  '',
  '### Handoffs Covered',
  recentlyDistilled.length ? recentlyDistilled.join('\n') : '- none',
  '<!-- rows:distillation:draft:end -->'
].join('\n');

const updated = current.replace(
  /<!-- rows:distillation:draft:start -->[\s\S]*<!-- rows:distillation:draft:end -->/,
  draft
);

const finalContent = updated === current ? `${current.trim()}\n\n${draft}\n` : `${updated.trim()}\n`;
mkdirSync(dirname(projectContextPath), { recursive: true });
writeFileSync(projectContextPath, finalContent);

console.log(`Updated distillation draft in PROJECT_CONTEXT.md with ${handoffs.length} active handoff(s).`);
