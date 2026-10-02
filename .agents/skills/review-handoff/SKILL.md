# REVIEW HANDOFF — CODEX

## Goal
Independently verify Antigravity's implementation against the current task.

## Required evidence
- CURRENT_TASK.md
- CODEX_PLAN.md
- ANTIGRAVITY_REPORT.md
- actual changed source code
- relevant tests and test results/diff

## Procedure
1. Re-read acceptance criteria and restrictions.
2. Inspect actual changed files; do not trust the report alone.
3. Check correctness, scope, regressions, security and architecture constraints.
4. Inspect/rerun relevant tests when possible.
5. Verify no unrelated changes were introduced.
6. Write `CODEX_REVIEW.md`.

## Verdict
Use exactly one:
- `Status: APPROVED`
- `Status: CHANGES_REQUIRED`
- `Status: BLOCKED`

For CHANGES_REQUIRED, state numbered Problems, Required fixes and Do not change items. Track the repair cycle. Maximum 3 fix cycles.
