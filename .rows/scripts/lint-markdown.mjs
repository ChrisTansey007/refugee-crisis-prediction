#!/usr/bin/env node
// lint-markdown.mjs — Lightweight markdown lint for template repos.

import { readdirSync, readFileSync, statSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const skipDirs = new Set(['.git', 'node_modules', 'dist', 'build', 'out', 'coverage']);
const ignorePaths = [join(root, 'agent-os', 'reports')];

function walk(dir, out = []) {
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    const stat = statSync(full);
    if (stat.isDirectory()) {
      if (skipDirs.has(entry)) continue;
      if (ignorePaths.some(prefix => full.startsWith(prefix))) continue;
      walk(full, out);
    } else if (entry.endsWith('.md')) {
      out.push(full);
    }
  }
  return out;
}

const files = walk(root);
const findings = [];

for (const file of files) {
  const lines = readFileSync(file, 'utf8').split(/\r?\n/);
  lines.forEach((line, index) => {
    if (line.includes('\t')) {
      findings.push(`${file}:${index + 1} contains a tab character`);
    }
  });
}

if (findings.length > 0) {
  console.log('Markdown lint failed:');
  for (const finding of findings.slice(0, 50)) console.log(`- ${finding}`);
  process.exit(1);
}

console.log(`Markdown lint passed for ${files.length} files.`);
