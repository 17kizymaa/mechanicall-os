# Discovery — people app as an ICM workspace

**When:** 2026-08-18  
**Choice:** option 1 — Mechanicall law + Jake’s factory  
**Operator Next (unchanged):** `mobile-planning-demo`  
**This folder:** factory only. Not a second Next. Not Play Store. Not OpenHands-as-architecture.

## Who it is for

A person who has a **folder of work** and wants an agent to do the pointing-and-clicking. They will not learn `aether`. They will not SSH to your LAN. They copy (or open) a workspace, say what the folder is, and walk stages. They tap **Yes** when the plan would change.

Not for: multi-tenant SaaS, swarm consoles, mum-in-the-room on a cancelled sitting, Hyprland rice.

## What “useful” means here

PRODUCT pitch, still: *You decide. AI does the point-and-clicking — under a plan you can read and a yes only you can give.*

Jake’s version of that: the **workspace is the app**. Numbered folders are the control flow. `output/` is the review surface. One agent reads the right files.

Mechanicall’s extra (keep): that person’s **project folder** has a `CURRENT.md`. Yes = apply a PROPOSE + `aether approve` in *that* folder. Models never write CURRENT. Silence is not Yes.

Failed casual bet (`docs/SINGLE-APP-DISTRIBUTION.md`): do not make the front door a CLI.

## What we take from Jake

- One agent, not a swarm
- Stages with Inputs / Process / Outputs
- Human edit of `output/` before the next stage
- Layered load (do not dump the repo)
- Factory configured once; each run is new Layer 4
- Where ICM **does not** work: real-time multi-agent, high concurrency, fat automated branching — so we do not start from OpenHands/swarm

## What we keep from Mechanicall

- `CURRENT.md` + preflight + human approve in the **bound project**, not in this factory
- Refuse if they bind the operator `mechanicall-os` tree
- Events / DECISIONS as receipts
- Pocket demo and `:8765` stay **lab**

## What the factory will emit (later stages)

A **copyable workspace** (not a store listing) whose stages are the people loop, roughly:

1. Bind a folder that is not this repo  
2. Show / init CURRENT in that folder  
3. Agent works only under that Next (writes PROPOSE, code, notes)  
4. Human Yes / Not yet  
5. Leave a receipt they can open tomorrow  

The workspace is the app. Docker/OpenHands, if they appear later, are **one runner** for that agent — not the product name.

## Honest limit this week

Live law still forbids calling the phone spike the people product. This discovery does not ship. Mapping (02) names stages. Scaffolding (03) writes empty tree. You still must `aether next` if you want this factory to *be* the operator Next.

## Checkpoint

Edit this file if the user is not “person with a folder.” Then say **proceed to 02**.
