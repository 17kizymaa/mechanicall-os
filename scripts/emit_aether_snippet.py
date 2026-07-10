#!/usr/bin/env python3
"""Emit shell integration for the aether command.

Similar spirit to local-navigator's emit_bashrc_snippet.py

Usage:
  python3 scripts/emit_aether_snippet.py >> ~/.bashrc
"""

import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

SNIPPET = f'''# ---- aether (awareness-agent) ----
export AETHER_ROOT="{ROOT}"

# Primary command
aether() {{
  PYTHONPATH="$AETHER_ROOT" python3 -m aether "$@"
}}

# Convenience aliases (feel free to customize)
alias ae='aether'
alias aeu='aether update'
alias aes='aether status'

# Example: quick context peek
context() {{
  if [[ -f .context.md ]]; then
    cat .context.md
  else
    echo "No .context.md here. Run: aether init"
  fi
}}
# ---- end aether ----
'''

print(SNIPPET)
