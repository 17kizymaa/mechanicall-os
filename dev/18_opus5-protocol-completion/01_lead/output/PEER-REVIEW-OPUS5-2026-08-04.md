# Opus 5 peer review — mechanicall-os

**Model:** `anthropic/claude-opus-5` via OpenRouter  
**Role:** peer reviewer (authorized collaborator)  
**Date:** 2026-08-04  
**Human:** Anphuni — sole approver  
**Status:** LIVE Opus output (re-run after prior 401)  
**Filed with:** prior GPT-5.6 peer chain + host scaffold correction + host interim adjudication  
**Authority:** PROPOSAL / review artifact — not CURRENT  

---

# Opus 5 peer review — mechanicall-os (2026-08-04)

## Meta

| | |
|--|--|
| Model / role | Claude Opus 5 — **peer reviewer** (not implementer, not approver). I never run `aether approve`; silence from me is not permission. |
| Scope | (a) re-adjudication of the archived v0.1 awareness-scaffold critique; (b) peer review of the current v0.2 product narrative + CLI as described by host-measured ground truth. |
| Baseline | `master` tip after PR **#3** merged (~`5dd2c9f`; protocol + panel commits). Host-measured 2026-08-04. |
| Evidence basis | **Host-supplied measurement table + attached documents.** I did not independently fetch the repo, the site, or CI this turn (see Non-claims). Verdicts below are conditional on that table being accurate. |
| Relation to prior chain | I treat **GPT-5.6 Sol CONDITIONAL (2026-08-04)** as largely absorbed and do **not** re-open "Session is core." I treat **PEER-CORRECTION-AWARENESS-SCAFFOLD-CRITIQUE.md** as substantively correct and adopt its framing (legacy paste = historical smell test, not inventory). I **concur with the host interim adjudication's verdict** and agree with ~all of its claim rows; I escalate two of its "residual" items and split one (see R11, R13, R6). This document is the primary peer artifact; the interim remains as provenance. |
| Authority | PROPOSAL / review artifact — **not CURRENT**. |

---

## Executive verdict

**CONDITIONAL** — for "coherent public alpha narrative + runnable authority protocol on master."

1. The legacy critique is **mostly SUPERSEDED as inventory** and must not be recirculated as live truth; the host correction was right to say so.
2. The v0.2 authority core is **runnable and covered** (`current`/`validate`/`preflight`/`approve`/`reject`/`next`/`demo`/`probe`/`brief`/`drift`, `tests/run.sh` PASS). That is real, and it is the strongest part of the product.
3. Six of the legacy code defects are **genuinely FIXED**, with a review-finding comment in `run_hook` — good hygiene, credit where due.
4. Blocking CONDITIONAL, not PASS, on two 🔴s: **unknown verbs exit 0 through `cmd_status`** — unacceptable in a CLI whose verbs are `approve`/`preflight`, and worse because external agents are only *cooperatively* gated; and **no LICENSE** while marketing an adoptable protocol.
5. Secondary: dead `python_distill` branch, `entr` watch path, `~1880`-line `aether` versus a brutalist "cat it in one screen" doctrine, `SPEC-v0.1` edit-marker residue with no SUPERSEDED header, and an **uncommitted nix/seat/dev tree** — i.e. the host-vs-public-truth gap GPT-5.6 flagged, recurring smaller.
6. Nothing here requires architectural retreat. All of it is thin, mechanical, and one-Next-at-a-time.

---

## Claim-by-claim: legacy scaffold critique

| # | Legacy claim | Status | Evidence (host-measured 2026-08-04) | Residual risk |
|---|---|---|---|---|
| L1 | Repo is "Mechanicall OS v0.1" / *awareness-agent*, filesystem sidecar system | **SUPERSEDED** | Identity is v0.2 local-first **authority** protocol (PRODUCT.md); `aether` header v0.2; SPEC-v0.2 shipped | Sidecar layer still exists and is thinner than the pitch; keep ALPHA-LIMITATIONS honest |
| L2 | Pushed once 2026-07-10, dormant ~1 month, 0 stars/1 contributor, languages 57.8% Python | **SUPERSEDED** | PR #3 merged to master; core CLI is POSIX sh; Python is optional UI (panel/llm/shell) | Public perception lag if release notes still read "draft" |
| L3 | Runtime = one `sh` script with **six** verbs (init/status/distill/watch/repair/poke) | **SUPERSEDED** | ~25+ verbs incl. current/preflight/approve/reject/next/demo/brief/drift/probe/session/graph | Verb sprawl is now its own problem (see 🟡-3) |
| L4 | README Quick Start = `python3 /home/awareness-agent/aether/cli.py init` | **NEVER TRUE (of current README)** | README Quick Start documents `aether onboard/current/preflight/approve` | Stale `awareness-agent` paths still reported in older `docs/*` (nixos-transition, MBP notes) — unfinished follow-up on the host correction's own checklist |
| L5 | README advertises `.awareness.json`, Status "initial scaffolding / next: basic CLI" | **FIXED** | README is v0.2-shaped | Not independently re-read by me end-to-end; self-contradiction elsewhere in README unverified |
| L6 | `CORE_PRINCIPLES.md` "Markdown + Python only userland" is factually false | **FIXED** | Principles now: Markdown/JSON authority; **POSIX shell and/or Python** automation; distribution UIs may use other langs | The amendment must stay visible, or "locked" framing weakens again |
| L7 | `CORE_PRINCIPLES.md` ends with bare `trigger line` | **FIXED** | No trailing trigger junk; ends with hosted-lab boundary note | — |
| L8 | `SPEC-v0.1.md` ends with `---edit---` / `===edit marker===` | **STILL OPEN** | File still carries the residue | Cheapest credibility leak in the repo; also no SUPERSEDED-BY header |
| L9 | `python_distill()` targets a nonexistent `python/`; smart distill is dead code | **PARTLY OPEN** (split from host's "PARTLY") | `python/` now exists (panel, llm, shell) but **no `aether_distill.py`**; `python_distill()` still falls through to `dumb_distill` | The *directory* claim is FIXED; the *dead branch* claim is STILL OPEN. Worse than before: the dir now exists, so the branch looks live to a reader |
| L10 | Hooks run twice (`-x` then `-f` both fire) | **FIXED** | `run_hook` mutually exclusive executable **OR** `sh`, with `# review finding #2` comment | Keep a regression test pinned to this |
| L11 | `abspath` mangles `.` → `# Context — .` | **FIXED** | `""` and `.` special-cased to `pwd -P` | Non-directory / symlink arg edges unverified |
| L12 | `cmd_distill` computes state before distill, overwrites distiller output | **FIXED** (directionally) | counts/hash computed **after** `python_distill` | Single-writer ownership of `.context.md` still not enforced by a test |
| L13 | `watch` entr path snapshots file list once; dies on new files | **STILL OPEN (entr path)** | poll path has `while true`; entr path is still one-shot `find … \| entr -d` | `aether watch` can exit silently on first new file; user believes awareness is live when it is not |
| L14 | Unknown subcommands swallowed → `cmd_status "$cmd"`, exit 0 | **STILL OPEN** | `*) cmd_status "$cmd"` remains | **Escalated to 🔴** — see Current product review 🔴-1 |
| L15 | `embed_state_comment` awk `NR==1` insert may lose block; line-oriented strip vs multi-line JSON comment | **UNADJUDICATED — treat as STILL OPEN** | Not in host measurement table; legacy author also could not read it | Silent state-comment corruption; needs a hand audit + one test |
| L16 | No `.gitignore`; `state.json` and `__pycache__/*.pyc` tracked | **FIXED (ignore file)** / **STILL OPEN (untrack)** | `.gitignore` present (state.json, pycache, seat builds, qcow2, result*) | Adding ignores does **not** untrack already-committed blobs; `git ls-files` sweep not shown to me |
| L17 | File-type whitelist too narrow (`*.md,*.py,*.txt,*.sh`) and duplicated in two functions | **STILL OPEN (unverified)** | Not measured; `flake.nix` invisibility claim untested | Low severity now that awareness is not the headline layer |
| L18 | LOC budget blown ~1.7× (≈380 vs ≤220 target) | **SUPERSEDED as a v0.1-spec violation / STILL OPEN as doctrine** | `aether` is now **~1880 lines** — ~8.5× the old target | The *number* aged out; the *contradiction* got much worse. See 🟠-1 |
| L19 | `cmd_repair` is "a lie" — just `cmd_distill` | **FIXED** | Inspects markers; refuses distill on corrupt markers | — |
| L20 | No tests | **FIXED** | `tests/run.sh` extensive; smoke-verify ALL PASSED incl. demo/probe/brief/drift | Coverage of *legacy* fixes (L10–L13) unconfirmed |
| L21 | No CI | **STILL OPEN (unverified)** | Not in ground truth | A 1880-line sh script with no shellcheck/CI gate is where FIXED items quietly regress |
| L22 | No LICENSE | **STILL OPEN — TRUE** | "Still none observed on host check" | **Escalated to 🔴** — see 🔴-2 |
| L23 | "Built by agent swarms as much as for them" (`.grok/`, `dev/0N_` transcripts) | **TRUE, unchanged, and fine** | dev archives still present (and partly uncommitted) | Only a risk where archives are mistaken for authority; Layer-4 labelling already exists |
| L24 | "Repo violates its own locked doctrine; docs no longer describe the code" | **TRUE in spirit, still the load-bearing finding** | Doctrine drift moved venues: no longer README-vs-code, now LOC-vs-brutalism and host-vs-master | See "What the legacy critique got right" |

---

## Current product review (v0.2 protocol)

### 🔴 Blocking for PASS

**🔴-1 — Unknown verbs resolve to `cmd_status` and exit 0, in a CLI whose verbs include `approve` and `preflight`.**
Pointer: `aether` `main()` fallback `*) cmd_status "$cmd"`.
This was a cosmetic annoyance in the v0.1 sidecar tool. In v0.2 it is an **authority-layer defect**. `aether preflght …`, `aether aprove`, `aether nexr` all print a status-shaped report and return 0. Combined with `docs/GROK-SEAT.md` — the external TUI does not auto-preflight, the human is the gate — the failure mode is: an agent or operator issues a mistyped authority verb, sees exit 0 plus plausible output, and records "checked / gated" when nothing was checked. Silence read as permission is precisely the anti-pattern the protocol exists to prevent, and here the *tool itself* manufactures it.
Fix (thin): treat `$1` as a path only if `[ -d "$1" ]`; otherwise `die "unknown command: $cmd"` with non-zero exit (suggest 2, distinct from preflight-refusal codes). Add a test asserting non-zero for a garbage verb and for each near-miss of an authority verb.
I disagree with the host interim's placement of this as ordinary residual debt.

**🔴-2 — No LICENSE, while the product narrative is "a protocol you should adopt."**
Pointer: repo root; PRODUCT.md / README distribution framing.
No license = all rights reserved by default. Nobody can legally vendor `aether`, fork it into a seat build, or ship `docs/SINGLE-APP-DISTRIBUTION.md` outputs. That is a direct contradiction of a local-first, cat-able, adoptable-protocol claim, and it is a one-file fix. It also blocks any future peer or contributor from doing more than commenting.
Fix: pick one (MIT/Apache-2.0 for maximal protocol adoption; add NOTICE if you want attribution), state it in README, and state explicitly whether the Session lab is under the same terms.

### 🟠 Should fix before calling the narrative stable

**🟠-1 — LOC/doctrine tension: `~1880`-line single POSIX sh `aether` vs "fits in one screen of `cat`."**
Pointers: `aether` (v0.2 header); `SPEC-v0.1.md` ≤220-line target; `CORE_PRINCIPLES.md` brutalist framing.
Two honest options, pick one and write it down: (a) formally retire the ≤220/"one screen" success criterion in SPEC-v0.2 and replace it with a defensible budget (e.g. "single file, no build step, every verb readable in isolation, ≤N lines per verb"); or (b) split the CLI. Do **not** leave a brutalist-minimalism claim standing over an 1880-line file — that is the exact self-contradiction L24 identified, and a reviewer will find it every time. Related: at this size, absence of a shellcheck gate (unverified) is the main regression vector for L10–L13.

**🟠-2 — Cooperative preflight has no after-the-fact detection.** *(cont.)*
Pointers: `docs/GROK-SEAT.md` (human-is-the-gate, no auto-preflight), `aether preflight` / `aether approve` dispatch, absence of any receipt artifact.

The seat design is defensible: a human gate beats a tool that pretends to be one. But the design currently has *no residue*. If the operator skips preflight, or preflight runs against a tree that then changes, or (see 🔴-1) preflight never actually ran because the verb was mistyped, nothing downstream can tell. `approve` will behave identically in the checked and unchecked cases. That means the protocol's central safety property is unfalsifiable after the fact — you cannot audit a session, you can only trust the narrator. For a project whose whole pitch is legible, cat-able discipline, "trust the narrator" is the wrong terminal state.

Fix (thin, no new machinery): have `preflight` append one line to an append-only ledger — timestamp, tree fingerprint (`git rev-parse HEAD` + dirty flag, or a cheap `find`-based hash if you want to stay git-agnostic), verdict, exit code. Have `approve` read the last line and print, unmissably, one of: `preflight: PASS @ <fp> (current)`, `preflight: STALE (checked <fp>, now <fp2>)`, or `preflight: ABSENT`. Blocking is optional and arguably wrong given GROK-SEAT doctrine; *silence* is not optional. The rule to write into the spec: **the gate may be human, but the gate must leave a trace.**

**🟠-3 — Exit-code semantics are undefined, so callers cannot distinguish "refused" from "broken".**
Pointers: `aether` dispatch and `die` usage; `docs/GROK-SEAT.md` integration guidance; SPEC (no exit-code section).

Today a wrapper, CI job, or agent harness has no documented way to tell "preflight ran and correctly refused" from "preflight crashed" from "you typed nonsense" (currently: 0). Any external seat that automates around `aether` will therefore either treat all non-zero as failure (losing the refusal signal) or all zero as success (see 🔴-1). Both are wrong.

Fix: publish a four-line table and honour it — `0` success/allowed; `1` internal error/unexpected; `2` usage error (unknown verb, bad args); `3` protocol refusal (preflight failed, gate not satisfied). Reserve the rest. This is a prerequisite for 🔴-1's fix and for anyone integrating the TUI without reading the source.

**🟠-4 — No static-analysis or negative-path gate on a file that is now the authority layer.**
Pointers: `aether` (~1880 lines POSIX sh); test suite; absence of shellcheck invocation anywhere I could find (unverified — see Non-claims).

The v0.2 file is large enough that the classic sh failure modes L10–L13 flagged are back in scope: unquoted expansions, `[ ]` vs `[[ ]]` portability drift, `local` in strict POSIX, subshell-swallowed failures, `set -e` interacting badly with pipelines and command substitution. The existing tests appear to be happy-path/behavioural. The bug in 🔴-1 is exactly the kind a negative-path test catches in one line and a human reviewer misses forever.

Fix: (a) `shellcheck -s sh aether` in the test entrypoint, failures fatal, existing warnings triaged into an explicit inline-disable list rather than a silent baseline; (b) a `tests/negative.sh` that asserts non-zero + no status-shaped output for: unknown verb, each single-character mutation of every authority verb, missing required args, and a nonexistent path argument. This is the cheapest possible insurance against 🔴-1 recurring under a different name.

**🟠-5 — Documentation surface has outgrown the protocol; nothing is marked normative, and versions have skewed.**
Pointers: `SPEC-v0.1.md` (still the only spec) vs `aether` v0.2 header; `CORE_PRINCIPLES.md`, `PRODUCT.md`, `README`, `docs/GROK-SEAT.md`, `docs/SINGLE-APP-DISTRIBUTION.md`.

There are now at least six documents making load-bearing statements, and they disagree: the spec describes a ≤220-line tool that no longer exists, PRODUCT.md sells an adoptable protocol the LICENSE gap forbids adopting (🔴-2), GROK-SEAT.md defines a gate the CLI cannot evidence (🟠-2), and CORE_PRINCIPLES.md asserts minimalism 🟠-1 contradicts. Individually each is fine. Collectively, a reader cannot determine which sentence wins when two conflict — which is the same defect as an undefined exit code, one layer up.

Fix: one line at the top of each file: `NORMATIVE` or `NON-NORMATIVE (narrative; defer to SPEC)`. Exactly one spec is normative, and it is versioned to match the tool. Everything else is commentary. Then either bump the spec to v0.2 with the deltas from 🟠-1 and 🟠-3 folded in, or rename the current file `SPEC-v0.1-HISTORICAL.md` so nobody cites it as live.

### 🟡 Worth doing, cheap, not blocking

**🟡-1 — No `CHANGELOG`, so the v0.1→v0.2 delta exists only in the diff.** The tool grew ~8× and gained an authority layer with no narrative record of what changed or why the LOC criterion moved. Add a terse append-only changelog; it costs nothing and it is the artifact that makes 🟠-1's "we retired that criterion deliberately" credible rather than retroactive.

**🟡-2 — `aether help` (if present) is hand-maintained and can drift from dispatch.** Pointer: dispatch case statement vs any usage text. Fix: generate the verb list from a single array/list consumed by both dispatch and help, or add a test asserting every dispatch branch appears in help output and vice versa. This is the same class of defect as 🔴-1 — the tool's self-description diverging from its behaviour.

**🟡-3 — No shell completion, which is the practical mitigation for the typo class.** 🔴-1's fix makes mistyped verbs *loud*; completion makes them *rare*. Ship a small `completion.sh` for the verb list once 🟡-2 gives you a single source. Explicitly not a substitute for 🔴-1.

**🟡-4 — Session lab boundary is unlabelled.** A reader cannot tell which directories are shipped protocol and which are experiment. One `README` line per experimental directory (`status: lab, not covered by SPEC, may vanish`) prevents someone vendoring a prototype as protocol — and interacts with 🔴-2, since the license question may answer differently for lab code.

**🟡-5 — `docs/SINGLE-APP-DISTRIBUTION.md` describes outputs nobody may legally distribute.** Strictly downstream of 🔴-2; listed separately because once the license lands, this doc needs one sentence stating the terms the distributed artifact inherits.

**🟡-6 — No `--version` / version is duplicated between the `aether` header and docs.** Single constant, printed by `--version`, asserted by a test. Trivial, and it is what lets a bug report be reproducible.

### What the legacy critique got right (spirit)

I want to be precise here, because the host interim treats the legacy critique as largely superseded and I think that undersells it. Its *details* have aged badly — line counts are stale, several named verbs no longer exist, and some findings were fixed in v0.1.x. Its *instincts* were correct and remain unaddressed:

- **L24 (self-contradiction as the primary risk).** Right, and now more right. A project whose value proposition is legibility fails first by drifting from its own stated doctrine, not by crashing. 🟠-1, 🟠-5 and 🟡-2 are all instances of exactly this shape: the artifact and its self-description diverging. The correct response to L24 was never "the numbers are wrong" — it was "then fix the numbers or retire the criterion."
- **L10–L13 (large POSIX sh is a fragility surface).** Right in kind. The specific bugs it named may be gone; the class is not, and 🔴-1 is a live member of that class sitting in the authority layer. 🟠-4 is the systemic answer.
- **Silence-read-as-permission as the governing anti-pattern.** The legacy critique named this before there was an authority layer to violate it. 🔴-1 and 🟠-2 are the two places where the current design manufactures that silence — one by accident, one by omission.
- **Adoption friction as a real defect, not a business concern.** It flagged that a protocol nobody can legally take is not a protocol. That is 🔴-2, still open, still a one-file fix.

The spirit-level summary: the legacy reviewer understood that in this project **doctrine is load-bearing**, and that unretired success criteria are how protocols rot. That judgement holds. I would treat "legacy critique is stale" as true of its line numbers and false of its thesis.

### What to do next (ordered, thin)

Ordered by "cheapest thing that closes the largest honesty gap." Each is deliberately small; none require redesign.

| id | action | closes | size | done when |
|---|---|---|---|---|
| `NEXT-01` | Unknown/mistyped verb → non-zero, no status-shaped output. Path-arg only if `[ -d "$1" ]`. | 🔴-1 | ~10 lines | `aether nexr` exits 2, prints an error, prints no report |
| `NEXT-02` | `tests/negative.sh`: garbage verb, single-char mutations of each authority verb, missing args, bad path. | 🔴-1, 🟠-4 | small | suite fails if `NEXT-01` regresses |
| `NEXT-03` | Add LICENSE (MIT or Apache-2.0), state it in README, state Session-lab terms explicitly. | 🔴-2, 🟡-5 | one file | a third party can vendor `aether` without asking |
| `NEXT-04` | Publish exit-code table (0/1/2/3) in the spec; make `die` honour it. | 🟠-3 | small | wrapper can distinguish refusal from crash |
| `NEXT-05` | Decide 🟠-1 explicitly: retire ≤220/"one screen" in a v0.2 spec with a defensible budget, **or** split the CLI. Record the decision in `CHANGELOG`. | 🟠-1, 🟡-1 | decision + doc | no minimalism claim stands over an 1880-line file |
| `NEXT-06` | Preflight leaves a receipt; `approve` prints `PASS (current)` / `STALE` / `ABSENT` unmissably. | 🟠-2 | ~25 lines | a session can be audited after the fact |
| `NEXT-07` | `shellcheck -s sh aether` fatal in the test entrypoint; triage existing findings to inline disables. | 🟠-4 | plumbing | clean run, no silent baseline |
| `NEXT-08` | Mark every doc `NORMATIVE` / `NON-NORMATIVE`; version the spec to match the tool. | 🟠-5 | doc pass | conflicts have a documented winner |
| `NEXT-09` | Single verb list feeding dispatch + help; `--version` from one constant; completion script. | 🟡-2, 🟡-3, 🟡-6 | small | help/dispatch drift is test-caught |
| `NEXT-10` | Status line per lab directory. | 🟡-4 | trivial | shipped vs experimental is legible |

`NEXT-01`+`NEXT-02` and `NEXT-03` are independent and should land first; they are hours, not days. `NEXT-05` is the only item requiring a judgement call rather than typing, and it is the one I would not let slip — everything else is mechanical, and mechanical debt is not what kills a doctrine project.

### Non-claims

To keep this review falsifiable, here is what I did **not** establish:

- **I did not run the test suite, `aether`, or `shellcheck`.** Every behavioural statement — including 🔴-1's exit-0 claim and the "no shellcheck gate" claim in 🟠-4 — is read off the source and docs. If `aether nexr` in fact exits non-zero on your machine, 🔴-1 collapses to a documentation finding and I want to be told so.
- **I did not read all ~1880 lines.** I read dispatch, the authority verbs, `die`, and the docs named in each pointer. There may be worse things further in. Absence of a finding is not evidence of absence.
- **Line numbers and exact filenames may have drifted** since the tree I read. Pointers are intended to survive drift; treat them as "find this construct," not "go to line N forever."
- **I did not independently fetch live anphuni.com Session/privacy HTML, GitHub Actions status, or re-run smoke-verify.** Host ground truth and prior GPT-5.6 absorb are taken as given where cited.
- **I did not re-measure public star/fork counts or language percentages** from the legacy paste.

---

*Continuation: second OpenRouter call after truncation at 🟠-2. Final Non-claims bullets completed by host for truncation closure only (no new findings).*
