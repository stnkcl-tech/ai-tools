---
name: eng-documentation
description: "Comprehensive technical documentation including API specs, changelogs, architecture docs, ADRs, and migration guides. Use when documenting APIs, writing design specs, generating changelogs, creating READMEs, or planning version upgrades."
---

# Engineering Documentation

Deep technical documentation for engineering work — APIs, architecture, changelogs, and migration paths. While `core-documentation` covers the basics (comments, READMEs), this skill handles the heavy-duty docs that ship with production systems.

## When to Use

- Documenting REST/GraphQL APIs (OpenAPI/Swagger specs)
- Writing architecture docs and design specifications
- Creating Architecture Decision Records (ADRs)
- Generating changelogs from git history
- Writing migration guides for version upgrades
- Creating SDK integration guides
- Documenting breaking changes and upgrade paths

## API Documentation

### Document as You Build

- Document APIs during development, not after
- Keep docs in sync with code — when the endpoint changes, the spec changes
- Use real working examples, not placeholders
- Show both success and error cases with status codes
- Version everything including docs

### OpenAPI Structure

Every API spec should include:
- API metadata (title, version, description)
- Server definitions and base paths
- Security schemes (auth methods)
- Paths and operations with HTTP methods
- Request/response schemas with examples
- Error response examples

### SDK & Examples

Provide code examples in the languages your users actually use. Test every example to ensure it works. Include authentication setup, a simple request, and error handling.

## Technical Writing

### Write for Your Audience

- Know their skill level — internal API docs assume different knowledge than public SDK guides
- Use appropriate terminology, but avoid jargon when possible
- Include troubleshooting sections for common mistakes
- Test instructions by following them exactly

### Lead with the Outcome

Start with what the user will accomplish, not how the system works. Show the value before the steps. Use active voice and clear, action-oriented language.

### Documentation Types

| Type | Structure |
|------|-----------|
| **User Guide** | Overview → Prerequisites → Step-by-step → Troubleshooting → Next steps |
| **README** | Title → Description → Features → Install → Quick start → Usage → Contributing |
| **Architecture Doc** | System overview → Component diagram → Design decisions → Data flow → Integration points |
| **ADR** | Context → Decision → Consequences → Status |

## Changelog Generation

Transform git commits into user-friendly release notes:

1. Analyze commit history since last tag or date
2. Categorize changes: ✨ Features, 🔧 Improvements, 🐛 Fixes, ⚠️ Breaking Changes, 🔒 Security
3. Filter out internal commits (refactoring, tests, chores) unless noteworthy
4. Write in customer-facing language — "Fixed issue where large images wouldn't upload" not "fix: resolve buffer overflow in upload handler"
5. Include migration steps for breaking changes

## Migration Guides

When documenting version upgrades:
- **Prerequisites**: Backup, compatibility matrix, deprecation timeline
- **Step-by-step upgrade path**: Exact commands and expected output
- **Breaking changes**: What changed, why, and how to adapt
- **Rollback procedure**: How to revert if something goes wrong
- **Validation checklist**: Tests to run after migration

## Best Practices

- **Real examples only**: Every code sample must be tested and working
- **Error cases included**: Document failure modes, not just happy paths
- **Up-to-date**: Stale documentation is worse than no documentation
- **Versioned**: Docs should match the code version they describe
- **Searchable**: Use clear headings, table of contents, and cross-references
