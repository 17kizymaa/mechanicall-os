# Mechanicall Seat (Tauri)

**status: lab** — incomplete single-app seat experiment · not Mechanicall core · may change  
See `docs/LAB-STATUS.md` · `docs/SINGLE-APP-DISTRIBUTION.md`.

**Desktop** Domain surface — one application window, not a terminal / GOP TUI.

| Layer | Role |
|-------|------|
| **UI** | Vite + TypeScript — conversation + CURRENT + human gates |
| **Shell** | Tauri 2 native window |
| **Truth** | `CURRENT.md` on disk via Rust commands |
| **CLI** | Optional local `aether` for approve / reject / preflight / status |

Negative prompt: **must not feel like a terminal.**

## Prerequisites (Linux)

- Rust (`rustc`, `cargo`)
- Node 18+ / npm
- WebKitGTK (Tauri Linux deps): see [Tauri prerequisites](https://tauri.app/start/prerequisites/)

Arch example:

```bash
sudo pacman -S webkit2gtk-4.1 base-devel curl wget file openssl appmenu-gtk-module libappindicator-gtk3 librsvg
```

## Run (dev)

From repo root or this folder:

```bash
cd seat
npm install

# Point at a Domain project (defaults try ../ CURRENT or ~/mechanicall-os)
export AETHER_HOME="$(cd .. && pwd)"
export MECHANICALL_PROJECT="$(cd .. && pwd)"
# optional: export AETHER_BIN="$AETHER_HOME/aether"

# Linux: avoid blank white WebView (GBM / IPv6 localhost issues)
export WEBKIT_DISABLE_DMABUF_RENDERER=1
export WEBKIT_DISABLE_COMPOSITING_MODE=1
# Vite is bound to 127.0.0.1:1420 (see vite.config.ts + tauri.conf.json)

npm run tauri dev
# or: npm run seat:dev
```

## Product frame

**Mechanicall** = a conversational digital partner for small orgs / charities / freelancers:

- Plan next steps · draft messages · keep AI honest  
- **You** always decide (Yes / Not yet)  
- Grounded in this folder’s `CURRENT.md`  
- Local model: `personal-llm-sft-v4` via Ollama (`OLLAMA_HOST`)

## What works

- [x] Chat-first UI with **Thinking…** presence
- [x] Real **Ollama** chat (sft-v4) + project system prompt
- [x] Product “What can I do?” framework + try starters
- [x] Human **Yes / Not yet** when plan is pending
- [ ] Streamed tokens (next)
- [ ] Kiosk single-app autostart on Kingston

## Env

| Variable | Meaning |
|----------|---------|
| `MECHANICALL_PROJECT` | Domain project root (has `CURRENT.md`) |
| `AETHER_HOME` | mechanicall-os tree (contains `aether`) |
| `AETHER_BIN` | Explicit path to `aether` executable |

## Build release

```bash
npm run tauri build
```

Artifacts under `src-tauri/target/release/` (and bundle dirs per OS).

## Doctrine

- Silence is never permission.
- Models never call approve/reject.
- Filesystem is sole durable truth.
