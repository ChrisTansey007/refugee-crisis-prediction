#!/usr/bin/env node
// validate-links.mjs — Scan Markdown files for broken relative links.

import { readFileSync, readdirSync, existsSync, statSync, writeFileSync, mkdirSync } from 'fs';
import { join, dirname, relative, resolve } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');

function walkMd(dir, files = []) {
  if (!existsSync(dir)) return files;
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) {
      if (!entry.startsWith('.git') && entry !== 'node_modules') {
        walkMd(full, files);
      }
    } else if (entry.endsWith('.md')) {
      files.push(full);
    }
  }
  return files;
}

const mdFiles = walkMd(root);
const linkRegex = /\[([^\]]*)\]\(([^)]+)\)/g;
let broken = 0;
let checked = 0;
const brokenLinks = [];

for (const file of mdFiles) {
  const content = readFileSync(file, 'utf-8');
  const fileDir = dirname(file);
  let match;
  while ((match = linkRegex.exec(content)) !== null) {
    const [, , rawUrl] = match;
    // Skip external URLs, mailto, anchors-only
    if (rawUrl.startsWith('http://') || rawUrl.startsWith('https://') || rawUrl.startsWith('mailto:')) continue;
    // Skip pure anchor links
    if (rawUrl.startsWith('#')) continue;

    // Resolve relative to the file's directory
    const [pathPart] = rawUrl.split('#');
    if (!pathPart) continue;

    const resolved = resolve(fileDir, pathPart);
    checked++;
    if (!existsSync(resolved)) {
      broken++;
      const relFile = relative(root, file);
      brokenLinks.push({ file: relFile, link: rawUrl, resolved: relative(root, resolved) });
      console.log(`BROKEN: ${relFile} → ${rawUrl}`);
    }
  }
}

// Write report
const reportsDir = join(root, 'agent-os', 'reports', 'links');
if (!existsSync(reportsDir)) mkdirSync(reportsDir, { recursive: true });

const now = new Date().toISOString().split('T')[0];
const report = [
  `# Link Validation Report — ${now}`,
  `> Generated: ${new Date().toISOString()}`,
  '',
  `- Total links checked: ${checked}`,
  `- Broken links: ${broken}`,
  '',
  brokenLinks.length > 0 ? '## Broken Links' : '## No broken links found.',
  ...brokenLinks.map(b => `- \`${b.file}\` → \`${b.link}\``),
  ''
].join('\n');

writeFileSync(join(reportsDir, `links-${now}.md`), report);
console.log(`\nLink Validation Results:`);
console.log(`  Checked: ${checked}`);
console.log(`  Broken:  ${broken}`);
console.log(`  Report:  agent-os/reports/links/links-${now}.md`);

if (broken > 0) {
  process.exit(1);
}
