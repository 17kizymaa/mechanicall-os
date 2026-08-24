# tsnet userspace (JNI gap)

**Not CURRENT. Not Yes.** JOIN `connected` requires this node to be **Up**. LAN Ollama is not JOIN.

## Intent

gomobile-bind a tiny Go wrapper around `tailscale.com/tsnet.Server`:

- `ControlURL` = Headscale login-server (HTTPS, LTE-reachable *before* join)
- `AuthKey` = pasted preauth (RAM only)
- `AdvertiseTags` = `tag:stranger`
- `Ephemeral` = true
- `HTTPClient()` dials `myarch:11434` and `wol-pi:7077`
- `Listen(":7078")` for the GET-only twin
- No Funnel, no VpnService

State dir: app `filesDir/tsnet/`, never the bound CURRENT folder.

## This sit

`scripts/build-tsnet-aar.sh` is the factory. Until it produces an AAR and the APK links it, `python/aether_pocket.py` `tsnet_up()` is false unless a test marker/`MECHANICALL_TSNET_UP` is set. JOIN stays **invited**.

Do not copy Camel/Tailscale secrets into this folder.
