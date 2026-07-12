# ADVERSARY — the Rival Editor

**Status:** v0 **CLI shipped** 2026-07-12 (`aether rival`) · v1 spec'd · v2 **PARKED per income gate** · companion to [[RHIZOME]] and [[STATE-LEDGER]].

## What it is

Every other agent in this system lives backstage — scout, drafter, gardener operate before or after the creative act. The Rival Editor sits **inside** the act, in real time, as a counterpart. It is adversarial architecture at human scale: the generator is the author at the mixing desk; the adversary's job is not to be correct but to be *other*.

Deep function: a strong signature calcifies into ruts precisely because nothing pushes back. The adversary is the unit of chaos, institutionalised. Not an enemy — an **anti-convergence engine**. Its one law: never converge.

## v0 — turn-based adversary ✅ shipped

Feed it the track (title, structure, narration from the listening experiment) plus the author's visual read. It must return the interpretation the author would *not* make: timestamped visual calls, a counter-treatment.

```
cd ~/reel
aether rival --track "JRJRJR" --structure "cold/hook/breath/peak/out" \
  --read "VHS grain, dark cold open on downbeat"
# optional: --narration "…"  |  --no-log
```

- System prompt: `skills/rival-editor/PROMPT.md` (verbatim — do not soften).
- CLI: `aether rival` → `python/aether_rival.py`.
- Backend: `XAI_API_KEY` (SpaceXAI / api.x.ai) preferred; else Ollama (`AETHER_OLLAMA_MODEL`).
- Session transcripts append to the project's `.session.md` ([[STATE-LEDGER]]).
- Shares API-key plumbing with the RHIZOME gardener (`python/aether_llm.py`).

## v1 — session watcher

A watcher on the exports/render folder sends each committed cut to a vision-capable model (frame grabs), and the adversary returns a **one-line challenge** appended to `.session.md` — during the session, filesystem-native, doctrine intact. Needs: export-dir watch (entr or poll, same pattern as `aether watch`), frame extraction (ffmpeg), vision model call.

## v2 — live mixing (PARKED)

True live sparring: audio features (BPM, section detection — librosa can feed this) drive the model's semantic directives against the author's hands on the desk. Two mixers, one human.

**Parked per the income gate.** But noted: v2 quietly resolves the identity split from the media audit — streaming adversarial mix sessions is the act where the Kick streamer and the alt music editor stop being parallel tracks and become one performance. The gaming channel's audience infrastructure serves the music identity. Possibly the whole channel concept. Revisit when the gate opens.

## Gates (unchanged by any of this)

Reel · DMs · scout batch two. This document is R&D notebook material, not gate ledger material.
