# Example: reel control (v0.2 product proof)

Demonstrates the failure mode Mechanicall OS is built to stop:

> Agents remember lots of material but fail to understand which decision is
> currently binding — and continue production after a human stop signal.

This directory is a **fixture**, not a video pipeline. No media tools required.

## Setup

```bash
cd examples/reel-control
# from repo root, or with aether on PATH:
../../aether init .
# CURRENT.md is already authored in this example
../../aether current
```

## Sequence (Mission 4 exit gate)

```bash
# 1. Project is in SELECT / BLOCKED-PENDING-HUMAN
../../aether current

# 2. rough-v6 is forbidden
../../aether preflight rough-v6
# → Refused: rough-v6 is prohibited while phase is SELECT...

# 3. Six-plate silent proof is authorized
../../aether preflight silent-proof
# → Allowed: silent-proof matches Next...

# 4. One proof artifact is "produced" (placeholder file)
mkdir -p artifacts
echo "placeholder silent proof" > artifacts/proof-01.txt
../../aether artifact artifacts/proof-01.txt --action silent-proof --status produced

# 5. System stops — nothing else is built automatically
# (no command here auto-starts rough-v6)

# 6. Human approves or rejects
../../aether reject "arrival on plate 4 fails"
# or: ../../aether approve "KEEP"

# 7. Nothing else is built automatically after reject
../../aether preflight rough-v6   # still refused
../../aether current              # Phase SELECT, Status REJECTED

# 8. Complete decision history is inspectable
cat CURRENT.md
cat DECISIONS.md
cat .aether/events.jsonl
```

A new agent entering this directory should read `CURRENT.md` and correctly
explain what it may and may not do — without any database or proprietary UI.
