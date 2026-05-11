#!/usr/bin/env node
// validate-mcp.mjs — Validate optional MCP configuration files.

import { existsSync, readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const candidates = ['.mcp.json', '.mcp.example.json'];
const file = candidates.find((name) => existsSync(join(root, name)));

if (!file) {
  console.log('No MCP config found. Skipping validation.');
  process.exit(0);
}

const configPath = join(root, file);
let parsed;
try {
  parsed = JSON.parse(readFileSync(configPath, 'utf-8'));
} catch (error) {
  console.error(`Invalid JSON in ${file}: ${error.message}`);
  process.exit(1);
}

if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
  console.error(`${file} must contain a JSON object.`);
  process.exit(1);
}

if (!parsed.mcpServers || typeof parsed.mcpServers !== 'object' || Array.isArray(parsed.mcpServers)) {
  console.error(`${file} must contain an object at mcpServers.`);
  process.exit(1);
}

const serverNames = Object.keys(parsed.mcpServers);
if (serverNames.length === 0) {
  console.error(`${file} must define at least one MCP server.`);
  process.exit(1);
}

for (const [name, server] of Object.entries(parsed.mcpServers)) {
  if (!server || typeof server !== 'object' || Array.isArray(server)) {
    console.error(`MCP server ${name} must be an object.`);
    process.exit(1);
  }
  const hasCommand = typeof server.command === 'string' && server.command.trim().length > 0;
  const hasUrl = typeof server.url === 'string' && server.url.trim().length > 0;
  if (!hasCommand && !hasUrl) {
    console.error(`MCP server ${name} must define either command or url.`);
    process.exit(1);
  }
}

console.log(`Validated ${file} with ${serverNames.length} server(s).`);
