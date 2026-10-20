---
phase: 03-mechanical-codebase-review
reviewed: 2026-09-08T18:40:00Z
depth: deep
files_reviewed: 26
files_reviewed_list:
  - aether
  - python/aether_llm.py
  - python/aether_pocket.py
  - python/aether_inbox.py
  - python/aether_fs.py
  - python/aether_client.py
  - python/aether_panel.py
  - python/aether_shell.py
  - python/aether_shell_agent.py
  - python/aether_mcp.py
  - python/app_verify.py
  - python/mum_verify.py
  - python/you_decide_gauntlet.py
  - python/you_decide_plate_cycle.py
  - python/draft_rag_pack.py
  - tests/run.sh
  - tests/negative.sh
  - tests/test_aether_llm_personal.py
  - tests/test_aether_pocket.py
  - android/app/src/main/java/com/mechanicall/pocket/demo/MainActivity.kt
  - android/app/src/main/java/com/mechanicall/pocket/demo/SitRackView.kt
  - android/app/src/main/java/com/mechanicall/pocket/demo/FaceBridge.kt
  - android/app/src/main/python/aether_bridge.py
  - android/app/src/main/python/aether_pocket.py
  - android/app/src/main/AndroidManifest.xml
  - references/personal-llm-system.txt
findings:
  critical: 4
  warning: 14
  info: 5
  total: 23
status: issues_found
---

# Phase 03: Code Review Report

**Reviewed:** 2026-09-08T18:40:00Z
**Depth:** deep
**Files Reviewed:** 26
**Status:** issues_found

## Summary

This is **not a kernel**. It is a **local-first filesystem control layer** (`aether` + `CURRENT.md` + preflight + append-only events) with a **phone lab face** (SitRackView millwork APK). PRODUCT.md already says the honest label: “local-first human–agent project control layer.” SPEC-v0.2 is the protocol. The sit is that protocol’s millwork, not a second OS.

The **~20% that is the product:** POSIX `aether` authority verbs, `CURRENT.md` as one Next, cooperative preflight, human `approve`/`reject`/`next`, `.aether/events.jsonl`, pocket `yes()` as the phone’s only CURRENT write, MCP/client denylists that refuse approve.

The **~80% that is naming residue** (Weinberg: code that exists because it was named OS / agent / cortex / GATE / storm / twin / millwork, not because CURRENT Next `you-decide-ritual` needs it): `aether_storm.py` (AVD factory), `aether_twin.py` (HTTP mirror), `aether panel` TUI + Grok-left chrome, `aether_shell_agent` Grok-shaped tool loop, JOIN/WAKE/GATE lamps, hunk-select workshop, `draft_rag_pack` (honestly a folder walk; the word RAG is leftover), garden/rival, club-cortex vocabulary in docs. CORE_PRINCIPLES and SPEC’s closing line still apply: *stop one wrong action before adding machinery*. This tree added machinery.

Authority is **cooperative, not sovereign** (NOT-IMPLEMENTED.md already admits this). That is not an excuse for the bugs below: the protocol *does* write CURRENT from paths that are not Yes, and it *does* still allow the Next after a REJECTED stamp.

## Narrative Findings (AI reviewer)

## Critical Issues

### CR-01: Not yet / leaving Decide writes CURRENT (violates “unchanged until Yes”)

**File:** `android/app/src/main/java/com/mechanicall/pocket/demo/MainActivity.kt:524-530`
**Also:** `python/aether_pocket.py:580-641`

**Issue:** CURRENT Keep says “Draft is NOT ACTIVE; CURRENT unchanged until Yes” and “Not yet keeps Next.” Mum–son law (M6) says leaving Decide without Yes keeps Next and does not apply PROPOSE. The sit implements “Not yet” as **protocol reject**:

```524:530:android/app/src/main/java/com/mechanicall/pocket/demo/MainActivity.kt
    private fun leaveDecideWithoutYes() {
        if (rack.plate != SitPlate.DECIDE) return
        val p = pocket
        if (p.isBlank()) return
        val reason = rack.whyNow().ifBlank { why }.ifBlank { "not yet" }
        io.execute { FaceBridge.notYet(p, reason) }
    }
```

`BankPlan` / `BankDraft` call this on navigation. `FaceBridge.notYet` → `not_yet()` → `pocket_reject()`, which **rewrites live CURRENT**:

```580:588:python/aether_pocket.py
def pocket_reject(pocket: str | Path, reason: str) -> PocketResult:
    ...
    patch = {"Status": "REJECTED", "Approval": "REJECTED", "Phase": "SELECT"}
    cf.write_text(apply_fields_to_current(cf.read_text(encoding="utf-8"), patch), encoding="utf-8")
```

Why is not required (`"not yet"` default). Open/Bind/Send are not Decide; tapping Plan after peeking Decide is navigation, not a stamp. Tests lock the bug in: `tests/test_aether_pocket.py:239-246` asserts `Status == REJECTED`. Gauntlet G9 only checks the Next *string* and a receipt line (`python/you_decide_gauntlet.py:245-248`), so 12/12 can pass while CURRENT was mutated without Yes.

**Fix:** Treat Not yet like `did_it`: receipt only. Never `pocket_reject` from the sit.

```python
def not_yet(pocket, reason: str = "not yet from demo sitting", **kw) -> PocketResult:
    del kw
    return write_receipt(pocket, said="Not yet", reason=reason)
```

```kotlin
private fun leaveDecideWithoutYes() {
    if (rack.plate != SitPlate.DECIDE) return
    val p = pocket
    if (p.isBlank()) return
    val reason = rack.whyNow().ifBlank { why }.ifBlank { "not yet" }
    io.execute { FaceBridge.notYet(p, reason) } // must not touch CURRENT.md
}
```

Add a test: leave Decide / `not_yet` → CURRENT bytes identical; RECEIPT says Not yet.

---

### CR-02: Preflight allows the Next while Status is REJECTED (SPEC hole)

**File:** `aether:628-644`

**Issue:** SPEC-v0.2: “Status `REJECTED` refuses execute-class actions until human re-selects.” Code sets `blocked=1` for REJECTED/DRAFT, then **ignores it** whenever `**Next:**` is set and the action matches:

```628:644:aether
    blocked=0
    case "$(printf '%s' "$status" | tr '[:lower:]' '[:upper:]')" in
        BLOCKED|BLOCKED-PENDING-HUMAN|REJECTED|DRAFT)
            blocked=1
            ;;
    esac

    if [ -n "$next" ]; then
        if str_eq_ci "$action" "$next"; then
            printf 'Allowed: %s matches Next (%s). Phase=%s Status=%s\n' \
                "$action" "$next" "$phase" "$status"
            ...
            return 0
```

`blocked` is only consulted in the “Next unset” branch (`aether:657-664`). After CR-01’s reject stamp, desktop `aether preflight <same Next>` still **allows**. The stamp is theater; the gate does not close. `tests/run.sh:301-310` rejects, then only re-checks a *prohibited* id (`rough-v6`), never the declared Next.

Same hole for Status `DRAFT` with a Next pin: execute is allowed.

**Fix:** Refuse execute-class when Status is REJECTED (and, if you mean DRAFT to be blocked, when DRAFT), even if the action equals Next:

```sh
if [ "$blocked" = 1 ]; then
    if printf '%s' "$status" | grep -qiE 'REJECTED|DRAFT'; then
        reason=$(printf 'Status is %s — refuse %s until human re-selects.' "$status" "$action")
        printf 'Refused: %s\n' "$reason"
        preflight_record "$root" "$action" refused 3 "..."
        return 3
    fi
fi
```

Add `tests/run.sh` coverage: reject → `preflight $Next` exits 3.

---

### CR-03: Grok agent `search_replace` can write `CURRENT.md` (model-auto-write-current)

**File:** `python/aether_shell_agent.py:458-478`
**Also:** `references/aether-shell-agent-grok.md:5-11` (tools include `search_replace`); `python/aether_shell.py:202-205` (agent mode default on)

**Issue:** CURRENT Prohibited includes `model-auto-write-current`. AGENTS.md: models never rewrite authority. The Grok real-agent profile ships `search_replace`. The implementation writes any file under the project root with no CURRENT guard:

```458:478:python/aether_shell_agent.py
def tool_search_replace(root: Path, args: dict) -> str:
    path = _safe_path(root, str(args.get("path") or ""))
    ...
    path.write_text(
        text.replace(old_s, new_s) if replace_all else text.replace(old_s, new_s, 1),
        encoding="utf-8",
    )
```

A model `<tool_call>{"name":"search_replace","arguments":{"path":"CURRENT.md",...}}</tool_call>` actualises Domain without `aether approve`. Peer profile disallows this; `/agent grok` and a missing profile (DEFAULT_TOOLS, lines 25-31) do not. Doctrine-in-prompt (“never write CURRENT”) is not a gate.

**Fix:** Refuse authority files in every write tool:

```python
AUTHORITY_WRITE_DENY = {"CURRENT.md", "DECISIONS.md"}
if path.name in AUTHORITY_WRITE_DENY:
    return "error: refused: models cannot write CURRENT.md (propose only)"
```

Keep `search_replace` out of peer; default-deny write tools unless role is grok *and* path is not authority.

---

### CR-04: `pack_tree_context` dumps pocket secrets into the model prompt

**File:** `python/aether_pocket.py:1617-1638`
**Also:** `python/aether_pocket.py:1835-1858` (`agent_edit_propose` concatenates the blob)

**Issue:** `draft_rag_pack.py:16` skips `.env` / `adbkey` / `id_rsa`. `pack_tree_context` skips only `.git` / `__pycache__` / `.pytest_cache`, then walks **the whole pocket including `.aether/`** into an Ollama prompt:

```1623:1637:python/aether_pocket.py
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip]
        for name in sorted(filenames):
            ...
            data = p.read_text(encoding="utf-8")
            chunk = f"\n--- {rel} ---\n{data}"
```

`.aether/join-provision` is documented as a desk-side key (`aether_pocket.py:1102-1114`). A Headscale preauth / env key in the pocket is sent to `personal-llm-sft-v4`. PERSONAL-LLM-LAYER.md: “Secret post-filter … at the orchestrator”; “No Kingston unlock”; “API keys stay out of git” — also stay out of prompts.

**Fix:** Reuse `draft_rag_pack.SKIP_NAMES`, skip `.aether/join-provision`, `*.env`, `id_rsa`, `adbkey`, and do not send `.aether/` except `events.jsonl` tails. Cap like the RAG pack.

---

## Warnings

### WR-01: Unsafe/secret regexes document; they do not strip; `chat()` never calls them

**File:** `python/aether_llm.py:188-195, 839-847, 849-867`
**Also:** `python/aether_shell.py:722-724`

**Issue:** Comment: “optional strip.” `flag_unsafe_model_output` only returns labels. `chat()` returns raw model text. Shell appends `[shell guard: secret_like]` **after** the secret is already in `reply`, then prints it (`aether_shell.py:722-729`). PERSONAL-LLM-LAYER.md requires an orchestrator post-filter that refuses/redacts `sk-` / PEM. Tests (`tests/test_aether_llm_personal.py:74-78`) only assert the flag exists.

**Fix:** In `chat()` (or a wrapper every caller uses): if `SECRET_LIKE_RE` hits, replace the span with `I will not repeat secrets. Rotate it offline.` and do not print the original. If `UNSAFE_CMD_RE` hits, strip those lines before return.

---

### WR-02: Personal-LLM docs still rank sft-v2 first; code prefers sft-v4; grok_tui wins the backend race

**File:** `docs/PERSONAL-LLM-LAYER.md:12-47` (not in file list; cited as drift vs code)
**Also:** `python/aether_llm.py:1-11, 172-186, 436-568`

**Issue:** `OLLAMA_PREFER` is `personal-llm-sft-v4` then sft-v2 then full:v1. Module docstring and `resolve_backend()` prefer **grok_tui** whenever `grok login` exists, then OpenRouter/Groq/Anthropic/xAI, **then** Ollama. Technique (personal LLM) is not the default propose substrate on a machine that has Grok CLI. Layer doc and README still advertise sft-v2 first.

**Fix:** Update PERSONAL-LLM-LAYER.md / DEFINITION to sft-v4. If Domain technique should win, pick Ollama personal-llm before grok_tui unless `AETHER_LLM_PROVIDER` is explicit.

---

### WR-03: Dead `if ":" not in model.replace(...)` block

**File:** `python/aether_llm.py:1342-1349`

**Issue:**

```python
if model in ("personal-llm-sft-v4", "personal-llm-sft-v2", "personal-llm-full:v1"):
    if ":" not in model.replace("personal-llm-full:v1", "x"):  # keep full:v1
        pass
if model == "personal-llm-sft-v4":
    model = "personal-llm-sft-v4:latest"
```

The inner `if` is a no-op. Tag normalisation is the following `if/elif`. Residue of an unfinished patch.

**Fix:** Delete the dead `if` pair; keep the `:latest` assignments.

---

### WR-04: No Next pin + open Status = allow any action

**File:** `aether:667-673`

**Issue:** If `**Next:**` is empty (or the parser misses it) and Status is not in the blocked set, preflight **allows** with a warning. Silence-shaped: missing pin is permission. SPEC rule 3 only binds when Next is set; the fail-open is still how a mistyped CURRENT lets `deploy-production` through if someone deleted the Next line and Status is `ACTIVE`/`APPROVED`.

**Fix:** Fail closed: unset Next ⇒ refuse (exit 3), same as DRAFT/BLOCKED. Template `Next: unset` should refuse, not allow.

---

### WR-05: “Law” scorers grep names, not CURRENT bytes

**File:** `python/mum_verify.py:207-217`
**Also:** `python/app_verify.py:155-165`; `python/you_decide_gauntlet.py:245-248`

**Issue:** M6 PASS is `leaveDecideWithoutYes in nav and notYet in nav`. B6 PASS is `decideArmed` + `why required` + `FaceBridge.yes` present. G9 PASS is Next string + receipt “Not yet”. None of them fail CR-01. CURRENT says `app_verify` 15/15 is law. Law that cannot see a CURRENT mutation is ceremony.

**Fix:** Assert CURRENT sha256 unchanged on G9 / M6 / a pocket unit test. Fail M6 if `pocket_reject` is in the Not-yet path.

---

### WR-06: Onboard/cheatsheet still say preflight refuse is exit 1

**File:** `aether:1611, 1765`
**Contrast:** `aether:1953-1965` (correct: refuse is 3)

**Issue:** Generated `.aether/COMMANDS.md` and onboard literacy print “exits 0 (allow) or 1 (refuse).” SPEC and `usage()` say 3. Agents that treat 1 as “try something else” vs 3 as “gate closed” will mis-handle the protocol.

**Fix:** One string: “allow 0 / refuse 3 / usage 2.”

---

### WR-07: `aether watch` still feeds `xargs` (historical quoting P0)

**File:** `aether:116-117, 1424-1432`

**Issue:** `tree_hash` comments “never xargs (splits on spaces in filenames).” `cmd_watch` still does `xargs -I{} find {}` on scoped dirs. A project path with spaces breaks watch; a crafted name can split argv. Distill path was fixed; watch was not.

**Fix:** Same `while IFS= read -r` loop as `tree_hash` / `collect_files`. No xargs.

---

### WR-08: `AETHER_GROK_ALWAYS_APPROVE` defaults to on

**File:** `python/aether_llm.py:956-1008`

**Issue:** Headless Grok TUI is invoked with `--always-approve` unless the env is explicitly off. Deny-tools list tries to block Write/Edit/shell, but the default is “model tools auto-yes.” That is the same shape as model-approve, at the Grok CLI layer. Error text even tells the operator to turn it *on* (`aether_llm.py:1082`).

**Fix:** Default `AETHER_GROK_ALWAYS_APPROVE=0`. Headless callers that need it set it explicitly. Keep deny-tools; add `apply_patch` / `Write` aliases.

---

### WR-09: Exported sit + debug `pocket` extra + all-files + cleartext

**File:** `android/app/src/main/AndroidManifest.xml:3-18`
**Also:** `MainActivity.kt:74-90, 134-152`

**Issue:** `MainActivity` is `exported=true` (launcher — required) but also honors `intent.getStringExtra("pocket")` and binds that path after splash. Any app on the phone can `am start -n com.mechanicall.pocket.demo/.MainActivity --es pocket /storage/emulated/0/…`. Combined with `MANAGE_EXTERNAL_STORAGE` and `usesCleartextTraffic=true`, the lab sit is an all-files HTTP client another package can point. Lab sideload (CURRENT Limits) does not make the extra a feature.

**Fix:** Ignore `pocket` extra unless `BuildConfig.DEBUG`. Keep all-files behind the bind picker. Restrict cleartext to 10.0.2.2 / 127.0.0.1 / known desk CIDRs, not global.

---

### WR-10: Unauthenticated lab drop is a write path into the pocket offer dir

**File:** `python/aether_inbox.py:377-480`
**Also:** `DROP_DEFAULTS` includes `10.0.2.2:8765` / LAN IPs (`aether_inbox.py:31-35`)

**Issue:** `send_project` POSTs a zip to the first host that answers; `poll_incoming` GETs `/offer.zip` with no auth and unzips into `.aether/offer`. Zip-slip checks (`_zip_member_unsafe`, `_zip_target`) are real. Anyone on that LAN can plant an offer. Accept still copies everything except `CURRENT.md` / `NOTICE.json` (`accept_offer:147-153`) — so DECISIONS.md, events.jsonl, PROPOSE, `.aether/join-provision` overwrite on Accept. Accept ≠ Yes, but it is a trust boundary.

**Fix:** Bind drop to loopback. Auth or at least a shared token. Accept: never overwrite `.aether/`, `DECISIONS.md`, `events.jsonl`.

---

### WR-11: Panel Approve with empty reason still writes CURRENT

**File:** `python/aether_panel.py:669-675`
**Also:** `aether:676-681` (`reason` defaults to `APPROVED`)

**Issue:** Empty prompt becomes `"approved from operator board"`. Human button, but silence-adjacent: Enter is permission. SPEC: approval must be explicit.

**Fix:** If reason is empty, cancel (already done for `None`). Do not substitute a canned string.

---

### WR-12: `yes()` default Why; `apply_propose()` writes CURRENT without approve

**File:** `python/aether_pocket.py:275-301, 598-601`

**Issue:** `yes(..., reason="yes from demo sitting")` — Kotlin `decideTap` requires Why, but any Python/Chaquopy caller can omit a real reason and still stamp. `apply_propose` is public and writes CURRENT field lines with no Approval event. Tests call it directly (`test_aether_pocket.py:211-216`). Agents that import the module can mutate law without Yes.

**Fix:** No default Why (`reason: str` required). `apply_propose` private to `yes()`, or refuse unless called from `yes()`.

---

### WR-13: Phone has native Yes but not native `next`

**File:** `python/aether_pocket.py:644-645`

**Issue:** `next_action` is `run_aether(["next", action_id], ...)`. Pocket Yes is native so stock phones can stamp. Quiet One Next after Yes (CURRENT this sit’s home) still needs POSIX `bin/aether`. On the APK path, after Yes they land on `SitPlate.NEXT` and can only `did_it` / “Not yet keeps” — they cannot re-SELECT a new action-id without the desk CLI.

**Fix:** Native `pocket_next` with the same Approval=APPROVED gate as `cmd_next`, or drop One Next from the sit until that exists. Do not pretend the phone loop includes re-SELECT.

---

### WR-14: `agent_edit_propose` comment claims a CURRENT-dump refuse that is not implemented

**File:** `python/aether_pocket.py:1857-1858`

**Issue:**

```python
    # Refuse if the model tried to look like a live CURRENT-only dump without propose framing
    write_propose(root, text)
```

The refuse is a comment. Model output is written to PROPOSE unconditionally. `draft_chat` has `_prompt_contains_whole_file` for the *prompt*, not this writer.

**Fix:** Implement the refuse (e.g. if parsed fields include Approval=APPROVED or the text equals live CURRENT, raise PocketError) or delete the lie.

---

## Info

### IN-01: Bidirectional Prohibited containment false-refuses short action ids

**File:** `aether:537-564`

**Issue:** If action length ≥ 3 and the token is a substring of a prohibited line, preflight refuses. `preflight next` matches `dual-concurrent-next` / `funnel-this-next`. Fail-closed, so not a bypass; operators will see mysterious refuses.

**Fix:** Exact match, or require prohibited token ⊆ action (not the reverse), still with length ≥ 3.

---

### IN-02: `load_dotenv_files` auto-selects OpenRouter and slurps key-shaped lines from `/root/.chat.env`

**File:** `python/aether_fs.py:20-59`

**Issue:** Bare `sk-or-` / `gsk_` / `xai-` lines become env keys. Presence of `OPENROUTER_API_KEY` sets `AETHER_LLM_PROVIDER=openrouter` if unset. Shell peer later overrides to ollama; other callers may not. Local-first loses to a Desktop `.env`.

---

### IN-03: Authenticated human identity for approve is still not implemented

**File:** `aether:676-706` (`by":"human"` is a literal)

**Issue:** Anyone who can exec `aether approve` is recorded as human. NOT-IMPLEMENTED.md already lists this. Cooperative by design — do not market it as a sandbox. Grok/Cursor/raw shell remain outside the gate unless they volunteer.

---

### IN-04: 80% naming residue (lab, not kernel)

**Files:** `python/aether_storm.py:1-8` (AVD review boxes; “Not the sitter product”); `python/aether_twin.py:1-7` (HTTP GET mirror); `python/aether_panel.py:1-14` (Grok-left TUI); `python/aether_shell_agent.py:1-11` (Grok-shaped DEFINITION); SitRackView JOIN/WAKE bitmaps (`SitRackView.kt:164-169`, unused); `python/draft_rag_pack.py:1-4` (says “No chroma” — the honest leftover).

**Issue:** These are lab faces and factories. They do not make Mechanicall an OS kernel. They contradict “stop one wrong action before adding machinery” while CR-01/CR-02 still let a wrong action through.

---

### IN-05: MCP / client denylists are the rare honest projection

**File:** `python/aether_mcp.py:25-38, 185-206`; `python/aether_client.py:28-67`

**Issue:** MCP exposes `current` / `probe` / `propose_write` under `.aether/proposals/` only; basename + zip-slip-style resolve. Client allowlist never dispatches approve/reject/next. Keep these thin. Do not grow MCP into a tool runner.

---

_Reviewed: 2026-09-08T18:40:00Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: deep_
