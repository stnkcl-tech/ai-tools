---
name: eng-dead-code-removal
description: "Detects and safely removes unused code — imports, functions, classes, variables — across multiple languages. Use after refactoring, when removing features, or before production deployment. Includes safety checks and incremental validation."
---

# Dead Code Removal

Safely identify and remove unused code to reduce bundle size, improve maintainability, and eliminate confusion. Dead code is a form of technical debt that accumulates silently. Remove it methodically with safety checks to avoid breaking anything.

## When to Use

- After refactoring or removing a feature
- Before production deployment to reduce bundle size
- When cleaning up legacy or deprecated code
- As part of routine codebase maintenance

## Safety Checks

**Never remove if any of these apply:**
- Dynamic usage detected (`getattr`, `eval`, `importlib`, `window[]`, reflection, decorators)
- Framework patterns (Django models, React components, Flask routes, Spring beans)
- Entry points (`main`, `__main__`, `index`, `run`, `app`)
- Public/exported APIs consumed by other modules
- Code referenced in configuration files or templates
- Test files, migrations, or seed data

## Safe Removal Process

1. **Create a backup** before making any changes
2. **Identify candidates** using static analysis (AST parsing, lint rules, IDE hints)
3. **Cross-reference** against the entire codebase — unused in one file may be imported elsewhere
4. **Remove incrementally** — one function or import at a time
5. **Validate after each removal:**
   - Syntax check (`python -m py_compile`, `eslint`, `tsc --noEmit`)
   - Run tests
   - Verify build succeeds
   - Check for runtime errors in dev

## Detection Patterns

**Static Analysis (preferred):**
- Use AST parsing for accurate import/function detection
- Track cross-file references
- Check for dynamic usage patterns before flagging

**Common targets:**
- Unused imports (`import os` with no reference)
- Unreferenced functions (private helpers with no callers)
- Dead branches (`if false` blocks, unreachable returns)
- Unused variables and parameters
- Commented-out code older than one release cycle

## Validation Checklist

- [ ] Tests pass after removal
- [ ] Build succeeds
- [ ] No dynamic usage detected
- [ ] No framework hooks broken
- [ ] No public API surface changed unexpectedly
