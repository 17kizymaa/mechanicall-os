# Ambient requests vs child CURRENT — research, not a recant

**When:** 2026-08-24  
**Not law. Not Yes. Not Funnel. Not dual-Next.**  
**Live Next stays `sit-distro-gate`.** W2=3 (stop four-door build). This file answers the *workflow* follow-up: shutdown/ambient logic, and session child `CURRENT.md` as a way to run multiple Nexts.

Sister: `../03_workflow-process/output/PROCESS.md`.

---

## 1. What “Funnel” is in this tree (so shutdown has an object)

**Funnel** here is **public expose**: Tailscale Funnel / `0.0.0.0` bind / public Ollama / public wake URL. Not “a request arrived.”

Already refused in code and law:

- CURRENT Reject: Funnel / public Ollama / public wake  
- `wake_desk`: POST `http://wol-pi:7077/wake` (or `WOL_WAKE_URL`); `_refuse_public_ollama`; refuse `0.0.0.0`  
- Desk generate: private hosts only (MagicDNS `myarch`, USB, LAN, tailnet `100.x`)  
- `android/tsnet/README.md`: no Funnel, no VpnService  
- SHARING: twin GET-only on `127.0.0.1:7078` until JNI; GET is not Yes  

**Shutdown Funnel logic that must stay present** is therefore:

1. **Never start Funnel.** No public Serve as product.  
2. **Refuse public bind** if something tries (`_refuse_public_ollama`, wake URL check).  
3. **Treat “online” as a lie** while drop is down or zip uncontained (live CURRENT Reject).  
4. **Desk may be off.** QUIET is a legal state, not a bug.

That is the shutdown logic. It is a **refuse-path**, not a Cloudflare feature you toggle.

---

## 2. Ambient self-hosted requests (already specified)

You do **not** need Funnel for “someone asked my house for a draft.” GATE-CONTRACT already sequences it:

```
WAKE (strip, not Yes)  →  POST wol-pi  →  myarch powers / answers /api/tags
LOAD                   →  weights into VRAM (amber)
STREAM                 →  tokens (purple)
QUIET                  →  desk may sleep again
```

| Piece | Role | Always-on? |
|-------|------|------------|
| **wol-pi** | Doorbell (WOL / wake HTTP on **tailnet**) | Yes — weak, cheap, not the 7B |
| **myarch** | 7B + (E3b) k3s + STORM host | **Should sleep** for ambient; E3b put k3s **on** myarch (conflict) |
| **JOIN** | Sitter on Headscale/tsnet as themselves | Not Yes; not public |
| **WAKE** | Human/strip tap or later an invited sitter’s tap | Not Yes |
| **GATE** | LOAD vs STREAM vs QUIET | Instrument only |
| **Decide** | Two-tap + Why on **their** folder | The only Yes |

**Necessary logic** (contract, not this Next’s implement):

1. **Doorbell ≠ desk.** Something small and on (wol-pi or a spare) accepts a tailnet POST. myarch is allowed to be dark.  
2. **ACL.** Only JOIN=connected (or lab USB/LAN) may WAKE. Invite paste is not a public URL.  
3. **Probe then load then stream.** `/api/tags` then LOAD timeout then STREAM. Timeouts → QUIET + note, not Yes.  
4. **One generate.** Queue extra Sends. Never a second Ollama to feel faster. Never write CURRENT from the queue.  
5. **Quiet is success.** After STREAM, desk may power off. No Funnel keep-alive.  
6. **Shutdown Funnel = default.** If Funnel or `0.0.0.0` is up, that is an incident, not a mode.  
7. **Request is not Yes.** WAKE / LOAD / STREAM / twin GET / inbox offer never actualise CURRENT.

What is **not** necessary (and is Reject): public Funnel so “anyone in the world” can hit myarch without JOIN; always-on 7B; k3s-as-Mechanicall-core.

**Conflict already on disk:** E3b selected **k3s on myarch**. That fights “home desktop shouldn’t be always-on.” Ambient as specified wants wol-pi (or a $5–20 always-on doorbell) and a **sleeping** workbench. That recant is a **later** CURRENT if you want it — not this sitting (W2=3).

---

## 3. Child CURRENT.md does not unlock multiple operator Nexts

### What already exists (legal multiples)

| Mechanism | What it is | One Next? |
|-----------|------------|-----------|
| `aether … [path]` | Each **folder** has its own `CURRENT.md`. SPEC-v0.2. | **One Next per folder.** |
| Phone bind ≠ this repo | Sitter law is **their** folder (D3=4; B10). | Their Next ≠ `sit-distro-gate`. |
| ICM `dev/NN/MM_stage/` | Sequenced work **inside** the live action-id. Halt at `output/`. | Same operator Next. |
| `aether brief` / stage CONTEXT.md | Session contract for an agent. **Not** authority. | No second Approve. |
| STORM cap 2 | Parallel **review**. Never Confirm. Never `aether approve`. | Same Next; look, don’t Yes. |
| Isolated git worktree | Another checkout. Still must not approve root law. | Factory, not a second live Next. |

Root Keep (historical, still right): **no child Domain as operator session authority.** Pocket bind is a different folder, not a sub-CURRENT on this tree (`PROPOSE-mobile-planning-demo.md`).

### What “session-based child CURRENT for subagents” would actually do

If a subagent gets a file **named** `CURRENT.md` with **Next:** and can `preflight` / (worse) `approve`:

- You now have **two clocks** (M5) by design.  
- Models never approve — unless the child file teaches them they are the human.  
- `aether next` on the child does not advance root `sit-distro-gate`. Operators will treat whichever file is in the prompt as law (HUMAN_ESCALATE hole).  
- That **is** dual-concurrent-next with extra folders. CURRENT Rejects it.

If the session file is named **`CONTEXT.md` / `BRIEF.md` / `PROPOSE-….md`**:

- That is ICM. You already do it.  
- Subagents execute **tasks** under the **one** live Next. They write `output/`. They do not Yes.  
- Parallel is allowed for **reads** and isolated drafts. Not for two APPROVED action-ids on this repo.

### “Execute multiple nexts”

| Want | Legal form | Illegal form |
|------|------------|--------------|
| Many steps this sitting | Numbered stages inside `sit-distro-gate` (`dev/42/01`…`06`) | Four APPROVED Next ids |
| Subagent help | CONTEXT.md + `output/` + never approve | Child CURRENT the model treats as law |
| Someone else plans | Bind **their** folder (`aether current /path`) | Child CURRENT under `mechanicall-os/` |
| Review in parallel | STORM / read-only spawn; cap 2 | Swarm that taps Confirm |

You **cannot** research-your-way into dual-Next without a human CURRENT recant. W2=3 declined that recant for the four-door bundle. Child CURRENT as a trick to do the bundle anyway is M1 (wishlist stacking) wearing a folder.

---

## 4. How implementation workflow should move (discussion)

Stay on **one** operator Next. Use children that are **not** CURRENT:

```
CURRENT.md                 ← one Next (human)
  .aether/proposals/       ← propose only
  dev/NN/CONTEXT.md        ← factory routing
  dev/NN/MM_stage/CONTEXT  ← this agent’s contract
  dev/NN/MM_stage/output/  ← halt
  ~/their-folder/CURRENT   ← their law, if they sit
```

Subagent prompt: read the stage CONTEXT, write output, **do not** `aether approve`, **do not** invent a Next. If isolation=worktree, still no child CURRENT unless that worktree **is a different project** the human owns.

Ambient path (later Next, after distro-gate): implement/verify GATE-CONTRACT + wake refuse-public; **do not** enable Funnel; **do** keep QUIET as the default desk.

---

## Checkpoint

This file does not start Funnel, k3s recant, child CURRENT, LTE, or Play.  
Grill **W7** (what “Funnel shutdown / ambient” means) and **W8** (child CURRENT vs dual-Next) in `decision-tree.md`.
