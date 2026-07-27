# Dashboard without compromise — interface research

**Status:** research · not shipped · not a CURRENT authority  
**Date:** 2026-07-27  
**Trigger:** Alpha first-run (`onboard` / CLI) feels too CLI-heavy even for a technical tester; operator instinct is “it needs a dashboard.”  
**Hard fence:** Must not violate Core Principles, `NOT-IMPLEMENTED.md`, or the honest preflight claim. Filesystem remains sole durable truth. Models never approve.

---

## 1. The real problem (not “we need React”)

Testers don’t refuse Mechanicall because authority is wrong. They refuse because:

| Friction | What they experience |
|----------|----------------------|
| **Command discovery** | “What do I type?” beats “what is authorized?” |
| **State is scattered** | CURRENT + events + artifacts live in different files; CLI shows slices |
| **Mental model is shell** | Preflight/approve feel like sysadmin, not project control |
| **No ambient overview** | No single glance: objective / next / last refuse / pending human |

A “dashboard” is the user saying: **I want one glanceable surface and safe buttons for the few actions that matter** — not “replace the filesystem with a product database.”

Architecture-compatible translation:

> **Projection UI** over authority files + **thin action buttons** that only shell out to `aether` (or write Markdown the human then approves).

Not:

> **Control plane UI** that holds its own state, bypasses CURRENT, or pretends to sandbox agents.

---

## 2. Non-negotiable design law

Any approach must pass this test:

1. **Read path:** UI state is derived from `CURRENT.md`, `.aether/events.jsonl`, `.aether/artifacts/`, `.context.md` (and optionally app.json).  
2. **Write path:** mutations go through `aether` or explicit human file edits — never a silent second store.  
3. **Approve path:** only human-triggered `aether approve` / `reject` (or human edit of CURRENT). No “Approve” that is model-driven without a hard human gesture.  
4. **Inspectability:** after any UI action, `cat` / `git diff` still explain what changed.  
5. **Offline / local:** no required cloud account; bind to localhost or local files.  
6. **Removability:** deleting the UI package leaves the project fully usable via CLI + files.  
7. **Honesty:** UI must surface “preflight is cooperative; this is not a sandbox.”

If an option fails 1–4, it compromises the architecture even if it “feels modern.”

---

## 3. Spectrum of approaches (low → high compromise risk)

### A. Markdown “dashboard” (generated panel)

**What:** `aether distill` (or `aether status --html` / `aether panel`) writes `.aether/PANEL.md` or `DASHBOARD.md` with tables: Objective, Next, Prohibited, last 10 events, open artifacts. Open in any editor / Obsidian / Typora.

**Feel:** Mild dashboard; still document-native.  
**Deps:** Zero new runtime.  
**Mutations:** None from the panel itself — human edits CURRENT or runs CLI.  
**Architecture fit:** ★★★★★  

**Pros:** Zero compromise; git-diff friendly; works for supported non-technical clients in a shared Obsidian vault with operator.  
**Cons:** No buttons; still “a file,” not a product moment.

**When:** Ship next as the *minimum* ambient overview that CLI alone lacked.

---

### B. Static HTML projection (file:// or one-shot generate)

**What:** Python/stdlib script renders CURRENT + events → single ` .aether/panel.html` (or `artifacts/panel.html`). Open in browser. Optional “refresh” is re-run script / `aether panel`.

**Feel:** Real visual dashboard cards without a server.  
**Deps:** Browser only; generator is stdlib Python (allowed userland).  
**Mutations:** Read-only by default. Buttons can be `href` to `aether:` custom protocol **or** disabled with copy-paste commands. Prefer read-only first.  
**Architecture fit:** ★★★★★ (read-only) · ★★★★☆ (if actions are clearly “run this shell”)  

**Pros:** Instant “this is a product” screenshot for alpha; no daemon; fully offline; HTML is still a file in the project.  
**Cons:** Actions are awkward on pure `file://` (no shell). Mutation needs C or D.

**When:** Best first “dashboard” that technical users open without memorizing flags.

---

### C. Localhost “thin panel” (read FS + invoke aether only)

**What:** Tiny stdlib `python -m http.server`-class or ~100–200 LOC Flask-free server:

- `GET /` → HTML rendered from files (same as B)  
- `POST /preflight` → subprocess `aether preflight …` → show result  
- `POST /approve` → subprocess `aether approve …` only after explicit confirm checkbox (“I am the human”)  
- **No** application database; no session store of authority  

**Feel:** Proper dashboard with buttons.  
**Deps:** Python stdlib only (ideal) or one tiny dependency if forced.  
**Architecture fit:** ★★★★☆ if every write is subprocess to aether and logged in events.jsonl  

**Pros:** Solves CLI aversion without second truth; matches club-cortex “GUI at the edge.”  
**Cons:** Is a small daemon — must be optional, documented, killable; risk of scope creep into “web app.”  
**Mitigations:**

- Bind `127.0.0.1` only  
- No auth theater that pretends multi-user security  
- Banner: “Local projection of this folder’s files”  
- Name it **panel** / **desk** / **board**, not “Mechanicall Cloud Console”  
- Package as `aether panel` that starts/stops; not always-on service  

**When:** Right alpha response to “it needs a dashboard” *without* Club-cortex backend.

---

### D. Editor-native dashboard (VS Code / Cursor / Zed webview or panel)

**What:** Extension or task webview that reads workspace files and runs tasks mapped to aether commands. Truth stays in workspace.

**Feel:** Dashboard inside the tool technical users already live in.  
**Deps:** Editor extension packaging.  
**Architecture fit:** ★★★★☆ (same rules as C: no private state)  

**Pros:** Technical tester adoption; “development application” from UI-forking is literally the IDE.  
**Cons:** Multi-editor fragmentation; non-technical clients may not use VS Code; maintenance cost.

**When:** Parallel track after C, or instead of C if all alpha users are IDE-bound.

---

### E. Full-screen TUI (Textual / Bubble Tea / gum+fzf menus)

**What:** Terminal app with panes: CURRENT, events stream, actions menu, approve confirm.

**Feel:** Dashboard *for people who tolerate a terminal window* but hate remembering flags.  
**Deps:** Extra language/runtime risk — Core Principles prefer Markdown + Python; a Python Textual app is cleaner than Rust-only for this repo.  
**Architecture fit:** ★★★★☆  

**Pros:** No browser; keyboard-driven; still local.  
**Cons:** Still “lives in the terminal”; may not fix the emotional “this is CLI” reaction you just felt. Your report suggests **visual browser/editor**, not another TUI.

**When:** Secondary, not the primary answer to this feedback.

---

### F. Chat-shaped dashboard (Open WebUI / local chat over Ollama)

**What:** Already sketched in `nix/modules/open-webui-local.nix` — chat UI bound to localhost Ollama.

**Feel:** Familiar “AI product.”  
**Architecture fit:** ★★☆☆☆ as **authority** surface; ★★★★☆ as **propose / capture** surface  

**Pros:** Non-technical friendly; personal-llm path; club-cortex edge GUI story.  
**Cons:** Chat is a terrible primary control for Next/Prohibited unless every turn is forced through structured tools that call aether. Easy to *feel* authoritative while bypassing CURRENT.

**Law if used:** Chat may **propose** CURRENT edits and **explain** status; buttons/tools must call aether; never “the model approved it.”

**When:** Companion to C, not substitute. Aligns with earlier “user-inspired may grow from personal-llm” note — but only as propose layer.

---

### G. Heavy SPA / Electron / multi-page admin (avoid for alpha)

**What:** React router, auth, API layer, postgres “for the dashboard.”

**Architecture fit:** ★☆☆☆☆ — directly contradicts NOT-IMPLEMENTED and Core Principles.

**Verdict:** Park. This is how Mechanicall becomes a fake SaaS.

---

## 4. Recommended path (does not compromise the feeling *of* the architecture)

### Product framing

Call it a **Project Panel** (or **Authority Desk**), not “Dashboard-as-product” and not “wizard.”

```text
  [Project Panel — optional UI]
         │  reads
         ▼
  CURRENT.md · events.jsonl · artifacts/   ← sole truth
         ▲
         │  writes only via aether subprocess
  [aether CLI — always sufficient without Panel]
```

### Build order (increasing ambition, each shippable)

| Step | Deliverable | Tester value | Risk |
|------|-------------|--------------|------|
| **P0** | `aether panel` generates `.aether/panel.html` (read-only cards + last events + copy-paste command chips) | Instant visual; screenshotable alpha | Minimal |
| **P1** | Auto-refresh: `aether panel --watch` regenerates on file change (poll or entr) | Ambient overview while agents work | Low |
| **P2** | `aether panel --serve` localhost thin server: Preflight / Approve / Reject / Refresh buttons → aether only | Actual “I want a dashboard” fix | Medium (daemon discipline) |
| **P3** | Propose card: paste reflection → fill propose-CURRENT template (optional LLM) → human applies | User-inspired without authority leak | Medium |
| **P4** | Optional IDE extension that embeds the same HTML/API contract | Technical power users | Higher maintenance |

Do **not** jump to G. Do **not** make Panel required for alpha install.

### What the Panel must show (single screen)

1. **Objective** (from CURRENT)  
2. **Phase / Status / Approval**  
3. **Next** (big)  
4. **Prohibited** (list)  
5. **Last preflight** allow/refuse (from events)  
6. **Recent artifacts**  
7. **Human actions:** Approve, Reject, “Open CURRENT.md”, “Open events”  
8. **Honest strip:** “This panel does not sandbox agents. Compatible tools must call preflight.”

### What the Panel must never do

- Store authority only in browser localStorage  
- Auto-approve on timer or model confidence  
- Expose bind-all (`0.0.0.0`) in alpha defaults  
- Replace `NOT-IMPLEMENTED` web-dashboard ban with an undocumented second backend  
- Require Nix portable host / Open WebUI to understand authority  

---

## 5. Mapping to existing project direction

| Existing thread | How Panel fits |
|-----------------|----------------|
| Core Principles | Panel is Markdown/HTML projection + Python; truth remains files |
| ARCHITECTURE Interface Layer | “Tiny optional UI” now has a concrete shape: projection + aether-backed actions |
| Club-cortex “GUI at the edge” | Panel is the edge GUI for **one project folder**, not multi-tenant seats |
| Personal-llm propose | P3 propose card; doctrine still refuse self-approve |
| UI-forking “development application” | Panel is the registered app’s control surface; `app.json` can point `panel: local` |
| DISTRIBUTE alpha | Technical tester may open Panel first; supported non-tech clients walk with operator on Panel + files |
| NOT-IMPLEMENTED “web dashboard” | Keep ban on **product SaaS dashboard**; allow **optional local panel** with explicit naming and limits |

Suggested NOT-IMPLEMENTED clarification when implementing:

> **Not implemented:** multi-tenant web dashboard / remote control plane.  
> **Allowed (optional):** localhost project panel that projects sidecars and invokes `aether`.

---

## 6. Alternatives considered and why not first

| Approach | Why deferred |
|----------|----------------|
| TUI-first | Your gut reaction is anti-CLI-family, not anti-flags-only |
| Open WebUI as control | Chat hides authority; good for propose/capture only |
| VS Code extension only | Misses non-technical supported clients |
| Full Electron app | Heavy, duplicates browser, hard to inspect |
| Streamlit/Gradio “quick app” | Hidden state habits, dependency bulk, feels like a notebook not an OS |

---

## 7. UX copy that preserves architecture feeling

Bad:

> “Mechanicall blocks unsafe agent actions from this dashboard.”

Good:

> “This panel shows the project’s authority files. Preflight checks what agents *should* call. You still decide Approve.”

Bad:

> “Login to manage workspaces.”

Good:

> “Open a folder. The files are the product.”

---

## 8. Success criteria for a Panel alpha

The technical tester **opens the panel twice unprompted** after an agent session.

Plus:

- Can answer “what is Next?” without typing `aether current`  
- Can trigger one refuse demo from a button and see it in events  
- Can open CURRENT.md in editor from the panel  
- Can uninstall panel usage without losing project state  
- `git diff` after Approve still makes sense  

Stars still don’t matter. A second voluntary open does.

---

## 9. Implementation sketch (when CURRENT allows)

**Behaviours (Python, stdlib):**

- `python/aether_panel.py`  
  - `render(root) -> html`  
  - `serve(root, host=127.0.0.1, port=8765)`  
  - subprocess helpers: preflight, approve, reject, status  

**CLI glue (shell):**

- `aether panel [path] [--serve] [--watch] [--port N]`  

**Files written:**

- `.aether/panel.html` (generated; safe to delete)  
- optional `.aether/panel-state.json` **only** for UI prefs (theme, port) — never authority  

**Tests:**

- render includes Objective/Next from fixture CURRENT  
- serve POST approve invokes aether and appends events (tmpdir)  
- no write to CURRENT on mere page load  

---

## 10. Decision options for the operator

| Choice | Meaning |
|--------|---------|
| **A — Panel P0 only** | Generate HTML; no server. Fastest honesty check. |
| **B — Panel P0+P2 (Recommended)** | HTML + localhost buttons via aether. Answers “needs a dashboard” without SaaS. |
| **C — Chat-first** | Open WebUI + propose only; risk of wrong primary metaphor. |
| **D — Stay CLI** | Re-teach; likely fails your own tester feeling again. |

**Recommendation (original):** **B** (HTML + localhost).  

**Operator decision (2026-07-27):** ship **E — TUI first** as the boring fix for
missing buttons. Name: **Project Panel** (`aether panel`). Same projection layer
writes `.aether/PANEL.md` + `panel.html` scaffolds for later GUI-friendly
surfaces. Keep CLI sovereign. Do not call it a wizard; do not call it Club-cortex.

---

## 11. One-sentence thesis

> The architecture doesn’t forbid a dashboard; it forbids a **second source of truth**. A dashboard that only projects files and shells out to `aether` is an Interface Layer feature — not a betrayal of Mechanicall.

---

## References (internal)

- `CORE_PRINCIPLES.md`  
- `ARCHITECTURE.md` § Interface Layer  
- `NOT-IMPLEMENTED.md`  
- `docs/DISTRIBUTE-MECHANICALL-ALPHA.md`  
- `docs/UI-forking-PR.md`  
- `docs/PERSONAL-LLM-LAYER.md`  
- `research/speculative/CLUB-CORTEX-SHAPE.md` (GUI at edge)  
- Session feedback: CLI alpha too CLI for even one technical tester  

## External patterns (inspiration, not dependencies)

- Local-first UIs that treat files as truth (Obsidian-style vaults; static projection of state)  
- “Thin client over local tools” rather than SPA-as-backend  
- Club-cortex direction already assumes GUI at the edge, desktop as backend — Panel is the smallest honest edge GUI for one folder  
