# Peer review — mechanicall-os (host adjudication, 2026-08-04)

**Author:** Grok Build host agent (not Claude Opus 5)  
**Reason:** OpenRouter `anthropic/claude-opus-5` chat returned **401 User not found** for both Desktop `.env` `sk-or-` keys.  
**Role:** peer-style adjudication so the review chain is complete; **replace with live Opus output when key works**.  
**Authority:** PROPOSAL / review artifact — **not CURRENT**  
**Baseline:** `origin/master` after PR **#3** merged (`5dd2c9f` merge commit; protocol + panel commits `6a1a014`, `33abafa`)  
**Filed with prior peer chain:** GPT-5.6 Sol CONDITIONAL (`06b_…`), absorb (`PEER-ABSORB-…`), host scaffold correction (`PEER-CORRECTION-…`)

---

## Meta

| | |
|--|--|
| Scope | Legacy v0.1 awareness-scaffold critique + current v0.2 protocol product on master |
| Operator | Anphuni — sole `aether approve` |
| Product lock | Local authority protocol; Session = capped lab; Grok seat observes, does not auto-preflight |

---

## Executive verdict

**CONDITIONAL** for “coherent public alpha narrative + runnable protocol core.”

**Why (short):**

1. The legacy paste is **largely SUPERSEDED** as a description of today’s tree; treating it as live inventory would mislead peers and agents.  
2. Core protocol surface is **runnable and tested** (`demo`, `preflight`, `approve`, `next`, `validate`, `probe`, `brief`, `drift`; `tests/run.sh` green on smoke-verify).  
3. Residual debt is real: **dead `python_distill` branch**, **SPEC-v0.1 edit markers**, **unknown-subcommand → status**, **~1880-line `aether` vs brutalist LOC myth**, **no LICENSE**, **uncommitted nix/seat/dev archives**, **Grok non-enforcement** (by design, must stay honest).  
4. GPT-5.6 boundary absorb + PR #3 closed the worst public-truth gap for PRODUCT/AGENTS/protocol docs **on master**.  
5. CONDITIONAL, not PASS: awareness-layer quality and “small `aether`” story still lag authority-layer maturity.

---

## Claim-by-claim: legacy scaffold critique

| # | Claim | Status | Evidence (2026-08-04 host) | Residual risk |
|---|--------|--------|----------------------------|---------------|
| R1 | README Quick Start uses `python3 /home/awareness-agent/aether/cli.py` | **FIXED / NEVER TRUE for current README** | README documents v0.2 aether onboard/current/preflight/approve | Stale paths may remain in older `docs/*` (nixos-transition, MBP notes) |
| R2 | README Status “scaffolding only” | **FIXED** | README “What it is (v0.2)” authority questions | Overclaim risk if Single-App distro pitched as done |
| R3 | CORE_PRINCIPLES “Markdown + Python only” | **FIXED** | Principles: shell and/or Python; UIs may use other langs | SPEC-v0.1 still carries older language in places |
| R4 | Trigger junk at end of CORE_PRINCIPLES | **FIXED** | No trailing trigger line | — |
| R5 | SPEC-v0.1 ends with `===edit marker===` | **STILL OPEN** | File still ends `---edit---` / `===edit marker===` | Looks unprofessional; easy strip |
| R6 | No `python/` + dead `python_distill` | **PARTLY OPEN** | `python/` exists (panel/llm/shell) but **no** `aether_distill.py`; still falls to `dumb_distill` | Dead branch rot; decide write-or-delete |
| R7 | Hooks run twice | **FIXED** | `run_hook`: executable OR `sh`, mutually exclusive | Regression tests should keep locking this |
| R8 | `abspath` mangles `.` | **FIXED** | `""` and `.` → `pwd -P` | Edge cases for non-dir paths |
| R9 | distill stamps pre-compute over writer | **FIXED** (directionally) | counts/hash after `python_distill` | Embed-comment path still worth audit |
| R10 | `watch` entr dies on new files | **PARTLY OPEN** | poll path has `while true`; entr path still list + `entr -d` | New files may still drop entr loop |
| R11 | Unknown cmds → silent status | **STILL OPEN** | `*) cmd_status "$cmd"` | Typos exit 0; agents confuse themselves |
| R12 | No `.gitignore` | **FIXED** | Present; state.json, pycache, seat, qcow2, result* | Keep reviewing what lands in git |
| R13 | LOC ≤220 / “one screen” | **SUPERSEDED / renegotiate** | `aether` ~**1880** lines; authority product expanded | Either split modules or rewrite success criterion |
| R14 | `repair` is lie (alias distill) | **FIXED (improved)** | Inspects markers; refuses corrupt; then distill | Not full “restore from mangle” magic |
| R15 | No tests/CI/LICENSE | **PARTLY FIXED** | Strong `tests/run.sh`; CI control-layer gates exist in-repo; **no LICENSE** | LICENSE still missing; public CI may be thin |
| R16 | Only six verbs | **SUPERSEDED** | Large authority + capture + UI surface | Docs must lead with protocol verbs |

---

## Current product review (v0.2 protocol)

### 🔴 High (honesty / confusion)

1. **LOC / brutalist myth** — SPEC-v0.1 “fits in one screen of `cat aether`” is false for the shipped CLI. Renegotiate in SPEC-v0.2 or factor authority subcommands. Leaving both myths invites peer FAIL next cycle.  
2. **Dead smart-distill branch** — `python_distill()` without `python/aether_distill.py` is exactly the rot the doctrine forbids. Write ≤80 lines or delete the branch + SPEC claim.  
3. **Grok/external TUI non-enforcement** — Correct by design (`docs/GROK-SEAT.md`), but any marketing that implies “agents cannot act without preflight” is false. Keep ALPHA-LIMITATIONS loud.

### 🟠 Medium

4. **Unknown subcommand swallow** — still `*) cmd_status`. Fix: die unless `[ -d "$1" ]`.  
5. **SPEC-v0.1 edit markers** — strip residue; freeze v0.1 as historical or mark archival.  
6. **Dirty tree beyond PR #3** — nix/kingston, seat/, older `dev/*`, research still uncommitted or local. Peer cannot assume master == full host workspace.  
7. **CURRENT body lag** — header Next can move via `aether next` while prose “Next allowed action” stays stale (seen during smoke-verify). Prefer thin template fields or post-`next` prose refresh by human/script (not model auto-write).

### 🟡 Low / hygiene

8. **No LICENSE** — choose one.  
9. **File-type whitelist for distill** — still narrow for Nix/JS/Rust monorepos; `.aether/.include` still a good idea if awareness layer is product.  
10. **Session lab honesty** — GPT-5.6 absorb landed on host/docs; re-check live privacy page only when deploying site (not verified this turn).

---

## What the legacy critique got right (spirit)

- **Docs can lie about code** — still the highest-value peer habit; run claim maps (`docs/PROTOCOL-TEST-SURFACE.md`).  
- **Dead branches rot brutalism** — distill path still proves it.  
- **Silent failures teach agents bad habits** — unknown subcommands.  
- **Tests catch hook double-fire** — fixed because someone measured; keep tests.  
- **Spec success criteria that can’t be met should be amended, not ignored.**

---

## What to do next (ordered, thin)

| Wave | Goal | Acceptance |
|------|------|------------|
| W0 | Strip SPEC-v0.1 edit markers; note v0.1 archival vs v0.2 authority | `tail SPEC-v0.1.md` clean; START-HERE points v0.2 |
| W1 | Kill or implement `aether_distill.py` | No silent dead branch; SPEC text matches |
| W2 | Unknown cmd → `die` unless directory path | `aether distil` nonzero |
| W3 | Renegotiate LOC success criterion or split `aether` | SPEC-v0.2 honest about size |
| W4 | LICENSE | File present |
| W5 | Optional: commit batches C–F per COMMIT-HYGIENE-PLAN | Human picks |

### Proposed thin Next action-ids (human only)

- `strip-spec-v01-markers`  
- `distill-write-or-delete`  
- `unknown-cmd-die`  
- `license-choose`  
- `park-protocol-alpha`  

---

## Non-claims / not verified this turn

- Live anphuni.com Session/privacy HTML  
- OpenRouter key validity (failed)  
- Whether GitHub Actions CI is green on PR #3 beyond local `tests/run.sh`  
- Full audit of `embed_state_comment` multi-line HTML comment edge cases  
- Content of uncommitted seat/nix trees  

---

## Relation to prior peer chain

| Artifact | Role |
|----------|------|
| GPT-5.6 `06b` CONDITIONAL | Boundary/docs; largely absorbed |
| `PEER-ABSORB-PROTOCOL-FIRST` | Operator decisions after GPT-5.6 |
| `PEER-CORRECTION-AWARENESS-SCAFFOLD-CRITIQUE` | Host: legacy paste ≠ current inventory |
| **This file** | Re-adjudicates full legacy findings against post–PR #3 master; **interim until Opus 5 chat works** |
| `PEER-INPUT-…-LEGACY` | Archived original paste |

---

## Bottom line

> **Do not use the 2026-07-era “cli.py / scaffolding only” paste as a review of current mechanicall-os.**  
> Current core is a **runnable local authority protocol** with tests and PR #3 on master.  
> Remaining peer pressure is **coherence of the awareness-layer leftovers** (distill, SPEC-v0.1 markers, unknown cmds) and **honest sizing** of `aether`, not “does the protocol exist.”

---

*Replace this document with `PEER-REVIEW-OPUS5-2026-08-04.md` from a successful OpenRouter Opus call when keys work.*
