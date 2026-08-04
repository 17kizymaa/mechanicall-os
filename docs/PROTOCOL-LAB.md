# Protocol Lab

**Status:** design + local commands  
**Primary surface:** operator terminal / **Grok Build** (not the website)  
**Web:** optional literacy (`anphuni.com/protocol`) — copyable commands only  
**Session:** capped ≤5-seat **hosted lab**, not this Lab and not core product  

## Loop (first 20 lines contract)

**action → bind → probe**

1. **Name** an action-id you want to try.  
2. **Bind** it as Next only via human CURRENT edit or after APPROVED `aether next`.  
3. **Probe** whether preflight would allow it **right now** (read-only).

```bash
./aether probe <action-id>          # exit 0 allow, 2 refuse — never mutates CURRENT
./aether preflight <action-id>      # same gate, writes an event
./aether approve "…"                # human only
./aether next <new-id>              # after APPROVED
./aether demo                       # full refuse→allow→approve→next in temp root
```

## External TUI caveat

If you work in Grok Build, preflight is **not** automatic. Run `./aether brief` at start; use `./aether drift` after big edits. See `docs/GROK-SEAT.md`.

## What this is not

- Not multi-tenant SaaS  
- Not “Session seats are the product”  
- Not a sandbox that forces Grok to preflight  
