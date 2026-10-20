# RESEARCH — crowdsourced UI opinions (2026-09-11)

**Not law. Not Yes. Not millwork.**
**Why:** event 970 — research crowdsourced opinions, then propose CURRENT again.
**What this recants:** last turn’s agent steal (`STEAL.md`: FreqUI trade pane + iMessage). Crowd does not sit FreqUI as a paper book.

Sources mixed on purpose: Reddit threads, StockBrokers.com (they open accounts and sit platforms), product docs people actually follow, HN, a little X. Affiliate review copy is labelled. X trading-bot spam is discounted.

---

## Paper — what people sit

### Crowd ranking (what comes up, not what I like)

| Rank in the conversation | Who | Crowd line | Use for us |
|---|---|---|---|
| 1 (feel) | **TradingView Paper Trading** | r/Daytrading: paper on TV “just feels so right”; “most user-friendly, cleanest layout”. StockBrokers FAQ: TV “often more intuitive and visually advanced than many legacy brokerage platforms.” | **Steal this grammar.** |
| 1 (broker-sim labs) | **Webull** | StockBrokers.com 2026: **best paper trading platform** — “high-fidelity simulation that perfectly mirrors its live trading experience”; “widget-based desktop”; short learning curve. | Runner-up grammar (panels, same-as-live). |
| Power, not a gift | **thinkorswim paperMoney** | Same r/Daytrading thread: “absolute biggest struggle” despite “the most powerful tools”. Stock Academy: “looks like it was designed for someone with three monitors and a Bloomberg terminal.” | Do **not** steal for a birthday they need not learn. |
| Named, prohibited | **IBKR TWS** | StockBrokers: “Density of features requires a significant time investment.” Reddit: TWS “overcomplicated”. CURRENT already Rejects IBKR name/passing-off. | **Out.** |
| Options-first | **tastytrade** | “Cut out the noise”; “charts are poor”; people who want modular IBKR-style panes don’t get them. | Not the gift. |
| Social/casino | **eToro / Robinhood** | StockBrokers: eToro = community/copy. Robinhood has **no** paper trading. CURRENT already Rejects casino-confetti. | **Out.** |
| Agent last turn | **FreqUI** | Freqtrade **bot** dashboard. Not in paper-trading Reddit/StockBrokers lists. | Recant as Paper steal. |

TradingView’s own paper docs (what users are told to sit): **chart is the page**; watchlist is a **side** panel; **Trading Panel is the bottom toolbar** (account, orders, positions, order ticket). Buy/Sell live on the **chart toolbar**, not as a homework form in the chart well. r/TradingView: people **hate** Buy/Sell buttons appearing on every layout.

X (weak, but consistent): people immediately recognise a TV screenshot by the bottom **“Paper Trading”** strip. That label is how the crowd tells paper from live. ToS crowd does the same with a yellow **PM** bar.

### What the crowd is *not* asking for

- Giant BUY/SELL filling the middle (our room).
- Empty white/black voids (r/fidelityinvestments: “too much white space”; they want density on a trader page).
- Dribbble/crypto-monospace “student weekend” chrome (r/FreetradeApp roasted a UK refresh for exactly that — maps to our gold DIY blotter).
- Bloomberg-as-pretty (HN: Bloomberg is ugly **on purpose** for power users. Wrong gift).

### Paper steal, from the crowd (grammar, not wrap)

**Named:** TradingView **paper-trading layout**.

1. Chart **fills** the work.
2. Watchlist is a **side** list (last, %).
3. Positions / working / fills live in a **bottom trading panel**, not a third empty column of homework.
4. Ticket is a **panel** (qty, limit, buy/sell) — small. Not the hero.
5. The word **Paper** is on the trading surface (TV bottom bar / ToS PM). Not a second legal essay in the OS chrome.
6. Optional: Webull-style widget dock *inside Paper* later. Not this cut.

**Mechanism without wrapping tradingview.com:** TradingView **Lightweight Charts** (Apache-2) for the pane. Steal the *layout*, not the TV wordmark, not their login, not a public quote wall.

---

## Chat — what people sit

| Who | Crowd line | Use for us |
|---|---|---|
| **Telegram Web / Desktop** | r/UI_Design (2026-07): “telegram is actually the best when it comes to UI/UX”; “desktop and web arent some laggy afterthought”; comment: “like a supercharged apple messages.” SideProject clones Telegram **K web** because that *is* the web-messenger grammar. | **Steal this grammar.** |
| **iMessage** | Crowd’s family metaphor (“Apple Messages”). No official web. | Metaphor only. Don’t fake iMessage bitmaps. |
| **WhatsApp Web** | “Fine for normal chats”; people pin it as a PWA and **hide the sidebar** for 1:1. | Optional: no left list on a one-peer room. |
| **Facebook Messenger.com** | Shutting down 2026; desktop shoved into facebook.com/messages. | Don’t steal dying Meta chrome. |
| **Slack / Discord** | Crowd routes those to *team channels*, not 1:1. | Don’t steal work chrome for a birthday chat. |

Telegram Web K failure mode the crowd filed: **all messages left-aligned, one colour** (“can’t tell who’s saying what”). Steal: **me vs them** (alignment + colour). Composer at the **bottom edge**. Peer **name** is the title — not a `CHAT` marketing label.

X on “Telegram UI” in Sep 2026 is mostly **crypto trading bots**. Discount that. Not this gift.

---

## Desk (two apps) — crowd does not argue this

Event 970 recants **agent-picked steal**, not “room = desktop”. No crowd thread says a 1:1 chat should live as a strip under a blotter. WhatsApp/Telegram people treat chat as **the app**. TV/Webull people treat the book as **the app**. Dock switching two apps is compatible with both crowds. Keep it.

What the crowd would FLAG on our stills (`dev/64_site-play/02_play/output/`):

- Paper: 3-point spark + giant BUY/SELL + empty well ≠ TV/Webull.
- Chat: leftover `CHAT | Anthony | Enter to send` + equity numbers in the messenger ≠ Telegram/iMessage.
- Host: `MECHANICALL` + legal + gold dock as product chrome = Freetrade-refresh class (invented).

---

## Honest limits of this research

- StockBrokers.com is a review lab (they sit platforms). Not Reddit. Still the ranking people cite.
- Could not fetch the r/Daytrading and r/UI_Design HTML bodies (tool fetch failed); titles + snippet quotes above are from search hits. Treat as cited snippets, not full-thread ethnography.
- No live sit of TradingView/Webull/Telegram inside this stage (would be wrapping vendor sites). Grammar from their own docs + crowd description.
- UK Webull/TV availability and IBKR paper web-vs-TWS are **not** this gift’s problem. We are not a broker.

---

## Steal list for the next CURRENT (crowd, not agent)

| App | Named steal | Recant |
|-----|-------------|--------|
| **Paper** | TradingView paper-trading layout (chart fill + side watch + **bottom** panel). Lightweight Charts as the chart widget. | FreqUI. ToS/Bloomberg. IBKR. DIY blotter. |
| **Chat** | Telegram Web grammar (peer title, thread fills, composer glued, me vs them). iMessage as the spoken metaphor. | Slack/Discord. Marketing header. Ticket chrome. |
| **Desk** | Quiet Paper \| Chat dock. No protocol bar as the product. | GTK twin. Chat-as-strip. |

PASS is not Yes. FLAGS are not millwork permission.
