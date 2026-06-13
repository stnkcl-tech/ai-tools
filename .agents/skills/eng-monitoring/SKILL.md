---
name: eng-monitoring
description: "Set up application monitoring, alerting, and logging for production health. Use when configuring observability, debugging production issues, or setting up error tracking."
---

# Monitoring for Prototypes

Know when your app is broken before your users tell you. At 1000 users, you need error tracking, basic logs, and a health check — not a full observability platform.

## Error Tracking

### Start Here: Sentry

- Free tier: 5,000 errors/month
- Auto-captures unhandled exceptions
- Captures stack traces, request context, user info
- Integrates with most frameworks in 2 lines of code

```javascript
// Node.js / Express
import * as Sentry from '@sentry/node';
Sentry.init({ dsn: process.env.SENTRY_DSN });
app.use(Sentry.Handlers.errorHandler());
```

```python
# Python / Django
import sentry_sdk
sentry_sdk.init(dsn=os.environ['SENTRY_DSN'])
```

**Rule:** Every uncaught exception should be tracked. Every caught exception that affects a user should be tracked with context.

## Logging

### Structured Logs

```javascript
// Use a structured logger (pino, winston)
logger.info({ userId: '123', action: 'purchase', amount: 50 }, 'User completed purchase');
logger.error({ error: err.message, stack: err.stack }, 'Payment processing failed');
```

**Rules:**
- Log at the right level: `debug` (dev), `info` (normal operations), `warn` (unexpected but handled), `error` (failed operations)
- Include context (userId, requestId, action) in every log line
- Don't log sensitive data (passwords, tokens, PII)
- Use structured JSON format in production (easily searchable)

### Log Aggregation

| Service | Cost | Notes |
|---------|------|-------|
| **Sentry** | Free tier | Errors + breadcrumbs |
| **Datadog** | Paid | Full observability |
| **Logtail / Better Stack** | Free tier | Log aggregation |
| **CloudWatch** | AWS | If already on AWS |

## Health Checks

### Required Endpoint

```javascript
app.get('/health', (req, res) => {
  // Check critical dependencies
  const dbHealthy = checkDatabaseConnection();
  const cacheHealthy = checkCacheConnection();
  
  if (dbHealthy && cacheHealthy) {
    res.status(200).json({ status: 'ok', timestamp: new Date().toISOString() });
  } else {
    res.status(503).json({ status: 'unhealthy', checks: { db: dbHealthy, cache: cacheHealthy } });
  }
});
```

**Use health checks for:**
- Load balancer / PaaS routing decisions
- Deployment verification (don't route traffic until healthy)
- Simple uptime monitoring

## Metrics

### What to Track

| Metric | Why | When |
|--------|-----|------|
| Request latency (p50, p95, p99) | Detect slowdowns | Always |
| Error rate (5xx / total requests) | Detect breakage | Always |
| Database query time | Find N+1 issues | Always |
| Active users | Growth signal | Daily |
| Queue depth (if using background jobs) | Backpressure | Always |

### Simple Metrics Setup

```javascript
// Basic request timing middleware
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log({ method: req.method, path: req.path, status: res.statusCode, duration });
  });
  next();
});
```

## Alerting

### When to Alert

- Error rate > 1% for 5 minutes
- Health check failing for 2 minutes
- Latency p95 > 2 seconds for 10 minutes
- Database connection failures

### How to Alert

- PaaS built-in alerts (Railway, Render)
- Uptime monitors: UptimeRobot (free), Pingdom
- Error spike alerts via Sentry

**Rule:** Alert on symptoms (users affected), not causes (CPU usage). A high CPU with no user impact doesn't need a 3am page.

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|----------|---------------|
| Log everything at `info` | Use appropriate log levels |
| Log passwords, tokens, credit cards | Redact sensitive fields |
| Catch and silently swallow errors | Log or report every error |
| Alert on every error | Alert on error rate spikes |
| Skip health checks | Add `/health` endpoint |
| Monitor CPU/memory without user context | Monitor request latency and error rate |
