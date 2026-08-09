# First project — five minutes (protocol alpha)

**Doc status:** NON-NORMATIVE walkthrough · supports `package-alpha-2`  
**Audience:** technical user helping a casual pilot · or a careful first-time operator  
**Outcome (06c):** install → project → refusal → resume — not “chat forever.”

## What you will own after this

A folder on **your** machine with:

| File | Role |
|------|------|
| `CURRENT.md` | Latest agreed objective + **one** Next + Prohibited |
| `.aether/events.jsonl` | What was allowed/refused/approved |
| (optional) notes / artifacts | Evidence — still not authority |

AI chat history is **not** the plan. CURRENT is.

---

## 0. Get Mechanicall (pick one)

### A. From git (developers)

```bash
git clone https://github.com/17kizymaa/mechanicall-os.git
cd mechanicall-os
# optional: checkout a release tag when human has cut one, e.g. v0.2.0-alpha.2
chmod +x aether
./aether version    # expect: aether 0.2
```

### B. Install script (if present on your tree)

```bash
# from a clone:
sh scripts/install-aether.sh
# puts aether on PATH when configured — see script comments
```

### C. Hosted lab (optional, not the core product)

Website Session on anphuni.com is a **capped multi-seat lab**.  
Model traffic may go through OpenRouter. Use **public / synthetic** data only.  
See PRODUCT.md + site privacy.

---

## 1. One-command literacy (sandbox — never touches your real CURRENT)

```bash
./aether demo
# expect last line: DEMO OK
```

You should see: **refuse** → **allow** → human-labelled **approve** → **re-SELECT**.

---

## 2. Create your first project

```bash
mkdir -p ~/mechanicall-projects/my-first
cd ~/mechanicall-projects/my-first
# if aether is the repo copy:
/path/to/mechanicall-os/aether init .
/path/to/mechanicall-os/aether current init .
```

Or casual sample:

```bash
sh /path/to/mechanicall-os/scripts/try.sh
```

Edit `CURRENT.md` (or use your agent **only to propose** text you accept):

```markdown
# CURRENT

**Objective:** <one sentence you care about>
**Phase:** EXECUTE
**Status:** ACTIVE
**Baseline:** first-day
**Next:** draft-outline
**Approval:** PENDING

## Keep
- public or non-sensitive material only

## Reject
- publishing without my yes

## Limits
- one Next at a time

## Next allowed action
**Action id:** draft-outline

Write a short outline for review; do not publish.

## Approval condition
I read the outline and decide next.

## Prohibited
- automatic-approve
- publish-content
- send-email-for-real
```

Check:

```bash
aether current validate .
aether current .
```

Header **Next** and body **Action id** must match.

---

## 3. Observe one refusal (the point of the product)

```bash
aether preflight publish-content .
# expect: Refused … exit 3

aether preflight draft-outline .
# expect: Allowed … exit 0
```

If something “felt allowed” in chat but preflight **refuses**, the **plan wins**. That is intentional.

---

## 4. Human decision

When work is ready for a gate:

```bash
aether approve "outline looks good"
aether next collect-sources   # only after APPROVED; new Next
```

Models **never** run approve for you. Silence is not permission.

---

## 5. Leave and return (the wedge)

Close everything. Tomorrow:

```bash
cd ~/mechanicall-projects/my-first
aether brief .
aether current .
cat CURRENT.md
```

You should recover **Objective**, **Next**, and **Prohibited** without rereading chat.

---

## 6. Uninstall / export

- **Export:** copy the project folder (CURRENT + `.aether/` + your files).  
- **Uninstall CLI:** `sh scripts/uninstall-aether.sh` if you used the install script.  
- **Remove project:** delete the folder — authority lived in files, not a vendor lock cloud.

---

## Success checklist (pilot)

| # | Proof |
|---|--------|
| 1 | Obtained one exact tree/version |
| 2 | Started without knowing repo history |
| 3 | Understands CURRENT ≠ full chat log |
| 4 | Created one project |
| 5 | Observed one refusal |
| 6 | Returned later and recovered Next |
| 7 | Could export or uninstall |

If any row fails, the product is not yet “casual-ready” — fix packaging/UX, not marketing.

---

## Related

- `PRODUCT.md` · `SPEC-v0.2.md` · `docs/ALPHA-LIMITATIONS.md`  
- `docs/RELEASE-NOTES-ALPHA.md` · `aether demo` · GPT peer **06c**
