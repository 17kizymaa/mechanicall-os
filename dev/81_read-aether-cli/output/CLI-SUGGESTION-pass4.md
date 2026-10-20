1. What the aether CLI is
2. What it is for
3. What it is not
4. Verbs now, and verbs parked
5. APK implication, names only
6. Holes that stay a human decision

---

**1. What the aether CLI is**
It is one POSIX shell script with AETHER_VERSION 0.2; the file name is `aether` and it reads CURRENT.md as authority. The gate is the job: approve records Yes, apply copies fenced proposal onto CURRENT.md, drift reports whether git is dirty only.

**2. What it is for**
It gates proposals by requiring explicit approval before Next runs, so human judgment stays on record. It keeps a small reversible workflow where current, preflight, approve, reject, next, apply, probe, event, artifact, bookmark, brief, and demo are the verbs now.

**3. What it is not**
It does not decide commits; drift reports git dirty status only. Apply is not Yes: it copies a fenced proposal onto CURRENT.md after approval. Restore is not a verb in this system.

**4. Verbs now, and verbs parked**
Verbs now are current, preflight, approve, reject, next, apply, probe, event, artifact, bookmark, brief, demo. Capture is not the job: garden, rival, spark, graph, session, seed remain installed but are prune list items.

**5. APK implication, names only**
The Android tester build is com.mechanicall.pocket.demo v0.19.21-loop-from-20 (versionCode 46); the aether script is not inside that APK. The weight personal-llm-sft-v6:latest is also not inside that APK.

**6. Holes that stay a human decision**
aether approve records the Yes but does not run Next; aether apply copies proposal text but does not commit. Whether to restore, whether drift means "commit now," and whether garden/seed are active remain open questions.
