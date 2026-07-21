# RHIZOME — phone card

**Repo:** `~/mechanicall-os` · **Commit:** `2b85aed` · **Day 3 (2026-07-12)**  
**Doctrine:** Capture is sacred; structure is deferred. Zero decisions at entry. Under two seconds.

---

## Daily loop (use this now)

| When | What | Command / action |
|------|------|------------------|
| Thought hits | Plant it. No naming, no folders. | **Super+S** or `aether seed "…"` |
| Need a shove | Draw one oblique line | `aether spark` |
| Start a creative session | Log what *conditioned* you | `cd ~/reel` → `aether session "listening: …"` |
| After a cut / pass | Log what you *made* | `aether session "made: …"` |
| Later / coffee | Browse seeds only — **do not file yet** | open `~/inbox.md` |
| Morning sort | Propose then approve | `aether garden` → check `[x]` → `aether garden apply` |
| At the desk | Counter-treatment | `aether rival --track "…" --read "…"` |
| Want the map | Wiki-link network as Mermaid | `aether graph` |

**Golden rule:** never decide *where* a thought goes at capture time. Filing is deferred (gardener, not you-at-the-desk).

---

## Paths (muscle memory)

| Thing | Path / env |
|-------|------------|
| CLI | `aether` → `~/.local/bin/aether` (from `mechanicall-os/aether`) |
| Seed inbox | `~/inbox.md` (`$AETHER_INBOX`) |
| Spark deck | `~/prompts.md` (`$AETHER_SPARKS`) — one line per line |
| Session ledger | `./.session.md` in the project cwd |
| Hotkey script | `scripts/seed-hotkey.sh` |
| Super+S | XFCE custom shortcut → that script |
| Design docs | `docs/RHIZOME.md` · `docs/STATE-LEDGER.md` · `docs/ADVERSARY.md` |

---

## Six layers — status

1. **seed** — ✅ ship. `aether seed "thought"` · also stdin: `echo x \| aether seed`
2. **hotkey** — ✅ ship. Super+S (xfce4-terminal fallback if no rofi/zenity)
3. **voice** — ⏭ after 1–2 prove out in daily use (whisper.cpp, not installed)
4. **graph** — ✅ ship. `[[wiki-links]]` → Mermaid, no DB
5. **spark** — ✅ ship. random line from `~/prompts.md`
6. **garden** — ✅ ship. `aether garden` → `~/inbox-proposals.md` → apply `[x]` only. LLM: `XAI_API_KEY` or Ollama.

---

## Companion systems (not capture)

### State ledger (inputs)
Creativity here is **conditioning**, not retrieval. Log the river’s banks:
- `listening:` = what loaded the state  
- `made:` = what came out  
Middle stays unmanaged. OS = banks, not river.

### Rival Editor (adversary)
- **v0** — ✅ `aether rival --track T --read "…"`; prompt verbatim; logs to `.session.md`
- **v1** — export-folder watcher → one-line challenge (not built)
- **v2 live mix** — **PARKED** (income gate). Future: stream identity merge note preserved

### Gates (unchanged)
Reel · DMs · scout batch two. RHIZOME is R&D infrastructure, not a substitute for gates.

---

## How to grow it (practice order)

1. **This week:** Super+S every time a thought appears. Don’t open inbox to reorganize. Just plant.
2. **Sessions:** In `~/reel` (or any project), `listening:` before work, `made:` after each meaningful cut.
3. **Spark deck:** When a good oblique line appears, append to `~/prompts.md` — never curate at entry.
4. **Prove layers 1–2** in real use for several days before voice or garden.
5. **Then:** voice hotkey → garden + Rival v0 (shared API-key work).

### Listening experiment (no build)
One track → narrate images aloud → seed the transcripts. Repeat same track three days later. Stable = vocabulary. Differs = chaos unit (leave it alone).

---

## One-liners to memorize

```
aether seed "…"
aether spark
aether session "listening: track — album"
aether session "made: cut v3, 0:00–0:31"
aether graph > graph.mmd
```

Empty `aether` (no args) → status of the current tree.  
Empty `aether session` → tail of this project’s ledger.

---

## Housekeeping notes from Day 3 ship

- Principle locked in `CORE_PRINCIPLES.md`: capture sacred / structure deferred  
- Home monorepo submodule pointer for mechanicall-os may lag (bump on next hygiene pass)  
- Optional polish: `pacman -S zenity` (or rofi) for a nicer seed popup  
- Claude Code session that built this: `6bcb5ae4-e896-4069-b9a7-de456a3334df` (org access cut mid follow-up)

---

*Open this file on phone. Practice the daily loop. Follow up in Grok when you want the next layer or a bug fix.*
