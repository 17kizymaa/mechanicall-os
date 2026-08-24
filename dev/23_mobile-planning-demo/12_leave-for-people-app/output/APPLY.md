# APPLY — human only

`APPLY:` model must not copy this over `CURRENT.md` and must not run the CLI below.

Proposal: `.aether/proposals/CURRENT-proposal-20260818-icm-people-app.md`  
Replacement: `output/CURRENT-icm-people-app.md`  
Lessons: `output/LESSONS.md`

**Order matters.** Header Next is still `mobile-planning-demo` (APPROVED), so `aether next icm-people-app` is allowed. If you `cp` first, `aether next icm-people-app` will refuse `next unchanged` and you will get no `NEXT_SELECTED` event.

From repo root:

```bash
# 1) re-SELECT (writes Next + resets Phase=SELECT Status=ACTIVE Approval=PENDING + event)
aether next icm-people-app --reason "leave sitting; people-app informed by failed stranger-send"

# 2) body must match header
cp dev/23_mobile-planning-demo/12_leave-for-people-app/output/CURRENT-icm-people-app.md CURRENT.md

# 3) pin + schema
./aether current validate .
./aether probe icm-people-app
```

Then, when you want implement (not silent):

```bash
aether approve "people-app factory is the Next; sitting is lab"
aether preflight icm-people-app
```

Then say **proceed to 03** in `dev/25_icm-people-app` (scaffold only).

## Do not

- Hand-edit only the `**Next:**` line.
- Run `aether next` / `approve` as the model.
- Apply CURRENT-D (`app-first-openhands-compose`) unless you revise the propose.
- Restart `:8765` as if the sitting were still the Next.
- Start `25` while Next is still `mobile-planning-demo`.
