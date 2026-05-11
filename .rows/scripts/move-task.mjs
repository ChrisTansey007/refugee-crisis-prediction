#!/usr/bin/env node
// move-task.mjs — Move a task between lifecycle folders.
// Usage: node scripts/move-task.mjs <task-id> <from-folder> <to-folder>

import { existsSync, renameSync, mkdirSync, readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const tasksDir = join(root, 'agent-os', 'tasks');

const VALID_FOLDERS = ['backlog', 'ready', 'claimed', 'in-progress', 'review', 'blocked', 'done'];

const taskId = process.argv[2];
const fromFolder = process.argv[3];
const toFolder = process.argv[4];

if (!taskId || !fromFolder || !toFolder) {
  console.log('Usage: node scripts/move-task.mjs <task-id> <from-folder> <to-folder>');
  console.log('Example: node scripts/move-task.mjs TASK-0002 backlog ready');
  console.log(`Valid folders: ${VALID_FOLDERS.join(', ')}`);
  process.exit(1);
}

if (!VALID_FOLDERS.includes(fromFolder)) {
  console.log(`ERROR: Invalid source folder "${fromFolder}". Must be one of: ${VALID_FOLDERS.join(', ')}`);
  process.exit(1);
}

if (!VALID_FOLDERS.includes(toFolder)) {
  console.log(`ERROR: Invalid destination folder "${toFolder}". Must be one of: ${VALID_FOLDERS.join(', ')}`);
  process.exit(1);
}

if (fromFolder === toFolder) {
  console.log('ERROR: Source and destination folders are the same.');
  process.exit(1);
}

// Prevent moving to done without review
if (toFolder === 'done' && fromFolder !== 'review') {
  console.log('WARNING: Moving task directly to done/ without review. Only an independent reviewer should do this.');
  console.log('Normal path: in-progress → review → done');
}

if (toFolder === 'ready') {
  const content = readFileSync(srcFile, 'utf-8');
  if (!content.includes('## Context Snapshot')) {
    console.log('ERROR: Task cannot move to ready/ without a Context Snapshot.');
    process.exit(1);
  }
}

const srcFile = join(tasksDir, fromFolder, `${taskId}.md`);
const destFile = join(tasksDir, toFolder, `${taskId}.md`);

if (!existsSync(srcFile)) {
  console.log(`ERROR: Task file not found: ${srcFile}`);
  process.exit(1);
}

if (existsSync(destFile)) {
  console.log(`ERROR: Task already exists at destination: ${destFile}`);
  process.exit(1);
}

// Ensure destination directory exists
const destDir = join(tasksDir, toFolder);
if (!existsSync(destDir)) {
  mkdirSync(destDir, { recursive: true });
}

renameSync(srcFile, destFile);
console.log(`Moved ${taskId}: ${fromFolder}/ → ${toFolder}/`);
