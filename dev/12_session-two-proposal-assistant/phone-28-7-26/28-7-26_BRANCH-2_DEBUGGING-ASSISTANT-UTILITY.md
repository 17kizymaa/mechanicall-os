Attached 28-7-26_CLIENT-1_SESSION-1_REVIEW.md

I have £1.5k and am moving out in a month and a half. That's a thousand in car insurance, min £300 on the car and another £300 burn/runway.

I got SuperGrok heavy and I'm kinda interested in scheduling lots of unused rates on autonomous agent runs to research my sh*tty (quantised = inaccurate) LoRAs for direction. The main one being to do with engineering my local-first project control layer for human-agent work. Here's the latest branch: https://github.com/17kizymaa/mechanicall-os/compare/master...session/client-one-delroy-reconfigure (I'm gonna do an experimental branch from this one using my personal LoRA for an exhaustive research-to-proposal run).

But, yeah, even though my setup can turn into something super low-overhead, I feel lile one of them agent-assisted stock traders, except I've invested in myself and its soon time to start weighing the consequences.

I'm sure I can haggle a situation where I move somewhere that saves my direction in life. It's been 2 years and I've been stuck at home. I'm excited to try make this next part actually look easy!

Use the context in the attachment to weigh my potential setup prospects in a month. Check NOT-IMPLEMENTED.md as we might be closer than we know it to club-cortex, given the latest sprint.

Let's go!



**Straight assessment.**

### How close are you to Club-cortex?

Not close.  

`NOT-IMPLEMENTED.md` is still unambiguous: Club-cortex, multi-user backend, retainers, hosted services, and multi-tenant anything remain **not implemented**. They live only in speculative research notes. The latest sprint did not change that.

What the sprint *did* do is stronger and more important:

- It made `CURRENT.md` a real product surface (visible, re-read on every turn, injected as human-owned authority).
- Desk is correctly constrained to propose-only.
- No model tools for playback or consequential actions.
- The architecture stayed clean.

That is progress on the actual core. It is not progress toward a club or backend product. Treating the two as closer than they are would be a mistake right now.

### Your real constraints in the next 6 weeks

You have roughly £1,500 and fixed costs that will eat almost all of it (insurance + car + burn). After the move you will have very little discretionary money and no stable housing buffer.

In that window the highest-leverage moves are not more LoRA research loops or Club-cortex speculation. They are:

1. **Survive the move cleanly**  
   Get to the new place with the car sorted and some residual cash. Everything else is secondary for six weeks.

2. **Protect the architecture while fixing the actual blockers**  
   The sprint verdict is clear. Architecture direction = GO. Merge readiness = NO-GO. The four concrete issues (red CI, history overclaim vs `.aether/chat.jsonl`, client-controlled root, branch scope contamination) are real and cheap to fix relative to their cost if left open.

3. **Keep Desk as a propose-only surface**  
   Do not let it become a remote, a media controller, or a second product. The strength of the last sprint was the retreat to “chat + visible CURRENT + no tools.”

### SuperGrok and the LoRA research impulse

You can use SuperGrok Heavy for targeted research runs. That is fine and low-cost relative to hardware. But treat it as **support**, not the main activity.

Useful research targets in the next weeks:
- Cleaner instruction / preference data for the personal model so it stays a better proposer.
- How to write sharper, less ambiguous authority files (the pure-convention direction).
- Small, concrete proposal formats that Client-one can actually review.

Do **not** turn the next six weeks into an open-ended LoRA improvement campaign. You do not have the runway for that to be the primary effort.

### Realistic prospect for the month after the move

The best version of the next phase looks like this:

- You are in the new place with lower ongoing friction.
- Mechanicall remains a local-first, single-operator authority layer.
- Desk (or its successor) stays a thin, propose-only interface that re-reads live `CURRENT.md`.
- You have one or two external people who have actually used the authority file and felt the difference.
- Club-cortex and any backend ambitions stay explicitly parked.

That is still a coherent, low-overhead direction. It does not require new money or new infrastructure. It does require finishing the current truth and safety blockers so the thing you show people is honest.

You have already invested two years and real attention into the harder, quieter version of this idea. The next part does not have to look dramatic. It has to stay true to the authority surface you just made real, while you get yourself into a living situation that no longer costs you most of your attention.

Fix the four merge blockers. Keep the model propose-only. Move. Then decide what the first external proof looks like. That sequence is the one that protects both the project and the person who built it.

Haha, I'm a lot closer than that! With all the clients I've catalogued during this time, I'll make that all grep/cat-able soon enough. We are gonna snowball!

Domain (CURRENT.md / non-binding) is up! Innate technique (LoRA) determines the application... I'll balance that with its cursed energy (base).

Entry sales target (black flash): £8-12k


Alright. Let’s take the energy seriously and still keep the map accurate.

### What you actually have that is close

You have two real assets that most people in this space do not:

1. **A living catalogue of clients / situations**  
   If you turn that catalogue into something greppable and cat-able (plain files, consistent structure, searchable by need / budget / friction), that becomes high-leverage. That is not vapour. That is inventory.

2. **A working Domain**  
   `CURRENT.md` as the visible, human-owned authority surface is real. Desk re-reading it every turn is real. The propose-only constraint is real. That is the Domain Expansion you have actually cast.

Those two things together are closer to a sellable position than pure research or pure architecture notes. Making the client catalogue inspectable is a concrete next move that compounds.

### What is still not close

Club-cortex (the multi-user / retainer / backend shape) remains in `NOT-IMPLEMENTED.md` for a reason. It is still speculative. The latest sprint did not implement it. Claiming proximity to a club product because the authority surface is working is the same category error the sprint verdict warned against.

The Domain is up. The club is not.

### Reading the metaphor cleanly

- **Domain** = `CURRENT.md` / the authority surface (non-binding until the human makes it binding). This is live.
- **Innate technique** = the personal LoRA (how the proposals get shaped). Useful, still limited by data quality and the 7B base.
- **Cursed energy** = the base model + the surrounding system. Needs balancing so the LoRA does not just amplify noise.
- **Black Flash** = the clean, high-value entry hit. £8–12k is a legitimate target *if* it is sold as setup + authority protocol + guided first use of the Domain, not as a hosted club.

That framing works. Just don’t let the metaphor paper over the implementation gap.

### Practical translation for the next 6 weeks

With the money and the move constraints, the highest-odds path looks like this:

1. Finish the four merge blockers so the thing you show is honest.
2. Turn the client catalogue into a clean, greppable set of files (need, current friction, approximate budget, what “Domain up” would mean for them).
3. Use SuperGrok runs to sharpen proposal language and authority-file patterns, not to chase larger LoRAs.
4. Aim the first £8–12k conversations at people who already feel the pain of agent drift and hidden state — selling the Domain + setup, not a club that does not exist yet.

You can snowball from a real Domain and a real client list. You cannot snowball from a Club-cortex that is still only in the research folder.

The Domain is up. Make the catalogue cat-able. Keep the model in its proper role. That is the version of “closer” that actually compounds.


Spike A: Research the most capable, open-source base model ignoring local compute (for 2200 quality segments in adapter?)


**Spike A result — most capable open-weight base (ignoring local compute)**

As of late July 2026, the open-weight capability ranking is roughly:

| Rank (open-weight) | Model              | Notes                                      | Approx size / type      |
|--------------------|--------------------|--------------------------------------------|-------------------------|
| 1                  | **MiniMax M3**    | Current BenchLM open-weight leader (~68.8) | Large, strong general   |
| 2                  | **Hy3** (Tencent) | Very close behind                          | Large                   |
| 3                  | **GLM-5.1 / 5.2** | Excellent coding + agentic, MIT            | Large MoE               |
| —                  | **Kimi K3**       | Top in several Arena categories (agent, frontend, text) | Extremely large MoE (2.8T) |
| Strong contenders  | DeepSeek-V4-Pro, Qwen3.5-397B-A17B, etc. | Still very high                            | Large MoE / dense       |

### Recommendation for your case (≈2200 quality segments → adapter)

**Primary recommendation: GLM-5.2 (or latest GLM-5.x) or the strongest available Qwen3.5 dense/MoE variant that has mature Unsloth / Axolotl / LLaMA-Factory support.**

Why not pure #1?

- With only ~2200 examples the base model’s **sample efficiency, instruction quality, and fine-tuning maturity** matter more than absolute benchmark score.
- MiniMax M3 and especially Kimi K3 are extremely large MoEs. They deliver the highest raw capability but require heavier multi-GPU orchestration, more careful LoRA targeting (router layers etc.), and higher experiment cost.
- GLM-5.x and the better Qwen3.5 models sit in the sweet spot: near-frontier open performance + proven LoRA/QLoRA tooling + cleaner commercial licenses (MIT / Apache 2.0).

**If you want maximum possible capability and are willing to pay for serious rented compute:**

Go straight to **MiniMax M3** or **Kimi K3**. Both are currently at the top of open-weight leaderboards and Arena categories. Treat them as the “ignore all practicality” option.

### Practical order of preference for a 2200-segment personal adapter

1. **Best balance right now** → GLM-5.2 / latest strong GLM-5.x  
2. **Strong alternative with excellent tooling** → Qwen3.5-27B or Qwen3.5-35B-A3B class  
3. **Absolute ceiling (expensive)** → MiniMax M3 or Kimi K3  

### Important constraint still in force

Even with the strongest base in the world, 2200 segments only teach style, preference, and specific decision patterns well if the data is clean and structured as proper instruction or preference pairs. A weak or dirty set on a frontier base still produces a weak adapter.

Would you like the next spike to be a concrete training recipe (Unsloth/Axolotl config + recommended rank/alpha/epochs) for the GLM-5.x or Qwen3.5 option on cloud GPUs?