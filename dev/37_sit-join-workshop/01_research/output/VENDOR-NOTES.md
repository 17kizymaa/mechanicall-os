# VENDOR-NOTES — document workshop + Tailscale userspace

**Not CURRENT. Not Decide.** Research for `sit-join-workshop`. CURRENT law outranks vendor taste.

## Steal (interaction)

### Google Docs Suggesting
Source: [Suggest edits in Google Docs](https://support.google.com/docs/answer/6033474).

- Mode switch: Editing vs **Suggesting**. Suggesting does not replace the original until the owner accepts.
- Marks: new colour for inserts; strikethrough for deletes; optional comment on a suggestion.
- Accept/Reject **one by one** (comment card) or **Accept all / Reject all** (Tools → Review suggested edits) with a **preview** of with/without changes.
- Mapping: **Plan** = published doc (Editing is off). **Draft** = Suggesting on a **copy** (`PROPOSE-CURRENT.md`). Accept/Reject mutates the copy only. **Decide** = the owner’s publish (Docs has no second file — we do, on purpose).

Do **not** steal: Google login, Drive-as-authority, “accept writes the only doc.”

### Word Track Changes
Source: [Accept or reject tracked changes in Word](https://support.microsoft.com/en-us/word/accept-or-reject-tracked-changes-in-word).

- Review tab: Accept / Reject **moves to the next change**.
- Hover preview of what accept/reject would do.
- Accept all exists — too close to Yes if it wrote CURRENT. Allowed only as “accept all remaining hunks **into PROPOSE**.”
- Mapping: hunk cursor + Accept/Reject + next. Why stays on Decide, not on hunk.

### Overleaf Track Changes
Source: [Track changes](https://docs.overleaf.com/collaborating/track-changes).

- Mode: Editing vs **Reviewing**. Reviewer role cannot switch to Editing.
- Accept/reject **selected** changes; confirm pop-up.
- **Copy of project auto-applies all tracked changes** — warning: a duplicate is law-shaped. Matches our Reject of zip/syncthing (S12).
- Mapping: Draft is Reviewing; Plan is the published file; never “copy applies.”

### HackMD Suggest edit
Source: [How to Raise a Suggest Edit](https://hackmd.io/c/tutorials/%2F%40docs%2Fsuggest-edit-en) (select span → Suggest edit → edit the selection).

- Markdown-native. Closest file format to CURRENT.md.
- Span-scoped proposal, not whole-file rewrite.
- Mapping: hunk = selected heading/section; 7B must stay in that span (S11).

## Steal (Tailscale component)

### Userspace networking
Source: [Userspace networking](https://tailscale.com/docs/concepts/userspace-networking) (validated Nov 2025).

- `--tun=userspace-networking`: no TUN device; SOCKS5/HTTP proxy for **this process**.
- Auth via `--auth-key` (ephemeral nodes recommended). **Key never in git / never baked in APK.**
- tsnet (Go): embed a node with gVisor userspace stack; no root; dial/listen on tailnet from-process. [tsnet](https://pkg.go.dev/tailscale.com/tsnet).

### Android honesty
- Official Tailscale Android app = **VpnService** (device-wide). GitHub [issue #10126](https://github.com/tailscale/tailscale/issues/10126): userspace mode on the **official Android client** is a feature request, not a shipped toggle.
- This Next’s S10c (userspace in **Mechanicall**) is therefore **embed tsnet/libtailscale in-process**, not “flip a switch in Tailscale’s app.” Dial Ollama/wol-pi through the userspace stack (SOCKS or tsnet `Dial`). Other apps stay on LTE.

## Do not steal
- ChatGPT canvas / bubbles (Rejected identity).
- Devin / OpenHands as the sitter face.
- Funnel, public `:11434`, public `/wake`.
- Accept-all that writes live CURRENT.
- Drive / Docs API as the store.
