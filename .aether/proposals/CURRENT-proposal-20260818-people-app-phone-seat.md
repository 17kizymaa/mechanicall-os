# Proposed CURRENT update (draft — not authority)

**Project:** mechanicall-os (operator)  
**Date:** 2026-08-18  
**Author:** human reject + continue

`APPLY:` human must approve then merge — model must not overwrite CURRENT.

## Latest reject (fact)

```
2026-08-18T17:02:49Z REJECTED
reason: We need to create an actual phone seat though; otherwise, this won't work with mate/
Phase → SELECT  Approval → REJECTED
Next still people-app-validation (header)
```

Desktop validation (bind folder) already recorded Yes. Operator said **Not yet** until a phone can sit SeatMate / people-app.

## Observations

- Bind `~/people-app-stranger-sit` Next `people-app-validation` APPROVED; walk bind+plan shown.
- Operator preflight `people-app-validation` still *matches Next* but Status is REJECTED — do not implement as approved.
- APK chrome exists as source (`android/`). No `gradlew` / APK on this host last check.
- URL face (`aether_pocket_serve`) is the sitting that works without an APK; GET is not Yes.

## Proposed CURRENT change

Replacement body: `examples/propose-current/CURRENT-people-app-phone-seat.md` (written with this file).

```
**Next:** people-app-phone-seat
**Phase:** SELECT
**Status:** ACTIVE
**Approval:** PENDING
```

## Conflicts

- Replaces rejected `people-app-validation` as the *operator* Next.
- Does not delete SeatMate or the bind walk.
- Not Play Store. Not Compose. Not Funnel.

## Human decision

- [ ] `aether next people-app-phone-seat` then `cp` the replacement over operator CURRENT.md (human 2026-08-18: APK path; pocket-face is fallback only)
- [ ] Stay REJECTED on `people-app-validation`
- [ ] Revise the action-id

**Do not** run `aether approve` / `next` from the model.
