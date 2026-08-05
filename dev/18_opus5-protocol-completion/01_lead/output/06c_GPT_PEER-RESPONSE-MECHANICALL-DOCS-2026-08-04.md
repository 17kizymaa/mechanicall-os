Direct verdict

You have shipped a real technical protocol alpha. You have not finished a casual-user software product yet.

The number of commits—36 or otherwise—is not the test. The repository now has a coherent, licensed, CI-green authority protocol on master, but its own documentation still labels casual single-app distribution as incomplete. The website successfully demonstrates the idea, while the downloadable product remains primarily for technical users. Repository · latest master CI · website

So:

- Yes: distribute it as a free technical alpha.
- Yes: offer Ste a supported experiment.
- No: say the complete casual product is finished.
- No: promise that one document automatically syncs the whole conversation.
- No: describe the hosted Session account as fully device-first or unqualified “private.”

1. What you have actually made

Mechanicall’s product nucleus is now:

A local authority protocol that turns the latest human decision into one inspectable project state: the current objective, one permitted next action, prohibited actions, evidence, and an explicit human decision boundary.

The shipped core includes:

- CURRENT.md;
- schema validation;
- deterministic preflight when called;
- allow/refuse events;
- approve/reject;
- artifact registration;
- aether next;
- demo, brief, drift and probe commands;
- local Panel/shell interfaces;
- installation and removal scripts;
- Apache-2.0 licensing;
- green integration and control-layer CI.

That is shippable as:

Mechanicall OS protocol alpha for technical users and supported design partners.

It is not yet shippable as:

A casual application that anybody can install and understand within 30 seconds.

Your own START-HERE.md says casual packaging is incomplete, and the README points to a missing docs/SINGLE-APP-DISTRIBUTION.md. START-HERE · README

2. The website is teaching the idea well

The website is currently stronger as a protocol literacy surface than as a product download page.

It correctly demonstrates:

see the plan
     ↓
try the wrong action
     ↓
observe refusal
     ↓
try the permitted action
     ↓
human decides

The static demo is particularly honest:

- it says it is a simulation;
- it says real authority lives on the user’s machine;
- it states that cooperative preflight is not a sandbox;
- it separates model proposals from human approval.

That is good distribution work. Protocol page · demo

The comparison page also gives visitors an immediate conceptual contrast between normal chat and plan-bound chat. Compare demo

But it proves comprehension, not adoption

A visitor can understand the idea quickly. That does not prove they can:

- install Mechanicall;
- create a useful CURRENT;
- connect it to their preferred AI;
- preserve the right information;
- return tomorrow and recover the project;
- know when to update or approve;
- use the protocol without your guidance.

The website currently proves:

“A casual user can understand the core distinction.”

It does not yet prove:

“A casual user can independently operate a real Mechanicall project.”

That second claim requires observation.

3. The 36 commits question

Commits are not the shipping unit

A product with three commits can ship. A product with 3,000 commits can remain unusable.

Your release test should be:

1. Can a fresh user obtain one exact version?
2. Can they start without knowing your repository history?
3. Can they understand what CURRENT means?
4. Can they create one project?
5. Can they observe one refusal?
6. Can they return later and recover state?
7. Can they uninstall or export everything?

The core passes some of these. The casual product has not yet passed all of them.

Release packaging is currently inconsistent

The public release is v0.2.0-alpha.1, but its tag points to the July 27 commit b7dc96d, not the August 4 master containing PR #3 and the newer protocol commands. The release page was edited later, but editing release notes does not move the Git tag. Release · latest merge

Therefore someone downloading v0.2.0-alpha.1 does not necessarily receive the product currently described on master.

Recommendation

After fixing the truth/documentation issues, cut:

v0.2.0-alpha.2

or:

v0.3.0-alpha.1

Do not retarget the old tag. Preserve release history.

Mark it as a GitHub prerelease, and include:

- exact supported systems;
- install;
- first project;
- five-minute demo;
- uninstall;
- limitations;
- checksum or immutable commit;
- what is core versus hosted Session.

4. Your root CURRENT currently fails its own clarity test

The current master authority says:

Next: commit-hygiene

But later says:

Action id: implement-remaining-waves

The approval condition also refers to implement-remaining-waves.

That means the human-readable authority contains two competing action IDs. Current master authority

This is precisely the kind of drift Mechanicall is meant to prevent.

Before the next release, make these identical:

Next: package-protocol-alpha-2

Next allowed action
Action id: package-protocol-alpha-2

Also do not leave:

Phase: APPROVE
Status: APPROVED
Next: an already completed action

An approved completed action should transition to the next SELECT state.

5. Park the UEFI/GOP direction

The UEFI CURRENT you pasted is internally disciplined, but it does not solve your immediate product problem.

A GOP framebuffer application could prove:

- extremely low-overhead rendering;
- boot-time display;
- static presentation of CURRENT;
- QEMU/OVMF experimentation.

It cannot yet provide:

- the local AI workflow;
- project file ownership;
- agent integration;
- conversation-to-plan handling;
- website distribution;
- ordinary casual installation;
- useful recovery across real projects.

Your own CURRENT correctly says not to port Aether into firmware. But that leaves the UEFI application as a static status-display experiment, not a Mechanicall distribution.

Recommendation: park EFI/GOP.

Label it:

research/seat-rendering/ — not current product packaging

The casual packaging problem is not graphics overhead. It is:

- installation;
- project creation;
- plain-language terminology;
- proposal review;
- state recovery;
- user trust.

A basic local webview or terminal application can test those much faster than firmware.

6. Review of your message to Ste

The warmth and concrete workflow idea are good. Several claims need tightening.

“I have just finished launching my software product”

Too strong.

Use:

I’ve launched the first public technical alpha of a project-control tool I’m building.

“It’s completely free”

Potentially true for the protocol, but distinguish the free open-source core from your limited hosted experiment.

Use:

The open-source alpha and website demo are free.

Do not imply indefinite free hosted model inference unless you intend to fund it.

“One single text document syncs the whole conversation”

This is not technically accurate.

CURRENT does not synchronize or summarize the entire conversation automatically. It records the latest binding project state. Conversations, event logs, artifacts and files remain separate.

Better:

It keeps the latest agreed objective and next step in one readable project file, so you don’t have to reconstruct the project from old chats.

That is a stronger and more defensible benefit.

“Start building something privately”

Qualify this.

Your hosted Session stores workspace files on your server and sends relevant chat/tool context to OpenRouter. It may be isolated, but it is not purely device-local. Your privacy page explains this correctly. Privacy policy

Use:

I can offer you one of the limited hosted alpha workspaces. It is isolated from other seats, but model requests are processed through OpenRouter; I’ll show you the privacy limits before you use it.

For sensitive CIC/client material, start with:

- public information;
- synthetic examples;
- explicitly approved photos;
- no account credentials;
- no private participant information;
- no safeguarding or health information.

7. Suggested corrected follow-up to Ste

Hello Ste,  
  
Small correction to my earlier message: I’ve launched the first public technical alpha of Mechanicall, rather than a fully finished consumer app. The website demo and open-source protocol are free.  
  
Mechanicall helps turn an AI conversation into a project you can return to. Instead of relying on old chat history, it keeps the latest agreed objective, one next step, and anything currently prohibited in a readable project file. The AI can propose work, but the project does not advance just because the chat sounded confident.  
  
I can also offer you a supported hosted-alpha workspace if you would like to test it. The workspace is isolated, but model requests are processed through an external model provider, so we should begin with public or non-sensitive material.  
  
A possible test project for Rhythym Reactions CIC would be a public social-media profile review, followed by a proposed photo-template workflow. We could keep the first outcome very small: one readable report, one agreed next action, and no automatic posting.  
  
The demo is at www.anphuni.com. No pressure—I’m specifically looking to learn where the process is confusing or unhelpful.  
  
Anthony K.

This version invites real testing without pretending the product has already passed it.

8. Can it beat normal chatrooms for ease?

For initial conversation: probably not yet

Normal chatrooms win on immediate ease:

open page
type
receive answer

Mechanicall adds structure and therefore adds some friction.

Your advantage cannot be:

easier than ChatGPT in the first 30 seconds.

Your advantage should be:

easier to resume, govern and trust after the first 30 minutes—or the next day.

That is the actual wedge.

The comparison to test

Do not ask:

Was Mechanicall easy?

Ask the same person to perform the same multi-session project in two conditions:

Normal chat

- create a social media report;
- stop for one day;
- return;
- identify the latest agreed objective;
- identify what was rejected;
- continue correctly.

Mechanicall

- same task;
- same interruption;
- CURRENT remains visible;
- return and resume.

Measure:

- time to recover;
- number of contradictory assumptions;
- whether the user remembers the agreed Next;
- whether the AI attempts an excluded action;
- whether the user understands who approved what;
- whether the user voluntarily returns.

Mechanicall wins if it makes the second session easier, not necessarily the first message.

9. What outcome are you trying to achieve?

Not deterministic conversation.

LLM responses remain probabilistic. Users also change their minds. “Real discussions” should not be flattened into deterministic dialogue.

The deterministic part is the decision boundary around the discussion.

Canonical product outcome

Mechanicall turns open-ended AI discussion into durable, inspectable project state, so a person can stop, return, and know exactly what has been agreed, what may happen next, and what still requires their decision.

Or shorter:

Have real conversations with AI without losing control of what became the plan.

The protocol should deterministically answer:

1. What project are we doing?
2. What is authoritative now?
3. What is the one permitted next action?
4. What must not happen?
5. What evidence was produced?
6. Has the human accepted the result?

The AI does not need deterministic prose. It needs a deterministic relationship to authority.

Discussion may branch.
Proposals may vary.
The binding Next must not be ambiguous.
Consequential progression must require a human decision.

That is the product.

10. Recommended application outcome for Ste

Do not begin with “build a photo production pipeline.” That is too large.

Use a first Domain like:

CURRENT

Objective: Produce a factual review of the public Rhythym Reactions social-media profile.
,Phase: EXECUTE
Status: ACTIVE
Next: collect-public-profile-observations
Approval: PENDING

Keep
- public information only
- separate observations from recommendations
- preserve links to source material
- no changes to live accounts

Next allowed action
Collect a small set of public profile observations and draft a report for review.

Approval condition
Ste reviews the observations and decides whether to proceed to template recommendations.

Prohibited
- publish-content
- access-private-accounts
- use-participant-personal-data
- invent-engagement-statistics
- contact-followers
- create-final-brand-strategy

Success is not “the AI produced an impressive report.”

Success is:

- Ste understands the Objective;
- Ste understands the single Next;
- nothing gets posted;
- observations remain distinguishable from recommendations;
- Ste returns later and knows exactly where the project stands.

11. Your next authority

I would replace the EFI direction with:

CURRENT

Objective: Package and test Mechanicall as an honest protocol alpha that one supported non-technical user can understand, begin, and resume.

Phase: SELECT
Status: ACTIVE
Next: package-alpha-2
Approval: PENDING

Keep
- CURRENT as the product
- one readable Objective and Next
- deterministic preflight when called
- explicit human decisions
- local ownership for the self-hosted core
- hosted Session labelled separately
- reversible installation

Reject
- firmware work
- new agent features
- finished-consumer-product claims
- automatic conversation-to-authority claims
- unqualified private-hosting claims
- multi-seat expansion

Limits
- one supported Client-one project
- public or synthetic test data
- Linux technical package first
- no new interface before observed use
- website must distinguish demo, download, and hosted lab

Next allowed action
Cut an immutable alpha release from green master after fixing CURRENT consistency, broken documentation links, release notes, and the supported first-project walkthrough.

Approval condition
A clean machine installs the release, runs the demo, initializes one project, observes one refusal, and removes it successfully.

Prohibited
- scaffold-uefi-gop-console
- build-new-dashboard
- add-hosted-registration-scale
- claim-conversation-auto-sync
- claim-fully-private-session
- automatic-approve

Final answer

You have made something real. The protocol is shippable as an alpha.

What you have not yet proved is that a casual person can independently convert a conversation into a sustainable project with less confusion than normal chat. Your website teaches the distinction well, but the downloadable release, hosted Session and casual product are currently three different surfaces.

Do not solve that with more low-level code.

Fix the release/version truth, fix CURRENT’s competing Next values, remove the broken packaging reference, qualify the message to Ste, and observe one real project across two sessions.

Your outcome is not deterministic discussion.

Your outcome is durable discussion with deterministic authority.