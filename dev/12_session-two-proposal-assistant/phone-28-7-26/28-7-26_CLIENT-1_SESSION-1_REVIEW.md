Sprint verdict

Architectural direction: GO. Merge readiness: NO-GO yet.

You are reading the architecture correctly:

- CURRENT.md is the product surface, not hidden prompt plumbing.
- Desk is a bounded proposal interface, not an agent runtime.
- The browser/TV is a thin client; keys and inference stay on myarch.
- Removing Kodi/remote action routes from Desk was the right correction.
- The LG/eME640/Fire Stick role split is sound.

And yes: you have now added real product code, not merely doctrine. The latest branch implements an HTTP surface, CURRENT rail, per-turn authority injection, local browser history, threaded requests, device scripts, tests, and UAT evidence.

But the branch should not merge in its current form. There are four concrete blockers: red CI, misleading history claims, an unsafe request-controlled root, and branch scope contamination.

The branch is currently 21 commits ahead of master with 91 changed files, and the latest CI run failed. Compare · branch · failed Actions run

1. Is CURRENT.md-as-product working?

Plain claim

Yes—as an authority-aware proposal surface. Not yet as proof of deterministic refusal.

What the implementation gets right

The implementation now makes CURRENT visible and operational:

1. /current returns the live file.
2. The rail refreshes on load, focus, input and immediately before Send.
3. desk_turn() independently re-reads CURRENT while constructing the model request.
4. CURRENT is injected as a human-owned project note.
5. The model has no Desk action routes or playback tools.
6. Model output does not write CURRENT.

That is a strong embodiment of:

authority remains visible while conversation remains disposable.

The server-side re-read matters more than the visual polling: the model receives the current filesystem version for each turn rather than trusting the browser’s cached rail. Desk core · Desk API/UI

The important qualification

Desk does not call aether preflight before chat—and that is acceptable because chat is proposal-only and has no consequential tools.

Therefore this sprint demonstrates:

CURRENT → visible context → bounded model proposal

It does not yet demonstrate:

CURRENT → deterministic refusal → prevented consequential integration action

Respect for CURRENT’s semantic contents remains probabilistic. Absence of tools is the mechanical boundary.

Risk if described incorrectly

If you call this “CURRENT enforcing chat,” you blur two different guarantees:

- Mechanical: the server re-reads CURRENT; Desk exposes no playback routes.
- Probabilistic: the model follows the instructions found in CURRENT.

Recommendation

Describe Desk as:

A propose-only surface that re-reads and displays the project’s live human authority on every conversational turn.

Do not describe this particular UI as the refusal gate. The refusal gate remains aether preflight when a consequential adapter is introduced.

2. Critical finding: history is not only stored in the browser

Plain claim

The current privacy copy and audit overstate client-local history.

Current behavior

The browser persists history in localStorage, but:

1. Recent history is sent to /chat with every message.
2. That history is passed onward as model context.
3. desk_turn(..., log=True) writes user and assistant messages to:

.aether/chat.jsonl

The unit tests explicitly verify that two server-side chat records are written. Desk test

So this statement is not presently complete:

“Chat history in browser localStorage on the client.”

Persistence happens in both browser storage and the project’s .aether directory. Recent history also leaves the client during a turn.

Risk

A family member may reasonably interpret “your chat stays on this device” as meaning the operator computer and model provider do not receive previous messages. That is not the implemented behavior.

It also creates a truth contradiction inside a product whose central claim is inspectability.

Concrete recommendation

Choose one of these policies before merge:

Preferred alpha policy

- Browser localStorage holds transcript persistence.
- Server does not persist message bodies by default.
- Event log records only metadata such as timestamp, request outcome and backend.
- Optional transcript logging requires an explicit operator flag.

Then use exact copy:

Your transcript is persisted in this browser. When you send a message, recent conversation is transmitted to the house computer and model provider as context. Desk does not save message bodies on the house computer unless transcript logging is explicitly enabled.

If you retain .aether/chat.jsonl, say so plainly in the popup and README.

3. Critical finding: the client can select an arbitrary server root

Plain claim

POST /chat must not accept a client-supplied root.

Current behavior

The handler contains the equivalent of:

if body contains root:
    use that path as the project root

That means a LAN client can direct Desk toward another accessible directory rather than the domain selected when desk-serve started.

Because CURRENT and selected local context files are injected into the model prompt, this creates an unnecessary local-file disclosure path. It also breaks the product statement that the operator launched Desk against one authority scope.

Risk

The browser becomes able to switch Domain without an operator filesystem action. A LAN peer could potentially choose another directory containing a CURRENT.md or expected context files and ask the model to reproduce them.

This is more serious because:

- --lan binds to every interface;
- responses use Access-Control-Allow-Origin: *;
- there is no pairing token;
- request sizes are not capped;
- /health exposes the host’s absolute root path.

Concrete recommendation

Before merge:

1. Remove request-controlled root.
2. Always use STATE.root, fixed at server startup.
3. Remove wildcard CORS; the UI and API are same-origin.
4. Stop returning the absolute filesystem root from /health.
5. Add a modest request-body limit.
6. Document --lan as trusted-house-LAN alpha behavior, not authentication.

A pairing token can come later if external users actually need LAN exposure. Do not build an account system.

4. Does poll-on-input correctly separate authority from history?

Plain claim

Conceptually yes, but polling itself is not the separation boundary.

The separation is created by where data lives and what may mutate authority:

CURRENT.md       human-owned authority
browser history  conversational continuity
model output     proposal

Polling makes that distinction visible and reduces stale context. It does not authenticate ownership or atomically bind a reply to one CURRENT revision.

Current mapping

The UI awaits /current before posting, and the server reads CURRENT again while building model messages. This is good defensive freshness.

There is still a small race:

browser displays revision A
human/process edits CURRENT
server reads revision B
model replies against B
rail may still momentarily show A

For propose-only conversation, that is acceptable in the alpha.

Risk

If Desk later gains consequential adapters, “we polled before Send” will not be strong enough. You would need to identify the authority revision against which the proposal or action was evaluated.

Concrete recommendation

Do not add locking yet. Add a small inspectable revision indicator when you introduce proposal artifacts:

Authority revision: 12

or use a displayed content hash/commit identifier.

Every saved proposal can then say:

Proposed against: authority-revision-12

That remains cat-able and git-diffable.

5. Device-role split

Plain claim

The split is sound:

myarch   = authority host, inference and media origin
eME640   = light Desk/Kodi client and optional control surface
LG       = primary living-room display sink
Fire TV  = fallback sink

Why it fits

- The weak eME640 does not perform model inference or heavy encoding.
- API keys remain on myarch.
- LG receives media through established playback paths rather than becoming a Mechanicall host.
- Fire Stick provides fallback without changing authority doctrine.
- Desk remains independent from the eventual player.

The research note correctly recommends ordinary media delivery before custom control machinery. LG streaming research

Risk

The architecture drifts if Desk becomes all three of these:

- proposal surface;
- universal remote;
- media orchestration server.

That would make hardware reliability look like failure of the authority product.

Concrete recommendation

Maintain explicit component ownership:

| Component | May do |
|---|---|
| Desk | Read CURRENT, converse, produce proposals |
| Media server | Index and stream media |
| Human-operated player | Start playback |
| Future accepted-action adapter | Execute one explicit preflighted media action |
| Model | Never invoke player or adapter |

6. Rank the next engineering

Before the three options: fix CI and the privacy/LAN boundaries.

After that:

1. Desk propose-play representation

Implement the smallest proposal artifact or copyable proposal shape. This advances CURRENT-as-product directly without granting playback capability.

2. Jellyfin/DLNA on myarch

Establish the ordinary manual delivery path:

human browses/accepts → human opens LG app → media plays

This proves the media substrate independently of Mechanicall automation.

3. webOS SSAP

Do this last. SSAP introduces:

- pairing;
- wake reliability;
- device credentials;
- external effects;
- action authorization;
- retry and failure semantics.

It only becomes valuable after manual Jellyfin/LG playback is reliable and users actually want one-step accepted execution.

Do not prioritize

- custom Leanback APK build;
- automatic wake/play;
- Fire Stick orchestration;
- remote desktop;
- elaborate TV guide integration;
- more visual Desk surfaces.

7. Representing preview → accept without model playback tools

Use two explicit authority states.

Proposal state

The model returns or drafts:

Playback proposal

Proposal: play-big-buck-bunny
Title: Big Buck Bunny
Source: library/movies-index.md
Sink: living-room-lg
Authority revision: 12
Status: PROPOSED

Unknowns
- LG wake state
- exact playable media URL

Human decision required
Accept, reject, or revise this proposal.

This can live at:

.aether/proposals/play-big-buck-bunny.md

It remains non-authoritative.

CURRENT then says:

Next: review-play-proposal

Next allowed action
Review .aether/proposals/play-big-buck-bunny.md.

Prohibited
- start-playback
- wake-lg
- model-approve

Accepted state

After human acceptance:

Next: manually-play-approved-media
Approval: APPROVED

Accepted proposal
- .aether/proposals/play-big-buck-bunny.md

Next allowed action
Human opens Big Buck Bunny using the LG/Jellyfin interface.

Prohibited
- model-start-playback
- substitute-title
- automatic-device-control

For the current alpha, acceptance records the decision; it does not give the model a tool.

If an execution adapter is later justified, it receives the proposal ID, re-runs preflight against the current revision, and performs only that declared action.

8. Doctrine audit

No direct doctrine violations found

The branch preserves:

- model propose-only;
- no model approval;
- silence is not permission;
- no Desk playback routes;
- no heavy eME640 inference;
- keys staying on myarch;
- CURRENT re-read per model turn;
- raw filesystem authority visible in the UI.

The tests also verify that action routes such as /kodi, /home, and /open-on-tv return 404. API tests

Doctrine ambiguities to correct

1. “History stays on this device” conflicts with server logging and history transmission.
2. Client-selected root lets a caller switch authority scope.
3. Wildcard CORS expands access beyond the intended same-origin Desk.
4. “Optional approval” is acceptable for conversation, but should not become the template for playback acceptance.
5. The promotional CURRENT is good onboarding copy, but pick-a-thread-and-chat is broad. It demonstrates grounding, not a sharp refusal boundary.

9. Branch and verification quality

CI is red

The latest GitHub Actions run failed in sh tests/run.sh. The public API exposes only the exit failure, not the detailed unauthenticated log, so I cannot responsibly name the exact failing assertion. But a red integration workflow is a merge blocker. Workflow run · test runner

Branch scope is too broad

The latest commit explicitly says it also includes Kingston VM host scaffolding already present on the session branch. Combined with 21 commits and 91 changed files, that makes the Desk product change harder to review and revert.

Concrete recommendation

Create a clean product branch from master and cherry-pick only:

- python/aether_desk.py;
- python/aether_desk_api.py;
- CLI wiring required for aether desk*;
- Desk tests;
- domains/house-tv-desk/;
- relevant TV scripts;
- stage verification and concise docs.

Keep Kingston, earlier boot experiments and unrelated Panel modifications out unless Desk actually depends on them.

Merge gate

P0 — before merge

- [ ] Make CI green.
- [ ] Remove request-controlled root.
- [ ] Reconcile browser-history claims with .aether/chat.jsonl.
- [ ] Remove wildcard CORS.
- [ ] Add a request-body limit.
- [ ] Remove absolute host path from /health.
- [ ] Split unrelated Kingston/host work from the Desk product diff.

P1 — immediately after

- [ ] Add one test proving CURRENT is re-read after changing between turns.
- [ ] Add one test proving /chat cannot select another project root.
- [ ] Add one test asserting whether transcript bodies are or are not persisted.
- [ ] Record a proposal against an inspectable authority revision.
- [ ] Observe Client-one completing a second unguided Desk session.

Final assessment

You are adding code within the architecture.

The strongest design decision was not the maximalist UI or Android work. It was the retreat from remote buttons to:

chat + visible CURRENT + no tools

That is the architecture becoming product.

The sprint becomes architecture drift only if the next move is to turn Desk into a media-control platform before the proposal/acceptance convention proves useful. Fix the truth and LAN boundaries, extract a clean branch, get CI green, and then test one inspectable entertainment proposal with Client-one.

Keep building the authority surface. Let Jellyfin play media. Do not make the model the remote.