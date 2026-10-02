# STUDYBOT V2 — HANDOFF WORKFLOW PROTOCOL

## Flow

`PLAN -> DEVELOP -> TEST -> REVIEW -> FIX -> TEST -> REVIEW -> APPROVE`

## State transitions

1. User gives one task.
2. Codex inspects specification/source/tests.
3. Codex writes CURRENT_TASK.md + CODEX_PLAN.md.
4. CURRENT_TASK state becomes `READY_FOR_ANTIGRAVITY`.
5. Antigravity implements and tests.
6. Antigravity writes ANTIGRAVITY_REPORT.md with `COMPLETED` or `BLOCKED`.
7. Codex independently reviews actual source/tests.
8. Codex writes CODEX_REVIEW.md:
   - `APPROVED` -> DONE.
   - `CHANGES_REQUIRED` -> Antigravity fixes and retests.
   - `BLOCKED` -> stop and report.
9. Maximum 3 fix cycles. After cycle 3 without approval, stop as `BLOCKED`.

## Non-negotiable rules

- One active task at a time.
- CURRENT_TASK.md defines scope.
- Antigravity cannot redefine task scope.
- Codex cannot approve from report alone.
- No infinite fix loop.
- Do not modify StudyBot source merely to connect agents.
- Automation/orchestrator comes only after the manual workflow is proven stable.
