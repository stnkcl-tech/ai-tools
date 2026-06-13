---
name: eng-secure-coding
description: "Incorporating security at every step of software development – writing code that defends against vulnerabilities and protects user data. Use when handling authentication, user input, sensitive data, or deploying to production."
---

# Secure Coding Practices

In the age of constant cyber threats, security is everyone's job. Developers are on the front lines of safeguarding applications, from locking down APIs to securing cloud deployments. This skill means anticipating how code could be exploited and coding defensively. With a majority of organizations attributing breaches to lack of cyber skills, there's high demand for developers who can build secure systems from the ground up.

## Examples
- Validating all inputs and encoding outputs to prevent injection attacks (SQL injection, XSS, etc.).
- Using secure libraries and protocols (HTTPS, OAuth) and storing sensitive data (passwords, API keys) in encrypted form or secret managers.

## Guidelines

### Defense in Depth
Treat security as layered defenses, not a single gate. As a developer, you control the inner layers:

| Layer | Developer Controls |
|-------|-------------------|
| Application | Input validation, secure coding, output encoding |
| Data | Encryption at rest and in transit, access control, minimal data collection |
| Identity | Strong authentication, MFA, least-privilege access |

### Secure Session Management
"Proper authentication" is meaningless without secure session handling:
- **Secure cookies**: Use `HttpOnly`, `Secure`, and `SameSite=Strict` attributes
- **Session timeouts**: Enforce idle timeout (e.g., 30 min) and absolute timeout (e.g., 8 hours)
- **Invalidation on logout**: Destroy server-side sessions, not just client-side tokens
- **Concurrent limits**: Prevent account sharing by limiting active sessions per user

### Secrets Management

| Never | Do |
|-------|-----|
| Commit secrets or API keys to git | Use environment variables or secret managers (Vault, AWS Secrets Manager, Doppler) |
| Log secrets, tokens, or passwords | Rotate secrets regularly and audit access |
| Pass secrets in URLs or expose in frontend | Scope credentials to the narrowest permission possible |

### Security Testing
Integrate automated security checks into your workflow:
- **SAST (Static Analysis)**: Semgrep, CodeQL, SonarQube — run on every commit, block high-severity findings
- **DAST (Dynamic Analysis)**: OWASP ZAP, Burp Suite — run against staging environments
- **Dependency Scanning**: Snyk, Dependabot, npm audit — check for known CVEs before deployment

### Least Privilege & Zero Trust
Design with a "default deny" mindset:
- Users get **no access** unless explicitly granted
- Collect only the data you actually need
- Scope API keys and tokens to the narrowest possible permission
- Validate authorization at every endpoint, not just the perimeter

### OWASP Top 10 & Secure Coding Standards
Adhere to well-known secure coding standards. Validate inputs, use proper error handling (never expose stack traces or internal paths), and keep dependencies up to date to patch known vulnerabilities.

### Cloud & API Security
Protect cloud infrastructure with appropriate configurations. Secure APIs with authentication, authorization, rate-limiting, and input validation. Understanding cloud security is essential for all developers, not just dedicated security teams.
