# Mechanicall desktop

Two apps on one glass. The **site room** is the desk (Paper + Chat).

Birthday: `https://anphuni.com/you-decide/t/e9b16791a12ac1ef521891b6eac3bf68`

Local GTK (`sh scripts/desktop.sh`) is a lab twin. Bind `127.0.0.1`. Paper only.

| App | Room | What it is |
|-----|------|------------|
| **Trader** | happy-birthday | Watchlist, simulated last, market/limit ticket, positions, P&L |
| **Serve** | hi-its-mother | Servant. Chat is hello. Send is not Yes. |

`this-works` stays parked. Not a third app.

Not live money. Not a brokerage. Not IBKR-named. Models never approve.

## Run

```bash
sh scripts/desktop.sh
# or: python python/desktop_os.py open
```

GTK WebKit window when available; otherwise the URL prints and the system browser opens.

Serve-only (no window):

```bash
python python/desktop_os.py serve --port 8766
```

Book lives in `desktop/var/paper-book.json` (gitignored). Engine: `python/paper_book.py`.
