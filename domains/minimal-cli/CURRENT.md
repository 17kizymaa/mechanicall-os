# CURRENT

**Objective:** Use terminal desk as chat + CURRENT surface (model proposes; file remains authority).
**Phase:** EXECUTE
**Status:** READY-FOR-REVIEW
**Baseline:** session/client-one-delroy-reconfigure
**Next:** run-aether-desk
**Approval:** PENDING

## Keep
- Project root = directory that holds this file (cwd)
- Default desk = multi-turn terminal chat to free/frontier model
- Slash commands for CURRENT / preflight (not buried in model tools)
- Free frontier API for propose only (OpenRouter / Groq)
- Human edits CURRENT by hand; approve optional

## Reject
- Nested stage factory as the daily surface
- Model auto-approve or silence-as-yes
- New dependencies beyond stdlib + existing aether
- Chat as second authority plane

## Limits
- One Next at a time
- Chat logs under .aether/chat.jsonl are evidence, not authority
- Keys stay in env, never in git

## Next allowed action
From this directory: `aether desk` and talk; use `/e` to edit CURRENT. Action id: `run-aether-desk`.

## Approval condition
Optional. Prefer living with the file over ceremony.

## Prohibited
- nag-approve
- model-approve
- secret-in-repo
