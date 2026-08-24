# TWIN-PROTOCOL — operator read-twin (draft of SHARING.md)

**Not CURRENT. Not Yes.** T8b: mechanicall-os **watches** the bound pocket. It does not become their law. 04_sharing copies this into repo `SHARING.md`. 02 may ship a GET listener; 04 names the standard.

## What “connected to mechanicall-os” means

The operator tree can **pull/read**:

- `CURRENT.md`
- `PROPOSE-CURRENT.md`
- `RECEIPT.md` (if present)
- `.aether/events.jsonl`
- `.aether/gate.json` (instrument)
- `.aether/tailnet.json` (status + fingerprint, never the key)

Writes stay on the phone until **their** Decide. Twin must not call `aether approve` / `yes` / rewrite their CURRENT.

## Wire this Next

Prefer Headscale, not adb-to-A33:

1. After JOIN, phone tsnet `Listen` on a high port (suggest `:7078`).
2. GET-only routes. No POST Yes. No POST propose.
3. Operator from mechanicall-os: `curl http://<phone-magicdns>:7078/current` (etc.) into a **watch directory that is not this repo’s CURRENT.md**.
4. Existing `aether_pocket_serve.py` **brake face** (GET page + POST yes/not_yet, A33 serial, `push_phone`) is **not** this twin. Do not reuse Yes endpoints.

adb pull remains a **lab** fallback when tsnet is down. It is not the product wire. Never share `RZCW2038KHN` across STORM.

## Bind vs twin

Twin reads whichever folder is bound. Bind ≠ mechanicall-os (B10). T8c grey-area: many CURRENT.md under an install dir is allowed; requiring CURRENT.md to bind is **not** law this Next.

## What this Next does not ship

- git in the pocket
- syncthing dual-write
- inbox.md on the operator tree as law
- realtime chat between phone and operator Grok
- Funnel

## Operator watch dir

Suggest `~/mechanicall-twin/<sitter-hostname>/` **outside** this git worktree. `refuse_if_operator` must still fire if someone points it at mechanicall-os.

GET is not Yes. Pull is not Decide.
