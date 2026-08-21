# GATE-CONTRACT — LOAD then STREAM

**Not Decide. Not Yes.** Instrument only. Two-tap + Why stays on Decide.

## Why two phases

myarch may be asleep. WAKE sends a magic packet. Ollama then **loads** `personal-llm-sft-v4` into VRAM (timeout). Only then do tokens exist. Today `write_gate` has `idle | warm | gate | quiet` and the face lights 16 LEDs during stream. Sitters cannot tell “still booting” from “still thinking” (T4).

## States (engine)

Written to bound pocket `.aether/gate.json`. Not CURRENT.

| state | Face label | Bar | Meaning |
|-------|------------|-----|---------|
| `quiet` | QUIET | 0 / 16 dark | No desk, or after stream. |
| `idle` | IDLE | 0 | Desk up (`/api/tags` 200). Model may not be in VRAM. |
| `queued` | QUEUE n | 0, count in LCD | Extra Send while a generate owns the desk. |
| `load` | LOAD | amber fill 0→16 against timeout | Weights paging in. |
| `warm` | WARM | amber 4/16 | Request accepted; first token not yet. Optional; may skip if LOAD already did this. |
| `gate` | STREAM | purple steps 1→16 on tokens | Streamed generate. Keep key `gate` so old readers work. |
| `quiet` | QUIET | 0 | Done or refused. |

Do **not** add `…` on SEND. Do not rename Send to GATE.

## Sequence (one Send)

```
WAKE (optional, strip button)     → wol-pi POST. Not GATE. Not Yes.
desk_probe                        → idle or quiet
LOAD                              → POST /api/generate keep_alive OR poll GET /api/ps
                                  → timeout 60s (engine). On timeout: quiet + note, not Yes.
STREAM                            → existing token on_chunk → write_gate(gate, step)
quiet
```

LOAD may start **after WAKE without a Send** (T5: background load, niced). That is still not Yes. LCD shows LOAD. Desktop stays the operator’s.

## Queue

One generate at a time on myarch.

- Second Send while `load`/`gate`: append to pocket `.aether/desk-queue.json` (focus + user text, no CURRENT dump). Face: QUEUE n.
- When STREAM quiets: pop one, run LOAD-if-needed then STREAM.
- Never write CURRENT from a queued job.
- Never auto-open Decide.

## Timeouts (engine, not Yes)

| Phase | Suggest | On fire |
|-------|---------|---------|
| WAKE wait for `/api/tags` | 90s | strip stays sleeping; GATE quiet |
| LOAD (`/api/ps` has model) | 60s | quiet + “desk did not load”; Send not retried unless they tap |
| STREAM first token | 30s after LOAD | quiet + note |
| STREAM total | existing generate timeout | quiet |

## Desk niceness (myarch, not APK)

One niced Ollama generate. Implementation is ops: systemd `Nice=10` on the ollama unit, or `OLLAMA_NUM_PARALLEL=1`. Phone queue is the product truth. Do not start a second generate to “feel faster.”

## `write_gate` change (02)

```python
ALLOWED = {"idle", "warm", "gate", "quiet", "load", "queued"}
```

`GateStrip` in `SeatTheme.kt`:

- `load` → label LOAD; LEDs **amber** (`SeatPalette.Lcd`) fill by `step/steps`.
- `gate` → label STREAM; LEDs **purple** as today.
- `queued` → label QUEUE; LEDs dark; count in LCD.
- Never typing dots.

B7 in BEHAVIOURS.md currently says IDLE/WARM/GATE/QUIET. 02 updates the scorer to accept LOAD/STREAM as the busy states (still fail on `…`).

## Never

- LOAD or STREAM as Yes
- Background load writing PROPOSE or CURRENT
- Funnel / public Ollama to skip LOAD
- Mixing LOAD progress and token steps on one undifferentiated 0–100 bar (T4 Reject)
