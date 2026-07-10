#!/usr/bin/env python3
"""
DEPRECATED - Centralized into Grok CLI.

The /codebase-review functionality is now fully centralized in the Grok CLI using its native in-built parallel subagent swarms.

Run the Grok CLI and use:

  /codebase-review [target]

It will use the CLI's agents in parallel (swarm) to review against the doctrines (loaded from AGENTS.md, CORE_PRINCIPLES.md, etc.), produce artifacts, etc.

No more external API scripts or custom swarms needed.

See /root/.grok/skills/codebase-review/SKILL.md for the implementation.

This keeps everything inside the CLI's agent system as requested.
"""
import sys
print("DEPRECATED: Use /codebase-review inside the Grok CLI instead.")
print("It now handles everything with native parallel subagent swarms.")
sys.exit(0)
