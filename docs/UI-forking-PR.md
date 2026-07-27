# UI Logic — mechanicallOS v0.2 pre-distribution patch

The interface should be **user-inspired**. For non-developer usage with operator
support, the intended flow is:

1. User follows README.md for installation  
2. User installs software (`scripts/install-aether.sh` or symlink)  
3. User reads preflight / alpha limitations (or is walked through them)  
4. User registers their **development application** with aether  
5. User uses basic aether commands to customise authority and project files  
6. User can inspect a project-local command cheatsheet and agent recipe  

## Shipped in alpha (within reason)

| Step | Mechanism |
|------|-----------|
| Install | `scripts/install-aether.sh` / `uninstall-aether.sh` |
| First-run literacy | `aether onboard [--yes]` |
| Development application | `aether app register <name>` → `.aether/app.json` + critique-oriented CURRENT when missing |
| Command literacy | `.aether/COMMANDS.md` cheatsheet; [INTEGRATION-AGENTS.md](./INTEGRATION-AGENTS.md) |
| Action buttons | `aether panel` — Project Panel TUI (select Preflight / Approve / …) |
| File projections | `aether panel --write` → `.aether/PANEL.md` + `panel.html` (scaffold for later GUI) |
| Propose exemplar | [examples/propose-current/](../examples/propose-current/) (human applies; models never approve) |

**Do not brand first-run as a “shell wizard.”** Day-to-day operation uses the
**Project Panel** so actions are buttons, not memorized ritual.
A more user-inspired surface may later grow from the personal-llm propose layer
([PERSONAL-LLM-LAYER.md](./PERSONAL-LLM-LAYER.md)); that is a developmental
direction to re-evaluate with real users, not a v0.2 product claim.

## Development application focus

The registered app is oriented toward **critiquing the codebase for the user’s
usage**, with aether docs and (when available) an agent-based IDE following the
preflight contract.

## Alpha cohort

- 1 technical self-serve user  
- Up to 3 non-technical users with operator support (local clients)  

## Explicit non-goals here

- Product web dashboard  
- Club-cortex accounts  
- Multi-tenant fork hosting  
- Shipping personal model weights  

See [ALPHA-LIMITATIONS.md](./ALPHA-LIMITATIONS.md) and
[DISTRIBUTE-MECHANICALL-ALPHA.md](./DISTRIBUTE-MECHANICALL-ALPHA.md).
