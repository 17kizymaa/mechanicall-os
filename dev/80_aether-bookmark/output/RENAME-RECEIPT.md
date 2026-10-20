# Receipt — bookmark-rename-nickname — 2026-10-19

**Not a Yes.** Preflight allowed. Rename prompt shipped. Restore parked. Verbs not pruned. Halt.

## What ran

1. `aether preflight bookmark-rename-nickname` → allow. Phase APPROVE, Status APPROVED.
2. `cmd_bookmark` prompts `Rename: [stem] ` when stdin is a TTY. Empty keeps the stem. `list` and `restore` exit 2. Bad charset exits 2. A non-TTY does not read stdin.
3. The bookmark event records `stem`.
4. `sh tests/bookmark.sh` pass. `shellcheck -s sh -S warning aether` pass.
5. One sentence added to the `aether bookmark` row in `SPEC-v0.2.md`.

## Evidence sought

| # | Question | Result |
|---|----------|--------|
| 1 | TTY nickname `ejected-verbs`, CURRENT unchanged? | yes |
| 2 | Empty Rename keeps `CURRENT`? | yes |
| 3 | `list` and `restore` as stem exit 2? | yes |
| 4 | Non-TTY does not hang and keeps `CURRENT`? | yes |
| 5 | Pin snapshot cksum `3532677481`? | yes |
| 6 | versionCode 46, garden and seed still in `AETHER_VERBS`? | yes |

## Untouched

Restore. Verb prune. Personas. `AETHER_VERSION`. versionCode. Onyx. APK. Yes tap. `aether next`.
