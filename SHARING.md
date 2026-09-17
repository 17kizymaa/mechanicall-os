# SHARING — twin + depreciated inbox

**Not CURRENT. Not Yes. Not a VCS product.** Headscale is a **login-server / mesh**. It does not store folders.

## Default wire — read-twin (T8b)

Operator **watches** the bound pocket. GET-only.

```
python3 python/aether_twin.py --host 127.0.0.1 --port 7078
# TWIN_POCKET=/path/to/their/folder   (never this repo)
```

| GET | File |
|-----|------|
| `/current` | `CURRENT.md` |
| `/propose` | `PROPOSE-CURRENT.md` |
| `/receipt` | `RECEIPT.md` |
| `/events` | `.aether/events.jsonl` |
| `/gate` | `.aether/gate.json` |
| `/tailnet` | status + fingerprint (never the preauth key) |

GET is not Yes. POST is 405. Twin does not call `aether approve`.

After JOIN, the same routes may ride tsnet `Listen :7078`. Until JNI is linked, that download is not live. adb pull is lab, not STORM, not A33-as-product.

Watch dir: `~/mechanicall-twin/<sitter>/` **outside** this git worktree.

## Depreciated folder send (E7 Other)

Opt-in. Not EdubaWare upload-to-cloud. Not syncthing dual-CURRENT.

Steal: **AirDrop / Nearby Share / Taildrop / ChatGPT “Download when ready”**.

1. **Offer** — a folder is staged. `NOTICE.json` with `notify: true`, `not_yes: true`, `status: offered`.
2. **Notify** — operator sees `inbox/sitters/<id>/`; sitter sees an incoming-offer lamp (not Decide).
3. **Accept / Decline** — like AirDrop. Decline is not reject-CURRENT. Accept copies files.
4. **Never auto-apply CURRENT.md.** Accept **skips** live `CURRENT.md`. A “new application” folder is still an offer (user installs/opens; not Yes).
5. **Gitignore** — `inbox/sitters/` and `inbox/outbox/` are local. Not law. Not this repo’s CURRENT.

```
python3 -c "from aether_inbox import upload_sitter, offer_outbound, accept_offer, decline_offer"
```

| Path | Direction |
|------|-----------|
| `inbox/sitters/<id>/` | sitter **upload** (lab drop or opt-in) → operator looks |
| `inbox/outbox/<id>/` | operator **send back** → sitter Accept/Decline |

Headscale may carry the tarball later (JNI leftover). The **store** is always a local gitignored directory, never the control plane.

## FILES button

In-app FILES overlay is **cut**. FILES opens the **device file manager** on the bound directory (`openBoundInFileManager`). DIR remains Bind.

## Bind

Phone bind ≠ this repo (B10). Uploading a *copy* into `inbox/sitters/` is not binding mechanicall-os. Operator must not `aether approve` from an inbox copy.

## Not this standard

- git auto-commit in the pocket
- syncthing dual-write of CURRENT
- Funnel / public Ollama
- Chat as a second authority
- `aether_pocket_serve.py` Yes POST as the send path
- Headscale object storage / Taildrop-on-Headscale as law
- Auto-install of an inbound APK as Yes
