---
name: eng-deployment
description: "Deploy applications to production with concrete hosting guides, Docker setup, SSL, and environment configuration. Use when shipping code, setting up staging, or configuring production infrastructure for small-to-medium scale applications."
---

# Deployment for Prototypes

Get working code into users' hands quickly and reliably. At 1000 users, you don't need Kubernetes — you need a solid container, a reliable host, and HTTPS.

## Hosting Strategy

### Start Here: PaaS (Platform as a Service)

| Platform | Best For | Notes |
|----------|----------|-------|
| **Railway** | Full-stack apps, databases included | Generous free tier, zero config |
| **Render** | Web services, static sites, databases | Free tier, automatic deploys from Git |
| **Fly.io** | Docker apps, global edge | Pay-per-usage, great for containers |
| **Vercel** | Frontend/Next.js | Edge network, serverless functions |
| **Netlify** | Static sites, JAMstack | Generous free tier |

**Prototype rule:** Use Railway or Render for full-stack apps. Use Vercel for frontend-only. Don't manage servers until you have a reason.

### When to Upgrade

| Scale | Infrastructure |
|-------|---------------|
| 0–1,000 users | PaaS (Railway/Render/Fly) |
| 1,000–10,000 users | Same PaaS, upgrade plan |
| 10,000–100,000 users | Consider VPS (Hetzner, DigitalOcean) or managed Kubernetes |
| 100,000+ users | Dedicated infrastructure, load balancers, multi-region |

## Docker & Containerization

### Dockerfile Basics

```dockerfile
# Multi-stage build for Node.js
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package.json .
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

### Docker Compose for Local Dev

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/myapp
    depends_on:
      - db
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
volumes:
  postgres_data:
```

**Prototype rule:** Docker Compose should mirror production as closely as possible. If you use Postgres in prod, use Postgres locally — not SQLite.

## Environment Configuration

### Environment Variables

Never commit secrets. Use `.env` files locally and platform env vars in production:

```bash
# .env.example (committed to repo)
DATABASE_URL=
JWT_SECRET=
API_KEY=
FRONTEND_URL=http://localhost:5173
```

```bash
# .env (ignored by git, created during setup)
DATABASE_URL=postgres://localhost:5432/myapp
JWT_SECRET=your-secret-key
```

**Required env vars for production:**
- `DATABASE_URL` — database connection string
- `JWT_SECRET` or session secret — auth signing key
- `NODE_ENV=production` — enables optimizations
- `FRONTEND_URL` — CORS allowed origin
- `PORT` — server port (platforms often set this)

### SSL / HTTPS

- PaaS platforms handle SSL automatically
- For custom domains: use Let's Encrypt (free) via platform or reverse proxy
- Always redirect HTTP → HTTPS in production
- Set `Secure` and `SameSite` flags on cookies

## Deployment Checklist

Before shipping:
- [ ] Environment variables configured in production
- [ ] Database migrations run
- [ ] Health check endpoint responds (`GET /health` → 200)
- [ ] Error tracking configured (Sentry)
- [ ] Logs are accessible
- [ ] Rollback plan ready (previous deploy tag or commit)

## Scaling Basics

At 1000 users, scaling means:
- **Vertical**: Upgrade to a larger instance (more RAM/CPU)
- **Database**: Connection pooling (PgBouncer or ORM-level)
- **Static assets**: CDN for images, CSS, JS (Cloudflare, Bunny.net)

Don't worry about horizontal scaling (multiple servers) until you hit 10,000+ users.

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|----------|---------------|
| Commit `.env` with secrets | Use `.env.example` + platform env vars |
| Run database migrations manually | Automate in deploy pipeline |
| Skip health checks | Add `/health` endpoint for monitoring |
| Deploy without rollback plan | Tag releases, keep previous version ready |
| Use `npm start` in production Docker | Use `node` directly with `NODE_ENV=production` |
