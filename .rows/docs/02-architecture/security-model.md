# Security Model

> **Customize after forking. Defines the security architecture of [PROJECT_NAME].**

## Authentication

- **Method:** [JWT / OAuth 2.0 / Session-based / API keys]
- **Token storage:** [HTTP-only cookies / localStorage (avoid if possible) / memory]
- **Token expiry:** [DURATION]

## Authorization

- **Model:** [RBAC / ABAC / custom]
- **Roles:** [ADMIN, USER, etc.]

## Data Protection

- **Encryption at rest:** [YES/NO, method]
- **Encryption in transit:** HTTPS enforced
- **Secrets management:** Environment variables, never committed

## Input Validation

- All inputs validated at the API boundary.
- SQL injection prevented via parameterized queries.
- XSS prevented via output encoding.

## Dependencies

- Regular dependency audits (`npm audit`, `pip audit`).
- Dependencies pinned to specific versions.

## Incident Response

- [Describe incident response process or link to runbook]

## Related Files

- [`system-overview.md`](./system-overview.md) — System architecture
- [`api-contracts.md`](./api-contracts.md) — API contracts
- [`../../agent-os/escalation-rules.md`](../../agent-os/escalation-rules.md) — Escalation rules
