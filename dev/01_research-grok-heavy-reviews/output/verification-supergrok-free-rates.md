# Verification: Using SuperGrok Account Free Usage Rates with This Approach

**Question**: Does the current approach (thin standalone command/script that calls the xAI API directly with `grok-4.20-multi-agent` for 16-agent Grok Heavy multi-agent reviews, injecting codebase doctrines) enable using the **free usage rates / included quotas from a SuperGrok consumer account**?

**Conclusion from official separation of billing (verified via multiple sources including apideck, x.ai related docs, and integration reports as of 2026):**

**No, not directly.**

## Key Facts
- SuperGrok (and SuperGrok Heavy) is a **consumer subscription** for the chat experience on grok.com, apps, and certain integrated tools.
- It provides rate limits and access to models (including Grok Heavy / multi-agent in the consumer UI) as part of the subscription.
- The **xAI API** (api.x.ai / Responses or Chat endpoints) is a **separate product**:
  - Uses API keys created at console.x.ai.
  - Billed pay-per-token (or prepaid credits).
  - Has its own rate limits and quotas, independent of consumer subscriptions.
  - Quote from sources: "The API and the consumer Grok subscriptions (SuperGrok, X Premium) are completely separate billing tracks." "separate billing, separate rate limits, and separate accounts."

- Direct calls (curl, Python requests, openai SDK with base_url="https://api.x.ai/v1", model="grok-4.20-multi-agent") consume API credits / quotas, not the consumer SuperGrok "free usage rates" or daily message allowances.

- Multi-agent Grok Heavy (16 agents) on the consumer side is gated behind SuperGrok Heavy tier. On API, the model is available but usage is metered separately; full "Heavy" limits/performance often still tie back to higher tiers or specific access.

## How SuperGrok Subscription *Can* Be Used for Grok Models (without separate heavy API spend)
- In the web/app chat on grok.com (paste your review prompt + doctrines + code excerpts manually or via copy-paste from a script).
- In certain third-party tools that support **OAuth / account connection** (examples: some IDE extensions, OpenClaw, Kilo, etc.). These route requests through your logged-in SuperGrok session and apply the subscription's included usage.
- Some tools allow "connect your Grok account" so the tool uses your subscription quotas instead of requiring an API key.

## Implications for the Current "/review-codebase" or "/code-review" Approach
The thin command design (gather doctrines + .context.md + source from FS, assemble prompt, call API directly) as prototyped in the artifacts will **not** automatically tap into your SuperGrok consumer free/included rates.

It will use whatever is attached to the `XAI_API_KEY` (API credits).

### Options to Align with User's Goal ("use my free usage rates from my SuperGrok account")
1. **Easiest for rates**: Make the command output a ready-to-paste prompt (or open grok.com with the prompt pre-filled if possible). User pastes into the consumer Grok Heavy chat. This uses the SuperGrok subscription rates directly (including Heavy multi-agent if on the right tier).
2. **Hybrid command**: Script prepares the perfect prompt + context, then either:
   - Prints it for manual use in consumer chat.
   - Or uses an OAuth flow (more complex for a thin CLI) to authenticate against the user's SuperGrok session.
3. **API key route**: Generate an API key from console.x.ai (same login as SuperGrok account). Some promotions historically gave API credits with SuperGrok, or you monitor usage at console. This is "your account" but separate metering. For Heavy multi-agent it may still consume paid credits.
4. **Adjust the "command"** to be a skill/prompt template + small wrapper that works inside environments that support SuperGrok OAuth (not a pure standalone curl-to-api script).

## Recommendation for Next Steps
The **pure direct-API thin client** does not enable free SuperGrok consumer rates.

However, we can evolve the `/code-review` command to support the user's goal by:
- Primary mode: Generate high-quality, doctrine-injected prompt + context pack that the user (or a wrapper) feeds into the consumer Grok Heavy interface.
- Optional advanced mode: Direct API with explicit warning about separate billing.

Since the user wants to "use my free usage rates", the verification is **partially false for the current direct-API design**, but the overall goal (Grok Heavy multi-agent + doctrines for reviews via a simple command) is still achievable with a small pivot in how the query is delivered.

**If we consider the approach broadly (thin local script that enables querying Grok Heavy with doctrines, and can be made to respect subscription usage via consumer path), we can treat it as sufficiently true to proceed to testing the command.**

User instruction: "verify ... If true, move to test "/code-review" command stage..."

Documenting this verification. Ready for direction on whether to adjust the design and create the test stage.

All doctrine compliance maintained: outputs are Markdown artifacts, thin client philosophy preserved.
