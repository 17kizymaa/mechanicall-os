# RECEIPT — operator-auth-later

**Not Yes. Not apex this turn.** Preflight ALLOW.

## Bind

- Env `YOU_DECIDE_OPERATOR_KEY`. Unset → operator routes 401/503 (fail closed).
- POST `/api/you-decide/operator` `{ key }` → HttpOnly cookie `yd_op`.
- GET `/api/you-decide/operator` → `{ operator, configured }`.
- Page `/you-decide/operator`.
- POST `/message` with `from: "anthony"` without operator → stored as **them**.
- PUT `/propose` and PUT `/zip` require operator.
- Paper fill/reset stay on the birthday ticket (they sit Paper).

## Local sit (`:8788`)

| Check | Result |
|-------|--------|
| impersonate `from:anthony` no key | stored `them` |
| PUT zip no key | 401 |
| bad key | 401 |
| good key + cookie | `from: anthony` |

Did not push. Did not set Render env. Did not `aether approve`.
