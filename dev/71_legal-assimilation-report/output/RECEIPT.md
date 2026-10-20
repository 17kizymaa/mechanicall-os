# RECEIPT — 71_legal-assimilation-report

**Action id:** `legal-assimilation-report`
**When:** 2026-09-19
**Preflight:** allowed (`Phase=APPROVE Status=APPROVED`, 11:36)
**Instance:** tool (`mechanicall-os`). Research artifact. **Not legal advice.**

## Also done this session (from the earlier "Go")
- Opened **PR #13** `feat/share-urls-readiness → master` — https://github.com/17kizymaa/mechanicall-os/pull/13 — for the kit commit `c94247a`. Note the branch carries earlier unmerged commits too (553 files vs master), not just the kit.

## Done
1. `CONTEXT.md` — stage contract; question fixed to the 07:52 approval reason (E&W, sole trader, £1k income + £4k savings before Jan).
2. Probed Onyx read-only (`/api/health` 200; DB: 1 user `anphuni@…`, LLM provider `openrouter`, **0 connectors, 0 documents**; `AUTH_TYPE=basic`). No credentials given → **not used for retrieval**. Nothing written to Onyx.
3. Checked site/protocol facts on disk (privacy page, contact page, `render.yaml`, paper trader source, room storage, INTAKE kit, LICENSE).
4. `output/LEGAL-ASSIMILATION-REPORT.md` — 12 areas, each: applies? · what the protocol already mitigates · what is open · cheapest closure; consolidated verdict table; verify-list.
5. `output/ONYX-INGEST-LIST.md` — primary sources + regulator guidance + vendor DPAs + five questions to put to Onyx for the source-grounded "gold" pass.

## Headline (details in the report)
- **The protocol is not the problem** — receipts, the Yes gate, aliases and INTAKE's default-off list are the best compliance evidence you have (CRA s.50, UK GDPR art 25, art 22 non-applicability, CMA/Fraud authority records).
- **Nothing found that blocks the January targets.**
- **Red, cheap:** business-name disclosure (CA 2006 Pt 41 — your name + service address on the site); a "You Decide rooms" paragraph in `privacy.html` (controller, storage location, retention, deletion route); Render region unset → likely US → transfer route needed or move to Frankfurt.
- **Amber, only when money appears:** HMRC SA registration once gross > £1,000 in a tax year (deadline 5 Oct after year end); CCR pre-contract info + 14-day cancellation right; ICO fee ~£52; IP ownership sentence; case-study consent line.
- **Watch:** paper room is green *as built* (random prices, no stake, one room) — goes red if live prices or suggestions ever appear. Verify `YOU_DECIDE_PAPER_TICKETS` is unset on Render (kit F3).
- **Housekeeping red:** `.aether/events.jsonl` / `DECISIONS.md` carry your income figures and private remarks about relatives and are in the public repo (the 07:52 reason is in `origin`). Not illegal; not wise. Stop committing that prose; consider `git filter-repo`.
- **Unknowns I could not resolve from disk:** whether you have PAYE employment or claim Universal Credit (changes the tax/benefit picture materially); whether any alias is under 18; Render's actual region setting.

## Not done (by design)
No legal advice · nothing filed · site untouched · no Onyx login or ingest · no external sends other than the PR you asked for · no `aether approve`/`next` · no commit of this stage.

## Suggested next (yours to select)
Each red item is small enough to be one operator-side edit rather than a Next. If you want them bundled: `site-legal-footer` (name/address line + privacy paragraph + paper disclaimer + region) — site repo on disk, then you deploy.

## Suggested commit (you / your other model)
```
docs(dev): legal-assimilation-report — E&W sole-trader stress-test of anphuni × You Decide

Research artifact, not legal advice. Protocol is the mitigation; open items are
business-name disclosure, privacy notice for rooms, Render region, HMRC/ICO
once paid. Onyx ingest list for the source-grounded pass.
```
Stage only `dev/71_legal-assimilation-report/`.

## Halt
Human reads the report. Silence is never permission.
