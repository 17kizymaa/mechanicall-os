# Test Report — Mechanical /codebase-review (Level 1)

## Setup
- Set XAI_API_KEY (get from console.x.ai with your SuperGrok account).
- Ensure target has .context.md (aether distill recommended).
- Run from repo root or adjust paths in script.

## Basic Mechanical Run (Level 1)
```bash
export XAI_API_KEY=your_key_here
python scripts/codebase_review.py . --output /tmp/my-review.md
# Or using wrapper
./scripts/codebase-review . 
```

Expected:
- Gathers .context.md + some sources.
- Calls grok-4.20-multi-agent with high effort.
- Writes review artifact (in target/reviews/ or specified file).
- Review should reference doctrines with quotes and use multi-agent style (if the model surfaces it).

## Progressive Notes
- Current: All-in-one prompt (Level 1 autonomy — Grok gets snapshot).
- To Level 2: Extend the script to support tools= in payload + handle tool_calls responses. Implement local read/grep tools. Grok Heavy can then call back for more evidence autonomously.

## MCP
Not added yet (see design). If desired, we can add a minimal stdio MCP tool server in Python for codebase tools. It would be true to repo (Python, observable via logs/sidecars). Only on explicit approval.

## Limitations (current prototype)
- urllib is basic (no streaming yet).
- Source gathering limited.
- Error handling basic.
- Paths for doctrines are relative — tune DOCTRINES_DIR in script if needed.
- API response parsing is simplified (inspect raw if issues).

Test on a small target first. The review will be Grok Heavy's multi-agent output, saved mechanically.

Next progressive step: Add tool calling loop or MCP server.
