# Data Model

> **Customize after forking. Defines the data structures and relationships for [PROJECT_NAME].**

## Entities

### [ENTITY_1]
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| [FIELD] | [TYPE] | [CONSTRAINTS] | [DESCRIPTION] |

### [ENTITY_2]
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| [FIELD] | [TYPE] | [CONSTRAINTS] | [DESCRIPTION] |

## Relationships

- [ENTITY_1] has many [ENTITY_2] via [FOREIGN_KEY].
- [Describe other relationships]

## Indexes

- `[INDEX_1]` on `[TABLE]`(`[COLUMNS]`) — `[Purpose]`

## Migrations

All schema changes must be done via migrations. See [`../03-development/setup.md`](../03-development/setup.md) for migration commands.

## Related Files

- [`system-overview.md`](./system-overview.md) — System architecture
- [`api-contracts.md`](./api-contracts.md) — API contracts
