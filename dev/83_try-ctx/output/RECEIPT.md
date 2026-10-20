# Receipt — try-ctx — 2026-10-19

**Not a Yes.** Preflight allowed. Spike is in `ctx/`. The APK was not built.

## Layout

- `ctx/RULES.md` — CURRENT.md is the only Yes
- `ctx/ctx` — `start` and `set` only. Spec 1.2. Not on `PATH`
- `ctx/memory/{operator,shared,agent}.json`
- `ctx/sessions/` — empty
- `shared.current_focus` — source operator, basis reported

`CTX_HOME=ctx ctx/ctx start` exited 0 and printed the rules.

CURRENT.md checksum stayed `3465288847` `14900` across `ctx set`. `preflight-log.toml` remains. `aether verbs` still contains `preflight`. `AETHER_VERSION` is `0.2`. versionCode is 46. Pin cksum is `3532677481`.
