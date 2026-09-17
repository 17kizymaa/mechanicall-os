#!/usr/bin/env python3
"""Mechanical You Decide plate cycle. Model only patches.

assemble → storm dest walk → look_verify → app_verify.

Never Confirm. Never A33. FLAG is iterate, not sitting death.
PASS is not human Yes. USB ≠ LTE.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

PY = Path(__file__).resolve().parent
ROOT = PY.parent
if str(PY) not in sys.path:
    sys.path.insert(0, str(PY))

from app_verify import render as law_render  # noqa: E402
from app_verify import score_source as law_score
from look_verify import L_ROWS, REFUSE_SERIAL  # noqa: E402
from look_verify import render as look_render
from look_verify import score as look_score
from mum_verify import render as mum_render  # noqa: E402
from mum_verify import score as mum_score

EXIT_PASS = 0
EXIT_BUDGET = 1
EXIT_ITERATE = 2
EXIT_REFUSE = 3
EXIT_ENV = 4

DEFAULT_JAVA = Path.home() / ".jdk" / "temurin-17"
DEFAULT_SDK = Path.home() / ".android-sdk-mechanicall"
DEFAULT_APK = ROOT / "android" / "app" / "build" / "outputs" / "apk" / "debug" / "app-debug.apk"
DEFAULT_STILLS = (
    ROOT / "dev" / "57_first-sit-look" / "06_still_again" / "output" / "stills"
)
ADB = DEFAULT_SDK / "platform-tools" / "adb"

PLATE_IDS = {
    "L0": "L0-frame",
    "L1": "L1-peek",
    "L2": "L2-crt-dest",
    "L3": "L3-draft-dest",
    "L4": "L4-folder-dest",
    "L5": "L5-title",
    "L6": "L6-decide-well",
    "L7": "L7-gate",
    "L8": "L8-receipt",
}


def normalize_plate(raw: str) -> str:
    s = (raw or "").strip()
    if s in PLATE_IDS:
        return PLATE_IDS[s]
    if s in PLATE_IDS.values() or s in L_ROWS:
        return s
    raise ValueError(f"unknown plate {raw!r}; want L0..L8 or a look_verify row id")


def _law_ok(law_rows: list[dict]) -> bool:
    return bool(law_rows) and all(r.get("ok") for r in law_rows)


def decide(plate_id: str, look_rows: list[dict], law_rows: list[dict]) -> dict:
    """Score this plate only. Other-row FLAG does not fail this plate."""
    look = {r["id"]: r for r in look_rows}
    law_fail = [r["id"] for r in law_rows if not r.get("ok")]
    l0 = look.get("L0-frame") or {}
    row = look.get(plate_id)
    if row is None:
        return {
            "name": "ENV",
            "exit": EXIT_ENV,
            "reason": f"no look row {plate_id}",
            "plate": None,
            "law_fail": law_fail,
            "l0": l0.get("verdict"),
        }
    if l0.get("verdict") == "FAIL":
        return {
            "name": "FAIL",
            "exit": EXIT_ITERATE,
            "reason": l0.get("evidence") or "L0-frame FAIL",
            "plate": row,
            "law_fail": law_fail,
            "l0": "FAIL",
        }
    if law_fail:
        return {
            "name": "FAIL",
            "exit": EXIT_ITERATE,
            "reason": "law FAIL " + ", ".join(law_fail),
            "plate": row,
            "law_fail": law_fail,
            "l0": l0.get("verdict"),
        }
    if row["verdict"] == "FAIL":
        return {
            "name": "FAIL",
            "exit": EXIT_ITERATE,
            "reason": row.get("evidence") or "plate FAIL",
            "plate": row,
            "law_fail": law_fail,
            "l0": l0.get("verdict"),
        }
    if row["verdict"] == "FLAG":
        return {
            "name": "FLAG",
            "exit": EXIT_ITERATE,
            "reason": row.get("evidence") or "plate FLAG",
            "plate": row,
            "law_fail": law_fail,
            "l0": l0.get("verdict"),
        }
    return {
        "name": "PASS",
        "exit": EXIT_PASS,
        "reason": row.get("evidence") or "plate PASS",
        "plate": row,
        "law_fail": law_fail,
        "l0": l0.get("verdict"),
    }


def budget_stop(decision: dict, iteration: int, maximum: int) -> dict:
    out = dict(decision)
    if out["exit"] == EXIT_ITERATE and iteration >= maximum:
        out["name"] = "STOP"
        out["exit"] = EXIT_BUDGET
        out["reason"] = f"N={maximum} exhausted; {decision['name']}: {decision['reason']}"
    return out


def render_verdict(
    *,
    plate_id: str,
    iteration: int,
    maximum: int,
    decision: dict,
    look_rows: list[dict],
    law_rows: list[dict],
    stills: Path,
    skipped: list[str],
) -> str:
    look_pass = sum(1 for r in look_rows if r["verdict"] == "PASS")
    look_flag = sum(1 for r in look_rows if r["verdict"] == "FLAG")
    look_fail = [r["id"] for r in look_rows if r["verdict"] == "FAIL"]
    law_pass = sum(1 for r in law_rows if r.get("ok"))
    plate = decision.get("plate") or {}
    names = {
        EXIT_PASS: "PASS",
        EXIT_BUDGET: "STOP",
        EXIT_ITERATE: "ITERATE",
        EXIT_REFUSE: "REFUSE",
        EXIT_ENV: "ENV",
    }
    label = names.get(decision["exit"], decision["name"])
    lines = [
        f"# VERDICT — plate {plate_id}",
        "",
        "**Not Yes. Not Decide.** Mechanical plate cycle. FLAG is iterate.",
        "",
        f"- plate: `{plate_id}`",
        f"- iter: {iteration} / {maximum}",
        f"- this plate: {decision['name']} — {decision['reason']}",
        f"- look row: {plate.get('verdict', 'n/a')}",
        f"- look: {look_pass}/{len(look_rows) or 0} PASS · {look_flag} FLAG · {len(look_fail)} FAIL",
        f"- law: {law_pass}/{len(law_rows) or 0} PASS",
        f"- stills: `{stills}`",
        f"- skipped: {', '.join(skipped) if skipped else 'none'}",
        f"- verdict: **{label}**",
        f"- exit: {decision['exit']}",
        "",
        "Other-row FLAG does not fail this plate. L0 FAIL and law FAIL fail-close.",
        "PASS is not human Yes. Confirm was not tapped. A33 was not used.",
        "",
    ]
    return "\n".join(lines)


def _env() -> dict[str, str]:
    env = os.environ.copy()
    java = Path(env["JAVA_HOME"]) if env.get("JAVA_HOME") else DEFAULT_JAVA
    sdk = Path(env.get("ANDROID_SDK_ROOT") or env.get("ANDROID_HOME") or DEFAULT_SDK)
    if java.is_dir():
        env["JAVA_HOME"] = str(java)
    if sdk.is_dir():
        env["ANDROID_HOME"] = str(sdk)
        env["ANDROID_SDK_ROOT"] = str(sdk)
        env["PATH"] = str(sdk / "platform-tools") + ":" + env.get("PATH", "")
    if java.is_dir():
        env["PATH"] = str(java / "bin") + ":" + env.get("PATH", "")
    return env


def _run(cmd: list[str], *, cwd: Path | None = None, timeout: int = 600) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        env=_env(),
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def adb_serials() -> list[str]:
    adb = ADB if ADB.is_file() else Path("adb")
    proc = subprocess.run(
        [str(adb), "devices"],
        capture_output=True,
        text=True,
        check=False,
        env=_env(),
    )
    if proc.returncode != 0:
        return []
    out: list[str] = []
    for ln in proc.stdout.splitlines()[1:]:
        if "\tdevice" in ln:
            out.append(ln.split()[0])
    return out


def refuse_a33(serials: list[str] | None = None) -> str | None:
    found = serials if serials is not None else adb_serials()
    if REFUSE_SERIAL in found:
        return REFUSE_SERIAL
    return None


def assemble(apk: Path) -> tuple[int, str]:
    gradlew = ROOT / "android" / "gradlew"
    if not gradlew.is_file():
        return EXIT_ENV, f"missing {gradlew}"
    proc = _run(
        [str(gradlew), "--no-daemon", ":app:assembleDebug"],
        cwd=ROOT / "android",
        timeout=900,
    )
    blob = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        tail = "\n".join(blob.splitlines()[-40:])
        return EXIT_ENV, f"assembleDebug exit {proc.returncode}\n{tail}"
    if not apk.is_file():
        return EXIT_ENV, f"assemble ok but missing {apk}"
    return 0, f"assembleDebug ok {apk}"


def archive(apk: Path) -> tuple[int, str]:
    script = ROOT / "scripts" / "sit-apk-archive.sh"
    if not script.is_file():
        return EXIT_ENV, f"missing {script}"
    proc = _run(["sh", str(script), str(apk)], cwd=ROOT, timeout=60)
    blob = (proc.stdout or "").strip() or (proc.stderr or "").strip()
    if proc.returncode != 0:
        return EXIT_ENV, f"archive exit {proc.returncode}: {blob}"
    return 0, blob


def dest_walk(stills: Path, apk: Path) -> tuple[int, str]:
    serials = adb_serials()
    bad = refuse_a33(serials)
    if bad:
        return EXIT_REFUSE, f"refused: live A33 {bad}"
    emus = [s for s in serials if s.startswith("emulator-")]
    if not emus:
        return (
            EXIT_ENV,
            "no storm emulator; boot first: sh scripts/storm-up.sh storm-0 (never A33)",
        )
    walker = PY / "sit_dest_walk.py"
    cmd = [sys.executable, str(walker), "--out", str(stills)]
    if apk.is_file():
        cmd += ["--apk", str(apk)]
    proc = _run(cmd, cwd=ROOT, timeout=900)
    blob = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 3:
        return EXIT_REFUSE, blob.strip() or "walker refused A33"
    if proc.returncode != 0:
        tail = "\n".join(blob.splitlines()[-40:])
        return EXIT_ENV, f"sit_dest_walk exit {proc.returncode}\n{tail}"
    return 0, f"stills {stills}"


def score_dirs(stills: Path, law_uidump: bool = False) -> tuple[list[dict], list[dict]]:
    look_rows = look_score(stills if stills.is_dir() else None)
    blob = ""
    if law_uidump and stills.is_dir():
        blob = _uidump_blob(stills)
    law_rows = law_score(blob)
    return look_rows, law_rows


def _uidump_blob(stills: Path) -> str:
    chunks: list[str] = []
    for p in sorted(stills.glob("uidump*.xml")):
        chunks.append(p.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(chunks)


def write_outputs(
    out: Path,
    *,
    plate_id: str,
    iteration: int,
    maximum: int,
    decision: dict,
    look_rows: list[dict],
    law_rows: list[dict],
    stills: Path,
    skipped: list[str],
    notes: list[str],
) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    (out / "LOOK.md").write_text(look_render(look_rows), encoding="utf-8")
    (out / "LAW.md").write_text(law_render(law_rows), encoding="utf-8")
    mum_rows = mum_score(png_dir=stills if stills.is_dir() else None)
    (out / "MUM.md").write_text(mum_render(mum_rows), encoding="utf-8")
    verdict = render_verdict(
        plate_id=plate_id,
        iteration=iteration,
        maximum=maximum,
        decision=decision,
        look_rows=look_rows,
        law_rows=law_rows,
        stills=stills,
        skipped=skipped,
    )
    if notes:
        verdict = verdict.rstrip() + "\n\n## Notes\n\n" + "\n".join(f"- {n}" for n in notes) + "\n"
    path = out / "VERDICT.md"
    path.write_text(verdict, encoding="utf-8")
    return path


def one_cycle(args: argparse.Namespace, iteration: int) -> dict:
    notes: list[str] = []
    skipped: list[str] = []
    stills: Path = args.stills_dir
    apk: Path = args.apk
    stills.mkdir(parents=True, exist_ok=True)

    if args.patch_cmd and not args.score_only:
        proc = _run(["sh", "-c", args.patch_cmd], cwd=ROOT, timeout=args.patch_timeout)
        notes.append(f"patch-cmd exit {proc.returncode}")
        if proc.returncode != 0:
            return {
                "decision": {
                    "name": "ENV",
                    "exit": EXIT_ENV,
                    "reason": f"patch-cmd exit {proc.returncode}",
                    "plate": None,
                    "law_fail": [],
                    "l0": None,
                },
                "look_rows": [],
                "law_rows": [],
                "skipped": skipped,
                "notes": notes,
            }

    if args.score_only or args.skip_assemble:
        skipped.append("assemble")
    else:
        code, msg = assemble(apk)
        notes.append(msg.split("\n", 1)[0])
        if code != 0:
            return {
                "decision": {
                    "name": "ENV",
                    "exit": code,
                    "reason": msg,
                    "plate": None,
                    "law_fail": [],
                    "l0": None,
                },
                "look_rows": [],
                "law_rows": [],
                "skipped": skipped,
                "notes": notes,
            }
        if args.skip_archive:
            skipped.append("archive")
        else:
            acode, amsg = archive(apk)
            notes.append(amsg)
            if acode != 0:
                notes.append("archive failed; stills may continue")

    if args.score_only or args.skip_walk:
        skipped.append("walk")
    else:
        code, msg = dest_walk(stills, apk)
        notes.append(msg.split("\n", 1)[0])
        if code != 0:
            return {
                "decision": {
                    "name": "REFUSE" if code == EXIT_REFUSE else "ENV",
                    "exit": code,
                    "reason": msg,
                    "plate": None,
                    "law_fail": [],
                    "l0": None,
                },
                "look_rows": [],
                "law_rows": [],
                "skipped": skipped,
                "notes": notes,
            }

    look_rows, law_rows = score_dirs(stills, law_uidump=args.law_uidump)
    decision = decide(args.plate, look_rows, law_rows)
    return {
        "decision": decision,
        "look_rows": look_rows,
        "law_rows": law_rows,
        "skipped": skipped,
        "notes": notes,
    }


def run(args: argparse.Namespace) -> int:
    if args.serial == REFUSE_SERIAL:
        print("refused: live A33", file=sys.stderr)
        return EXIT_REFUSE
    bad = refuse_a33()
    if bad and not args.score_only and not args.skip_walk:
        print(f"refused: live A33 {bad}", file=sys.stderr)
        return EXIT_REFUSE

    args.stills_dir = args.stills_dir.resolve()
    args.out = (args.out or args.stills_dir.parent).resolve()
    args.apk = args.apk.resolve()
    started = time.monotonic()
    last: dict | None = None
    maximum = max(1, args.max)
    start_iter = max(1, args.iter)
    looping = args.loop
    if looping and not args.patch_cmd and not args.score_only:
        print(
            "loop without --patch-cmd is one cycle (model patches, then re-run)",
            file=sys.stderr,
        )
        looping = False

    iteration = start_iter
    while True:
        if args.timeout and (time.monotonic() - started) > args.timeout:
            decision = {
                "name": "STOP",
                "exit": EXIT_BUDGET,
                "reason": f"wall clock {args.timeout}s",
                "plate": None,
                "law_fail": [],
                "l0": None,
            }
            look_rows, law_rows = last["look_rows"] if last else ([], [])
            write_outputs(
                args.out,
                plate_id=args.plate,
                iteration=iteration,
                maximum=maximum,
                decision=decision,
                look_rows=look_rows,
                law_rows=law_rows,
                stills=args.stills_dir,
                skipped=last["skipped"] if last else ["timeout"],
                notes=(last["notes"] if last else []) + [decision["reason"]],
            )
            print(
                f"CYCLE plate={args.plate} iter={iteration}/{maximum} "
                f"verdict=STOP exit={EXIT_BUDGET}"
            )
            return EXIT_BUDGET

        last = one_cycle(args, iteration)
        decision = last["decision"]
        if looping:
            decision = budget_stop(decision, iteration - start_iter + 1, maximum)
        last["decision"] = decision
        path = write_outputs(
            args.out,
            plate_id=args.plate,
            iteration=iteration,
            maximum=maximum,
            decision=decision,
            look_rows=last["look_rows"],
            law_rows=last["law_rows"],
            stills=args.stills_dir,
            skipped=last["skipped"],
            notes=last["notes"],
        )
        row = (decision.get("plate") or {}).get("verdict", decision["name"])
        law_n = len(last["law_rows"])
        law_ok = "PASS" if _law_ok(last["law_rows"]) else ("FAIL" if law_n else "n/a")
        print(
            f"CYCLE plate={args.plate} iter={iteration}/{maximum} "
            f"look_row={row} law={law_ok} verdict={decision['name']} "
            f"exit={decision['exit']}"
        )
        print(path)
        if decision["exit"] != EXIT_ITERATE:
            return int(decision["exit"])
        if not looping:
            return EXIT_ITERATE
        iteration += 1
        if (iteration - start_iter + 1) > maximum:
            return EXIT_BUDGET


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "exit 0 PASS this plate + law green\n"
            "exit 1 STOP budget (N exhausted or clock)\n"
            "exit 2 ITERATE this plate FLAG/FAIL — patch one gap, re-run\n"
            "exit 3 REFUSE live A33\n"
            "exit 4 ENV assemble/walk/missing\n"
            "\n"
            "Orchestrator:\n"
            "  patch ONE FLAG\n"
            "  python3 python/you_decide_plate_cycle.py --plate L2 "
            "--stills-dir dev/57_first-sit-look/06_still_again/output/stills\n"
            "  # exit 2 → patch again; exit 0 → next plate; exit 1 → human carry\n"
        ),
    )
    ap.add_argument("--plate", required=True, help="L2 or L2-crt-dest")
    ap.add_argument(
        "--stills-dir",
        type=Path,
        default=DEFAULT_STILLS,
        help="dest walker PNG+uidump dir",
    )
    ap.add_argument("--out", type=Path, default=None, help="VERDICT/LOOK/LAW dir")
    ap.add_argument("--apk", type=Path, default=DEFAULT_APK)
    ap.add_argument("--max", type=int, default=5, help="iteration budget per plate")
    ap.add_argument("--iter", type=int, default=1, help="starting iteration (orchestrator count)")
    ap.add_argument(
        "--loop",
        action="store_true",
        help="repeat until PASS, N, or clock; requires --patch-cmd unless --score-only",
    )
    ap.add_argument("--patch-cmd", default="", help="shell run at the start of each loop iter")
    ap.add_argument("--patch-timeout", type=int, default=600)
    ap.add_argument("--timeout", type=int, default=0, help="wall clock seconds for --loop")
    ap.add_argument("--score-only", action="store_true", help="skip assemble+walk; score stills")
    ap.add_argument(
        "--law-uidump",
        action="store_true",
        help="pass dest uidumps into app_verify (default is source probes, matching python3 python/app_verify.py)",
    )
    ap.add_argument("--skip-assemble", action="store_true")
    ap.add_argument("--skip-walk", action="store_true")
    ap.add_argument("--skip-archive", action="store_true")
    ap.add_argument("--serial", default="", help="adb serial; RZCW2038KHN refused")
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        args.plate = normalize_plate(args.plate)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_ENV
    if args.max < 1:
        print("--max must be >= 1", file=sys.stderr)
        return EXIT_ENV
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
