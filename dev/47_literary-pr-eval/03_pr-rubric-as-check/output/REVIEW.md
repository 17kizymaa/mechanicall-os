# REVIEW — rubric as check (no open PR)

**When:** 2026-08-28  
**Next pin used:** `pr-rubric-as-check` (preflight allowed).  
**Not Yes.** Do not `gh pr review`. Do not `aether approve`. Do not assemble.

No GitHub PR is open. This sitting scored:

| Target | What it is | Mechanical verdict | Judged verdict |
|--------|------------|--------------------|----------------|
| PR **#8** (merged) | SitRackView host + lab archive | blocker (B2/B3 false positives) | **lab-ok** (already merged; do not treat as distribution) |
| PR **#7** (merged) | testers sit + zip contain + native Publish + API 36 | not-distribution (B4 CURRENT.md) | **lab-ok after the distro fixes; still not distribution** (GPT-56 `13` was right at `70a4c8e`; merge included contain + native yes) |
| **dirty tree** (would-be PR) | 97 porcelain paths on `feat/sit-rack-lab` | blocker B1/B3/B4 | **do not open as-is** |

Script: `03_pr-rubric-as-check/scripts/score_pr.py`. JSON: `score-pr8.json` `score-pr7.json` `score-dirty.json`.

Center test (unchanged): **Does this change make authority more inspectable, or does it make a capability look like consent?**

---

## Pin note (before the scores)

Operator `CURRENT.md` is still a proposal overlay. Header now has `**Next:** pr-rubric-as-check`. Body still says keep **Next `sit-mvp-rack`**. `aether probe sit-mvp-rack` **REFUSE**. Schema still FAIL (no Objective/Keep/Reject/Limits).

That is B4 on the *operator tree itself*: a proposal is sitting in the law slot, and the header Next was used to route this factory. Cold-start docs say stop when header and body disagree. This stage honoured the **header** because the human said Continue and preflight allowed it. It did **not** recant SitRackView or assemble sit.

Human still owes one apply: restore a schema-valid CURRENT (sit-mvp-rack or a real new Next) **or** keep research Next but write the full sections. Silence is not that apply.

---

## PR #8 — judged **lab-ok** (merged)

Mechanical FAIL B2/B3 are greps against *this* diff only:

- B2: `FaceBridge.yes` appears in `MainActivity.kt`. Native `pocket_approve` already shipped in #7 and is not in the #8 file list. **Judged PASS.**
- B3: no inbox unzip in #8. **Judged N/A.**
- B5 mechanical PASS because the PR *body* mentions `assembleDebug`. CI (`.github/workflows/test.yml`) still has no Android job. **Judged FLAG**, not a blocker for a lab host recant.

Judged table:

| # | Score | Note |
|---|-------|------|
| B1 | PASS | No events.jsonl; tests not looping approve on ROOT |
| B2 | PASS | Decide still `FaceBridge.yes` → Chaquopy `pocket_approve` (no POSIX `aether`) |
| B3 | N/A | Transport not in this PR |
| B4 | PASS | Live CURRENT excluded; three files under `.aether/proposals/` |
| B5 | FLAG | Local assemble claimed; CI still `tests/run.sh` + control-layer |
| B6 | PASS | USB look/sideload; copy says USB ≠ LTE |
| S1 | PASS | One host (`SitRackView`) + `sit-apk-rollback.sh` |
| S2 | PASS | Opening the app is not Yes |
| S5 | PASS | Leftover Compose modules **not** in the PR (they remain in tree) |
| S6 | PASS | 41 paths; rollback named |

**Preserve:** native blit + CRect + LCD clip; lab archive before overwrite; proposals not law.

**Not authorized to be:** production, Play, LTE, Yes.

**Leftover honesty:** #8 left Compose modules (`SeatNav`, `ChatHome`, …) in the repo. That is why the dirty tree can still look like a second host. S5 pass on the PR ≠ S5 pass on HEAD+dirty.

---

## PR #7 — judged **not-distribution**, merge-as-lab understandable

GPT-56 `13` said NO at head `70a4c8e`. Merged head `af452f2` / merge `b2bf1c4` **did** land zip contain (`_zip_member_unsafe`) and native `yes()` / `pocket_approve`. Mechanical B2/B3 PASS on the merge range is that later work.

Still not a distribution:

| # | Score | Note |
|---|-------|------|
| B4 | FAIL | Operator `CURRENT.md` is in the merge diff (+67/−45). Seed `CURRENT.md` under storm output / pocket-demo-client are *client* templates — those are OK. Operator law in the PR is the real miss. |
| B5 | FLAG | Play-listing pack and API 36 are in-tree; CI still does not assemble APK/AAB |
| B6 | PASS as disclaimer | USB ≠ LTE language exists; LTE receipt still BLOCKED in `dev/42` |
| S5 | FAIL *as host* | Compose millwork was the testers face. Recanted later by #8, not by #7 |
| S6 | FAIL | 676 paths — GPT-56 breadth objection still true |

**Preserve:** walk (Bind → Plan → Draft → Decide+Why → Receipt); offers skip CURRENT; bind ≠ operator repo; native Publish; zip contain.

**Do not cite #7 as “the distribution.”** Closed testers / lab only.

---

## Dirty tree — judged **do not open as-is**

97 porcelain paths. If this became PR #9 tomorrow, the rubric would refuse it as a product PR and as a honest lab PR until packed.

### Mechanical vs judged

| # | Mechanical | Judged | Why |
|---|------------|--------|-----|
| B1 | FAIL | **FAIL** | `.aether/events.jsonl` is modified. Do not ship the doorbell log as a PR. |
| B2 | N/A | N/A | Decide path not in the dirty set (already on HEAD). |
| B3 | FAIL | **N/A** | False positive: `ZipFile` string in `dev/42_sit-distro-gate/CONTEXT.md`, not an extractor. |
| B4 | FAIL | **FAIL** | Live `CURRENT.md` overlay in the working tree. A PR that adds this file ships a proposal as law. |
| S5 | FAIL | **FAIL** | Dirty/untracked leftover Compose: `SeatNav.kt`, `ChatHome.kt`, `PlanModule.kt`, **`LcdViewer.kt`**, **`SkinLayout.kt`**. That is the freeze-host #8 recanted. |
| S6 | PASS (14 < 20 storm paths) | **FLAG** | 14 storm dumps + overlay `sit_*.png` (abcd, lamps, plan_keep, crt, chassis, …) are lab diary, not testers install. |

### Packing list for a *next* lab PR (human Go)

**Leave out**

- `CURRENT.md` — keep as local overlay or move text to `.aether/proposals/`
- `.aether/events.jsonl`
- `.context.md`, `.continue-here.md` unless you mean them as docs
- `dev/39/**/storm-0/` `storm-1/` PNG/XML dumps
- Untracked overlay plates (`sit_abcd.png`, `sit_lamp_*.png`, `sit_plan_*.png`, `sit_crt.png`, …) until sit-ui-sprint freeze **Go**
- `LcdViewer.kt` / `SkinLayout.kt` as *new* host files — they are the failed Compose overlay unless the PR is a **delete**
- EdubaWare / MCP implementation

**Candidate include (each still needs a reason)**

- `tests/run.sh` authority snap (GPT-56 `10_` hygiene) — lab-ok if that is the whole PR
- Delete leftover Compose modules *if* SitRackView is the only host (align dirty tree with #8 claim)
- `dev/47_literary-pr-eval/` as research receipts — optional, not product
- sit-ui-sprint plates freeze **only after** that pocket’s PENDING recant (CRT-only, MECHANICALL, painted buttons)

Until CURRENT schema is valid, **any** GitHub PR should say in the body: live CURRENT is local; this PR does not authorize Next.

---

## Two pockets — what the rubric says to take forward

Operator (`mechanicall-os`, this tree)

1. Do not open the dirty tree. Pack or discard.
2. Restore a pin that `aether current validate` accepts. Header/body must match.
3. Future PRs: one artifact (host, contain, CI assemble, events provenance) — not 97 paths.
4. MCP stays out. Optional later projection of `current`/`probe`/`propose.write` is a different Next.

Sit-ui-sprint (`/home/anphuni/sit-ui-sprint`)

1. Face law is still `discuss-sit-ui`. CRT recant is still PENDING.
2. Overlay PNGs appearing as untracked files **in mechanicall-os `drawable-nodpi/`** are the wrong pocket until freeze Go. They look like a second host (S5) if committed here.
3. Literary copy belongs on STATUS glass after Imagine halt, not as operator CURRENT.

Dual-Next remains Reject. Do not apply both pins in one sitting.

---

## How to run this check next time

```bash
# from mechanicall-os
python3 dev/47_literary-pr-eval/03_pr-rubric-as-check/scripts/score_pr.py --root . --pr N
python3 dev/47_literary-pr-eval/03_pr-rubric-as-check/scripts/score_pr.py --root . --dirty
```

Then write the judged overlay (this file’s job). Mechanical FAIL is a signal. Do not merge from JSON alone. Do not post from a model unless the human asks to paste.

Script false positives to remember: ZipFile in markdown; FaceBridge.yes without pocket.py in the same diff; CURRENT.md in *seed* pockets vs operator root; assemble mentioned in a PR body vs CI.

---

## Comment template (when an open PR exists)

1. One line: lab-ok / not-distribution / blocker.
2. Blockers with path.
3. Walk to preserve.
4. What it is not (production, LTE, Yes).
