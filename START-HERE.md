# Start here

**Doc status:** **NON-NORMATIVE** — read-order routing only.  
**Map:** [docs/DOC-AUTHORITY.md](./docs/DOC-AUTHORITY.md) (who wins on conflict)

## For product truth (read order)

0. **[docs/DOC-AUTHORITY.md](./docs/DOC-AUTHORITY.md)** — NORMATIVE vs NON-NORMATIVE; conflict winners  
0b. **[docs/LAB-STATUS.md](./docs/LAB-STATUS.md)** — which dirs are shipped vs **lab**  
1. **[PRODUCT.md](./PRODUCT.md)** — boundary map (core protocol vs Session lab vs research)  
2. **[CURRENT.md](./CURRENT.md)** — live Next (**INSTANCE** gate)  
3. **[SPEC-v0.2.md](./SPEC-v0.2.md)** — **NORMATIVE** CURRENT + preflight contract (not SPEC-v0.1)  
4. **[docs/ALPHA-LIMITATIONS.md](./docs/ALPHA-LIMITATIONS.md)**  
5. **[NOT-IMPLEMENTED.md](./NOT-IMPLEMENTED.md)**  
5b. **[LICENSE](./LICENSE)** — **Apache-2.0** (repo + in-tree tools; Session host use ≠ redistribution terms — see PRODUCT.md License)  

## For contributing / agents

6. **[AGENTS.md](./AGENTS.md)** — **CURRENT first**, then ICM  
7. **[CORE_PRINCIPLES.md](./CORE_PRINCIPLES.md)**  
8. **[ARCHITECTURE.md](./ARCHITECTURE.md)**  

## For interfaces

9. **[docs/PANEL-GROK-SPLIT.md](./docs/PANEL-GROK-SPLIT.md)**  
10. **[docs/SINGLE-APP-DISTRIBUTION.md](./docs/SINGLE-APP-DISTRIBUTION.md)**  
11. **[docs/PROTOCOL-TEST-SURFACE.md](./docs/PROTOCOL-TEST-SURFACE.md)** — this sprint’s lab design  

## Personal models / research bounds

12. **[docs/PERSONAL-LLM-DEFINITION.md](./docs/PERSONAL-LLM-DEFINITION.md)** when present  
13. **[docs/OUTLOOK-RESEARCH-BOUNDARY.md](./docs/OUTLOOK-RESEARCH-BOUNDARY.md)**  

---

## What the product is (one line)

**Local authority protocol:** `CURRENT.md` + `aether preflight` + human yes.  
Hosted Session = optional capped **lab**, not the definition of Mechanicall.

## First project (casual / pilot)

**[docs/FIRST-PROJECT.md](./docs/FIRST-PROJECT.md)** — install → demo → project → refuse → resume → uninstall.  
Release notes draft: **[docs/RELEASE-NOTES-ALPHA-2.md](./docs/RELEASE-NOTES-ALPHA-2.md)**.

## Developer path (core)

```bash
aether current
aether current validate
aether preflight <action>
# human: aether approve "…"
```

## Casual packaging (incomplete)

Single-app distro / seat UX: **[docs/SINGLE-APP-DISTRIBUTION.md](./docs/SINGLE-APP-DISTRIBUTION.md)**.  
Not “learn the CLI to manage files” as the casual dream — but **protocol literacy** still is the product.

```bash
sh scripts/try.sh   # service/dev sample Domain — not the casual front door
```
