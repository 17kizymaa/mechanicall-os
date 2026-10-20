# Compact — new-apk-sprint-start

Not a Yes. Live Next is `new-apk-sprint-start`. Phase APPROVE. Status APPROVED. Approval APPROVED.

## Reason

We should get back to what we was doing - 'aether' CLI is something confident enough to scaffold off of in terms of the modelling work.

## Where this halt stops

`dev/87_new-apk-sprint-start/output/SCAFFOLD.md` is the modelling scaffold. It names the CLI surface and the pin. It is not an assemble script.

`aether pre-apply` approves one turn of the visible conversation session. That session is the suggestion. An approved proposal is applied for that session. The verb writes `.aether/suggestions.toml`. The team copy is `ctx/teams/suggestions.toml`. A hidden session writes nothing and applies nothing. The model does not run `pre-apply`.

versionCode stays 46. Pin cksum stays `3532677481`. Weight stays outside the APK. The next assemble is parked as `apk-sprint`.

## Client rows

One script, `/home/anphuni/.aether/current-statusline.py`, prints `Next · Phase / Status / Approval`.

| Client | What is wired |
|---|---|
| Grok | `~/.grok/statusline.sh`. Restart Grok. Hidden in minimal mode. |
| Claude Code | Existing GSD row kept. CURRENT is a second line via `~/.claude/hooks/aether-current-statusline.sh`. |
| Antigravity | `statusLine.command` in `~/.gemini/antigravity-cli/settings.json`. Restart `agy`. |
| Copilot CLI | Settings and script written. The binary is not installed, so the row was not shown. |
| Codex CLI | Script only. No command hook in Codex. Not installed. |
| Gemini CLI | Script only. `/footer` cannot run it. The binary is not installed. |
| OpenCode | Script only. No status hook in the installed plugin package. Not on PATH. |
