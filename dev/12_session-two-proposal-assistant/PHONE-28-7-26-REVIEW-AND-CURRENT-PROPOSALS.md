# Phone tag `28-7-26` — review + CURRENT proposals (not applied)

**Date:** 2026-07-29  
**Sources (pulled from phone `/sdcard/`):**

1. `28-7-26_CLIENT-1_SESSION-1_REVIEW.md` — sprint verdict, merge blockers, engineering rank  
2. `28-7-26_BRANCH-2_DEBUGGING-ASSISTANT-UTILITY.md` — life/runway + SuperGrok/LoRA impulse + Spike A base-model research  

**Branch now:** still `session/client-one-s2-proposal-assistant` (update at session end).  
**Today’s client session branch:** switch **after** human reviews this file.  
**Authority:** no CURRENT.md rewritten in this pass — **proposals only**.

Copies on host: `/tmp/phone-28-7-26/` (re-pull anytime via adb).

---

## 1. Understand (session intent)

| Step | Status |
|------|--------|
| Read both `28-7-26_*` phone docs | done |
| Propose CURRENT changes + missing doc pointers | **this file** |
| Wait for your review | **now** |
| Switch to the actual “today client session” branch | **after** you say so |
| Update `client-one-s2-proposal-assistant` at session end | noted |
| Finance life narrative for finance agent | separate edit under `~/finance/` |

---

## 2. Synthesis of the two phone docs

### A. Session-1 product verdict (architecture GO · merge NO-GO)

**Keep building:** CURRENT-as-product, propose-only Desk, thin clients, myarch keys, device role split (myarch / eME640 / LG / Fire Stick).

**Do not merge Desk product until P0:**

1. CI green (`tests/run.sh` / Actions).  
2. **No client-supplied `root`** on POST /chat; fix CORS `*`; body limit; redact absolute path from `/health`.  
3. **Honest history copy** — localStorage *and* optional `.aether/chat.jsonl` + transmission of recent turns to model.  
4. **Split branch** — Desk-only product branch from master; Kingston/VM noise out of Desk merge.

**Engineering order after P0:** propose-play artifact shape → Jellyfin/DLNA manual path → webOS SSAP last.

### B. Branch-2 / life + utility framing

- **Runway pressure:** ~£1.5k · move in ~6 weeks · insurance/car/burn dominate → survive move; no open-ended LoRA campaign as primary.  
- **Club-cortex:** still NOT-IMPLEMENTED — Domain up ≠ club up.  
- **Assets that *are* close:** Domain (CURRENT) + **client catalogue → greppable files**.  
- **Entry sales target (black flash):** £8–12k as Domain+setup, not hosted club.  
- **Spike A (research):** open-weight base ranking for ~2200 adapter segments → prefer GLM-5.x / Qwen3.5 tooling balance over pure #1 MoE.

### C. Align with already-accepted session-two split

| Track | Fits phone review? |
|-------|-------------------|
| personal-llm technique + sample quality | Support, not main money path for 6 weeks |
| Kingston VM + hardcore panel TUI | Operator tooling; keep **out of Desk merge** until product branch clean |
| Client-one Desk | Fix P0 truth/LAN then prove one proposal artifact |

---

## 3. Missing documentation jobs (should exist; mostly don’t)

| Gap | Why phone review needs it | Suggested path |
|-----|---------------------------|----------------|
| **Desk privacy & persistence policy** | History claim vs chat.jsonl + cloud context | `docs/DESK-PRIVACY-AND-HISTORY.md` or section in `domains/house-tv-desk/README.md` |
| **Desk LAN threat model (alpha)** | `--lan`, no token, CORS, fixed root | `docs/DESK-LAN-ALPHA.md` |
| **Merge gate checklist** | P0 list is operational product | `domains/house-tv-desk/MERGE-GATE.md` |
| **Proposal artifact convention** | preview→accept without tools | `docs/PROPOSE-ARTIFACTS.md` + example under `domains/house-tv-desk/.aether/proposals/` |
| **Authority revision / hash display** | bind proposals to CURRENT revision | short section in PROPOSE-ARTIFACTS or desk README |
| **Greppable client catalogue schema** | “snowball” inventory | `~/clients/README.md` + per-client `PROFILE.md` template (need/budget/friction/Domain-up-meaning) |
| **Clean product branch recipe** | 91-file contamination | `dev/11_aether-desk-android-tv/EXTRACT-DESK-PRODUCT-BRANCH.md` |
| **CI failure log capture** | red Actions without detail | `docs/CI-DESK.md` or note in MERGE-GATE |
| **6-week operator runway note** | finance + product coupling | finance already; cross-link from house-tv CURRENT Keep only |
| **Spike A base-model shortlist** | adapter research parking | `MODEL+RAG/personal-llm/artifacts/SPIKE-A-BASE-MODEL-SHORTLIST.md` (phone already has content) |

---

## 4. Proposed CURRENT changes (draft — **not applied**)

### 4.1 `domains/house-tv-desk/CURRENT.md`

**Shift from** promo `pick-a-thread-and-chat` **toward** merge-honest alpha + one sharp proof.

```markdown
**Objective:** Client-one Desk = propose-only authority surface (chat + visible CURRENT). Architecture GO; product merge blocked until P0 truth/LAN gates. Prove one inspectable proposal artifact with Client-one — not media remote, not club-cortex.
**Phase:** EXECUTE
**Status:** ACTIVE
**Baseline:** 2026-07-29 · phone 28-7-26 session-1 review absorbed as propose
**Next:** desk-p0-merge-gates
**Approval:** PENDING human apply

## Keep
- CURRENT-as-product rail + server re-read per turn
- Propose-only; no playback tools; keys on myarch
- Device roles: myarch host · eME640 light client · LG sink · Fire Stick fallback
- Honest privacy: browser transcript + what leaves device (see docs when written)

## Reject
- Desk as universal remote / media orchestrator
- Model approve / silence-as-permission
- Merging Kingston/VM scaffolding into Desk product PR
- Claiming club-cortex shipped

## Next allowed action
Execute Desk P0 merge gates (CI green; fixed STATE.root; honest history policy; CORS/body limit; health redaction; extract clean product branch notes). Pointers: phone session-1 review §P0; this file §3 missing docs. Action id: `desk-p0-merge-gates`.

## Prohibited
- model-approve · secret-in-repo · local-heavy-llm-eme640 · auto-kodi-play · start-playback · wake-lg
```

**After P0 green (later Next):** `prove-one-play-proposal-artifact` → then Jellyfin manual path research remains non-Desk.

### 4.2 `MODEL+RAG/personal-llm/CURRENT.md`

**Keep** technique + warm-up done; **add** support role under runway pressure (not open LoRA campaign).

```markdown
**Next:** support-propose-language-and-authority-patterns
# (or keep await-human-or-wire-propose-defaults)

## Next allowed action
Support Client-one / entry-sales **propose language** and cleaner authority-file patterns; optional SuperGrok research as support only. Do **not** open a full retrain campaign. Spike A base shortlist may be filed as artifact only. Action id: `support-propose-language-and-authority-patterns`.
```

Park “ignore compute” frontier base training as research note, not Next.

### 4.3 `MODEL+RAG/rag-archive-manager/CURRENT.md`

**Keep** VM-on-host + hardcore panel TUI as operator path; **explicit fence:** panel work must not contaminate Desk product branch merge.

```markdown
## Keep (add)
- Operator panel/TUI and Kingston VM stay on **operator tooling** track; Desk product branch extraction remains separate (session-1 review)

## Next allowed action
(unchanged intent) `implement-operator-panel-v0` — hardcore aether panel for daily use; document isolation from Desk merge PR.
```

### 4.4 Optional new CURRENT field set: greppable clients

Not a full CURRENT replace — **new Next** on a tiny project or mechanicall `domains/client-catalogue/` later:

```markdown
**Next:** client-catalogue-grep-schema
**Objective:** Make journaled clients cat/grep-able (need, friction, budget band, Domain-up meaning) for Domain+setup entry conversations — not club-cortex.
```

---

## 5. What I will *not* do until you say “apply” / “switch”

- Rewrite live CURRENT.md files  
- Switch git branch to “today’s client session”  
- Start Desk P0 code fixes on the wrong branch without your call  
- Expand LoRA train as primary work  

---

## 6. Finance

Life narrative paragraph for the finance agent space: edited under `~/finance/` (PROMPT + short context file) in the same turn as this review — **not** mixed into Client CURRENT.

---

## 7. Your review checklist

- [ ] House-tv CURRENT → `desk-p0-merge-gates` OK?  
- [ ] personal-llm stays support / no retrain campaign OK?  
- [ ] Panel TUI continues on rag-archive track OK?  
- [ ] Client catalogue as separate Next OK?  
- [ ] Name of **today’s client session branch** to switch to after apply?  

Reply with edits or **“apply proposals and switch to \<branch\>"**.
