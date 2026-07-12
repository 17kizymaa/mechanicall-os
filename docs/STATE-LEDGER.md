# STATE LEDGER — instrumenting the input side

**Status:** shipped 2026-07-12 (`aether session`) · companion to [[RHIZOME]].

## The correction that produced this

RHIZOME captures **outputs** — seeds, ideas, the exhaust of creativity. The Nah-x3 correction from the design session: the input side is a different thing entirely. Creativity here is **conditioning-based, not retrieval-based**. A context window doesn't take notes on the prompt; it is *conditioned* by it — the prompt becomes the shape of everything generated afterward. Music works the same way on the author: the track loads the state, and generation happens *as* that state. "I become the context."

Corollary — the unit of chaos: structure organises, but it doesn't generate. Generation needs entropy the system didn't put there. So the OS must not try to contain the river. **The OS's job is to be the banks, not the river.** Log what went in; harvest what came out; leave the middle gloriously unmanaged.

## The mechanism: `.session.md`

A sidecar per project. `aether session "…"` appends a timestamped line; no arg shows the tail.

```
cd ~/reel
aether session "listening: <track> — <album>"
aether session "made: cut v3, 0:00–0:31, grain pass"
```

Convention (loose, greppable, not enforced): prefix input lines `listening:` and output lines `made:`. The Rival Editor ([[ADVERSARY]]) also appends its transcripts here.

## What it becomes

- **Conditioning map** — over weeks the ledgers show which albums reliably load which mode, which tracks produce which visual grammar. `grep -h "listening:" */.session.md` is the whole query language.
- **Prompt playlists** — the map inverts into a tool: before a client edit, load the playlist that induces the right state, the way you'd load context before a generation. Musicians warm up; this is the editor's version, documented, so it compounds.

## The listening experiment (R&D protocol, no build needed)

1. One track, voice recorder on, narrate the images as they arrive — no editing, no judging, pure transcription of what the language says.
2. Same track again three days later. Compare.
3. What's **stable** across both listens = the fixed translation-layer vocabulary. What **differs** = the chaos unit itself — the part no system should touch.

Results are seeds: pipe them in with `aether seed`.
