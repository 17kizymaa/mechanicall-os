# Stage map — people-app workspace (factory product)

**When:** 2026-08-18  
**From:** `01_discovery/output/discovery.md`  
**Not this file:** do not write the tree (that is factory `03_scaffolding`).  
**Not law:** operator Next stays `mobile-planning-demo`.

The **app** a person copies is a workspace with these stages. One agent. One bound folder. CURRENT in *that* folder is the Yes.

```
people-app/                     # copyable workspace (name TBD at scaffold)
  CONTEXT.md                    # Layer 1: route to 01_bind
  01_bind/
  02_show-plan/
  03_propose/
  04_gate/
  05_do/
  06_receipt/
  references/                   # Layer 3: refuse-operator, PRODUCT pitch, Yes rules
```

One-way: `01 → 02 → 03 → 04 → 05 → 06`. No stage reads a later `output/`. Human may edit any `output/` before saying proceed.

---

## 01_bind

**Job:** name the project folder. Refuse this operator repo.

| | |
|--|--|
| **Inputs** | User path (Layer 4). `references/refuse-operator.md` (L3). |
| **Process** | Resolve path. Fail if it is `mechanicall-os` (PRODUCT.md + AGENTS.md + `bin/aether` markers). Else write the bind. |
| **Outputs** | `output/BIND.md` — absolute path, refuse result, one line “this is not the operator tree.” |
| **Checkpoint** | Human confirms the folder before 02. |

---

## 02_show-plan

**Job:** put the live plan in front of them. No CLI as the front door — write a page they can read.

| | |
|--|--|
| **Inputs** | `../01_bind/output/BIND.md`. Bound `CURRENT.md` (or “missing”). |
| **Process** | If CURRENT missing: write a seed *proposal* for init, do not invent law. If present: copy Objective / Next / Limits into a short face. Never bind operator CURRENT. |
| **Outputs** | `output/PLAN.md` — what they would see. `output/MISSING.md` if no CURRENT (init is a human Yes in 04, not silent `current init`). |
| **Checkpoint** | Human reads PLAN.md. |

---

## 03_propose

**Job:** agent drafts only. Point-and-clicking that would change the plan goes into PROPOSE, not CURRENT.

| | |
|--|--|
| **Inputs** | BIND.md, PLAN.md, bound folder tree (scoped — not the whole disk). `references/yes-rules.md`. |
| **Process** | One agent. Write/update `PROPOSE-CURRENT.md` in the bound folder *or* `output/PROPOSE.md` if they want the draft in the workspace first. Do not write CURRENT. Do not approve. |
| **Outputs** | `output/PROPOSE.md` (and pointer to bound PROPOSE if written there). |
| **Checkpoint** | Human edits the propose. Creative audit: still one Next; no secrets; no second folder. |

---

## 04_gate

**Job:** human Yes or Not yet. This is Mechanicall. Silence is not Yes.

| | |
|--|--|
| **Inputs** | PLAN.md, PROPOSE.md, BIND.md. Bound `aether` (via AETHER_HOME), not a clone of the protocol. |
| **Process** | **Yes:** apply propose fields into bound CURRENT + `aether approve` with a real reason. **Not yet:** `aether reject` or leave CURRENT; stay; do not run 05. Agent never clicks Yes. |
| **Outputs** | `output/GATE.md` — yes / not-yet / skipped, reason, event snippet. |
| **Checkpoint** | If not-yet, stop. Human may return to 03. No automated loop. |

---

## 05_do

**Job:** agent does the approved Next in the bound folder. Only if GATE is yes.

| | |
|--|--|
| **Inputs** | GATE.md (must say yes), BIND.md, bound CURRENT Next. |
| **Process** | Preflight that Next in the bound folder. Do the work. Write artifacts in the bound tree and `output/WORK.md`. Do not change CURRENT. Do not start a swarm. |
| **Outputs** | `output/WORK.md` — what changed (paths). |
| **Audit** | Still one Next; no operator-tree writes. |

---

## 06_receipt

**Job:** something they can open tomorrow.

| | |
|--|--|
| **Inputs** | GATE.md, WORK.md, bound `.aether/events.jsonl` tail, DECISIONS.md. |
| **Process** | One page: what was Next, what was Yes, what files moved, what is still open. |
| **Outputs** | `output/RECEIPT.md` |
| **Checkpoint** | Human keeps or edits. Pipeline ends. |

---

## Out of this workspace

| Thing | Where it lives |
|-------|----------------|
| Operator `mechanicall-os` CURRENT | Never this bind |
| Pocket LAN `:8765` / A33 | Lab (`dev/23_*`) |
| OpenHands / Compose / Play Store | Not a stage. Optional *runner* later, not architecture |
| Swarm / multi-agent | Jake: ICM does not work here |

## Factory next

Scaffold these six folders under a `people-app/` tree (empty `output/` except `.gitkeep`). That is factory **03**. Say **proceed to 03**.
