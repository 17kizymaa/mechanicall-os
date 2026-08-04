# Lab vs shipped — directory status

**Doc status:** **NON-NORMATIVE** catalog (labels for humans/agents).  
**Does not** replace PRODUCT.md boundary or SPEC-v0.2.  
**Date:** 2026-08-04 · `next-10-lab-status`  
**Map:** `docs/DOC-AUTHORITY.md`

## Purpose

A reader must see **what is shipped protocol** vs **lab / experiment / may vanish** without reading every file.  
Vendoring a lab tree as “Mechanicall core” is a claim error.

## Status vocabulary

| Tag | Meaning |
|-----|---------|
| **SHIPPED** | Part of v0.2 core product surface; covered by SPEC-v0.2 / PRODUCT core |
| **SUPPORT** | In-tree helpers for core (tests, install scripts); not the product definition alone |
| **LAB** | Experimental / incomplete; not core; may change or vanish; not covered by SPEC as complete product |
| **ARCHIVE** | Historical ICM/dev receipts; Layer-4 only |
| **LOCAL** | Machine/build artifacts; do not treat as product (often gitignored) |

## Root / core (SHIPPED or SUPPORT)

| Path | Tag | Note |
|------|-----|------|
| `aether` | **SHIPPED** | POSIX CLI v0.2 |
| `SPEC-v0.2.md` · `PRODUCT.md` · `CORE_PRINCIPLES.md` · `AGENTS.md` | **SHIPPED** | Normative docs |
| `LICENSE` | **SHIPPED** | Apache-2.0 |
| `python/` (panel, shell, llm helpers) | **SUPPORT** | Cooperative UIs; not a second authority store |
| `scripts/` (protocol-demo, grok brief, try, …) | **SUPPORT** | Behaviours for core / ops |
| `tests/` | **SUPPORT** | Integration + unit |
| `docs/` (ALPHA-LIMITATIONS, DOC-AUTHORITY, GROK-SEAT, …) | **SUPPORT** | Mixed NORMATIVE/NON-NORMATIVE — see DOC-AUTHORITY |
| `examples/` | **SUPPORT** | Samples |
| `bin/` | **SUPPORT** | Install helpers |

## Explicit LAB / ARCHIVE / LOCAL

| Path | Tag | One-line status |
|------|-----|-----------------|
| `research/` | **LAB** | Speculative + personal-llm proposals — **not product claims** |
| `research/speculative/` | **LAB** | Club-cortex / vault / multi-LoRA sketches — research only |
| `domains/` | **LAB** | Sample Domain folders (house-tv-desk, minimal-cli) — not the product |
| `seat/` | **LAB** | Tauri/Vite seat shell — incomplete single-app experiment |
| `android/` | **LAB** | Android/boot experiments — not core protocol |
| `nix/` · `flake.nix` · `shell.nix` | **LAB** / host tooling | Portable Kingston / NixOS seating — distribution lab |
| `legacy/` | **ARCHIVE** | Old Python package path — not the one-true CLI |
| `dev/` | **ARCHIVE** / **LAB** | ICM stages, peer packs, client work — Layer-4 receipts |
| `dev/18_opus5-protocol-completion/` | **ARCHIVE** | Opus peer sprint workspace (receipts) |
| `.planning/` | **LOCAL** / tooling | GSD planning noise — not product |
| `.aether/` | **INSTANCE** | Project sidecars / events (per machine) |
| `result` · `result-vm` · `*.qcow2` | **LOCAL** | Nix/build/VM outputs — never product |

## Hosted Session (anphuni.com)

| Surface | Tag |
|---------|-----|
| Website Session seats | **LAB** (hosted multi-seat alpha ≤5) — **not** Mechanicall core (PRODUCT.md) |

## Rule of thumb

```text
If it is not aether + CURRENT + SPEC-v0.2 + PRODUCT boundary,
ask: is it labelled LAB/ARCHIVE in this file?
If yes → do not ship it as “the product.”
```
