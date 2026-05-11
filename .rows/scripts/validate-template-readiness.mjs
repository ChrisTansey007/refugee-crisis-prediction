#!/usr/bin/env node
// validate-template-readiness.mjs — Check template readiness gates.

import { existsSync, writeFileSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');

const CHECKS = {
  rootDocs: [
    'README.md', 'AGENTS.md', 'PROJECT_GOAL.md', 'TEMPLATE_USAGE.md',
    'HUMAN_OWNER_GUIDE.md', 'TEMPLATE_READINESS.md', 'CONTRIBUTING.md',
    'SECURITY.md', 'CHANGELOG.md', 'RELEASE_CHECKLIST.md', 'CODE_OF_CONDUCT.md',
    '.env.example', '.editorconfig', '.gitattributes'
  ],
  agentOsDirs: [
    'agent-os/workers', 'agent-os/roles', 'agent-os/tasks/backlog',
    'agent-os/tasks/ready', 'agent-os/tasks/claimed', 'agent-os/tasks/in-progress',
    'agent-os/tasks/review', 'agent-os/tasks/blocked', 'agent-os/tasks/done',
    'agent-os/handoffs/active', 'agent-os/locks', 'agent-os/reports', 'agent-os/schemas'
  ],
  agentOsFiles: [
    'agent-os/README.md', 'agent-os/assignment-model.md', 'agent-os/execution-modes.md',
    'agent-os/worker-contract.md', 'agent-os/task-lifecycle.md', 'agent-os/definition-of-done.md',
    'agent-os/verification-gates.md', 'agent-os/tasks/task-template.md', 'agent-os/handoffs/handoff-template.md',
    'agent-os/mcp.md', 'agent-os/worktree-strategy.md', 'agent-os/provider-routing.md',
    'agent-os/prompt-injection-policy.md', 'agent-os/startup-sequence.md'
  ],
  agentOsStateFiles: [
    'agent-os/state/provider-tiers.json'
  ],

  promptLibrary: [
    'prompt-library/README.md', 'prompt-library/goal-intake-to-tasks.md',
    'prompt-library/solo-worker-start.md', 'prompt-library/multi-worker-start.md',
    'prompt-library/hybrid-primary-worker-start.md', 'prompt-library/support-worker-start.md',
    'prompt-library/reviewer-worker-start.md', 'prompt-library/verification-worker-start.md',
    'prompt-library/reassignment-continuation.md', 'prompt-library/status-report-request.md',
    'prompt-library/template-publish-check.md'
  ],
  examples: [
    'examples/README.md', 'examples/sample-project-goal.md', 'examples/sample-task.md',
    'examples/sample-handoff.md', 'examples/sample-verification-report.md',
    'examples/sample-reassignment-record.md', 'examples/sample-status-report.md'
  ],
  mcpFiles: [
    '.mcp.example.json'
  ],
  adrFiles: [
    'docs/02-architecture/decisions/ADR-0001-repo-orchestrated-worker-system.md',
    'docs/02-architecture/decisions/ADR-0002-template-fork-workflow.md',
    'docs/02-architecture/decisions/ADR-0003-flexible-worker-assignment.md'
  ],
  noCopilot: [
    '.copilot', '.copilot-instructions.md', '.github/copilot-instructions.md'
  ]
};

let passed = 0;
let failed = 0;
const failures = [];

function check(name, files) {
  for (const f of files) {
    if (!existsSync(join(root, f))) {
      failures.push(`MISSING: ${f}`);
      failed++;
    } else {
      passed++;
    }
  }
}

check('Root Docs', CHECKS.rootDocs);
check('Agent OS Dirs', CHECKS.agentOsDirs);
check('Agent OS Files', CHECKS.agentOsFiles);
check('Agent OS State Files', CHECKS.agentOsStateFiles);
check('Prompt Library', CHECKS.promptLibrary);
check('Examples', CHECKS.examples);
check('MCP Config', CHECKS.mcpFiles);
check('ADR Files', CHECKS.adrFiles);

// Check no Copilot files
for (const f of CHECKS.noCopilot) {
  if (existsSync(join(root, f))) {
    failures.push(`COPILOT FILE FOUND: ${f}`);
    failed++;
  } else {
    passed++;
  }
}

// Write report
const reportsDir = join(root, 'agent-os', 'reports', 'template-readiness');
if (!existsSync(reportsDir)) mkdirSync(reportsDir, { recursive: true });

const now = new Date().toISOString().split('T')[0];
const report = [
  `# Template Readiness Report — ${now}`,
  `> Generated: ${new Date().toISOString()}`,
  '',
  `- Total checks: ${passed + failed}`,
  `- Passed: ${passed}`,
  `- Failed: ${failed}`,
  '',
  failures.length > 0 ? '## Failures' : '## All checks passed.',
  ...failures.map(f => `- ${f}`),
  ''
].join('\n');

writeFileSync(join(reportsDir, `readiness-${now}.md`), report);

console.log(`Template Readiness Results:`);
console.log(`  Passed: ${passed}`);
console.log(`  Failed: ${failed}`);
if (failures.length > 0) {
  console.log('\nFailures:');
  failures.forEach(f => console.log(`  - ${f}`));
}

if (failed > 0) {
  process.exit(1);
}
