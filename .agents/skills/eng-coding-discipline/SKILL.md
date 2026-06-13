---
name: eng-coding-discipline
description: "Apply disciplined coding practices including project spine analysis, test verification, scaffold discipline, and design quality standards. Use when writing or modifying code, scaffolding projects, running tests, or making UI/visual changes."
---

# Coding Discipline

## Code Discipline

Before writing or changing code:

1. **Read the project spine** — manifest, entry points, existing patterns, CI/test scripts.
2. **Find how this repo proves correctness** — `package.json` scripts, `Makefile`, CI workflows.
3. **Read the target file and callers/tests before editing**; base changes on exact contents.
4. **Match project conventions** over patterns from another stack.
5. **For APIs and versions**, read current docs or installed source — do not invent.

While changing code:
- Smallest diff that achieves the goal.
- One logical concern per change.
- Reuse existing abstractions.
- **Handle errors explicitly**: fail early, return meaningful error messages, log errors with context, and never swallow exceptions silently.
- **No drive-by refactors**.
- **Consider performance impact**: avoid N+1 queries, minimize unnecessary re-renders or bundle bloat, and profile if unsure.
- **Add observability**: log important state changes and errors with actionable context. Avoid noisy logs.

After meaningful changes:
- Run the repo's proving commands (`go test`, `cargo test`, `npm test`, `pytest`, `flutter analyze`, etc.).
- For UI changes, re-read the post-change screenshot/frame when one is available.
- For architecture depth, apply SOLID and clean-structure principles.
- For UI or 3D work, load design skills when available.

## Scaffold Discipline

- Verify new packages, frameworks, and toolchains against current sources before recommending them.
- Use official CLI or `create` or `init` scaffolding paths when they exist.
- Do not hand-write manifests, boilerplate, or generated project structure when an official scaffold exists.
- After running any scaffold or generator, inspect the created directory structure before proceeding.

## Closeout Checklist

Before finishing work, state:
- **What changed** — brief summary of the work
- **How it was tested** — commands run, checks performed
- **What risks remain** — untested paths, assumptions, follow-ups

## Skill References

- For UI/frontend aesthetics, typography, color, motion, and visual composition, invoke the **eng-front-end-design** skill.
- For documentation standards — code comments, READMEs, and project docs — invoke the **core-documentation** skill.
- For API specs, changelogs, architecture docs, and migration guides — invoke the **eng-documentation** skill.
- For test strategy, TDD, and test writing, invoke the **eng-testing-debugging** skill.
- For project setup, tooling, and workflow optimization, invoke the **eng-developer-experience** skill.
- For deployment, hosting, and infrastructure — invoke the **eng-deployment** skill.
- For UI or 3D work, load design skills when available.
