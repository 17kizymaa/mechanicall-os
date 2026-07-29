# Client-one — Session two handoff (House Desk)

**Branch:** `session/client-one-s2-proposal-assistant`  
**Same client:** Delroy / house stack (eME640 + LG + Fire Stick + myarch Desk)  
**Speed:** less ceremony; CURRENT-as-product continues; personal-llm as technique when operator sets Ollama  

## Depends on personal-llm accept

Operator must review and accept:

`/home/anphuni/MODEL+RAG/personal-llm/artifacts/PROPOSE-CURRENT-SESSION-TWO.md`

Until then, personal-llm CURRENT remains Kingston validation Next.

## Session-two intent (client surface)

- Keep Desk: chat + CURRENT rail, propose only  
- Steer proposals toward **this client’s** real goals (entertainment preview→accept, house helper, future myarch→LG stream)  
- Optional later: proposal assistant interjections (PROPOSE-*.md) from personal-llm technique  
- Do not auto-play media; LG stream design remains research until CURRENT Next says so  

## Launch

```bash
cd /home/anphuni/mechanicall-os
git checkout session/client-one-s2-proposal-assistant
aether desk-serve --lan --port 8788 domains/house-tv-desk
```

## Devices (reminder)

| IP | Role |
|----|------|
| 192.168.1.241 | myarch Desk backend |
| 192.168.1.235 | eME640 Client box |
| 192.168.1.179 | LG TV (standby often) |
| 192.168.1.189 | Fire Stick |

## Audit attach (phone)

`dev/11_aether-desk-android-tv/SESSION-AUDIT-2026-07-28-PHONE.md`
