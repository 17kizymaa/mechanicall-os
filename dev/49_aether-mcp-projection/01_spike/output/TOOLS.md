# aether MCP spike — tools

**Not Yes. Not default-on. Not EdubaWare.**  
Server: `python/aether_mcp.py` (stdlib, stdio). Bind-root = one folder.

| Tool | Does | Does not |
|------|------|----------|
| `current` | `aether current <root>` | write CURRENT; approve |
| `probe` | `aether probe <action> <root>` | write events (dry); approve |
| `propose_write` | write `<root>/.aether/proposals/<basename>` | write `CURRENT.md`; path escape |

Forbidden even if a client asks: `approve` `reject` `next` `yes` `not_yet` `deinit`.

## Opt-in (human)

Do **not** add this to a global client config from an agent. Example only:

```json
{
  "mcpServers": {
    "aether": {
      "command": "python3",
      "args": [
        "/mnt/kingston-nixos-sync/opt/mechanicall-os/python/aether_mcp.py",
        "--root",
        "/path/to/bound-folder"
      ]
    }
  }
}
```

`--root` must be **one** pocket. Operator tree is allowed for desktop inspect/propose (this Domain). Phone bind ≠ this repo still holds for the sit.

## Run tests

```bash
python3 tests/test_aether_mcp.py
```
