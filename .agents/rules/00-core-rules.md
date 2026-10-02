# CORE RULES
Always obey `AGENTS.md`.

When instructions conflict, prefer:
1. explicit current user instruction;
2. project specification;
3. approved decisions;
4. current task queue;
5. existing implementation conventions;
6. agent preference.

Never silently resolve a contradiction between authoritative project documents.

## V2 HANDOFF RULE
For an active implementation task, `PROJECT_SPEC/HANDOFF/CURRENT_TASK.md` is the task-level source of truth. Codex creates/refines it; Antigravity executes it. Neither agent may silently expand its scope.
