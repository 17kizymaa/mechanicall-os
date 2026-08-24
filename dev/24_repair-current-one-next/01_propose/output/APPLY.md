# APPLY — human only

`APPLY:` copy one file over `CURRENT.md`. Model must not do this.

Index propose: `.aether/proposals/CURRENT-proposal-20260818-0627.md`

After copy, from repo root:

```bash
python3 dev/24_repair-current-one-next/01_propose/output/check_current_pin.py
./aether current validate .
./aether probe <the-id-you-chose>
```

`check_current_pin.py` exits 0 only if header Next equals body Action id.

---

## A — keep `mobile-planning-demo`

Use if the header you already set is still what you want (demo paused, not Play Store).

```bash
cp dev/24_repair-current-one-next/01_propose/output/CURRENT-A-mobile-planning-demo.md CURRENT.md
python3 dev/24_repair-current-one-next/01_propose/output/check_current_pin.py
./aether current validate .
./aether probe mobile-planning-demo
```

Do **not** run `aether next mobile-planning-demo` — it refuses (`next unchanged`). There will still be no `next_selected` row for this id. That is recorded, not faked. Optional human line in `DECISIONS.md`.

Then work only that Next (or `aether reject` if the parked sitting means stop).

---

## B — return to `casual-core-interface`

Use if the last real `next_selected` (2026-08-11) is still the work: write the missing contract.

**Preferred (events + header via CLI):**

```bash
# human only — resets Phase SELECT / Status ACTIVE / Approval PENDING
./aether next casual-core-interface --reason "restore one Next; header had drifted to mobile-planning-demo"
cp dev/24_repair-current-one-next/01_propose/output/CURRENT-B-casual-core-interface.md CURRENT.md
# B’s file sets Approval APPROVED again; if you want the CLI reset to stand,
# change those three header fields back to SELECT / ACTIVE / PENDING after the copy.
python3 dev/24_repair-current-one-next/01_propose/output/check_current_pin.py
./aether current validate .
./aether probe casual-core-interface
```

**File-only (events already have this NS):** skip `aether next`, only `cp` the B file, then probe.

Do not implement `android/` under B.

---

## C — hold (`hold-one-next`)

Use if the sitting is dead and you do not want to pretend either Next is live. Required landing pad before a **new** product id (including any Play Store propose).

```bash
# human only — writes next_selected from mobile-planning-demo -> hold-one-next
./aether next hold-one-next --reason "forensics: close split; no implement until re-SELECT"
cp dev/24_repair-current-one-next/01_propose/output/CURRENT-C-hold-one-next.md CURRENT.md
python3 dev/24_repair-current-one-next/01_propose/output/check_current_pin.py
./aether current validate .
./aether probe hold-one-next
```

Order matters: `aether next` first (header is still `mobile-planning-demo`, so next is allowed), then copy C so body matches. If you copy C first, `aether next hold-one-next` refuses unchanged.

---

## D — people app (`app-first-openhands-compose`)

Use if the demo is not useful enough and you want Compose + OpenHands as the Next.

```bash
# human only — header is still mobile-planning-demo, so next is allowed
./aether next app-first-openhands-compose --reason "people-facing app: compose + OpenHands + aether Yes"
cp dev/24_repair-current-one-next/01_propose/output/CURRENT-D-app-first-openhands.md CURRENT.md
python3 dev/24_repair-current-one-next/01_propose/output/check_current_pin.py
./aether current validate .
./aether probe app-first-openhands-compose
```

Then human `aether approve` with a real reason before implement. I will not start Compose until that Next is live.

---

## Do not

- Edit only the `**Next:**` line.
- Run `aether approve "APPROVED"` with no reason.
- Apply two options.
- Launch OpenHands against the unrepaired file.
