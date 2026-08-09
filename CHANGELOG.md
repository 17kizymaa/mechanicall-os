# Changelog

**Doc status:** **NON-NORMATIVE** — narrative history only.  
**Map:** `docs/DOC-AUTHORITY.md`

All notable changes to Mechanicall OS / `aether` are recorded here.
Format: newest first. Authority remains `CURRENT.md` + SPECs; this file is narrative.

## 2026-08-05

### Package alpha-2 prep (`package-alpha-2`)

- CURRENT rewritten: one Next `package-alpha-2`; Sept-9 casual-proof objective; 06c alignment.
- `docs/FIRST-PROJECT.md` — install → demo → refuse → resume → uninstall.
- `docs/RELEASE-NOTES-ALPHA-2.md` — prerelease draft (no tag until human + clean-machine).
- START-HERE / README / install-aether pointers.

## 2026-08-04

### Park — protocol alpha (`park-protocol-alpha`)

- Opus peer NEXT-01…10 complete on working tree; tests green.
- Handoff: `dev/18_opus5-protocol-completion/02_execute/output/PARK-PROTOCOL-ALPHA-RECEIPT.md`
- Uncommitted delta remains (~110 paths); commit/push is a separate human Next.

### Lab directory status (`next-10-lab-status`)

- `docs/LAB-STATUS.md` — SHIPPED / SUPPORT / LAB / ARCHIVE / LOCAL tags.
- Status lines on `research/`, `domains/`, `dev/`, `seat/` READMEs.

### Verb list + version (`next-09-verb-list`)

- `AETHER_VERSION` / `AETHER_VERBS` single sources in `aether`.
- `aether version` / `--version` / `-V`; `aether verbs`; help lists verbs.
- Bash completion: `scripts/aether-completion.bash` (loads verbs live).

### Document authority map (`next-08-normative-docs`)

- Added `docs/DOC-AUTHORITY.md` (NORMATIVE vs NON-NORMATIVE; conflict winners).
- Marked SPEC-v0.2 / PRODUCT / CORE_PRINCIPLES / AGENTS / NOT-IMPLEMENTED / ALPHA-LIMITATIONS as NORMATIVE.
- SPEC-v0.1 historical; README/ARCHITECTURE/AUTHORITY narrative NON-NORMATIVE.
- Tool alignment: live CLI = `aether` v0.2; protocol text = SPEC-v0.2.

### Shellcheck gate (`next-07-shellcheck`)

- `shellcheck -s sh aether` required in `tests/run.sh` (and `tests/shellcheck.sh`).
- aether cleaned to zero findings (hooks list via `find`, not `ls`).

### Preflight receipt (`next-06-preflight-receipt`)

- `aether preflight` writes `.aether/preflight-last` + append-only `preflight.jsonl` (ts, action, result, ec, fingerprint).
- `aether approve` prints `preflight: PASS|STALE|ABSENT` (never blocks).
- Approve accepts trailing project path with multi-word reasons.

### Decision — CLI size doctrine (`next-05-loc-decision`)

- **Retired** SPEC-v0.1 success criteria: `aether` ≤ 220 lines and “fits in one screen of `cat aether`”.
- **Kept** single POSIX `aether` file (no build step) as the core CLI.
- **Normative text:** SPEC-v0.2 → “CLI size doctrine”; SPEC-v0.1 LOC section marked HISTORICAL.
- **Why:** v0.2 authority verbs (`current`, `preflight`, `approve`, `next`, `probe`, `demo`, …) legitimately exceed a brutalist 220-line sketch. Leaving the old numbers standing was doctrine rot (Opus peer 🟠-1).
- **Not done this cycle:** splitting `aether` into multiple scripts.

### Protocol alpha (same day, earlier waves)

- Exit codes 0/1/2/3 (`next-04-exit-codes`)
- Apache-2.0 license discoverability (`next-03-license`; LICENSE already present)
- `tests/negative.sh` (`next-02-negative-tests`)
- Unknown command → exit 2 (`next-01-unknown-cmd`)
- PR #3: protocol demo/brief/drift/probe + panel commits merged to `master`
