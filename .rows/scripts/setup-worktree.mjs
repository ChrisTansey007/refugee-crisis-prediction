#!/usr/bin/env node
// setup-worktree.mjs — Create a task-scoped git worktree for a worker.

import { execSync, spawnSync } from 'child_process';
import { existsSync, mkdirSync } from 'fs';
import { basename, dirname, join, resolve } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const repoName = basename(root);

function usage() {
  console.log('Usage: node scripts/setup-worktree.mjs <worker> <task-id> [--base <branch>] [--path <dir>] [--branch <branch>] [--dry-run]');
}

function slug(value) {
  return String(value)
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function run(cmd) {
  return execSync(cmd, { cwd: root, encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] }).trim();
}

function detectBaseBranch() {
  try {
    const remoteHead = run('git symbolic-ref --quiet --short refs/remotes/origin/HEAD');
    return remoteHead.split('/').pop();
  } catch {
    try {
      const branch = run('git branch --show-current');
      if (branch) return branch;
    } catch {}
    return 'main';
  }
}

const args = process.argv.slice(2);
if (args.length < 2) {
  usage();
  process.exit(1);
}

const worker = args[0];
const taskId = args[1];
let baseBranch;
let worktreePath;
let branchName;
let dryRun = false;

for (let i = 2; i < args.length; i++) {
  const arg = args[i];
  if (arg === '--base') {
    baseBranch = args[++i];
  } else if (arg === '--path') {
    worktreePath = resolve(args[++i]);
  } else if (arg === '--branch') {
    branchName = args[++i];
  } else if (arg === '--dry-run') {
    dryRun = true;
  } else if (arg === '--help' || arg === '-h') {
    usage();
    process.exit(0);
  } else {
    console.error(`Unknown argument: ${arg}`);
    usage();
    process.exit(1);
  }
}

const workerSlug = slug(worker);
const taskSlug = slug(taskId);
const defaultBranch = `agent/${workerSlug}/${taskSlug}-worktree`;
const targetBranch = branchName || defaultBranch;
const targetPath = worktreePath || join(dirname(root), `${repoName}-${workerSlug}`);
const targetParent = dirname(targetPath);
const base = baseBranch || detectBaseBranch();

if (existsSync(targetPath)) {
  console.error(`Worktree path already exists: ${targetPath}`);
  process.exit(1);
}

mkdirSync(targetParent, { recursive: true });

const cmd = ['worktree', 'add', '--checkout', '--branch', targetBranch, targetPath, base];

console.log(`Repository root: ${root}`);
console.log(`Worker: ${worker}`);
console.log(`Task: ${taskId}`);
console.log(`Base branch: ${base}`);
console.log(`Branch: ${targetBranch}`);
console.log(`Path: ${targetPath}`);

if (dryRun) {
  console.log(`Dry run: git ${cmd.map(part => JSON.stringify(part)).join(' ')}`);
  process.exit(0);
}

try {
  const result = spawnSync('git', cmd, { cwd: root, stdio: 'inherit' });
  if (result.status !== 0) {
    throw new Error(`git exited with status ${result.status ?? 'unknown'}`);
  }
} catch (error) {
  console.error('\nFailed to create worktree.');
  process.exit(typeof error.status === 'number' ? error.status : 1);
}

console.log('\nWorktree created successfully.');
console.log(`Next: cd ${targetPath} && git status`);
