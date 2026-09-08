# inbox — lab folder send (not Headscale-as-Drive)

**Not CURRENT. Not Yes.** Bytes land here. Headscale only carries the mesh later.

| Path | Direction | Who Accepts |
|------|-----------|-------------|
| `sitters/<id>/` | sitter → operator (lab drop or opt-in upload) | operator *looks*; never apply as mechanicall-os CURRENT |
| `outbox/<id>/` | operator → sitter (new app, template, …) | **sitter Accept/Decline** (AirDrop / Taildrop-shaped notify) |
| `drop/` | last lab-drop slot (`offer.zip` + `progress.json`) | one offer; GATE reads percent |

`NOTICE.json` on every offer. Accept copies files and **skips live CURRENT.md**. Decline leaves the offer marked declined.

See `SHARING.md` and `python/aether_inbox.py`. Drop: `python/aether_drop.py` (127.0.0.1:8765).
