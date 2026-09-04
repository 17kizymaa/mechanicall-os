# Aggressive mechanicall-os dev mode — in-tree, not child CURRENT

**When:** 2026-08-24  
**Not law.** W8=1: **no child CURRENT** on this operator tree. Amendment: keep projects **under this folder** as aggressive **dev mode**.

Live operator Next remains root `CURRENT.md` (`sit-distro-gate`). Subagents still never `aether approve`.

---

## What “the old workflow” already is

Projects live **in this git tree**, not as a second live Next:

| Path | Role | Has CURRENT.md? | Operator law? |
|------|------|-----------------|---------------|
| `/CURRENT.md` | One Next | **Yes — live** | **Yes** |
| `dev/NN_*/` | ICM factory (CONTEXT.md + output/) | No (must not) | No |
| `examples/dev-task/` | Sample Domain | Yes — **sample** | No |
| `examples/pocket-demo-client/` | Bind-off-repo template | Yes — **sample** | No |
| `examples/propose-current/` | Propose files, not applied law | Propose only | No |
| `domains/` | LAB samples (README; samples named, often absent) | Must not become live Next | No |
| `research/` | Speculative | No | No |

`aether … [path]` still means: **one Next per folder**. A sample CURRENT under `examples/` is a **toy folder**. The operator session must not `aether next` it as if it were root.

Historical Keep: **no child Domain as operator session authority.** That stays. Aggressive dev mode does **not** recant it.

---

## Aggressive mechanicall-os dev mode (proposed discipline)

Use the monorepo as the **factory**:

1. **All mechanicall-os development** lands under this folder (`dev/`, `examples/`, `research/`, `android/`). Do not exile work to a sibling repo so a subagent can have a fake CURRENT.  
2. **Subagent contract is `CONTEXT.md`**, never `CURRENT.md`. Parallel = many stages / many `output/` dirs, **one** root Next.  
3. **Sample CURRENTs** stay under `examples/` (and empty `domains/` toys). Agents may `aether current examples/dev-task` to **learn** the schema. They must not treat it as live operator law.  
4. **Sitter law stays off this tree** (B10). Client folders are `~/…` or the phone bind path — that is the opposite of dev mode.  
5. **Halt at `output/`.** Aggressive means more factories in-tree, not skipping Yes.

This is how `dev/01`–`dev/43` already work. “Aggressive” = lean into that, instead of inventing session child CURRENTs.

---

## What would break W8=1

- `dev/43/CURRENT.md` with **Next:** a subagent can preflight  
- `domains/my-sprint/CURRENT.md` that the operator session approves as if it were root  
- Worktree child CURRENT that `aether approve`s root law  

Those are dual-Next. Rejected.

---

## Checkpoint

**Locked W13=2:** `dev/` ICM factories + `examples/` sample CURRENTs as toys. No new `projects/` tree. `domains/<name>/CURRENT.md` is not the operator session. Root CURRENT remains the only live Next. Not this Next’s implement.
