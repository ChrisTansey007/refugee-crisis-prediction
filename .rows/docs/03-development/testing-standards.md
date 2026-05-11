# Testing Standards

> **Customize after forking. Testing conventions for [PROJECT_NAME].**

## Test Types

| Type | Scope | Tool | When to Write |
|------|-------|------|---------------|
| Unit | Single function/component | [Jest/Vitest] | Always |
| Integration | Multiple modules | [Jest/Supertest] | For API endpoints, DB queries |
| E2E | Full user flows | [Playwright/Cypress] | For critical paths |

## Rules

- Every new feature must have tests.
- Bug fixes must include a regression test.
- Tests must be independent and isolated.
- Use descriptive test names: `it('returns 401 when token is expired')`.
- Mock at the boundary, not internals.
- Test error paths as thoroughly as happy paths.

## Coverage

- Target: [80%] line coverage on new code.
- Coverage is a signal, not a goal. 100% of trivial code is noise.

## Running Tests

```bash
npm test              # Run all tests
npm run test:watch    # Watch mode
npm run test:coverage # With coverage
```

## Related Files

- [`coding-standards.md`](./coding-standards.md) — Coding standards
- [`.claude/rules/testing.md`](../../.claude/rules/testing.md) — Testing rules for Claude
- [`../../agent-os/verification-gates.md`](../../agent-os/verification-gates.md) — Verification gates
