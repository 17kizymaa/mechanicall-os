# FRAMEWORKS — app reviewer (2026)

**Not Decide.** Choose the factory that can score BEHAVIOURS.md. Do not install a second authority.

## Candidates

| Factory | What it is | Fit here | Cost |
|---------|------------|----------|------|
| **uidump + Python + Grok swarm** (already in-tree) | `adb uiautomator dump` + `screencap` + `python/app_verify.py` + parallel explore agents | Filesystem-native. Never Confirm. Matches CORE_PRINCIPLES. storm-0 already exists | Low. Flaky taps if we script gestures; source probes are deterministic |
| **Grok workflow** (`parallel()` in `.rhai`) | Bounded fan-out of read-only reviewers, one synthesis | We already have `product-review.rhai`. Same host, no new SDK | Agent budget. Judgment, not locators |
| **Maestro YAML + Maestro MCP** | Declarative flows; MCP lets an agent drive emulator/device | Good for *replay* of bind→plan→draft. YAML is inspectable. MCP is optional | New CLI. iOS unused. Cloud needs a secret (reject for git). Must **forbid Confirm** in every flow |
| **Appium / WebDriver** | Language drivers over UIAutomator2 | Power, flaky, Java/Node stack | Violates “Python or shell for mechanical work” unless we wrap it. Do not add |
| **Pie / commercial agent QA** | Vision agents tap like a person | Opaque, hosted, not cat/grep | Reject for core |
| **Espresso** | In-process Android tests | Fast, needs instrumentation APK | Fine later; not the reviewer *agent* |

## Decision (this Next)

**Primary:** behaviours contract + `python/app_verify.py` (source + optional uidump) + `.grok/skills/app-reviewer` + workflow `actual-app-verification.rhai`.

**Optional later (not this sprint’s install):** Maestro flows that **assertVisible** and never `tapOn: Confirm`. Maestro MCP only if a human wants agent-driven replay on storm-0.

**Never:** Appium as product, hosted QA as authority, walker Confirm, model approve.

## Why not Maestro first

Maestro is the 2026 default for YAML E2E (MIT; MCP since 2026). This repo already walks with uidump. Adding Maestro before the **contract** exists would test chrome, not behaviours. Contract first; Maestro is a later driver for the same ids.
