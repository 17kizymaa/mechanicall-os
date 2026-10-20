1. What the aether CLI is
A single POSIX shell script (aether, version 0.2) that reads CURRENT.md as authority and gates change through explicit approve/reject cycles. It is not a full OS — it is one file under your control.

2. What it is for
It turns CURRENT.md into the source of truth by making every important change require an explicit gate: preflight checks, human approve, then apply. It prevents silent drift and keeps proposals fenced until they are reviewed.

3. What it is not
It does not decide commits, does not run Next automatically, and does not replace your editor or terminal workflow. aether drift only reports whether git is dirty; it never creates commits on its own.

4. Verbs now, and verbs parked
Installed gate verbs: current, preflight, approve, reject, next, apply, probe, event, artifact, bookmark, brief, demo. Parked capture verbs still installed but not the job: garden, rival, spark, graph, session, seed.

5. APK implication, names only
The Android tester build is com.mechanicall.pocket.demo v0.19.21-loop-from-20 (code 46). The aether script is not inside that APK; the weight personal-llm-sft-v6:latest is also not inside it.

6. Holes that stay a human decision
You decide whether to run Next after approve, you decide when to prune old garden items, and you decide whether drift means "commit now" or "review later." Restore is not a verb — recovery remains manual.
