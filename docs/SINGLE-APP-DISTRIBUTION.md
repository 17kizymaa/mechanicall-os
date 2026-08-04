# Single-app distribution (product shape)

**Status:** CONTRACT · UX incomplete · CLI is not the product  
**Date:** 2026-08-03  
**Audience:** operator, packagers, future casual users  

---

## Verdict (locked)

| Claim | Truth |
|-------|--------|
| Casual users will run `aether` / edit files in a terminal | **Failed product bet** |
| Product is a **custom distribution** | **Yes** |
| That distro opens **exactly one application** | **Yes — the seat UX** |
| That UX is finished | **No — incomplete** |
| CLI / CURRENT / preflight | **Backend + power tools**, not the front door |
| License of artifacts built from this repo | **Apache-2.0** (`LICENSE`) unless a package NOTICE says otherwise |

Third parties redistributing a seat image or app built from this tree must keep Apache-2.0 notices. Hosted Session on anphuni.com is a separate *service* surface (see PRODUCT.md License).
Nobody in their right mind *has* to use a CLI to “do files” for day-to-day Mechanicall.  
Filesystem remains **truth**; the **UX** is how humans and the agent meet that truth.

---

## What the user boots into

```text
[ Power on custom image / stick ]
        │
        ▼
[ Firmware → bootloader → kernel ]     (no desktop choice)
        │
        ▼
[ Autologin operator ]                 (single-user appliance)
        │
        ▼
[ compositor or TTY kiosk session ]
        │
        ▼
[ ONE app: Mechanicall Seat UX ]       ← incomplete, but only surface
        │
        └── if UX exits → session restarts UX (no bash playground)
```

**Not in the casual path:** seat-menu with 7 options, host shell, ollama CLI, `aether try`, multi-window DE.

Power operators may still use CLI when they deliberately escape (`MECHANICALL_SEAT_SKIP` / debug boot) — that is **service mode**, not product mode.

---

## The one application (incomplete)

| Role | Today | Honest label |
|------|--------|--------------|
| Seat UX | `aether panel` / `aether_panel_tui` (curses) | **Incomplete product UI** |
| Domain law | `CURRENT.md` always visible or one action away | Required |
| Human gates | Approve / Reject | Required |
| Agent chat | Domain chat bound to CURRENT | Incomplete fidelity |
| File browser / IDE | Out of scope for v0 appliance | Not the app |

**Incomplete means:** ship the distro contract and kiosk session **now**; iterate UX **inside** that single app. Do not invent a second front door (CLI pack, Electron “wizard”, multi-app menu).

### Non-goals for the one app

- Full desktop (files, browser, settings as peer apps)
- Multi-tenant SaaS web UI
- Forcing casual users through `onboard` / `preflight` ceremony in a raw shell
- Replacing Grok Build binary as the distro’s only chat (optional backend, not the shell)

---

## Distro targets

| Target | Role | Status |
|--------|------|--------|
| **Kingston NixOS** (`portable-kingston`) | Primary appliance stick | Host exists; **kiosk single-app not default yet** |
| **seat-kiosk module** | `greetd`/`getty` + session → only UX | **Scaffold in tree** (`nix/modules/seat-kiosk.nix`) |
| aetherOS / archiso | Separate calm workstation ISO | Different product lineage — do not merge casually |
| MBP Alpine cage dual-page | Lab | Parked unstable — not casual distribution |

Enable on Kingston when ready:

```nix
mechanicall.seat-kiosk.enable = true;
# implies: no multi-app menu; UX only; autologin
```

---

## Backend still real (invisible to casual)

The UX must still call / bind:

- `CURRENT.md` authority  
- preflight / approve / reject / events (human or agent under contract)  
- optional local PEER model  

Casual user **sees** chat + plan + approve.  
They do **not** need to know `aether preflight` exists until Advanced / service mode.

---

## Success test (casual)

1. Boot stick/image.  
2. No “which app?” menu.  
3. Only the seat UX is interactive.  
4. User can see CURRENT, talk, approve/reject without opening a shell.  
5. Closing the UX does not dump them into a free desktop — session returns to UX or clean reboot.

If step 2–3 fail, distribution failed even if CLI is perfect.

---

## Relation to earlier mistakes

| Bet | Outcome |
|-----|---------|
| `scripts/try.sh` / CLI first project | Useful for **devs**; **not** casual product |
| seat-menu (7 choices) | Operator foundation; **too many apps** for appliance |
| PEER middleman on desktop Grok | Side path; not the distro UX |
| Dual-page MBP thrash | Parked; chrome ≠ product |

---

## Next engineering (ordered)

1. **Default Kingston (or ISO) to seat-kiosk** — one session, one binary.  
2. **UX completeness** inside that binary only (CURRENT always on, approve, chat, no quit-to-bash).  
3. **Casual UAT** on real hardware with someone who will not open a terminal.  
4. Package/install story = “flash stick / boot ISO”, not “clone and symlink”.

CLI remains for CI, agents, and you in service mode.
