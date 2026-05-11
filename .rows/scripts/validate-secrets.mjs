#!/usr/bin/env node
// validate-secrets.mjs — Lightweight secret-pattern scan for the template repo.

import { existsSync, readFileSync, readdirSync, mkdirSync, writeFileSync, statSync } from 'fs';
import { join, dirname, extname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');

const ALLOWED_EXTENSIONS = new Set([
  '.md', '.txt', '.json', '.yaml', '.yml', '.js', '.mjs', '.ts', '.tsx', '.sh', '.toml', '.ini', '.env', '.example', '.css', '.html'
]);
const SKIP_DIRS = new Set(['.git', 'node_modules', '.turbo', 'dist', 'build', 'coverage']);
const SKIP_PATH_PARTS = ['/reports/', '/.next/', '/.cache/'];

const PATTERNS = [
  { name: 'GitHub token', regex: /gh[pousr]_[A-Za-z0-9_]{20,}/g },
  { name: 'GitHub PAT', regex: /github_pat_[A-Za-z0-9_]{20,}/g },
  { name: 'OpenAI key', regex: /sk-[A-Za-z0-9]{20,}/g },
  { name: 'AWS access key', regex: /AKIA[0-9A-Z]{16}/g },
  { name: 'Google API key', regex: /AIza[0-9A-Za-z\-_]{35}/g },
  { name: 'Slack token', regex: /xox[baprs]-[A-Za-z0-9-]{10,}/g },
  { name: 'Private key block', regex: /-----BEGIN (?:RSA|EC|OPENSSH|DSA|PRIVATE) KEY-----/g }
];

function walk(dir, files = []) {
  if (!existsSync(dir)) return files;
  for (const entry of readdirSync(dir)) {
    if (SKIP_DIRS.has(entry)) continue;
    const full = join(dir, entry);
    const rel = full.replace(root, '').replace(/\\/g, '/');
    if (SKIP_PATH_PARTS.some(part => rel.includes(part))) continue;
    const stat = statSync(full);
    if (stat.isDirectory()) {
      walk(full, files);
      continue;
    }
    const ext = extname(entry).toLowerCase();
    if (ALLOWED_EXTENSIONS.has(ext) || entry === '.env.example' || entry === '.mcp.example.json' || entry === '.gitattributes' || entry === '.editorconfig') {
      files.push(full);
    }
  }
  return files;
}

const files = walk(root);
const findings = [];

for (const file of files) {
  let content;
  try {
    content = readFileSync(file, 'utf-8');
  } catch {
    continue;
  }
  const lines = content.split(/\r?\n/);
  lines.forEach((line, index) => {
    if (line.includes('[REDACTED]')) return;
    for (const pattern of PATTERNS) {
      pattern.regex.lastIndex = 0;
      if (pattern.regex.test(line)) {
        findings.push(`${file.replace(root, '')}:${index + 1}: ${pattern.name}`);
      }
    }
  });
}

const reportsDir = join(root, 'agent-os', 'reports', 'security');
if (!existsSync(reportsDir)) mkdirSync(reportsDir, { recursive: true });
const now = new Date().toISOString().split('T')[0];
const report = [
  `# Secret Scan Report — ${now}`,
  `> Generated: ${new Date().toISOString()}`,
  '',
  `- Files scanned: ${files.length}`,
  `- Findings: ${findings.length}`,
  '',
  findings.length > 0 ? '## Findings' : '## No findings.',
  ...findings.map(item => `- ${item}`),
  ''
].join('\n');
writeFileSync(join(reportsDir, `secret-scan-${now}.md`), report);

console.log('Secret Scan Results:');
console.log(`  Files scanned: ${files.length}`);
console.log(`  Findings: ${findings.length}`);

if (findings.length > 0) {
  console.log('\nFindings:');
  for (const finding of findings) console.log(`  - ${finding}`);
  process.exit(1);
}
