# Receipt — package-alpha-2

**Date:** 2026-08-05  
**Action:** `package-alpha-2` · APPROVED  
**Peer:** GPT 06c (phone) · goal: honest package for casual resume-proof product  

## Done this execute

| Item | Path / proof |
|------|----------------|
| CURRENT consistency | Header **Next** = body **Action id** = `package-alpha-2` |
| Objective | Sept-9 protocol product proof (install/create/refuse/resume) |
| First-project walkthrough | `docs/FIRST-PROJECT.md` |
| Alpha-2 release notes (DRAFT) | `docs/RELEASE-NOTES-ALPHA-2.md` — **no tag** |
| Entry pointers | START-HERE, README, `scripts/install-aether.sh` |
| Demo | `./aether demo` → DEMO OK |
| Temp project smoke | refuse publish-content **3** · allow draft-outline **0** |
| CI (prior) | shellcheck fix push green |

## Not done (human gates)

- [ ] `git tag -a v0.2.0-alpha.2` + `gh release create --prerelease`  
- [ ] Clean-machine install checklist performed by human (or second machine)  
- [ ] Observed Ste-class two-session pilot  
- [ ] Casual seat/webview path beyond CLI fluency  

## Clean-machine checklist (before tag)

```text
1. git clone @ immutable SHA or tag
2. ./aether version && ./aether demo
3. sh scripts/install-aether.sh
4. mkdir project && aether onboard --yes  (or FIRST-PROJECT.md)
5. preflight a Prohibited action → refuse exit 3
6. preflight Next → allow
7. leave; return; aether brief recovers Next
8. uninstall-aether.sh; project folder still exportable
```

## Message discipline (06c)

Say: **technical / protocol alpha** ready for supported pilots.  
Do **not** say: finished consumer app; conversation auto-sync; fully private Session.

## Human next

```bash
# commit + push package docs when ready
# then after clean-machine proof:
#   git tag -a v0.2.0-alpha.2 <sha>
#   gh release create v0.2.0-alpha.2 --prerelease -F docs/RELEASE-NOTES-ALPHA-2.md
aether next casual-seat-or-pilot-observe
```
