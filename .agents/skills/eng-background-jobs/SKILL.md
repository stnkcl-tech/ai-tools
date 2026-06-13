---
name: eng-background-jobs
description: "Design and implement background job processing with queues, workers, retries, and scheduling. Use when offloading slow operations, processing webhooks, or building task pipelines."
---

# Background Jobs for Prototypes

Move slow, unreliable, or scheduled work out of the request path. At 1000 users, a simple job queue keeps your API responsive without adding operational complexity.

## When to Use Background Jobs

| Scenario | Why Offload? |
|----------|--------------|
| Sending emails | SMTP is slow and unreliable |
| Image/video processing | CPU-intensive, timeouts |
| Data imports/exports | Can take minutes or hours |
| Webhook delivery | External services are flaky |
| Scheduled tasks (reports, cleanup) | Not user-initiated |
| Third-party API calls | Rate limits, latency |
| Bulk operations | Affects many records |

## Job Queue Options

| Technology | Best For | Notes |
|------------|----------|-------|
| **Bull / BullMQ** (Node.js) | Redis-backed, feature-rich | Most popular Node.js option |
| **Bull + Redis** | Prototype to production | Easy setup, reliable |
| **Celery** (Python) | Python ecosystem | Mature, many backends |
| **Sidekiq** (Ruby) | Ruby ecosystem | Fast, Redis-backed |
| **Inngest** | TypeScript, event-driven | Great for workflows |
| **pg-boss** | PostgreSQL-backed | No Redis needed |

**Prototype rule:** Use Bull/BullMQ (Node) or Celery (Python). Both use Redis and scale well.

## Basic Job Pattern

### Producer (API endpoint)

```javascript
import Queue from 'bull';
const emailQueue = new Queue('emails', process.env.REDIS_URL);

// Add job to queue
app.post('/signup', async (req, res) => {
  const user = await createUser(req.body);
  
  // Offload email sending
  await emailQueue.add('welcome-email', {
    userId: user.id,
    email: user.email
  });
  
  res.json({ user }); // Fast response — email sends in background
});
```

### Consumer (Worker process)

```javascript
// worker.js — run as separate process
emailQueue.process('welcome-email', async (job) => {
  const { userId, email } = job.data;
  await sendWelcomeEmail(email);
  console.log(`Welcome email sent to ${email}`);
});
```

## Retries & Error Handling

```javascript
emailQueue.add('welcome-email', data, {
  attempts: 3,           // Retry 3 times
  backoff: {
    type: 'exponential', // 1s, 2s, 4s
    delay: 1000
  },
  removeOnComplete: 10,  // Keep last 10 completed jobs
  removeOnFail: 5        // Keep last 5 failed jobs
});

// Log failures
emailQueue.on('failed', (job, err) => {
  console.error(`Job ${job.id} failed:`, err.message);
  // Send to error tracking (Sentry)
});
```

**Rule:** Every job must be idempotent — running it twice should have the same result as running it once.

## Scheduling

### Delayed Jobs

```javascript
// Send reminder in 24 hours
await reminderQueue.add('send-reminder', data, {
  delay: 24 * 60 * 60 * 1000
});
```

### Recurring Jobs

```javascript
// Run every day at 9 AM
const cron = require('node-cron');
cron.schedule('0 9 * * *', () => {
  dailyReportQueue.add('generate-report');
});
```

Or use Bull's repeat option:
```javascript
queue.add('cleanup', {}, { repeat: { cron: '0 2 * * *' } }); // Daily at 2 AM
```

## Job Visibility & Monitoring

- Use a dashboard: Bull Arena, Bull Board, or Celery Flower
- Track: queue depth, processing rate, failure rate, average job duration
- Alert when queue depth grows or failure rate spikes

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|----------|---------------|
| Run slow work synchronously in API | Offload to background job |
| Skip retries | Configure retry with backoff |
| Make jobs non-idempotent | Design jobs to handle duplicate runs |
| Ignore failed jobs | Monitor and alert on failures |
| Use cron on the web server | Use a job queue with scheduling |
| Store large payloads in the job | Pass IDs, fetch data in worker |
| Run long jobs without timeout | Set job timeout and handle gracefully |
