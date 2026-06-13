---
name: eng-developer-experience
description: "Optimizing developer workflows, reducing friction, and automating repetitive tasks to make development more productive and enjoyable. Use when setting up projects, onboarding developers, configuring tooling, or improving build and test workflows."
---

# Developer Experience

Great developer experience (DX) is invisible when it works and obvious when it breaks. This skill focuses on reducing friction, automating repetitive tasks, and creating fast feedback loops so developers can focus on solving problems.

## Principles

1. **Invisible When Working**: Seamless tooling that stays out of the way
2. **Obvious When Broken**: Clear, actionable error messages
3. **Fast Feedback**: Quick build, test, and reload cycles
4. **Clear Documentation**: Setup guides that actually work on the first try
5. **Helpful Defaults**: Sensible configurations out of the box

## Environment Setup

- **Onboarding under 5 minutes**: One-command setup (`npm run setup`, `make init`, etc.)
- **Intelligent defaults**: Sensible `.env` values, pre-configured tooling
- **Automated validation**: Check Node.js version, dependencies, environment variables
- **Clear error messages**: Tell the developer exactly what's wrong and how to fix it

## Workflow Automation

Identify and eliminate repetitive tasks:
- **npm/yarn scripts** for common operations (dev, test, lint, format, db:migrate)
- **Makefile** commands for polyglot projects
- **Git hooks** for pre-commit linting and pre-push testing
- **VS Code tasks** and debug configurations

## Tooling Configuration

Standardize the development environment:
- **EditorConfig** for consistent formatting across editors
- **ESLint / Prettier** with project-specific rules
- **Debug configurations** ready to use
- **Snippet libraries** for boilerplate reduction

## Success Metrics

- **Time to First Success**: How long until a new developer runs the app?
- **Build/Test Time**: Execution time for common tasks
- **Manual Steps**: Count of steps eliminated through automation
