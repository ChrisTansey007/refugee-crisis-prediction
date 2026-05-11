# API Contracts

> **Customize after forking. Defines the API surface of [PROJECT_NAME].**

## Base URL

[API_BASE_URL]

## Authentication

[Describe auth method: JWT, OAuth, API keys, etc.]

## Endpoints

### [RESOURCE]

#### `GET /[resource]`
- **Description:** List all [resource].
- **Query params:** `?page=1&limit=20`
- **Response:** `{ data: [...], meta: { page, limit, total } }`

#### `POST /[resource]`
- **Description:** Create a new [resource].
- **Body:** `{ [field]: [value] }`
- **Response:** `{ data: { id, ... } }`

#### `GET /[resource]/:id`
- **Description:** Get a single [resource].
- **Response:** `{ data: { id, ... } }`

#### `PUT /[resource]/:id`
- **Description:** Update a [resource].
- **Body:** `{ [field]: [value] }`
- **Response:** `{ data: { id, ... } }`

#### `DELETE /[resource]/:id`
- **Description:** Delete a [resource].
- **Response:** `{ data: { deleted: true } }`

## Error Format

All errors return:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {}
  }
}
```

## Related Files

- [`system-overview.md`](./system-overview.md) — System architecture
- [`data-model.md`](./data-model.md) — Data model
