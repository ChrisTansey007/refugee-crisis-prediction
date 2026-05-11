#!/usr/bin/env node
// validate-json.mjs — Recursively find and validate JSON files.
// If a matching schema exists in agent-os/schemas/, validate structure too.

import { readFileSync, readdirSync, existsSync, statSync, writeFileSync, mkdirSync } from 'fs';
import { join, dirname, basename, relative } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const schemaDir = join(root, 'agent-os', 'schemas');

function walk(dir, files = []) {
  if (!existsSync(dir)) return files;
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) {
      if (!entry.startsWith('.git') && entry !== 'node_modules') {
        walk(full, files);
      }
    } else if (entry.endsWith('.json')) {
      files.push(full);
    }
  }
  return files;
}

function typeOf(value) {
  if (value === null) return 'null';
  if (Array.isArray(value)) return 'array';
  return typeof value;
}

function validateSchema(schema, value, path = '') {
  const errors = [];
  const valueType = typeOf(value);

  if (schema.enum && !schema.enum.includes(value)) {
    errors.push(`${path || '$'} expected one of ${JSON.stringify(schema.enum)}, got ${JSON.stringify(value)}`);
    return errors;
  }

  if (schema.type) {
    const types = Array.isArray(schema.type) ? schema.type : [schema.type];
    if (!types.some((expected) => {
      if (expected === valueType) return true;
      if (expected === 'number' && valueType === 'integer') return true;
      if (expected === 'integer' && valueType === 'number' && Number.isInteger(value)) return true;
      return false;
    })) {
      errors.push(`${path || '$'} expected type ${types.join(' | ')}, got ${valueType}`);
      return errors;
    }
  }

  if (schema.type === 'object' || (Array.isArray(schema.type) && schema.type.includes('object')) || schema.properties || schema.required) {
    if (valueType !== 'object' || value === null || Array.isArray(value)) {
      return errors;
    }
    const required = schema.required || [];
    for (const key of required) {
      if (!(key in value)) {
        errors.push(`${path || '$'} missing required property ${key}`);
      }
    }
    const properties = schema.properties || {};
    for (const [key, subSchema] of Object.entries(properties)) {
      if (key in value) {
        errors.push(...validateSchema(subSchema, value[key], path ? `${path}.${key}` : key));
      }
    }
    if (schema.additionalProperties === false) {
      for (const key of Object.keys(value)) {
        if (!(key in properties)) {
          errors.push(`${path || '$'} has unexpected property ${key}`);
        }
      }
    }
  }

  if (schema.type === 'array' || (Array.isArray(schema.type) && schema.type.includes('array')) || schema.items) {
    if (valueType !== 'array') {
      return errors;
    }
    if (schema.items) {
      for (let i = 0; i < value.length; i += 1) {
        errors.push(...validateSchema(schema.items, value[i], `${path}[${i}]`));
      }
    }
    if (schema.minItems !== undefined && value.length < schema.minItems) {
      errors.push(`${path || '$'} expected at least ${schema.minItems} items`);
    }
  }

  if ((schema.type === 'string' || (Array.isArray(schema.type) && schema.type.includes('string'))) && typeof value === 'string') {
    if (schema.minLength !== undefined && value.length < schema.minLength) {
      errors.push(`${path || '$'} expected string length >= ${schema.minLength}`);
    }
    if (schema.pattern) {
      const re = new RegExp(schema.pattern);
      if (!re.test(value)) {
        errors.push(`${path || '$'} does not match pattern ${schema.pattern}`);
      }
    }
  }

  if ((schema.type === 'number' || schema.type === 'integer' || (Array.isArray(schema.type) && (schema.type.includes('number') || schema.type.includes('integer')))) && typeof value === 'number') {
    if (schema.type === 'integer' && !Number.isInteger(value)) {
      errors.push(`${path || '$'} expected integer, got number`);
    }
    if (schema.minimum !== undefined && value < schema.minimum) {
      errors.push(`${path || '$'} expected >= ${schema.minimum}`);
    }
    if (schema.maximum !== undefined && value > schema.maximum) {
      errors.push(`${path || '$'} expected <= ${schema.maximum}`);
    }
  }

  return errors;
}

function schemaPathFor(file) {
  const name = basename(file);
  if (!name.endsWith('.json')) return null;
  const schemaName = name.replace(/\.json$/, '.schema.json');
  const candidate = join(schemaDir, schemaName);
  return existsSync(candidate) ? candidate : null;
}

const jsonFiles = walk(root);
let valid = 0;
let invalid = 0;
let schemaValidated = 0;

for (const file of jsonFiles) {
  const display = relative(root, file);
  try {
    const raw = readFileSync(file, 'utf-8');
    const data = JSON.parse(raw);
    const schemaPath = schemaPathFor(file);
    if (schemaPath) {
      const schema = JSON.parse(readFileSync(schemaPath, 'utf-8'));
      const errors = validateSchema(schema, data);
      if (errors.length > 0) {
        console.log(`SCHEMA INVALID: ${display}`);
        for (const err of errors) console.log(`  - ${err}`);
        invalid++;
        continue;
      }
      schemaValidated++;
    }
    valid++;
  } catch (e) {
    console.log(`INVALID JSON: ${display} — ${e.message}`);
    invalid++;
  }
}

console.log(`\nJSON Validation Results:`);
console.log(`  Total:           ${jsonFiles.length}`);
console.log(`  Valid:           ${valid}`);
console.log(`  Schema-checked:   ${schemaValidated}`);
console.log(`  Invalid:         ${invalid}`);

if (invalid > 0) {
  process.exit(1);
}
