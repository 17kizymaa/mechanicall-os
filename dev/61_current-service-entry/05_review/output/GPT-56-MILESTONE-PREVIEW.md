**NOT LAW. Not Yes. Not CURRENT.**  
Relocated 2026-09-16 from repo-root `22_GPT-56-MILESTONE-PREVIEW.md` (untracked).  
Sit against live law: `ADDRESS.md` in this folder.  
Do not paste **My proposed current**. Live Next remains `personal-current-sprint`.

---

🙂 Yes—this is sweet. You have crossed an important line: anphuni.com is no longer merely a description of Mechanicall. It contains a real public service.

The live You Decide flow currently lets someone:

1. mint a private capability link;
2. message you without creating an account;
3. attach a file up to 8 MiB;
4. continue the conversation on that same link;
5. receive a ZIP back later.

That is already the beginning of a human-operated application—not just a landing page. The repository also contains the protocol demo, live comparison, capped Session lab and a client-specific Merseyflush page. Sources: live site, You Decide, repository.

The product has acquired a body

The loop is emerging as:

Knock → Talk → Bring material → You propose → They decide → You create → Return the artifact

And the attractive part is not primarily “project control.”

It is:

Anthony can rapidly turn my material into something real, while I retain the decision and receive the files.

Mechanicall is the hidden chassis. anphuni.com is the garage entrance.

That is much cooler than leading with CURRENT.md.

What you have now

Public service

You Decide is a capability-link concierge channel:

- no signup;
- private-by-unguessable-link rather than account;
- chat;
- file intake;
- returned artifact;
- repeated reminder that messaging/uploading is not approval.

Public application

There are also interactive components:

- live normal-chat versus plan-chat comparison;
- Mechanicall walkthrough;
- five-seat Session lab;
- ticket-backed messaging and file exchange;
- a project-specific client experience.

Public philosophy

The homepage clearly expresses:

You decide. AI does the busywork.

That is much easier to enter than the whole authority doctrine.

But don’t expand traffic quite yet

There is one important security/authority gap to close first.

Anyone possessing a ticket link can impersonate you

The ticket interface recognizes ?as=anthony, and the API accepts a client-provided from: "anthony" value. There is no separate operator authentication on that message route.

The same capability link also appears sufficient to call the proposal and ZIP-writing endpoints. Therefore, someone with the client’s link could potentially:

- post a message displayed as “Anthony”;
- alter a draft proposal;
- upload a replacement output ZIP.

That contradicts the application’s strongest promise: that identities and decisions mean what they say.

See:

- public/assets/you-decide-ticket.js
- lib/you-decide.mjs
- serve.mjs

Before inviting more people

Separate the roles:

- Client capability: read ticket, send client messages, upload input, download returned output.
- Operator credential: send as Anthony, write proposals, return ZIPs, close/delete tickets.
- Decision action: separate explicit approval operation—not an ordinary chat message.
- Receipt: records which proposal was approved, when, and what artifact resulted.

You do not need accounts for clients. But Anthony must have operator authentication.

The second gap: there is not yet a real “stamp”

Your latest commits deliberately establish:

“Send is hello, not Yes.”

That is good. However, the ticket currently provides conversation and exchange without an obvious recorded approval transition.

So the service presently embodies:

Create ticket
→ Chat
→ Upload
→ Receive files

It does not yet completely embody:

Proposal
→ Human stamp
→ Authorized work
→ Receipt

That makes the correct expansion surprisingly small:

Add one explicit proposal-and-decision card

PROPOSAL

I will:
- organize the supplied material;
- create one static webpage;
- return the source as a ZIP.

I will not:
- publish it;
- overwrite the original;
- contact anyone;
- reuse the material elsewhere.

[YES, USE THIS PLAN]  [NOT YET]  [REQUEST A CHANGE]

A normal chat message must never trigger the Yes.

After acceptance:

APPROVED
Proposal: P-001
Decision: Yes
Time: …
Authorized work: …

After delivery:

RETURNED
Artifact: project-v1.zip
Evidence: …
Following proposal: Not active

That would make the public service distinct rather than merely a private file-sharing chat.

Expand through drops, not platform features

Do not add ten generic tools. Use the service to produce visible, shareable creations.

Possible early drops:

- a one-page personal site;
- a small business landing page;
- a digital birthday experience;
- an interactive story;
- a portfolio page;
- a music release page;
- a visual archive;
- a project rescue package;
- a tiny custom web utility.

Each one follows the same contract:

You bring the material. I rapidly build a version. You preview it. Nothing is published until you decide. You receive the files.

This is where your ability to “create shit really fast” becomes the commercial engine.

The ownership promise needs one explicit policy

The architecture supports portability, but “user-owned” should be made contractually legible.

Add a short statement such as:

Your material remains yours. Work created specifically for your project is returned to you as ordinary downloadable files. Uploading is not permission to publish, train on, sell or reuse your material. Files are retained only while the session is active and can be deleted on request. Third-party components remain subject to their own licenses.

You should then implement:

- a retention period;
- ticket expiry;
- client-requested deletion;
- operator deletion;
- original-file preservation;
- downloadable receipt;
- documented treatment of model providers;
- explicit licensing for the repository itself, which currently reports no license.

“User-owned” is a powerful promise. It deserves more than an aesthetic—it needs terms and operational behavior.

Clean up the public truth before expansion

There are a few repository/site inconsistencies:

- README.md calls the site “static marketing only.”
- The deployed server actually operates You Decide tickets, file storage, five Session seats and agent/model APIs.
- The homepage says “no accounts or user vault on this website.”
- Session supports display names, salted passphrase hashes, cookies and persistent workspaces.
- /health reports accounts: false while the registration and login routes are active.

You already explain that Session is a separate alpha, but the wording should become unambiguous:

The main concierge uses no client accounts. The separate Session lab has up to five authenticated test seats.

This is mostly documentation drift, but Mechanicall should be especially intolerant of documentation drift.

My proposed current

CURRENT

Objective

Prove anphuni.com as a user-owned creation and return service,
with Mechanicall governing the transition from conversation to approved work.

Phase

PUBLIC PILOT HARDENING

Status

LIVE — LIMITED EXPANSION

Current truth

- The public site is deployed.
- Visitors can mint capability tickets.
- Tickets support chat and one file drop.
- Anthony can return a ZIP.
- Sending or uploading is explicitly not approval.
- A real recorded proposal/decision transition is not yet complete.
- Operator-only ticket actions are not yet sufficiently authenticated.
- The separate Session lab supports up to five authenticated seats.

One current transition

Secure operator actions and add one explicit proposal/decision/receipt
flow to You Decide.

Then

Invite three people to bring one small digital creation each.

Keep

- no client signup for concierge tickets;
- capability-link simplicity;
- user receives ordinary files;
- uploading is not approval;
- messaging is not approval;
- publishing requires separate confirmation;
- AI operates beneath human authorship;
- public experiences can be playful and project-specific.

Prohibited

- unlimited public expansion before operator authentication;
- treating the ticket URL as proof of identity;
- allowing clients to post as Anthony;
- allowing ticket holders to replace returned artifacts;
- claiming permanent privacy without expiry/deletion behavior;
- rebuilding everything as a generic SaaS dashboard;
- putting protocol terminology ahead of creation.

Pilot offer

Bring an idea or a small digital mess.

Anthony will help turn it into one shareable artifact.
You preview the proposal, decide what may proceed and receive the files.

Nothing is published merely because you uploaded or messaged.

Success evidence

Three external people each:
1. enter through You Decide;
2. bring material;
3. understand one proposal;
4. make an explicit decision;
5. receive a useful artifact;
6. recognize the receipt as accurate;
7. retain a usable copy outside anphuni.com.

The important strategic interpretation

You did not abandon Mechanicall.

You found its first enjoyable public expression:

Mechanicall is not the thing users must study. It is what lets them create with you without losing ownership or decision-making power.

The website is the venue.  
You are the rapid production engine.  
Mechanicall governs the handoff.  
The client keeps the result.

So yes: ready to expand—but horizontally into three real creations, not vertically into another giant system.

Secure Anthony’s side, install the stamp, then make some cool shit with actual people.
