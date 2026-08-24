# WALK — Rae impersonates a sitter (storm-1). Bob receives (storm-0).

**Not Yes.** Confirm not tapped. A33 not used. Operator `CURRENT.md` left at 3411 bytes (`sit-storm-factory`). storm-0 process left alive.

I am **Rae**. I have a shop folder, not this operator tree. I want a Next I can sit with a client on.

## What I did

| Seat | Serial | Folder | Role |
|------|--------|--------|------|
| storm-1 | emulator-5556 | `/storage/emulated/0/sitrae` | me (send) |
| storm-0 | emulator-5554 | `/storage/emulated/0/sitbob` | other seat (receive) |
| host drop | `127.0.0.1:8765` | `.inbox/drop/` | lab carry. Not mesh. Not Play Store. |

APK `0.16.0-hunk-drop`.

1. Bound **sitrae** (lab prefs after path-typing failed). PLAN showed my CURRENT.md, a **Changes** list (Objective / Next / Approval), and a **Proposal** with struck live lines and purple draft lines plus an editor that writes PROPOSE only.
2. DECIDE listed **multiple hunks for the same request**: Objective DESK vs LIVE, Next `sit-with-client` (IN). I did not tap YES/AGAIN/Confirm.
3. SEND FOLDER opened **IN THE WORKS**: folder `sitrae`, files 3, PUT ON THE WIRE · not Yes. Desk said *In the works. Accept on the other seat is not Yes.*
4. On storm-0, Bob’s seat showed **OFFER FOLDER**. ACCEPT copied `shop-notes.md` (*Hours, keys, till. Rae's notes.*) and left Bob’s CURRENT (`wait-offer`) untouched.

## Bottlenecks → standardised solutions

| # | Bottleneck | Standardised solution |
|---|------------|------------------------|
| B1 | `adb shell input text /sdcard/sitrae` dies at the second `/` (`/sdcard` only) | Product path = **Choose your folder** (SAF). Lab: write `mechanicall_seat.xml` `pocket_one` then force-stop. Never hyphen paths. |
| B2 | KEYCODE 73 is **backslash**, 76 is slash; IME still eats `storage`→`stora` | Do not type paths characterwise. Prefs or SAF. |
| B3 | DIR overlay + `CLOSE` can hide a successful prefs bind | force-stop + cold start after writing prefs. |
| B4 | Walker `tap_text("Next")` hits CURRENT.md body, not the Changes chip | Chips now have `contentDescription="Change Next"`. Walkers tap that, not raw "Next". |
| B5 | Decide hunk alts below the fold (Next#2/#3 hidden behind YES) | Hunk list is scrollable. Shrink pads if a sit shows >2 fields. |
| B6 | SEND while IME up | Hide IME by tapping chassis, never BACK. |
| B7 | After Accept, poll re-downloaded the same drop and put OFFER back | `poll_incoming` must not clobber accepted/declined unless the host id is new. |
| B8 | Two AVDs + 7B | Cap 2. This walk seeded hunks so the 7B was not required. |
| B9 | Host Java 26 vs Gradle | `JAVA_HOME=$HOME/.jdk/temurin-17`. |
| B10 | Mesh JNI still missing | Lab drop `python/aether_drop.py` on 127.0.0.1:8765; emulators use `10.0.2.2`. Not a store listing. |

## What this is not

- Not a rewrite of live operator CURRENT.
- Not Play Store / Funnel / public Ollama.
- Not a Yes (Decide never Confirm).
- Not bind-phone-to-this-repo.
- Not Headscale-as-folder-store. G4 mesh remains BLOCK.

## Glass

storm-1: `plan.png`, `decide.png`, `send-panel.png`, `sent.png`  
storm-0: `bob-wait0.png` / `bob-accepted.png`
