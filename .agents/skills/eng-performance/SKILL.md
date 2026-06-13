---
name: eng-performance
description: "Optimize application performance with profiling, database query optimization, bundle size reduction, and caching strategies. Use when apps are slow, pages load slowly, or resource usage is high."
---

# Performance for Prototypes

Make your app fast enough that users don't notice. At 1000 users, performance means efficient database queries, small bundles, and smart caching — not micro-optimizations.

## Database Performance

### Query Optimization

**N+1 Problem:**
```javascript
// ❌ N+1: 1 query for posts + N queries for authors
const posts = await db.posts.findAll();
for (const post of posts) {
  post.author = await db.users.findById(post.authorId); // N queries!
}

// ✅ JOIN: 1 query total
const posts = await db.posts.findAll({
  include: [{ model: db.users, as: 'author' }]
});
```

**Select Only What You Need:**
```javascript
// ❌ Selecting all columns
const users = await db.users.findAll();

// ✅ Selecting only needed columns
const users = await db.users.findAll({
  attributes: ['id', 'name', 'email']
});
```

**Add Indexes:**
```sql
-- Index columns used in WHERE, JOIN, ORDER BY
CREATE INDEX idx_posts_author_id ON posts(author_id);
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);
```

### Connection Pooling

```javascript
// Always use connection pooling
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,        // Max connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000
});
```

## Frontend Performance

### Bundle Size

| Target | Action |
|--------|--------|
| Initial JS < 200KB | Code splitting, tree shaking |
| Images optimized | WebP/AVIF, lazy loading, responsive sizes |
| Fonts subset | Only load needed character sets |
| Dependencies audited | `webpack-bundle-analyzer`, remove unused deps |

### Code Splitting

```javascript
// React lazy loading
const Dashboard = lazy(() => import('./Dashboard'));

// Route-based splitting
<Route path="/dashboard" element={<Dashboard />} />
```

### Image Optimization

```html
<!-- Responsive images with lazy loading -->
<img 
  src="image-400.webp" 
  srcset="image-400.webp 400w, image-800.webp 800w"
  sizes="(max-width: 600px) 400px, 800px"
  loading="lazy"
  alt="Description"
/>
```

### Critical CSS

Inline above-the-fold CSS, load rest asynchronously:
```html
<style>
  /* Critical styles: header, hero, fonts */
</style>
<link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
```

## API Performance

### Response Time Targets

| Endpoint Type | Target |
|---------------|--------|
| Simple read | < 100ms |
| Complex read (multiple joins) | < 300ms |
| Write | < 200ms |
| File upload | < 5s |

### Pagination

Always paginate list endpoints:
```javascript
// Offset pagination (simple)
GET /posts?page=2&limit=20

// Cursor pagination (better for large datasets)
GET /posts?cursor=abc123&limit=20
```

### Compression

```javascript
// Enable gzip/brotli compression
app.use(compression());
```

## Caching (see **eng-caching** skill)

Quick wins:
- Cache expensive DB queries (Redis, 5–60s TTL)
- Cache API responses with `Cache-Control` headers
- Use CDN for static assets
- Cache user sessions in Redis

## Monitoring Performance

### Real User Monitoring (RUM)

Track in the browser:
- First Contentful Paint (FCP)
- Largest Contentful Paint (LCP)
- Time to Interactive (TTI)
- Cumulative Layout Shift (CLS)

```javascript
// Web Vitals
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';
getCLS(console.log);
getLCP(console.log);
```

### Server-Side Metrics

Log on every request:
- Request duration
- Database query count and duration
- External API call duration

## Profiling

### Database Query Analysis

```sql
-- PostgreSQL: find slow queries
SELECT query, mean_exec_time, calls 
FROM pg_stat_statements 
ORDER BY mean_exec_time DESC 
LIMIT 10;
```

### Node.js Profiling

```bash
# CPU profile
node --prof app.js
node --prof-process isolate-*.log > profile.txt

# Heap snapshot for memory leaks
node --inspect app.js
# Use Chrome DevTools to capture heap snapshot
```

## Performance Budget

Set limits and enforce them:
| Resource | Budget |
|----------|--------|
| JS bundle (initial) | < 200KB gzipped |
| CSS | < 50KB gzipped |
| Images (above fold) | < 500KB total |
| API response (p95) | < 500ms |
| Page load (LCP) | < 2.5s |

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|----------|---------------|
| Premature optimization | Measure first, optimize hotspots |
| Load entire database tables | Paginate and filter |
| Ignore N+1 queries | Use JOINs or DataLoader |
| Bundle all JS into one file | Code split by route |
| Load full-resolution images | Serve responsive, optimized images |
| Optimize without profiling | Profile first to find real bottlenecks |
| Skip compression | Enable gzip/brotli |
| Cache everything forever | Set appropriate TTLs |
