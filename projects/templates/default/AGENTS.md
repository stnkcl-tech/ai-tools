# AGENTS.md — {{PROJECT_NAME}}

## Project Identity

- **Name**: {{PROJECT_NAME}}
- **Status**: Experiment (lives in `projects/experiments/`)
- **Type**: Research-driven software solution

## Inheritance

This project inherits all conventions, rules, and agent behavior guidelines defined in the root workspace `AGENTS.md` (`../../../AGENTS.md`).

If any instruction in this file conflicts with the root `AGENTS.md`, this file takes precedence for this project only.

## Project Phase

- **Current phase**: Discovery (pilot-pm-*) | Delivery (eng-* / pilot-pm-execution) | Growth (growth-pm-*)
- **Selected on**: <date>
- **Rationale**: <user's reason>

> **Agent instruction**: If this section is unfilled, ask the user: "Are we in discovery mode (finding PMF, 0–100K users), delivery mode (problems validated, moving straight into build/execution), or growth mode (scaling beyond 100K users)?" Then record the phase here before doing any PM work.

## Project Key Questions

1. **What problems will be solved?**
   <!-- Agent: fill in after asking the user -->

2. **Who experiences these problems?**
   <!-- Agent: fill in after asking the user -->

3. **What are currently available solutions that are used?**
   <!-- Agent: fill in after asking the user -->

> **Agent instruction**: If any answer above is empty, ask the user before proceeding with product work. These answers anchor all discovery and scoping.

## Skill Usage

Root skills are available at `../../../.agents/skills/`.

> **Agent instruction**: At the start of this project, ask the user:
> "Should I copy specific skills into this project folder, or reference them from the root workspace?"
>
> Default behavior: reference skills from the root. Only copy skills if the user explicitly requests it.

**Phase-aware skill references:**
- In **Discovery** phase, prefer `pilot-pm-*` skills (e.g., `pilot-pm-interview-script`, `pilot-pm-create-prd`, `pilot-pm-lean-canvas`)
- In **Delivery** phase, prefer `eng-*` + execution-focused `pilot-pm-*` skills (e.g., `pilot-pm-create-prd`, `pilot-pm-user-stories`, `eng-coding-discipline`, `eng-front-end-design`, `eng-deployment`, `full-stack-builder`)
- In **Growth** phase, prefer `growth-pm-*` skills (e.g., `growth-pm-ab-test-analysis`, `growth-pm-cohort-analysis`)
- For engineering work, use `eng-*` skills regardless of phase (e.g., `eng-coding-discipline`, `eng-api-design`)
- For end-to-end feature builds, use `full-stack-builder` flow skill

## Project Structure

```
.
├── AGENTS.md          # This file
├── README.md          # Public project description
├── .gitignore         # Git ignore rules
├── references/        # Locked decisions & reference materials (folder committed, contents gitignored)
├── research/          # Research notes, drafts, data (gitignored by default)
└── src/               # Source code (committed)
```

## Git Policy

- This project is an independent git repository.
- `research/` is gitignored by default. Do not commit it unless the user explicitly says otherwise.
- `references/` contents are gitignored by default, but the folder structure is committed. Only commit contents if the user explicitly says otherwise.
- Only software code and public documentation should be committed for GitHub publication.

## Project-Specific Conventions

- Before making design, product, or engineering decisions, check `references/` for locked decisions.
- If a decision is not yet in `references/`, treat it as draft and confirm with the user before locking it.
- When a decision is finalized, move or copy it to `references/` for agents to consult.
- **Gatekeep implementation**: Do not start writing code, building, shipping, or implementing until the user explicitly says "go build this," "start building," "implement this," or an equivalent explicit go-ahead.

<!-- Add any rules unique to this project below -->
