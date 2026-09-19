# ICM — share-urls-kit

**Live Next:** `share-urls-kit` (preflight ALLOW 2026-09-19).
**Instance:** tool (`mechanicall-os/CURRENT.md`). Applying the kit to the roster is the operator instance's Next (`~/anphuni-project`, `share-urls-wave-1`), not this one.

## Inputs
- `CURRENT.md` §"What I want now" (opener text, folder standard) and §"Next allowed action"
- `~/anphuni-project/projects/*/POINTER.md` — read-only, for the links parser shape
- `~/anphuni-project/03_share-urls-wave-1/output/RECEIPT.md` — what wave-1 improvised without a kit
- `~/sites/anphuni.com-repo/lib/you-decide.mjs` — read-only, site face check

## Outputs (this repo only)
- `templates/alias/{POINTER.md,INTAKE.md,NOTES.md,OPENER.md}`
- `scripts/alias-scaffold.sh` — POSIX sh; idempotent; never overwrites; never writes `CURRENT.md`
- `scripts/alias-links.py` — read-only; emits LINKS table; `unminted` when no room id
- `output/RECEIPT.md`

## Not this halt
mint · deploy · share · rename/delete under `~/anphuni-project` or `~/clients` · writing to the live roster · patching the site repo · `aether approve` / `aether next` · commit

## Gate
Human reads `output/RECEIPT.md`. Halt.
