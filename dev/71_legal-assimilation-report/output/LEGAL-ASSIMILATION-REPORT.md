# Legal assimilation report — anphuni × Mechanicall: You Decide

**Status:** research artifact · **not legal advice** · England & Wales · sole trader · written 2026-09-19 from repo facts + general knowledge of UK law. Thresholds quoted are the ones in force for tax year 2025/26 as I know them — **verify each against the linked primary source before relying on it**; some may have moved.
**Question:** can the anphuni business's targets (£1,000 income + £4,000 extra savings before Jan 2027) run through this application without legal exposure, and are the protocol docs / aether CURRENT machinery themselves a problem?
**Short answer:** the protocol is not the problem — it is the strongest thing you have on the compliance side. The exposures are ordinary small-business ones (business-name disclosure, a privacy notice that describes the rooms, ICO fee, consumer pre-contract information, HMRC registration once income exceeds £1,000). All are cheap. One item needs care: the paper-trading room, if it ever drifts from simulation towards suggestion. Nothing found that blocks the January targets.

---

## 0. What the application actually does (facts checked on disk)

| Fact | Source |
|------|--------|
| Public site is static + a "You Decide" room per 32-hex ticket id. No accounts, link is the key. | `serve.mjs`, `privacy.html` |
| A room stores `messages.jsonl`, `NOTICE.json`, `propose.md`, one file drop ≤ 8 MiB, optional `out.zip`, on a Render persistent disk (`/var/data/seats`). | `lib/you-decide.mjs`, `render.yaml` |
| Region for that disk is not set in `render.yaml` → Render default (**Oregon, US**) unless set in the dashboard. | `render.yaml` |
| Room chat is **not** sent to a model; the operator replies by hand via `YOU_DECIDE_OPERATOR_KEY`. `/session` and `/compare` do proxy to OpenRouter. | `serve.mjs`, `privacy.html` |
| Paper trader: **simulated prices** (`Math.random` walk from seeds), real UK ticker *names* (VOD, LLOY, BP, SHEL, AZN, HSBA), no live data, no real money, labelled "paper · not live". Only one room (`happy-birthday`) gets it. | `you-decide-trader.js:1-10`, `DEFAULT_PAPER_TICKETS` |
| Site shows business name "anphuni" and an email. **No legal name, no postal/service address.** | `contact.html`, `index.html` |
| `privacy.html` exists; describes Session and rooms in general terms. Does not name a controller, lawful basis, retention period, or the US hosting. | `privacy.html` |
| No prices anywhere. Work is currently given, not sold. | roster, POINTERs, site |
| Aliases replace client names; INTAKE template forbids identity; "never without asking" list defaults to all-on; every destructive/external action needs the operator's explicit Yes; approvals are timestamped in `events.jsonl`/`DECISIONS.md`. | `templates/alias/*`, `CURRENT.md`, `.aether/` |
| Repo licence Apache-2.0. | `LICENSE` |

Hold these facts against each law below. Where a law bites, it is usually because of a missing sentence on the site, not because of the protocol.

---

## 1. Tax — HMRC (the £1,000 income target)

| | |
|--|--|
| **Law** | Income Tax (Trading and Other Income) Act 2005 Part 6A (trading allowance); Taxes Management Act 1970 s.7 (notice of liability); Social Security Contributions and Benefits Act 1992 (Class 2/4 NICs) |
| **Applies?** | Yes, the moment anyone pays you for a project transition — money, or goods/services in kind. Gifts with no expectation attached are not trading income; "pay what you like *for the work*" is. |
| **Threshold** | **Trading allowance £1,000 gross per tax year.** Gross income ≤ £1,000 → no tax, no need to register or file. Gross > £1,000 → must register for Self Assessment by **5 October after the end of the tax year** (for income in 2026/27, that's 5 Oct 2027) and file by 31 Jan following. You may still deduct the £1,000 allowance instead of expenses. |
| **Your target** | £1,000 *income* before January sits **exactly at** the allowance — but the tax year runs 6 Apr 2026 – 5 Apr 2027, so anything you earn Jan–Apr 2027 counts too. Plan as if you will exceed it. |
| **NICs** | Class 2 is no longer a charge (since 6 Apr 2024) — profits over the small-profits threshold (~£6,845) earn credits for free; below it you may pay voluntarily to protect State Pension. Class 4 (6%) only over £12,570 profit. At your scale: nil. |
| **Interaction with employment / benefits** | If you have PAYE employment, your Personal Allowance is probably already used there → trading profit above £1,000 is taxed at 20% from the first pound. If you claim **Universal Credit**, self-employed earnings must be reported monthly and the Minimum Income Floor may apply after the start-up period — this is the item most likely to surprise; check before invoicing anyone. |
| **The £4,000 savings** | Not a tax event. Savings interest has its own Personal Savings Allowance (£1,000 basic rate). If the savings come from *trading* profit, that profit is taxed as above first. If any of it is meant to come from *trading securities* (see §5) it is capital gains territory — CGT annual exempt amount **£3,000**. Paper trading generates no gain. |
| **Protocol already gives you** | `RECEIPTS/` per alias and `DELIVERED/` = the record HMRC wants (keep 5 years after the 31 Jan deadline). Add one line per payment: date, alias, amount, what for. |
| **Open** | (a) A single ledger file — `~/anphuni-project/LEDGER.md` or CSV — none exists. (b) Decide whether "servant-class" family rooms (Mum, Dad) are ever paid; if not, they are outside trade entirely. |
| **Cheapest closure** | Ledger file + a calendar note for 5 Oct 2027. Nothing to file until then. |

## 2. Trading under a business name — Companies Act 2006 Part 41

| | |
|--|--|
| **Law** | Companies Act 2006 ss.1200–1206 (sole traders and partnerships trading under a business name) |
| **Applies?** | **Yes.** "anphuni" is not your name. A sole trader using a business name must state their own name and an address for service on business letters, written orders, invoices, receipts, written demands for payment **and websites**, and must give it in writing on request to anyone you deal with. |
| **Facts** | Site shows "anphuni" + email only. |
| **Open** | No legal name or service address anywhere on anphuni.com or in the room. |
| **Risk** | Low (fine on summary conviction; more practically, a client can refuse to pay and the contract can be unenforceable against them if they were prejudiced). But it is the one thing an unhappy person's solicitor checks first. |
| **Cheapest closure** | One footer line on `contact.html`/`privacy.html`: "anphuni is the trading name of [Your Name], [address for service]". A PO box or a virtual-office address is fine; it need not be your home. Same line on any invoice/receipt template. |

## 3. Website information duties — E-Commerce Regulations 2002 & Consumer Contracts Regulations 2013

| | |
|--|--|
| **Law** | Electronic Commerce (EC Directive) Regulations 2002 reg.6; Consumer Contracts (Information, Cancellation and Additional Charges) Regulations 2013 (CCRs) |
| **Applies?** | ECRs: yes, you provide an "information society service". CCRs: yes **the moment a consumer agrees to pay** for a service at a distance (via the room, email, WhatsApp). While work is free, CCRs mostly don't bite. |
| **ECR reg.6 wants** | Name, geographic address, email, (VAT number if registered — you aren't). Same fix as §2. |
| **CCR wants** (once paid) | Pre-contract information (reg.13/Sch 2): main characteristics, your identity, total price, duration, **the 14-day cancellation right and a model cancellation form**. If you fail to tell them about the cancellation right, it extends to **12 months**. If they want you to start within the 14 days they must ask expressly, and if they then cancel they pay for work done. |
| **Digital content** | If you deliver a file (site, PDF, zip) it's "digital content not on a tangible medium": you need their express consent + acknowledgement they lose the cancellation right on download, or they can cancel after receiving it. |
| **Protocol already gives you** | The room's "Nothing is decided until you say so" + operator Yes gate means no contract forms by accident. The opener's "how often do you want to hear from me" → service duration. |
| **Open** | No paid-work terms exist yet. |
| **Cheapest closure** | One `templates/alias/TERMS.md` (or `OFFER.md`) used only when money is mentioned: what/price/duration/your identity/14-day right/request-to-start-early sentence. Send it into the room before any payment; their "yes, start" reply in the thread is your record. Do **not** put this in the hello opener — CURRENT rejects `form-instead-of-hello`, and legally it isn't needed until money. |

## 4. Consumer service standards — Consumer Rights Act 2015; DMCC Act 2024

| | |
|--|--|
| **Law** | Consumer Rights Act 2015 Part 1 Ch.4 (services: s.49 reasonable care and skill; s.50 information you give is binding; s.51 reasonable price if none agreed; s.52 reasonable time) and Ch.3 (digital content: s.34 satisfactory quality, s.35 fit for purpose, s.36 as described). Digital Markets, Competition and Consumers Act 2024 Part 4 Ch.1 (unfair commercial practices — replaced CPUTRs from 6 Apr 2025). |
| **Applies?** | CRA: yes once paid. DMCC: yes now — it covers **misleading actions/omissions in any commercial communication**, including "case studies" and testimonials, even for free work if it promotes a trade. Fake or unconsented reviews are a banned practice. |
| **Facts** | `merseyflush/CASE-STUDY.md` exists (operator-only). Prospectus roadmap wants "3 usable testimonials" and "one honest case study" published. |
| **Protocol already gives you** | s.50 — "information you give is binding" is *exactly* what the CURRENT/receipt discipline records; you are unusually well protected against "you promised X". Alias practice + "post it publicly" default-off in INTAKE = consent gate for case studies. |
| **Open** | Case-study / testimonial publication has no written consent artefact. |
| **Cheapest closure** | Before publishing anything about a project, get a one-line "yes you can show this" in the room and copy it to `RECEIPTS/consent-publish-YYYY-MM-DD.md`. Never edit a testimonial. |

## 5. Financial regulation — the paper-trading room

| | |
|--|--|
| **Law** | Financial Services and Markets Act 2000 s.19 (general prohibition), s.21 (financial promotion restriction), s.22 + Regulated Activities Order 2001 (arts 25 arranging, 53 advising); Gambling Act 2005 (s.3 gambling, s.9 betting) |
| **Applies?** | **Not as built.** Simulated random prices; no real instruments traded; no stake; no return; no recommendation of a particular investment. That is a game with stock-ticker labels — outside FSMA (no specified investment is dealt in or advised on) and outside the Gambling Act (nothing of value staked or won). |
| **Where it turns red** | Any one of: (a) real prices with the operator or a model suggesting "buy X" → *advising on investments* (RAO art 53) — needs FCA authorisation or an exemption; (b) a public page inviting people to trade real money anywhere → *financial promotion* (s.21) — needs an authorised person's approval; (c) linking or referring to a real broker for reward → *arranging*/introducer. Also the DECISIONS log shows a rejected idea to "steal a fully-interactive paper trader" grammar — grammar is fine; a **live feed** would move you towards (a). |
| **Protocol already gives you** | Paper locked to one id (`DEFAULT_PAPER_TICKETS`); CURRENT rejects `live-money-as-paper-trading`, `ibkr-passing-off`, `stocks-on-every-room`; "not live" labels in the UI. |
| **Open** | (i) `paperTicketIds()` also reads `YOU_DECIDE_PAPER_TICKETS` from env — unverified on Render (F3 from the kit receipt). (ii) No on-page sentence saying "simulation, not advice, not a real market". (iii) Using real ticker names is fine but keep prices obviously synthetic. |
| **Cheapest closure** | One line in the desk header: "Practice only. Prices are invented. Nothing here is investment advice or an invitation to trade." Confirm the Render env var is unset. Never add a live price feed without re-reading this section. **Your own £4,000 savings target must not be sourced from anything this room does** — the room is a toy; keep it a toy. |

## 6. Data protection — UK GDPR & Data Protection Act 2018

| | |
|--|--|
| **Law** | UK GDPR arts 5, 6, 13, 17, 28, 30, 32, 44–49; DPA 2018; Data Protection (Charges and Information) Regulations 2018 |
| **Applies?** | **Yes.** A room holds whatever a person types and drops — that is personal data (often about third parties too: customers, family). Aliases reduce but do not remove it. You are the **controller**. |
| **Facts** | Data on Render disk, region probably **US**; OpenRouter (US) only for Session/compare, not rooms; privacy page exists but is Session-centric; no retention period; no named controller; no lawful basis stated. |
| **ICO fee** | Sole traders processing personal data must pay the data protection fee (**Tier 1, ~£52/yr**, direct debit −£5) **unless exempt**. Exemption covers processing *only* for staff admin, advertising your own business, or **accounts and records** of your own customers. Holding a client's *project material* to do the work for them is arguably beyond "accounts and records". Assume **not exempt** once you take a paying client; use the ICO self-assessment tool to confirm. Failure to pay is a fixed penalty (£400 tier 1), not a crime. |
| **Lawful basis** | Art 6(1)(b) contract / 6(1)(f) legitimate interests for the room; 6(1)(a) consent only for publishing case studies and for "use your photos/videos". Your INTAKE checklist is literally a consent record for those — keep it. |
| **International transfer** | If the Render disk is in Oregon, every room is a restricted transfer to the US. Lawful routes: the **UK-US Data Bridge** (only if Render is certified under the EU-US DPF + UK extension — check Render's DPA), or the ICO **IDTA / UK Addendum** (Render's standard DPA usually includes SCCs + UK Addendum — check and keep a copy). Or simply set the service region to **Frankfurt** (EU adequacy) at next redeploy — one line in `render.yaml`. |
| **Processors (art 28)** | Render (hosting) and OpenRouter (inference for Session/compare) are processors → you need their DPA terms on file. Both publish one; download and put in `~/anphuni-project/01_architecture/` or similar. Anthropic/OpenAI via OpenRouter are sub-processors. Your **local** tools (Onyx, opencode, aether) processing client material on your own disk are *you*, not processors — but any cloud model you point them at is. |
| **Retention (art 5(1)(e))** | Nothing deletes anything. Prospectus line 410 already asks for "deletion and retention practices". |
| **Security (art 32)** | Link-is-the-key is capability security: adequate for low-sensitivity, but a leaked URL leaks the room. Reasonable given the data class **if** you say so in the notice and never put health/financial/children's data in a room. |
| **Rights** | Erasure (art 17): a person can ask you to delete the room; you need to be able to (`rm -rf` the ticket dir + the `inbox/tickets` mirror in mechanicall-os + any alias `MATERIAL/`). Access (art 15): the room itself is nearly the SAR answer. |
| **Children** | If any alias is under 18 (`pocket-playtester`? `the-block-p`?) the Age Appropriate Design Code applies to the room. Flag if so. |
| **Protocol already gives you** | Data minimisation by design (aliases, no accounts, no identity in INTAKE), purpose limitation (one room, one project), an audit trail (events), human-in-the-loop for every disclosure. This is a genuinely good Art 25 privacy-by-design story. |
| **Open** | Privacy notice gaps; ICO fee; region/transfer; retention rule; DPA copies; deletion runbook. |
| **Cheapest closure** | (1) Add a "You Decide rooms" paragraph to `privacy.html`: who the controller is (your name, §2), what is stored, where (host + region), why (to do the project you asked for), how long (e.g. "until you ask, or 12 months after the last message"), that a room link is the key, how to ask for deletion (email). (2) Pay the ICO fee when the first paying client appears. (3) Set the Render region to Frankfurt at the next deploy, or file Render's DPA. (4) A `scripts/room-forget.sh <id>` that previews then deletes — under the operator Next, with your Yes each time. |

## 7. Electronic marketing — PECR 2003

| | |
|--|--|
| **Law** | Privacy and Electronic Communications (EC Directive) Regulations 2003 reg.22 (unsolicited marketing by electronic mail — includes SMS, WhatsApp, DMs) |
| **Applies?** | When you **hand out URLs**. A personal, individual message to someone you know, about their own project, is a conversation, not marketing. A templated blast to 100 followers inviting them to "get a room" is direct marketing to individual subscribers and needs **prior consent** (or the soft opt-in: existing customers, similar services, opt-out offered). Public posts (Instagram story, a page) are not PECR — they're ASA/CAP Code territory instead. |
| **Protocol already gives you** | The roster is people who already know you and mostly already talked to you; wave-1 in the prospectus is "privately invite 5–10". |
| **Open** | Nothing today. Watch it at "Wave 2/3" (public story) — use a public post with a link people come *to*, not outbound DMs. |
| **Cheapest closure** | Keep `LINKS.md` sharing 1:1 and personal. No bulk sends. |

## 8. Intellectual property in delivered work

| | |
|--|--|
| **Law** | Copyright, Designs and Patents Act 1988 s.11 (first owner = author), s.90(3) (assignment must be in writing, signed), s.9(3) (computer-generated works — author is the person making the arrangements) |
| **Applies?** | Yes for every page, image, text you produce. Default: **you** own it, the client gets an implied licence to use it for the purpose it was made. Model-generated portions: UK gives copyright to the person who made the arrangements (probably you), but ownership of purely AI-generated output is unsettled. Client-supplied material stays theirs; you need their permission to use it (INTAKE's "use your photos/videos" toggle). |
| **Protocol already gives you** | `MATERIAL/` (theirs) vs `DELIVERED/` (yours→theirs) separation. |
| **Open** | No statement of who owns `DELIVERED/`. Some clients (CIC, Toastmasters district) will want an assignment. |
| **Cheapest closure** | One sentence in the `TERMS.md` from §3: "On payment, copyright in what I deliver is assigned to you; anything you gave me stays yours; I may keep a copy for my records and, only with your yes, show it as an example." For free work, say "licensed to you for any use" in the delivery message. |

## 9. Acting on someone's behalf — Computer Misuse Act 1990, Fraud Act 2006, platform terms

| | |
|--|--|
| **Law** | CMA 1990 s.1 (unauthorised access), s.3 (unauthorised acts impairing a computer); Fraud Act 2006 s.2 (false representation) |
| **Applies?** | Only if you log in to, post from, or message *as* the client without their authority. With their express authority it is not unauthorised — but most platforms' terms forbid sharing credentials, and a "message anyone as you" that misleads the recipient about who is speaking can be a false representation. |
| **Protocol already gives you** | "message anyone as you" and "post it publicly" default to **never without asking** in INTAKE; every such act needs the operator Yes; the model is prohibited (`agent-publish-delete-spend-message-deploy`). This is the right shape. |
| **Open** | Keep the authority *in writing in the room* before each act, not a standing blanket. Prefer being added as a collaborator/manager to using their password. |
| **Cheapest closure** | None needed beyond current practice; record each authorisation in `RECEIPTS/`. |

## 10. Advertising — CAP Code / ASA; DMCC Act 2024

| | |
|--|--|
| **Applies?** | Public claims on anphuni.com and Instagram. Claims must be substantiated ("dozens of real sessions" — only once true). Prospectus phrasing like "Anphuni has processed enough real projects…" is aspirational; don't publish numbers you can't evidence from `RECEIPTS/`. |
| **Open** | Nothing now. |
| **Cheapest closure** | Evidence-first is already a Keep in CURRENT. |

## 11. The protocol docs and the aether/CURRENT Python themselves

| | |
|--|--|
| **Licence** | Apache-2.0 — permissive; you keep copyright, others may use it with attribution. If you want the *method* to be yours commercially, the moat is the operating evidence (Eduwares, receipts), not the licence. No legal issue. |
| **Records** | `events.jsonl` approvals with a reason, `DECISIONS.md`, per-alias `RECEIPTS/` = contemporaneous business records. Under the Electronic Communications Act 2000 s.7 and Civil Evidence Act 1995 these are admissible; a client's "yes, go" in the room is evidence of instruction. **The protocol protects you here.** |
| **Automated decisions** | UK GDPR art 22 (decisions based solely on automated processing) does not apply — a human takes every consequential decision. That is precisely what "models never approve" buys you. |
| **Risk in the docs** | Only one: `.aether/events.jsonl` and `DECISIONS.md` contain your own approval prose including income figures and private remarks about relatives — in a **public GitHub repo**. Not illegal; not wise. The 07:52 approval reason quoted above is now in `origin`. Consider `git filter-repo` on those two files or moving them out of tree; at minimum stop committing them. |
| **Client CURRENT** | The "no client CURRENT / no stamp for them" rule also has a legal upside: you never purport to hold their authority over their own affairs — you are a contractor acting on instruction, not an agent with delegated power. Keep it. |

## 12. Other small items

- **Insurance** — Professional indemnity is not compulsory for this work, but £100–200/yr for £100k cover is cheap peace of mind once money changes hands.
- **Accessibility** — Equality Act 2010 s.29 duty on service providers; the site is simple HTML — fine; keep the room usable without JS-heavy dependencies.
- **Late payment** — Late Payment of Commercial Debts (Interest) Act 1998 only for B2B (merseyflush, CIC) — statutory 8% + base rate. Mention on invoice.
- **Domain/brand** — "anphuni" unregistered mark; unregistered rights (passing off) accrue with use. A UK trade mark is £170 per class if you ever care.
- **Cash basis** — Default for sole traders since 2024/25; simplest for you.

---

## 13. Consolidated verdict

| # | Area | State | Blocks Jan targets? | Cost to close |
|---|------|-------|---------------------|---------------|
| 1 | HMRC / trading allowance | amber — nothing to file yet; ledger missing | No | 10 min: ledger file + calendar note |
| 2 | Business-name disclosure | **red** (easy) | No, but fix before first invoice | 5 min: footer line |
| 3 | ECR / CCR pre-contract info | amber — only bites when paid | No | 30 min: `TERMS.md` template |
| 4 | CRA / DMCC (case studies, testimonials) | amber | No | consent line in `RECEIPTS/` |
| 5 | FSMA — paper room | green as built; red if live prices/suggestions ever appear | No | 1 line disclaimer; verify env |
| 6 | UK GDPR | **amber/red** — notice gaps, ICO fee, US region, no retention/deletion | No | 1 hr: notice paragraph; £52 fee when paid; region or DPA; forget script |
| 7 | PECR | green today | No | keep 1:1 sharing |
| 8 | IP | amber | No | one sentence in TERMS |
| 9 | Acting as them | green (protocol) | No | keep per-act record |
| 10 | Advertising | green | No | evidence first |
| 11 | Protocol / repo | green legally; **housekeeping red**: private prose in public git | No | stop committing events/DECISIONS prose; consider filter-repo |

**Are your efforts protected?** Against the ordinary failure modes — "you never told me", "you did that without asking", "who owns this", "what did you do with my stuff" — yes, unusually so, because of the receipts, the Yes gate, and the alias/INTAKE discipline. Against the state (HMRC, ICO, Companies Act), you are a normal pre-revenue sole trader with four cheap notices to add. Against yourself: keep the paper room a toy, and keep private prose out of public git.

---

## 14. Sources to verify (index these in Onyx — see `ONYX-INGEST-LIST.md`)

legislation.gov.uk: ITTOIA 2005 Pt 6A · Companies Act 2006 Pt 41 · CCRs 2013 · CRA 2015 · DMCC Act 2024 Pt 4 · FSMA 2000 ss.19–22 · RAO 2001 arts 25, 53 · Gambling Act 2005 ss.3, 9 · UK GDPR (retained) · DPA 2018 · DP (Charges and Information) Regs 2018 · PECR 2003 reg.22 · CDPA 1988 ss.9, 11, 90 · CMA 1990 ss.1, 3 · Fraud Act 2006 s.2 · ECRs 2002 reg.6.
gov.uk / HMRC: "Tax-free allowances on property and trading income" · "Register for Self Assessment" · "Self-employed National Insurance rates" · "Cash basis".
ICO: "Data protection fee — self-assessment" · "International transfers" · "UK-US data bridge" · "Privacy notices" · "Children's code".
FCA: Perimeter Guidance manual (PERG) 2 and 8 · "Financial promotions — unauthorised persons".
CMA/CAP: DMCC Act 2024 unfair commercial practices guidance · CAP Code s.3 (misleading advertising).
Render: Data Processing Addendum · region list. OpenRouter: privacy/DPA.

*Not legal advice. Prepared as a research artifact under `legal-assimilation-report`. Before the first paid engagement, a one-hour session with a solicitor or an accountant who does sole-trader work would cost less than a mistake under §2 or §6.*
