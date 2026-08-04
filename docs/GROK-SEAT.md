# Grok Build seat + Mechanicall protocol

**Status:** observability contract · not enforcement  
**Audience:** operator who lives in Grok Build TUI  

## Truth

The protocol **observes** Grok Build; it does **not** gate it.

- Grok (and any external TUI) can edit files without calling `aether preflight`.  
- Authority still lives in `CURRENT.md`; it only binds when something consults it.  
- The **human** is the gate. Drift is a **report**, not a lockout.

## Paste at SessionStart

```bash
cd /path/to/mechanicall-os   # or your Domain project
./aether brief
# optional:
./aether drift; echo "drift_exit=$?"
```

`brief` always exits 0. `drift` exits 1 if git sees dirty paths.

## After approve

Do **not** hand-edit `**Next:**`. Use:

```bash
aether next <new-action-id>
```

## Grok hooks (installed)

### Project (this repo)

| File | Event |
|------|--------|
| `.grok/hooks/aether-session-start.json` | SessionStart → `aether brief` (stderr + `.aether/last-grok-brief.txt`) |
| `.grok/hooks/aether-prompt-context.json` | UserPromptSubmit → inject brief as `additionalContext` |
| `.grok/hooks/session-start.json` | ICM meta-agent reminder (legacy) |

**Trust once:** open the project in Grok and run `/hooks-trust` (or `grok --trust`).  
Project hooks are **skipped** until trusted.

### Global (this machine)

`~/.grok/hooks/aether-mechanicall-session.json` — SessionStart + UserPromptSubmit when `CURRENT.md` is in cwd or under `AETHER_HOME` (default Kingston mechanicall-os path). Always trusted (user global).

### Script

`scripts/grok-aether-brief.sh` — non-blocking; never denies tools; never edits CURRENT.

### Disable

- Remove or rename the JSON files under `.grok/hooks/` / `~/.grok/hooks/`.  
- Or set env in the hook command to no-op (edit JSON).  
Never use PreToolUse deny for “force preflight” in the Grok seat — that fights the primary TUI.

## Related

- `.grok/hooks/README.md`  
- `docs/PROTOCOL-TEST-SURFACE.md`  
- `docs/PROTOCOL-LAB.md`  
- `NOT-IMPLEMENTED.md` (sovereign TUI gap)  
