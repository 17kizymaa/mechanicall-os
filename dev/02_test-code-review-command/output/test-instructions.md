# Test Instructions for /code-review Prototype

## Prerequisites
- This prototype (code-review script in this stage's output/).
- A target directory with some files and ideally a .context.md (run aether distill on it first if possible).
- Your SuperGrok account login (for consumer rates + Grok Heavy multi-agent).

## Step-by-Step Test (Consumer Rates Path — Recommended)
1. Run the prototype against a small target:
   ```bash
   cd /path/to/awareness-agent   # or any project
   /home/awareness-agent/dev/02_test-code-review-command/output/code-review . --output /tmp/review-prompt.md
   ```

2. Open grok.com in your browser and log in with the SuperGrok account that has your desired usage rates / Heavy access.

3. Start a new chat. If available, select Grok Heavy / multi-agent mode.

4. Copy the entire contents of `/tmp/review-prompt.md` and paste it as your first message. Send.

5. Observe the response:
   - Does it use multi-agent collaboration (may show thinking or agent perspectives)?
   - Does it reference the injected doctrines with quotes?
   - Is the review evidence-based against CORE_PRINCIPLES, AGENTS.md, etc.?

6. Save the resulting review as a Markdown artifact in the target (e.g. `reviews/code-review-2026-06-25.md`).

## Direct API Test (for comparison, uses separate billing)
```bash
# (requires XAI_API_KEY set)
# Extend the prototype or manually use the prompt with curl to api.x.ai using model grok-4.20-multi-agent + high reasoning.
```

## What Success Looks Like
- The command itself is tiny and inspectable (`cat` the script).
- The generated prompt is self-contained and doctrine-heavy.
- When used in your SuperGrok chat, it triggers Grok Heavy multi-agent to do the external evaluation.
- Review output is a clean Markdown file you can commit or treat as sidecar.

## Known Prototype Limitations (for this test stage)
- Source collection is very limited (first ~20 files, truncated).
- Doctrines path may need manual adjustment (`DOCTRINES_BASE`).
- No sophisticated scoping yet.
- No token estimation / dry-run.
- Full implementation would live in a proper scripts/ or bin/ in future stages.

Run the test and report back (or edit the prototype). This validates the rates + multi-agent + doctrines approach.
