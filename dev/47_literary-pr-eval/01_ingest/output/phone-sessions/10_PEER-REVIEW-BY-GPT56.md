Verdict: do not merge yet

The CI runs are green, but I found one serious test-safety bug, one likely read-only contract violation, and several authority/provenance inconsistencies that undermine the exact thing Mechanicall is claiming to preserve.

Reviewed head: 85139b2

1. Blocker: the verb-list test executes destructive commands in the real repo

At the beginning of tests/run.sh, this loop executes every listed verb without arguments:

for v in $verbs; do
    set +e
    out=$("$AETHER" "$v" 2>&1)
    ec=$?
    set -e
    ...
done

That is not merely checking dispatch. Some verbs are valid with no arguments and operate on the current directory, including:

- approve
- reject
- brief
- distill
- possibly init, repair, status, and other default-path commands

Because this loop runs before the test suite creates and enters its temporary test project, it can mutate the actual checkout's:

- CURRENT.md
- DECISIONS.md
- .aether/events.jsonl
- .context.md
- preflight receipts/state

The PR’s ledger contains evidence of exactly this:

{"kind":"approve","reason":"APPROVED","by":"human"}
{"kind":"reject","reason":"REJECTED","by":"human","phase":"SELECT"}

Those generic approve/reject pairs appear during test activity, followed by preflights under Status=REJECTED. This means the test suite can manufacture events labelled "by":"human" and alter the repository authority state.

Required fix

Do one of:

1. Run the verb-dispatch loop inside a disposable project created before any verb is executed; and still exclude destructive verbs.
2. Better: test the declared verb list against dispatch/help metadata without invoking each command.
3. Add a dedicated non-mutating dispatch option such as aether help  and test that.

Also add a CI assertion that the source checkout remains unchanged:

git diff --exit-code
git status --porcelain

Allow only explicitly expected ignored test artifacts.

This is a merge blocker because sh tests/run.sh must not rewrite the operator’s real authority files.

2. Blocker: committed ledger contains test noise presented as human authority

The PR adds 215 lines to .aether/events.jsonl, including entries such as:

{"kind":"approve","reason":"abs /tmp/tmp.kBvJYkZSsY","by":"human"}
{"kind":"approve","reason":"pass /tmp/tmp.kBvJYkZSsY","by":"human"}
{"kind":"approve","reason":"stale /tmp/tmp.kBvJYkZSsY","by":"human"}
{"kind":"approve","reason":"APPROVED","by":"human"}
{"kind":"reject","reason":"REJECTED","by":"human","phase":"SELECT"}

These are clearly smoke/integration-test operations, not meaningful human project decisions.

That creates a provenance problem:

- Tests are represented as "by":"human".
- Root project events are mixed with temporary test events.
- Repetitive preflight probes dominate the durable ledger.
- The resulting record cannot reliably distinguish actual authority from test exercise.

For a product whose central claim is durable receipts of human authority, that distinction needs to be trustworthy.

Required fix

Before merge:

- Remove the test-generated additions from the root project ledger, or move them into a clearly labelled fixture.
- Introduce provenance such as:
  - "by":"test"
  - "actor":"ci"
  - "environment":"sandbox"
- Ensure integration tests always use a temporary AETHER_PROJECT/working directory.
- Add a regression test proving tests do not touch the repository’s root ledger.

If you intentionally want to preserve these as historical development evidence, put them in a non-normative receipt under dev/, not in the live instance ledger.

3. Likely contract violation: probe is described as read-only but uses preflight machinery

The normative spec describes:

aether probe  [path] — Read-only would-preflight

However, the implementation path shown in aether has cmd_probe calling cmd_preflight. Preflight now writes:

- .aether/preflight-last
- .aether/preflight.jsonl
- .aether/events.jsonl

Therefore probe appears to mutate the project despite being described as read-only.

brief also calls preflight internally, so merely asking for a brief may similarly manufacture a preflight event and replace the last receipt.

Why this matters

A probe should answer:

“Would this action pass?”

It should not become evidence that a real preflight occurred. Otherwise an exploratory read can create or refresh the receipt later displayed by approve.

Required fix

Separate gate evaluation from receipt writing:

- Internal evaluator: no writes, returns allow/refuse and reason.
- probe: evaluator only.
- brief: evaluator only.
- preflight: evaluator plus durable receipt/event.

Then test hashes or snapshots of all relevant files before and after probe and brief.

4. Documentation contradiction: refusal exit code is both 2 and 3

SPEC-v0.2.md defines:

- 2 = usage error
- 3 = protocol refusal

The tests also expect probe and next refusal to exit 3.

But docs/PROTOCOL-LAB.md still says:

./aether probe   # exit 0 allow, 2 refuse

That should be 3, not 2.

There are also stale comments in the tests referring to missing arguments or refusals as exit 1/2 while the assertions expect 2/3. Runtime assertions matter more, but the comments should be corrected to avoid future regressions.

5. PR scope statement conflicts with its contents

The PR says:

“Archive / LAB material stays out of this PR”

and:

“Explicitly not this PR’s identity: … client session archaeology”

But the commits add substantial archive/LAB material, including:

- numerous dev/18_opus5-protocol-completion/** peer artifacts and receipts;
- a roughly 482-line GPT peer response under dev/17_client-one-session-three/**;
- a duplicate copy of that response under dev/18_opus5-protocol-completion/**;
- seat/README.md;
- domains/README.md;
- research/README.md.

This may be acceptable documentation work, but it contradicts the PR description. In particular, duplicating the same long peer response in two archive paths adds repository weight without additional authority.

Required decision

Either:

- remove/archive the duplicated and client-specific material from this PR; or
- rewrite the PR description to say it includes archive/LAB classification and peer-evidence files.

Do not merge with a checklist asserting that archive/LAB material was excluded when it demonstrably was not.

6. CI is green, but it does not test the most important failure mode

Both GitHub Actions runs for the head commit completed successfully:

- Run 35
- Run 34

That is good, but CI currently permits the tests to dirty the checkout. It checks whether commands return the expected values, not whether the testing process corrupted the repository authority state.

There are also Node.js 20 deprecation warnings for older action versions. Those are non-blocking, but update actions/checkout and actions/setup-python when practical.

Recommended pre-merge checklist

Ask the agent to push a corrective commit that does all of the following:

- [ ] Move test setup before any aether verb execution.
- [ ] Stop executing every verb merely to verify dispatch.
- [ ] Prove tests/run.sh leaves the source checkout unchanged.
- [ ] Keep all test events inside disposable sandboxes.
- [ ] Remove test-generated "by":"human" records from the root ledger.
- [ ] Make probe and brief genuinely non-mutating.
- [ ] Add no-mutation tests for probe and brief.
- [ ] Change Protocol Lab’s refusal exit code from 2 to 3.
- [ ] Correct stale exit-code comments.
- [ ] Remove duplicate peer-review artifacts or justify them.
- [ ] Reconcile the PR’s “no archive/LAB” statement with its actual files.
- [ ] Re-run CI from the corrected head.
- [ ] Confirm git status --porcelain is empty after the complete test suite.

Bottom line

The feature direction is coherent, and CI success is encouraging. But a test suite that can approve/reject the real project and append those operations as human receipts is exactly the class of authority confusion Mechanicall is supposed to prevent.

I would request changes rather than merge the current head.