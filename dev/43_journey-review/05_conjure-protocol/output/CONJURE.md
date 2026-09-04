# Conjure the desk — draft protocol (not CURRENT, not Yes)

**When:** 2026-08-24  
**Not law until a later CURRENT propose.** Live Next stays `sit-distro-gate`.  
**Locked this grill:** W7=1 Funnel stays Reject; working hours fully asleep until conjured. **W9=1 recant E3b later** (k3s off myarch; later CURRENT, not this Next). **W10=1 S3. W11=1 HOLD then S3 unless local session (N=15 min, skip-obvious). W12=2 connected sitter may WAKE.**  
**Existing law this draft must not fight:** S4 WAKE via wol-pi (magic packet, tailnet-only); GATE-CONTRACT LOAD then STREAM; JOIN/WAKE are not Decide; no public `/wake`.

The verb on the face is still **WAKE**. **Conjure** is the whole sequence from S3 to tokens and back to S3.

---

## What you are conjuring (one picture)

```
ASLEEP          myarch S3 (suspend-to-RAM); NIC listens for WoL
   │
   │  JOIN=connected  AND  WAKE tap (sitter tag:stranger or operator)
   │  wol-pi POST  →  magic packet to myarch MAC
   │  Not Yes. Not Funnel. Not 0.0.0.0. Send does not imply WAKE.
   ▼
CONJURE         NIC + S3 resume. Face: sleeping → waking
   │  timeout ~90s until GET myarch:11434/api/tags == 200
   ▼
IDLE            kernel up, Ollama answers tags; 7B may not be in VRAM
   │  LOAD (amber)  —  weights
   ▼
STREAM          tokens (purple)  —  one niced generate
   │  quiet
   ▼
HOLD            15 min keep_alive unless a local session is active
   │
   ▼
ASLEEP          S3 again — working hours included
```

Funnel never appears. If Funnel or public bind is up, that is an **incident**, not a mode. Shutdown logic = this default (ASLEEP) + refuse public.

---

## Roles (who is allowed to be always-on)

| Box | Job | Always-on? |
|-----|-----|------------|
| **wol-pi** | Doorbell. Tailnet HTTP. Sends magic packet. Never holds CURRENT. Never Ollama. | **Yes** |
| **myarch** | 7B `personal-llm-sft-v4`, Kingston tree, STORM when you review | **No** — fully asleep in working hours until conjured |
| **phone sit** | JOIN / WAKE / LOAD / STREAM / Decide | Sitter’s radio; not a server |
| **Funnel / 0.0.0.0** | — | **Never** |

Kingston stick: **S3 keeps the mount** (frozen in RAM). Poweroff would unmount; that is not this protocol.

E3b (k3s on myarch): **W9=1 recant later** — cluster off myarch so S3 is a clean workbench. Not this Next; needs a future CURRENT propose. Until that apply, do not implement k3s-off or S3 from this file. STORM remains factory and must not inhibit S3 when you do implement (never A33).

---

## Sequence (normative *if* this draft becomes a later CURRENT)

### 0. Default: ASLEEP

Working hours included. QUIET on the sit is the honest face of ASLEEP (GATE-CONTRACT already: quiet = no desk).

**Locked W10=1:** suspend-to-RAM (S3). NIC in WoL. Magic packet (S4). Almost everything frozen, including 7B VRAM and any k3s/STORM that was running. Not poweroff. Not display-off. Not “kernel up, daemons stopped.”

### 1. Permission to conjure (not Yes)

Already locked: WAKE enabled when **JOIN=connected** (S4). Invite/Wake/Send are not Decide.

**Locked W12=2:** a connected sitter (`tag:stranger`) **may WAKE**. Operator strip may WAKE. **Send does not imply WAKE** (still a separate tap; not Decide).

### 2. CONJURE (wol-pi)

```
POST http://wol-pi:7077/wake     # tailnet only; WOL_WAKE_URL
body: {}                         # no CURRENT, no prompt
wol-pi → etherwake <myarch MAC>  # MAC off git, off APK
```

Refuse: public URL, `0.0.0.0`, Funnel. `wake_desk` already refuses those.

Face: sleeping → waking. GATE stays quiet until tags 200. Timeout **90s** (GATE-CONTRACT). On fire: strip stays sleeping; not Yes; no retry storm.

Honest gap (S4 post-select): wol-pi HTTP **may still be thin**. Chrome without the packet is decoration. This draft does not pretend the service is certified.

### 3. IDLE → LOAD → STREAM → quiet

Unchanged from GATE-CONTRACT. One generate. Queue extras. Never write CURRENT from the queue. LOAD timeout 60s; first token 30s; then quiet + note.

### 4. Back to ASLEEP (the missing half)

GATE-CONTRACT ends at quiet. **Fully asleep in working hours** needs a return path:

```
quiet  →  HOLD (15 min keep_alive)  →  S3
```

**Locked W11=1:** 15 minutes after last token (skip-obvious N; override if you say so), **unless** a local graphical or ssh session is active. Working hours are not a keep-alive. Not Yes.

---

## What this protocol is not

- Funnel with a shutdown switch  
- Public `/wake`  
- Always-on 7B for a “good SLA”  
- k3s-as-Mechanicall-core (Reject) staying up while you claim ASLEEP  
- WAKE as Decide  
- Auto-publish CURRENT when the desk comes up  

---

## Checkpoint

Holes filled (W9–W12). Spec is **frozen pending human confirm** that this shared understanding is closed. Then it is still **not** live law until a later CURRENT propose. Do not implement WoL/S3/k3s-move from this file. Do not apply to CURRENT this sitting. Live Next remains `sit-distro-gate`.
