# personal-llm peer REPL — on **this** hardware

**Shape:** peer agent (sft-v4) for proposals/synthesis.  
**Where it runs:** inference + preferred REPL on **this host** (not a cloud API).  
**Remote access:** LAN / Tailscale **into** this host.

## Shell integration (default)

`aether shell` **defaults to peer** (`/agent peer` + `personal-llm-sft-v4`).

On start it:

1. Loads peer agent profile  
2. Probes Ollama: env → `.aether/ollama-host` → `127.0.0.1` → Tailscale self IP  
3. Pins provider `ollama`

```bash
aether shell /path/to/Domain     # peer by default
/peer-serve                      # how THIS host serves remotes
/ollama-host http://100.x:11434  # pin remote personal-llm host (saved in project)
/ollama-host local               # back to loopback
/agent grok                      # opt-in real coding agent
```

## Make Ollama reachable beyond loopback

Today many installs still show `127.0.0.1:11434` only. For Tailscale/LAN:

### NixOS (preferred)

`nix/modules/ollama-personal.nix` defaults:

- `mechanicall.ollama.host = "0.0.0.0"`
- firewall opens port `11434` when not loopback-only

Rebuild host after enabling the module, then:

```bash
ss -ltnp | grep 11434
# expect 0.0.0.0:11434 or *:11434
```

### Manual (no rebuild yet)

```bash
# stop existing loopback-only ollama if needed, then:
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

## Remote clients (other machines)

**A — API only** (remote aether talks to **this** host’s Ollama):

```bash
export AETHER_OLLAMA_HOST=http://100.x.y.z:11434   # this host Tailscale IP
export AETHER_OLLAMA_MODEL=personal-llm-sft-v4
export AETHER_LLM_PROVIDER=ollama
aether shell .
/agent peer
```

**B — full REPL on this host** (TTY over Tailscale):

```bash
ssh user@100.x.y.z -t 'cd /path/to/Domain && aether shell . --provider ollama --model personal-llm-sft-v4'
```

## Security

- Tailscale preferred over raw public bind.
- Peer is propose-only; still never auto-approves CURRENT.
- Do not expose Ollama to the open internet without auth/firewall.

## Related

- Profiles: `references/aether-shell-agent-peer.md`
- Shell: `/agent peer` · `/peer-serve`
- Env: `AETHER_OLLAMA_HOST`, `AETHER_OLLAMA_MODEL`, `OLLAMA_HOST` (server bind)
