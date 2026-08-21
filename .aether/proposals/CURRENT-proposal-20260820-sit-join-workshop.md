# Proposed CURRENT update (draft — not authority)

**Project:** mechanicall-os (operator tree)  
**Date:** 2026-08-20  
**Author:** grill S1–S13 + human “propose this as CURRENT.md” / “Go!” (propose only)

`APPLY:` human must approve then merge — model must not overwrite CURRENT without human gate.

## Summary

Replace live Next `ACTUAL-APP-VERIFICATION` (APPROVED; body Action id still `mechanicall-debug-window`) with **one** Next `sit-join-workshop`: stranger-as-themselves **userspace Tailscale in the APK**, **WAKE** via wol-pi, **document workshop** (Plan = published CURRENT.md, Draft = Suggesting on PROPOSE, Decide publishes), **hunk-scoped 7B+LoRA ICM**. Not four Nexts. Not a VST product. Not Play Store.

Replacement body: `examples/propose-current/CURRENT-sit-join-workshop.md`  
Grill (closed): `decision-tree.md`

## Observations

- Live CURRENT: Next `ACTUAL-APP-VERIFICATION`, Phase APPROVE, Status APPROVED, Approval APPROVED. `aether current validate`: OK with warning that Phase/Status/Approval are all APPROVE(D) — prefer a **new Next**.
- Body **Action id** still `mechanicall-debug-window` (header/body drift). Agents did not silently rewrite.
- Closed grill S1–S13: document chrome now; Camel Space later; recant S2 (embed Tailscale, userspace); no pocket share; hunk ICM + schema auto-complete on PROPOSE; grouped git exclude CURRENT.
- S6 had been “stay under ACTUAL-APP-VERIFICATION as lab” (user override). Operator 2026-08-20: **propose this as CURRENT.md so we can execute under a single NEXT. Go!**
- Last-pass APK can score B3/B4 mechanically and still fail as a workshop (human). Painted VST remains a UI-fail.
- 18 August: Tailscale-as-me is not a send path. `kamilas-tab` as `17kizymaa@` is not a stranger.

## Inferences

- Keeping `ACTUAL-APP-VERIFICATION` as Next while shipping join+workshop is the same class of lie as header/body Action-id drift. One new id is the honest single Next.
- Join, wake, paper workshop, and 7B hunk ICM are **one sit**, not extra Nexts (Reject: splitting).
- Research-first (S8) is clause 1 of the Next allowed action, not a second law.

## Unknowns

- Human apply path: copy file vs `aether next sit-join-workshop` after copy.
- libtailscale Android userspace artifact availability (research).
- wol-pi HTTP not in tree yet (MAC/token off git).

## Proposed CURRENT change

Apply the full file `examples/propose-current/CURRENT-sit-join-workshop.md` as root `CURRENT.md`.

Field extract:

```markdown
**Objective:** One sit: a stranger joins the tailnet **as themselves** (userspace Tailscale in the APK), wakes myarch, and works a **document workshop** — Plan is published `CURRENT.md`, Draft is Suggesting on a PROPOSE copy of that whole file, Decide publishes. Desk is a 7B+LoRA on hunk-scoped ICM. Same law: pocket folder, human Yes. Not Play Store. Not four Nexts.
**Phase:** SELECT
**Status:** DRAFT
**Baseline:** 2026-08-20 · ACTUAL-APP-VERIFICATION (mechanical 10/10 last-pass; VST chrome still a UI-fail; Draft not a workshop; Tailscale-as-me still not a send path)
**Next:** sit-join-workshop
**Approval:** PENDING
**Host:** myarch · anyone can boot this desk to run `personal-llm-sft-v4` (7B + active LoRA)
```

**Action id:** `sit-join-workshop`

## Conflicts with existing authority

- Live Next `ACTUAL-APP-VERIFICATION` APPROVED vs this SELECT/DRAFT/`sit-join-workshop`.
- Body Action id `mechanicall-debug-window` vs both header Next and this proposal.
- CURRENT “This Next” still names Camel Space–vibes debug plugin; S9 moved that to a **later settings reskin**.
- S6 in `decision-tree.md` said stay under verification as lab — **recanted** by this human request.
- Reject still says splitting desk-hop/storm/window — this Next **keeps** one-Next discipline, new contents.

## Fidelity checklist

- [x] still one Next
- [x] models never approve
- [x] no secrets
- [x] silence ≠ permission
- [x] JOIN / WAKE / SEND / hunk-accept ≠ Decide
- [x] phone bind ≠ this repo
- [x] dual-concurrent-next still Reject

## Human decision required

- [ ] Apply `examples/propose-current/CURRENT-sit-join-workshop.md` over root `CURRENT.md`
- [ ] `aether next sit-join-workshop --reason "one sit: join + wake + document workshop"`
- [ ] `aether approve "…" ` with a real reason
- [ ] Reject and leave CURRENT unchanged
- [ ] Revise and re-propose

**Do not** run `aether approve` / `aether next` from a model or agent.

Human apply sketch (you run these):

```bash
cp examples/propose-current/CURRENT-sit-join-workshop.md CURRENT.md
aether current validate
aether next sit-join-workshop --reason "one sit: join + wake + document workshop"
aether approve "one sit: stranger join (userspace) + wake + document workshop under hunk ICM"
aether preflight sit-join-workshop
```
