---
name: eng-auth-implementation
description: "Implement secure authentication and authorization with sessions, JWT, OAuth, and RBAC. Use when building login, signup, password reset, or permission systems."
---

# Authentication & Authorization for Prototypes

Implement auth that is secure enough for real users without over-engineering. At 1000 users, JWT + bcrypt + secure cookies is sufficient. Don't build your own crypto.

## Authentication Methods

### Start Here: JWT (JSON Web Tokens)

Best for stateless APIs and SPAs.

```javascript
// Sign token on login
const token = jwt.sign(
  { userId: user.id },
  process.env.JWT_SECRET,
  { expiresIn: '7d' }
);

// Verify on every protected request
try {
  const payload = jwt.verify(token, process.env.JWT_SECRET);
  req.userId = payload.userId;
} catch (err) {
  return res.status(401).json({ error: 'Invalid token' });
}
```

**Rules:**
- Store `JWT_SECRET` in environment variables — never commit it
- Set short expiry (7 days for access tokens, 30 days for refresh)
- Use refresh tokens for long sessions
- Never store tokens in `localStorage` — use `httpOnly` cookies

### Session-Based Auth

Best for server-rendered apps.

```javascript
// Server-side session with Redis or memory store
app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: process.env.NODE_ENV === 'production',
    httpOnly: true,
    sameSite: 'strict',
    maxAge: 1000 * 60 * 60 * 24 * 7 // 7 days
  }
}));
```

### OAuth / Social Login

Use a library — never implement OAuth manually.

| Provider | Library |
|----------|---------|
| Google | `passport-google-oauth20` (Node), `social-auth-app-django` (Python) |
| GitHub | `passport-github2` |
| Magic Link | `next-auth`, `Auth.js` |

**Rule:** Always verify the user's email from the OAuth provider before creating an account.

## Password Handling

- Never store plaintext passwords
- Use bcrypt (cost factor 10–12): `bcrypt.hash(password, 12)`
- Compare with timing-safe comparison: `bcrypt.compare(password, hash)`
- Enforce minimum complexity (8+ chars) but don't be overly restrictive
- Rate-limit login attempts (5 attempts per 15 min per IP)

## Authorization (RBAC)

### Simple Role-Based Access Control

```javascript
// Middleware
function requireRole(role) {
  return (req, res, next) => {
    if (req.user.role !== role) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    next();
  };
}

// Usage
app.delete('/posts/:id', authenticate, requireRole('admin'), deletePost);
```

### Ownership Checks

```javascript
// Users can only edit their own posts
async function canEditPost(userId, postId) {
  const post = await db.posts.findById(postId);
  return post && post.authorId === userId;
}
```

**Rule:** Check authorization at the API boundary, not deep in business logic.

## Security Essentials

### Cookie Security

```javascript
{
  httpOnly: true,   // Not accessible via JavaScript
  secure: true,     // HTTPS only in production
  sameSite: 'strict', // CSRF protection
  maxAge: 604800000  // 7 days
}
```

### CORS

```javascript
// Whitelist specific origins
app.use(cors({
  origin: process.env.FRONTEND_URL,
  credentials: true
}));
```

### CSRF Protection

- For APIs: Use `SameSite=strict` cookies + proper CORS
- For forms: Include CSRF token in forms, validate server-side

## Password Reset Flow

1. User requests reset → generate secure token (UUID or crypto.randomBytes)
2. Store token hash in database with expiry (1 hour)
3. Send email with link: `/reset-password?token=xyz`
4. User submits new password → verify token, hash password, invalidate token

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|----------|---------------|
| Store JWT in localStorage | Use httpOnly cookies |
| Store passwords in plaintext | Hash with bcrypt |
| Use MD5/SHA1 for passwords | Use bcrypt, Argon2, or scrypt |
| Implement OAuth manually | Use battle-tested libraries |
| Trust client-provided userId | Verify token server-side |
| Skip rate limiting | Limit login attempts per IP |
| Return different errors for "user not found" vs "wrong password" | Return generic "Invalid credentials" |
