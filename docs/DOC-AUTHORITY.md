# Document authority map

**Doc status:** NORMATIVE — how to resolve conflicts between markdown files.  
**Date:** 2026-08-04 · `next-08-normative-docs`  
**Tool version:** `aether` v0.2 (repo-root POSIX CLI)

## Winner order (when two docs disagree)

1. **Live instance:** project `CURRENT.md` (gates Next / preflight / approve)  
2. **Protocol contract:** `SPEC-v0.2.md` (schema, exit codes, preflight rules, CLI size doctrine)  
3. **Product boundary:** `PRODUCT.md` (what is core vs Session lab vs research)  
4. **Principles:** `CORE_PRINCIPLES.md` (filesystem truth, cooperative authority)  
5. **Agent operating rules:** `AGENTS.md` (CURRENT-first; models never approve)  
6. **Core denials:** `NOT-IMPLEMENTED.md`  
7. Everything else — **NON-NORMATIVE** (narrative, design, history, receipts)

If a NON-NORMATIVE doc conflicts with (1)–(6), **the higher item wins**.  
If SPEC-v0.1 conflicts with SPEC-v0.2, **SPEC-v0.2 wins** (v0.1 is historical).

## Labels

| Label | Meaning |
|-------|---------|
| **NORMATIVE** | Load-bearing. May be cited as product/protocol law. |
| **NON-NORMATIVE** | Helpful narrative, design, ops, research, or history. Defer on conflict. |
| **INSTANCE** | Per-project live state (not a factory doc). |

## Catalog (core tree)

| Path | Status | Notes |
|------|--------|--------|
| `CURRENT.md` | **INSTANCE** | Sole live Next / Approval gate for that project |
| `SPEC-v0.2.md` | **NORMATIVE** | Authority protocol + CLI exit codes + size doctrine |
| `SPEC-v0.1.md` | **NON-NORMATIVE** (historical) | Awareness sidecars; LOC ≤220 **retired** |
| `PRODUCT.md` | **NORMATIVE** | Boundary map + license framing |
| `CORE_PRINCIPLES.md` | **NORMATIVE** | Locked core principles |
| `AGENTS.md` | **NORMATIVE** | Agent operating protocol (CURRENT-first) |
| `NOT-IMPLEMENTED.md` | **NORMATIVE** | Explicit denials for core claims |
| `AUTHORITY.md` | **NON-NORMATIVE** | Durable doctrine essay; does not replace CURRENT or SPEC-v0.2 |
| `ARCHITECTURE.md` | **NON-NORMATIVE** | Sketch / structure |
| `README.md` | **NON-NORMATIVE** | Entry narrative |
| `START-HERE.md` | **NON-NORMATIVE** | Read-order routing |
| `CHANGELOG.md` | **NON-NORMATIVE** | Narrative history |
| `LICENSE` | **NORMATIVE** (legal) | Apache-2.0 |
| `docs/DOC-AUTHORITY.md` | **NORMATIVE** | This map |
| `docs/ALPHA-LIMITATIONS.md` | **NORMATIVE** (limits honesty) | What core does **not** force |
| `docs/PROTOCOL-TEST-SURFACE.md` | **NON-NORMATIVE** | Sprint design + claim→command map |
| `docs/GROK-SEAT.md` | **NON-NORMATIVE** | Ops contract for Grok TUI |
| `docs/PROTOCOL-LAB.md` | **NON-NORMATIVE** | Lab design |
| `docs/SINGLE-APP-DISTRIBUTION.md` | **NON-NORMATIVE** | Incomplete product shape |
| `docs/PANEL-GROK-SPLIT.md` | **NON-NORMATIVE** | UI contract |
| `docs/OUTLOOK-RESEARCH-BOUNDARY.md` | **NON-NORMATIVE** | Research bound |
| `dev/**` | **NON-NORMATIVE** | ICM stages, peer reviews, receipts |
| `research/**` | **NON-NORMATIVE** | Speculative only |
| `docs/AGENT-AGNOSTIC-COLD-START.md` | **NON-NORMATIVE** | Any agent/IDE cold-start checklist (no TUI required) |
| `docs/LAB-STATUS.md` | **NON-NORMATIVE** | Lab vs shipped directory tags (`next-10`) |

Directory lab tags (LAB / SHIPPED / ARCHIVE): **`docs/LAB-STATUS.md`**.

## Tool alignment

| Claim | Truth |
|-------|--------|
| Live CLI | Repo-root `./aether` (POSIX sh), header **v0.2** |
| Normative protocol text | **SPEC-v0.2.md** (not v0.1) |
| “One screen / ≤220 lines” | **Retired** — see SPEC-v0.2 CLI size doctrine |

## Anti-patterns

- Citing `dev/` peer reviews as CURRENT or SPEC  
- Treating Session lab docs as core product law  
- Preferring SPEC-v0.1 LOC budget over shipped `aether`  
- Letting README marketing override NOT-IMPLEMENTED or PRODUCT boundary  
