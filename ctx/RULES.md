# CTX rules

- **ctx is shared notes.** It is not CURRENT.md. CURRENT.md at the repo root is the only Yes. ctx does not approve, apply, or replace it.
- **ctx is the shared memory for this spike.** Project knowledge that is not the gate goes into ctx. An agent's private memory holds at most a pointer to ctx.
- **Write only through `ctx`.** Do not edit the store files directly: ctx keeps the lock, the timestamps and the status fields correct.
- **READ means read.** When the operator says READ or READ ONLY, change nothing (ctx, files, version control) until they say WRITE.
- **Sign your own work.** End each session with a one-page summary in `sessions/`, headed with your own name (`**Agent:** <name>`). Set `CTX_AUTHOR` to the same name.
