# Transfer manifest — after SSH

Copy from operator host → client. Paths are relative to `mechanicall-os` repo root unless absolute.

## Priority 0 — session binding (required)

| Source | Destination (suggested) |
|--------|-------------------------|
| `dev/10_client-one-emachine/` (entire tree) | `/home/Delroy/incoming/mechanicall-session-2026-07-28/10_client-one-emachine/` |

## Priority 1 — thin product surface for TTY demo (optional, small)

| Source | Destination |
|--------|-------------|
| `aether` | `…/mechanicall-surface/aether` |
| `python/aether_panel.py` | `…/mechanicall-surface/python/aether_panel.py` |
| `examples/dev-task/` | `…/mechanicall-surface/examples/dev-task/` |
| `docs/getting-started.md` | `…/mechanicall-surface/docs/getting-started.md` |
| `docs/ALPHA-LIMITATIONS.md` | `…/mechanicall-surface/docs/ALPHA-LIMITATIONS.md` |
| `SPEC-v0.2.md` | `…/mechanicall-surface/SPEC-v0.2.md` |
| `CORE_PRINCIPLES.md` | `…/mechanicall-surface/CORE_PRINCIPLES.md` |

On client after copy:

```sh
chmod +x aether
export AETHER_HOME="$PWD"    # if using surface dir as faux home
# or: place aether on PATH and set AETHER_HOME to mechanicall-os checkout
```

Full repo clone is **not** required for first TUI proof.

## Priority 2 — do not transfer by default

- `mechanicall-portable-vm.qcow2`
- `result`, `result-vm` nix store links
- `.planning/` bulk unless requested
- secrets (`.env`, credential files, private keys)
- operator-only Kingston rebuild scripts (unless stick work resumes)

## Verification on client

```sh
find /home/Delroy/incoming/mechanicall-session-2026-07-28 -type f | head -50
cat …/10_client-one-emachine/CURRENT.md
cat …/10_client-one-emachine/output/SESSION-TRANSFER-2026-07-28.md
```

## Deferred INIT (not in this rsync alone)

When later authorized:

```sh
# as Delroy, in chosen project directory under /home/Delroy
aether onboard
# or: aether init && aether current init
# then replace CURRENT with edited PROPOSED-CLIENT-CURRENT.md content
```
