## Inputs
- Layer 1: `../CONTEXT.md`
- Layer 1: `../../../CURRENT.md` (do not rewrite)
- Layer 3: `../06_mum-face/output/RECEIPT.md`
- Layer 3: `../07_resume-rehearsal/output/RECEIPT.md`
- Layer 3: `../../../scripts/serve-pocket-face.sh`
- Layer 3: `../../../python/aether_pocket_serve.py`
- Layer 4: human “08_serve-face”

## Process
You are serving the **existing** LAN mum face. No new surface.

- Preflight `mobile-planning-demo`.
- Start `sh scripts/serve-pocket-face.sh` (bind `192.168.0.51:8765`, twin `~/mechanicall-pocket`).
- Prove GET `/` is not Yes: page loads; twin CURRENT hash does not become an approve.
- GET `/yes` must not apply (404 or not a GET verb).
- Do **not** POST `/yes`, `/not-yet`, `/save`, or `/agent`.
- Do not write operator `CURRENT.md`.
- Do not `aether approve` / `next` / `reject` on the operator tree.
- Sitting of 2026-08-16 stays cancelled; this is a rehearsal face, not mum-in-the-room.

## Outputs
- RECEIPT.md -> output/
- summary.md -> output/
