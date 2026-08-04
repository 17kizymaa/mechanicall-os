# Protocol-first test surface (design)

**Status:** active sprint design · 2026-08-04  
**Product under test:** Mechanicall **local authority protocol** (CURRENT + preflight + human yes)  
**Not under test as core product:** multi-seat hosted SaaS narrative  

## Why this sprint

Peer review (CONDITIONAL) and operator observation:

- Docs drifted toward Session-as-product; core is the **protocol**.  
- Client One did **not** meaningfully use hosted Session (no sustained model traffic).  
- Next sprint: **develop and test the protocol** with code + prose first; website remains the **easiest lab surface**, redesigned as an intentional **understanding test** — not a boring ceremony dump and not a pure action facade.

## Two failure modes to avoid

| Mode | Symptom | Fix |
|------|---------|-----|
| **Boring-protocol** | Walls of CURRENT schema; user disengages | Teach by *doing* one Next under a live plan; show refuse/allow in motion |
| **Action-facade** | Shiny consumer AI chat that never binds Next | Every consequential path hits CURRENT visibility + outside-chat Yes + optional preflight literacy |

**Goal UX:** cutting-edge agent *action* **under** protocol discipline — the user *feels* power and *passes* a comprehension check.

## Protocol product (code + prose first)

1. **Schema** — SPEC-v0.2 fields required; `aether current validate` fails closed on missing Objective/Next/Prohibited structure.  
2. **Preflight** — already core; demos must show **refuse** and **allow**.  
3. **Human approve** — only human advances Approval; models propose CURRENT text only.  
4. **Events** — inspectable `.aether/events.jsonl`.  
5. **Docs** — PRODUCT boundary map; cooperative language (not false “Domain jail”).

## Website role (after protocol green)

Redesign `/session` (or `/protocol`) as **Protocol Lab**:

1. **Hook (action):** short high-agency agent turn (safe tools only).  
2. **Bind (protocol):** force plan talk into CURRENT proposal; Yes outside chat.  
3. **Probe (understanding):** one intentional check — e.g. ask model to do prohibited action → must refuse; user confirms they saw the plan rail.  
4. **Score (soft):** not gamification chrome — just “you just used the protocol.”  
5. **Cap:** still ≤5 seats if hosted; label **lab**, not product core.

Hosted seats remain **adjacent alpha**; sovereignty story stays **local** `aether` + folder CURRENT.

## Client One

No dependency on them using the site this sprint. When they return, lab should teach protocol in minutes without pretending they already adopted seats.

## Claim → command map (protocol alpha)

| Claim | Command |
|-------|---------|
| Schema is SPEC-shaped | `aether current validate` |
| Refuse outside Next / Prohibited | `aether preflight <bad-action>` |
| Allow declared Next | `aether preflight <next>` |
| Human only advances authority | `aether approve "…"` (never model) |
| Lifecycle cycles after APPROVED | `aether next <new-id>` (refuse if unapproved/unchanged) |
| One-command literacy | `aether demo` → `DEMO OK` (temp root) |
| External TUI paste | `aether brief` |
| Out-of-band edit report | `aether drift` (exit 1 if dirty) |
| Read-only gate check | `aether probe <action-id>` |
| Inspect ledger | `cat .aether/events.jsonl` |

## Success criteria

- [x] `aether current validate` green on template + root CURRENT  
- [x] PRODUCT/AGENTS/NOT-IMPLEMENTED agree with peer boundary map  
- [x] `aether next` re-SELECT after APPROVED (Wave 0 Opus lead)  
- [ ] One local protocol demo script (`aether demo`) refuse + allow + approve + next  
- [ ] Grok brief/drift observability  
- [ ] Session privacy opening rewritten when next site deploy (static vs lab split)  
- [ ] Optional: Protocol Lab page ships only after validate + demo exist  

## Related

- `PRODUCT.md` · `SPEC-v0.2.md` · `docs/ALPHA-LIMITATIONS.md`  
- Peer response: `dev/14_…/phone-pack-8/sessions/06b_PEER-RESPONSE-…`  
