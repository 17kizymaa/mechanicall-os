# Core Principles (Locked In)

These principles define awareness-agent and Mechanicall OS v0. They are non-negotiable.

## Locked Principles

- **Filesystem is the single source of truth**  
  No hidden databases. All state, context, memory, and configuration live in the filesystem as plain files. Everything is directly readable, editable, grep-able, and version-controllable with git.

- **Markdown + Python as the only "userland"**  
  User-facing and extension content is either:
  - Markdown (`.md`) for docs, context, memory, interfaces, and knowledge.
  - Python (`.py`) for all logic, agents, scripts, and automation.
  No other languages, heavy frameworks, or opaque formats in the user layer.

- **Active context sidecars**  
  Small, observable files and scripts (e.g. `.context.md`, `.awareness.json`, `.memory/`) live at the OS/workspace level alongside normal project files.
  These sidecars carry active state and are managed by scripts. They are first-class citizens in the filesystem.

- **Extremely low overhead and high inspectability**  
  The system must be:
  - Lightweight (minimal CPU/RAM, no unnecessary daemons or deps).
  - Fully inspectable (you can `cat`, `ls`, `grep`, `tail`, `diff` everything that matters).
  - Debuggable with standard tools.

## Why These Principles

- Transparency and ownership: you always know exactly what the system knows and can change it directly.
- Portability and durability: plain files survive tool changes, LLM changes, and platform migrations.
- Simplicity and reliability: fewer moving parts means fewer surprises.
- Leverage existing tools: git, editors, ripgrep, find, etc. work out of the box.

Violations of these principles require explicit justification and broad agreement.
trigger line
