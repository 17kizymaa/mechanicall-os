1. What the aether CLI is
It is one POSIX shell script, version 0.2, named `aether`. It reads CURRENT.md as authority and gates work through human-controlled verbs. The script lives on disk; it does not run inside the Android APK.

2. What it is for
It turns CURRENT.md into a controlled workspace: you propose fenced text, review it, approve it once, then apply it. It prevents accidental commits by separating approval from Next. It keeps your current state explicit and reversible.

3. What it is not
It is not a chat interface or an AI backend. It does not decide commits; drift only reports whether git is dirty. Apply copies text onto CURRENT.md — it is not a Yes. Restore is not a verb.

4. Verbs now, and verbs parked
Verbs now: current, preflight, approve, reject, next, apply, probe, event, artifact, bookmark, brief, demo. Verbs parked (still installed): garden, rival, spark, graph, session, seed.

5. APK implication, names only
The Android tester build is com.mechanicall.pocket.demo v0.19.21-loop-from-20 (v46). The aether script is not inside that APK. The weight personal-llm-sft-v6:latest is not inside that APK.

6. Holes that stay a human decision
Whether drift decides the commit stays with you — the script only reports dirty status. Whether approve means "Yes" stays with you — it records Yes, it does not run Next.
