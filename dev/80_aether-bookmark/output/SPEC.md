# aether bookmark — command spec

**Not CURRENT. Not a Yes.** Grilled 2026-10-16 with `personal-llm-sft-v6:latest`. Live Next is still `advanced-local-model`. This spec is the body of `.aether/proposals/CURRENT-proposal-20261016-1841.md`.

v6's grill (`output/V6-GRILL.md`) kept propose-only doctrine. It then named a path `.aether/bookmarks/<label>/<path>`, refused duplicate labels, required sha256, refused root, and listed restore/snapshot/preflight as next verbs. Those are **not** this spec. The live shape below is.

---

## 1. What it is

`aether bookmark` copies `CURRENT.md` bytes into `.aether/bookmarks/`. It is a witness. It is not a Yes. It does not replace CURRENT. It does not apply.

Sudo analogy from the Doctor's Note: attribution. The copy is tied to one file at one time. The copy never becomes the grant.

---

## 2. Difference from neighbours

| Verb / dir | What it does | Bookmark |
|------------|--------------|----------|
| `apply` | copies a fenced proposal onto CURRENT; backup in `.aether/current-before/` | does not write CURRENT; does not use current-before |
| `approve` | Yes | not Yes |
| `event` | one JSONL line | also logs a line; the product is the file copy |
| `current-before/` | apply side-effect | operator-requested snapshot; survives later applies |
| `restore` | would copy a snapshot onto CURRENT | **not this verb** |

---

## 3. Usage

```
aether bookmark [label] [path]
aether bookmark list [path]
```

- No args: snapshot with no label.
- `list` is reserved. It is not a label.
- Label charset matches action-id: letters, digits, `.`, `_`, `-`.
- `[path]` is the project root, same as other authority verbs.
- Models may snapshot. Models never approve, apply, next, or restore.

---

## 4. What it writes

Path:

```
.aether/bookmarks/CURRENT-<UTC>[-label].md
```

Example already on disk:

`.aether/bookmarks/CURRENT-20261016T162428Z-this-current.md`  
cksum `3532677481`

Event kind: `bookmark`. Fields: `path`, `source`, `label`, `checksum` (cksum, house standard), `bytes`. No secret, no Yes.

It does not write `CURRENT.md`. It does not create `.aether/current-before/`. It does not write `preflight.md` / `apply.md` / `approve.md`.

Duplicate labels are allowed. The UTC stamp is the unique id. Refusing a second `this-current` would block the verb the operator already used.

---

## 5. What it must never do

- Rewrite, delete, or restore onto `CURRENT.md`
- Stamp Approval / Status
- Claim to be Yes
- Name or store a password, key, or token
- Add `restore` in this Next
- Invent `aether snapshot` as a second verb for the same copy

---

## 6. Failure modes

1. No `CURRENT.md` → exit 1, `no CURRENT.md`
2. Unknown flag → exit 2
3. Invalid label → exit 2
4. Treating the snapshot as apply or Yes
5. v6 path `.aether/bookmarks/<label>/<path>` — refuse; that is not the shape
6. Root-refuse as a new special case — out of scope; `aether` does not do that on other verbs
7. Restore sneaking in as a flag

---

## 7. Tests (`tests/bookmark.sh`)

- Snapshot; `cmp` snapshot to CURRENT; CURRENT bytes unchanged
- cksum in the event matches `cksum` of the snapshot
- `aether bookmark list` prints the new file
- Label `this-current` is accepted; label `list` is the list subcommand
- Invalid label exits 2
- Missing CURRENT.md exits 1
- `aether bookmark restore` is not a verb (usage / exit 2)
- Apply still writes `current-before/`, not `bookmarks/`

---

## 8. Grill holes that would become a Yes

- Writing CURRENT from bookmark
- Creating current-before from bookmark
- Event kind `approve` or a reason that looks like Yes
- A restore flag in the first verb
- Model-only "by":"human" on a model-run snapshot — omit `by`, or set it from the caller only when the human invoked the slash

---

## 9a. Stem nickname (bookmark-rename-nickname)

On a TTY, after the default stem is known and before the copy, the verb prints `Rename: [stem] ` and reads one line. Empty keeps the stem. `list` and `restore` exit 2. Any other character outside letters, digits, `.`, `_`, `-` exits 2. A non-TTY does not read stdin. The event records `stem`. The copy is still not a Yes.

## 9. After the human applies the proposal

Next becomes `add-aether-bookmark`. Apply is not a Yes. A later `aether approve` opens the implement halt. This folder does not add the verb now.
