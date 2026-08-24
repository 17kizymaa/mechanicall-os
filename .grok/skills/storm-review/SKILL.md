---
name: storm-review
description: >
  Persistent STORM factory for mechanicall-os: isolated emulator review
  environments for chat-session subagents scoring the original sit APK.
  Never Confirm. Never A33. Never aether approve. Use when asked for
  STORM, storm-0, emulator review, or mass-app subagent review.
---

# STORM review (developer infrastructure)

The **original sit APK** is the product. STORM is **not** the product. Emulators are **subagent review boxes** for this chat.

## Law

1. Read `CURRENT.md`. Do not rewrite it. Do not `aether approve` / `next` / `reject`.
2. Never tap Confirm / Yes. Never serial `RZCW2038KHN`.
3. Cap **2** AVDs (`storm-0`, `storm-1`). Pause AVDs when the 7B desk is hot if RAM fights.

## Factory (persistent components)

```bash
python3 python/aether_storm.py status
python3 python/aether_storm.py setup --name storm-0   # create AVD, do not boot
sh scripts/storm-sdk-setup.sh                          # packages + storm-0
sh scripts/storm-up.sh storm-0                         # boot (heavy)
sh scripts/storm-walk.sh emulator-5554 /tmp/storm-env/0/out
python3 python/app_verify.py --uidump-dir /tmp/storm-env/0/out
```

Home: `~/.mechanicall/storm` (not git). SDK: `~/.android-sdk-mechanicall`.

## Swarm

Spawn **read-only** reviewers against uidump/source. `/app-reviewer` = behaviours. `/visual-reviewer` = FACE-SPEC. This skill = the **environment**. A PASS is not human Yes.

## Not this

- EdubaWare / k3s clone
- Play Store / Funnel / public Ollama
- Sharing the A33
- Binding mechanicall-os as the pocket
