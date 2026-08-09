# Agent-agnostic cold start

**Doc status:** **NON-NORMATIVE** — operational checklist for any agent / IDE.  
**Yields to:** live `CURRENT.md`, SPEC-v0.2, PRODUCT, AGENTS.md.  
**Map:** [DOC-AUTHORITY.md](./DOC-AUTHORITY.md) · product face: [../README.md](../README.md)

One page. Works **outside** Grok TUI / panel / seat. Claude Code, Codex, Cursor, plain shell, CI — same loop.

---

## What this product is (30 seconds)

Not “open a chat UI and talk forever.”

```text
CURRENT.md     → live plan (one Next)
aether preflight → deterministic refuse/allow for declared actions
human approve  → only actualisation of consequential change
events.jsonl   → receipts when chat dies
```

**Chat is disposable. The folder is session continuity.**  
Panel / shell / Grok TUI are optional **projections** of this loop — not product identity.  
Seat packaging is **LAB** — see [LAB-STATUS.md](./LAB-STATUS.md).

---

## Cold-start checklist (do this in order)

### 1. Land in the project folder

```bash
cd /path/to/project    # the tree that owns CURRENT.md
```

### 2. Read authority (input, not chat history)

| Read | Why |
|------|-----|
| `CURRENT.md` | Objective, **one Next**, Prohibited, Limits — **INSTANCE law** |
| `AGENTS.md` (if present) | Agent operating rules (CURRENT-first; models never approve) |
| `PRODUCT.md` / `docs/ALPHA-LIMITATIONS.md` | What core is / is not (when making claims) |

Optional: `aether current` · `aether current validate` · `aether brief` (paste for external TUIs).

**Which Next is binding?** Preflight/probe pin the header field `**Next:**` (same pin as `aether current`). The body line `**Action id:**` under `## Next allowed action` should match; if header and body disagree, **stop and ask the human** — do not guess. See [FIRST-PROJECT.md](./FIRST-PROJECT.md) (header Next and body Action id must match).

### 3. Work only under Next

- Do the action-id from header `**Next:**` / `aether current` (or propose file edits the **human** accepts).  
- Do **not** invent a parallel plan.  
- Do **not** treat long chat as authority — **CURRENT** wins.  
- If `**Next:**` and body `**Action id:**` differ → stop; human fixes CURRENT (or re-SELECTs).

### 4. Before consequential work — preflight

```bash
aether preflight <action-id>    # must match Next when pinned
# exit 0 = allow · exit 3 = protocol refuse · stop on refuse
```

Read-only check (no events/receipts): `aether probe <action-id>`.

### 5. Human actualises — agents never approve

```bash
# human only:
aether approve "…"
aether next <new-action-id>     # after APPROVED — re-SELECT
# or:
aether reject "…"
```

**Silence is never permission.** Models do not run `aether approve` as their own decision.

### 6. Leave a trail (when work matters)

```bash
cat .aether/events.jsonl        # receipts
# optional: artifacts, stage output/ receipts under dev/
```

---

## The “consistent variable”

| Disk state | New agent session |
|------------|-------------------|
| **Unedited** `CURRENT.md` | Same Next — no re-brief required |
| Human-edited CURRENT / approved `aether next` | Deliberate new state — rehydrate from disk |

---

## Minimal command card

```bash
aether current
aether current validate
aether preflight <action-id>
# human: aether approve "…"
# human: aether next <id>
aether probe <action-id>        # dry would-preflight
aether brief                    # short paste for any TUI
aether demo                     # sandbox full loop (never live CURRENT)
cat .aether/events.jsonl
```

Demo / first project: [FIRST-PROJECT.md](./FIRST-PROJECT.md) · `sh scripts/alpha-demo.sh`.

---

## Alpha honesty

This is a **cooperative** contract, not a jail. Agents *can* skip preflight.  
Maturity = make the contract so cheap that good agents **default into it**.

---

## Explicit non-goals (this page)

- Not “install seat / open multi-agent dashboard first.”  
- Not conversation auto-sync as the plan (`claim-conversation-auto-sync`).  
- Not Session multi-seat SaaS as core product.  
- Not renaming Mechanicall OS in this checklist.

---

## Handoff source

PR #5 session note (multi-agent cold start):  
https://github.com/17kizymaa/mechanicall-os/pull/5#issuecomment-5232860932
