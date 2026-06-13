---
name: eng-api-design
description: "Design and build REST or RPC APIs with clear conventions, error handling, versioning, and documentation. Use when creating new endpoints, refactoring APIs, or defining contract boundaries between services."
---

# API Design for Prototypes

Build APIs that are predictable, well-documented, and easy to consume. At 1000 users, clarity beats cleverness — use REST conventions, consistent error formats, and explicit documentation.

## REST Conventions

### URL Design

- Use nouns, not verbs: `/users` not `/getUsers`
- Use plural nouns: `/posts`, `/comments`
- Nested resources for relationships: `/posts/123/comments`
- Filtering/sorting via query params: `/posts?author=alice&sort=created_at`
- Pagination: `?page=2&limit=20` or `?cursor=abc123&limit=20`

### HTTP Methods

| Method | Use | Example |
|--------|-----|---------|
| `GET` | Read | `GET /users/123` |
| `POST` | Create | `POST /users` |
| `PATCH` | Partial update | `PATCH /users/123` |
| `PUT` | Full replace | `PUT /users/123` |
| `DELETE` | Remove | `DELETE /users/123` |

### Status Codes

| Code | When to Use |
|------|-------------|
| `200` | Success |
| `201` | Created |
| `204` | Success, no body |
| `400` | Bad request (client error) |
| `401` | Unauthorized (not authenticated) |
| `403` | Forbidden (no permission) |
| `404` | Resource not found |
| `409` | Conflict (duplicate, state conflict) |
| `422` | Validation error |
| `429` | Rate limited |
| `500` | Server error |

## Request/Response Format

### Consistent Response Shape

```json
{
  "data": { ... },
  "error": null,
  "meta": {
    "page": 2,
    "total": 100
  }
}
```

Or for errors:
```json
{
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "field": "email"
  }
}
```

**Rule**: Always return the same shape. Never return raw arrays at the top level — wrap in `{ data: [...] }`.

### Validation

- Validate at the API boundary (body, query, params)
- Return `422` with specific field-level errors
- Sanitize inputs before database queries (prevent injection)

## Authentication & Authorization

- Authenticate via Bearer token in `Authorization` header
- Check permissions before business logic, not after
- Return `401` for missing/invalid auth, `403` for insufficient permissions

## Versioning

- **Start with v1**: `GET /api/v1/users`
- Don't version until you need to break a contract
- When breaking changes are needed, bump to v2 and keep v1 running

## Documentation

- Auto-generate from code when possible (OpenAPI/Swagger, tRPC, GraphQL introspection)
- Document: endpoints, params, request/response shapes, error codes
- Include example requests for non-trivial endpoints

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|----------|---------------|
| Return raw arrays `[]` | Wrap in `{ data: [...] }` |
| Use verbs in URLs | Use HTTP methods + nouns |
| `200` with error body | Use proper status codes |
| Silent failures | Return explicit errors with codes |
| Deep nesting >3 levels | Flatten or use separate endpoints |
| Undocumented query params | Document all parameters |
