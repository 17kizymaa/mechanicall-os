# CI — control-layer gates (local-first)

**Domain Next:** `ci-control-layer-gates`  
**Scope:** Prove **panel + shell + CURRENT/preflight** seats.  
**Not in scope:** Slack/Matrix, Gitea, K8s, REST authority APIs, WebSocket product, cloud EDA.

---

## What is gated

| Check | How |
|-------|-----|
| Unit tests (shell, agent, panel, llm) | `pytest` (or subset without pytest) |
| Desk product gone | `aether desk` / `desk-serve` must fail with redirect |
| Shell offline smoke | `aether shell . --smoke` / `python3 python/aether_shell.py --smoke` |
| Panel projection | `aether panel --dump` shows **Next** |
| Preflight | allow Next · refuse Prohibited |
| Artifacts present | peer/grok agent profiles, `aether_panel_tui.py` |
| Secret hygiene | best-effort scan of product paths (no raw `ghp_` / `sk-or-` in tree) |

Full integration (sidecars, onboard, authority) remains: `sh tests/run.sh` (ends by calling control-layer gates).

---

## Local setup (no SaaS required)

```bash
cd /path/to/mechanicall-os
export AETHER_HOME="$PWD"
export PATH="$PWD:$PATH"

# Recommended for full unit coverage
python3 -m pip install --user pytest   # or use your nix/dev shell

# Control-layer gates only
sh scripts/ci-control-layer-gates.sh

# Full integration suite (includes gates at end)
sh tests/run.sh
```

### Seats (manual dogfood — not CI)

```bash
aether panel .     # real TTY fullscreen TUI
aether shell .     # peer default (personal-llm when Ollama up)
```

Optional LAN personal-llm: see `docs/PERSONAL-LLM-PEER-REPL.md`.  
Tailscale is **optional** for reaching Ollama on another host — **not** a CI dependency.

---

## GitHub Actions (optional remote runner)

Workflow: `.github/workflows/test.yml`

| Job | Command |
|-----|---------|
| `aether-integration` | `sh tests/run.sh` |
| `control-layer-gates` | `sh scripts/ci-control-layer-gates.sh` |

CI runners are **not** product infrastructure. The source of truth for “gates green” on a developer machine is the local scripts above.

---

## What we deliberately do **not** run in this CI

- Slack / Matrix / Misskey  
- Self-hosted forge (Gitea/GitLab CE) as product  
- Tornado/REST CRUD over CURRENT  
- Kubernetes / GitOps / cloud control plane  
- Replacing filesystem events with a message bus  

Those are rejected as control-layer scope. See `NOT-IMPLEMENTED.md`, `docs/DESK-REMOVED.md`, `docs/PANEL-GROK-SPLIT.md`.

---

## Approve when green

```bash
sh scripts/ci-control-layer-gates.sh   # must print ALL PASSED
# optional: sh tests/run.sh

aether approve "ci-control-layer-gates"
```

There is **no** `aether verify` subcommand — the gate script **is** the verify.

---

## Related

- `scripts/ci-control-layer-gates.sh`  
- `docs/AETHER-SHELL.md` · `docs/PANEL-GROK-SPLIT.md` · `docs/PERSONAL-LLM-PEER-REPL.md`  
- PR product branch: `feat/domain-shell-panel-tui`  
