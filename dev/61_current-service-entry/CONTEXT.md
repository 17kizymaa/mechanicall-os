# ICM Task Context — complete CURRENT.md draft (Layer 1 Routing)

**Doc status:** factory for this sitting. Not live law.  
**Live law:** repo-root `CURRENT.md` (uncommitted concierge rewrite).  
**Halt:** models do **not** overwrite `CURRENT.md`. Models do **not** `aether approve` / `aether next`.

Folder structure = the agent architecture.
Markdown files = skills, contracts, context.
Python = behaviours.
Single agent orchestrates by reading the structure.

## Pipeline

- **01_analyze:** Grill + facts. Frontier rounds. Persist Y-series in repo `decision-tree.md`. Output: `FACTS.md`, `ROUND-NN.md`. **This stage is live.**
- **02_plan:** After grill frontier is empty **and** human confirms shared understanding: write `.aether/proposals/CURRENT-proposal-YYYYMMDD-HHMM.md` (propose-current). Not apply.
- **03_implement:** `publish-pilot-page` on APPROVED. Door + tickets on anphuni.com-repo. Look PNGs in `03_implement/output/`.
- **04_verify:** Apex mint/drop. Receive was Render `src/data`, not Kingston.
- **05_review:** Parked.
- **06_os-cycle:** Live Next `you-decide-os-cycle`. Durable store in `inbox/tickets/`. Pull live drop. Zip + receipt + NOT ACTIVE proposal. Do not overwrite CURRENT.

## How to run

1. Answer the grill round in chat (or edit `01_analyze/output/ROUND-01.md`).
2. Agent updates `decision-tree.md` + next ROUND, then waits.
3. When frontier is empty, human says **proceed to 02_plan** to get a proposal file.
4. Human applies CURRENT (or `/mechanicall-domain:approve` then paste). Silence is never permission.

## Law this factory honours

- One Next. Dual-Next Reject.
- Models never approve. Silence ≠ permission.
- Draft / proposal is NOT ACTIVE until Yes.
- Header `**Next:**` and body `**Action id:**` must match after apply.
- PRODUCT.md: anphuni.com Session is not Mechanicall **core protocol**. A Domain CURRENT may still authorize a service instance; that is this grill.
