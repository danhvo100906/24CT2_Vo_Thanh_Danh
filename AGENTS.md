# STUDYBOT — AI DEVELOPMENT KIT V2 — AGENT CONSTITUTION

## 1. Purpose

This repository uses a controlled two-agent workflow:

- **Codex** = planner + reviewer.
- **Antigravity** = implementer + tester + fixer.
- **HANDOFF files** = the only formal task/review bridge between them.

Do not modify StudyBot merely to connect the two agents. Coordination belongs in `.agents/` and `PROJECT_SPEC/HANDOFF/`.

## 2. Authority and required reading

Before significant work, read in this order:

1. `AGENTS.md`
2. `PROJECT_SPEC/MASTER_PROJECT_SPECIFICATION.md`
3. `PROJECT_SPEC/CURRENT_STATUS.md`
4. `PROJECT_SPEC/DECISIONS.md`
5. `PROJECT_SPEC/TASK_QUEUE.md`
6. Relevant files in `.agents/rules/`
7. Relevant files in `.agents/skills/`
8. `PROJECT_SPEC/HANDOFF/CURRENT_TASK.md`
9. Relevant source code and tests

If authoritative documents conflict, do not silently choose. Record the conflict and stop the affected work.

## 3. Agent roles

### Codex
Codex must:
- inspect the specification, source and tests;
- convert a user request into one executable task;
- write/update `CURRENT_TASK.md`;
- write `CODEX_PLAN.md` before implementation;
- review actual source changes and test evidence after Antigravity reports;
- write `CODEX_REVIEW.md` as `APPROVED` or `CHANGES_REQUIRED`;
- never approve based only on `ANTIGRAVITY_REPORT.md`.

Codex should not implement the task while acting in planner/reviewer role unless the user explicitly overrides the workflow.

### Antigravity
Antigravity must:
- read the current task, rules, skills and plan;
- inspect real source/tests before changing code;
- implement only the approved scope;
- test the result;
- write `ANTIGRAVITY_REPORT.md` with evidence;
- when review status is `CHANGES_REQUIRED`, fix only the required items and retest.

Antigravity must not rewrite `CURRENT_TASK.md` or redefine acceptance criteria.

## 4. Scope control

Implement only:
- the explicit current task;
- required dependencies;
- necessary bug fixes directly blocking the task;
- technically necessary changes.

Do not implement unsolicited ideas. Future ideas belong in `TASK_QUEUE.md` or `ROADMAP.md`.

Prefer the smallest safe change. Do not refactor unrelated code, mass-format files, change architecture, database schema, authentication behavior, main AI approach, or add external services unless explicitly approved.

## 5. Handoff protocol

Formal loop:

`PLAN -> DEVELOP -> TEST -> REVIEW -> FIX -> TEST -> REVIEW -> APPROVE`

Files:
- `CURRENT_TASK.md` — shared source of truth for the active task.
- `CODEX_PLAN.md` — Codex analysis and implementation plan.
- `ANTIGRAVITY_REPORT.md` — implementation/test report from Antigravity.
- `CODEX_REVIEW.md` — Codex verdict and required fixes.

A task is not DONE until `CODEX_REVIEW.md` has `Status: APPROVED`.

## 6. Maximum repair loops

Maximum: **3 fix/review cycles** after the initial implementation.

- Cycle 0: initial Antigravity implementation.
- Cycles 1–3: fixes requested by Codex.
- If still not approved after cycle 3, mark the task `BLOCKED` and report unresolved problems. Do not continue an infinite agent loop.

## 7. Evidence-first implementation

Before modifying an existing feature:
1. locate implementation;
2. read relevant source;
3. read relevant tests;
4. reproduce or verify current behavior when possible;
5. identify root cause;
6. choose the smallest fix.

Never invent files, functions, endpoints, fields, data sources or test results.

## 8. Definition of Done

A task is complete only when:
- acceptance criteria are satisfied;
- relevant tests have actually run and pass, or limitations are explicitly documented;
- behavior is verified;
- diff contains no unrelated changes;
- required documentation is updated;
- Codex review says `APPROVED`.

Use honest status values: `READY`, `IN_PROGRESS`, `COMPLETED`, `CHANGES_REQUIRED`, `APPROVED`, `BLOCKED`.

## 9. StudyBot priorities

Priority order:
1. Correct focus.
2. Correct data/source.
3. Useful learning support.
4. Short relevant context.
5. Extensibility.

Do not turn StudyBot into a generic chatbot.

## 10. Language

Project communication and handoff files: Vietnamese.
Code identifiers: follow existing convention; prefer English.
Comments: concise.
