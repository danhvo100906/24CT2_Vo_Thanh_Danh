# TESTING RULES
Never declare completion from code inspection alone when execution is possible.

For a change:
1. run the most relevant existing tests;
2. add a regression test for a bug when practical;
3. run broader tests when the change may affect shared behavior;
4. inspect failures rather than hiding them.

Never claim tests passed if they were not run.

Minimum quality gates:
- syntax/import validity;
- affected unit/integration tests;
- relevant chatbot/data tests;
- final diff review.

## V2 REVIEW LOOP
Antigravity must record exact tests/commands/results in `ANTIGRAVITY_REPORT.md`. Codex must independently inspect code/tests and may rerun or request relevant tests. A report alone is never sufficient evidence for approval.
