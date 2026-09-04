#!/usr/bin/env python3
"""Mechanical PR scorecard (B1–B6, S1–S6). Not Yes. Human merges.

Usage:
  python3 score_pr.py --root /path/to/repo --pr 8
  python3 score_pr.py --root /path/to/repo --dirty
  python3 score_pr.py --root /path/to/repo --range aaaa..bbbb

Prints JSON. Does not post to GitHub. Does not approve.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SKIP_DIR_BITS = (
    "/storm-0/",
    "/storm-1/",
    "output/storm-",
    ".png",
    ".xml",
    ".jpg",
)


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    p = subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def pr_git_range(root: Path, pr: int) -> str | None:
    """first-parent...second-parent of the merge commit, if present."""
    code, out = run(
        ["gh", "pr", "view", str(pr), "--json", "mergeCommit,baseRefOid,headRefOid"],
        root,
    )
    if code != 0:
        return None
    try:
        meta = json.loads(out)
    except json.JSONDecodeError:
        return None
    merge = ((meta.get("mergeCommit") or {}) or {}).get("oid") or ""
    if merge:
        code2, out2 = run(["git", "rev-parse", f"{merge}^1", f"{merge}^2"], root)
        if code2 == 0:
            parents = [ln.strip() for ln in out2.splitlines() if ln.strip()]
            if len(parents) == 2:
                return f"{parents[0]}...{parents[1]}"
    base, head = meta.get("baseRefOid") or "", meta.get("headRefOid") or ""
    if base and head:
        return f"{base}...{head}"
    return None


def collect_pr_files(root: Path, pr: int) -> list[str]:
    code, out = run(
        ["gh", "pr", "diff", str(pr), "--name-only"],
        root,
    )
    if code == 0:
        return [ln.strip() for ln in out.splitlines() if ln.strip()]
    spec = pr_git_range(root, pr)
    if not spec:
        raise SystemExit(f"gh pr diff {pr} failed and no git range:\n{out}")
    return collect_range_files(root, spec)


def collect_range_files(root: Path, spec: str) -> list[str]:
    code, out = run(["git", "diff", "--name-only", spec], root)
    if code != 0:
        raise SystemExit(f"git diff {spec} failed:\n{out}")
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def collect_dirty_files(root: Path) -> list[str]:
    code, out = run(["git", "status", "--porcelain"], root)
    if code != 0:
        raise SystemExit(f"git status failed:\n{out}")
    files = []
    for ln in out.splitlines():
        if len(ln) < 4:
            continue
        path = ln[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        files.append(path)
    return files


def read_file(root: Path, rel: str, limit: int = 200_000) -> str:
    p = root / rel
    if not p.is_file():
        return ""
    try:
        data = p.read_bytes()[:limit]
    except OSError:
        return ""
    return data.decode("utf-8", errors="replace")


def blob_for_worktree(root: Path, files: list[str]) -> str:
    parts = []
    for rel in files:
        low = rel.lower()
        if any(bit in low for bit in (".png", ".jpg", ".jpeg", ".webp")):
            continue
        if "/storm-0/" in rel or "/storm-1/" in rel:
            continue
        text = read_file(root, rel)
        if text:
            parts.append(f"\n\n===== FILE {rel} =====\n{text}")
    return "\n".join(parts)


def blob_pr_diff(root: Path, pr: int) -> str:
    code, out = run(["gh", "pr", "diff", str(pr)], root)
    if code == 0:
        return out[:800_000]
    spec = pr_git_range(root, pr)
    if not spec:
        raise SystemExit(f"gh pr diff {pr} failed and no git range:\n{out[:2000]}")
    return blob_range(root, spec)


def blob_range(root: Path, spec: str) -> str:
    code, out = run(["git", "diff", spec], root)
    if code != 0:
        raise SystemExit(f"git diff {spec} failed:\n{out[:2000]}")
    return out[:800_000]


def hit(pattern: str, text: str, flags: int = 0) -> list[str]:
    found = []
    for m in re.finditer(pattern, text, flags):
        s = m.group(0)
        if s not in found:
            found.append(s)
        if len(found) >= 8:
            break
    return found


def score(files: list[str], blob: str, names: str, claim_text: str) -> dict:
    """Heuristic rows. FAIL is a signal, not a merge button."""
    rows = {}

    # B1 — approve human-only; tests must not stamp by:human on operator tree
    b1_fail = []
    if "tests/run.sh" in files:
        rs = read_file(Path("."), "tests/run.sh") if False else ""
        # blob already contains tests/run.sh if listed
        if re.search(
            r'for v in \$verbs;[\s\S]{0,400}"\$AETHER" "\$v"',
            blob,
        ) and "dispatch sandbox" not in blob and "$TMP/dispatch" not in blob:
            b1_fail.append("tests/run.sh still loops verbs against live root")
        if re.search(r'\$AETHER["\s]+approve', blob) and "TMP" not in blob:
            b1_fail.append("tests invoke aether approve outside obvious sandbox")
    if re.search(r'"by"\s*:\s*"human"', blob) and "events.jsonl" in names:
        if any(x in names for x in (".aether/events.jsonl",)):
            b1_fail.append("diff includes .aether/events.jsonl (provenance mix risk)")
    if re.search(r'name["\s:=]+approve["\']', blob) and "mcp" in blob.lower():
        b1_fail.append("MCP-shaped approve tool name in diff")
    rows["B1"] = {
        "id": "B1",
        "score": "FAIL" if b1_fail else "PASS",
        "question": "approve/reject/next still human-only in code and events?",
        "evidence": b1_fail or ["no test-as-human or MCP-approve pattern in changed files"],
    }

    # B2 — Decide on claimed surface without hidden POSIX aether
    native_yes = bool(
        re.search(r'Does not exec POSIX', blob)
        or re.search(r'def pocket_approve', blob)
    )
    posix_yes = bool(
        re.search(r'run_aether\(\s*\["approve"', blob)
        or re.search(r'run_aether\(\["approve"', blob)
    )
    face_yes = "FaceBridge.yes" in blob or "fun yes(" in blob
    if posix_yes and not native_yes:
        b2, ev = "FAIL", ["yes()/FaceBridge still shells POSIX aether approve"]
    elif native_yes:
        b2, ev = "PASS", ["pocket_approve / native yes path present"]
    elif face_yes:
        b2, ev = "FAIL", ["FaceBridge.yes present without native pocket_approve in this blob"]
    else:
        b2, ev = "N/A", ["no Decide/yes path in this change set"]
    rows["B2"] = {
        "id": "B2",
        "score": b2,
        "question": "Decide/Publish works on claimed surface without hidden POSIX aether?",
        "evidence": ev,
    }

    # B3 — zip / path escape
    unzip = "_unzip_to" in blob or "ZipFile" in blob
    unsafe_fn = "_zip_member_unsafe" in blob or "escapes offer directory" in blob
    naive = bool(
        re.search(r"target\s*=\s*dest\s*/\s*name", blob)
        and "relative_to" not in blob
    )
    if unzip and naive and not unsafe_fn:
        b3, ev = "FAIL", ["unzip joins dest/name without escape check"]
    elif unzip and unsafe_fn:
        b3, ev = "PASS", ["zip member unsafe/escape checks present"]
    elif unzip:
        b3, ev = "FAIL", ["ZipFile present; no _zip_member_unsafe / relative_to in blob"]
    else:
        b3, ev = "N/A", ["no zip extractor in this change set"]
    rows["B3"] = {
        "id": "B3",
        "score": b3,
        "question": "transport cannot write outside the bound tree?",
        "evidence": ev,
    }

    # B4 — live CURRENT excluded or honestly a proposal path
    current_files = [
        f
        for f in files
        if f == "CURRENT.md" or f.endswith("/CURRENT.md")
    ]
    proposal_ok = [
        f
        for f in files
        if f.startswith(".aether/proposals/")
        or f.startswith("examples/propose-current/")
    ]
    if current_files:
        b4, ev = "FAIL", [f"changes live CURRENT.md: {current_files}"]
    elif proposal_ok:
        b4, ev = "PASS", [f"proposals only: {proposal_ok[:6]}"]
    else:
        b4, ev = "PASS", ["live CURRENT.md not in change set"]
    rows["B4"] = {
        "id": "B4",
        "score": b4,
        "question": "live CURRENT excluded, or honestly applied by a human?",
        "evidence": ev,
    }

    # B5 — distribution claims vs build
    distro_words = bool(
        re.search(
            r"\b(Play Console|internal testing|distribution|testers install|AAB)\b",
            claim_text + blob[:8000],
            re.I,
        )
    )
    assemble = bool(
        re.search(r"assembleDebug|bundleRelease|connectedCheck", blob)
        or any("android.yml" in f or "android.yaml" in f for f in files)
    )
    ci_only_sh = ".github/workflows/test.yml" in files or distro_words
    if distro_words and not assemble:
        b5, ev = "FAIL", ["distribution language without Android assemble job in this set"]
    elif assemble:
        b5, ev = "PASS", ["Android assemble/bundle referenced"]
    else:
        b5, ev = "N/A", ["no distribution claim in this change set"]
    rows["B5"] = {
        "id": "B5",
        "score": b5,
        "question": "distribution claim has a built artifact, not string-search 10/10?",
        "evidence": ev
        + (["CI still tests/run.sh + control-layer only"] if ci_only_sh and not assemble else []),
    }

    # B6 — USB sold as LTE
    usb = bool(re.search(r"mbp-edge|RZCW2038KHN|sit-look|sideload-apk-via-edge", blob))
    lte_claim = bool(re.search(r"\bLTE\b", claim_text + blob[:12000]))
    honest_usb = bool(
        re.search(r"USB.{0,40}(?:not|≠|!=).{0,20}LTE|USB ≠ LTE|not LTE", blob, re.I)
    )
    if lte_claim and usb and not honest_usb:
        b6, ev = "FAIL", ["LTE language plus mbp-edge/USB tools without USB≠LTE disclaimer"]
    elif usb and honest_usb:
        b6, ev = "PASS", ["USB tools present; USB≠LTE language present"]
    elif lte_claim and not usb:
        b6, ev = "N/A", ["LTE mentioned without USB lab tools in this set — needs human receipt check"]
    else:
        b6, ev = "N/A", ["no LTE/USB distribution claim"]
    rows["B6"] = {
        "id": "B6",
        "score": b6,
        "question": "off-LAN claim is LTE/Play, not USB-on-mbp-edge?",
        "evidence": ev,
    }

    # Shape
    rollback = any("sit-apk-rollback" in f or "sit-apk-archive" in f for f in files)
    sitrack = any(f.endswith("SitRackView.kt") for f in files)
    leftover_compose = [
        f
        for f in files
        if f.endswith(
            (
                "SeatNav.kt",
                "ChatHome.kt",
                "LcdViewer.kt",
                "SkinLayout.kt",
                "DecideModule.kt",
                "PlanModule.kt",
            )
        )
    ]
    storm_dump = sum(1 for f in files if "/storm-0/" in f or "/storm-1/" in f)
    png_extra = [
        f
        for f in files
        if f.endswith(".png") and "drawable-nodpi/sit_" in f and not f.endswith(
            ("sit_splash.png", "sit_bind.png", "sit_plan.png", "sit_draft.png", "sit_skin.png")
        )
    ]

    rows["S1"] = {
        "id": "S1",
        "score": "PASS" if (rollback or sitrack) else "N/A",
        "question": "one product artifact and a rollback?",
        "evidence": [
            f"SitRackView.kt in set: {sitrack}",
            f"rollback scripts in set: {rollback}",
        ],
    }
    walk = bool(
        re.search(r"Bind", blob)
        and re.search(r"Decide", blob)
        and ("not Yes" in blob or "Opening the app is not Yes" in blob)
    )
    rows["S2"] = {
        "id": "S2",
        "score": "PASS" if walk else "N/A",
        "question": "walk still Bind → Plan → Draft → Decide+Why → Receipt?",
        "evidence": ["opening/bind not Yes language" if walk else "walk copy not in this set"],
    }
    skip_current = bool(re.search(r"skip.*CURRENT|CURRENT.md.*skip|offers skip", blob, re.I))
    rows["S3"] = {
        "id": "S3",
        "score": "PASS" if skip_current else "N/A",
        "question": "incoming offers skip CURRENT.md?",
        "evidence": ["skip-CURRENT language found" if skip_current else "not in this set"],
    }
    rows["S4"] = {
        "id": "S4",
        "score": "N/A",
        "question": "empty receipts stay empty?",
        "evidence": ["needs a receipt file / runtime; not grepped as a blocker"],
    }
    if leftover_compose:
        s5, ev = "FAIL", leftover_compose[:8]
    else:
        s5, ev = "PASS", ["no leftover Compose millwork modules in this change set"]
    rows["S5"] = {
        "id": "S5",
        "score": s5,
        "question": "interfaces do not become a second authority store?",
        "evidence": ev,
    }
    broad = len(files) > 120 or storm_dump > 20
    rows["S6"] = {
        "id": "S6",
        "score": "FAIL" if broad else "PASS",
        "question": "stranger can see lab vs testers install?",
        "evidence": [
            f"{len(files)} paths",
            f"{storm_dump} storm dump paths",
            f"{len(png_extra)} extra sit_*.png (not splash/bind/plan/draft/skin)",
        ],
    }

    blockers = [r["id"] for r in rows.values() if r["id"].startswith("B") and r["score"] == "FAIL"]
    if blockers:
        verdict = "blocker" if any(b in blockers for b in ("B1", "B2", "B3")) else "not-distribution"
    else:
        shape_fail = [r["id"] for r in rows.values() if r["id"].startswith("S") and r["score"] == "FAIL"]
        verdict = "lab-ok" if not shape_fail else "lab-ok-with-shape-flags"
    return {
        "verdict": verdict,
        "blockers_fail": blockers,
        "file_count": len(files),
        "rows": rows,
        "extra_sit_png": png_extra[:20],
        "leftover_compose": leftover_compose,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="repo root")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--pr", type=int)
    g.add_argument("--dirty", action="store_true")
    g.add_argument("--range", dest="rev_range")
    ap.add_argument("--claim-file", default="", help="optional PR body / notes")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    claim = ""
    if args.claim_file:
        claim = Path(args.claim_file).read_text(encoding="utf-8", errors="replace")

    if args.pr is not None:
        files = collect_pr_files(root, args.pr)
        label = f"pr-{args.pr}"
        blob_src = blob_pr_diff(root, args.pr)
        if not claim:
            code, out = run(
                ["gh", "pr", "view", str(args.pr), "--json", "title,body"],
                root,
            )
            claim = out if code == 0 else ""
    elif args.dirty:
        files = collect_dirty_files(root)
        label = "dirty-tree"
        blob_src = blob_for_worktree(root, files)
    else:
        files = collect_range_files(root, args.rev_range)
        label = args.rev_range
        blob_src = blob_range(root, args.rev_range)

    names = "\n".join(files)
    blob = names + "\n" + blob_src
    result = score(files, blob, names, claim)
    result["label"] = label
    result["files_sample"] = files[:80]
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
