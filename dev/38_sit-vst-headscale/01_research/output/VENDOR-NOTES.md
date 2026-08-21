# VENDOR-NOTES — genuine frame + Headscale + GATE

**Not CURRENT. Not Decide.** Research for `sit-vst-headscale`. CURRENT law outranks vendor taste.

Paper Suggesting steal (Docs / Word / Overleaf / HackMD) remains `dev/37_sit-join-workshop/01_research/output/VENDOR-NOTES.md`. This file adds the unparked vendors.

## Steal (visual) — Camel Space is a *gate*, not a chat

Source: [Sound on Sound, Nov 2005 — Camel Space](https://www.soundonsound.com/reviews/camel-space-dvr2); [Splice plugin page](https://splice.com/plugins/1992-camelspace-vst-au-by-camel-audio); Camel Audio manuals (Scribd scan of *Camel Space Manual*).

Camel Space (Camel Audio, ~2005) is a multi-effect whose **heart is a trance-gate sequencer**: up to 128 steps in eight banks, modulating pan, filter cutoff, and a one-button output attenuator named the **trance gate**. The SOS reviewer called out an “attractive, well thought-out interface,” an X-Y pad, rotary controls, MIDI learn, and a randomise that stays usable. The look of the era: dark metal rack, amber/orange LCD, rectangular step pads.

**What we steal (grammar, not DSP):**

| Camel Space | Sit |
|-------------|-----|
| Plugin *editor* hosted by a DAW | Sit hosted by Android OEM (`resizeableActivity`). We are the editor, not the OS window. |
| Dark rack around modules | Compact metal *frame* (title, LCD, bevel). Fill the activity. |
| Trance-gate step row | GATE strip: LOAD fills amber; STREAM lights purple steps. The product word GATE is this steal. |
| Preset name in the header | Bound folder name in the title bar. DIR/FILES = slots. |
| Module sections (filter, delay, …) | Plan / Draft / Decide / Receipt as banks. Paper is the *score* inside the rack. |

**What we do not steal:**

- Audio DSP, 128-step editors as a page, knobs that are not functions (verb museum).
- Traffic-light OS window buttons (those are DAW *host* chrome, not the plugin editor).
- A painted 360×560 plugin card on a black letterbox (the 0.8.0-vst fail; B9).
- JUCE as a second runtime. Compose stays (S9 / S15).

Steinberg VST: the editor is a **child window of the host**. Honest mapping = fill our activity; let Samsung pop-up / split-screen be the host frame. `resizeableActivity=true` already in `AndroidManifest.xml`.

Licensing: we *read* public chrome. We do not copy Camel Audio bitmaps or trademarks into the APK. Palette + layout grammar only.

## Steal (control plane) — Headscale preauth

Sources: [Headscale registration](https://headscale.net/stable/ref/registration/); [Getting started](https://headscale.net/stable/usage/getting-started/).

- Two ways to join: **web auth** (browser + admin `headscale auth register`) or **preauth key** (non-interactive).
- Default preauth: **once**, **one hour**. Operator mints; sitter pastes.
- Tagged keys: `headscale preauthkeys create --tags tag:stranger` — node lands under `tagged-devices`. Matches CURRENT `tag:stranger`.
- Client: `tailscale up --login-server <URL> --authkey <KEY>`.
- **OIDC is extra login.** CURRENT Reject. Do not enable.
- Username must not end with `@` (Headscale OIDC footnote — still true for policy).

**IdP-less, not key-less.** The sitter never opens Google/Apple. The operator still mints a key. Key never in git / never baked in APK.

**login-server must be LTE-reachable *before* the phone is on the tailnet.** MagicDNS of Headscale itself is a chicken-egg. Use public HTTPS (wol-pi + Caddy/name, or a small always-on box). Health: `https://<login-server>/health`.

## Steal (userspace) — tsnet, not VpnService

Sources: [tsnet](https://pkg.go.dev/tailscale.com/tsnet); [Userspace networking](https://tailscale.com/docs/concepts/userspace-networking); [Tailscale Android gomobile](https://tailscale.com/blog/android); GitHub [issue #10126](https://github.com/tailscale/tailscale/issues/10126) (userspace mode on the *official Android client* is still a feature request).

`tsnet.Server` runs a gVisor userspace stack in-process:

- `ControlURL` = Headscale login-server (else Tailscale Inc — we must set this).
- `AuthKey` = pasted preauth (RAM only; not `tailnet.json`).
- `AdvertiseTags` = `tag:stranger`.
- `Ephemeral` = true for sitters (node dies with the process; re-paste).
- `HTTPClient()` dials MagicDNS (`http://myarch:11434`, `http://wol-pi:7077/wake`).
- `Listen` / `Up` for twin HTTP on the phone.
- `ListenFunnel` = **Reject** (CURRENT: not Funnel / not public Ollama).

Official Tailscale Android app = **VpnService** (device-wide). We embed tsnet. Other apps stay on LTE.

**JNI path (honest leftover from 37):** Chaquopy cannot run Go. 02 ships a gomobile-bound Go wrapper the Kotlin face calls; Python `urllib` to `myarch` only succeeds today via USB reverse / LAN / a *device-wide* Tailscale — i.e. the current “connected” is a lab lie. `join_accept` must not set `status=connected` until `tsnet.Up` succeeds.

## Steal (LOAD) — Ollama is a boot, then a stream

Sources: Ollama HTTP — `GET /api/ps` (models in memory); `POST /api/generate` with `stream: true` (token chunks); `keep_alive`.

`personal-llm-sft-v4` on myarch (32 GiB, 0 swap) may page into VRAM after WAKE. That interval is **LOAD**, not thinking. Mixing it with token LEDs is how sitters think the model hung (T4).

Engine today (`write_gate`): states `idle | warm | gate | quiet` only. 02 adds `load` (and optional `queued`). STREAM may keep the existing `gate` key so old `gate.json` readers do not explode, but the **face** must say STREAM.

Desktop niceness is **myarch ops**, not the APK: one generate; extra Sends queue on the phone; never auto-Yes.

## Do not steal

- Imagine-mocks as visual law (T7 Reject).
- ChatGPT canvas / bubbles as identity.
- Tailscale Funnel, public `:11434`, public `/wake`.
- Headscale OIDC / web-auth as the sitter path.
- `aether_pocket_serve.py` Yes/Not-yet POST as the operator twin (that face *writes*). Twin is GET/read.
- Binding mechanicall-os (B10).
- Camel Audio assets in the APK.
