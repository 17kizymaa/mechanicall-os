# Mechanicall OS v0.2.0-alpha.1 (draft)

**Do not publish until:** suite green on clean clone, LICENSE present, operator confirms push/tag.

## Summary

Filesystem-native authority and preflight gates for human–AI projects.

One readable authority file (`CURRENT.md`), one permitted next action,
deterministic refusal via `aether preflight`, and an inspectable event log.

## Install

```bash
git clone <repo-url> && cd mechanicall-os
sh scripts/install-aether.sh
export AETHER_HOME="$(pwd)"   # if not already set by install hints
cd /path/to/your/project
aether onboard --yes
aether panel              # daily surface — action buttons (preflight, approve, …)
# optional:
aether app register my-project
aether panel --write      # refresh .aether/PANEL.md + panel.html
```

## Uninstall

```bash
sh scripts/uninstall-aether.sh
aether deinit --yes    # per project; keeps CURRENT.md unless --with-current
```

## Demo

```bash
sh scripts/alpha-demo.sh
```

## Supported environment

- Linux + POSIX sh (primary)
- macOS best-effort; Windows via WSL
- Optional: python3, entr, local Ollama

## Known limitations

See `docs/ALPHA-LIMITATIONS.md`. Notably:

- no sandbox
- no authenticated human identity
- agents must call preflight
- no hosted service
- personal model weights not included

## Agent recipe

`docs/INTEGRATION-AGENTS.md`

## Looking for

- 1 technical alpha user (self-serve)
- up to 3 non-technical users with operator support

## License

Apache License 2.0 — see `LICENSE`.
