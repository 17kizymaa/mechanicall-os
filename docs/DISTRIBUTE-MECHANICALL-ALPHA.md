DISTRIBUTE-MECHANICALL-ALPHA.md

Verdict

GO: distribute Mechanicall OS now as a small, public technical alpha.

NO-GO: sell Club-cortex as an operational backend retainer yet.

The branch contains a real product nucleus:

A plain-file authority protocol for AI-assisted projects: declare the one permitted action, record decisions and artifacts, and refuse actions outside the current human-approved boundary.

That is useful, demonstrable, and more concrete than the earlier “awareness OS” language.

But the linked branch is not yet a distributable release, and Club-cortex is still service research rather than a delivered product.

The right sequence is:

release Mechanicall alpha
        ↓
observe three external users
        ↓
offer paid setup/support
        ↓
learn which repeated operations justify a backend
        ↓
only then test Club-cortex membership

Do not reverse this by building the club before anyone has adopted the protocol.

1. Branch reality

The linked branch currently points to commit:

aecd460f6fbc93690d7f1ee51615b67fbddc8f6b
2026-07-22
docs: PR statement of changes for personal-llm propose layer

It is two commits ahead of master, with the functional change in 989b115 and a documentation commit afterward. The Club-cortex and July 25 financial documents pasted in your message are not visible on that linked branch. They should therefore be treated as local research unless pushed somewhere else.  
Sources: branch · branch API · comparison

What is genuinely shipped on the branch

- CURRENT.md authority format
- deterministic aether preflight
- approve/reject state changes
- append-only events
- artifact registration
- Rhizome capture and session ledgers
- hook trust improvements
- tests covering primary authority paths
- optional Ollama model selection
- personal-model SYSTEM doctrine
- model-output flagging helpers
- reel and development-task examples
- explicit anti-hallucination fence in NOT-IMPLEMENTED.md

That is a coherent alpha.

What the personal-model commit actually adds

The public integration currently:

1. discovers personal Ollama tags;
2. prefers personal-llm-sft-v2, then full and pilot variants;
3. optionally injects the Mechanicall doctrine prompt;
4. connects the model to garden and rival;
5. flags some secret-like text and unsafe command suggestions.

It does not publicly ship:

- model weights;
- training tools or datasets;
- proposal automation;
- email or Upwork integration;
- negotiation machinery;
- a model evaluation interface;
- Club-cortex accounts or queues;
- train-job scheduling;
- multi-user isolation;
- adapter lifecycle management.

The current public consumers are garden and rival, not a sales-proposal product. The adapter may already help you privately, but that use is not yet represented as a reproducible public capability.  
Sources: Personal LLM layer · aether_llm.py · model tests

2. The strongest product claim

Your current README says Mechanicall blocks unapproved execution. That is directionally correct but technically too strong.

aether preflight can refuse an action when the operator or agent calls it. It cannot presently prevent an unconstrained agent from:

- skipping preflight;
- editing CURRENT.md;
- invoking aether approve;
- running a shell command directly;
- writing an artifact without registering it.

“Human only” is presently a protocol rule, not an authenticated identity boundary.

Therefore the honest alpha claim is:

Mechanicall gives humans and AI agents an inspectable authority contract and deterministic preflight gate for project actions.

Or more directly:

Mechanicall tells an AI agent what it may do next—and gives it a deterministic way to refuse everything else.

Do not yet say:

“Mechanicall guarantees that agents cannot perform unapproved actions.”

That would require an enforced wrapper, capability boundary, permissions layer, or integration through which consequential actions must pass.

This is not a reason to delay distribution. It is a reason to label the boundary correctly.

3. Where you overlap with GSD—and where you do not

Your excitement about converging with GSD is justified. Both systems recognize that chat history cannot be the only project state.

GSD maintains project, roadmap, requirement, state, phase, plan, verification, and review artifacts. Its workflow is broadly:

discuss → plan → execute → verify → review → ship

It also requires roadmap approval before implementation and tracks decisions across planning and verification.  
Source: GSD User Guide

OpenSpec similarly uses plain Markdown proposals, specifications, designs, tasks, implementation and archival. Spec Kit provides a comprehensive specification-to-plan-to-task-to-implementation process.  
Sources: OpenSpec · GitHub Spec Kit

The overlap

- filesystem-native project state;
- explicit phases;
- human review;
- recoverability across sessions;
- plans and artifacts rather than ephemeral prompts;
- deterministic checks around AI work.

Mechanicall’s defensible difference

GSD, OpenSpec and Spec Kit primarily answer:

“How do we define, plan and execute software work?”

Mechanicall can answer a narrower but more general question:

“Given everything this project has captured, what is the one action presently authorized—and what must the agent refuse?”

That can apply to:

- video editing;
- client communication;
- archive operations;
- model training;
- data migration;
- creative projects;
- software development.

Your wedge is not “better GSD.”

It is:

A tiny, agent-agnostic authority and refusal layer that can sit beneath GSD, OpenSpec, Grok Build, Claude Code, or an ordinary shell session.

That is worth distributing.

4. What the personal adapter means

The adapter is not the product moat yet.

Its current behavior—especially over-refusing commercial prompts—shows that it has learned the boundary language more strongly than the commercial task. That is not failure. It makes the adapter useful as:

- a doctrine checker;
- a privacy-sensitive first drafter;
- a contradiction detector;
- a claim-risk reviewer;
- a taste/proposal sidecar.

It is not yet reliable as:

- a sales closer;
- an offer designer;
- a factual financial model;
- an autonomous negotiator;
- the primary reason somebody buys Mechanicall.

The important architecture is:

personal model proposes
        ↓
Mechanicall checks authority
        ↓
human decides
        ↓
external action occurs

Not:

personal model knows me
        ↓
therefore it may act for me

The adapter’s first public demonstration

Give the public model interface one narrow job:

Draft a proposed update to CURRENT.md from a reflection while preserving facts, inferences, unknowns, and prohibited actions as separate fields.

Output only:

Observations

Inferences

Unknowns

Proposed CURRENT change

Conflicts with existing authority

Human decision required

Then the user manually reviews and applies it.

That demonstrates personal-model value without requiring you to distribute private weights or promise model magic.

5. Distribution blockers

Mechanicall is public, but it is not yet properly open source or release-shaped.

P0 — Add a license

The repository currently has no detected license. GitHub reports license: null, and the license endpoint returns 404.

Without a license, people may read the source, but they do not receive clear permission to use, modify or redistribute it. That contradicts the “open-core” claim.

Choose deliberately:

- MIT if maximum adoption and reuse matter;
- Apache-2.0 if explicit patent language matters;
- another license only if you can clearly explain why.

For this project, Apache-2.0 or MIT is the practical choice. Do not call it open-core before this is settled.  
Sources: repository metadata · license endpoint

P0 — Merge the release candidate

The product-facing work is on a feature branch while master remains the default branch.

Before inviting users:

1. open or finalize the PR;
2. run the test suite on a clean clone;
3. merge into the default branch;
4. tag the exact tested commit.

P0 — Add real CI

The repository has no project test workflow visible through GitHub Actions; only GitHub’s dependency-graph workflow is reported.

Add one minimal workflow that runs:

sh tests/run.sh

on pushes and pull requests.

You do not need a large matrix yet. One Linux runner is enough for the alpha.  
Source: Actions workflow API

P0 — Cut an actual release

There are currently no tags or GitHub releases.

Create:

v0.2.0-alpha.1

Include:

- checksum or source archive;
- installation instructions;
- supported environment;
- known limitations;
- removal instructions;
- link to one five-minute demonstration.

Sources: releases · tags

P1 — Make installation reversible

The current quick start asks users to clone and symlink the executable. That is workable for developers, but the release needs explicit answers to:

- What dependencies are required?
- Which shells and operating systems are supported?
- Which files does aether init create?
- What happens to existing .context.md?
- How do I uninstall it?
- How do I remove Mechanicall from one project?
- How do I disable all hooks?
- How do I inspect a hook before trusting it?

No installer magic is required. A documented clone-and-link route is enough if removal is equally clear.

P1 — Expose the enforcement boundary

Add a section called:

What preflight can and cannot enforce

State plainly:

- preflight deterministically evaluates CURRENT.md;
- compatible agents and workflows must call preflight;
- Mechanicall does not sandbox arbitrary shell access;
- approve is not identity-authenticated in the alpha;
- project files remain writable by any process with filesystem access.

This honesty will strengthen the project rather than weaken it.

P1 — Add one integration recipe

Do not support thirty agents.

Choose one:

- Grok Build,
- Claude Code,
- or a generic AGENTS.md contract.

The recipe should require:

1. read CURRENT.md;
2. call aether preflight ;
3. stop on nonzero exit;
4. register the artifact;
5. never invoke approve;
6. wait for explicit review.

Then demonstrate refusal.

6. The release demo

The demo should be under five minutes and use a disposable project.

Scene 1 — Authority

aether init
aether current init

Show:

Next: write-tests

Prohibited
- deploy-production
- add-postgres

Scene 2 — Refusal

aether preflight deploy-production

Expected:

REFUSED

Scene 3 — Allowed action

aether preflight write-tests

Expected:

ALLOWED

Scene 4 — Evidence

Create one test artifact and register it:

aether artifact artifacts/test-report.txt \
  --action write-tests \
  --status produced

Scene 5 — Human decision

Show the review, then run approve manually.

Scene 6 — Inspectability

cat CURRENT.md
cat .aether/events.jsonl
git diff

The product should be understood without mentioning:

- LoRA;
- Club-cortex;
- ChromaDB;
- Kingston;
- the van;
- personal journals;
- multi-user inference;
- biological metaphors.

Those are adjacent experiments. They are not required to understand the first value proposition.

7. Club-cortex verdict

The vision contains a real future service

The useful idea is not “host people’s personalities.”

It is:

Help a small number of people establish private, human-controlled AI workflows in which personal material remains theirs, model output cannot silently become authority, and exit remains possible.

That could eventually become:

- workflow setup;
- private corpus/data classification;
- model adapter experiments;
- local or hosted inference;
- regular policy and archive maintenance;
- export and deletion support.

But the current offer sheet jumps from:

one operator + one local adapter

to:

£300–£1,200/month inference club

without a delivered service record between them.

Why the current retainer is premature

A paying member would reasonably ask:

- What exact interface do I receive?
- What uptime should I expect?
- What is the latency and queue policy?
- What happens when your machine or internet goes down?
- Where is my corpus stored?
- How is one member isolated from another?
- How are backups encrypted?
- Who can access adapters?
- How is deletion verified?
- How are support incidents handled?
- What does a train run produce?
- How is model quality evaluated?
- What do I receive at the end of the month?
- What legal basis governs sensitive journal processing?
- What happens if you travel or your hardware fails?

The research acknowledges most of these gaps. Therefore the honest status remains:

Club-cortex: design partner programme, not membership service

Better first paid offer

Do not sell backend membership first.

Sell a bounded implementation:

Personal AI Workflow Alignment Session

Outcome: one existing AI-assisted project becomes inspectable and human-controlled.

Includes:

- workflow interview;
- Mechanicall installation;
- one real CURRENT.md;
- preflight integration with one agent;
- approval/refusal demonstration;
- one reflection template;
- one handoff document;
- one follow-up session.

Pilot price hypothesis: £75–£150 for an individual, or £150–£300 for a technical freelancer/small business.

This is not passive income. It is product discovery that can produce:

- installation evidence;
- objections;
- user language;
- bug reports;
- a testimonial;
- a second non-you case study;
- knowledge of what users will actually pay you to maintain.

Only after two or three setups should you ask whether recurring backend support exists.

8. Your first users

**Operator revision (2026-07-27 alpha cohort):**

- **1 technical** self-serve tester
- **Up to 3 non-technical** users with **operator support** (local clients)

Do not target generic remote SMBs yet. Day-to-day human surface is **`aether panel`**
(Project Panel TUI — buttons for preflight/approve). Agents still use the CLI contract.

Best alpha users:

- developers using two or more coding agents;
- technical artists moving between editing, scripts and AI tools;
- researchers with multi-day AI sessions;
- solo builders who repeatedly lose the latest binding decision;
- people already using Markdown, Git and terminal tools;
- local clients who will accept a short supported walkthrough of the Panel.

Poor first users:

- businesses merely wanting “AI automation”;
- people expecting a multi-tenant hosted chat SaaS;
- anyone requiring a service-level agreement;
- sensitive-data users expecting production security assurances.

Your first user needs to recognize this pain immediately:

“My agent has plenty of context, but it cannot tell which instruction is still binding.”

That sentence is your market filter.

9. The first distribution page

Use this copy:

Mechanicall OS

A plain-file authority layer for AI-assisted projects.

AI agents can remember a lot and still follow the wrong instruction.

Mechanicall gives each project one inspectable authority file:

- the current objective;
- the next allowed action;
- prohibited actions;
- approval status;
- evidence of what happened.

aether preflight evaluates the action before work begins. Decisions and artifacts remain ordinary Markdown and JSONL that can be inspected with cat, grep, and git diff.

Mechanicall does not replace your coding agent, project manager or specification framework. It sits underneath them as a small authority and refusal protocol.

Alpha limitations

- Unix-like shell environment
- no sandbox
- no authenticated human identity
- agents must be configured to call preflight
- no hosted service
- optional local models propose only
- sensitive model weights and personal data are not included

Looking for

Three technical alpha users with one active AI-assisted project and one repeated context/authority failure.

10. Seven-day release sequence

Day 1 — Truth

- Add license.
- Correct “block execution” to “provide deterministic preflight/refusal.”
- Add the enforcement-boundary section.
- Ensure the linked branch contains every claim you intend to publish.

Day 2 — Verification

- Clean-clone test.
- Add GitHub Actions.
- Verify tests/run.sh.
- Test installation and removal in a disposable repository.

Day 3 — Demonstration

- Record the five-minute demo.
- Add one screenshot or terminal capture to the README.
- Write ALPHA-LIMITATIONS.md.

Day 4 — Release

- Merge.
- Tag v0.2.0-alpha.1.
- Create GitHub release notes.
- Add repo description and topics.

Suggested description:

Filesystem-native authority and preflight gates for human–AI projects.

Suggested topics:

ai-agents
human-in-the-loop
cli
local-first
agent-governance
project-management
shell

Day 5 — First invitations

Invite three people individually.

Message:

I’ve built a tiny local-first control layer for AI-assisted projects. It gives the project one readable authority file and lets an agent deterministically refuse actions outside the current human-approved boundary. I’m looking for three technical alpha users with a real context-drift problem—not people to praise it. Would you be willing to try it on one project and tell me where it breaks?

Days 6–7 — Observe

For each tester, record:

- time to install;
- time to first refusal (Panel `d` demo or agent preflight);
- whether they used **`aether panel`** again unprompted;
- whether the agent actually respected preflight;
- where terminology confused them;
- whether CURRENT.md reduced reconstruction;
- whether the event log / PANEL.md helped;
- what they expected the system to enforce but it did not;
- supported non-technical: which step needed the operator.

Do not build Club-cortex during this week.

11. Distribution success criteria

The alpha earns another development cycle if:

- three people clone it;
- two initialize a real project;
- one agent correctly refuses a prohibited action;
- one user returns after an interruption and recovers state faster;
- one limitation is discovered by someone other than you;
- one user asks to keep using it;
- one person is willing to pay for setup, integration or support.

Stars are not the main signal.

A real refusal is.

A second session is.

A paid setup is.

12. Proposal silence and the product

Two weeks of proposal silence is evidence about the proposal channel, targeting, proof or offer—not proof that you should abandon creative services, and not proof that Club-cortex has demand.

Do not let the system become an emotionally safer market merely because nobody has rejected it yet.

Software can provide a more controllable form of hope than client outreach:

- you push and something changes;
- tests pass;
- files accumulate;
- the system answers;
- no stranger has to choose you.

That does not invalidate the product. It means distribution must become the next test.

Engineering progress is now complete enough that more engineering without external adoption would become another form of waiting.

Your adapter may lower proposal stress by producing drafts and checking boundaries. Good. Let it reduce the activation energy—but keep these rules:

- it does not invent client facts;
- it does not send;
- it does not negotiate unsupervised;
- it does not treat silence as rejection;
- it cannot replace the daily outbound unit;
- every generated proposal is still your claim.

The model absorbs drafting friction. It does not absorb commercial reality.

Final decision

KEEP

- Mechanicall OS name
- filesystem truth
- CURRENT.md
- deterministic preflight
- explicit refusal
- events and artifacts
- propose-only model layer
- anti-hallucination denial file
- broader-than-code applicability

REWRITE

- “blocks unapproved execution” → “provides deterministic preflight and refusal”
- “open-core” → add a license first
- personal model as sales engine → personal model as optional bounded proposer
- Club-cortex retainer → design-partner research

PARK

- multi-user backend
- paid inference seats
- train queues
- hosted personal journals
- cloud overflow
- adapter membership
- £400–£1,200 monthly promises
- remote desktop services

SHIP

Mechanicall OS v0.2 alpha: one readable authority file, one permitted next action, deterministic refusal, and an inspectable record of what happened.

You have reached the point where the next proof cannot come from your own archive.

Merge it. License it. Tag it. Show the refusal. Invite three people.

Distribute the protocol before selling the club.