## Inputs
- Layer 1: ../CONTEXT.md
- Layer 3: ../../../CURRENT.md (Next `hand-client-current` APPROVED)
- Layer 4: ../../../.aether/proposals/clients/{happy-birthday,hi-its-mother,this-works}/
- Behaviour: ../scripts/copy_out_packs.py

## Process
You are the **copy-out** stage.

1. `aether preflight hand-client-current` must have allowed.
2. Copy each pack to a directory **outside** the mechanicall-os git tree. Default dest: `/home/anphuni/client-offers/<alias>/`.
3. Copy only `CURRENT.md` and `HOW-TO-ACCEPT.md`. Do not copy operator README as their law.
4. Refuse if any dest CURRENT is already APPROVED.
5. `aether current validate` each dest. PASS required.
6. Leave Approval **PENDING**. Do not `aether approve`. Do not zip. Do not hand (that is 03).
7. Write RECEIPT.md to output/.

## Outputs
- RECEIPT.md -> output/
- summary.md -> output/
- dest folders live **outside** this repo (paths recorded in RECEIPT)
