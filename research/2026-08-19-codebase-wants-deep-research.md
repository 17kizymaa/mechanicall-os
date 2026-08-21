# Deep research report — this codebase (decisions + Grok/agent logs)

**Status:** research · **not** CURRENT · not an approve  
**When:** 2026-08-19  
**Trigger:** operator: *Do the research again but on this codebase (lots of markdown decisions / grok/agent chatlogs exist). We'll use both to inform me.*  
**Sister report (web + protocol + market):** `research/2026-08-19-operator-wants-deep-research.md`  
**Protocol:** Open Deep Research (scope → parallel executors → one-shot write); GPT-Researcher local-docs crawl; IterDRAG gap pass.  
**Corpus:** 638 unique Grok `prompt_history` entries (2026-07-21 → 2026-08-19) under mechanicall-os / kingston / people-app / client-one session dirs; Claude project for this cwd (thin: XFCE plugin slash commands, not product talk); `DECISIONS.md`; `decision-tree.md`; `PRODUCT.md`; `docs/SINGLE-APP-DISTRIBUTION.md`; `.aether/proposals/`; ICM 23–27; `AUTHORITY.md`.

Chat logs are **evidence**. They do not override `CURRENT.md` (`AUTHORITY.md`).

---

## Research brief

What does *this tree* already know about the operator’s wants — in their typed prompts and in markdown they locked — that a web-only research pass cannot see?

---

## Corpus honesty

| Source | Weight |
|--------|--------|
| Grok TUI `prompt_history.jsonl` (this cwd + related) | Primary. 638 unique prompts. This is the month of work. |
| `DECISIONS.md` / live `CURRENT.md` / `decision-tree.md` | Locked or logged human gates. |
| ICM `dev/23`–`27`, proposals | Human choices mixed with agent paper. |
| Claude `~/.claude/projects/…mechanicall-os` | One session, 18 user events, almost all `/mechanicall-domain:next` / plugin — **not** a product log. |
| `dev/**/SESSION-LOG.md` | Thin (MBP seat ops). |

There is no second secret product spec. The Grok prompts *are* the journal.

---

## Findings from the Grok chatlog (their mouth)

### The want that does not change

From 27 July to 19 August they ask, over and over, for **a face a non-developer will actually sit in and keep using**, with **CURRENT on the screen**, without a zoo of CLIs.

Exact turns:

> “It feels way too CLI-based for even the 1 technical tester to **want** to use. It needs a dashboard, I feel.” — 2026-07-27T10:13

> “No - "E. TUI" is actually going to work perfectly. Real friction point, at the moment, is the lack of "buttons" and that makes operating the software ritualistic.” — 2026-07-27T10:29

> “the aether panel interface actually needs a chat **on-the-same-page**. This way, the client doesn't have to worry about agent-agnostic stacks” — 2026-07-28T08:21

> “heterogenous agent CLIs and TUIs; it is a real technical hurdle that is gonna shrink my audience to the developers and indie hackers, **which my wallet doesn't want.**” — same day

> “the application to a casual user **is** the **UX/UI** so all chatting needs to be governed with permission **outside-the-4th-wall**” — 2026-08-04

> “My clients aren't getting results. CURRENT.md needs to be the resource.” — 2026-08-19T08:26

### CURRENT as-product — they said it on 28 July

This morning’s “CURRENT.md needs to be the resource” is not new. The same feeling as today’s 08:18 reject is already in the log:

> “When you told me to "aether approve [insert description]", I didn't even feel like approving it. I have been feeling that way for a while now. … I've **over-tooled the system already instead of developing the CURRENT.md as-product.**” — 2026-07-28T09:02

31 July they correct an agent: CURRENT is **SACRED**, not a toolbox. 8 August they trust one thing: *if they edit CURRENT, an empty session becomes the last expected state.* 19 August they refuse “a folder that’s yours” as air. Same spine.

### What a client result was, when they named it

They almost never name a KPI. They name **sits**:

- Chat on the same page as the plan; no command soup.
- They *see* the model; history “stored locally and is protected.”
- Preview-then-accept (TV, shopping list, Outlook, “tell someone something they’ve developed”) — 28 July promo CURRENT for **client one**.
- They keep using it. The failure they wrote down: website seat, “they said they would use the application,” **stopped after like 2 minutes**, **zero OpenRouter calls** — 2026-08-04.
- Casual install: site name / download. Not “join my tailnet.” Not “log in as my email.” Friend-sim 18 August: “You failed.”
- Mum / Emilia: a playground for coding agents, not a protocol class.
- 19 August: “a solid workspace I can improve other peoples apps with” — then they **rejected** the agent turning that into folder-jargon. The job is **other people’s apps getting better**, not a philosophy of folders.

### Money in the log (so “bills” is not a vibe)

- Wallet doesn’t want only indie hackers (28 Jul).
- “cash is 1700GBP” (31 Jul).
- Consumer product before **September 9** — car insurance / move-out (5 Aug).
- “I have plenty of takers for this!” then “this isn't going in the right direction” the same day (5 Aug).
- “it hasn't been paying me like I thought” (17 Aug).
- “got bills to pay!” (19 Aug).

### Faces they built, then threw, in the log

Dashboard → TUI+buttons → chat-only → website chat+plan → playground Geobook/eMachine → Android IDEs → “F*ck all them IDEs” → mum Geobook → phone demo → Play Store talk → APK “will work” → people-app. Each rebuild follows a person leaving or a face that felt like ritual.

---

## Findings from markdown decisions (what they locked)

**Stable law:** one Next; models never approve; silence ≠ Yes; GET is not Yes; do not bind strangers to this git tree; Session is not core; Play Store / Funnel / operator-email login off this Next.

**3 August (SINGLE-APP-DISTRIBUTION.md), locked as a failed-bet verdict:** casual CLI failed; the distro opens **exactly one application — the seat UX**; that UX is **incomplete**.

**16 August (decision-tree.md), closed then left:** phone is a **demo projection**; client is the planner; proposal-doc editor not bubble chat; same `aether` in the APK.

**18 August:** people-app factory; then reject of desktop-only validation; “APK will work”; SeatMate identity they Yes’d says **“Not an app. Stack later.”**

**19 August:** three rejects; live CURRENT still `people-app-phone-seat` / REJECTED.

**Document contradiction (the tree arguing with itself):**

| File | “The application” |
|------|-------------------|
| `CURRENT.md` / `PRODUCT.md` | local-first **protocol** |
| `SINGLE-APP-DISTRIBUTION.md` | one incomplete **seat window** |
| `decision-tree.md` | **demo APK**, not the product |
| `dev/25` | **workspace is the app** |
| SeatMate `IDENTITY.md` | **not an app** |
| `.continue-here.md` | still says APPROVED — **stale vs live REJECTED** |

`AUTHORITY.md`: chat does not win. Live CURRENT wins. Live CURRENT is a **rejected phone-seat Next**, identity line still “protocol.”

---

## IterDRAG gap this pass filled

The 19 Aug morning report used PRODUCT + DECISIONS + market. It could not hear:

1. **28 July** already named over-tooling vs CURRENT-as-product, and already refused the *feeling* of approve.
2. **Client one** is a real sit with a named failure (2 minutes, zero calls).
3. **Wallet numbers** and **9 September**.
4. **“the application to a casual user is the UX/UI”** — their sentence, 4 August.
5. Claude logs are **not** a second brain for this product. Grok TUI is.

---

## Explicit conclusion (codebase only)

In this repository’s own memory, the operator has been trying to get **other people to stay in one window long enough to finish a job**, with **CURRENT visible**, **Yes that they mean**, and **no CLI zoo** — because **the CLI even failed the one technical tester**, and **the website failed in two minutes**, and **the wallet cannot live on indie hackers**.

They locked the **engine** (protocol) in markdown. They locked the **glass** (one seat, incomplete) on 3 August. They have spent a month **re-cutting the glass** every time a person left. The chatlog’s verdict on 19 August is empirical: **clients aren’t getting results.** “A folder that’s yours” is them catching an agent selling the box. “CURRENT.md needs to be the resource” is the same 28 July line: the plan on the screen is the product they can point at; the rest is over-tooling.

**People-app** in the log is not a new company. It is: *send this to a non-dev friend without making them become me.* After Tailnet-as-me failed.

**Improve other people’s apps** in the log is the *result* (their software gets better / their email gets drafted / mum’s agents work), not a new architecture.

This does not approve `people-app-phone-seat`. The leftover Next is APK chrome for a sit. The sit is the want. The APK is one glass.

---

## Sources

- `/tmp/grok-prompt-history-mechanicall.md` (extract of `~/.grok/sessions/…mechanicall-os…/prompt_history.jsonl` and related)
- `DECISIONS.md`, `CURRENT.md`, `decision-tree.md`, `PRODUCT.md`, `docs/SINGLE-APP-DISTRIBUTION.md`, `AUTHORITY.md`
- `dev/25_icm-people-app/people-app/05_do/output/IDENTITY.md`
- `.continue-here.md` (stale)
- Claude project jsonl (negative finding: not a product corpus)
