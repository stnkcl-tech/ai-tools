---
name: eng-caching
description: "Implement caching strategies for APIs, databases, and frontend assets. Use when optimizing response times, reducing database load, or designing cache invalidation."
---

# Caching for Prototypes

Cache expensive work to make your app fast without over-engineering. At 1000 users, in-memory caching or a simple Redis instance covers most needs.

## When to Cache

| Scenario | Cache? | Strategy |
|----------|--------|----------|
| Database query results | Yes | Short TTL (seconds to minutes) |
| API responses | Yes | Cache-Control headers |
| User sessions | Yes | In-memory or Redis |
| Static assets | Yes | CDN + long cache headers |
| Real-time data | No | Stale data is worse than slow |
| Write-heavy data | No | Cache invalidation becomes a nightmare |

## Caching Strategies

### 1. In-Memory Cache (Node.js / Python)

Simplest option — data lives in process memory.

```javascript
// Simple in-memory cache with TTL
const cache = new Map();

function getCached(key, ttlMs, fetchFn) {
  const cached = cache.get(key);
  if (cached && Date.now() - cached.time < ttlMs) {
    return cached.value;
  }
  const value = fetchFn();
  cache.set(key, { value, time: Date.now() });
  return value;
}

// Usage
const user = await getCached(`user:${userId}`, 60000, () => db.users.findById(userId));
```

**Limitations:**
- Cleared on server restart
- Not shared across processes
- Memory usage grows unbounded without eviction

### 2. Redis Cache

Shared cache across all server instances. The standard for production.

```javascript
import { Redis } from 'ioredis';
const redis = new Redis(process.env.REDIS_URL);

async function getCached(key, ttlSeconds, fetchFn) {
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached);
  
  const value = await fetchFn();
  await redis.setex(key, ttlSeconds, JSON.stringify(value));
  return value;
}
```

**When to use Redis:**
- Multiple server instances
- Cache needs to survive deploys
- Need cache eviction policies (LRU)

### 3. HTTP Cache Headers

Let the browser and CDNs cache for you.

```javascript
// Cache API responses
res.set('Cache-Control', 'public, max-age=300'); // 5 minutes

// Never cache authenticated data
res.set('Cache-Control', 'private, no-store');

// Cache static assets forever (with hash in filename)
res.set('Cache-Control', 'public, max-age=31536000, immutable');
```

### 4. Database Query Cache

Some ORMs have built-in query caching:

```python
# Django
from django.core.cache import cache

def get_user(user_id):
    return cache.get_or_set(f'user:{user_id}', 
                           lambda: User.objects.get(id=user_id), 
                           timeout=300)
```

## Cache Invalidation

### Strategies

| Strategy | When to Use |
|----------|-------------|
| **TTL (Time to Live)** | Default — cache expires after N seconds |
| **Write-through** | Update cache when DB is updated |
| **Cache-aside** | Check cache, fetch from DB on miss, write to cache |
| **Invalidate on write** | Delete cache key when data changes |

### Example: Cache-Aside Pattern

```javascript
async function getPost(postId) {
  // 1. Check cache
  const cached = await redis.get(`post:${postId}`);
  if (cached) return JSON.parse(cached);
  
  // 2. Fetch from DB
  const post = await db.posts.findById(postId);
  
  // 3. Store in cache
  await redis.setex(`post:${postId}`, 300, JSON.stringify(post));
  
  return post;
}

async function updatePost(postId, data) {
  // 1. Update DB
  const post = await db.posts.update(postId, data);
  
  // 2. Invalidate cache
  await redis.del(`post:${postId}`);
  
  return post;
}
```

## CDN Caching

For static assets (images, CSS, JS, fonts):
- Upload to CDN (Cloudflare, Bunny.net, S3 + CloudFront)
- Use versioned filenames: `app.v2.js`, `logo.abc123.png`
- Set `Cache-Control: max-age=31536000` for versioned assets

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|----------|---------------|
| Cache everything | Cache only expensive, read-heavy operations |
| Infinite TTL | Set reasonable TTLs (seconds to hours) |
| Cache user-specific data without userId in key | Include userId or use `private` cache headers |
| Ignore cache invalidation | Plan invalidation strategy upfront |
| Cache write operations | Never cache mutations |
| Use cache as primary data store | Cache is ephemeral — DB is source of truth |
