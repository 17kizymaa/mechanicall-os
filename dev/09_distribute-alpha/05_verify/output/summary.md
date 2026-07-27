# Stage 05 — Verify

## Local suite

```
sh tests/run.sh
```

Result (this session): **All aether integration tests passed**, including:

- personal-llm unit tests
- v0.2 authority refuse/allow/approve/reject
- onboard --yes
- app register + status
- deinit
- alpha-demo.sh

## Checklist before public tag

- [x] LICENSE Apache-2.0
- [x] Honest README claims
- [x] ALPHA-LIMITATIONS.md
- [x] INTEGRATION-AGENTS.md
- [x] CI workflow file
- [x] install/uninstall scripts
- [x] onboard / app register / deinit
- [x] alpha demo
- [x] Project Panel TUI (`aether panel`) + PANEL.md/html projections
- [x] Onboard lands on panel as next step; cheatsheet prefers panel
- [ ] Operator: commit selection / PR / merge
- [ ] Operator: tag `v0.2.0-alpha.1` + GitHub Release
- [ ] Operator: invite 1 technical + 3 supported non-technical users

## Human-gated

Push, merge, tag, and invitations require explicit operator confirmation.

## Suggested tester script (post-install)

```bash
aether onboard --yes
aether panel          # p = preflight next, d = demo refuse, a = approve
```
