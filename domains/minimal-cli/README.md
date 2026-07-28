# Minimal CLI domain

**Root = this directory** (or any folder with `CURRENT.md`).

```bash
cd domains/minimal-cli   # or your project root
export OPENROUTER_API_KEY=...   # or GROQ_API_KEY — docs/FREE-API.md
aether desk                 # terminal chat (default)
```

Type normally to chat with the model (propose only).  
Slash commands for the file/authority plane:

| Cmd | Action |
|-----|--------|
| `/c` | show CURRENT |
| `/e` | edit CURRENT |
| `/n` `/p` | Next + preflight |
| `/w` | save last reply → `.aether/propose-CURRENT.md` |
| `/clear` | clear chat memory |
| `/quit` | leave |

Empty line is not yes. Model never approves.  
Optional: `aether desk --keys` for old single-key mode.
