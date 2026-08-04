# Core Principles (Locked In)

**Doc status:** **NORMATIVE** — locked core principles.  
**Conflict:** yields to live `CURRENT.md` and SPEC-v0.2 for operational gates; wins over casual docs on filesystem/cooperative authority.  
**Map:** `docs/DOC-AUTHORITY.md`

These principles define Mechanicall OS. They are non-negotiable for **core** product truth.

## Locked Principles

- **Filesystem is the single source of truth**  
  No hidden databases for authority. All state, context, memory, and configuration that *bind* a project live as plain files. Everything that matters is readable, editable, grep-able, and version-controllable with git.

- **Durable authority stays plain text**  
  User-owned authority and durable project state are **Markdown and JSON** (e.g. `CURRENT.md`, `.aether/events.jsonl`, sidecars).  
  **Core automation** uses inspectable **POSIX shell** and/or **Python**.  
  **Distribution interfaces** (Panel TUI, browser Session, future desktop shells) may use other languages, but **must not** become a second authority store — they call or project the same files.

- **Active context sidecars**  
  Small, observable files and scripts (e.g. `.context.md`, `.awareness.json`, `.memory/`, `.aether/`) live beside normal project files. They are first-class and manageable with normal tools.

- **Capture is sacred; structure is deferred**  
  Getting a thought into the filesystem must cost zero decisions and under two seconds. Filing and sorting happen later — proposed, then human-approved — never at the moment of entry. (See `docs/RHIZOME.md`.)

- **Extremely low overhead and high inspectability**  
  Lightweight; no unnecessary daemons. You can `cat`, `ls`, `grep`, `tail`, `diff` everything that matters. Debuggable with standard tools.  
  **Not** “the whole CLI fits on one terminal screen” — that was a v0.1 sketch target, **retired** in SPEC-v0.2 (single-file POSIX `aether` remains; size doctrine is honesty, not a LOC myth).

- **Cooperative authority, not a universal sandbox**  
  Preflight refuses when *consulted*. It does not currently force every external agent or shell to comply. See `docs/ALPHA-LIMITATIONS.md` and `NOT-IMPLEMENTED.md`.

## Why These Principles

- Transparency and ownership: you know what the system knows and can change it.  
- Portability: plain files survive tool and model churn.  
- Simplicity: fewer moving parts.  
- Leverage: git, editors, ripgrep work out of the box.

Violations require explicit justification and broad agreement. Hosted alpha labs (e.g. anphuni Session) must not redefine core principles by implication — document them as **separate surfaces** in `PRODUCT.md`.
