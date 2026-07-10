# Research: Lowest-Friction Mechanical Setup for Quick Test Protocol

**Protocol (from test-instructions.md and prototype):**
1. Run `./code-review . --output /tmp/review-prompt.md`
2. Log into grok.com with SuperGrok account.
3. Select Grok Heavy / multi-agent mode.
4. Copy entire prompt and paste as first message.
5. Observe multi-agent review against doctrines.
6. Save review as Markdown artifact in target.

**Goal of research**: Lowest-friction mechanical setup (automation of steps 1-4/5). Respect project doctrines (thin, FS, Markdown/Python/sh only, minimal overhead, no heavy frameworks).

**Additional**: Crowd-sourced opinions on similar LLM web-app flows with own domains (flagged as important/relevant).

## Friction Points in Current Protocol
- Manual browser open + login + mode selection.
- Manual copy of potentially very long prompt (thousands of tokens for doctrines + code).
- Context switch terminal <-> browser.
- For repeated tests on different targets: repetitive.
- No automatic "send" (impossible reliably without automation due to consumer web app).

## Lowest-Friction Recommendations (Minimalist, Doctrine-Aligned)
Prioritize zero or stdlib-only additions. No Playwright/Selenium (brittle, heavy deps).

### 1. Clipboard + Auto-Open Browser (Lowest Friction, ~0 extra setup)
Enhance the existing `code-review` script:

- After generating prompt:
  - Detect OS.
  - Copy to clipboard.
  - Open grok.com in default browser.
  - Print: "Prompt copied to clipboard. Paste into Grok Heavy chat (already open)."

Cross-platform snippets (add to prototype):

**macOS**:
```sh
echo "$PROMPT" | pbcopy
open "https://grok.com"
```

**Linux (X11)**:
```sh
echo "$PROMPT" | xclip -selection clipboard
xdg-open "https://grok.com"
```

**Linux (Wayland)**:
```sh
echo "$PROMPT" | wl-copy
xdg-open "https://grok.com"
```

**Windows (Git Bash / MSYS)**:
```sh
echo "$PROMPT" | clip
start "https://grok.com"
```

Add a `--no-browser` flag. Make it the default in consumer mode.

**Community validation**: Common pattern in terminal-to-LLM tools (ChatGPT CLI wrappers, etc.). Very low friction once in PATH.

### 2. Local Web UI (Slightly Higher Setup, Much Better UX for Review)
Use Python stdlib only (`python -m http.server` + single HTML/JS file).

- Script generates prompt, writes to a temp dir.
- Starts a local server on http://localhost:8765
- Serves a simple page:
  - "Review Prompt for [target]"
  - Big "Copy to Clipboard" button (JS navigator.clipboard).
  - "Open grok.com in new tab" button (opens https://grok.com).
  - Instructions: "Log in with SuperGrok → select Heavy → paste".
  - Optional: "Download prompt.md".

Run with `./code-review . --web` or auto.

This is "mechanical" (scripted) and can be bookmarked or turned into PWA-ish.

For even lower daily friction: alias or add to shell.

### 3. Browser Extension / Userscript (If User Already Uses One)
- Tampermonkey/Greasemonkey script on grok.com that adds a "Paste from local" button or listens for clipboard.
- Or a simple extension that watches a local file/clipboard.

**Friction**: One-time install. Good if repeated often.

### 4. Launcher Integration (Raycast, Alfred, etc.)
- For Mac users (common in dev): Create a Raycast command/script that runs the code-review and handles clipboard+open.
- Community loves this for "from anywhere" LLM flows.

Avoid full automation of paste/send (login cookies, selectors break, against "thin").

**Overall Lowest Friction Setup Recommendation**:
1. Update prototype to do OS-aware clipboard + open grok.com.
2. Add `--web` mode with stdlib local server + HTML UI (single file).
3. Document `DOCTRINES_BASE` and make script find doctrines relative to repo root reliably.
4. Optional: symlink the script to ~/bin/code-review and add to PATH.
5. For repeated: hotkey in terminal multiplexer or launcher.

This keeps everything `cat`-able, no new deps, respects minimalism.

## Crowd-Sourced Opinions on Similar LLM Web-App Flows with Own Domains

I researched via web (Reddit/selfhosted, Product Hunt implied, blogs, YouTube, indie discussions). Flagged important/relevant below. Focused on:
- Custom/self-hosted LLM chat UIs.
- Flows involving copy-paste or automation from local/tools into web LLM (esp. consumer tiers).
- Deploying on own/custom domains/subdomains.
- Low-friction patterns (clipboard, local servers, embeds).
- Opinions on using consumer subscriptions vs API in custom setups.
- Relevance to "own domain" + doctrine-like custom prompts/reviews/agents.

### Highly Relevant / Flagged
1. **AnythingLLM** (Mintplex Labs)
   - Self-hosted + cloud. Embeddable AI chatbot widget (single HTML snippet) for any website.
   - Deploy on own domain easily. Supports RAG from local files/docs.
   - Community (YouTube, their site, PH mentions): Praised for quick "add AI to my site" without heavy code. "Embed takes minutes". Good for custom branded flows on own domain.
   - Relevance: Similar to generating "prompt" but for persistent chat. Low friction for end-users. People use for internal tools on custom subdomains. Has collection/indexing similar to our .context.md awareness.
   - Opinion: Positive for no-code/low-friction. Self-hosted version free/open. Cloud for ease.

2. **Open WebUI** (formerly Ollama WebUI) + LibreChat
   - Top self-hosted LLM frontends (Reddit selfhosted, "Top 5 Local Hosted AI Frontends" lists).
   - Docker one-click. Full custom domain via reverse proxy (Nginx/Caddy/Cloudflare).
   - Support multiple providers (OpenAI compat — can point at Grok API key if using paid).
   - Features: file uploads, RAG, multi-user, custom prompts/presets.
   - Community opinions (Reddit r/selfhosted, blogs): "Best looking and functional". Loved for privacy, running on home lab/VPS with own domain. "Host your own private AI chatbot" videos show custom domains (e.g., blog.parametric.camp).
   - Relevance: Exactly "LLM web-app with own domain". People complain about copy-paste friction for large contexts → value file upload and persistent chats. For consumer Grok: limited (most use API keys or local models). Many run alongside grok.com.
   - Important flag: Strong for "mechanical" self-host. Minimal Docker setups align with our thin philosophy. Crowds love it for cost control vs pure cloud.

3. **Self-hosted patterns in blogs/YouTube (KoboldAI, Jan AI, etc.)**
   - "Self-hosting an AI LLM chatbot without going broke" — discusses KoboldAI + custom setups.
   - "Host your Own Private AI Chatbot" — deploys on personal domain.
   - "Ultimate Self-Hosted AI LLM Cluster" — Docker compose for multiple backends, free/private.
   - Opinions: High praise for control and custom domain access ("browser chat dot mydomain"). Complaints about local hardware needs; many prefer hybrid (own UI + cloud models via key).
   - Relevance: Low-friction local generators feeding into web UIs or direct. People build "prompt to my custom agent" flows.

4. **Embed/Custom Widget Approaches (AnythingLLM, Ethora, etc.)**
   - "Custom AI Chatbot for Websites using any LLM | No-Code".
   - Deploy embed on own domain/site.
   - Opinions (PH-style, videos): "Unleash power of local LLMs with Ollama + AnythingLLM". Good traction for indie makers wanting branded AI on their domain without full rebuild.

### General Crowd Opinions on Friction & Own Domain Flows
- **Clipboard / terminal-to-web pain**: Common. Many CLI wrappers for ChatGPT/Grok do exactly pbcopy + open. People want "one command to send large context to my LLM".
- **Own domain wins**: Privacy, branding, no vendor lock, easy with free tiers (Vercel/Netlify for frontend, cheap VPS/Docker for backend). Indie hackers report good feedback when customers get "chat.yourdomain.com".
- **Consumer subscription vs custom UI**: Many note that for free/included rates (like SuperGrok), you stick to official web. Custom UIs almost always require API keys (separate billing). Browser automation scripts exist but "brittle". Hybrid (local generator → official web) is mentioned as practical.
- **Self-hosted popularity**: Very high in r/selfhosted, r/LocalLLaMA. Tools like OpenWebUI get "why pay OpenAI when I can self-host". For closed models like Grok: "use API key in the UI".
- **Crowd-funded / Indie traction**: These are mostly open-source with community (sponsorships, hosted paid versions). PH launches of similar (AnythingLLM mentions) get upvotes for ease. Indie Hackers threads praise "bring your own domain" for perceived professionalism.
- **Important flags for us**:
  - AnythingLLM and OpenWebUI stand out for low-friction custom domain + prompt/context handling.
  - For our case (consumer Grok rates + doctrines): Best to enhance clipboard/local UI rather than full self-hosted backend.
  - Avoid heavy frameworks (matches our doctrines — many self-hosted use Docker but core is simple).
  - Opportunity: Our prompt generator + local web UI could be "the missing piece" for feeding doctrine-rich reviews into Grok Heavy without API spend.

## Proposed Lowest-Friction Implementation for This Project
- Update `code-review` prototype with clipboard + open logic (OS detection, fallbacks).
- Add `--web` / default local server mode using pure Python (http.server + one HTML file with buttons).
- Make it discoverable (e.g., `aether review` integration later? but keep thin).
- Document deployment of a static version of the UI to user's own domain (for sharing the generator if desired), while generation stays local for FS access.
- Test protocol becomes: `./code-review . --web` → browser opens localhost page → one-click copy + open grok.com.

This is mechanical, minimal, and directly reduces the outlined friction.

Further research (if needed): specific Raycast recipes, Playwright examples for grok.com (flagged as higher friction).

Sources synthesized from web searches on self-hosted LLMs, custom domains, terminal-to-LLM flows.
