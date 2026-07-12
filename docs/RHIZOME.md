# RHIZOME — the capture layer

**Status:** design locked 2026-07-12 (Day 3) · layers 1, 2, 4, 5 shipped same day · provenance: design session with CC; this file is the repo-side record of that session. If the original chat draft of RHIZOME.md surfaces, diff it against this and merge.

## The one locked principle this adds

> **Capture is sacred; structure is deferred.**

Getting a thought into the filesystem must cost **zero decisions** and **under two seconds**. Filing, naming, linking, sorting — all of it happens later, and never by the author at the moment of capture. Any feature that adds a decision to the capture path violates doctrine.

This is the fix for the rbrbbrbrb problem: the monster thinks faster than hands, and every "where does this go?" at entry kills a thought. The CLI was never the enemy; the filing tax was.

Recorded in `CORE_PRINCIPLES.md` as a locked principle.

## Why "rhizome"

Any node connects to any node; no hierarchy. Atomic notes plus links implement exactly this, and plain markdown on a filesystem does it better than most apps — grep doesn't care about hierarchy either. No database. Doctrine intact.

## The six layers

### Layer 1 — `aether seed` ✅ shipped
Append-only capture to a single global inbox (`$AETHER_INBOX`, default `~/inbox.md`). Timestamped line, no prompts, no categories, no filenames. Also reads stdin, so anything can pipe into it.

```
aether seed "cut on the snare, not the kick"
echo "some thought" | aether seed
```

### Layer 2 — global hotkey ✅ shipped
`scripts/seed-hotkey.sh` pops an input line over whatever you're doing and pipes it to `aether seed`. Thought → file in under two seconds. Prefers rofi/dmenu/zenity if installed; falls back to a small floating xfce4-terminal prompt (works with zero new deps). Bind it to a key in XFCE settings (see script header).

### Layer 3 — voice capture (whisper.cpp) ⏭ next, only after 1–2 prove out
Speaking is 3–4× faster than typing. Local whisper.cpp, hotkey-started recording, transcript piped straight to `aether seed`. Deliberately **not** built yet — build order below.

### Layer 4 — wiki-links + `aether graph` ✅ shipped
`[[wiki-links]]` in any scoped markdown are the rhizome's connective tissue: greppable, git-diffable, no database. `aether graph` renders the link network as Mermaid to stdout:

```
aether graph > graph.mmd     # or pipe into anything that renders Mermaid
```

### Layer 5 — spark deck (`prompts.md`) ✅ shipped
One oblique line per line in `~/prompts.md` (`$AETHER_SPARKS`). `aether spark` deals one at random. Costs nothing; started 2026-07-12 with "cut to the part of the song that doesn't have lyrics" — the best sentence the old proposal ever produced.

### Layer 6 — distill as gardener 📋 spec
The crucial other half of the bargain. Nightly (or on demand), distill clusters the day's seeds from the inbox and **proposes** destinations — project, note file, spark deck, trash. Morning review is a two-minute yes/no pass over the proposals; nothing moves without approval. You never file a thought again; you only approve the sorting with coffee.

Implementation sketch: `aether garden` reads `~/inbox.md` entries since last run, clusters (LLM call — this is the one place a model enters the loop), writes `~/inbox-proposals.md` with one `- [ ] seed → destination` line per seed. Approval = check the box; a follow-up pass moves approved seeds and appends `[[links]]`. Rejected proposals stay in the inbox. All plain files, all diffable.

## Build order (locked in the design session)

1. Layers 1 + 2 — a single evening each; kill ~80 % of the friction on their own. **Ship before touching voice.** ✅ done
2. Layer 5 spark deck — free. ✅ done
3. Layer 4 graph — cheap, doctrine-pure. ✅ done
4. Layer 3 voice — only after 1–2 are proven in daily use.
5. Layer 6 gardener — spec'd above; needs an LLM hook, so it lands with the API-key plumbing that [[ADVERSARY]] v0 also needs.

## Companion documents

- [[STATE-LEDGER]] — the *input* side: RHIZOME captures outputs; the state ledger instruments what conditioned them.
- [[ADVERSARY]] — the in-act counterpart: the Rival Editor.
