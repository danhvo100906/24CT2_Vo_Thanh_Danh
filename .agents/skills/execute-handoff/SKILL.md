# EXECUTE HANDOFF — ANTIGRAVITY

## Goal
Implement exactly the active handoff task with evidence.

## Procedure
1. Read AGENTS.md, relevant rules/skills, CURRENT_TASK.md and CODEX_PLAN.md.
2. Inspect the real source and tests.
3. Verify assumptions from the plan.
4. Make the smallest safe change.
5. Add/update regression tests where practical.
6. Run focused tests, then broader relevant tests if shared behavior changed.
7. Review the diff for unrelated changes.
8. Write `ANTIGRAVITY_REPORT.md` including changed files, implementation, exact tests/results, problems and scope deviations.
9. If responding to `CHANGES_REQUIRED`, address only required fixes and update the report with the current cycle number.

Never claim PASS for a test that was not run.
