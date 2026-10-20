# Receipt — add-aether-bookmark — 2026-10-16

**Not a Yes.** Preflight allowed. Snapshot + list shipped. Restore parked. Halt.

## What ran

1. `aether preflight add-aether-bookmark` → allow.
2. `bookmark` added to `AETHER_VERBS`, `usage()`, `main()`, `SPEC-v0.2.md`.
3. `tests/bookmark.sh` pass. `shellcheck -s sh -S warning aether` pass.
4. Live `aether bookmark add-aether-bookmark .` → `.aether/bookmarks/CURRENT-20261016T182629Z-add-aether-bookmark.md`. CURRENT.md unchanged (`cmp`).

## Evidence sought

| # | Question | Result |
|---|----------|--------|
| 1 | Copy CURRENT.md and leave live file unchanged? | yes · `cmp` |
| 2 | `aether bookmark list` shows the new file? | yes · newest first |
| 3 | restore absent from `AETHER_VERBS`? | yes · `aether bookmark restore` exits 2 |
| 4 | Old snapshot cksum still `3532677481`? | yes |
| 5 | versionCode 46? | yes |

## Earlier grill (same folder)

Proposal `.aether/proposals/CURRENT-proposal-20261016-1841.md` was applied by the operator. v6 grill is `output/V6-GRILL.md`. Spec is `output/SPEC.md`.

## Untouched

Restore. Onyx. APK pin. Draft sheet. Operator CURRENT. Yes tap.
