# inbox — lab folder send (not Headscale-as-Drive)

**Not CURRENT. Not Yes.** Bytes land here. Headscale only carries the mesh later.

| Path | Direction | Who Accepts |
|------|-----------|-------------|
| `sitters/<id>/` | sitter → operator (lab drop or opt-in upload) | operator *looks*; never apply as mechanicall-os CURRENT |
| `outbox/<id>/` | operator → sitter (new app, template, …) | **sitter Accept/Decline** (AirDrop / Taildrop-shaped notify) |
| `drop/` | last lab-drop slot (`offer.zip` + `progress.json`) | one offer; GATE reads percent |
| `tickets/<id>/` | You Decide web tickets (capability URL) | drop `in/`; `out.zip` empty until later Yes; never CURRENT |

Apex door is `https://anphuni.com/you-decide`. Live drops do not write this tree by themselves. Pull:

```
python3 python/you_decide_os.py pull <ticket-url-or-id>
python3 python/you_decide_os.py put-zip <id> path/to/out.zip
```

`YOU_DECIDE_ORIGIN` defaults to `https://anphuni.com`. Do not point it at lab `127.0.0.1` as the public drop.

`NOTICE.json` on every offer. Accept copies files and **skips live CURRENT.md**. Decline leaves the offer marked declined.

See `SHARING.md` and `python/aether_inbox.py`. Drop: `python/aether_drop.py` (127.0.0.1:8765).
