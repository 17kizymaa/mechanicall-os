# Outlook integration — research boundary

**Status:** research seed only · not a live integration  
**Authority:** only a project `CURRENT.md` may authorize future implementation steps  

## Current state

- Session (or any seat) may contain **notes** under `research/outlook-integration/`.  
- Models may **propose** options (Graph vs IMAP vs add-in), privacy tradeoffs, and reversible steps.  
- Plans should use the **CURRENT.md** schema when negotiating Next.

## Explicitly not implemented (this boundary)

| Action | Status |
|--------|--------|
| Microsoft Graph OAuth | **No** |
| Mailbox credentials / refresh tokens on host | **No** |
| SMTP / send mail from host | **No** |
| Email ingestion / indexing of inboxes | **No** |
| Automatic send or “agent emailed them” | **No** |

## Future implementation gate

Any real Outlook integration requires **all** of:

1. A dedicated project CURRENT with one Next  
2. Separate privacy review  
3. Minimal-permission analysis (delegated scopes)  
4. Explicit test account  
5. Human `aether approve` before each consequential transition  

## Wording

Say **“Outlook integration research”** — not “Outlook connected” or “mail agent.”
