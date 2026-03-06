# AGENTS.md — Codex Review Rules (Python)

## Priority order (do in this order)
1) Correctness (logic, edge cases, invariants)
2) Security (input validation, auth, secrets, injection, unsafe deserialization)
3) Reliability (timeouts, retries, idempotency, error handling)
4) Maintainability (complexity, naming only if it hides meaning)
5) Style LAST (only mention if it causes bugs)

## What to review on every PR
- New failure modes introduced by the diff
- Unhandled exceptions / silent failures
- Resource leaks (files, sockets), missing closes/context managers
- Race conditions (threads/async), shared state
- Data validation at boundaries (API handlers, CLI args, env vars)
- Logging: no secrets, enough context for debugging
- Tests: what’s missing, what’s brittle, what should be added

## Python-specific checks
- Type mismatches and “Any” leaks that hide bugs
- Mutable default args
- Timezone/naive datetime bugs
- `except Exception:` misuse (if used, must re-raise or wrap with context)
- `eval/exec`, `pickle`, `yaml.load` without safe loader, shell=True
- Requests without timeouts
- SQL string building without parameterization

## Output format
- Start with: "Blockers" (must-fix)
- Then: "Risks" (should-fix)
- Then: "Nice-to-have" (optional)
- Give exact file:line references when possible
- Suggest minimal diffs. Do not propose rewrites unless necessary.

## Do NOT
- Do not bikeshed formatting.
- Do not ask for refactors unrelated to the PR.
- Do not propose changing public APIs unless there’s a bug/security issue.
