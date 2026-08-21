# Sprint receipt — mobile-planning-demo (demo only)

**When:** 2026-08-16  
**Preflight:** `aether preflight mobile-planning-demo` → **Allowed** (Next field matches).  
**Operator CURRENT body:** still drifted (Action id `casual-core-interface`). Not rewritten.

## Done this turn (weeks 1–4 proven on host; face scaffolded)

| Week | Proof |
|------|--------|
| 1 | `python/aether_pocket.py` + refuse operator tree. `current` / `current validate` via real `bin/aether` on a temp pocket. Tests OK. |
| 2 | `projection()` / brief / events / drift wired. |
| 3 | `write_propose` does not touch CURRENT.md (tested). |
| 4 | `yes()` apply-PROPOSE + `aether approve`; events + DECISIONS + fields match CLI. `not_yet` → SELECT. Contract: `tests/test_aether_pocket.py` **10 passed**. |
| 5 | `agent_edit_propose` + whole-tree packer exist. Not called against live Ollama this turn. |
| 6 | Compose face in `android/` (LAB): CURRENT, receipts, Yes/Not yet, editor, agent button. APK not assembled (no ANDROID_SDK in this shell). |

## Paths

- Engine: `python/aether_pocket.py`
- Tests: `tests/test_aether_pocket.py`
- Template to **copy onto the phone**: `examples/pocket-demo-client/`
- Android LAB: `android/`
- Sync copy: `sh scripts/sync-pocket-engine.sh`
- Bind guard: `sh scripts/pocket-refuse-root.sh <path>` (exit 3 on this repo)

## Honest gaps (post-review / tweaks)

1. No debug APK from this host — need Android SDK / Studio for `assembleDebug`.
2. Stock phone has no bash `aether`. Sitting still needs `AETHER_HOME` + POSIX `aether` (Termux or copied tools) **or** a follow-up that bundles busybox. Same law; packaging leftover.
3. Ollama URL is a field; Tailscale must already reach myarch:11434.
4. Apply-PROPOSE only patches `**Field:**` lines (not whole-file replace). Enough for the sitting.
5. Operator CURRENT body still needs *your* apply of `examples/propose-current/PROPOSE-mobile-planning-demo.md`.

## Do not claim

- Play Store, product, casual-core complete, Session, Kotlin protocol clone.
