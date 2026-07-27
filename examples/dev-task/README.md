# Example: non-reel dev task (v0.2 generality)

Shows that the authority model is **not** hardcoded to video editing.

```bash
cd examples/dev-task
../../aether init .
../../aether preflight add-postgres     # Refused
../../aether preflight write-tests      # Allowed
../../aether approve "tests green"      # Human only
# or day-to-day:
#   ../../aether panel
```
