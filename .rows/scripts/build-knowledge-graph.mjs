#!/usr/bin/env node
// build-knowledge-graph.mjs — Generate the ROWS knowledge graph and repo map.

import {
  existsSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  statSync,
  writeFileSync
} from 'fs';
import { createHash } from 'crypto';
import { dirname, join, relative, resolve } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');

const graphPath = join(root, 'agent-os', 'state', 'knowledge-graph.json');
const mapPath = join(root, 'docs', '04-research', 'repo-map.md');
const dependencyMapPath = join(root, 'agent-os', 'state', 'dependency-map.json');

const args = new Set(process.argv.slice(2));
const checkMode = args.has('--check');

const existingGraph = existsSync(graphPath) ? JSON.parse(read(graphPath)) : null;

const lifecycleFolders = ['backlog', 'ready', 'claimed', 'in-progress', 'review', 'blocked', 'done'];
const decisionRegisterPath = join(root, 'agent-os', 'state', 'decision-register.json');

function read(filePath) {
  return readFileSync(filePath, 'utf-8');
}

function walk(dir, files = []) {
  if (!existsSync(dir)) return files;
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    const relativePath = rel(full);
    const stats = statSync(full);
    if (stats.isDirectory()) {
      if (entry !== 'node_modules' && entry !== '.git') {
        if (relativePath.startsWith('agent-os/reports/') && !relativePath.endsWith('reports')) {
          continue;
        }
        walk(full, files);
      }
    } else {
      if (relativePath.startsWith('agent-os/reports/') && relativePath !== 'agent-os/reports/promotion-log.md') {
        continue;
      }
      files.push(full);
    }
  }
  return files;
}

function rel(filePath) {
  return relative(root, filePath).replace(/\\/g, '/');
}

function normalizeTargetPath(fromFile, rawTarget) {
  if (!rawTarget) return null;
  if (rawTarget.startsWith('http://') || rawTarget.startsWith('https://') || rawTarget.startsWith('mailto:') || rawTarget.startsWith('#')) {
    return null;
  }
  const [pathOnly] = rawTarget.split('#');
  if (!pathOnly) return null;
  return rel(resolve(dirname(fromFile), pathOnly));
}

function slugify(value) {
  return String(value || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 60) || 'item';
}

function parseMarkdownLinks(content) {
  const regex = /\[([^\]]+)\]\(([^)]+)\)/g;
  const links = [];
  let match;
  while ((match = regex.exec(content)) !== null) {
    links.push({ label: match[1], target: match[2] });
  }
  return links;
}

function parseBulletItems(sectionText) {
  return sectionText
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line.startsWith('- '))
    .map((line) => line.slice(2).trim())
    .filter(Boolean);
}

function getSection(content, heading) {
  const escaped = heading.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const pattern = new RegExp(`^## ${escaped}\\s*$([\\s\\S]*?)(?=^## |\\Z)`, 'm');
  const match = content.match(pattern);
  return match ? match[1].trim() : '';
}

function getSubsection(content, heading) {
  const escaped = heading.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const pattern = new RegExp(`^### ${escaped}\\s*$([\\s\\S]*?)(?=^### |^## |\\Z)`, 'm');
  const match = content.match(pattern);
  return match ? match[1].trim() : '';
}

function parseTaskFields(content) {
  const titleMatch = content.match(/^#\s+([A-Z]+-\d+):\s+(.+)$/m);
  const taskId = titleMatch?.[1] || null;
  const title = titleMatch?.[2]?.trim() || '';
  const status = getSection(content, 'Status').split('\n')[0]?.trim() || '';
  const deps = parseBulletItems(getSection(content, 'Dependencies'))
    .map((line) => {
      const id = line.match(/TASK-\d+/)?.[0];
      return id;
    })
    .filter(Boolean);
  const blockedByMatch = content.match(/^blocked_by:\s*\[([^\]]*)\]/m);
  const blockedBy = blockedByMatch?.[1]
    ? blockedByMatch[1].split(',').map((item) => item.trim()).filter(Boolean)
    : [];
  const blockerId = content.match(/^blocker_id:\s*(.+)$/m)?.[1]?.trim() || '~';
  const relatedAdrs = parseBulletItems(getSection(content, 'Related ADRs'))
    .map((line) => line.match(/ADR-\d+/)?.[0])
    .filter(Boolean);
  const relatedDecisions = parseBulletItems(getSection(content, 'Related Decisions'))
    .map((line) => line.match(/ADR-\d+|BLOCKER-\d+/)?.[0] || line)
    .filter(Boolean);
  const requiredReading = parseMarkdownLinks(getSection(content, 'Required Reading'))
    .map((entry) => entry.target);
  const contextLinks = parseMarkdownLinks(getSubsection(getSection(content, 'Context Snapshot'), 'Required Context Links'))
    .map((entry) => entry.target);

  return {
    taskId,
    title,
    status,
    deps,
    blockedBy,
    blockerId,
    relatedAdrs,
    relatedDecisions,
    requiredReading,
    contextLinks
  };
}

function parseHandoffFields(content) {
  const taskId = content.match(/TASK-\d+/)?.[0] || null;
  const relatedDecisions = parseBulletItems(getSection(content, 'Related Decisions'))
    .map((line) => line.match(/ADR-\d+|BLOCKER-\d+/)?.[0] || line)
    .filter(Boolean);
  const relatedAdrs = parseBulletItems(getSection(content, 'Related ADRs'))
    .map((line) => line.match(/ADR-\d+/)?.[0])
    .filter(Boolean);
  return { taskId, relatedDecisions, relatedAdrs };
}

function parseBlockerFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  const block = match ? match[1] : '';
  const record = {};
  for (const line of block.split('\n')) {
    const kv = line.match(/^([a-z_]+):\s*(.+)$/);
    if (kv) record[kv[1]] = kv[2].trim();
  }
  const relatedDecisions = parseBulletItems(getSection(content, 'Related Decisions'))
    .map((line) => line.match(/ADR-\d+|BLOCKER-\d+/)?.[0] || line)
    .filter(Boolean);
  const relatedAdrs = parseBulletItems(getSection(content, 'Related ADRs'))
    .map((line) => line.match(/ADR-\d+/)?.[0])
    .filter(Boolean);
  return { ...record, relatedDecisions, relatedAdrs };
}

function getNodeKind(filePath) {
  const path = rel(filePath);
  if (path === 'PROJECT_GOAL.md') return 'project-goal';
  if (path === 'PROJECT_CONTEXT.md') return 'project-context';
  if (path === 'AGENTS.md') return 'rules';
  if (path === 'agent-os/BOOTSTRAP.md') return 'bootstrap';
  if (path.startsWith('agent-os/tasks/')) return 'task';
  if (path.startsWith('agent-os/handoffs/')) return 'handoff';
  if (path.startsWith('agent-os/blockers/')) return 'blocker';
  if (path.startsWith('agent-os/skills/')) return 'skill';
  if (path.startsWith('agent-os/protocols/')) return 'protocol';
  if (path.startsWith('agent-os/agents/')) return 'onboarding';
  if (path.startsWith('docs/02-architecture/decisions/')) return 'adr';
  if (path === 'docs/05-decisions/decision-register.md') return 'decision-register-doc';
  if (path === 'agent-os/state/decision-register.json') return 'decision-register-json';
  if (path.startsWith('docs/')) return 'doc';
  if (path.startsWith('.github/workflows/')) return 'workflow';
  if (path.startsWith('scripts/')) return 'script';
  if (path.startsWith('agent-os/state/')) return 'state';
  return 'file';
}

const nodes = new Map();
const edges = [];
const reverseRefs = new Map();
const ignoredForOrphans = new Set([
  'agent-os/handoffs/active/EXAMPLE-handoff.md',
  'agent-os/tasks/backlog/TASK-0001-initialize-project-from-goal.md'
]);

function ensureNode(path, partial = {}) {
  const key = path.replace(/\\/g, '/');
  if (!nodes.has(key)) {
    nodes.set(key, {
      id: key,
      path: key,
      kind: partial.kind || getNodeKind(key),
      label: partial.label || key.split('/').pop(),
      title: partial.title || partial.label || key.split('/').pop(),
      tags: partial.tags || []
    });
  } else {
    const current = nodes.get(key);
    nodes.set(key, {
      ...current,
      ...partial,
      id: key,
      path: key,
      kind: partial.kind || current.kind
    });
  }
  return nodes.get(key);
}

function addEdge(source, target, type, options = {}) {
  if (!source || !target || source === target) return;
  ensureNode(source);
  ensureNode(target);
  const edge = {
    source,
    target,
    type,
    structural: Boolean(options.structural),
    source_section: options.sourceSection || null,
    target_kind: nodes.get(target)?.kind || null,
    confidence: options.confidence || 'high'
  };
  const key = JSON.stringify(edge);
  if (!reverseRefs.has(key)) {
    reverseRefs.set(key, true);
    edges.push(edge);
  }
}

// Seed known key nodes.
[
  'AGENTS.md',
  'PROJECT_GOAL.md',
  'PROJECT_CONTEXT.md',
  'agent-os/BOOTSTRAP.md',
  'agent-os/knowledge-model.md',
  'docs/04-research/repo-map.md',
  'agent-os/state/knowledge-graph.json',
  'agent-os/state/decision-register.json',
  'docs/05-decisions/decision-register.md'
].forEach((path) => ensureNode(path));

const allFiles = walk(root)
  .filter((filePath) => {
    const relativePath = rel(filePath);
    return !relativePath.startsWith('.git/');
  });

for (const filePath of allFiles) {
  const relativePath = rel(filePath);
  const kind = getNodeKind(filePath);
  const content = read(filePath);
  const title = content.match(/^#\s+(.+)$/m)?.[1]?.trim() || relativePath.split('/').pop();
  ensureNode(relativePath, { kind, title, label: title });

  if (filePath.endsWith('.md')) {
    for (const link of parseMarkdownLinks(content)) {
      const normalized = normalizeTargetPath(filePath, link.target);
      if (normalized) {
        addEdge(relativePath, normalized, kind === 'bootstrap' || kind === 'onboarding' ? 'onboards_to' : 'links_to', {
          structural: kind === 'bootstrap' || kind === 'onboarding' || relativePath.startsWith('agent-os/skills/'),
          sourceSection: 'markdown-link'
        });
      }
    }
  }

  if (kind === 'task') {
    const fields = parseTaskFields(content);
    if (fields.taskId) {
      ensureNode(relativePath, {
        title: `${fields.taskId}: ${fields.title}`,
        label: fields.taskId,
        task_id: fields.taskId,
        status: fields.status
      });
    }
    for (const dep of fields.deps) {
      const target = lifecycleFolders
        .map((folder) => `agent-os/tasks/${folder}/${dep}.md`)
        .find((candidate) => nodes.has(candidate) || existsSync(join(root, candidate)));
      if (target) addEdge(relativePath, target, 'depends_on', { sourceSection: 'Dependencies' });
    }
    for (const dep of fields.blockedBy) {
      const target = lifecycleFolders
        .map((folder) => `agent-os/tasks/${folder}/${dep}.md`)
        .find((candidate) => nodes.has(candidate) || existsSync(join(root, candidate)));
      if (target) addEdge(relativePath, target, 'blocked_by', { sourceSection: 'blocked_by' });
    }
    if (fields.blockerId && fields.blockerId !== '~') {
      const target = allFiles
        .map(rel)
        .find((candidate) => candidate.startsWith(`agent-os/blockers/${fields.blockerId}`));
      if (target) addEdge(relativePath, target, 'blocked_by_blocker', { sourceSection: 'Blocker Fields' });
    }
    for (const adr of fields.relatedAdrs) {
      const target = allFiles
        .map(rel)
        .find((candidate) => candidate.startsWith(`docs/02-architecture/decisions/${adr}`));
      if (target) addEdge(relativePath, target, 'implements_adr', { sourceSection: 'Related ADRs' });
    }
    for (const decision of fields.relatedDecisions) {
      if (decision.startsWith('ADR-')) {
        const target = allFiles
          .map(rel)
          .find((candidate) => candidate.startsWith(`docs/02-architecture/decisions/${decision}`));
        if (target) addEdge(relativePath, target, 'cites_decision', { sourceSection: 'Related Decisions' });
      }
    }
    for (const targetPath of [...fields.requiredReading, ...fields.contextLinks]) {
      const normalized = normalizeTargetPath(filePath, targetPath);
      if (normalized) addEdge(relativePath, normalized, 'requires_reading', { sourceSection: 'Required Reading' });
    }
  }

  if (kind === 'handoff') {
    const fields = parseHandoffFields(content);
    if (fields.taskId) {
      const target = lifecycleFolders
        .map((folder) => `agent-os/tasks/${folder}/${fields.taskId}.md`)
        .find((candidate) => nodes.has(candidate) || existsSync(join(root, candidate)));
      if (target) addEdge(relativePath, target, 'handoff_for', { sourceSection: 'Metadata' });
    }
    for (const adr of fields.relatedAdrs) {
      const target = allFiles
        .map(rel)
        .find((candidate) => candidate.startsWith(`docs/02-architecture/decisions/${adr}`));
      if (target) addEdge(relativePath, target, 'cites_decision', { sourceSection: 'Related ADRs' });
    }
    for (const decision of fields.relatedDecisions) {
      if (decision.startsWith('ADR-')) {
        const target = allFiles
          .map(rel)
          .find((candidate) => candidate.startsWith(`docs/02-architecture/decisions/${decision}`));
        if (target) addEdge(relativePath, target, 'cites_decision', { sourceSection: 'Related Decisions' });
      }
    }
  }

  if (kind === 'blocker') {
    const fields = parseBlockerFrontmatter(content);
    if (fields.id) {
      ensureNode(relativePath, {
        label: fields.id,
        title: `${fields.id} — ${title.replace(/^#\s*/, '')}`
      });
    }
    if (fields.task_id) {
      const target = lifecycleFolders
        .map((folder) => `agent-os/tasks/${folder}/${fields.task_id}.md`)
        .find((candidate) => nodes.has(candidate) || existsSync(join(root, candidate)));
      if (target) addEdge(relativePath, target, 'blocks_task', { sourceSection: 'frontmatter' });
    }
    for (const adr of fields.relatedAdrs) {
      const target = allFiles
        .map(rel)
        .find((candidate) => candidate.startsWith(`docs/02-architecture/decisions/${adr}`));
      if (target) addEdge(relativePath, target, 'cites_decision', { sourceSection: 'Related ADRs' });
    }
  }
}

// Decision register JSON edges.
if (existsSync(decisionRegisterPath)) {
  const register = JSON.parse(read(decisionRegisterPath));
  for (const decision of register.decisions || []) {
    const adrPath = decision.file?.replace(/\\/g, '/');
    if (adrPath) {
      ensureNode(adrPath, {
        kind: 'adr',
        label: decision.adr,
        title: `${decision.adr}: ${decision.title}`
      });
      addEdge('agent-os/state/decision-register.json', adrPath, 'indexes_decision', {
        sourceSection: 'decisions'
      });
      addEdge('docs/05-decisions/decision-register.md', adrPath, 'indexes_decision', {
        sourceSection: 'Decisions'
      });
    }
  }
}

// Reverse task dependency edges.
for (const edge of [...edges]) {
  if (edge.type === 'depends_on' || edge.type === 'blocked_by') {
    addEdge(edge.target, edge.source, 'blocks', { sourceSection: 'generated', confidence: 'derived' });
  }
}

// Generated-from edges.
addEdge('docs/05-decisions/decision-register.md', 'agent-os/state/decision-register.json', 'generated_from', {
  sourceSection: 'header',
  confidence: 'high'
});
addEdge('docs/04-research/repo-map.md', 'agent-os/state/knowledge-graph.json', 'generated_from', {
  sourceSection: 'header',
  confidence: 'high'
});

const orphanCandidates = [];
for (const node of nodes.values()) {
  if (ignoredForOrphans.has(node.path)) continue;
  const incoming = edges.filter((edge) => edge.target === node.path);
  const outgoing = edges.filter((edge) => edge.source === node.path);
  const isReadme = /README\.md$/.test(node.path);
  const isExample = node.path.includes('/EXAMPLE') || node.path.includes('/examples/');
  const canIgnore = isReadme || isExample;
  if (!canIgnore && incoming.length === 0 && outgoing.length === 0) {
    orphanCandidates.push(node);
  }
}

const taskNodes = Array.from(nodes.values()).filter((node) => node.kind === 'task');
const adrNodes = Array.from(nodes.values()).filter((node) => node.kind === 'adr');
const skillNodes = Array.from(nodes.values()).filter((node) => node.kind === 'skill');
const handoffNodes = Array.from(nodes.values()).filter((node) => node.kind === 'handoff' && node.path.startsWith('agent-os/handoffs/active/'));

const orphanSummary = {
  adrs: adrNodes.filter((node) => edges.every((edge) => edge.target !== node.path && edge.source !== node.path)).map((node) => node.path),
  skills: skillNodes.filter((node) => edges.every((edge) => edge.target !== node.path && edge.source !== node.path)).map((node) => node.path),
  handoffs: handoffNodes.filter((node) => edges.every((edge) => edge.source !== node.path || edge.type !== 'handoff_for')).map((node) => node.path),
  all: orphanCandidates.map((node) => node.path)
};

const dependencyEntries = taskNodes
  .filter((node) => node.task_id)
  .map((node) => {
    const outgoingDeps = edges
      .filter((edge) => edge.source === node.path && (edge.type === 'depends_on' || edge.type === 'blocked_by'))
      .map((edge) => nodes.get(edge.target)?.label || edge.target.match(/TASK-\d+/)?.[0] || edge.target);
    const blocks = edges
      .filter((edge) => edge.source === node.path && edge.type === 'blocks')
      .map((edge) => nodes.get(edge.target)?.label || edge.target.match(/TASK-\d+/)?.[0] || edge.target);
    return {
      task_id: node.task_id,
      depends_on: outgoingDeps.filter((value, index, array) => array.indexOf(value) === index),
      blocked_by: [],
      blocks: blocks.filter((value, index, array) => array.indexOf(value) === index)
    };
  });

const generatedAt = checkMode && existingGraph?.generated_at
  ? existingGraph.generated_at
  : new Date().toISOString();
const graph = {
  generated_at: generatedAt,
  source_commit_hint: createHash('sha1').update(edges.map((edge) => JSON.stringify(edge)).join('\n')).digest('hex').slice(0, 12),
  node_count: nodes.size,
  edge_count: edges.length,
  nodes: Array.from(nodes.values()).sort((a, b) => a.path.localeCompare(b.path)),
  edges: edges.sort((a, b) => JSON.stringify(a).localeCompare(JSON.stringify(b))),
  orphan_summary: orphanSummary
};

const repoMapLines = [
  '# ROWS Repo Map',
  '',
  `> Generated from [agent-os/state/knowledge-graph.json](../../agent-os/state/knowledge-graph.json) by \`npm run graph:build\`.`,
  '',
  '## Generated Metadata',
  '',
  `- Generated at: ${generatedAt}`,
  `- Nodes: ${graph.node_count}`,
  `- Edges: ${graph.edge_count}`,
  `- Orphans flagged: ${orphanSummary.all.length}`,
  '',
  '## Executive Summary',
  '',
  `- Tasks mapped: ${taskNodes.length}`,
  `- ADRs mapped: ${adrNodes.length}`,
  `- Active handoffs mapped: ${handoffNodes.length}`,
  `- Skills mapped: ${skillNodes.length}`,
  '',
  '## Task Dependency Graph',
  '',
  '| Task | Status | Depends on | Blocks |',
  '|---|---|---|---|',
  ...taskNodes
    .filter((node) => node.task_id)
    .sort((a, b) => a.label.localeCompare(b.label))
    .map((node) => {
      const dependsOn = edges
        .filter((edge) => edge.source === node.path && (edge.type === 'depends_on' || edge.type === 'blocked_by'))
        .map((edge) => nodes.get(edge.target)?.label || edge.target)
        .join(', ') || 'none';
      const blocks = edges
        .filter((edge) => edge.source === node.path && edge.type === 'blocks')
        .map((edge) => nodes.get(edge.target)?.label || edge.target)
        .join(', ') || 'none';
      return `| [${node.label}](../../${node.path}) | ${node.status || 'unknown'} | ${dependsOn} | ${blocks} |`;
    }),
  '',
  '## ADR and Decision Coverage',
  '',
  '| ADR | Referenced by |',
  '|---|---|',
  ...adrNodes
    .sort((a, b) => a.label.localeCompare(b.label))
    .map((node) => {
      const refs = edges
        .filter((edge) => edge.target === node.path && ['implements_adr', 'cites_decision', 'indexes_decision'].includes(edge.type))
        .map((edge) => nodes.get(edge.source)?.label || edge.source)
        .filter((value, index, array) => array.indexOf(value) === index)
        .join(', ') || 'none';
      return `| [${node.label}](../../${node.path}) | ${refs} |`;
    }),
  '',
  '## Handoff Context Flow',
  '',
  '| Handoff | Task | Distilled? |',
  '|---|---|---|',
  ...handoffNodes
    .sort((a, b) => a.path.localeCompare(b.path))
    .map((node) => {
      const task = edges.find((edge) => edge.source === node.path && edge.type === 'handoff_for');
      const distilled = edges.some((edge) => edge.source === 'PROJECT_CONTEXT.md' && edge.target === node.path);
      return `| [${node.path.split('/').pop()}](../../${node.path}) | ${task ? nodes.get(task.target)?.label || task.target : 'none'} | ${distilled ? 'yes' : 'no'} |`;
    }),
  '',
  '## Onboarding and Skill Entry Points',
  '',
  '| Source | Target | Type |',
  '|---|---|---|',
  ...edges
    .filter((edge) => edge.type === 'onboards_to' || (edge.type === 'links_to' && edge.structural))
    .sort((a, b) => `${a.source}:${a.target}`.localeCompare(`${b.source}:${b.target}`))
    .slice(0, 60)
    .map((edge) => `| [${edge.source}](../../${edge.source}) | [${edge.target}](../../${edge.target}) | ${edge.type} |`),
  '',
  '## Skills and Protocol Usage',
  '',
  '| Skill/Protocol | Referenced by |',
  '|---|---|',
  ...Array.from(nodes.values())
    .filter((node) => node.kind === 'skill' || node.kind === 'protocol')
    .sort((a, b) => a.path.localeCompare(b.path))
    .map((node) => {
      const refs = edges
        .filter((edge) => edge.target === node.path)
        .map((edge) => nodes.get(edge.source)?.path || edge.source)
        .filter((value, index, array) => array.indexOf(value) === index)
        .join(', ') || 'none';
      return `| [${node.path.split('/').pop()}](../../${node.path}) | ${refs} |`;
    }),
  '',
  '## Orphans and Warnings',
  '',
  `- ADRs with no meaningful references: ${orphanSummary.adrs.length ? orphanSummary.adrs.join(', ') : 'none'}`,
  `- Skills with no meaningful references: ${orphanSummary.skills.length ? orphanSummary.skills.join(', ') : 'none'}`,
  `- Active handoffs with no task edge: ${orphanSummary.handoffs.length ? orphanSummary.handoffs.join(', ') : 'none'}`,
  `- All other orphan candidates: ${orphanSummary.all.length ? orphanSummary.all.join(', ') : 'none'}`,
  '',
  '## How to Refresh',
  '',
  '```bash',
  'npm run graph:build',
  'npm run validate:graph',
  '```',
  ''
];

const graphJson = `${JSON.stringify(graph, null, 2)}\n`;
const repoMap = `${repoMapLines.join('\n')}\n`;
const dependencyMap = `${JSON.stringify({
  description: 'Dependency map for tasks in the ROWS system. Tracks which tasks depend on which other tasks.',
  schema: {
    task_id: 'string — the dependent task',
    depends_on: ['array of task IDs this task depends on'],
    blocked_by: ['array of task IDs currently blocking this task'],
    blocks: ['array of task IDs this task blocks']
  },
  dependencies: dependencyEntries,
  last_updated: generatedAt
}, null, 2)}\n`;

function compareOrWrite(path, nextContent) {
  const current = existsSync(path) ? read(path) : null;
  if (checkMode) {
    if (current !== nextContent) {
      throw new Error(`${rel(path)} is out of date. Run npm run graph:build.`);
    }
    return;
  }
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, nextContent);
}

try {
  compareOrWrite(graphPath, graphJson);
  compareOrWrite(mapPath, repoMap);
  compareOrWrite(dependencyMapPath, dependencyMap);
  if (!checkMode) {
    console.log(`Wrote ${rel(graphPath)}`);
    console.log(`Wrote ${rel(mapPath)}`);
    console.log(`Wrote ${rel(dependencyMapPath)}`);
  } else {
    console.log('Knowledge graph outputs are up to date.');
  }
} catch (error) {
  console.error(error.message);
  process.exit(1);
}
