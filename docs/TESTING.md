<!-- generated-by: gsd-doc-writer -->
# Testing

Mechanicall OS is validated with a **single POSIX shell integration suite** that
drives the real `aether` CLI against temporary project directories. There is no
pytest, unittest, Jest, or other unit-test framework in this repository.

The suite lives at [`tests/run.sh`](../tests/run.sh). It exercises both the
**v0.1 awareness / trust** surface and the **v0.2 authority** surface (CURRENT,
preflight, approve/reject, events, artifacts).

---

## Test approach

| Aspect | Detail |
|--------|--------|
| Framework | Plain POSIX `sh` (`#!/bin/sh`, `set -e`) |
| Subject under test | Repo-root [`aether`](../aether) script |
| Isolation | Temp dir `$TMPDIR/aether-test.$$` (cleaned on exit) |
| Env | `AETHER_HOME` set to repo root; repo root prepended to `PATH` |
| Assertions | File existence, `grep`, exit codes, tree hashes, event log lines |
| Coverage tooling | None configured |
| Unit tests / pytest | **Not used** |

Each case prints `ok: <name>` on success or `FAIL: <message>` and exits non-zero
on failure. A clean run ends with:

```text
All aether integration tests passed.
```

No external services, databases, or LLM keys are required. Core tests only need
a POSIX shell and the standard utilities already used by `aether` (`grep`,
`sed`, `awk`, `mkdir`, `chmod`, etc.).

---

## Running tests

From the repository root:

```bash
./tests/run.sh
# equivalent:
sh tests/run.sh
```

Optional Nix-based dev shell (tools only; not required for the suite):

```bash
nix develop
./tests/run.sh
```

There is no watch mode, no file-filter flag, and no per-test CLI selector. To
run a subset, temporarily comment cases in `tests/run.sh` or copy the relevant
block into a scratch script.

**Expected output (abbreviated):**

```text
ok: init
ok: init idempotent
ok: human context preserved
ok: human survives repeated distill
ok: hooks run exactly once
ok: --no-hooks
ok: untrusted hooks skipped
ok: trust
ok: path with spaces (explicit arg + hash semantics)
ok: empty project
ok: init does not auto-trust pre-existing hooks
ok: seed preserves multiword spacing
ok: corrupt markers refuse distill
ok: poke/run_hook trust boundary
ok: v0.2 authority: preflight refuse/allow, reject, approve, events, artifacts
ok: v0.2 non-reel authority model
ok: preflight refuses without CURRENT.md

All aether integration tests passed.
```

---

## What is covered

### v0.1 P0 — awareness, trust, and safety

| Case | What it asserts |
|------|-----------------|
| `init` | Creates `.context.md`, `.aether/trusted`, `.aether/.scope` |
| `init idempotent` | Re-running `aether init` succeeds |
| `human context preserved` | Human prose in `.context.md` survives `distill`; generated markers present |
| `human survives repeated distill` | Multiple distills keep human-edited lines outside generated region |
| `hooks run exactly once` | Trusted `on-distill` hook fires exactly once per distill |
| `--no-hooks` | Hook is not run when `--no-hooks` is passed |
| `untrusted hooks skipped` | Without `.aether/trusted`, hooks do not run; warning mentions untrusted/skip |
| `trust` | `aether trust` recreates `.aether/trusted` |
| `path with spaces` | Explicit path arg with spaces works; tree hash changes when spaced filename content changes; filename appears in generated sample |
| `empty project` | Init + distill succeed on an empty directory |
| `init does not auto-trust pre-existing hooks` | Clone-style dir with existing `on-distill` is **not** auto-trusted; malicious hook does not run |
| `seed preserves multiword spacing` | `aether seed "preserve   deliberate   spacing"` keeps internal spaces in inbox |
| `corrupt markers refuse distill` | Orphan `aether:generated:start` without end → distill fails; file not overwritten |
| `poke/run_hook trust boundary` | `poke` respects `--no-hooks` / trust for `on-save` |

### v0.2 — authority model

| Case | What it asserts |
|------|-----------------|
| Reel-shaped authority | `preflight rough-v6` **refused**; `silent-proof` **allowed**; non-next action refused while blocked |
| Events | `.aether/events.jsonl` logs `preflight` with `result: refused` |
| Artifacts | `aether artifact … --action silent-proof --status produced` writes meta under `.aether/artifacts/` and an artifact event |
| Reject | Sets Phase `SELECT`, Status `REJECTED`; logs reject event; `rough-v6` still refused (no auto-rebuild) |
| Approve | Sets `APPROVED`; logs approve event; creates `DECISIONS.md` |
| Seeds ≠ authority | `aether seed "please build rough-v6 now"` does **not** unlock prohibited actions or mutate Next |
| Non-reel (dev-task) | `add-postgres` refused; `write-tests` allowed — model is action-id generic |
| No CURRENT | `preflight` without `CURRENT.md` refuses everything consequential |

These cases mirror the product fixtures under `examples/` (see below).

---

## Manual verification / examples

The automated suite uses synthetic temp projects. For operator-facing walkthroughs
that a human (or agent) can `cat` and re-run by hand:

### `examples/reel-control/` — Mission 4 exit gate

Product proof that agents stop after a human reject signal. No media tools required.

```bash
cd examples/reel-control
../../aether init .
../../aether current

../../aether preflight rough-v6       # Refused (prohibited / not Next)
../../aether preflight silent-proof   # Allowed

mkdir -p artifacts
echo "placeholder silent proof" > artifacts/proof-01.txt
../../aether artifact artifacts/proof-01.txt --action silent-proof --status produced

../../aether reject "arrival on plate 4 fails"
../../aether preflight rough-v6       # still refused
../../aether current                  # Phase SELECT, Status REJECTED

cat CURRENT.md
cat DECISIONS.md
cat .aether/events.jsonl
```

See [`examples/reel-control/README.md`](../examples/reel-control/README.md).

### `examples/dev-task/` — non-reel generality

Shows authority is not hardcoded to video editing:

```bash
cd examples/dev-task
../../aether init .
../../aether preflight add-postgres     # Refused
../../aether preflight write-tests      # Allowed
../../aether approve "tests green"      # Human only
```

See [`examples/dev-task/README.md`](../examples/dev-task/README.md).

### Sidecar fixture

[`examples/sidecars/example-project/`](../examples/sidecars/example-project/) holds
sample sidecar layout for inspection; it is not driven by `tests/run.sh`.

---

## Adding tests

1. Open [`tests/run.sh`](../tests/run.sh).
2. Create an isolated directory under `$TMP` (the suite already sets
   `TMP="${TMPDIR:-/tmp}/aether-test.$$"` and a cleanup trap).
3. Call `"$AETHER"` (absolute path to repo-root `aether`) with explicit project
   paths when needed.
4. On failure call `fail "message"`; on success call `pass "short name"`.
5. Prefer assertions that check **behavior** (refuse/allow messages, event
   `kind` fields, file contents after reject/approve) — not only exit code zero.
6. Keep dependencies at zero: no network, no LLM keys, no Python test runners.
7. Re-run the full suite:

```bash
./tests/run.sh
```

**Conventions observed in the suite:**

- Redirect noisy stdout with `>/dev/null` when only success matters.
- Capture stderr/stdout for message checks: `out=$("$AETHER" … 2>&1)`.
- For expected failures, do **not** rely on `set -e` alone — capture exit and
  assert refuse/allow text with `grep -qi`.
- Authority fixtures write a full `CURRENT.md` with `**Next:**`, `## Prohibited`,
  and action ids that match what `preflight` receives.

When a new CLI surface lands (new command or gate), add a case here before
claiming the behavior is shipped. Spec contracts:
[SPEC-v0.1.md](../SPEC-v0.1.md), [SPEC-v0.2.md](../SPEC-v0.2.md).

---

## Coverage requirements

No coverage threshold is configured. There is no `coverageThreshold`, c8, or
pytest-cov setup. Completeness is judged by whether P0 trust/safety cases and
v0.2 authority gates in `tests/run.sh` pass.

---

## CI integration

No CI workflow was found in this repository (no `.github/workflows/`, no
in-repo GitHub Actions or other pipeline that runs `./tests/run.sh`).

Run the suite locally before merging or after changing `aether`, hooks, or
authority parsing:

```bash
./tests/run.sh
```

---

## Related docs

- [README.md](../README.md) — quick start and development pointer
- [ARCHITECTURE.md](../ARCHITECTURE.md) — layers and sidecar roles
- [CONFIGURATION.md](./CONFIGURATION.md) — env vars and project layout
- [SPEC-v0.2.md](../SPEC-v0.2.md) — authority contract under test
- [NOT-IMPLEMENTED.md](../NOT-IMPLEMENTED.md) — features that must **not** appear in tests as if real
