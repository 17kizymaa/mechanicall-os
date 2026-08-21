# ENGINE-DONE — pocket engine sync (03_implement)

**When:** 2026-08-19  
**Role:** engine specialist only (no Kotlin, no AndroidManifest, no `applicationId` change).  
**Next (operator CURRENT, not rewritten):** `people-app-phone-seat`  
**Did not:** `aether approve` · rewrite `CURRENT.md` · tap Yes.

## Commands

From repo root (`/mnt/kingston-nixos-sync/opt/mechanicall-os`, also `/home/anphuni/mechanicall-os`):

```bash
sh scripts/sync-pocket-engine.sh
python3 -m pytest tests/test_aether_pocket.py tests/test_aether_pocket_serve.py -q
```

## Sync

`scripts/sync-pocket-engine.sh` copied:

```text
python/aether_pocket.py
  -> android/app/src/main/python/aether_pocket.py
```

`diff` empty. `cmp` identical. Same SHA-256:

```text
c8741b4e75b8d974e43e9fa088f4fb8ff3041c9421367f1f4414279759b9dfd4
```

Chaquopy tree matches the one source. Size 15116 bytes.

## Tests

`python3 -m pytest tests/test_aether_pocket.py tests/test_aether_pocket_serve.py -q`

```text
................                                                         [100%]
16 passed in 2.89s
```

Refuse-related cases included:

- `TestRefuseOperator::test_operator_tree_detected`
- `TestRefuseOperator::test_refuse_operator_bind`
- `TestRefuseOperator::test_plain_folder_ok`
- `TestPocketAether::test_yes_refuses_operator`
- `TestFace::test_refuse_operator_page`

## `refuse_if_operator` still refuses mechanicall-os markers

Markers (all present on this tree):

```text
PRODUCT.md
bin/aether
CORE_PRINCIPLES.md
AGENTS.md
```

`is_operator_tree(ROOT)` is **True** for `/mnt/kingston-nixos-sync/opt/mechanicall-os`.

`refuse_if_operator(ROOT)` raises `PocketError`:

```text
refused: /mnt/kingston-nixos-sync/opt/mechanicall-os is the mechanicall-os operator tree — bind a client pocket folder outside this repo
```

Same raise from the Chaquopy copy (`android/app/src/main/python/aether_pocket.py`). A temp folder without those four files is allowed.

Bind law unchanged: phone seat must use a client pocket (e.g. `/sdcard/mechanicall-pocket`), not this repo.

## Not done (out of engine scope)

- No Kotlin / `MainActivity.kt` edits.
- No `AndroidManifest.xml` edits.
- `applicationId` left as `com.mechanicall.pocket.demo`.
- No APK assemble (stage `04_verify`).
- Operator `CURRENT.md` not rewritten; no `aether approve`.

## Handoff

Engine copy is in the Chaquopy tree. Face specialist owns chrome. Next stage `04_verify` assembles debug APK when JDK 17 + SDK 34 + `gradlew` exist.
