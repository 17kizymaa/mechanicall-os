# Alpha demo (≤5 minutes)

Disposable proof of Mechanicall OS v0.2:

1. Authority (`CURRENT.md`)
2. Refusal (`preflight deploy-production`)
3. Allowed action (`preflight write-tests`)
4. Artifact registration
5. Human `approve`
6. Inspect with `cat` / `git diff`

## Run

From repo root:

```bash
sh scripts/alpha-demo.sh /tmp/my-alpha-demo
cd /tmp/my-alpha-demo && aether panel   # daily surface with action buttons
```

Or manually in a throwaway directory using `examples/dev-task/` as a template.

After onboard/demo, `.aether/PANEL.md` and `panel.html` are projections of the same
authority state (scaffold for editor/browser later).

## What this is not

No LoRA, Club-cortex, hosted service, or sandbox claim. See
[docs/ALPHA-LIMITATIONS.md](../../docs/ALPHA-LIMITATIONS.md).
