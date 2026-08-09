# Initial Architecture Sketch — Mechanicall OS v0

**Doc status:** **NON-NORMATIVE** — architecture sketch. Defer to SPEC-v0.2 / PRODUCT / CORE_PRINCIPLES.  
**Map:** `docs/DOC-AUTHORITY.md`

Three layers. Strictly following the Core Principles.

## 1. Filesystem Substrate

- Every Project is a **normal folder**.
- No special "workspace" databases or containers.
- Special **sidecar files** carry active state:
  - `.context.md` — distilled, human+machine readable project context
  - `.awareness.json` — lightweight structured metadata (timestamps, hashes, summaries)
  - `.memory/` — directory of small markdown fragments or indexed recall files
  - Other `.aether.*` or dotfiles as needed (always plain text / json / md)
- All sidecars are:
  - Small by design
  - Observable and editable with normal tools
  - Managed by inspectable shell/Python tools (never mutated magically)
  - Safe to `git add` / commit / share (or `.gitignore` selectively)

## 2. Awareness Layer (the daemon / agent)

A POSIX shell CLI called `aether` (optional Python helpers for panel/LLM).

Responsibilities:
- Observes file changes (within a project and optionally across projects)
- Distills context (single-project and cross-project)
- Updates sidecars
- Can be triggered manually (`aether update`, `aether distill`) or on events
- Maintains minimal in-memory state only while running; durable state is always in sidecars / FS
- Exposes a tiny CLI surface and optional simple socket or stdio for integration

Design constraints:
- Pure Python + stdlib where possible
- Extremely lightweight polling or native FS events (Linux inotify preferred)
- All behavior driven by or logged to `.md` / sidecars
- No persistent hidden stores

Example commands (to be implemented):
- `aether init` — bootstrap sidecars in current folder
- `aether watch` — start watcher for current (or specified) workspace
- `aether update` — manually trigger context refresh
- `aether distill --project .` — force context distillation
- `aether status` — show what sidecars exist and their freshness
- `aether cross-project ...` — awareness across multiple folders

## 3. Interface Layer

- **Authority substrate:** plain Markdown / JSON files + `aether` (POSIX shell).
- **Helpers:** Python for panel/shell-agent/LLM propose layers; never a second authority DB.
- **Not core product:** multi-tenant web SaaS dashboard (see `NOT-IMPLEMENTED.md`, `PRODUCT.md` boundary map).
- Primary self-hosted interaction:
  - Read/edit `CURRENT.md` and sidecars in your editor.
  - Run `aether` from shell (`current`, `preflight`, `approve`, `reject`).
  - Optional small `.py` scripts that consume/produce sidecars.
- Optional first-run helpers:
  - `aether onboard` — init + CURRENT + short preflight literacy
  - `aether app register` — mark a project as a development application
- Optional **Project Panel** (`aether panel`):
  - Cooperative TUI: CURRENT visible + chat/actions; mutations via `aether`
  - Not a sandbox that forces all tools through preflight (see ALPHA-LIMITATIONS)
- **Adjacent (not core):** anphuni.com Session = capped hosted alpha lab; separate privacy surface.

The Interface Layer is where humans and agents meet the protocol. Prefer boring and transparent over chrome that hides CURRENT.

### 3a. Optional Personal LLM (propose-only)

A **local** Ollama (or similar) personal model may sit under the Interface Layer as a
**propose substrate** for garden / rival / draft language. It is **not** an authority
layer: it never runs `aether approve`, never advances CURRENT, and never owns tools.

See **[docs/PERSONAL-LLM-LAYER.md](./docs/PERSONAL-LLM-LAYER.md)** and
`references/personal-llm-system.txt`. Wiring: `python/aether_llm.py` prefers
`personal-llm-*` tags when present; weights stay off-git.

## Layer Interactions

```
User / Scripts (Interface)  [+ optional personal-llm propose]
          ↕ reads + writes
Sidecars (.md, .json, dirs)  (Filesystem Substrate)
          ↕ observed + updated
aether (Awareness Layer)
```

- The Awareness Layer only ever reads and writes through the filesystem.
- Sidecars are the contract between all layers.
- The Filesystem Substrate is the durable truth.
- Personal LLM (if any) only **drafts**; human + `aether approve` remain sole authority.

## Non-Goals (for v0)

- Rich GUI or TUI
- Vector databases or embedded search indexes (use ripgrep + small md files + simple python indexes if needed)
- Heavy frameworks (no FastAPI, no SQLAlchemy, no LangChain in core)
- Cloud sync (git is the sync mechanism)
- Multi-user collaboration primitives beyond what git + markdown provides
- Multi-tenant SaaS / “everyone gets a remote full desktop”

## Direction (not shipped) — club-cortex shape

Operator-locked product direction (2026-07-25). **Research only** until CURRENT opens a phase. See:

- [`research/speculative/CLUB-CORTEX-SHAPE.md`](./research/speculative/CLUB-CORTEX-SHAPE.md) — anti-SaaS club, open-core + retainer sketch  
- [`research/speculative/MULTI-USER-LORA-CLUB-SCALE.md`](./research/speculative/MULTI-USER-LORA-CLUB-SCALE.md) — scaling math  

**Hardware roles (direction, not a deploy claim):**

| Role | Class | Job |
|------|--------|-----|
| GUI / presence | Low-end edge nodes (thin clients, daily laptops) | Capture, chat, light work |
| Desktop host | Capable machine (myarch-class) | **Backend**: queues, model serve, train jobs, networking, optional cloud bridge |
| Cloud | Deferred | Overflow/convenience for the **same backend jobs** — not a second identity |

Do **not** invert this into “product = multi-session remote XFCE.” Multi-user leverage is **protocol + multi-LoRA under Domain + fair queues**, not ten full DE seats. Personal LoRAs remain technique under Domain (propose/taste gate). Sample integrity: journals → transcripts → prompts (decay under reward bias).

## Evolution Path

Later versions may add:
- A tiny optional TUI (still Markdown-first)
- Better cross-project indexing (still filesystem backed)
- Pluggable "distillers" implemented as small Python scripts
- (Only with CURRENT) club backend queues / multi-adapter layout as in research docs

All additions must still obey the Core Principles and `NOT-IMPLEMENTED.md`.
