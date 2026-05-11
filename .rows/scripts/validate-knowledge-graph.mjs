#!/usr/bin/env node
// validate-knowledge-graph.mjs — Ensure generated graph artifacts are current.

import { execFileSync } from 'child_process';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');

try {
  execFileSync(process.execPath, [join(root, 'scripts', 'build-knowledge-graph.mjs'), '--check'], {
    cwd: root,
    stdio: 'inherit'
  });
} catch (error) {
  process.exit(error.status || 1);
}
