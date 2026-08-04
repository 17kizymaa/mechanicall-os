# Mechanicall OS v0.2 — Authority & Approval Layer

**Doc status:** **NORMATIVE** — protocol contract for live `aether` v0.2.  
**Conflict winner:** over SPEC-v0.1 and all NON-NORMATIVE docs; loses only to live project `CURRENT.md`.  
**Map:** `docs/DOC-AUTHORITY.md`

**Name:** Mechanicall OS (product) · `mechanicall-os` (repository)  
**Builds on:** SPEC-v0.1 (awareness sidecars + `aether` shell CLI) — historical  
**Mission (authorized):** filesystem-native authority and approval for human–agent projects.  
**Not authorized:** PostgreSQL / pgvector / LangGraph / autonomous multi-agent studio.  
**Tool alignment:** repo-root `./aether` POSIX CLI (header v0.2).

## Goal

Prevent long-running AI-assisted projects from:

1. forgetting the brief;
2. treating every idea as an instruction;
3. continuing production after a human stop signal.

The system must answer five questions reliably:

1. What is the current objective?
2. What decision is presently authoritative?
3. What is the next allowed action?
4. What actions are prohibited or require approval?
5. What happened, and which artifact proves it?

## Non-negotiable principles (still locked)

1. Filesystem is the single source of truth. No hidden databases.
2. Markdown + POSIX shell + (optional tiny Python) as userland.
3. Active, observable sidecars only. `cat` / `grep` / `git diff` sufficient.
4. Default happy path has **zero running daemons**.
5. **Silence is never permission.** Approval must be explicit.
6. **LLMs may propose; only humans approve.** Workers cannot approve their own work.

## Official authority layout (v0.2)

```
project/
├── CURRENT.md                  # AUTHORITATIVE operating state (human-owned)
├── DECISIONS.md                # Optional durable decision log
├── .context.md                 # Descriptive context (v0.1; not authority)
├── .session.md                 # Chronological activity (Rhizome)
├── inbox.md / ~/inbox.md       # Raw capture (not authority)
├── .aether/
│   ├── state.json              # Distill cache (gitignored)
│   ├── trusted                 # Local hook trust marker
│   ├── events.jsonl            # Append-only machine transition log
│   ├── artifacts/              # Registered artifact metadata (JSON)
│   ├── hooks/
│   └── .scope
└── artifacts/                  # Optional produced outputs (project-owned)
```

### Authority separation

| File | Role | Can override CURRENT? |
|------|------|------------------------|
| `CURRENT.md` | Present authority | — (source of truth for gates) |
| `.context.md` | Descriptive inventory + human notes | **No** |
| `.session.md` | Chronological log | **No** |
| `inbox.md` / seeds | Capture only | **No** |
| Older seeds / history | Evidence | **No** |

## CURRENT.md semantics

Human-readable Markdown. Structured fields (parsed by `aether`):

```markdown
# CURRENT

**Objective:** <one sentence>
**Phase:** CAPTURE | SELECT | COMMIT | EXECUTE | REVIEW | APPROVE
**Status:** DRAFT | READY-FOR-REVIEW | APPROVED | REJECTED | BLOCKED | BLOCKED-PENDING-HUMAN
**Baseline:** <label or path>
**Next:** <action-id>          # machine-facing next allowed action id
**Approval:** PENDING | APPROVED | REJECTED

## Keep
- ...

## Reject
- ...

## Limits
- ...

## Next allowed action
Human prose describing the one authorized next step.

## Approval condition
What the human must write/do to approve.

## Prohibited
- action-id-or-phrase
- another-forbidden-action
```

### Lifecycle

```text
CAPTURE → SELECT → COMMIT → EXECUTE → REVIEW → APPROVE/REJECT
```

- **CAPTURE** — seeds accepted; never become authority automatically.
- **SELECT** — compare evidence; keep/kill.
- **COMMIT** — human locks baseline + constraints into CURRENT.
- **EXECUTE** — agent may perform **only** the declared next action.
- **REVIEW** — present artifact; no automatic repair build.
- **APPROVE/REJECT** — explicit human event; reject returns to SELECT.

## CLI surface (v0.2 additions)

| Command | Purpose |
|---------|---------|
| `aether current [path]` | Show parsed authority summary |
| `aether current init [path]` | Create template `CURRENT.md` if missing |
| `aether preflight <action> [path]` | Allow (exit 0) or refuse (exit **3**) with reason |
| `aether approve [reason] [path]` | Record human APPROVED; update Status/Approval |
| `aether reject [reason] [path]` | Record human REJECTED; return Phase to SELECT |
| `aether next <action-id> [path]` | After APPROVED: re-SELECT (refuse exit **3** if not approved / unchanged) |
| `aether probe <action-id> [path]` | Read-only would-preflight (exit 0 allow / **3** refuse) |
| `aether event <msg> [path]` | Append freeform transition to events.jsonl |
| `aether artifact <path> [--action A] [--status S]` | Register an artifact metadata record |

Existing v0.1 commands (`init`, `status`, `distill`, `watch`, `seed`, …) remain.
`status` also surfaces CURRENT summary when present.

### Exit codes (normative)

| Code | Meaning | Examples |
|------|---------|----------|
| **0** | Success / allowed | `preflight` allow, `approve`, `demo` OK |
| **1** | Internal error **or** report signal | Write failure; `aether drift` when dirty (not a crash) |
| **2** | Usage error | Unknown verb, missing required args, invalid flags/ids |
| **3** | Protocol refusal | `preflight` / `probe` refuse; `next` not approved or unchanged |

Wrappers and agent harnesses **must not** treat all non-zero as equal: **3** is a correct closed gate; **2** is a typo/bad invocation; **1** needs investigation (except documented `drift`).

### CLI size doctrine (normative, v0.2)

**Decision (2026-08-04 · `next-05-loc-decision`):** Retire SPEC-v0.1’s ≤220-line /
“one screen of `cat aether`” success criteria. **Do not** split the CLI solely
to chase a line-count myth this sprint.

| Keep | Meaning |
|------|---------|
| **Single file** | Core CLI remains one POSIX `#!/bin/sh` script at repo root (`aether`) — no build step to run authority verbs |
| **No hidden runtime** | Authority still `cat`/`grep`/`git diff`-able; no second opaque binary as law |
| **Readable by verb** | Prefer section comments + `cmd_*` naming so a verb can be found without reading the whole file |
| **Inspectable helpers** | Optional Python (panel, llm, shell) stays *beside* the shell core, not a replacement authority store |

| Retire | Why |
|--------|-----|
| ≤220 lines total | Authority surface alone exceeded that; keeping the number was false doctrine |
| “Fits in one screen of `cat aether`” | False for a working protocol CLI; peers correctly called the contradiction |

**Budget (soft, not a hard CI fail):** Prefer not to grow `aether` without a verb-level reason. Large growth → consider extracting *non-authority* helpers first; authority verbs stay in the single file until a future explicit split decision.

Measured ~2026-08-04: `wc -l aether` ≈ **1900** lines (v0.2 + peer exit-code work).

## Preflight rules

Before a consequential action id is considered allowed:

1. `CURRENT.md` must exist (else refuse with “no authority file”).
2. Action must not match any entry under `## Prohibited` (exact match, or
   case-insensitive containment with token length ≥ 3 — short accidents like
   `x` never match).
3. If `**Next:**` is set (and not the literal `unset`), action must match it
   (exact, case-insensitive).
4. If Status is `BLOCKED` or `BLOCKED-PENDING-HUMAN`, only the declared Next
   action (if any) may pass; everything else is refused.
5. Status `REJECTED` refuses execute-class actions until human re-selects
   (Phase back to SELECT; Next may be updated by human).
6. Failed preflight prints a readable refusal and exits **3** (protocol
   refuse). Never infers approval from silence or sentiment. Usage mistakes
   (missing action id) exit **2**.
7. **Preflight leaves a receipt** (`.aether/preflight-last` + append-only
   `.aether/preflight.jsonl`): timestamp, action, result, exit code, tree
   fingerprint (`git:HEAD:d0|d1` or `tree:<hash>`).  
   **`aether approve` prints** one unmissable line (never blocks):
   - `preflight: PASS @ <fp> (current) …` — last check matches current tree  
   - `preflight: STALE (checked <fp>, now <fp2>) …` — tree changed since check  
   - `preflight: ABSENT` — no receipt  
   Rule: **the gate may be human, but the gate must leave a trace.**

## Events (`.aether/events.jsonl`)

One JSON object per line, append-only. Example fields:

```json
{"ts":"2026-07-18T12:00:00Z","kind":"phase","from":"SELECT","to":"COMMIT","by":"human"}
{"ts":"2026-07-18T12:02:00Z","kind":"preflight","action":"rough-v6","result":"refused","reason":"..."}
{"ts":"2026-07-18T12:14:00Z","kind":"artifact","path":"artifacts/proof-01.mp4","action":"silent-proof","status":"produced"}
{"ts":"2026-07-18T12:20:00Z","kind":"reject","reason":"arrival on plate 4 fails","by":"human"}
```

Humans may also keep a prose trail in `.session.md` / `DECISIONS.md`.

## Artifact registration

`aether artifact <path>` writes `.aether/artifacts/<id>.json` and logs an event:

- input/baseline (from CURRENT if present);
- action id;
- output path;
- timestamp;
- status;
- optional checksum (`cksum`).

## Explicit non-goals for v0.2

See `NOT-IMPLEMENTED.md`. In particular: no PostgreSQL, no vector memory, no
LangGraph, no autonomous agent pool, no web dashboard, no “industrial OS” claim.

## Acceptance criteria (mission-ready)

### Correctness

- Human notes survive repeated distillation (v0.1).
- Quoted arguments survive unchanged.
- Current authority cannot be silently overwritten by older context/seeds.
- Malformed CURRENT/marker state fails closed.
- Writes are atomic (temp + `mv`).

### Safety

- Untrusted hooks never execute.
- `--no-hooks` identical across watch/distill/poke.
- Consequential actions require explicit permission (preflight).
- Workers cannot approve their own outputs (`approve`/`reject` are human CLI).
- Rejection never automatically initiates another attempt.

### Control

- One unambiguous active objective per project (`CURRENT.md`).
- Only one next action authorized (`**Next:**`).
- Prohibited actions produce clear refusal messages.
- Approval and rejection are explicit events.
- Silence is never permission.

### Inspectability

Operator understands state with:

```text
cat CURRENT.md
cat .aether/events.jsonl
grep -i refuse .aether/events.jsonl
git diff
```

### Product proof

- Reel-control example demonstrates stop-before-spiral.
- At least one non-reel example shows the model is not video-hardcoded.
- Tests cover refuse / allow / approve / reject paths.

## Condition that must remain true

> The product must prove that it can stop one wrong action before it adds any
> machinery for performing more actions.
