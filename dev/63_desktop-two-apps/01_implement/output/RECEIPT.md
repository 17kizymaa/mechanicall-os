# RECEIPT — desktop two apps

**Next:** `personal-current-sprint` (preflight allowed).
**Not Yes.** This is a sitting of the desk, not a stamp.

## What shipped

A local desktop with two apps:

| Dock | Room | Behaviour |
|------|------|-----------|
| Trader | happy-birthday | Watchlist, simulated last that ticks, market/limit ticket that fills, positions, P&L |
| Serve | hi-its-mother | Servant. Send is hello. Send is not Yes. |

`this-works` is not on the dock.

## Paths

- Engine: `python/paper_book.py`
- Glass: `python/desktop_os.py` + `desktop/static/`
- Launch: `sh scripts/desktop.sh`
- Book: `desktop/var/paper-book.json` (gitignored)
- Tests: `tests/test_paper_book.py`, `tests/test_desktop_os.py`

## Proof

- 12 unit/API tests green. CURRENT.md bytes unchanged.
- Window on `:0` titled Mechanicall. Paper buy of 10 BOLT filled. Last moved. P&L moved.
- Chrome says paper / simulated last / not live money. No IBKR name.
- Bind `127.0.0.1:8766`. No `create_order_instruction`.

## Sit it

```bash
sh scripts/desktop.sh
```

Click a name. Submit. Watch last and P&L. Dock **Serve** for Mum. They need not stamp.
