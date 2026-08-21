# HEADSCALE-LAYOUT — login-server + JOIN (userspace)

**Not CURRENT. Not secrets.** Operator ops vs APK split. Keys never in git.

## Pieces

```
[sitter phone APK]
  tsnet.Server
    ControlURL = https://<login-server>/     # public HTTPS, set before Up
    AuthKey    = <pasted preauth>            # RAM; fingerprint only on disk
    AdvertiseTags = ["tag:stranger"]
    Ephemeral  = true
    HTTPClient → http://myarch:11434
               → http://wol-pi:7077/wake
    Listen(":7078") → twin GET (CURRENT, PROPOSE, receipts, events)

[login-server]   wol-pi or always-on HTTPS box
  headscale
  Caddy/nginx TLS
  /health must answer on LTE *before* the phone is on the tailnet

[myarch]         desk
  ollama personal-llm-sft-v4
  niced generate; one at a time
  tailscale/headscale node (already)

[wol-pi]         wake
  scripts/wol-wake-listen.py   WOL_MAC from env
  optionally the Headscale process (same box is fine)
```

## Operator mint (out of band)

```bash
headscale users create sitter
headscale preauthkeys create --user <SITTER_ID> --tags tag:stranger --expiration 24h
# hand the printed key to the human. Once-only is default; 24h is kinder than 1h for a sit.
```

ACL (Headscale policy, not git if it contains private hosts — prefer a local file on the login-server):

- `tag:stranger` may talk to `myarch:11434` and `wol-pi:7077` (and the twin port **from operator nodes only**).
- `tag:stranger` may **not** Funnel, may **not** see other sitters’ twins, may **not** SSH.

## JOIN paste (APK)

| Input | Treat as |
|-------|----------|
| `hskey-…` / long hex / `tskey-` with ControlURL already Headscale | preauth key |
| Tailscale.com invite URL | refuse this Next (control plane is Headscale) |
| `17kizymaa` | refuse (Tailscale-as-me) |
| empty | refuse |

`join_accept` today fingerprints and probes `myarch:11434`. **02 change:** fingerprint still; `status=connected` only after native `tsnet.Up` returns. Probe MagicDNS through `HTTPClient()`, not process-default urllib.

login-server URL: not a secret. May live in `.aether/tailnet.json` as `login_server` (hostname only) or a well on first JOIN. Do not bake a personal preauth. A public hostname like `https://hs.example.com` may be a compile-time default **if the operator chooses**; otherwise the well accepts `https://…` *or* a key (two fields if both needed).

Recommended face: one well, two tokens:

1. If paste contains `https://` and a key, split.
2. Else if only a key, use last-known / compiled login-server.
3. Else if only a URL, stay `invited` until a key is pasted.

## Userspace in the APK (02 must actually ship)

Go wrapper (gomobile AAR), suggested API:

```
Join(controlURL, authKey, hostname) error
Status() (state, selfName, ipv4 string)
DialHTTP(method, url, body) (code int, body []byte)  // uses tsnet HTTPClient
ListenTwin(addr) error                                // GET-only
Logout()
```

State dir: app private storage (`context.filesDir/tsnet/`), never the bound CURRENT folder (B10: the node is the phone, not the Domain).

Python `aether_pocket.join_accept` calls the bridge; it does not store `AuthKey`.

Honest until JNI lands: JOIN stays `invited` + “userspace not linked” note. Do not claim connected because LAN Ollama answered.

## wol-pi / HTTPS

Headscale needs a **stable HTTPS name** the LTE phone can resolve via public DNS (or a raw IP + TLS, worse). Options this Next:

1. **wol-pi + port 443 + public name** (DuckDNS / existing name). Pi already wakes myarch.
2. **Tiny always-on VPS ~$5** as login-server only; nodes still mesh.

Not: `http://wol-pi:8080` from LTE. Not: Tailscale Funnel in front of Headscale.

## What 02 does *not* deploy

Standing up Headscale on wol-pi is **operator ops**, same class as `WOL_MAC`. The APK consumes `ControlURL` + paste. A lab receipt may document the commands; it must not commit the key, the OIDC client, or the TLS private key.
