# Receipt — prune-aether-verbs — 2026-10-19

**Not a Yes.** Preflight allowed. Six verbs are gone from the CLI. Personas stay. Halt.

## Removed from `AETHER_VERBS`, `usage()`, and `main()`

`garden` `rival` `spark` `graph` `session` `seed`

Each now prints `aether: unknown command` and exits 2.

## Still present

`preflight` `bookmark` `current` `approve` `apply`

`AETHER_VERSION` is `0.2`. versionCode is 46. Pin cksum is `3532677481`.

`.grok/personas/preflight-log.toml` is still on disk. Python files `python/aether_garden.py` and `python/aether_rival.py` are still on disk. They are not verbs.

## Tests

`sh tests/run.sh` passed, including `seed is not a verb` and `shellcheck aether`.
