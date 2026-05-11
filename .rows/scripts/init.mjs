#!/usr/bin/env node
// init.mjs — Initialize a fresh ROWS fork with project metadata and starter scaffolding.

import { execSync } from 'child_process';
import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'fs';
import { dirname, join, basename } from 'path';
import { fileURLToPath } from 'url';
import readline from 'readline/promises';
import process from 'process';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

function usage() {
  console.log('Usage: node scripts/init.mjs [--project-name NAME] [--owner-username USER] [--execution-mode solo|multi-worker|hybrid] [--primary-worker WORKER] [--dry-run]');
}

function slugify(value) {
  return String(value)
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function parseArgs(argv) {
  const out = { dryRun: false };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    switch (arg) {
      case '--project-name':
        out.projectName = argv[++i];
        break;
      case '--owner-username':
        out.ownerUsername = argv[++i];
        break;
      case '--execution-mode':
        out.executionMode = argv[++i];
        break;
      case '--primary-worker':
        out.primaryWorker = argv[++i];
        break;
      case '--dry-run':
        out.dryRun = true;
        break;
      case '--help':
      case '-h':
        out.help = true;
        break;
      default:
        throw new Error(`Unknown argument: ${arg}`);
    }
  }
  return out;
}

async function prompt(question, fallback = '') {
  const suffix = fallback ? ` [${fallback}]` : '';
  const answer = (await rl.question(`${question}${suffix}: `)).trim();
  return answer || fallback;
}

function readJson(path) {
  return JSON.parse(readFileSync(path, 'utf8'));
}

function writeJson(path, value, dryRun) {
  const content = `${JSON.stringify(value, null, 2)}\n`;
  if (!dryRun) writeFileSync(path, content);
  return content;
}

function replaceAll(text, replacements) {
  let next = text;
  for (const [from, to] of replacements) {
    next = next.split(from).join(to);
  }
  return next;
}

function updateTextFile(path, replacements, dryRun) {
  if (!existsSync(path)) return false;
  const original = readFileSync(path, 'utf8');
  const next = replaceAll(original, replacements);
  if (next === original) return false;
  if (!dryRun) writeFileSync(path, next);
  return true;
}

function gitRemoteInfo() {
  try {
    const remote = execSync('git remote get-url origin', { cwd: root, encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] }).trim();
    const match = remote.match(/github\.com[:/](?<owner>[^/]+)\/(?<repo>[^/.]+)(?:\.git)?$/);
    if (!match?.groups) return null;
    return { owner: match.groups.owner, repo: match.groups.repo };
  } catch {
    return null;
  }
}

function ensureDir(path, dryRun) {
  if (!existsSync(path) && !dryRun) mkdirSync(path, { recursive: true });
}

function listTaskFiles(dir) {
  if (!existsSync(dir)) return [];
  return readdirSync(dir).filter((name) => /^TASK-\d+.*\.md$/i.test(name));
}

function ensureStarterTask(projectName, dryRun) {
  const taskDir = join(root, 'agent-os', 'tasks', 'backlog');
  const taskPath = join(taskDir, 'TASK-0001-initialize-project-from-goal.md');
  if (existsSync(taskPath)) return false;

  const templatePath = join(root, 'agent-os', 'tasks', 'task-template.md');
  const template = readFileSync(templatePath, 'utf8');
  const content = template
    .replace('[TASK-ID]: [Task Title]', 'TASK-0001: Initialize Project from Goal')
    .replace('backlog | ready | claimed | in-progress | review | blocked | done', 'backlog')
    .replace('[ROLE_NAME]', 'goal-builder')
    .replace('- [ROLE_NAME]', '- project-planner')
    .replace('- [CAPABILITY]', '- goal-decomposition')
    .replace('- [WORKER_NAME]', '- Hermes')
    .replace('[Clear, one-paragraph description of what must be accomplished. Be specific enough that a worker can understand the goal without additional context.]', `Read PROJECT_GOAL.md, populate the starter project brief, and create the initial task set for ${projectName}.`);

  if (!dryRun) writeFileSync(taskPath, content);
  return true;
}

async function main() {
  const parsed = parseArgs(process.argv.slice(2));
  if (parsed.help) {
    usage();
    process.exit(0);
  }

  const projectName = parsed.projectName || await prompt('Project name', basename(root));
  const ownerUsername = parsed.ownerUsername || await prompt('GitHub owner username');
  const executionMode = parsed.executionMode || await prompt('Execution mode', 'solo');
  const primaryWorker = parsed.primaryWorker || await prompt('Primary worker', 'hermes');
  const projectSlug = slugify(projectName) || slugify(basename(root));

  if (!projectName) {
    throw new Error('Project name is required.');
  }
  if (!ownerUsername) {
    throw new Error('GitHub owner username is required.');
  }

  const timestamp = new Date().toISOString();
  const origin = gitRemoteInfo();

  const changed = [];

  const projectGoalPath = join(root, 'PROJECT_GOAL.md');
  if (updateTextFile(projectGoalPath, [['[PROJECT_NAME]', projectName]], parsed.dryRun)) changed.push('PROJECT_GOAL.md');

  const envExamplePath = join(root, '.env.example');
  if (updateTextFile(envExamplePath, [['[PROJECT_NAME]', projectName]], parsed.dryRun)) changed.push('.env.example');

  const licensePath = join(root, 'LICENSE');
  if (updateTextFile(licensePath, [['[OWNER_USERNAME]', ownerUsername]], parsed.dryRun)) changed.push('LICENSE');

  const codeownersPath = join(root, '.github', 'CODEOWNERS');
  ensureDir(dirname(codeownersPath), parsed.dryRun);
  if (!existsSync(codeownersPath)) {
    const codeowners = `# Replace OWNER_USERNAME with the GitHub handle that owns this fork.\n* @${ownerUsername}\n`;
    if (!parsed.dryRun) writeFileSync(codeownersPath, codeowners);
    changed.push('.github/CODEOWNERS');
  } else if (updateTextFile(codeownersPath, [['OWNER_USERNAME', ownerUsername]], parsed.dryRun)) {
    changed.push('.github/CODEOWNERS');
  }

  const readmePath = join(root, 'README.md');
  if (origin && existsSync(readmePath)) {
    const before = readFileSync(readmePath, 'utf8');
    const next = before.replaceAll(`https://github.com/${origin.owner}/${origin.repo}`, `https://github.com/${ownerUsername}/${projectSlug}`);
    if (next !== before) {
      if (!parsed.dryRun) writeFileSync(readmePath, next);
      changed.push('README.md');
    }
  }

  const packagePath = join(root, 'package.json');
  if (existsSync(packagePath)) {
    const pkg = readJson(packagePath);
    if (pkg.name !== projectSlug) {
      pkg.name = projectSlug;
      writeJson(packagePath, pkg, parsed.dryRun);
      changed.push('package.json');
    }
  }

  const systemStatePath = join(root, 'agent-os', 'state', 'system-state.json');
  if (existsSync(systemStatePath)) {
    const state = readJson(systemStatePath);
    state.repo_name = projectName;
    state.mode = 'project';
    state.execution_mode = executionMode;
    state.active_task_count = listTaskFiles(join(root, 'agent-os', 'tasks', 'backlog')).length;
    state.last_updated = timestamp;
    state.notes = `Initialized for ${projectName} with ${executionMode} execution mode.`;
    writeJson(systemStatePath, state, parsed.dryRun);
    changed.push('agent-os/state/system-state.json');
  }

  const assignmentStatePath = join(root, 'agent-os', 'state', 'assignment-state.json');
  if (existsSync(assignmentStatePath)) {
    const assignment = readJson(assignmentStatePath);
    assignment.mode = executionMode;
    assignment.active_workers = primaryWorker ? [primaryWorker] : [];
    assignment.assignments = primaryWorker ? [{ worker: primaryWorker, role: executionMode === 'solo' ? 'generalist' : 'primary-worker', status: 'active' }] : [];
    assignment.active_goal_builder = executionMode === 'solo' ? primaryWorker : null;
    assignment.active_coordinator = executionMode !== 'solo' ? 'hermes' : null;
    assignment.notes = [`Initialized at ${timestamp}.`, `Primary worker: ${primaryWorker}.`];
    writeJson(assignmentStatePath, assignment, parsed.dryRun);
    changed.push('agent-os/state/assignment-state.json');
  }

  const starterTaskCreated = ensureStarterTask(projectName, parsed.dryRun);
  if (starterTaskCreated) changed.push('agent-os/tasks/backlog/TASK-0001-initialize-project-from-goal.md');

  console.log(`Init ${parsed.dryRun ? 'dry run' : 'complete'} for ${projectName}`);
  console.log(`Owner: ${ownerUsername}`);
  console.log(`Execution mode: ${executionMode}`);
  console.log(`Primary worker: ${primaryWorker}`);
  console.log(`Project slug: ${projectSlug}`);
  if (changed.length > 0) {
    console.log('Changed files:');
    for (const file of changed) console.log(`- ${file}`);
  } else {
    console.log('No files changed.');
  }
}

main()
  .catch((error) => {
    console.error(error?.message || error);
    process.exit(1);
  })
  .finally(() => rl.close());
