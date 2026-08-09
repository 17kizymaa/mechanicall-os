# What Mechanicall is

**Doc status:** **NORMATIVE** — product boundary map (core vs lab vs research).  
**Conflict:** yields to live `CURRENT.md` and SPEC-v0.2 for protocol mechanics; wins over README/marketing on “what is core.”  
**Map:** `docs/DOC-AUTHORITY.md`

## Pitch (one breath)

**You decide. AI does the point-and-clicking — under a plan you can read and a yes only you can give.**

Mechanicall is a **local-first human–agent control and project-versioning layer**: one written plan (`CURRENT.md`), cooperative preflight/refusal, human-only approval, and append-only receipts. Not an auditor-only log. Not an AI hosting platform. Not “another chatbot.” Not multi-tenant SaaS.

**Durable project conversations** mean: chat is ephemeral unless it lands as CURRENT updates + events + artifacts. The trail you can `cat` later *is* the product surface.

---

## Boundary map (read this first)

| Surface | Honest label | In v0.2 core release? |
|---------|--------------|------------------------|
| **Mechanicall repository** (`aether`, CURRENT, preflight, events) | **Local filesystem authority protocol** | **Yes — this is the product** |
| **CLI + Panel + shell/chat helpers** | Self-hosted **cooperative** interfaces on the same CURRENT (not a sandbox jail) | Optional tools on core |
| **anphuni.com Session** | **Separate** capped hosted **alpha lab** (≤5 isolated server seats, OpenRouter proxy) | **No** — not Mechanicall core |
| **Club-cortex / multi-LoRA host** | Research direction only | **No** |
| **Outlook / mail integrations** | Research seed only until a dedicated CURRENT + privacy review | **No** live OAuth/SMTP |

Every public claim should fit this table. If a surface is not “core,” say so.

**Directory labels:** in-repo lab vs shipped tags live in **`docs/LAB-STATUS.md`** (research, seat, domains, dev, …).

---

## The protocol (what *is* the product)

```text
Base model      → capacity (substrate)
Personal model  → technique (propose / taste only)
CURRENT.md      → Domain / live authority (one Next)
aether preflight→ cooperative refuse/allow for declared actions
Human approve   → only actualisation of consequential change
Silence         ≠ permission
```

Filesystem is truth: `cat`, `grep`, `git diff` the plan and the event log.

| Piece | Role |
|--------|------|
| `CURRENT.md` | Plan / law for this folder (schema: SPEC-v0.2) — **versions** the live Next |
| `aether preflight` / `approve` / `reject` | Deterministic gate + human record |
| `.aether/events.jsonl` | Append-only evidence (receipts of authority) |
| Panel / shell / Session | **Interfaces** — cooperative; they do not replace CURRENT |

---

## The game (when there is a Seat UI)

On a seat-like screen, the helper **listens for competency** and answers in that register.  
You see **layout**: chat + plan + rare **outside-the-chat** yes/no. No operator dashboard cosplay.

| You | The system |
|-----|------------|
| Intent, judgment, yes/no | Drafts, tools, point-and-click **under** the plan |
| Stay human | Stay bounded |

---

## Distribution split (honest)

1. **Self-hosted technical path:** `aether` CLI + optional `aether panel` / shell helpers.  
2. **Hosted alpha lab (separate):** operator-provisioned Session seats on anphuni.com — **not** the core product definition.  
3. **Packaged single-app appliance:** research / incomplete — see `docs/SINGLE-APP-DISTRIBUTION.md`.

Do not imply CLI, Panel, Tauri, and Session are already one product.

---

## Not this product

- Multi-tenant AI host / “agent seats for sale” as the **core** offer  
- Model auto-approve  
- ChatGPT skin without a control layer  
- Sandbox that forces every external agent to preflight (cooperative only today)  
- Club-cortex as shipped  

If a session drifts into “generic AI platform,” re-read this file and `NOT-IMPLEMENTED.md`.

---

## License

| Surface | Terms |
|---------|--------|
| **This repository** (protocol CLI, docs, cooperative interfaces in-tree) | **[Apache License 2.0](./LICENSE)** — copyright 2026 anphuni / Mechanicall OS contributors |
| **Packaged single-app / seat distributions** built *from this tree* | Inherit **Apache-2.0** unless a separate NOTICE or package manifest says otherwise (`docs/SINGLE-APP-DISTRIBUTION.md`) |
| **anphuni.com Session (hosted lab)** | **Not** the same as redistributing this repo. Operator-run service: site privacy + seat provision terms apply to *use of the host*. Code paths in this repo that support Session remain Apache-2.0 when shipped as source. |

Third parties may vendor `aether` and the protocol docs under Apache-2.0 without a separate permission grant. Hosted Session capacity is not an open multi-tenant product license.

---

## Related

- Live Next: root `CURRENT.md`  
- Contract: `SPEC-v0.2.md`  
- Denials: `NOT-IMPLEMENTED.md`  
- Limits: `docs/ALPHA-LIMITATIONS.md`  
- License: `LICENSE` (Apache-2.0) · Session vs core: this boundary map + site privacy (must not contradict)