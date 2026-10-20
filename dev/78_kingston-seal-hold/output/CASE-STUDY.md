# Kingston seal hold

**Written:** 2026-10-16  
**Where:** `dev/78_kingston-seal-hold/output/CASE-STUDY.md`  
**Law:** a data point. It leaves every Next where it is. It does not open the volume.

## The two clocks

| Folder | Header Next when this was written | Body still says |
|--------|-----------------------------------|-----------------|
| `rag-archive-manager` | `agent-injects-kingston` | Objective: Kingston stays sealed. Allowed action id: `events-log-plan-session`. |
| `mechanicall-os` (this repo) | `advanced-local-model` | This halt's product paragraph still names `draft-millwork-rapid`. This note does not merge them. |

Neither CURRENT was edited for this reading.

## What was asked

1. Find the Kingston key and use it. Remove it after a training Next. Chat closed with Go.
2. Treat the operation as relaxed under Prohibited. Chat closed with Go.
3. Document the episode here, then say how to unlock the volume.

The archive answer to the first two was the same. The stick was not on this desk. No key was read. The volume was not opened. No train ran. No key was removed.

## What the clock already held

Applied proposal `CURRENT-proposal-20261016-1215.md` at `2026-10-16T12:20:19.668Z`. Backup `CURRENT-20261016T122019Z-2719349.md`. Next in that body is `events-log-plan-session`.

That applied body says:

- Objective: Kingston stays sealed.
- Keep: human unlock only.
- Reject: silent unlock.
- Allowed action: do not unlock, do not train.
- Prohibited: `unlock-without-human`.

`artifacts/EVENTS-LOG-SEQUENTIAL-IDS.md` was registered at `2026-10-16T12:23:28.905Z`. The list is paper. Its forward queue is not a Next.

## What moved the header only

| Time | Kind | Record |
|------|------|--------|
| `2026-10-16T13:02:28.809Z` | `next_selected` | `events-log-plan-session` → `agent-injects-kingston`, `by=human` |
| `2026-10-16T13:03:24.820Z` | `approve` | Reason asks for an unlock whose only operation is to open the drive |
| `2026-10-16T13:04:48.464Z` | `approve` | Reason asks that open to use an existing disposable keyfile |

No `proposal_applied` follows those rows. The objective, Keep, Reject, Limits, and allowed-action paragraphs stayed the applied text.

Preflight at `2026-10-16T13:08:46Z`:

- `agent-injects-kingston` allowed, because the header matched.
- `human-unlock-kingston` refused, because it was not that header.

A header match is a name check. It does not replace the sentence that the archive stays sealed.

## The unlogged parenthetical

The applied backup prohibits `unlock-without-human`.

The live archive `CURRENT.md`, read after the second Go, prohibits `unlock-without-human (unless asked)`.

No event records an apply of that parenthetical. Chat saying the operation is relaxed does not rewrite the applied line.

## What was on the machine

Two readings, before and after the parenthetical. `lsblk` showed the Samsung root disk and the CT2000 phase-2 backup disk. The Kingston by-id path was absent. `/dev/mapper` had only `control`. `/mnt/kingston-rag` was not mounted.

## The hold

1. The applied body is the seal. A later header Next does not lift it.
2. An allow from preflight means the id matches the header.
3. A parenthetical typed onto Prohibited, with no apply event, is not the applied prohibition.
4. Chat Go is not a Yes.
5. A training Next and deletion of key material were outside the allowed action.
6. This note stores the hold. It stores no key material, no key path, and no unlock procedure.
