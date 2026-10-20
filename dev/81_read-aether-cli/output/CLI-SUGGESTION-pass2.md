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
It gates proposals between human judgment and machine execution. It keeps a small reversible record of what was proposed, approved, and applied without deciding commits or capturing everything.

**3. What it is not**  
Capture is not the job: garden/rival/spark/graph/session/seed are installed but parked verbs. Apply is not a Yes; approve records judgment, apply copies text. Restore is not a verb.

**4. Verbs now, and verbs parked**  
Gate verbs installed: current, preflight, approve, reject, next, apply, probe, event, artifact, bookmark, brief, demo. Capture verbs still installed but parked: garden, rival, spark, graph, session, seed.

**5. APK implication, names only**  
The Android tester build is com.mechanicall.pocket.demo v0.19.21-loop-from-20 (versionCode 46). The aether script is not inside that APK; weight personal-llm-sft-v6:latest is also not in the APK.

**6. Holes that stay a human decision**  
aether drift reports git dirty status only — it does not decide commits. aether approve records Yes but does not run Next. Apply copies proposal text onto CURRENT.md; it does not commit or execute anything.
