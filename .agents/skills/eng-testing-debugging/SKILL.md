---
name: eng-testing-debugging
description: "Ensuring software correctness and reliability by writing automated tests, using quality assurance tools, and systematically debugging issues. Use when writing tests, investigating bugs, or setting up CI quality gates."
---

# Testing & Debugging

Writing robust software requires verifying that it works as intended. Developers are expected to build automated tests for their code and use debugging skills to quickly isolate issues. Thorough testing (unit tests, integration tests, etc.) gives confidence that changes won't break existing functionality. It's far cheaper to catch bugs early with tests or static analysis than in production.

## Test Strategy

### Test Pyramid

Distribute tests by speed and scope:

| Type | Portion | Purpose |
|------|---------|---------|
| **Unit Tests** | 70% | Fast, isolated, test individual functions |
| **Integration Tests** | 20% | Test component interactions |
| **E2E Tests** | 10% | Test complete user workflows |

Test categories: functional (happy path, edge cases, errors), regression (prevent breaking changes), and smoke (critical path verification).

### Test-Driven Development (TDD)

TDD is a **design technique**, not just a testing technique. It produces better-designed, more maintainable code.

**The Three Laws:**
1. Write NO production code without a failing test first
2. Write only enough test to demonstrate one failure
3. Write only enough code to pass that test

**Red-Green-Refactor Cycle:**
- **RED**: Write one test that defines desired behavior. Run it — verify it FAILS for the right reason.
- **GREEN**: Write the MINIMAL code to make the test pass. No extra features.
- **REFACTOR**: Clean up — remove duplication, improve naming, extract functions. Run ALL tests — they must stay green.
- **Repeat** for the next behavior.

### Test Writing Patterns

**Arrange-Act-Assert (AAA):**
1. **Arrange** — Set up test data and conditions
2. **Act** — Execute the code being tested
3. **Assert** — Verify the expected outcome

**Given-When-Then (BDD style):**
1. **Given** — Initial context
2. **When** — Action triggers behavior
3. **Then** — Expected outcome

### Coverage Goals

- **Lines / Functions / Branches**: 80%+ minimum
- **Critical paths** (auth, payments, validation): Aim for 100%

Common gaps to fill: error handling paths, edge cases, boundary conditions, integration points.

## Automated Testing

Write tests to cover your code's behavior — unit tests for individual functions, integration tests for components. Aim for meaningful coverage of critical paths and edge cases. This ensures your code is correct and stays correct as it evolves.

## Quality Tools

Employ linters and formatters to catch issues and enforce standards automatically. For example, use ESLint or Prettier so style issues are fixed upfront, freeing code reviews to focus on logic. Use static analysis and security scanners to find flaws early.

**Security Testing:**
- **SAST** (Static Analysis): Semgrep, CodeQL — run on every commit
- **DAST** (Dynamic Analysis): OWASP ZAP — run against staging
- **Dependency Scanning**: Snyk, Dependabot — check for known CVEs

## CI/CD Integration

Structure your test pipeline in stages:
1. **Unit Tests** — Fast feedback, run on every commit
2. **Integration Tests** — Run on pull requests
3. **E2E Tests** — Run before merging to main
4. **Performance Tests** — Run on main branch

**Quality gates:** All tests pass, coverage meets threshold, no critical security issues.

## Web Application Testing

For frontend and E2E testing, use Playwright or Cypress:
- Wait for `networkidle` before inspecting dynamic apps
- Use descriptive selectors (`text=`, `role=`, IDs)
- Always close the browser when done
- Run E2E tests against a real server instance

## Systematic Debugging

When bugs arise, debug methodically:
1. **Reproduce** the issue in a controlled environment
2. **Isolate** — use breakpoints or logging to inspect state
3. **Bisect** changes if necessary to find the culprit
4. **Fix** and add a test to prevent regression
5. **Verify** the fix doesn't break existing tests

A disciplined debugging approach saves time and builds more reliable software.

## Test Quality Checklist

- **Isolation**: Tests are independent and runnable in any order
- **Deterministic**: Tests produce consistent results
- **Fast**: Unit tests run quickly; mock external dependencies
- **Clear**: Test names describe the behavior being tested
- **Maintainable**: Tests are easy to update when code changes
