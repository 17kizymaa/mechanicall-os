# Re-evaluation: the actual system

**Important scope note:** the branch tip is July 14 (`bc9255b`), while the reel audit and v5 evidence are from July 15. I can verify the branch implementation and use your pasted July 15 artifacts as evidence of how the wider local system behaved, but those latest artifacts are not yet visible in the branch.

## Executive verdict

**Aether did not fail completely. It succeeded as a capture and forensic system, but failed as a control system.**

It successfully preserved:

- the changing human judgments;
- what was listened to;
- what was built;
- the exact point at which v4 worked;
- the instructions that produced v5;
- enough evidence to reconstruct why the direction collapsed.

That is genuinely valuable. Without the inbox and session ledger, this failure would be remembered only as “the video looks shit.”

But Aether did **not** turn the most important human signals into binding production constraints. It kept accepting new ideas and generating counter-directions after the project needed convergence. Consequently, the system documented the spiral more effectively than it stopped it.

### Revised ratings

| Area | Rating | Verdict |
|---|---:|---|
| Core filesystem/context CLI | **7/10** | Much improved; several real P0 fixes landed |
| Capture and provenance | **8/10** | The strongest part of the system |
| Technical safety | **7/10** | P0 trust/watch, argv, markers, and tree-hash issues fixed in current `aether` |
| Creative decision support | **4/10** | Good memory, weak prioritisation |
| Agent control/governance | **3/10** | Prose gates are not enforced |
| Holistic usefulness today | **6/10** | Useful if reduced to capture + ledger + explicit gates |

This is no longer just “initial scaffolding.” But it also is not yet an awareness OS. It is currently a **good personal evidence ledger with experimental agent utilities attached**.

---

# 1. Did the P0 branch improve the real system?

Yes. Substantially.

The branch correctly addresses several findings from the first review:

| Prior finding | Current status |
|---|---|
| Distill deletes human context | **Fixed in normal cases** with generated markers |
| Executable hooks run twice | **Fixed** in `run_hook()` |
| No hook trust boundary | **Fixed** (`run_hook` + `entr` via `poke`; init does not auto-trust pre-existing hooks) |
| No `--no-hooks` | **Added** |
| Direct non-atomic context writes | **Mostly fixed** |
| Polling always rebuilds | **Mostly fixed** |
| No integration tests | **Basic suite added** (includes space-path + hash semantics) |
| README points at nonexistent Python CLI | **Main README corrected** |
| No `.gitignore` | **Added** |

Sources: [`aether`](https://github.com/17kizymaa/mechanicall-os/blob/fix/gpt56-review-p0/aether), [`tests/run.sh`](https://github.com/17kizymaa/mechanicall-os/blob/fix/gpt56-review-p0/tests/run.sh), [branch commit](https://github.com/17kizymaa/mechanicall-os/commit/bc9255b5ca679a9e66c28d89155f127be95ddf9b)

That deserves acknowledgment: this was not superficial review theatre. The implementation actually changed.

The technical P0 holes in §2.1–2.5 are **fixed in current `aether`**. Remaining medium items (e.g. §2.6 temp-name fallback) and the control-layer gaps in later sections still apply.

---

# 2. Technical P0 problems (status updated)

## 2.1 Fixed — `entr` watch now goes through `poke` / `run_hook`

**Status: FIXED in current `aether`.**

The `entr` callback no longer shells hooks directly. It runs:

```sh
"$AETHER_SELF" distill "$root" --quiet || true
"$AETHER_SELF" poke "$root" >/dev/null || true
```

`cmd_poke` calls `run_hook on-save`, so trust checks and `AETHER_NO_HOOKS` / `--no-hooks` apply on the entr path the same way as on the poll path.

Source: `cmd_watch()` / `cmd_poke()` in `aether`; tests in `tests/run.sh` (`poke/run_hook trust boundary`).

---

## 2.2 Fixed — `aether init` does not auto-trust pre-existing hooks

**Status: FIXED in current `aether`.**

`cmd_init` tracks whether any default hook already existed. It writes `.aether/trusted` **only** when every default hook was created by that init. If a hook was pre-existing (e.g. after clone), the project stays untrusted and init reports that fact.

Integration coverage: `tests/run.sh` — “init does not auto-trust pre-existing hooks.”

Ideal follow-up still open: trust digests so a later hook rewrite invalidates trust. The silent auto-trust hole is closed.

---

## 2.3 Fixed — `main()` preserves argv boundaries

**Status: FIXED in current `aether`.**

`main()` no longer rebuilds `$@` via unquoted string join. Global flags are stripped with a sentinel-terminated loop that re-appends each argument intact:

```sh
set -- "$@" '::AETHER_END::'
while [ "$1" != '::AETHER_END::' ]; do
    case "$1" in
        --no-hooks) AETHER_NO_HOOKS=1; export AETHER_NO_HOOKS ;;
        *) set -- "$@" "$1" ;;
    esac
    shift
done
```

Space-containing paths and multiword seeds keep their boundaries. Tests cover explicit path-with-spaces args and multiword seed spacing (`tests/run.sh`).

---

## 2.4 Fixed — marker corruption refuses automatic distill / repair

**Status: FIXED in current `aether`.**

`validate_context_markers()` requires absent markers (legacy) or exactly one start before one end. `dumb_distill` dies on corrupt markers without overwriting the file. `cmd_repair` refuses automatic distill when markers are corrupt and tells the operator to fix them by hand.

Integration coverage: `tests/run.sh` — “corrupt markers refuse distill.”

---

## 2.5 Fixed — line-based `tree_hash` + space-path hash tests

**Status: FIXED in current `aether`.**

`tree_hash()` is line-based (one path per line via `while IFS= read -r`), not `xargs cksum`. Filenames with spaces are hashed as single paths.

Integration tests create `my file.md` under a path with spaces, pass the path as an explicit argument, assert tree hash changes on edit, and check the generated sample names the file (`tests/run.sh` — “path with spaces (explicit arg + hash semantics)”).

---

## 2.6 Medium — the “secure” fallback temporary name remains predictable

The fallback is:

```text
.aether/.tmp.<pid>.<purpose>.<pid>
```

It is local to the project rather than global `/tmp`, which is better, but still predictable and opened without exclusive creation. There is also no cleanup trap for interrupted operations.

Given the Linux/NixOS target, it may be cleaner to require `mktemp` rather than maintain an insecure fallback that exists only to support a broader portability claim.

---

# 3. What the reel failure says about the architecture

The reel failure is not evidence that filesystem-native context is useless.

It reveals that the system has **three different layers confused as one**:

1. **Capture** — what was thought or felt.
2. **Knowledge** — what has been learned.
3. **Authority** — what the agent is currently allowed to do.

Aether handles the first two reasonably well. It barely implements the third.

## The inbox captured truth

The inbox contains strong, progressively clearer information:

- framing was not intentional;
- panning shots did not arrive correctly;
- cohesive visual continuity was required;
- v4’s `tmix` treatment worked on motion;
- stills remained weak;
- v5 was rejected comprehensively.

That is excellent provenance.

## But every seed has the same operational weight

These are all stored as similar timestamped lines:

- “research other tools”
- “colour grading was a mistake”
- “research NMA deeply”
- “v4 is tight”
- “add rhythm strobes”
- “v5 is genuinely shit”

The system does not distinguish:

- observation;
- experiment;
- approval;
- rejection;
- hard constraint;
- superseded instruction;
- stop command.

Chronology alone is not authority.

The result was predictable: the latest idea became another build input, even when an earlier judgment should have become a gate.

---

# 4. The central systemic failure: no commitment mode

Aether has strong machinery for divergence:

- `seed` creates new possibilities;
- `spark` injects randomness;
- `rival` generates an opposing treatment;
- research documents expand methodologies;
- the gardener proposes additional connections;
- RHIZOME explicitly privileges deferred structure.

But it has almost nothing equivalent for convergence.

This matters because the project had already found a partial direction at v4. At that point the correct operation was no longer:

> What else could this become?

It was:

> Which six shots survive, and what must be removed?

The Rival Editor’s explicit law is **“never converge.”** That can be useful during exploration, but it is actively harmful after a baseline has been selected. In the session ledger, each rival response invited the next thesis:

- density;
- then starvation;
- then excess;
- then apparatus;
- then mathematical stills;
- then rhythm strobing.

That is exactly what an anti-convergence system is designed to do. The problem was not that Rival malfunctioned. The problem was that it remained available after its useful phase.

Source: [`ADVERSARY.md`](https://github.com/17kizymaa/mechanicall-os/blob/fix/gpt56-review-p0/docs/ADVERSARY.md)

## Required conceptual correction

> **Capture can remain structure-deferred. Production cannot.**

“Capture is sacred; structure is deferred” is a good inbox law. It should not be a universal operating law.

A production process needs an explicit phase:

```text
EXPLORE → SELECT → COMMIT → EXECUTE → REVIEW
```

Each phase should change what the agent may do.

| Phase | Allowed |
|---|---|
| Explore | Seed, spark, rival, research, rough variations |
| Select | Compare, rank, delete, isolate successful moments |
| Commit | Declare baseline, constraints and rejection conditions |
| Execute | Build only the approved bounded proof |
| Review | Compare output against gate; no unsolicited repair build |

Once v4 received **TIGHT**, the project should have moved from Explore to Select. Instead, it stayed in Explore and treated the positive signal as permission to integrate every unresolved research thread.

---

# 5. The session ledger is evidence, not state

The current `.session.md` is good at recording:

- `listening:`
- `made:`
- rival input/output.

But it does not prominently record:

- current baseline;
- active phase;
- approved elements;
- rejected elements;
- prohibited actions;
- next bounded deliverable;
- who must approve it;
- maximum time/plate/effect budget.

That is why the July 15 audit had to reconstruct all of these after the failure.

A useful production state could remain plain Markdown:

```markdown
# CURRENT

**Phase:** SELECT  
**Baseline:** rough-v4  
**Deliverable:** silent 15–20s proof  
**Human approval required:** yes

## Keep
- motion tmix
- opening silence
- WYLD/Liver/ring pool

## Kill
- full still-math parade
- automatic quarter-note strobes
- full-length v6

## Limits
- maximum 6 motion plates
- no new FX
- no new software
- no full export

## Next allowed action
Select and export one silent proof.

## Unlock condition
Human writes: KEEP
```

This is not a new grand subsystem. It is a small authoritative contract that agents must read before acting.

The critical distinction is:

- inbox = append-only evidence;
- session = chronological history;
- `CURRENT.md` = present authority.

---

# 6. Aether’s generated context is still not useful awareness

`.context.md` now safely preserves human prose, which is technically important. But the generated section is primarily:

- root path;
- file count;
- sample file list;
- README excerpt;
- timestamp and hash.

That is filesystem inventory, not meaningful project awareness.

It cannot answer:

- What is the active objective?
- What failed most recently?
- What decision superseded earlier decisions?
- What action is forbidden?
- What requires human approval?
- What is the smallest next deliverable?

The reel demonstrates the gap perfectly. Aether could know that 88 files exist while still not know that **v5 is rejected and v6 is forbidden**.

The next useful distillation target is not an LLM summary of everything. It is a deterministic extraction of a few authoritative fields from a human-owned current-state file.

---

# 7. The gardener did not solve this—and should not

The gardener’s responsibility is seed placement:

- spark;
- trash;
- hold;
- note;
- project.

That is fine. It should not be promoted into an autonomous project manager.

However, there are implementation concerns:

- It rewrites the inbox non-atomically.
- Destination paths derived from model output can write almost anywhere available to the user.
- Approved proposals are matched back to inbox lines using fuzzy 40-character prefixes.
- Reapplying after partial failure can duplicate destination entries.
- There are no visible tests for proposal parsing, interrupted apply, duplicate seeds, or malicious destination strings.

These are fixable, but they are not today’s central problem. The reel failed before seed filing mattered.

Source: [`aether_garden.py`](https://github.com/17kizymaa/mechanicall-os/blob/fix/gpt56-review-p0/python/aether_garden.py)

---

# 8. Reassessment of the reality sprint

The three-week commercial plan is directionally much healthier than the reel spiral because it includes:

- bounded offers;
- prices;
- deposits;
- numerical outreach targets;
- explicit exit gates;
- a separation between art and income;
- instructions not to add software;
- a daily controllable unit;
- permission to use existing evidence.

Its strongest principle is:

> The art and income lanes run in parallel. Neither is permitted to hold the other hostage.

That is a real correction.

But the document itself shows the same systemic tendency: a valid insight expanded into a very large operating constitution.

You do **not** need to turn the entire excerpt into another Aether feature set. Its executable core is much smaller:

```markdown
# REALITY-SPRINT-CURRENT

Window: 2026-07-15 → 2026-08-05
Target: one paid bounded engagement

Today:
- [ ] one warm/local approach
- [ ] one platform proposal
- [ ] one appropriate follow-up
- [ ] ≤30 minutes on silent reel proof

Offers:
1. Short Onsite Story
2. Existing Footage Rescue
3. Digital Friction Audit

Art gate:
No full reel until silent 15–20s proof receives KEEP.

Business gate:
The unfinished reel cannot delay outreach.

Score:
sent: 0
replies: 0
conversations: 0
quoted: 0
deposits: 0
```

The full strategy can remain reference material. Daily operation should fit on one screen.

Otherwise, the system risks repeating the reel failure in business form: replacing action with a sophisticated stack of correct documents.

---

# 9. What should remain active now

## Keep active

1. **`aether seed`**  
   It demonstrably captured useful human truth.

2. **Voice capture**  
   Appropriate because the bottleneck is critique density, not ideation. It should produce seeds—not automatically trigger builds.

3. **`.session.md`**  
   Keep it as forensic history.

4. **Filesystem-native Markdown**  
   Still the right substrate.

5. **Human-authored current-state contract**  
   This is the missing layer.

## Park temporarily

1. **`aether rival` for the reel**  
   The project does not need more opposition. It needs selection.

2. **`aether spark` during execution sessions**  
   Random prompts are counterproductive after direction lock.

3. **Gardener expansion**
4. **Graph work**
5. **New creative agents**
6. **New reel research documents**
7. **Any v6/full-length automation**

These features are not inherently bad. They are wrong for the current phase.

---

# 10. Minimal system correction

Do not build another large subsystem. Add one small convention and make agents respect it.

## `CURRENT.md`

Every active project gets one present-tense control file with:

- objective;
- phase;
- baseline;
- keep list;
- kill list;
- limits;
- next allowed action;
- human unlock condition.

## Agent rule

Before any multi-step or export-producing action:

1. Read `CURRENT.md`.
2. Refuse actions listed under Kill/Forbidden.
3. Execute only the Next allowed action.
4. Stop after producing the bounded artifact.
5. Never infer approval from silence.
6. Human critique updates `CURRENT.md`; it does not automatically initiate another build.

## Important: do not automate this heavily yet

Start with a plain file and agent instructions. Prove it prevents one spiral. Only then consider commands such as `aether current` or machine validation.

The system already has enough commands.

---

# Revised holistic judgment

The honest conclusion is not:

> Aether caused a bad video.

It is:

> Aether made divergent thinking extremely cheap, captured the resulting process well, but provided no equally strong mechanism for commitment, subtraction, or stopping.

The artistic failure is therefore a **real system test**, and a useful one. It exposed the missing half of the architecture:

```text
Capture without authority becomes accumulation.
Memory without prioritisation becomes noise.
Adversarial creativity without a commitment phase becomes genre thrash.
```

The July 15 audit is actually the most convincing Aether artifact you have shown. It transforms an emotional rejection into a precise account of:

- last known good state;
- introduced variables;
- failed assumptions;
- forbidden next actions;
- bounded recovery path.

That document is closer to genuine “awareness” than the generated `.context.md` inventory.

## Immediate decision

- **Keep Aether.**
- **Stop expanding it.**
- Technical P0 holes from this re-eval (§2.1–2.5: entr trust, init auto-trust, argv quoting, marker validation, space-safe tree hash) are **fixed in current `aether`**; residual medium item §2.6 (predictable temp fallback) remains optional hardening.
- Introduce one authoritative `CURRENT.md`.
- Disable divergent tools when a project enters Select/Commit.
- Run the commercial sprint from a one-screen scoreboard, not another software layer.
- Treat v4 as evidence, not as a template that must be preserved wholesale.

## Before the next export is allowed

> **The next export is allowed only when six or fewer motion plates have intentional silent arrivals, every effect can be justified by a visible picture problem, and the human explicitly approves the sequence—not merely one treatment inside it.**
