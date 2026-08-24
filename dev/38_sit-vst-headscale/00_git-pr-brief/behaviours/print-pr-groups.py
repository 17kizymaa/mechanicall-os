#!/usr/bin/env python3
"""Print sit-vst-headscale PR file groups. Does not git add / commit.

Not Yes. Not Go-git. Exit 2 if a never-commit path is listed in a PR group.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]

NEVER = (
    "CURRENT.md",
    ".aether/events.jsonl",
    ".aether/preflight-last",
    ".aether/preflight.jsonl",
    ".aether/last-grok-brief.txt",
    ".context.md",
    "android/local.properties",
    "android/app/build",
)

PR1_ENGINE = (
    "python/aether_pocket.py",
    "python/aether_client.py",
    "python/aether_pocket_serve.py",
    "python/aether_twin.py",
    "python/app_verify.py",
    "tests/test_aether_pocket.py",
    "tests/test_aether_client.py",
    "tests/test_aether_pocket_serve.py",
    "tests/test_aether_twin.py",
    "tests/test_app_verify.py",
    "tests/run.sh",
    "scripts/sync-pocket-engine.sh",
    "scripts/wol-wake-listen.py",
    "scripts/rehearse-pocket-spike.sh",
    "scripts/pocket-refuse-root.sh",
    "scripts/build-tsnet-aar.sh",
    "scripts/desk-nice.sh",
    ".grok/skills/app-reviewer/SKILL.md",
    ".grok/skills/visual-reviewer/SKILL.md",
)

PR2_ANDROID = (
    "android/",
    "docs/LAB-STATUS.md",
    "scripts/sideload-apk-via-edge.sh",
    "scripts/storm-walk.sh",
    "examples/pocket-demo-client/",
)

PR3_FACTORY = (
    "dev/37_sit-join-workshop/",
    "dev/38_sit-vst-headscale/",
    "decision-tree.md",
    "examples/propose-current/CURRENT-sit-join-workshop.md",
    "examples/propose-current/CURRENT-sit-vst-headscale.md",
    "examples/propose-current/PROPOSE-sit-join-workshop.md",
    ".grok/workflows/actual-app-verification.rhai",
    ".grok/workflows/product-review.rhai",
    "scripts/boot-desk.sh",
    "scripts/desk-hop-proxy.py",
    "scripts/desk-through-a33.sh",
    "scripts/send-brake.sh",
    "scripts/serve-pocket-face.sh",
    "scripts/aether-on-a33.sh",
    "scripts/agent-edit-a33.sh",
    "scripts/push-aether-via-edge.sh",
    "scripts/push-pocket-via-edge.sh",
)

PR4_STORM = (
    "dev/38_sit-vst-headscale/03_storm/",
    "dev/38_sit-vst-headscale/04_sharing/",
    "SHARING.md",
    "android/tsnet/",
)

PARK_ARCHIVE = (
    "dev/23_mobile-planning-demo/",
    "dev/24_repair-current-one-next/",
    "dev/25_icm-people-app/",
    "dev/26_understand-what-built/",
    "dev/27_people-app-phone-seat/",
    "dev/28_mechanicall-phone-app/",
    "dev/29_people-app-phone-face/",
    "dev/30_modular-seat/",
    "dev/31_sequential-walk/",
    "dev/32_phase-close-agent-ci/",
    "dev/33_app-core/",
    "dev/34_one-goal-vst/",
    "dev/35_debug-window/",
    "dev/36_actual-app-verification/",
    "research/2026-08-19-BOTH-inform.md",
    "research/2026-08-19-codebase-wants-deep-research.md",
    "research/2026-08-19-operator-wants-deep-research.md",
    "examples/propose-current/CURRENT-mechanicall-debug-window.md",
    "examples/propose-current/CURRENT-people-app-phone-seat.md",
    "examples/propose-current/PROPOSE-agent-review-ci.md",
    "examples/propose-current/PROPOSE-mobile-planning-demo.md",
)

HUMAN_ONLY = (
    "CURRENT.md",
    "DECISIONS.md",
    ".aether/events.jsonl",
    ".context.md",
    ".aether/proposals/",
)

GROUPS = (
    ("PR1 engine+tests", PR1_ENGINE),
    ("PR2 android lab (source only)", PR2_ANDROID),
    ("PR3 sit-vst factory + leftover 37", PR3_FACTORY),
    ("PR4 STORM+twin (after sdcard)", PR4_STORM),
    ("PARK archive (later, optional)", PARK_ARCHIVE),
    ("HUMAN-ONLY (never model-commit)", HUMAN_ONLY),
)


def exists(rel: str) -> bool:
    return (ROOT / rel).exists()


def iter_files(rel: str):
    p = ROOT / rel
    if p.is_file():
        yield p
        return
    if not p.is_dir():
        return
    for child in p.rglob("*"):
        if not child.is_file():
            continue
        try:
            rel_f = child.relative_to(ROOT).as_posix()
        except ValueError:
            continue
        if rel_f.startswith("android/app/build/") or "/__pycache__/" in rel_f:
            continue
        yield child


def main() -> int:
    print(f"root: {ROOT}")
    print("print-only. no git add. no commit. not Yes.\n")
    bad = 0
    for title, paths in GROUPS:
        print(f"## {title}")
        for rel in paths:
            mark = "OK " if exists(rel) else "ABSENT"
            print(f"  {mark}  {rel}")
            if rel.rstrip("/") in {n.rstrip("/") for n in NEVER} and title.startswith("PR"):
                print(f"    REFUSE: never-commit path listed in a PR group")
                bad += 1
            if exists(rel) and title.startswith("PR") and rel.endswith("/"):
                skipped = 0
                tracked = 0
                for f in iter_files(rel):
                    rel_f = f.relative_to(ROOT).as_posix()
                    if rel_f.endswith(("local.properties", ".apk", ".ap_")):
                        skipped += 1
                        continue
                    tracked += 1
                print(f"    walk: {tracked} source files; skipped apk/local.properties={skipped}")
                if rel.startswith("android/"):
                    print("    git add android/; rely on android/.gitignore for app/build")
        print()
    print("never-commit:")
    for rel in NEVER:
        print(f"  {rel}")
    return 2 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
