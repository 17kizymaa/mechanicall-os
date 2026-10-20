# Team: grouped-by--consistency

**Not a Yes.** Agent-agnostic. Any client may read this file. It is not bound to one vendor's chat session. It does not edit `.grok/personas/`. It does not approve.

Days first, oldest day first. Inside a day, relevancy to the prompt, closest first. The sort below is for this prompt: fix pre-apply so the session applies an approved proposal, then put suggestions.toml on the teams. `preflight-log` is not on this team. `before-current` is not on this team.

## 2026-07-10

Review voices. Closer to a prototype than the gate quotes.

- `.grok/personas/architecture-auditor.toml` — shape of the thing being designed.
- `.grok/personas/principles-auditor.toml` — what stays true while the form changes.
- `.grok/personas/icm-auditor.toml` — how a sprint sits in folders.
- `.grok/personas/sidecar-auditor.toml` — sidecars, not a desk shape.

## 2026-10-14

Gate quotes. A quoted row is not a second Next.

- `.grok/personas/decisions-log.toml` quotes `DECISIONS.md`.
- `.grok/personas/proposals-log.toml` quotes the proposal index.
- `.grok/personas/next-selected-log.toml` quotes rows already in `.aether/events.jsonl`.
- `.grok/personas/approve-log.toml` quotes approve reasons.
- `.grok/personas/reject-log.toml` quotes reject reasons.

## 2026-10-20

Closest to this prompt first.

- `ctx/teams/suggestions.toml` — team copy. `aether pre-apply` writes `.aether/suggestions.toml` for one turn. Not a persona. Not a Yes.
- `.grok/agents/coherency.md` sorts this file. Day, then relevancy to the prompt. Not a Yes.

## Copies

Persona sources stay in `.grok/personas/`. This roster does not edit them. The copies of those personas are the other `.toml` files in `ctx/teams/`. `suggestions.toml` is a team file, not one of those persona copies. The sorter is `.grok/agents/coherency.md`. The note is `ctx/teams/suggestions.md`. `preflight-log` is not an agent. The mini-sidecar that sees is `.aether/preflight-see.toml`.
