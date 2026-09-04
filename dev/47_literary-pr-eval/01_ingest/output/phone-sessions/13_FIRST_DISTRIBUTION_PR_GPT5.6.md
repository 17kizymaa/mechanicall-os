Distribution verdict: NO — not yet.

But: this is the first PR that looks worth turning into the distribution. The product direction is strong; the submitted build is not distribution-grade.

I reviewed the current latest PR, #7 — feat(sit): testers face, at head 70a4c8e. It is open and mergeable, with 11 commits, 645 files, and +28,698/−1 lines.

Release-blocking findings

1. Critical: incoming ZIPs can escape the offer directory

In aether_inbox.py::_unzip_to, the extractor rejects .., but does not reject absolute paths or verify that the resolved target remains under dest:

name = Path(info.filename)
if ".." in name.parts:
    continue
target = dest / name

An absolute ZIP member can make target ignore dest, potentially writing elsewhere within the process’s permissions. Worse, this happens during polling—before the user presses Accept.

The drop server also has no authentication and stores the last uploaded ZIP. That is acceptable only for a tightly controlled lab—not a distributed feature.

Required: reject absolute paths, backslash/drive paths, symlinks and special entries; resolve each target and require it to be inside dest; add adversarial ZIP tests.

2. The central “Decide → Publish” path is not self-contained on a stock phone

The Android UI’s FaceBridge.yes() calls Python yes(), which calls:

run_aether(["approve", reason], ...)

That depends on an executable POSIX aether being on PATH or under AETHER_HOME.

The project’s own Android README explicitly acknowledges:

“On a stock phone there is no bash aether.”

It suggests Termux/toybox or using the URL face. Therefore the defining phone workflow—two-tap Publish with a Why—is not a dependable distributed Android experience.

That alone prevents this from being the distribution.

Required: either package a native/self-contained authority engine, route Publish to an authenticated authority service, or clearly distribute the URL face instead of claiming the APK is the operative product.

3. Green CI does not build or test the Android distribution

All four checks are green, but the workflow runs only:

- sh tests/run.sh
- sh scripts/ci-control-layer-gates.sh

It does not:

- compile the APK/AAB;
- run Android unit tests;
- run Compose instrumentation tests;
- install on an emulator;
- exercise first-sit → draft → Decide → Confirm;
- publish a signed or checksummed artifact.

The advertised “10/10 mechanical verification” is largely source-string inspection. For example, app_verify.py decides behaviours by finding strings such as OutlinedTextField, FaceBridge.yes, and GateStrip. That proves structural intent, not runtime behaviour.

Required CI gate: clean checkout → sync engine → assembleDebug/bundleRelease → emulator install → smoke/instrumentation tests → upload artifact.

4. It is not currently Play-ready

build.gradle.kts uses:

compileSdk = 34
targetSdk = 34
versionName = "0.17.0-testers"

Google states that starting August 31, 2026, new apps and updates must target API 36. The PR targets API 34. See Google’s current target-SDK requirement.

There is also no AAB, signing configuration, Play upload receipt, privacy/release material, or distributable asset.

The latest repository release has zero attached assets and predates this PR.

5. The required real-world test has not happened

The proposed CURRENT-sit-testers.md explicitly requires:

1. cellular AVD testing;
2. then one LTE sideload receipt;
3. then Play internal testing.

It also says:

“Lab 127.0.0.1 drop is not that receipt.”

No such off-LAN receipt is present. The PR itself says the mesh JNI gap remains unresolved and does not claim LTE folder-send.

So, by the project’s own acceptance condition, this has not passed its distribution gate.

6. The authority transition is still pending

The PR explicitly excludes live CURRENT.md, and the proposed replacement says:

Approval: PENDING

It requires a human to apply it, set sit-testers as Next, and approve with a real reason.

That is consistent with Mechanicall’s principles—but it also means this PR is not yet authorized as the distributed state. Green CI cannot substitute for that human transition.

7. The change is too broad for a trustworthy release candidate

This is not a focused tester-face PR. It brings 645 changed files and seven preceding unpublished commits, including Android, Python bridge code, STORM infrastructure, inbox/drop transport, documentation and generated receipts.

That makes it difficult to answer:

- What is the actual product artifact?
- Which pieces are supported?
- Which pieces are lab infrastructure?
- What is the rollback boundary?
- What exactly should testers install?

A distribution PR should be narrower or built from a separately reviewed integration branch.

What is good enough to preserve

The product shape is substantially better:

- Bind → Plan → Draft → Decide → Receipt is understandable.
- Decide as Publish, rather than a hunk-management screen, is the right abstraction.
- PROPOSE remains separate from live CURRENT until human action.
- Opening, binding, sending and receiving are explicitly not approval.
- Incoming offers skip CURRENT.md.
- Empty receipt language does not fabricate consent.
- The app refuses binding to the operator repository.
- The PR is honest about being a demo, about the mesh gap, and about not being production.

That is why my answer is not “throw it away.” It is:

This is a credible distribution candidate, not a distributable release.

Minimum gate before calling it “the distribution”

1. Fix ZIP extraction containment and add malicious-archive tests.
2. Make Decide → Publish work on a stock phone, without Termux/manual CLI provisioning—or distribute the URL face instead.
3. Add an Android build job and attach the resulting APK/AAB.
4. Add at least one emulator test covering:
   - fresh install;
   - bind;
   - first-sit template;
   - edit proposal;
   - Why-required two-step confirmation;
   - real authority/event/receipt result.
5. Raise compileSdk/targetSdk to 36 for Play submission.
6. Complete the documented off-LAN/LTE test and retain its receipt.
7. Apply and human-approve the new CURRENT.md.
8. Produce a narrowly defined release:
   - tag such as v0.17.0-testers.1;
   - signed/checksummed artifact;
   - installation instructions;
   - known limitations;
   - upgrade/uninstall path.
9. Call it exactly what it is: closed tester distribution, not production.

Final decision

| Gate | Decision |
|---|---|
| Merge immediately | No |
| Public/product distribution | No |
| Play internal upload today | No |
| Controlled developer lab build | Yes, with trusted inputs only |
| Worth finishing into the canonical closed-test distribution | Yes |

Do not distribute PR #7 as-is. Fix the containment vulnerability and the stock-phone Publish path first. Then this can plausibly become the first real Mechanicall tester distribution.