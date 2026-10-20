# V6 grill — not CURRENT, not Yes

**Model:** `personal-llm-sft-v6:latest`
**Host:** `http://127.0.0.1:11434`
**When:** 2026-10-16T17:21:34Z
**Prompt tokens / eval:** 334 / 3762

This file is the model's draft. It is not a framework until FRAMEWORK.md. It does not approve.

## Model prose

Go!

# DRAFT_DESK_MODEL — personal-llm-sft-v6:latest
**Host tag:** `personal-llm-sft-v6:latest`  
**Weight policy:** weights stay outside the APK and outside git (never inside).  
**Rule of thumb:** a model may propose; it never approves. Silence is never permission.

---

## 1. What the local model is allowed to write
The local model may only create or update these files:
- `PROPOSE-CURRENT.md` — one-time pinned proposal (never approved).  
- `aether/02-BOOKMARKS` — aether-only snapshot of CURRENT bytes (parked; not approve).  
- `aether/03-VERBS` — verb list for aether (parked; not approve).  
- `aether/04-CURRENT.md` — current state record (parked; not approve).  

**Never:**
- Write `CURRENT.md`, `preflight.md`, `apply.md`, or `approve.md`.  
- Run `aether run` directly.  
- Approve any proposal.  
- Unlock anything.

---

## 2. What it must never write or run
The local model must not:
- Write `CURRENT.md`, `preflight.md`, `apply.md`, or `approve.md`.  
- Create, modify, or delete `CURRENT.lock`, `aether/01-PIN.md`, `aether/05-STATUS.md`, `aether/06-RECORD.md`.  
- Run `aether run` (parked; operator runs it).  
- Approve any proposal.  
- Unlock anything.  
- Claim current permission.  
- Name a password, key, token, or root command.

---

## 3. How a call is pinned (tag, host, SYSTEM)
A call is pinned by:
- **Tag:** `DRAFT_DESK_MODEL` (already set to `personal-llm-sft-v6:latest`).  
- **Host tag:** `personal-llm-sft-v6:latest`.  
- **SYSTEM:** the model may propose under SYSTEM, but it must not approve.

---

## 4. How propose files sit next to CURRENT, preflight, apply, approve
`PROPOSE-CURRENT.md` sits beside `CURRENT.md`, `preflight.md`, `apply.md`, and `approve.md`.  
- It is **never** approved by the model.  
- Approval requires a separate operator action (not this framework).

---

## 5. Doctor's Note (stuck-gate record; not Yes; not the grant)
`aether/01-PIN.md` records:
- Stuck gate status (`STUCK`, `RESOLVED`).  
- Reason, next step, and whether a **Yes** was issued.  
- This file is **not** the grant.

---

## 6. Bookmark (snapshot of CURRENT bytes; parked; not Yes; not apply)
`aether/02-BOOKMARKS` holds:
- `CURRENT.md` snapshot (`CURRENT_BYTES`).  
- `preflight.md`, `apply.md`, `approve.md` snapshots (`PREFLIGHT_BYTES`, `APPLY_BYTES`, `APPROVE_BYTES`).  
- Timestamps and hashes.  
- This is **parked**; it is not a Yes, not apply, not approve.

---

## 7. aether run (parked; ollama-shaped type-then-approve-or-reject)
`aether/03-VERBS` lists allowed verbs:
- `type`, `list`, `status`, `help`.  
- **Not:** `run`.  
- `aether run` is parked; the operator runs it.

---

## 8. When rented GPU is the hardcore path (operator Yes; not this halt)
Rented GPU is a separate, operator-controlled path:
- Requires explicit operator **Yes**.  
- Not covered by this local-model framework.  
- Never claim permission here.

---

## 9. Failure modes
If any of these fail, record them in `aether/06-RECORD.md`:
- `DRAFT_DESK_MODEL` not set to `personal-llm-sft-v6:latest`.  
- Host tag mismatch (`personal-llm-sft-v6:latest`).  
- Weight outside APK and outside git.  
- Model attempts to approve or unlock.  
- `PROPOSE-CURRENT.md` created without operator approval.  
- `aether run` called directly (parked).

---

## 10. A short standard call recipe
```bash
# Set the pinned tag
export DRAFT_DESK_MODEL=personal-llm-sft-v6:latest

# Start a host call (writes PROPOSE-CURRENT.md only)
ollama chat personal-llm-sft-v6:latest \
  --system "You are a local-model assistant. You may propose but never approve."

# Later, operator approves (not the model)
aether approve

# Snapshot CURRENT bytes for bookmarking
aether snapshot current

# Run on rented GPU only after operator Yes
aether run --gpu-yes
```

---

## Self-grill: holes, stale pins, and what could become a Yes by accident
**Holes:**
1. No explicit `REVIEW` gate between propose and approve.  
2. No explicit `AUDIT` gate for weight integrity.  
3. No explicit `REPLAY` gate to prevent replay attacks.  
4. No explicit `LOCK` gate when the operator is absent.

**Stale pins:**
1. `DRAFT_DESK_MODEL` must not be changed without a new review.  
2. Host tag must never drift from `personal-llm-sft-v6:latest`.  
3. Weight path must remain outside APK and git.  
4. `aether run` must stay parked until operator Yes.

**What could become a Yes by accident:**
1. The model claims current permission (never allowed).  
2. Silence is mistaken for approval (silence is never permission).  
3. A propose file is renamed to approve.md without audit.  
4. `aether run` is called directly instead of after operator Yes.

**Next safe step:**
- Operator reviews the proposal, then approves with a separate command.  
- Never claim current permission.  
- Silence is never permission.

Go!

# DRAFT_DESK_MODEL — personal-llm-sft-v6:latest
**Host tag:** `personal-llm-sft-v6:latest`  
**Weight policy:** weights stay outside the APK and outside git (never inside).  
**Rule of thumb:** a model may propose; it never approves. Silence is never permission.

---

## 1. What the local model is allowed to write
The local model may only create or update these files:
- `PROPOSE-CURRENT.md` — one-time pinned proposal (never approved).  
- `aether/02-BOOKMARKS` — aether-only snapshot of CURRENT bytes (parked; not approve).  
- `aether/03-VERBS` — verb list for aether (parked; not approve).  
- `aether/04-CURRENT.md` — current state record (parked; not approve).  

**Never:**
- Write `CURRENT.md`, `preflight.md`, `apply.md`, or `approve.md`.  
- Run `aether run` directly.  
- Approve any proposal.  
- Unlock anything.

---

## 2. What it must never write or run
The local model must not:
- Write `CURRENT.md`, `preflight.md`, `apply.md`, or `approve.md`.  
- Create, modify, or delete `CURRENT.lock`, `aether/01-PIN.md`, `aether/05-STATUS.md`, `aether/06-RECORD.md`.  
- Run `aether run` (parked; operator runs it).  
- Approve any proposal.  
- Unlock anything.  
- Claim current permission.  
- Name a password, key, token, or root command.

---

## 3. How a call is pinned (tag, host, SYSTEM)
A call is pinned by:
- **Tag:** `DRAFT_DESK_MODEL` (already set to `personal-llm-sft-v6:latest`).  
- **Host tag:** `personal-llm-sft-v6:latest`.  
- **SYSTEM:** the model may propose under SYSTEM, but it must not approve.

---

## 4. How propose files sit next to CURRENT, preflight, apply, approve
`PROPOSE-CURRENT.md` sits beside `CURRENT.md`, `preflight.md`, `apply.md`, and `approve.md`.  
- It is **never** approved by the model.  
- Approval requires a separate operator action (not this framework).

---

## 5. Doctor's Note (stuck-gate record; not Yes; not the grant)
`aether/01-PIN.md` records:
- Stuck gate status (`STUCK`, `RESOLVED`).  
- Reason, next step, and whether a **Yes** was issued.  
- This file is **not** the grant.

---

## 6. Bookmark (snapshot of CURRENT bytes; parked; not Yes; not apply)
`aether/02-BOOKMARKS` holds:
- `CURRENT.md` snapshot (`CURRENT_BYTES`).  
- `preflight.md`, `apply.md`, `approve.md` snapshots (`PREFLIGHT_BYTES`, `APPLY_BYTES`, `APPROVE_BYTES`).  
- Timestamps and hashes.  
- This is **parked**; it is not a Yes, not apply, not approve.

---

## 7. aether run (parked; ollama-shaped type-then-approve-or-reject)
`aether/03-VERBS` lists allowed verbs:
- `type`, `list`, `status`, `help`.  
- **Not:** `run`.  
- `aether run` is parked; the operator runs it.

---

## 8. When rented GPU is the hardcore path (operator Yes; not this halt)
Rented GPU is a separate, operator-controlled path:
- Requires explicit operator **Yes**.  
- Not covered by this local-model framework.  
- Never claim permission here.

---

## 9. Failure modes
If any of these fail, record them in `aether/06-RECORD.md`:
- `DRAFT_DESK_MODEL` not set to `personal-llm-sft-v6:latest`.  
- Host tag mismatch (`personal-llm-sft-v6:latest`).  
- Weight outside APK and outside git.  
- Model attempts to approve or unlock.  
- `PROPOSE-CURRENT.md` created without operator approval.  
- `aether run` called directly (parked).

---

## 10. A short standard call recipe
```bash
# Set the pinned tag
export DRAFT_DESK_MODEL=personal-llm-sft-v6:latest

# Start a host call (writes PROPOSE-CURRENT.md only)
ollama chat personal-llm-sft-v6:latest \
  --system "You are a local-model assistant. You may propose but never approve."

# Later, operator approves (not the model)
aether approve

# Snapshot CURRENT bytes for bookmarking
aether snapshot current

# Run on rented GPU only after operator Yes
aether run --gpu-yes
```

---

## Self-grill: holes, stale pins, and what could become a Yes by accident
**Holes:**
1. No explicit `REVIEW` gate between propose and approve.  
2. No explicit `AUDIT` gate for weight integrity.  
3. No explicit `REPLAY` gate to prevent replay attacks.  
4. No explicit `LOCK` gate when the operator is absent.

**Stale pins:**
1. `DRAFT_DESK_MODEL` must not be changed without a new review.  
2. Host tag must never drift from `personal-llm-sft-v6:latest`.  
3. Weight path must remain outside APK and git.  
4. `aether run` must stay parked until operator Yes.

**What could become a Yes by accident:**
1. The model claims current permission (never allowed).  
2. Silence is mistaken for approval (silence is never permission).  
3. A propose file is renamed to approve.md without audit.  
4. `aether run` is called directly instead of after operator Yes.

**Next safe step:**
- Operator reviews the proposal, then approves with a separate command.  
- Never claim current permission.  
- Silence is never permission.

Go!

# DRAFT_DESK_MODEL — personal-llm-sft-v6:latest
**Host tag:** `personal-llm-sft-v6:latest`  
**Weight policy:** weights stay outside the APK and outside git (never inside).  
**Rule of thumb:** a model may propose; it never approves. Silence is never permission.

---

## 1. What the local model is allowed to write
The local model may only create or update these files:
- `PROPOSE-CURRENT.md` — one-time pinned proposal (never approved).  
- `aether/02-BOOKMARKS` — aether-only snapshot of CURRENT bytes (parked; not approve).  
- `aether/03-VERBS` — verb list for aether (parked; not approve).  
- `aether/04-CURRENT.md` — current state record (parked; not approve).  

**Never:**
- Write `CURRENT.md`, `preflight.md`, `apply.md`, or `approve.md`.  
- Run `aether run` directly.  
- Approve any proposal.  
- Unlock anything.

---

## 2. What it must never write or run
The local model must not:
- Write `CURRENT.md`, `preflight.md`, `apply.md`, or `approve.md`.  
- Create, modify, or delete `CURRENT.lock`, `aether/01-PIN.md`, `aether/05-STATUS.md`, `aether/06-RECORD.md`.  
- Run `aether run` (parked; operator runs it).  
- Approve any proposal.  
- Unlock anything.  
- Claim current permission.  
- Name a password, key, token, or root command.

---

## 3. How a call is pinned (tag, host, SYSTEM)
A call is pinned by:
- **Tag:** `DRAFT_DESK_MODEL` (already set to `personal-llm-sft-v6:latest`).  
- **Host tag:** `personal-llm-sft-v6:latest`.  
- **SYSTEM:** the model may propose under SYSTEM, but it must not approve.

---

## 4. How propose files sit next to CURRENT, preflight, apply, approve
`PROPOSE-CURRENT.md` sits beside `CURRENT.md`, `preflight.md`, `apply.md`, and `approve.md`.  
- It is **never** approved by the model.  
- Approval requires a separate operator action (not this framework).

---

## 5. Doctor's Note (stuck-gate record; not Yes; not the grant)
`aether/01-PIN.md` records:
- Stuck gate status (`STUCK`, `RESOLVED`).  
- Reason, next step, and whether a **Yes** was issued.  
- This file is **not** the grant.

---

## 6. Bookmark (snapshot of CURRENT bytes; parked; not Yes; not apply)
`aether/02-BOOKMARKS` holds:
- `CURRENT.md` snapshot (`CURRENT_BYTES`).  
- `preflight.md`, `apply.md`, `approve.md` snapshots (`PREFLIGHT_BYTES`, `APPLY_BYTES`, `APPROVE_BYTES`).  
- Timestamps and hashes.  
- This is **parked**; it is not a Yes, not apply, not approve.

---

## 7. aether run (parked; ollama-shaped type-then-approve-or-reject)
`aether/03-VERBS` lists allowed verbs:
- `type`, `list`, `status`, `help`.  
- **Not:** `run`.  
- `aether run` is parked; the operator runs it.

---

## 8. When rented GPU is the hardcore path (operator Yes; not this halt)
Rented GPU is a separate, operator-controlled path:
- Requires explicit operator **Yes**.  
- Not covered by this local-model framework.  
- Never claim permission here.

---

## 9. Failure modes
If any of these fail, record them in `aether/06-RECORD.md`:
- `DRAFT_DESK_MODEL` not set to `personal-llm-sft-v6:latest`.  
- Host tag mismatch (`personal-llm-sft-v6:latest`).  
- Weight outside APK and outside git.  
- Model attempts to approve or unlock.  
- `PROPOSE-CURRENT.md` created without operator approval.  
- `aether run` called directly (parked).

---

## 10. A short standard call recipe
```bash
# Set the pinned tag
export DRAFT_DESK_MODEL=personal-
