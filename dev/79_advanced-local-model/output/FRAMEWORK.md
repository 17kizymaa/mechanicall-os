# Advanced local-model framework

**Not CURRENT. Not a Yes.** One document for host tag `personal-llm-sft-v6:latest`. Written 2026-10-16 under Next `advanced-local-model`.

The operator still disposes. This file does not add `aether bookmark`. It does not restore a snapshot onto `CURRENT.md`. It does not spend Onyx.

---

## 1. What it is

The local model is a **propose substrate**. It drafts text. It never holds the gate.

```text
human
  └─ Interface (Markdown, shell, Grok)
       ├─ aether — CURRENT, preflight, apply, approve
       ├─ filesystem — truth
       └─ personal-llm-sft-v6:latest — propose only
```

It is not a fourth authority layer. `CURRENT.md` plus human `aether approve` remain the Yes.

v6's grill (`output/V6-GRILL.md`) kept that doctrine and then invented a second tree (`aether/01-PIN.md`, `preflight.md`, `apply.md`, `approve.md`, `aether snapshot`, `aether run --gpu-yes`). Those paths are **not** this framework. The live verbs and files below are.

---

## 2. Pin (tag, host, SYSTEM, constant)

| Pin | Live value | Where |
|-----|------------|--------|
| Serve tag | `personal-llm-sft-v6:latest` | Ollama id `ee279269b24a`, 2.7 GB |
| Desk constant | `DRAFT_DESK_MODEL = "personal-llm-sft-v6:latest"` | `python/aether_pocket.py` |
| Pick order | `personal-llm-sft-v6` first | `python/aether_llm.py` `OLLAMA_PREFER` |
| SYSTEM | `references/personal-llm-system.txt` | loaded by `personal_llm_system_text()` |
| Host | `http://127.0.0.1:11434` / `http://myarch:11434` | pocket `DEFAULT_DESK_HOSTS`; never `0.0.0.0` |
| Weight | local Ollama store only | not git, not `android/` |

Older tags stay installed: `sft-v4`, `sft-v2`, `full:v1`, `pilot:v0`. They are fallbacks. The desk pin is v6.

`docs/PERSONAL-LLM-LAYER.md` still lists v2 as preferred. That paragraph is **stale**. The code pin is v6. A later docs Next may catch the page up. This halt does not rewrite that doc as law.

Env that may override a call, and must not silently replace the desk pin:

- `AETHER_LLM_PROVIDER=ollama`
- `AETHER_OLLAMA_MODEL`
- `AETHER_OLLAMA_HOST`
- `AETHER_PERSONAL_LLM_SYSTEM=1`

A tag change is a CURRENT body change, then human apply, then human approve. Editing the Python constant without that loop is not this framework.

---

## 3. What a call may write

Allowed, under a later allowed action that names the call:

- `PROPOSE-CURRENT.md` in a **pocket** that is not the operator tree and not this repo (`agent_edit_propose`, `draft_chat`).
- Lab notes under `dev/NN_*/output/` (this folder).
- `.aether/events.jsonl` notes and `aether artifact` metadata when a human or this halt registers a file.

Never:

- `CURRENT.md` as the model's own write
- `aether approve` / `apply` / `next` / `reject`
- a weight, GGUF, adapter, or Modelfile under `android/`
- a model drawn on `sit_well_draft.png`
- secrets, keys, tokens, passwords, unlock commands
- Onyx spend
- `~/anphuni-project/CURRENT.md`

`draft_chat` already refuses operator-tree pockets and public Ollama hosts. Keep that.

---

## 4. Where it sits next to preflight, apply, approve

| Hand | Who | What |
|------|-----|------|
| Propose | model / parent call | writes `PROPOSE-CURRENT.md` or a `.aether/proposals/*.md` |
| `aether preflight <Next>` | cooperative agent | allows only the pinned Next |
| `aether apply <proposal>` | human | copies the fenced `# CURRENT` body. Refuses a Next/Action-id split. Not a Yes |
| `aether approve "…"` | human | Yes |
| `aether next <id>` | human | re-SELECT after APPROVED; refuses unchanged |
| Doctor's Note | anyone | stuck-gate record. Not CURRENT. Not Yes. Not the grant |
| Bookmark | parked | copy of `CURRENT.md` bytes. Not Yes. Not apply |

Silence is never permission. A green score is not a Yes. A propose file renamed is still a propose file.

Apply backups land in `.aether/current-before/`. That is an apply side-effect. It is not bookmark.

---

## 5. Doctor's Note

A Doctor's Note names:

- the live Next at the time of the note
- the exam
- what was refused
- a blank the operator fills before a later proposal

It must not contain a Yes, a secret, a root command, or a claim of current permission.

Sudo analogy: attribution. The note ties an allowed grant to one action at one time. The note never becomes the grant.

This halt's exam already used that shape on the header/body split. After apply of `CURRENT-proposal-20261016-1724.md`, header Next and body Action id both read `advanced-local-model`.

---

## 6. Bookmark (parked)

Spec already written: `.aether/proposals/CURRENT-proposal-20261016-1724.md`.

```
aether bookmark [label] [path]
  copy CURRENT.md → .aether/bookmarks/CURRENT-<UTC>[-label].md
  log kind=bookmark
  do not change CURRENT.md, do not approve, do not apply
```

Live snapshot, not the verb:

`.aether/bookmarks/CURRENT-20261016T162428Z-this-current.md`  
cksum `3532677481` · 12087 bytes (the pre-apply split file).

`bookmark` is **absent** from `AETHER_VERBS`. Restore is a later human hand, like apply. Models do not restore.

---

## 7. Standard call recipe (shipped)

Desk propose (pocket, not this repo):

```bash
# constant already in python/aether_pocket.py
# DRAFT_DESK_MODEL = "personal-llm-sft-v6:latest"

# parent call only, after CURRENT allows it:
# agent_edit_propose(pocket_under_tmp, ollama_host="http://127.0.0.1:11434")
# writes PROPOSE-CURRENT.md only
```

Garden / rival (same tag via pick order):

```bash
export AETHER_LLM_PROVIDER=ollama
# omit AETHER_OLLAMA_MODEL to let OLLAMA_PREFER pick v6
aether garden status
```

Authority (human):

```bash
aether current
aether current validate
aether preflight advanced-local-model
# human: aether apply <proposal.md>
# human: aether approve "reason"
```

Do not `export DRAFT_DESK_MODEL`. That name is a Python constant. Do not `ollama chat` as the desk. Do not `aether snapshot`. Do not `aether run --gpu-yes`. Those strings came from the v6 grill and are not verbs.

---

## 8. Rented GPU (parked)

Hardcore / on-demand train or long eval on rented compute is a **later operator Yes**. It is not this halt. It does not copy a weight into `android/`. It does not absorb personal-llm ownership into mechanicall-os (`absorb-personal-llm` stays an archive prohibition).

---

## 9. Failure modes (grilled)

From the live clock and from v6's own draft:

1. **Invented CLI.** v6 named `aether snapshot`, `aether run --gpu-yes`, and files `preflight.md` / `apply.md` / `approve.md`. Treat that as a refuse. The framework is the real verb list in `aether`.
2. **Loop.** The grill repeated the same ten sections three times. A call needs a byte cap and a single-pass halt.
3. **Header/body split.** `aether next` can move the header while the applied body stays. Apply refuses that split. Doctor's Note it. Do not guess which id is Next.
4. **Approve-as-notebook.** Freeform ideas stored as `aether approve` touch the gate. Seed or event is the notebook. Approve is Yes.
5. **Stale docs.** `PERSONAL-LLM-LAYER.md` still prefers v2. Code prefers v6. Docs are not the pin.
6. **Weight in the package.** An old approve quote asked to wire the model into the APK. Keep: weight outside. Draft sheet stays NOT ACTIVE and "not the plan".
7. **Silence as Yes.** Model agreement is not approval.
8. **Bookmark as Yes.** A snapshot of bytes is not apply and not approve.
9. **Onyx ungrounded.** Empty index cannot ground a Yes. Onyx stays parked.
10. **Env override.** `AETHER_OLLAMA_MODEL` can point a garden call at the wrong tag while `DRAFT_DESK_MODEL` stays v6. Name the pin in the call receipt.

---

## 10. Shipped / parked / prohibited

**Shipped**

- Tag `personal-llm-sft-v6:latest` on this host
- `DRAFT_DESK_MODEL` and `OLLAMA_PREFER` pointing at v6
- Pocket writes `PROPOSE-CURRENT.md` only
- SYSTEM file
- `aether` authority verbs (current, preflight, apply, approve, reject, next, probe, event, artifact)

**Parked (not this halt)**

- `aether bookmark` / restore
- `aether run` (ollama-shaped type then approve or reject)
- `cmd-aether-approve` (protect typed reasons)
- event-inject hook
- desk-model-turn / Onyx
- rented GPU
- millwork host propose into `/tmp` as a product cycle
- catching `PERSONAL-LLM-LAYER.md` up to v6

**Prohibited**

- `automatic-approve`, `model-auto-write-current`, `bookmark-as-yes`, `restore-bookmark-by-model`
- model `aether approve` / `apply` / `next`
- weight in git or APK
- secrets in git

---

## 11. Evidence this halt can show

1. Header Next and body Action id both `advanced-local-model`.
2. `bookmark` absent from `AETHER_VERBS`.
3. Snapshot cksum `3532677481` unchanged.
4. No GGUF / Modelfile / safetensors under `android/`.
5. `versionCode` 46, `versionName` `0.19.21-loop-from-20`, `applicationId` `com.mechanicall.pocket.demo`.
6. One local v6 call at `2026-10-16T17:21:34Z`, 334 prompt / 3762 eval tokens, no Onyx.

---

## 12. What the operator does with this file

This document is the framework the Next asked for. It is still not a Yes.

Later proposals may: implement `aether bookmark`; add `aether run`; refresh `PERSONAL-LLM-LAYER.md`; or name one pocket call. Each of those is a new body the human applies, then a real approve reason.

Until then: v6 proposes. The operator disposes. The weight stays outside the APK.
