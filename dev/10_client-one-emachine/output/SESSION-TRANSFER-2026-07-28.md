# Session transfer package — 2026-07-28

**P0:** Move this chat’s binding decisions onto the client device as files.  
**Where agent lives:** operator host (`myarch`), branch `session/client-one-delroy-reconfigure`, repo `mechanicall-os` source — **not** yet on the eMachine.  
**Client:** eMachine E640 · short-term Alpine USB · overheats · TTY-first.

---

## Shared understanding (locked this session)

| Item | Decision |
|------|----------|
| Authority model | Execute only under `CURRENT.md`; silence ≠ permission |
| Role | Runtime assistant: ops, bootstrap, genuine local research docs |
| Agent location | Stays on operator Arch host for this phase |
| Git | Branch of session changes on source repo |
| Client home user | `Delroy` → `/home/Delroy` (create when INIT unlocks) |
| Project folder | **Deferred** (test-operation session soon) |
| Next auth’d step | **RECONFIGURE** → action id `reconfigure-wlan` |
| Networking | **WLAN → LAN preferred**; USB tethering is **not** preferred steady state |
| Open WLAN issue | `setup-interfaces` accepted Wi‑Fi password but **`wlan0` did not come up** |
| UX floor | TUI/panel from TTY is enough for alpha; GUI later only if needed |
| Disk | Uncertain: failed AndroidOS, archived Win7, Alpine USB — **no wipe**; decision tree only |

---

## What “transfer this chat” means in Mechanicall terms

Chat is not authority. Transfer = copy **inspectable artifacts**:

1. This handoff + sibling docs in `dev/10_client-one-emachine/output/`
2. Stage `CURRENT.md` (operator stage) and `PROPOSED-CLIENT-CURRENT.md` (client draft)
3. After SSH: place under e.g. `/home/Delroy/incoming/mechanicall-session-2026-07-28/` (home may be created at transfer time as a unix user without running product INIT)
4. Later INIT (separate Next): `aether onboard` or `init` + `current init` **inside** the real project path under Delroy

---

## Operator host facts (2026-07-28)

| Fact | Value |
|------|--------|
| Host | `myarch` · Linux 7.1.3-arch1-1 |
| LAN | `enp34s0` · `192.168.1.241/24` · gateway `192.168.1.254` |
| Tailscale | `100.90.85.68` · resolver `100.100.100.100` |
| Repo HEAD (branch base) | `b7dc96d` on `session/client-one-delroy-reconfigure` |
| Known other edge | MacBook Alpine `mbp-edge` / `192.168.1.88` — **not** the eMachine client |
| eMachine on LAN | **Not yet identified** (expected until WLAN works) |

---

## Sequence (graceful)

```text
[now]  Operator: package docs + branch .............. DONE in this folder
[now]  Client console: RECONFIGURE wlan0 ............ see RECONFIGURE-WLAN-ALPINE.md
[gate] Human: confirm IP / sshd
[next] Operator: ssh Delroy@<client-ip> · scp/rsync TRANSFER-MANIFEST
[later] Create unix user Delroy if missing · still no aether project INIT unless CURRENT says so
[later] Test-operation session: project folder + INIT under /home/Delroy
```

---

## SSH transfer (template — run after WLAN + sshd)

On **operator** (adjust IP and user once known):

```bash
CLIENT_IP=192.168.1.XX          # from client: ip -4 addr show wlan0
CLIENT_USER=Delroy              # or root for first push, then chown
DEST=/home/Delroy/incoming/mechanicall-session-2026-07-28

ssh "${CLIENT_USER}@${CLIENT_IP}" "mkdir -p '$DEST'"
rsync -avz --progress \
  /home/anphuni/mechanicall-os/dev/10_client-one-emachine/ \
  "${CLIENT_USER}@${CLIENT_IP}:${DEST}/10_client-one-emachine/"

# Optional thin product surface (no full clone required for TUI demo):
# rsync -avz aether python/aether_panel.py examples/dev-task/ docs/getting-started.md \
#   "${CLIENT_USER}@${CLIENT_IP}:${DEST}/mechanicall-surface/"
```

First-login Alpine often only has `root`. Acceptable path: push as root to `/home/Delroy/...` after:

```sh
# on client (root)
adduser -D -g 'Delroy' Delroy   # Alpine busybox adduser; set password with passwd Delroy
mkdir -p /home/Delroy/incoming
chown -R Delroy:Delroy /home/Delroy
```

---

## Facts / inferences / unknowns

**Facts**

- Operator session authorized Next = reconfigure-wlan.
- USB tether is not the preferred steady state.
- setup-interfaces password step did not result in a live wlan0 association (operator report).
- eMachine overheats; TTY/TUI preferred.

**Inferences**

- Likely missing: interface UP, `wpa_supplicant` running, DHCP client, firmware/module, or rfkill.
- Alpine USB root is ephemeral relative to internal disks — Delroy home on USB alone is short-lived unless a disk is mounted.

**Unknowns**

- Client IP once up; whether `sshd` is installed/enabled.
- Exact Wi‑Fi chipset (Broadcom vs Realtek common on eMachines).
- Which internal partition is safe for a persistent `/home/Delroy`.
- Whether phone tether is currently the only path to the internet on the eMachine for `apk add`.

---

## Explicit non-goals (this transfer)

- Full mechanicall-os clone on the eMachine (optional later).
- GUI / desktop environment.
- Club-cortex, LoRA training, or paid-backend work.
- Disk wipe or dual-boot redesign.
