# Coding Standards

> **Customize after forking. Coding conventions for [PROJECT_NAME].**

## General

- Write code for readability first, performance second.
- Functions should do one thing and have descriptive names.
- Maximum line length: [100] characters.
- Use [2 / 4] spaces for indentation (no tabs).

## Naming

- **Variables/functions:** camelCase
- **Classes/components:** PascalCase
- **Constants:** UPPER_SNAKE_CASE
- **Files:** kebab-case or PascalCase (match default export)

## Comments

- Comment WHY, not WHAT. The code should explain what.
- No commented-out code in commits. Delete it or restore it.
- Use JSDoc for public APIs.

## Imports

- Group imports: external packages first, then internal modules.
- No circular imports.

## Error Handling

- Never swallow errors silently.
- Use try/catch at async boundaries.
- Provide meaningful error messages.

## Git

- Commit messages: `type(scope): description` (e.g., `feat(auth): add login endpoint`).
- Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`.
- One logical change per commit.

## Related Files

- [`testing-standards.md`](./testing-standards.md) — Testing standards
- [`.claude/rules/`](../../.claude/rules/) — Domain-specific rules
