---
name: eng-database-design
description: "Database design for prototypes and early-stage products. Schema design, ORM selection, indexing basics, and safe migrations for small-to-medium scale applications. Use when designing data models, choosing databases, or planning schema evolution."
---

# Database Design for Prototypes

Good database design at the prototype stage means choosing the right tool, modeling data cleanly, and avoiding traps that become expensive later. You don't need to optimize for millions of users yet — but you do need to avoid fundamental mistakes.

## Database Selection

Choose based on your actual needs, not defaults:

| Scenario | Choice | Why |
|----------|--------|-----|
| Single developer, local dev, simple app | **SQLite** | Zero setup, file-based, perfect for prototyping |
| Team collaboration, production deploy, complex queries | **PostgreSQL** | Full relational features, mature, hosts everywhere |
| Serverless/edge deployment | **Neon** or **Supabase** | Managed PostgreSQL, branching for preview envs |

**Prototype rule:** Start with SQLite. Upgrade to PostgreSQL when you need concurrent writers, team collaboration, or hosted production data.

## ORM Selection

| ORM | Best For | Trade-off |
|-----|----------|-----------|
| **Prisma** | TypeScript, schema-first, migrations | Heavier bundle, not edge-ready |
| **Drizzle** | TypeScript, SQL-like, smaller bundle | Newer ecosystem |
| **SQLAlchemy 2.0** | Python, async support | Verbose for simple cases |
| **Raw SQL + query builder** | Complex queries, maximum control | Manual type safety |

**Prototype rule:** Pick the ORM your framework recommends (Prisma for Next.js, SQLAlchemy for FastAPI/Django). Don't optimize for bundle size until you have users.

## Schema Design

### Every Table Gets

```sql
id          UUID or auto-increment PRIMARY KEY
created_at  TIMESTAMPTZ DEFAULT NOW()
updated_at  TIMESTAMPTZ DEFAULT NOW()
-- deleted_at TIMESTAMPTZ  -- only if soft deletes needed
```

### Primary Key Choice

| Type | Use When |
|------|----------|
| **Auto-increment integer** | Simple apps, single database, no security concern |
| **UUID** | Exposed in URLs, distributed systems, or security-sensitive IDs |

**Prototype rule:** Use auto-increment integers internally. Use UUIDs if IDs appear in public URLs.

### Relationships

| Type | Implementation |
|------|----------------|
| One-to-Many | Foreign key on the child table |
| Many-to-Many | Junction table with two foreign keys |
| One-to-One | Separate table with unique foreign key (rarely needed) |

### Foreign Key Behavior

```sql
ON DELETE CASCADE    -- Delete children with parent (e.g., post comments)
ON DELETE SET NULL   -- Keep children, remove reference (e.g., user posts)
ON DELETE RESTRICT   -- Prevent delete if children exist (safety default)
```

### JSONB vs Structured Columns

| Use JSONB | Use Structured Columns |
|-----------|------------------------|
| Flexible schema that changes often | Data you query, filter, or join on |
| Configuration/settings objects | Relational data with clear relationships |
| Logs or event metadata | Data with constraints (NOT NULL, UNIQUE) |

**Prototype rule:** Default to structured columns. Use JSONB only when the schema is genuinely unpredictable.

## Indexing Basics

At 1000 users, you only need basic indexing:

**Always index:**
- Primary keys (automatic)
- Foreign key columns
- Columns in `WHERE`, `JOIN`, and `ORDER BY` clauses
- Unique constraints

**Don't over-index:**
- Write-heavy tables — every index slows down inserts
- Low-cardinality columns (booleans, status enums with 3 values)
- Columns rarely queried

**Prototype rule:** Add indexes when queries are slow. Don't pre-optimize.

## The N+1 Problem

The most common database performance mistake:

```
Bad:  1 query for users + N queries for each user's posts = N+1 queries
Good: 1 JOIN query fetching users + posts together
```

**Fixes:**
- Use JOINs or eager loading in your ORM
- For GraphQL, use DataLoader to batch requests

## Connection Pooling

Even at 1000 users, raw database connections will exhaust without pooling:

- **PostgreSQL default:** 100 max connections
- **Pool size rule:** (core_count × 2) + effective_spindle_count for the app
- **Most ORMs handle this automatically** — just verify it's configured

## Migrations

**Safe prototype approach:**
1. Test migrations on a copy of production data first
2. Have a rollback script ready
3. Make additive changes (add columns) rather than destructive ones (rename/drop)
4. Run migrations in a transaction when possible

**Prototype rule:** You don't need zero-downtime migrations yet. A brief maintenance window is fine.

## Example: Simple Blog Schema

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  published BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE comments (
  id SERIAL PRIMARY KEY,
  post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
  user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for common queries
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_published ON posts(published) WHERE published = TRUE;
CREATE INDEX idx_comments_post_id ON comments(post_id);
```

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|----------|---------------|
| Default to PostgreSQL for everything | Start with SQLite, upgrade when needed |
| Use `SELECT *` in production | Select only columns you need |
| Skip indexing foreign keys | Index FK columns for fast joins |
| Store everything in JSONB | Use structured columns for queryable data |
| Ignore the N+1 problem | Use JOINs or eager loading |
| Hardcode connection limits | Use connection pooling |
