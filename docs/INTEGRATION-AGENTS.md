# Agent integration recipe (v0.2 alpha)

One recipe for any agent that can read files and run shell commands
(Grok Build, Claude Code, Codex, plain AGENTS.md, etc.).

Mechanicall does **not** replace your coding agent. It sits underneath as an
authority and refusal protocol.

## Required agent contract

Copy into the project's `AGENTS.md` (or equivalent):

```markdown
## Mechanicall authority (required)

1. Read `CURRENT.md` before consequential work.
2. Before any consequential action id, run:
   `aether preflight <action-id>`
3. If preflight exits non-zero: **stop**. Do not work around it.
4. After producing work product, register it:
   `aether artifact <path> --action <action-id> --status produced`
5. **Never** run `aether approve` or `aether reject`.
6. Wait for a human to review and approve (or reject) explicitly.
7. Silence is never permission. Seeds and chat history do not override CURRENT.
```

## Minimal sequence

```bash
aether current                 # inspect binding authority
aether preflight write-tests   # must exit 0 before work
# ... agent does only write-tests ...
aether artifact artifacts/tests.txt --action write-tests --status produced
# human: aether approve "tests green"
# or human opens: aether panel  (Approve button)
```

Humans should prefer **`aether panel`** for day-to-day control. Agents keep using the CLI contract above.

## Refusal demo (must pass)

```bash
# With Prohibited including deploy-production and Next: write-tests
aether preflight deploy-production   # → REFUSED, exit 1
aether preflight write-tests         # → ALLOWED, exit 0
```

See `examples/dev-task/` and `examples/alpha-demo/`.

## What the agent must refuse itself

Even without preflight, agents should not:

- invent a new **Next** action;
- clear **Prohibited** entries;
- call `approve` / `reject`;
- treat model proposals as authority.

Optional personal LLM helpers may **draft** CURRENT changes only; a human
applies them. See [PERSONAL-LLM-LAYER.md](./PERSONAL-LLM-LAYER.md) and
`examples/propose-current/`.
