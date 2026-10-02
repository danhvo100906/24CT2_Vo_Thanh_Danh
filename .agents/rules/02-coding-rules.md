# CODING RULES
- Inspect existing code before changing it.
- Preserve existing architecture unless the task requires change.
- Prefer small, local changes.
- Reuse existing utilities and conventions.
- Avoid duplicate implementations.
- Do not add a library when the existing stack can solve the problem reasonably.
- Keep error handling explicit.
- Do not remove working behavior merely to simplify implementation.

## V2 IMPLEMENTER BOUNDARY
When acting as Antigravity, do not change files outside `CURRENT_TASK.md` unless a directly required dependency or technical necessity is discovered. Any such extra file must be explained in `ANTIGRAVITY_REPORT.md`.
