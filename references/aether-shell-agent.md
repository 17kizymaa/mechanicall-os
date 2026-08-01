---
name: aether-shell-legacy-pointer
description: >
  Legacy single-profile path. Prefer dual agents:
  aether-shell-agent-grok.md (real) and aether-shell-agent-peer.md (personal-llm).
tools: []
disallowedTools:
  - web_search
role: peer-propose
---

# Legacy pointer

Use:

| Role | File | When |
|------|------|------|
| **grok** (real agent) | `references/aether-shell-agent-grok.md` | Implement under Domain; full tools |
| **peer** (personal-llm) | `references/aether-shell-agent-peer.md` | Proposals / synthesis only |

Shell: `/agent grok` · `/agent peer` · auto by provider (grok_tui→grok, ollama→peer).
