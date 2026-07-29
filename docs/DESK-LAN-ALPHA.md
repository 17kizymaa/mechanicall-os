# Desk LAN alpha (trusted house)

`--lan` binds `0.0.0.0`. There is **no** pairing token and **no** multi-tenant auth.

## Assumptions

- Home/LAN peers are trusted at the operator’s risk.
- UI and API are **same-origin** (no wildcard CORS).
- Project root is fixed at process start (`STATE.root`); clients cannot switch Domain via JSON.

## Hardening applied (P0)

- No request `root` override
- Request body size cap
- `/health` omits absolute filesystem path
- CORS not `*`

## Not goals

Accounts, OAuth, public internet exposure, SaaS multi-tenant.
