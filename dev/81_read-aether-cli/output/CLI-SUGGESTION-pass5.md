1. What the aether CLI is
It is one POSIX shell script, version 0.2, whose file name is `aether`. It reads CURRENT.md as authority and gates work through job verbs. The gate verbs are current, preflight, approve, reject, next, apply, probe, event, artifact, bookmark, brief, demo; the capture verbs installed but later pruned are garden, rival, spark, graph, session, seed.

2. What it is for
It gates proposal work by requiring CURRENT.md to exist and be human-authored before Next can run. It separates approval from execution: approve records a Yes without running Next, and apply copies a fenced proposal onto CURRENT.md without deciding the commit. drift reports whether git is dirty; it does not decide a commit.

3. What it is not
It is not an APK or package runner: the aether script is not inside com.mechanicall.pocket.demo v0.19.21-loop-from-20 (code 46), and weight personal-llm-sft-v6:latest is not inside that APK either. It is not a restore verb, and it does not run the Next on approve.

4. Verbs now, and verbs parked
Verbs now are current, preflight, approve, reject, next, apply, probe, event, artifact, bookmark, brief, demo; they gate work through CURRENT.md. Verbs parked are garden, rival, spark, graph, session, seed; they capture material but are not the job.

5. APK implication, names only
The aether script is not inside com.mechanicall.pocket.demo v0.19.21-loop-from-20 (code 46). The weight personal-llm-sft-v6:latest is not inside that APK either. Restore is not a verb; drift may be deciding a commit, but apply is not stated as not a Yes.

6. Holes that stay a human decision
Whether to approve remains the gate. Whether to run Next after approve remains the gate. Whether to commit remains the gate.
