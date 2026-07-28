# Thermal + TUI notes — eMachine E640

## Hardware posture

eMachine E640-class machines are mid/late-2000s, often thermally marginal under:

- browser + electron
- full desktop compositors
- large `apk upgrade` / compile jobs
- multiple parallel SSH + package fetches

## Alpha floor: TTY is enough

Mechanicall v0.2 daily surface:

```sh
# from a directory with CURRENT.md (example template first):
aether panel
# or simple mode if curses is painful:
aether panel --simple
```

Panel is a **projection** over files (`CURRENT.md`, events). It is not a second control plane.  
No GUI install is required to demonstrate: authority → refuse → allow → artifact → approve.

## Practical thermal hygiene

1. Firmware fans: elevate chassis; hard surface only.
2. Stay on text VT (`Ctrl+Alt+F1`…); skip Xorg/Wayland until needed.
3. Cap work: WLAN fix + rsync + panel demo, then idle.
4. Prefer `apk add` of named packages over full upgrade during first session.
5. If throttling: pause; do not force GUI “to make it easier”.

## When GUI might be justified later

- Non-technical local client cannot use TTY even with operator beside them
- Need browser-only workflow (still second choice to Panel.md / files in Obsidian-style vault)

Not justified merely for operator comfort if SSH from `myarch` works.
