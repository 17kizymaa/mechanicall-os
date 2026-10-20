# Receipt — pre-apply a suggestion

**Not a Yes.** Live `CURRENT.md` was not rewritten. `cksum 3835662854`, 15405 bytes, before and after the temp-project check.

## What the command does

`aether pre-apply [reason words] [project]`

No suggestion file. The operator allows approval for this one turn. The command logs `turn_approval` with `"by":"operator"` and `"scope":"turn"`, then stamps approve. It does not copy a body. It is not a mode. A second run is another turn the operator typed.

A suggestion file remains optional. When one is given, the command still copies that `# CURRENT` body and then stamps. A path under `.aether/proposals/`, a `CURRENT-proposal-*` name, and a proposal wrapper are refused.

It refuses:

- a path under `.aether/proposals/`
- a name `CURRENT-proposal-*`
- a proposal wrapper, including a `Proposed CURRENT` heading
- a missing reason or a missing file (exit 2, no write)
- the slow hands already on `apply --approve` (exit 2, no write)

`--dry-run` writes nothing and does not stamp.

## Plugin

`commands/pre-apply.md` in the installed mechanicall-domain plugin. Model invocation is disabled. The grey argument list loads at session start.

## Check

Temp project only. Missing args exit 2. Proposal path, proposal name, and wrapper exit 3. A slow hand exits 2. A real suggestion prints `SUGGESTION APPLIED` and `APPROVED: operator approves the suggestion`. Live `CURRENT.md` stayed `3835662854`.

`sh tests/run.sh` stops earlier in `scripts/ci-control-layer-gates.sh`, which still expects `aether desk` to die. That check is from before `desk` shipped. The new section in `tests/run.sh` did not run inside that suite.

## Not done

The APK was not assembled. versionCode was not bumped. `.grok/personas/` was not edited. This command was not run on the live tree.
