# Opus 5 PEER REVIEW brief

## Role this turn
You are **Claude Opus 5, peer reviewer** (not implementer, not approver).  
Human (Anphuni) authorized you as sprint collaborator earlier; this turn is **peer review documentation**.  
Host agent (Grok Build) will file your output next to previous peer docs.  
You **never** `aether approve`. Silence ≠ permission.

## Task
1. Re-adjudicate the **legacy awareness-scaffold critique** (archived as PEER-INPUT-…-LEGACY.md; full text included in user message context / host will attach).
2. Account for **prior peer chain**:
   - GPT-5.6 Sol CONDITIONAL (2026-08-04) — docs/boundary; absorbed into PRODUCT/AGENTS/etc.
   - Host correction: PEER-CORRECTION-AWARENESS-SCAFFOLD-CRITIQUE.md (claims most v0.1 paste is stale)
   - Protocol completion waves shipped + smoke-verify PASS + PR #3 merged to master (commits protocol + panel)
3. Produce a **new peer review of current mechanicall-os** that:
   - Verdicts claim-by-claim on the legacy paste (TRUE / FIXED / STILL OPEN / SUPERSEDED)
   - Reviews the **current product identity** (local authority protocol vs Session lab)
   - Surfaces residual risks after PR #3
   - Does **not** invent facts; use ground truth below when host verified

## Ground truth (host-measured 2026-08-04 after PR #3)

| Fact | Value |
|------|--------|
| Repo | github.com/17kizymaa/mechanicall-os |
| Default branch | master |
| Merge | PR #3 MERGED — `feat(protocol)` + `feat(panel)` on master tip ~5dd2c9f |
| Product identity | PRODUCT.md: local-first authority protocol (CURRENT + preflight + human yes). Session = capped multi-seat **lab**, not core |
| CLI | Single `./aether` POSIX sh, header **v0.2**, **~1880 lines** |
| Verbs | init, onboard, try, panel, shell, app, deinit, status, distill, watch, repair, poke, trust, **current**, **preflight**, **approve**, **reject**, **next**, **demo**, **brief**, **drift**, **probe**, event, artifact, seed, spark, session, graph, garden, rival… |
| SPEC | SPEC-v0.1.md (awareness sidecars) + **SPEC-v0.2.md** (authority protocol) |
| README Quick Start | Documents aether onboard/current/preflight/approve — **not** python cli.py path |
| CORE_PRINCIPLES | Markdown/JSON authority; **POSIX shell and/or Python** automation; distribution UIs may use other langs |
| .gitignore | Present (state.json, pycache, seat builds, qcow2, result*) |
| Tests | `tests/run.sh` extensive — smoke-verify ALL PASSED; demo/probe/brief/drift covered |
| python/ | Exists with panel, llm, shell agents — **no** `aether_distill.py` still |
| python_distill() | Still falls through to dumb_distill if no aether_distill.py |
| run_hook | **Fixed** — mutually exclusive executable OR sh (comment: review finding #2) |
| abspath | Special-cases `""` and `.` to `pwd -P` |
| cmd_distill | Counts files **after** python_distill |
| cmd_repair | Inspects markers; refuses distill on corrupt markers; not a pure alias |
| cmd_watch | Has `while true` poll path; entr path still one-shot list + entr -d |
| Unknown cmds | `*) cmd_status "$cmd"` — **still** treats typos as paths |
| SPEC-v0.1.md | Still ends with `---edit---` / `===edit marker===` residue |
| CORE_PRINCIPLES | No trailing "trigger line" junk |
| Live Next (host) | commit-hygiene APPROVED; residual dirty tree (nix/seat/dev archives) not all committed |
| License | Still none observed on host check |
| Grok seat | External TUI does **not** auto-preflight; human is gate (docs/GROK-SEAT.md) |

## Prior peer status (must honour)

GPT-5.6 CONDITIONAL mostly **absorbed**: PRODUCT/AUTHORITY/START-HERE/AGENTS CURRENT-first, Session honesty, principles shell amendment, protocol-first sprint, validate/demo shipped.  
Do not re-open "Session is core product."  
Do not recommend CURRENT v2 schema unless residual overload is severe.

## Required output format (STRICT markdown)

```
# Opus 5 peer review — mechanicall-os (2026-08-04)

## Meta
- Model, role, scope, baseline commit/branch if known
- Relationship to prior peer chain (GPT-5.6 + host correction)

## Executive verdict
- One of: PASS | CONDITIONAL | FAIL (for current public product narrative + code)
- ≤12 lines why

## Claim-by-claim: legacy scaffold critique
Table: claim | status (FIXED/STILL OPEN/SUPERSEDED/NEVER TRUE) | evidence | residual risk

## Current product review (v0.2 protocol)
Findings by severity 🔴🟠🟡 with concrete file pointers
Cover at least: authority lifecycle, Grok non-enforcement, LOC/spec tension, dead distill branch, SPEC-v0.1 markers, remaining dirty/uncommitted surfaces, Session boundary honesty on master after PR#3

## What the legacy critique got right (spirit)
Even if facts aged out

## What to do next (ordered, thin)
Wave-style recommendations for host; no approve claims
Propose thin Next action-ids only

## Non-claims
What you did not verify (live anphuni.com, CI, etc.)
```

Be rigorous and fair. Prefer SHORT over grandiose. No secrets.
