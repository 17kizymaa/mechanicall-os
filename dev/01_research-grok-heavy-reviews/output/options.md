# Options for /review-codebase Command (Grok Heavy via API)

All options **strictly obey** the project's Core Principles and SPEC-v0.1 (Markdown + tiny Python or POSIX sh, no hidden state, FS as truth, minimal overhead, inspectable).

## Option 1: Pure Thin Shell Client (Most Aligned with Brutalism)
- `review-codebase` or `aether review-codebase` as a single static POSIX sh script (or very small wrapper).
- Uses `curl` + `jq` (both tiny, commonly available or statically linkable).
- Gathers files with `git ls-files`, `find`, or by reading `.aether/.scope`.
- Reads doctrine .md files and target `.context.md` with `cat`.
- Calls `https://api.x.ai/v1/chat/completions` (or responses) directly.
- Writes result to stdout and/or `target-dir/reviews/review-$(date +%s).md`.
- **Pros**: Zero Python runtime dep for the core path. Perfectly `cat`/`diff`able. Matches SPEC-v0.1 "FROM scratch + busybox + entr + aether" spirit.
- **Cons**: More verbose JSON handling in sh. Harder structured outputs (can still ask for JSON in prompt and `jq` it).
- **When to choose**: When minimalism is the highest priority.

## Option 2: Tiny Optional Python Behaviour (Recommended Balance)
- `scripts/review_codebase.py` (or `bin/review-codebase`) — pure stdlib + `urllib` + `json` where possible, or document `pip install openai` / `xai-sdk` as convenience.
- Or use the official lightweight path.
- Still reads everything from FS (doctrines, .context.md, source files).
- Can support `--format json|md`, `--effort high`, `--output file.md`, `--scope .`.
- Can optionally call `aether distill` first if present (as a behaviour).
- **Pros**: Easier to handle large prompts, structured outputs, error handling, streaming. Python already exists in the project for "smart" parts (distill).
- **Cons**: Slightly heavier than pure sh.
- **When to choose**: Default for most users. Keep the sh version as an alternative in the same dir.

## Option 3: Prompts-as-Artifacts + Generic Caller
- No special command at all.
- The "command" is: 
  1. Curate a prompt file in the target (or this repo's `references/review-prompt.md`).
  2. Use a generic tiny tool (or even `curl` one-liner documented in docs) that takes a prompt file + API key and posts it.
- Doctrines stay in their .md files and are concatenated at call time by a tiny script.
- **Pros**: Even less code to maintain. Review logic lives in plain Markdown (editable by humans).
- **Cons**: Slightly more manual each time.
- **When to choose**: For extreme minimal projects or when experimenting with prompt wording.

## Option 4: aether Extension (Integration, Not Replacement)
- Add `review` subcommand to the existing aether CLI (which is already Python-assisted).
- `aether review --model grok-4.3 --effort max .`
- Reuses the project's watcher/distill infrastructure for gathering context.
- Still calls external API only.
- **Pros**: Feels native to the awareness system. Can auto-include fresh .context.md.
- **Cons**: Slightly couples the review tool to aether (acceptable if kept optional).
- **When to choose**: If the user wants one unified `aether` surface.

## Recommendation
Start with **Option 2** (tiny Python) + strong documentation of a pure-curl path.

This matches how the project already uses Python: only for the parts that benefit from it (distillation logic), while everything important remains readable .md or trivial sh.

The actual "heavy" evaluation always happens externally on grok-4.3.

## Non-Goals (per principles)
- Do not build a server, web UI, or persistent review database.
- Do not embed an LLM locally.
- Do not require the Grok Build CLI.
- Do not add heavy dependencies to the happy path.
