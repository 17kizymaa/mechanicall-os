# CURRENT

**Objective:** Use a minimal hotkey desk over CURRENT.md as the daily product surface.
**Phase:** EXECUTE
**Status:** READY-FOR-REVIEW
**Baseline:** session/client-one-delroy-reconfigure
**Next:** run-aether-desk
**Approval:** PENDING

## Keep
- Project root = directory that holds this file (cwd)
- Hotkeys over chrome: show/edit CURRENT, preflight Next, optional free-model propose
- Free frontier API for propose only (OpenRouter / Groq)
- Human edits CURRENT by hand; approve is optional, not required for truth

## Reject
- Nested stage factory as the daily surface
- Chat-in-panel as product
- Model auto-approve
- New dependencies beyond stdlib + existing aether

## Limits
- One Next at a time
- Desk does not sandbox agents
- Keys stay in env, never in git

## Next allowed action
From this directory: `aether desk` (or `python3 ../../python/aether_desk.py .`) and use hotkeys. Action id: `run-aether-desk`.

## Approval condition
Optional. Prefer living with the file over ceremony.

## Prohibited
- nag-approve
- model-approve
- secret-in-repo
