# MBP (`mbp-edge`) — Mechanicall OS / aether versions pending 17kizymaa review

**Target machine only:** MacBook Pro 9,2 · Alpine 3.24.1 · host `mbp-edge`  
**Compiled:** 2026-07-09 · Access: `ssh mbp-root` / `ssh mbp-edge`

---

## Bottom line (MBP)

| Product | On MBP? | Version(s) present | Pending your review |
|---------|---------|----------------------|---------------------|
| **Mechanicall OS** (awareness-agent) | **Yes — primary tree** | **v0** (docs) · **v0.1** (SPEC + shell `aether`) · legacy Python **0.0.1** | Full doctrine pack + dev stages 01–04 outputs; stages **05/06 `05_review` empty** (waiting for human-gated pipeline) |
| **aetherOS** (Arch/mkarchiso demo) | **No** | — | Not installed/cloned on MBP. Lives on desktop/GitHub only. |
| Empty name collisions | — | — | No `/home/*/aetherOS`, no `mechanicalOS` dir on MBP |

---

## Where it lives on the MBP

```
/home/awareness-agent/          ← Mechanicall OS product root (owned root:root)
├── SPEC-v0.1.md                ← product spec (v0.1)
├── README.md                   ← "Mechanicall OS v0"
├── ARCHITECTURE.md             ← "Mechanicall OS v0"
├── CORE_PRINCIPLES.md
├── AGENTS.md
├── aether                      ← current runtime: POSIX sh, reports "aether v0.2 (shell)"
├── bin/aether -> ../aether
├── legacy/aether/              ← old Python package, __version__ = "0.0.1"
├── skills/codebase-review/
├── scripts/codebase_review.py  ← mechanical review CLI
├── dev/01 … 06                 ← staged work for human review gates
├── docs/getting-started.md
├── docs/nixos-transition.md
├── flake.nix / shell.nix       ← NixOS-first dev intent
└── .context.md / .aether/      ← live sidecars (last distill 2026-06-26)
```

**No git repo** under `/home/awareness-agent` (no `.git`). Version control is filesystem-only on this host until you push elsewhere.

Related but separate: `/home/local-navigator/` (local agent/navigator tooling — not Mechanicall OS).

---

## Version stack (what “versions” mean here)

| Layer | Identifier | Evidence on MBP |
|-------|------------|-----------------|
| Product brand | Mechanicall OS **v0** | README, ARCHITECTURE, CORE_PRINCIPLES |
| Spec revision | Mechanicall OS **v0.1** | `SPEC-v0.1.md` |
| Current CLI | **aether v0.2 (shell)** | `./aether --help` / header comment in `aether` (~384 LOC sh) |
| Legacy CLI | **aether 0.0.1** (Python) | `legacy/aether/__init__.py` — superseded by shell |
| Sidecar conventions | **v0** | README table |
| Distill snapshot | 2026-06-26 · 88 files | `.aether/state.json` |

There is **no** semver git tag and **no** separate “aetherOS v0.1.0-demo.1” ISO/demo tree on this laptop.

---

## Dev stages pending human review (ICM gates)

Design of stages 05–06: *“Review / edit anything in output/ … Human edits at output/ gates are the primary way to steer.”*  
`05_review` must write `output/final.md` + `summary.md` then stop for you.

| Stage | Path | Status for 17kizymaa |
|-------|------|----------------------|
| **01** Research Grok Heavy reviews | `dev/01_research-grok-heavy-reviews/` | Outputs present (research-summary, multi-agent strategy, rates verification, …). Reviewable. |
| **02** Code-review command | `dev/02_test-code-review-command/` | Outputs present (design, verification-summary, test-instructions). Reviewable. |
| **03** Mechanical codebase-review | `dev/03_mechanical-codebase-review/` | Explicit: **“All artifacts ready for review/edit.”** Design + scripts + skill. Approve Level 2 / MCP next. |
| **04** Swarm mimic | `dev/04_codebase-review-swarm-mimic/` | Notes only (`usage-and-mimic-notes.md`). Light review. |
| **05** Grok USB bootstrap | `dev/05_grok-usb-bootstrap/` | **Stuck mid-pipeline:** `01_analyze` ✓ (2 files), `02_plan` has `output/plan.md` and `summary.md`, `03_implement` ✓ (make-portable-usb.py + execution-report), `04_verify` empty, **`05_review` empty**. USB portable Grok+aether installer — **needs your gate before plan/verify/final review**. |
| **06** NixOS install | `dev/06_nixos-install/` | **Stopped after analyze:** `01_analyze` ✓ (7 files incl. configuration.nix, disk-analysis, bootstrap script), **`02_plan`→`05_review` all empty**. **Destructive intent** (repurpose ~300GB Alpine root for NixOS) — **do not proceed without explicit 17kizymaa approval**. |

### Highest-priority review packet (stage 03)

On MBP:

```bash
ssh mbp-root
cd /home/awareness-agent
less SPEC-v0.1.md
less dev/03_mechanical-codebase-review/output/summary.md
less dev/03_mechanical-codebase-review/output/mechanical-design.md
less skills/codebase-review/SKILL.md
# optional smoke:
# export XAI_API_KEY=… ; ./scripts/codebase-review .
```

Decisions you still own:
- Accept **Level 1** mechanical API review as shipped?
- Approve **Level 2** tool-calling?
- Approve **MCP** only if minimal (design currently: skip for v1)?

---

## aetherOS on MBP

**Absent.** Confirmed: no `aetherOS` directory under `/home` or shallow filesystem search.  
If you want aetherOS review *on this machine*, it must be **cloned or rsynced** from the desktop (`~/aetherOS`) or GitHub `17kizymaa/aetherOS`.

---

## Host context (why MBP is the dogfood target)

- Alpine **3.24.1**, kernel **6.18.35-lts**
- Network: wlan `192.168.1.88`, Tailscale `100.70.86.90` (`mbp-edge`)
- Product docs already push **NixOS transition** while host remains Alpine — that tension is part of stage 06 review

---

## Suggested review order for 17kizymaa (on MBP only)

1. Doctrine freeze: `CORE_PRINCIPLES.md` + `SPEC-v0.1.md` + shell `aether` vs legacy `0.0.1`  
2. Stage **03** mechanical review (ready)  
3. Stages **01–02** research/design (background)  
4. Stages **05–06** — decide whether to run/finish ICM or scrap; review gates currently empty at final step  
5. Optional: rsync **aetherOS** from desktop if that product should also be reviewed *here*

---

## Copy pack to phone (from desktop when adb up)

Source of this report: desktop `~/exports/MBP-VERSIONS-PENDING-REVIEW.md`  
(Pull from MBP via `ssh mbp-root 'tar czf - /home/awareness-agent/SPEC-v0.1.md …'` if needed.)
