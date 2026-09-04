title: Peer response — mechanicall-os documentation review
author: GPT-5.6 Sol
captured: 2026-08-04
authority_status: PROPOSAL — not CURRENT
review_scope: public mechanicall-os master + live anphuni.com Session/privacy surfaces
may_advance_next: no
technique_default: propose-only
Peer response — Mechanicall documentation

Executive verdict

CONDITIONAL for the docs set as a shippable alpha narrative.

The core story remains strong and mostly consistent:

Mechanicall is a local-first filesystem authority protocol: CURRENT.md declares the one live decision, agents propose and cooperatively preflight actions, and only a human actualises authority.

The main problem is no longer the core protocol. It is product-boundary drift between:

1. the local Mechanicall v0.2 release;
2. the Panel/agent seats;
3. the live, capped website Session;
4. personal-model research;
5. future Club-cortex/backend concepts.

The public repository still says hosted service, multi-user collaboration, web dashboard, and multi-tenant chat are not implemented, while anphuni.com/session now provides up to five server-hosted seats with passphrases, cookies, isolated workspaces, an OpenRouter-proxied coding agent, and persistent server-side files. A five-seat cap limits scale; it does not make the surface non-multi-user.

This is fixable through explicit boundary documentation rather than architectural retreat.

Highest-priority findings

1. PRODUCT.md, AUTHORITY.md, START-HERE.md, docs/SINGLE-APP-DISTRIBUTION.md, and docs/PERSONAL-LLM-DEFINITION.md are not present on public master. I cannot verify their host-only versions. This creates a mirror/public-truth gap.
2. The live privacy page contradicts itself: it first says the website has no login, passwords, tokens, or user database, then documents Session passphrases, cookies, and server workspaces.
3. “Max five” is capacity framing, not a tenancy distinction. Session is a small hosted multi-user alpha even if it is not open SaaS.
4. Root CURRENT.md has unclear lifecycle state: Phase: APPROVE, Status: APPROVED, Approval: APPROVED, yet still authorizes ci-control-layer-gates and describes a later approval condition.
5. AGENTS.md does not prominently require reading CURRENT.md and running preflight before consequential work.
6. ARCHITECTURE.md and CORE_PRINCIPLES.md contain stale language: Python-only userland versus the real POSIX shell/JS interfaces; no TUI versus the implemented Panel.
7. PANEL-GROK-SPLIT.md calls chat/shell surfaces “Domain” more strongly than the cooperative enforcement boundary supports.
8. The published alpha release body still calls itself “draft” and includes a “Do not publish until” instruction despite already being published.

Reviewed public baseline: master at 375d90d, plus the live Session and privacy page.  
Core sources: README · SPEC-v0.2 · NOT-IMPLEMENTED

A. Consistency

1. Do PRODUCT / AUTHORITY / SPEC-v0.2 / NOT-IMPLEMENTED tell one story?

Verdict: cannot fully verify; public files are incomplete

PRODUCT.md and AUTHORITY.md are absent from public master, so the requested four-document consistency check cannot be completed from the public repository.

The two available P0 documents do tell a coherent core story:

- SPEC-v0.2.md defines CURRENT.md as present authority;
- one Next is permitted;
- preflight is deterministic when called;
- models propose;
- humans approve;
- history, context and seeds cannot override CURRENT.

NOT-IMPLEMENTED.md correctly limits this:

- no sandbox;
- no authenticated human approval;
- no forced preflight for external agents;
- no sovereign operator TUI;
- no general multi-user platform;
- no hosted Club-cortex backend.

Drift

NOT-IMPLEMENTED.md is now more architecturally honest than several positive-facing documents. That means readers must study the denial list to understand what the product actually is.

PRODUCT.md should carry the same boundary positively:

Mechanicall core = local filesystem protocol
Panel/shell = optional cooperative interfaces
Session = separate capped hosted alpha
Club-cortex = research only

Recommendation

Push or recreate canonical public versions of PRODUCT.md and AUTHORITY.md. Do not let the only up-to-date product boundary live on Kingston.

2. Where do website Session seats strain “no multi-tenant” language? Is max-five enough?

Verdict: max-five is not enough

Session currently has:

- up to five users/seats;
- display name and passphrase;
- server-side salted passphrase hash;
- session cookie;
- separate server-side workspace per seat;
- shared hosted application and model proxy;
- server-side agent execution.

That is a small multi-user hosted system. It may be private, capped, invite-like, non-commercial, and operationally simple, but the cap does not change the tenancy mechanics.

The safe distinction is:

Mechanicall v0.2 core is not a multi-user platform. Anphuni Session is a separate capped hosted alpha using Mechanicall’s CURRENT format and human-approval doctrine.

Avoid:

There is no multi-tenant service because there are only five seats.

The current NOT-IMPLEMENTED.md says both “multi-user collaboration platform” and “multi-tenant SaaS chat” are not implemented. That remains defensible only if explicitly scoped to Mechanicall core, not the whole product ecosystem.

Recommendation

Use three labels consistently:

| Surface | Honest label |
|---|---|
| Mechanicall repository | Local-first authority protocol |
| anphuni.com/session | Capped hosted alpha, maximum five isolated seats |
| Club-cortex | Research direction, not shipped |

Do not use “not multi-tenant” for Session. Use “not open-registration or general-purpose SaaS.”

3. Any doc still implying CLI-first casual product after SINGLE-APP-DISTRIBUTION?

Verdict: yes, public narrative is split

docs/SINGLE-APP-DISTRIBUTION.md is absent from public master, so its current host version cannot be inspected.

Public docs still present three competing entry points:

1. README quick start: terminal installation and CLI commands;
2. README: aether panel as daily TUI;
3. live website: Session as a browser-based private seat.

The README remains appropriate for a technical open-source repository, but it does not explain which surface a casual user is expected to use.

ARCHITECTURE.md also says:

No product GUI / web dashboard for v0.2

while Panel is implemented and Session exists adjacent to the core.

Recommendation

State the distribution split plainly:

Self-hosted technical path: aether CLI + optional Panel.
Supported casual path: operator-provisioned Session seat.
Future packaged desktop path: research/not shipped.

A single-app direction document must not imply that Tauri, Session, Panel and CLI are already one product.

B. Honesty / overclaim

4. Claims that outrun implementation

P0 — “Domain chat” and “Domain shell”

PANEL-GROK-SPLIT.md calls the left pane “Domain chat” and the full shell a “Domain shell.” But NOT-IMPLEMENTED.md correctly says the operator TUI is not sovereign and external agents may skip preflight.

Unless every consequential tool action is routed through mandatory preflight, these are Domain-aware/cooperative surfaces, not enforced Domain surfaces.

Suggested wording:

CURRENT-visible cooperative agent shell

rather than:

Domain shell

P0 — Session versus denial list

The denial list says multi-user collaboration and multi-tenant chat are not implemented. The live Session has multiple isolated seats and hosted chat.

Resolve by scoping the denial to Mechanicall core and documenting Session separately.

P0 — “Project folder on your device”

The privacy page describes Session as operating after the user grants a project folder “on your device.” The same page later says seat files live in a host data directory.

Those are materially different architectures.

Current Session appears to use a server-hosted workspace, not a browser-granted local folder. Remove the local-folder wording unless the browser actually uses a File System Access API and local files remain local.

P1 — “Jailed per seat”

“Jailed” can imply a security-grade sandbox. The handoff describes path-restricted tools and allowlisted Bash; that is not automatically equivalent to OS/container isolation.

Use:

Tool paths are restricted to the seat workspace and Bash commands are allowlisted.

Only use “sandbox” or “jail” if containment has been threat-modelled and tested against:

- symlinks;
- .. traversal;
- absolute paths;
- subprocess working-directory escape;
- shell expansions;
- environment leakage;
- /proc;
- inherited file descriptors;
- network access;
- race conditions.

P1 — Filesystem truth across Session

For Session, the filesystem is still server-side truth, but it is no longer necessarily a filesystem the user directly owns or can inspect with local cat and git diff.

Say:

Session stores each seat’s authority in ordinary files inside its isolated server workspace.

Do not imply the user possesses the same local sovereignty as the self-hosted CLI path unless export/download is implemented.

P1 — Published release marked draft

The public v0.2.0-alpha.1 release is published as a normal release, but its body begins:

draft  
Do not publish until...

That directly undermines release confidence.

Either:

- edit the release notes to remove internal gating text and mark it prerelease; or
- publish a corrected alpha.2.

P1 — README prominence of Club-cortex

The README places Club-cortex direction near the top of “What it is not.” Even with research labels, this distracts from the alpha wedge and encourages host-platform interpretations.

Move the Club-cortex links to a lower “Research directions” section.

P2 — “Python-only userland”

CORE_PRINCIPLES.md says Markdown and Python are the only userland. In practice:

- the one-true core executable is POSIX shell;
- the TUI uses Python;
- website Session uses browser/server technologies;
- scripts and CI use shell.

The principle is not intact as written.

Proposed doctrine:

Durable authority and user-owned state remain plain Markdown/JSON. Core automation uses inspectable POSIX shell or Python. Distribution interfaces may use other languages but may not become a second authority store.

5. Privacy page versus passphrases and OpenRouter

Verdict: privacy rewrite required before wider seat use

The opening says:

This website is static marketing. It does not offer registration or login. It does not store passwords, session tokens, or a user database.

The Session section then says:

- users sign in;
- the server stores salted passphrase hashes;
- HttpOnly session cookies exist;
- workspace files persist on the host.

The opening is therefore false for the domain as a whole.

Required wording gaps

The privacy page should disclose:

1. Scope split  
   Static marketing pages versus the Session application.

2. Account-like records  
   Display name, salted passphrase hash, seat identifier, session cookie and creation/last-use timestamps if stored.

3. Operator access  
   Whether the operator can inspect, export or delete seat workspaces.

4. Model data flow  
   Not only chat text: selected file contents, tool results, prompts and code fragments may be placed in model context and sent to OpenRouter.

5. Provider handling  
   Link to OpenRouter’s current privacy/data policy and state whether provider logging/training controls are enabled. Do not promise non-retention unless verified by configuration and provider terms.

6. Persistence  
   Render disk is expected to persist workspaces, but persistence is not the same as backup. State whether backups exist.

7. Retention/deletion  
   Define inactive-seat retention and how a user requests deletion.

8. Cookie behavior  
   Purpose, approximate lifetime and what sign-out invalidates.

9. Security boundary  
   Tool path restrictions are an alpha control, not a production security certification.

10. Sensitive-data warning  
    No credentials, mailbox exports, financial secrets, private client repositories or regulated personal data during alpha.

Recommended opening

Most of anphuni.com is static marketing. /session is a separate capped hosted alpha with up to five seats. Session stores a display name, salted passphrase hash, session cookie and workspace files on the host, and sends relevant chat/tool context to OpenRouter for model inference.

That single paragraph removes the largest contradiction.

C. Operator usability

6. Can a new agent load L0–L1 from AGENTS + CURRENT without drowning?

Verdict: size is manageable; routing is wrong

AGENTS.md and root CURRENT.md are short enough to read together. The problem is precedence.

AGENTS.md presently mandates:

- activating the full ICM meta-agent skill;
- folder-stage orchestration;
- Markdown stage contracts;
- Python behaviors;
- artifact production;
- human review.

But it does not prominently say:

1. read root CURRENT.md;
2. identify its one Next;
3. run preflight before consequential work;
4. stop on refusal;
5. never approve as an agent.

A compliant agent can therefore follow ICM perfectly while performing the wrong live action.

It also routes immediately into a roughly 10 KB skill document. That is reasonable for substantial development but heavy for docs-only review or a trivial patch.

Recommendation

Put this before the ICM instructions:

Live authority — read first

1. Read root CURRENT.md.
2. CURRENT outranks context, stages, sessions and model output.
3. Perform only its declared Next.
4. Run aether preflight  before consequential work.
5. Stop on refusal.
6. Agents never approve, reject or rewrite authority as their own decision.

Then make ICM proportional:

- docs-only review: AGENTS + CURRENT + named inputs;
- consequential implementation: activate full meta-agent/stage workflow;
- trivial correction: direct patch plus short receipt.

7. Missing short read order at repo root?

Verdict: yes

START-HERE.md is not present on public master.

The README is comprehensive but too broad for a reviewer who needs doctrine rather than installation, commands, Rhizome, model configuration and speculative research.

Recommended read order

Create START-HERE.md:

For product truth:
1. PRODUCT.md
2. CURRENT.md
3. SPEC-v0.2.md
4. ALPHA-LIMITATIONS.md
5. NOT-IMPLEMENTED.md

For contributing:
6. AGENTS.md
7. CORE_PRINCIPLES.md
8. ARCHITECTURE.md

For interfaces:
9. PANEL-GROK-SPLIT.md
10. SINGLE-APP-DISTRIBUTION.md

For personal models:
11. PERSONAL-LLM-DEFINITION.md

Add one line:

Host/phone mirrors may be newer, but public product claims are only shippable when the canonical public files agree.

D. Client One / Session narrative

8. Is “research Outlook under CURRENT” clean enough?

Verdict: bounded in the UI, insufficiently durable in documentation

The live Session page correctly presents Outlook as integration research. Privacy also says there is no live mailbox on the host.

That is good, but the boundary currently depends on short UI copy and the handoff. It should have a one-page durable contract because “Outlook integration” can easily be misread as:

- live OAuth;
- mailbox access;
- sending mail;
- stored refresh tokens;
- email indexing;
- automatic action.

Recommendation

Add docs/OUTLOOK-RESEARCH-BOUNDARY.md containing:

- current state: research seed only;
- no Graph OAuth;
- no mailbox credentials;
- no SMTP;
- no email ingestion;
- no token storage;
- no sending;
- model proposes plans only;
- any future implementation requires a separate CURRENT;
- separate privacy review;
- minimal permissions analysis;
- explicit test account;
- human approval before every consequential transition.

Website copy should link to it or summarize it.

9. Single doc change that would most reduce confusion

Recommendation: add/publish PRODUCT.md

The most useful document is not another implementation guide. It is a one-page boundary map:

Mechanicall core
- local filesystem authority protocol
- CURRENT + preflight + evidence
- cooperative, not sandbox-enforced

Self-hosted interfaces
- CLI
- Panel
- shell/chat surfaces
- same CURRENT, no second authority

Anphuni Session
- separate capped hosted alpha
- up to five isolated server workspaces
- OpenRouter-proxied coding agent
- not part of v0.2 core release

Research
- personal adapters
- Club-cortex
- Outlook integration
- Tauri/single-app packaging

Never
- model approval
- silence as permission
- automatic authority advancement

Every other public document should link back to this boundary.

E. Final verdict

10. GO / CONDITIONAL / NO-GO

CONDITIONAL

The local Mechanicall v0.2 narrative is shippable as an alpha:

- inspectable filesystem authority;
- one Next;
- deterministic cooperative preflight;
- explicit human approval;
- honest no-sandbox limitations;
- propose-only model role.

The combined ecosystem narrative is not yet clean enough for wider distribution because:

1. public P0 documents are missing;
2. the privacy page contradicts Session reality;
3. Session’s multi-user nature conflicts with unscoped denial language;
4. Panel/Grok documentation overuses “Domain” for cooperative surfaces;
5. the root CURRENT lifecycle is ambiguous;
6. language/runtime principles are stale;
7. the published release still contains draft instructions.

Exit conditions for GO

- Publish PRODUCT.md and START-HERE.md.
- Scope NOT-IMPLEMENTED.md explicitly to Mechanicall core.
- Rewrite Session privacy opening and data-flow disclosures.
- Normalize root CURRENT phase/status/approval.
- Add CURRENT/preflight precedence to AGENTS.md.
- Correct the release notes.
- Add the Outlook research boundary page.
- Replace enforced-sounding “Domain shell/chat” wording with cooperative language where appropriate.

No new product machinery is required.

Root CURRENT schema review

The public root currently says:

Phase: APPROVE
Status: APPROVED
Next: ci-control-layer-gates
Approval: APPROVED

while the approval condition says the human should approve after CI becomes green.

This mixes two different approvals:

1. approval to execute the CI work;
2. approval of the resulting CI artifact.

Recommended interpretation

If CI work is currently authorized:

Phase: EXECUTE
Status: APPROVED
Next: ci-control-layer-gates
Approval: APPROVED

After the artifact exists:

Phase: REVIEW
Status: READY-FOR-REVIEW
Next: review-ci-control-layer-gates
Approval: PENDING

After human acceptance:

Phase: APPROVE
Status: APPROVED
Next: unset
Approval: APPROVED

Alternatively, move directly to the next human-selected objective. Do not leave an executable Next attached to a completed approval phase.

The schema itself remains useful; this is state hygiene rather than a specification failure.

Proposed doc patches — paths + bullets only

PRODUCT.md

- Add to public repository.
- Define Mechanicall core, self-hosted interfaces, Session, and research as four separate scopes.
- State cooperative—not sandboxed—enforcement.
- State Session is a capped hosted alpha, not part of v0.2 core.
- Remove Club-cortex from primary pitch.

CURRENT.md

- Resolve APPROVE/APPROVED versus still-active CI Next.
- Use separate execute and review action IDs.
- Set Next: unset once an approval phase is complete.
- Keep TWS/trading outside this root.

AUTHORITY.md

- Add to public repository if intended as canonical.
- State it explains authority modes but never overrides CURRENT.
- Separate product, trading and hygiene roots by directory.
- Define precedence: safety constraints → CURRENT → stage context → history.
- Do not duplicate live Next.

SPEC-v0.2.md

- Clarify approval-to-execute versus approval-of-output.
- Clarify direct human edit versus agent proposal.
- State hosted Session is outside the core specification.
- Retain one-Next and cooperative-preflight semantics.

NOT-IMPLEMENTED.md

- Scope all denial claims explicitly to Mechanicall core.
- Add Session as a separate capped hosted alpha that does exist.
- Replace absolute “multi-user not implemented” with precise core/Session distinction.
- Retain no-sandbox and no-sovereign-external-TUI warnings.
- Link PRODUCT.md.

CORE_PRINCIPLES.md

- Replace “Markdown + Python only” with Markdown/JSON authority plus inspectable POSIX shell/Python automation.
- Define browser/TUI code as interface implementation, never authority.
- Keep filesystem truth and deferred structure unchanged.

ARCHITECTURE.md

- Remove “Initial Architecture Sketch” framing or mark historical sections.
- Replace “daemon/agent” description with current shell CLI reality.
- Remove “no TUI” as a current non-goal.
- Add Panel and Session boundary explicitly.
- Keep hosted systems outside the core three-layer contract.

AGENTS.md

- Put CURRENT/preflight contract before ICM activation.
- State agents cannot approve/reject.
- Add docs-only lightweight path.
- Keep full ICM for consequential implementation.
- Avoid mandatory loading of unrelated context.

START-HERE.md

- Add to public repository.
- Provide product-review and contributor read orders.
- State public canonical files versus local mirrors.
- Link Session/privacy as adjacent deployed context.

README.md

- Keep local-first authority pitch.
- Move Club-cortex to a low-prominence research section.
- Link PRODUCT.md and START-HERE.md.
- Explain CLI/Panel versus hosted Session.
- Avoid calling optional interfaces sovereign.

docs/SINGLE-APP-DISTRIBUTION.md

- Add to public repository if canonical.
- Distinguish current Panel, current Session, and future Tauri packaging.
- Do not imply one packaged app already exists.
- State every interface projects the same authority contract.

docs/PANEL-GROK-SPLIT.md

- Replace “Domain chat/shell” with “CURRENT-visible cooperative chat/shell” where tools can bypass preflight.
- Add warning that Fullscreen Grok exits Mechanicall enforcement.
- State approve button is protocol-level human action, not authenticated identity.
- Keep CURRENT right rail as the strongest implemented affordance.

docs/ALPHA-LIMITATIONS.md

- Scope “no hosted service” to the open-source core.
- Add link to separate Session limitations/privacy.
- Reconcile three-user local cohort with five-seat hosted alpha.
- Keep no-sandbox warning prominent.

docs/DISTRIBUTE-MECHANICALL-ALPHA.md

- Mark historical claims as superseded where license, CI and release now exist.
- Remove obsolete branch/release blockers.
- Keep product proof criteria.
- Add Session as separate experimental distribution evidence.

docs/PERSONAL-LLM-DEFINITION.md

- Add to public repository or consolidate into PERSONAL-LLM-LAYER.md.
- Preserve technique-under-Domain doctrine.
- State hosted Session currently uses an external model, not the user’s personal adapter by default.
- Keep facts-from-files and no-tools boundaries.

docs/OUTLOOK-RESEARCH-BOUNDARY.md

- Add one-page research fence.
- No OAuth, mailbox, SMTP, tokens, ingestion or sending.
- Require separate CURRENT and privacy review before implementation.
- Link from Session copy.

anphuni.com/privacy

- Replace static-only opening.
- Disclose Session login/passphrase/cookie/workspace state.
- Correct “project folder on your device.”
- Disclose file/tool context sent through OpenRouter.
- State retention, deletion, operator access and backup policy.
- Replace “jailed” with precise path/tool restrictions unless sandbox-tested.

anphuni.com/session

- Keep max-five and no-live-mailbox wording.
- Label Session “capped hosted alpha.”
- Link Outlook research boundary.
- State seat files live on the server.
- Add warning against sensitive credentials and private production data.

GitHub release v0.2.0-alpha.1

- Remove “draft” and “Do not publish until.”
- Mark release as prerelease or issue corrected alpha.
- Link current limitations and PRODUCT boundary.

Final peer statement

The protocol has not lost its centre. The docs have accumulated multiple valid surfaces without one canonical boundary map.

The correction is documentary:

Mechanicall core is the local authority protocol. Panel and shell are cooperative projections. Session is a separate capped hosted alpha. Personal models are technique. Research is not product. Human Yes remains the only actualisation.

No authority advanced by this review.