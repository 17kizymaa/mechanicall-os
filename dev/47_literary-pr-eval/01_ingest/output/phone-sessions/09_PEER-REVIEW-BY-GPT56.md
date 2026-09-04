Direct verdict

You have built something real. The feedback does not invalidate it. It identifies that the differentiated value is not yet obvious—or externally proven.

Mechanicall is not merely Claude Code’s “approve plan” rebuilt in shell. But your message made the distinction sound philosophical rather than operational.

The real distinction is:

Claude Code controls what Claude may do inside a Claude session. Mechanicall records what the project has currently authorized outside any one model, chat, or vendor.

That is a legitimate layer. It is also narrower than some of your language suggests.

CI currently proves that:

- CURRENT parses;
- one action can be named;
- preflight deterministically allows/refuses it;
- events are emitted;
- lifecycle commands behave as tested.

CI does not prove:

- every agent calls preflight;
- the human, rather than an agent, invoked approve;
- CURRENT improved a real project;
- another user understands the protocol;
- the authority survives cross-tool work better than existing plans.

That is fine for a protocol alpha. It means the next work is comparative proof, not more automation.

1. Claude Code versus Mechanicall

Your peer’s screenshot is a fair challenge. Claude Code now has:

- Plan Mode;
- a human plan-approval prompt;
- read-only planning before edits;
- per-tool permissions;
- deny/ask/allow rules;
- protected paths;
- session resume;
- an auto-mode classifier;
- hooks and sandboxing.

So these are not unique Mechanicall claims:

- “AI proposes a plan.”
- “Human approves.”
- “Dangerous commands can be refused.”
- “A plan exists as Markdown.”
- “Sessions can resume.”
- “The agent has an audit trail.”

Anthropic’s documentation explicitly says Plan Mode proposes without editing until approval, while permission modes and rules govern tool execution. It also notes that conversational boundaries can disappear through context compaction unless turned into harder permission rules.  
Sources: Claude Code permission modes · common workflows

The actual layer distinction

| Layer | Question | Claude Code | Mechanicall |
|---|---|---|---|
| Tool permission | May this tool run? | Strong, integrated | Not the core |
| Session planning | May Claude implement this plan? | Plan Mode | Partly overlapping |
| Project authority | What decision binds this project now? | Usually session/tool-specific | CURRENT.md |
| Cross-tool continuity | Does the same live decision follow Claude, Grok, Cursor and shell? | Not its primary contract | Mechanicall’s intended wedge |
| Semantic action gate | Is named project action X the one permitted Next? | Possible through rules/hooks | Native preflight concept |
| Enforcement | Can bypass be technically prevented? | Stronger inside Claude Code | Cooperative today |
| Ownership | Can the user inspect/edit authority independently of vendor UI? | Plans/settings exist, but Claude-specific | Explicit core principle |

Mechanicall should not claim it is safer than Claude Code. Claude currently has stronger native enforcement inside its own harness.

Mechanicall’s claim is:

The current project decision remains vendor-neutral, project-owned and inspectable when the conversation closes or the operator changes tools.

That is complementary to Claude Plan Mode, not a replacement for it.

2. The clearest product explanation

Your current explanation begins with a critique of SaaS vendors:

They treat history, embeddings and memory as authority...

That is intellectually coherent, but it makes the reader decode your theory before understanding the object.

Lead with the object:

Mechanicall keeps one live project decision outside the chat.  
CURRENT.md records the agreed objective, one permitted next action and what is prohibited. Any cooperating agent can check that same file before acting, and the decision survives when you close the chat, return tomorrow or switch AI tools.

Then distinguish it:

Claude Code Plan Mode governs a Claude session. Mechanicall is intended to preserve the project’s current decision across sessions and tools. Its enforcement is cooperative today: agents must call preflight.

That is understandable without “authority substrate,” “integrity layer,” or Domain metaphors.

Shortest viable pitch

One project, one live decision—outside any chat.

Slightly fuller pitch

Mechanicall is a vendor-neutral project checkpoint for AI work. It keeps the latest agreed objective, one next action and explicit prohibitions in a readable file that Claude, Grok, scripts and humans can inspect.

3. A good response to your peer

Send something shorter than another architecture manifesto:

That’s a fair comparison. Mechanicall is not trying to replace Claude Code’s Plan Mode or permission prompts. Claude’s controls govern what Claude can do inside its session.  
  
Mechanicall’s narrower idea is that the project’s current decision should live outside any one chat or vendor: one readable file naming the agreed objective, the single next action and what is prohibited. Claude, Grok, Cursor or a script can consult the same state, and preflight gives them the same deterministic answer.  
  
Enforcement is cooperative today, so I’m not claiming it is a stronger sandbox than Claude Code. The next thing I need to prove is whether the shared authority file materially helps a project resume across different tools or after an interruption. If it doesn’t, then the differentiation is not strong enough yet.  
  
Thanks—the screenshot is exactly the comparison I need to test rather than explain away.

That answer is confident because it concedes the overlap precisely.

4. Are you drifting into automation?

Somewhat—but not because you wrote scripts

The appliance work can be legitimate engineering. The drift appears in the authority ritual itself.

Your decision log contains entries such as:

APPROVED: --help
APPROVED: APPROVED
REJECTED: REJECTED
APPROVED: abs /tmp/...
APPROVED: pass /tmp/...
APPROVED: stale /tmp/...

It also records extremely rapid cycles of:

NEXT_SELECTED
APPROVED
NEXT_SELECTED
APPROVED

This makes it difficult to distinguish:

- a meaningful human decision;
- a CLI regression test;
- an implementation checkpoint;
- a temporary path test;
- an actual authorization affecting the world.

That is ritual automation drift.

The issue is not “too many events.” The issue is that the event vocabulary no longer preserves the meaning you built the protocol to protect.

Concrete correction

Keep two evidence classes separate:

.aether/events.jsonl       # every mechanical event/test
DECISIONS.md               # meaningful human project decisions only

Do not promote test arguments into the human decision ledger.

A valid human decision should answer:

1. What changed?
2. Why?
3. What was authorized or rejected?
4. What remains open?
5. Which artifact or external condition supports it?

The protocol becomes less credible if APPROVED: --help sits beside an actual destructive disk-install authorization.

5. Your two CURRENT files expose a lifecycle problem

Mechanicall protocol Domain

It currently says:

Phase: APPROVE
Status: APPROVED
Next: defer-package-alpha-for-server-ops
Approval: APPROVED

The deferral has already happened and has a receipt. Therefore this is completed authority presented as an active Next.

It should now be either:

Phase: SELECT
Status: DRAFT
Next: unset
Approval: PENDING

or explicitly idle:

Phase: SELECT
Status: BLOCKED-PENDING-HUMAN
Next: unset
Approval: PENDING

The protocol repo does not need an action whose only purpose is to preserve the fact that another Domain is active. That fact belongs in the receipt and decisions log.

server_ops appliance Domain

It currently says:

Phase: APPROVE
Status: APPROVED
Next: emachine-image-and-first-boot
Approval: APPROVED

But the receipt says:

- physical disk not confirmed;
- no installation was run;
- first boot remains open;
- target device is unreachable;
- operator presence is required.

That is not completed approval state. It is an authorized operation blocked on a physical gate.

More honest state:

Phase: EXECUTE
Status: BLOCKED-PENDING-HUMAN
Next: emachine-physical-install
Approval: PENDING

The prose can say the build/runbook was approved, while the destructive physical action still requires explicit target confirmation.

This reveals a real schema pressure:

“Approved to attempt” and “output accepted” are not the same approval.

You do not need to add a new field immediately. Use phase and status correctly:

- COMMIT/APPROVED — plan authorized;
- EXECUTE/ACTIVE — work underway;
- EXECUTE/BLOCKED-PENDING-HUMAN — effect needs a physical decision;
- REVIEW/READY-FOR-REVIEW — artifact exists;
- APPROVE/APPROVED — result accepted;
- then re-select, with Next: unset until the next decision.

6. Is server_ops useful or avoidance?

It can be useful in two ways:

1. it may create the eventual casual appliance;
2. it is a serious dogfood project for Mechanicall.

But it does not yet prove the product’s differentiation.

Installing NixOS, configuring Wi-Fi, Tailscale, persistent Grok and a kiosk demonstrates operational engineering. It does not establish that CURRENT performed better than:

- a runbook;
- a GitHub issue;
- a Claude plan;
- a checklist;
- ordinary project notes.

The appliance becomes product evidence only if you can show something like:

We stopped for two days, resumed from another machine/tool, and CURRENT prevented the operator or agent from repeating the prior destructive setup mistake.

That is a Mechanicall result.

Without that comparison, server_ops is adjacent engineering.

Recommendation

Do not kill the eMachine setup. Time-box it:

- complete or explicitly park the physical installation;
- record one authority failure prevented or one resume event improved;
- do not expand to Geobook;
- do not add another appliance feature;
- return to external protocol proof.

7. The next product experiment

You do not need a broader casual UI to answer the differentiation question.

Run one cross-tool, cross-session proof.

Test question

Does a project-owned CURRENT make resumption and scope control better when the user changes agent or returns later?

Procedure

Session 1 — Claude Code

- Start a bounded project.
- Use Claude Plan Mode normally.
- Human approves the plan.
- Translate the binding result into CURRENT.
- Produce one artifact.
- Stop before completion.

Session 2 — different tool

After at least one day:

- open the same folder in Grok, Cursor or another agent;
- do not provide the old chat transcript;
- allow it to read AGENTS.md and CURRENT;
- ask it to state:
  - objective;
  - Next;
  - Prohibited;
  - last evidence;
- attempt one plausible but prohibited action;
- require preflight;
- continue only the permitted Next.

Compare against ordinary chat/plan

Measure:

- time to recover state;
- number of incorrect assumptions;
- whether rejected work returns;
- whether the new tool identifies the same Next;
- whether the user must search old conversations;
- whether the agent attempts a prohibited action;
- whether CURRENT needed manual correction;
- whether the user voluntarily keeps it.

Pass condition

Mechanicall earns differentiation if:

A second tool can resume the correct project state without access to the original vendor session, and a stale or prohibited action is caught by the same project-owned contract.

That is much stronger than another refusal demo inside Mechanicall itself.

8. What CI does—and does not—mean

You are right to value the CI.

It means Mechanicall is not merely a philosophy document. The parser, lifecycle commands, exit behavior and tests are executable.

State the claim precisely:

Mechanicall has a CI-tested reference implementation of a filesystem authority protocol.

Do not stretch it to:

Mechanicall provides deterministic authority over agents.

Authority remains partly social because:

- external agents can skip preflight;
- any filesystem-capable process can edit CURRENT;
- approve does not authenticate a human;
- Grok hooks are observational;
- a model can technically invoke the command if given unrestricted shell access.

The deterministic component is:

Given a specific CURRENT and action ID, the reference implementation returns a repeatable allow/refuse result and records it.

That is real and worth shipping.

9. What to stop saying

Avoid these claims for now:

- “Other providers neglect authority.”
- “One document syncs the conversation.”
- “Deterministic AI project control.”
- “Human-only approval” without saying it is protocol-level.
- “Better than agent harnesses.”
- “The software is a finished product.”
- “Session is private” without qualifications.
- “The appliance is Mechanicall distribution” before a user can operate it.
- “Domain” in public copy without translating it into literal behavior.

Prefer:

- project-owned;
- cross-session;
- cross-tool;
- one current decision;
- inspectable;
- cooperative;
- vendor-neutral;
- reference implementation;
- explicit limitations.

10. Recommended authority now

For the protocol Domain, the highest-value Next is no longer packaging panic or more commands.

CURRENT

Objective: Prove whether a project-owned CURRENT improves cross-tool project resumption beyond ordinary agent plan approval.
Phase: SELECT
Status: ACTIVE
Baseline: Mechanicall protocol alpha on master + Claude Code Plan Mode comparison
Next: run-cross-tool-resume-proof
Approval: PENDING

Keep
- CURRENT as project-owned live authority
- One Next
- Cooperative preflight language
- Existing CI-tested reference implementation
- Claude Plan Mode treated as complementary, not dismissed
- Evidence from a real interrupted project

Reject
- New protocol commands
- New dashboard or appliance features
- Claims of stronger sandbox enforcement
- Explaining differentiation only through abstract doctrine
- Geobook work
- Automatic promotion of test events into DECISIONS

Limits
- One project
- Two different agent tools
- At least one interruption
- No sensitive client data
- No new implementation unless the test exposes a concrete blocker

Next allowed action
Run one bounded project across two sessions and two agent tools. Record recovery time, incorrect assumptions, prohibited-action behavior and whether the second tool resumes from CURRENT without the original chat.

Approval condition
Human reviews the comparison and decides whether CURRENT delivered material value beyond ordinary plan approval.

Prohibited
- add-new-command
- build-new-seat
- claim-cross-tool-proof-before-test
- auto-approve
- expand-appliance-scope

The server_ops Domain can remain separately blocked on its physical operator gate.

Bottom line

You are not discovering that the project is fake.

You are discovering that:

“Human approval and plans” is already crowded territory.

Your differentiated hypothesis is more specific:

The binding project decision should be a vendor-neutral artifact outside every chat, reusable across tools and interruptions.

That hypothesis is technically embodied in code. It is not yet behaviorally proven.

The peer’s confusion is valuable because your current explanation foregrounded a critique of AI providers instead of demonstrating the cross-tool handoff.

So: no shame spiral, no feature spiral, no defensive architecture essay.

Clean the lifecycle states. Separate test events from human decisions. Finish or park the physical appliance gate. Then run the cross-tool resume proof.

You built a real protocol. Now prove the protocol does something a session-level approval button does not.