# CURRENT proposal — 2026-08-31T18:17Z

**Not law. Not Yes.** Live `CURRENT.md` stays until a **human** applies this file.  
**APPLY: human must approve then merge — model must not overwrite CURRENT without human gate.**

Source of intent: `.aether/events.jsonl` reject `2026-08-31T17:59:12.461Z` (`by:human`, phase SELECT).  
Toy body (not law): `examples/propose-current/CURRENT-listing-bar-pin.md`  
Unified diff: `.aether/proposals/CURRENT-proposal-20260831-1817.diff`  
Off-root schema: `aether current validate /tmp/listing-bar-pin-pwzJ` → **VALIDATE: OK** · Next `listing-bar-pin`

### Continue clock (2026-08-31T18:43Z) — applied this sitting

Human `aether next listing-bar-pin` then approve. Preflight **allowed**. Operator `CURRENT.md` body applied from this offer (header Next kept; Phase set EXECUTE so header/body match). Toy example left as the draft. Model did not `aether next` / `approve`.

**Halt** on the pin. Following ids still not live.

### Continue clock (2026-08-31T18:34Z) — superseded (do not apply *was* the gate)

Two clocks after this propose:

| Surface | State |
|---------|--------|
| events.jsonl | reject 17:59Z, then **approve** 18:33:26Z reason `speech ≠ listing; park MCP; UI other pocket; Headscale following; idkr unnamed` |
| live CURRENT.md | **Next still `aether-mcp-projection`** · Phase APPROVE · Status APPROVED · Approval APPROVED |
| `aether preflight listing-bar-pin` | **refused** (not the next allowed action) |
| `aether preflight aether-mcp-projection` | allowed on the pin — **do not take as permission to ship MCP**; the approve *reason* parks it |

`aether approve` flipped the header off REJECTED **without** `aether next listing-bar-pin` and **without** pasting this body. Models do not hand-edit `**Next:**`. Models do not apply this file while preflight refuses.

Missing human verb:

```bash
aether next listing-bar-pin
# then paste examples/propose-current/CURRENT-listing-bar-pin.md onto CURRENT.md
# (or say apply after Next matches)
```

Do **not** `aether next` from a model. Do **not** execute `aether-mcp-projection` default-on.

---

## Observations

- Speech teased `mechanicall-pocket`. Human then **rejected** the live Next. Reason: before Play listing, (1) UI fully executed, (2) Headscale up and operable, (3) UI fully executed again, (4) `idkr`.
- MCP spike is **already Done**: `python/aether_mcp.py` + `tests/test_aether_mcp.py`; tools `current` / `probe` / `propose_write` only; not default-on. CURRENT already said Halt for human opt-in.
- Live law still **Rejects** `Play production listing this Next` and parks **Mesh / doorbell / Funnel** later than this pin.
- sit-ui-sprint (`/home/anphuni/sit-ui-sprint`) already has its own CURRENT: Next `discuss-sit-ui` APPROVED. That pocket **Rejects** Headscale / Play / Funnel. Operator CURRENT **Rejects** child-current-as-operator-law.
- Item 4 is unnamed. Do not invent a fourth Next to fill `idkr`.

## Inferences

- The reject is a **listing bar**, not “MCP is wrong,” not “list on Play now,” not “do UI and Headscale as one operator Next.”
- Sequential ≠ dual-Next. One live action-id in **this** file. sit-ui-sprint may keep its own Next; that is the existing two-pocket split, not dual-Next here.
- Recanting “mesh later” into live `sit-headscale-operable` is a **different** human pick (revise option below). This propose does not sneak that recant.

## Unknowns

- What “UI fully executed” means vs SitRackView already on A33 `0.18.1-storage` (PR #8) vs sit-ui-sprint freeze (CRT-only / title / painted-button).
- Whether Headscale-operable recants mesh-later **now**, or stays a following id.
- What item 4 `idkr` is.

## Proposed change (summary)

1. **Park** `aether-mcp-projection`. Spike stays in Done. Not default-on. Not this Next.
2. **One new Next:** `listing-bar-pin` — absorb the reject into operator law; halt.
3. **Encode the listing bar** in Keep / Limits / Reject: speech ≠ listing; production listing still Reject; closed testers not this Next either until the bar is honest.
4. **UI finish** stays the **other pocket** (`discuss-sit-ui`). Do not rewrite sit-ui-sprint CURRENT from this tree.
5. **Headscale** named as **following** action-id `sit-headscale-operable` (human re-SELECT later). Doorbell / Funnel still later. Mesh is not live.
6. **Do not recant** SitRackView host, leftover-compose-delete, PR rubric, ICM factory, local-first, models-never-approve.

## Fidelity checklist

- [x] Still **one** Next (`listing-bar-pin`)
- [x] Models never approve / never auto-write CURRENT
- [x] No secrets
- [x] Silence ≠ permission
- [x] Following ids named, not live (`sit-headscale-operable`; sit-ui-sprint remains other pocket)
- [x] MCP tools still not named `approve` / `next`
- [x] Play **production** listing still Reject
- [x] child-current-as-operator-law still Reject
- [x] `idkr` not filled with a fake fourth Next
- [x] Offers stay in `.aether/proposals/` until human action

## Conflicts with existing authority

- Live Next `aether-mcp-projection` — this propose **replaces** that pin (human already rejected it).
- Limits “Mesh / doorbell / Funnel stay later than this pin” — **kept** for this pin. Headscale is named as following, not unparked.
- sit-ui-sprint APPROVED `discuss-sit-ui` — **untouched**. UI-executed is their sitting.
- PRODUCT: sit is lab face, not a second product; Play production is not core. This propose aligns.

## Before → after (header)

| Field | Live | Proposed |
|-------|------|----------|
| Objective | literary-eval into law; SitRackView host; restore pin | Absorb 2026-08-31 reject: speech ≠ Play listing. Park MCP. Listing bar named. SitRackView stands. |
| Phase / Status / Approval | was SELECT/REJECTED; now APPROVE/APPROVED on the **MCP** pin | SELECT / DRAFT / PENDING on `listing-bar-pin` until `aether next` + body apply |
| Baseline | 2026-08-28 take-forward | 2026-08-31 reject + MCP spike Done + sit-ui-sprint `discuss-sit-ui` other pocket |
| Next | `aether-mcp-projection` | `listing-bar-pin` |
| This Next | MCP opt-in / park | Apply this pin. Halt. Do not list. Do not unpark mesh. Do not default-on MCP. |

## Human decision required

- [x] Approve reason recorded `2026-08-31T18:33:26Z` (listing-bar prose) — **landed on the MCP pin**
- [ ] **`aether next listing-bar-pin`** — missing; preflight refuses until this
- [ ] Apply toy body `examples/propose-current/CURRENT-listing-bar-pin.md` as live `CURRENT.md` **after** Next matches
- [ ] **Revise A** — make `sit-headscale-operable` the live Next (explicit recant of mesh-later; UI still other pocket; still not Play production)
- [ ] **Revise B** — work only in sit-ui-sprint; leave this operator file parked until you name a Next here
- [ ] **Revise C** — name item 4 `idkr` before applying anything
- [ ] Leave live CURRENT as APPROVED `aether-mcp-projection` (contradicts the 18:33 reason)

**Do not** run `aether approve` / `aether next` / `aether reject` from a model.  
**Do not** add MCP to a default client config.  
**Do not** open the dirty tree as a PR.  
**Do not** treat USB look as an LTE / testers receipt.

---

## Proposed CURRENT.md (paste)

```markdown
# CURRENT

**Objective:** Absorb the 2026-08-31 reject into operator law: a speech teasing mechanicall-pocket is not a Play listing. Park the aether MCP spike. Name the listing bar (UI executed in the sit-ui-sprint pocket; Headscale operable as a following id here; item 4 still unnamed). SitRackView stays the freeze host. Not a recant of the sit or of ICM.
**Phase:** SELECT
**Status:** DRAFT
**Baseline:** 2026-08-31 · human reject of aether-mcp-projection · MCP spike on disk not default-on · leftover Compose millwork deleted · PR #8 SitRackView · A33 0.18.1-storage · sit-ui-sprint Next discuss-sit-ui (other pocket)
**Next:** listing-bar-pin
**Approval:** PENDING
**Host:** myarch · A33 lab USB via mbp-edge (USB ≠ LTE)

## Product (non-negotiable identity)
- **Is:** local-first authority protocol. Inference is not authority. You decide. AI does the point-and-clicking — under a plan you can `cat` and a yes only you can give. The **phone sit** is the lab face of that protocol, not a second product.
- **This Next:** `listing-bar-pin` — write the reject as Limits/Keep/Reject; park MCP; halt. Not Play upload. Not Headscale bring-up. Not sit-ui freeze (other pocket). Not MCP default-on.
- **Not core:** EdubaWare-clone, hosted multiplayer ICM, meeting-as-chat as the product, MCP-as-core, Play production, Funnel, dual-Next, model Yes.

## Done (keep)
- Zip contain (`_zip_member_unsafe`) · stock-phone `pocket_approve` / native `yes()` · API 36 pack (PR #7 merge; still **not** distribution)
- SitRackView host on HEAD and A33 `0.18.1-storage` (PR #8) — one `View`, one CBitmap, CRect hits, LCD clipped to glass
- Lab APK archive/rollback (`scripts/sit-apk-*.sh`)
- PR rubric + scorer: `dev/47_literary-pr-eval/02_eval/output/PR-RUBRIC.md` · `03_pr-rubric-as-check/`
- Literary file ingested: phone `14_PROPOSED-LITERARY-DIFFS-GPT-56.txt` (copy, not a new SPEC)
- leftover Compose millwork deleted (`SeatNav` / `SeatTheme` / `LcdViewer` / `SkinLayout` / `modules/*`); Compose off `build.gradle.kts`
- aether MCP spike: `python/aether_mcp.py` (`current` / `probe` / `propose_write`); tests `tests/test_aether_mcp.py`; **parked**; **not** default-on

## Keep
- One Next; models never approve; silence ≠ permission
- Bind / Send / JOIN / WAKE / LOAD / STREAM / twin / inbox / FILES / opening the app are **not** Decide
- Phone bind ≠ this operator repo
- Freeze host = **SitRackView** (native blit + `Matrix` + pack CRects). Compose forbidden on millwork **and** paper
- Walk: Bind → Plan → Draft → Decide+Why → Receipt. PROPOSE stays off live CURRENT until human action. Offers skip `CURRENT.md`. Empty receipts stay empty
- Imagine = paint, not spec. M2=1 / M7=1 stand
- ICM numbered `dev/` = **factory**. Mechanicall CURRENT = **gate**. Do not collapse them
- Literary `14` = PRODUCT-adjacent **copy** (glass / README / pitch). Not a recant of sit, ICM, or local-first
- PR center test: does this change make authority more inspectable, or does it make a capability look like consent? Score with `PR-RUBRIC.md` before calling anything distribution
- `tests/run.sh` as CI; Android assemble job is a FLAG not this Next
- USB-on-mbp-edge is not LTE. NeuralBridge capture is lab
- Personal LLM = propose/taste only
- Two pockets: this file is operator law; sit-ui-sprint CURRENT is face law. Not dual-Next in either file
- Listing bar (from 2026-08-31 reject): a tease of the APK is not a store listing. Before any Play listing: UI executed (sit-ui-sprint), Headscale operable (following id here), item 4 named by a human. Closed testers remain the honest ceiling until that bar is real

## Reject
- dual-concurrent-next
- leftover-compose-millwork-as-sos
- LcdViewer/SkinLayout overlay host returning as millwork
- Imagine-as-spec
- Camel PNG theft
- model-auto-approve / model-auto-write-current
- proposal-as-CURRENT shipped in a PR (B4)
- events.jsonl / tests stamped `by:human` as if they were judgment (B1)
- clone-edubaware-as-core
- meeting-becomes-the-chat as Mechanicall product
- MCP tools named `approve` / `next`
- Funnel / public wake / public Ollama
- Play **production** listing this Next
- speech-tease-as-listing-go
- USB look sold as testers/LTE receipt
- bind-phone-to-operator-tree
- child-current-as-operator-law (sit-ui-sprint CURRENT is not this file)
- recant-sit-because-the-essay-is-prettier
- recant-ICM-out-of-this-repo
- mcp-default-on-this-next
- ui-and-headscale-as-one-next

## Limits
- Closed testers / lab sideload — not release
- No secrets in git
- Do not rewrite a bound client CURRENT from this tree
- Grouped git exclude live CURRENT unless human Go-git
- Dirty tree: **do not open as a PR**. Leave out events.jsonl, this CURRENT until Go-git, storm dumps, overlay `sit_*.png` until sit-ui freeze Go, Compose overlay files unless the PR is a **delete**
- sit-ui-sprint (`/home/anphuni/sit-ui-sprint`) owns CRT-only / MECHANICALL title / painted-button recant. Next there: `discuss-sit-ui`. That is where “UI fully executed” is decided. Not this Next
- EdubaWare org-MCP: **look** (scope + draft-not-apply + zip carry). Local `aether` projection spike is **Done and parked**. Never `approve`/`next` tools. Not an EdubaWare clone
- Cooperative gate (ALPHA-LIMITATIONS): preflight refuses when consulted; it is not a jail
- Mesh / doorbell / Funnel stay later than this pin. Following action-id (not live): `sit-headscale-operable`. Doorbell / Funnel not even following until named
- Item 4 of the 2026-08-31 reject (`idkr`) is unnamed. Do not fill it from a model
- Do not assemble overlay-Compose sit. Native host already on device; leftover Compose must not become the face again

## Next allowed action
**Action id:** `listing-bar-pin`

1. Human applies this file as `CURRENT.md` (this proposal is not law until then).
2. leftover-compose-delete and aether-mcp-projection spike are **done**. MCP stays parked. Agents do not add a default MCP config.
3. **Halt.** Do not Play-upload. Do not unpark Headscale. Do not rewrite sit-ui-sprint CURRENT. Do not assemble overlay-Compose.
4. After this pin is live: human works the other pocket, or `aether next sit-headscale-operable`, or names `idkr`. Models do not re-SELECT.

## Approval condition
Human `aether next listing-bar-pin` then `aether approve` with a real reason (e.g. speech ≠ listing; park MCP; UI other pocket; Headscale following). Models do not run `aether approve` / `next` / `reject`.

Silence is never permission.

## Prohibited
- automatic-approve
- commit-secrets
- dual-concurrent-next
- model-auto-write-current
- leftover-compose-millwork-as-sos
- clone-edubaware-as-core
- mcp-approve-tool
- mcp-default-on-this-next
- funnel-this-next
- play-production-this-next
- speech-tease-as-listing-go
- bind-phone-to-operator-tree
- child-current-as-operator-law
- usb-as-lte
- camel-png-theft
- imagine-as-spec
- open-dirty-tree-as-pr
- assemble-overlay-compose
- recant-sit-for-essay
- recant-icm-factory
- ui-and-headscale-as-one-next
```
