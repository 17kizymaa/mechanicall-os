# RECEIPT — 70_share-urls-kit

**Action id:** `share-urls-kit`
**When:** 2026-09-19
**Preflight:** allowed (`Phase=APPROVE Status=APPROVED`, event 10:32)
**Instance:** tool (`mechanicall-os`). Nothing written under `~/anphuni-project`, `~/clients`, or `~/sites/anphuni.com-repo`.
**Human confirmations this run:** build kit first, legal report as a later Next (A); FLAG-only for the site face; gitignore `.aether/proposals/clients/`.

## Done (this repo only)

1. **`templates/alias/`** — `POINTER.md`, `INTAKE.md`, `NOTES.md`, `OPENER.md`. Placeholders are `{alias}` and `{date}` only.
   - `OPENER.md` = the six hello-grammar lines from CURRENT §"What I want now", verbatim, framed by "Replying is hello. Nothing is decided until you say so." No technical questions. No "aether", "CURRENT", or "Yes" as a term.
   - `INTAKE.md` mirrors the five questions with empty `>` answer slots, plus a **never without asking** checklist (six items, all ticked by default) that maps to the tool's `agent-publish-delete-spend-message-deploy` prohibition. Header: their words verbatim, no identity, append-only.
   - `NOTES.md` has a **Limits** section — where I write what they said, they never stamp.
   - `POINTER.md` uses the same table shape as the live roster; `Room id` row starts as `unminted`.
2. **`scripts/alias-scaffold.sh <alias> [--root DIR] [--templates DIR] [--dry-run]`** — POSIX sh, shellcheck clean.
   - Creates `projects/<alias>/{POINTER.md,INTAKE.md,NOTES.md,MATERIAL,PROPOSALS/OPENER.md,DELIVERED,RECEIPTS}`.
   - Idempotent: second run prints `keep` for every path, writes nothing (tested).
   - Refuses alias not matching `[a-z0-9-]+`, refuses `current`, refuses to write any `CURRENT.md`, FLAGs if a client `CURRENT.md` already exists.
   - Tested only against `/tmp/opencode/kit` (fixture alias `amber-window`). **Not run on the live roster.**
3. **`scripts/alias-links.py [--root DIR] [--base URL] [--out FILE] [--json]`** — read-only.
   - Parses `| Room id | \`<32-hex>\` |` (falls back to any 32-hex in the POINTER); prints `unminted` when absent.
   - Columns: alias · room URL · status · opener · intake. FLAGS section for missing POINTER, missing kit opener, or a client `CURRENT.md`.
   - Refuses `--out` inside `projects/`. Paper allow-list is the one hard-coded id CURRENT permits.
   - Ran read-only against the live roster → `output/LINKS-dryrun-2026-09-19.md`.
4. **Site face check** on disk, `~/sites/anphuni.com-repo` @ `e99af1c` — see FLAGS. Nothing patched. Nothing deployed.
5. **`.gitignore`** += `.aether/proposals/clients/` (Mum draft reply, birthday paper-book). Verified with `git check-ignore`.

## Evidence from the read-only roster scan (2026-09-19)

- 17/17 aliases minted. `happy-birthday` is the only Paper owner (matches `DEFAULT_PAPER_TICKETS`).
- **0/17 have a kit opener on disk** (`PROPOSALS/OPENER.md`); 2 mention an opener in the POINTER only.
- **0/17 have an INTAKE answer.** Nobody has replied yet — or replies haven't been pasted.
- No client `CURRENT.md` anywhere in `projects/`. Good.

## FLAGS

**F1 — the opener cannot reach the visitor face as the code stands (two independent gaps).**
- Server: `lib/you-decide.mjs:282` `seedFromPropose()` only regex-matches `hi anthony` inside `propose.md` and injects that phrase as a message *from them*. The kit opener contains no such phrase → seeds nothing. It also only runs when `messages.jsonl` does not yet exist.
- Client: `public/assets/you-decide-ticket.js` renders `j.messages` and `j.paper`; it never renders `j.propose`. So even a correct `propose.md` is invisible.
- Consequence: CURRENT's premise "one `propose.md` per alias that seeds the thread" is **not true** of the deployed code. Wave-1's PUT of `NOT ACTIVE. Not the plan. Not Yes.` to 16 rooms was inert for the same reason (its receipt already noted "cosmetically inert").
- Options for a later Next (yours): (a) make `seedFromPropose` emit the opener as an operator message when `propose.md` is non-default; (b) have the operator post the opener as an ordinary first chat message via the existing operator auth; (c) render `propose` on the ticket page. (b) needs no deploy. All need your Yes — external write.

**F2 — wave-1 seeded the wrong text.** 16 rooms hold `# {alias} — proposed CURRENT (draft — not authority)\n\nNOT ACTIVE. Not the plan. Not Yes.` — the old `DEFAULT_PROPOSE` shape, not hello grammar. Re-seeding with `templates/alias/OPENER.md` is the operator Next with your Yes (it is a PUT to apex).

**F3 — paper gate holds on disk; env not verified.** `DEFAULT_PAPER_TICKETS` = birthday only; `serve.mjs:680` routes only that id to the desk; `ticket.js setChatOnly()` hides the dock for everyone else. `paperTicketIds()` also reads `YOU_DECIDE_PAPER_TICKETS` from env — I did not check Render's env (no external reads this halt). If that var is set on Render, someone inherits Paper. Worth one glance in the Render dashboard.

**F4 — chat-only default holds.** Non-paper ids → `you-decide-ticket.html`; `setChatOnly()` on load. Send is hello (`note: "A message is a hello. It is not a Yes."`).

**F5 — site repo has untracked `public/offers*`** (`/offers/` index is Parked in CURRENT). Not touched. Note it before the next site commit so it doesn't ride along.

**F6 — "competing apps" review.** The path you pasted is doc 24 again; it contains no competing-apps material (grepped `compet|similar product|adjacent|assimilat`). Your 07:52 approval mentions a `25_...` report — not on disk. Point me at it when it lands.

## Not done (by design)

No mint · no deploy · no share · no PUT to apex · no write under `~/anphuni-project` or `~/clients` · no rename/delete · no `aether approve`/`next` · no commit · no site patch · no Render reads.

## Hand-off to the operator Next (`share-urls-wave-1`, `~/anphuni-project`)

```sh
# per alias, idempotent — adds PROPOSALS/OPENER.md, keeps everything already there
for a in ~/anphuni-project/projects/*/; do
  /mnt/kingston-nixos-sync/opt/mechanicall-os/scripts/alias-scaffold.sh "$(basename "$a")"
done
# links table
/mnt/kingston-nixos-sync/opt/mechanicall-os/scripts/alias-links.py --out ~/anphuni-project/03_share-urls-wave-1/output/LINKS.md
```
Then, with your Yes: re-seed the 16 rooms from `PROPOSALS/OPENER.md` (F2), after deciding F1.

## Suggested commit (you / your other model run it)

```
feat(kit): share-urls-kit — alias scaffold, hello opener, read-only links

templates/alias/{POINTER,INTAKE,NOTES,OPENER}.md; scripts/alias-scaffold.sh
(idempotent, never CURRENT.md); scripts/alias-links.py (read-only, unminted
fallback). Site face checked on disk: FLAG seedFromPropose ignores opener.
gitignore .aether/proposals/clients/. No mint/deploy/share.
```
Stage only: `templates/ scripts/alias-scaffold.sh scripts/alias-links.py dev/70_share-urls-kit/ .gitignore`. Review `CURRENT.md`, `DECISIONS.md`, `.aether/events.jsonl` separately — the events diff contains your approval prose including income figures.

## Halt

Kit is on disk. Human reads this, decides F1, then `aether next` (e.g. `legal-assimilation-report`) when ready. Silence is never permission.
