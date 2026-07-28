# Speculative / direction documents

**Default status: FICTIONAL / NOT IMPLEMENTED as product features**

This directory holds architecture notes, external analyses, and **operator direction**
that must **not** be treated as shipping acceptance criteria unless the same claim
is implemented in this repository and gated by `CURRENT.md`.

Durable truth for the **shipped** OS lives in:

- `CORE_PRINCIPLES.md`
- `ARCHITECTURE.md`
- `SPEC-v0.1.md` / `SPEC-v0.2.md`
- `NOT-IMPLEMENTED.md`
- the `aether` CLI and plain project sidecars

---

## Index

| Document | Kind | Notes |
|----------|------|--------|
| **[CLUB-CORTEX-SHAPE.md](./CLUB-CORTEX-SHAPE.md)** | **Operator direction** (2026-07-25) | Product shape: anti-SaaS club, GUI-at-edge, desktop-as-backend, journal→LoRA hierarchy. Not multi-tenant SaaS. |
| **[MULTI-USER-LORA-CLUB-SCALE.md](./MULTI-USER-LORA-CLUB-SCALE.md)** | Research analysis | Scaling math for ≤100 / ~10 concurrent; queues vs full desktops. |
| **[DASHBOARD-WITHOUT-COMPROMISE.md](./DASHBOARD-WITHOUT-COMPROMISE.md)** | Interface research (2026-07-27) | Project Panel: HTML/localhost UI that only projects files + shells to `aether`. Not SaaS dashboard. |
| **[KINGSTON-VAULT-EVAL.md](./KINGSTON-VAULT-EVAL.md)** | Host research | LUKS vault usefulness vs protocol product |
| **[KINGSTON-NIXOS-STATE-REVIEW.md](./KINGSTON-NIXOS-STATE-REVIEW.md)** | Host review (2026-07-27) | Live + flake review of portable Kingston Phase 2 image |
| **[VIRTUALIZATION-OPTIONS.md](./VIRTUALIZATION-OPTIONS.md)** | Host dev (2026-07-27) | KVM guest `#portable-kingston-vm` + virtiofs; stick stays portable |
| `mechanicall-os-v0.2.handoff.md` | External / companion | Handoff notes; verify claims against code. |

---

## How to read club-cortex docs

1. **Shape** (`CLUB-CORTEX-SHAPE.md`) defines **where the project is going** in the operator’s words.  
2. **Scale research** (`MULTI-USER-LORA-CLUB-SCALE.md`) explains **limits and phases** without authorizing a build.  
3. **`NOT-IMPLEMENTED.md`** still kills Cortex/SaaS/monorepo fiction and multi-user platform claims **until CURRENT opens a phase**.

If a document claims PostgreSQL, LangGraph, pgvector, Cortex/Ganglion runtimes,
sandboxed tool execution, mandatory Critic validation, holographic state, or any
other enterprise agent platform machinery — treat it as fiction unless the same
claim is also implemented in this repository.

See `NOT-IMPLEMENTED.md` at the repo root for the explicit denial list.
