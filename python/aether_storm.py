#!/usr/bin/env python3
"""STORM factory — persistent review environments for this repo.

Not Yes. Not Decide. Not the sitter product.

Emulators here are **mass-app subagent review boxes** for chat sessions:
isolated AVD + pocket, uidump, never Confirm, never the live A33.

Default home: ~/.mechanicall/storm (machine-local, not git).
SDK: ~/.android-sdk-mechanicall unless ANDROID_SDK_ROOT is set.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REFUSE_SERIAL = "RZCW2038KHN"
CAP = 2
DEFAULT_SDK = Path.home() / ".android-sdk-mechanicall"
DEFAULT_JAVA = Path.home() / ".jdk" / "temurin-17"
DEFAULT_HOME = Path.home() / ".mechanicall" / "storm"
IMAGE = "system-images;android-34;google_apis;x86_64"
DEVICE = "pixel_5"
PKG = "com.mechanicall.pocket.demo"


class StormError(Exception):
    """Factory refuse (never silent)."""


def refuse_serial(serial: str) -> str:
    s = (serial or "").strip()
    if s == REFUSE_SERIAL:
        raise StormError("refused: live A33")
    return s


def sdk_root() -> Path:
    env = os.environ.get("ANDROID_SDK_ROOT") or os.environ.get("ANDROID_HOME")
    return Path(env).expanduser() if env else DEFAULT_SDK


def java_home() -> Path:
    env = os.environ.get("JAVA_HOME")
    if env:
        return Path(env)
    if DEFAULT_JAVA.is_dir():
        return DEFAULT_JAVA
    return Path("/usr")


def storm_home() -> Path:
    env = os.environ.get("MECHANICALL_STORM_HOME")
    return Path(env).expanduser() if env else DEFAULT_HOME


def avd_home() -> Path:
    return storm_home() / "avd"


def bin_sdk(*parts: str) -> Path:
    return sdk_root().joinpath(*parts)


def _env() -> dict[str, str]:
    env = os.environ.copy()
    sdk = str(sdk_root())
    java = str(java_home())
    path = [
        str(bin_sdk("cmdline-tools", "latest", "bin")),
        str(bin_sdk("emulator")),
        str(bin_sdk("platform-tools")),
        str(Path(java) / "bin"),
        env.get("PATH", ""),
    ]
    env["ANDROID_SDK_ROOT"] = sdk
    env["ANDROID_HOME"] = sdk
    env["ANDROID_AVD_HOME"] = str(avd_home())
    env["JAVA_HOME"] = java
    env["PATH"] = ":".join(path)
    return env


def probe() -> dict:
    sdk = sdk_root()
    emu = bin_sdk("emulator", "emulator")
    avdm = bin_sdk("cmdline-tools", "latest", "bin", "avdmanager")
    img = sdk / "system-images" / "android-34" / "google_apis" / "x86_64"
    adb = shutil.which("adb") or str(bin_sdk("platform-tools", "adb"))
    return {
        "ok": emu.is_file() and avdm.is_file() and img.is_dir(),
        "sdk": str(sdk),
        "java": str(java_home()),
        "storm_home": str(storm_home()),
        "avd_home": str(avd_home()),
        "emulator": str(emu) if emu.is_file() else "",
        "avdmanager": str(avdm) if avdm.is_file() else "",
        "image": str(img) if img.is_dir() else "",
        "adb": adb if Path(adb).exists() else "",
        "cap": CAP,
        "refuse": REFUSE_SERIAL,
        "note": "STORM is developer infrastructure. Opening is not Decide.",
    }


def list_avds() -> list[str]:
    home = avd_home()
    if not home.is_dir():
        return []
    names: list[str] = []
    for ini in sorted(home.glob("*.ini")):
        names.append(ini.stem)
    return names


def ensure_home() -> Path:
    dest = avd_home()
    dest.mkdir(parents=True, exist_ok=True)
    (storm_home() / "out").mkdir(parents=True, exist_ok=True)
    return dest


def create_avd(name: str = "storm-0") -> dict:
    """Create an isolated AVD. Does not boot. Not Yes."""
    if not name.startswith("storm-"):
        raise StormError("refused: AVD name must start with storm-")
    n = int(name.split("-")[-1]) if name.split("-")[-1].isdigit() else 0
    if n >= CAP:
        raise StormError(f"refused: STORM cap {CAP} AVDs")
    info = probe()
    if not info["ok"]:
        raise StormError(
            "refused: STORM SDK incomplete "
            "(need emulator + system-images;android-34;google_apis;x86_64)"
        )
    ensure_home()
    if name in list_avds():
        return {"ok": True, "name": name, "existed": True, "avd_home": str(avd_home())}
    avdm = info["avdmanager"]
    cmd = [
        avdm,
        "create",
        "avd",
        "-n",
        name,
        "-k",
        IMAGE,
        "-d",
        DEVICE,
        "--force",
    ]
    proc = subprocess.run(
        cmd,
        input="no\n",
        text=True,
        capture_output=True,
        env=_env(),
        check=False,
    )
    if proc.returncode != 0:
        raise StormError(f"avdmanager failed: {proc.stderr or proc.stdout}")
    return {"ok": True, "name": name, "existed": False, "avd_home": str(avd_home())}


def adb_devices() -> list[str]:
    adb = probe()["adb"]
    if not adb:
        return []
    proc = subprocess.run(
        [adb, "devices"],
        capture_output=True,
        text=True,
        env=_env(),
        check=False,
    )
    serials: list[str] = []
    for line in (proc.stdout or "").splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "device":
            refuse_serial(parts[0])
            serials.append(parts[0])
    return serials


def status() -> dict:
    st = probe()
    st["avds"] = list_avds()
    try:
        st["devices"] = adb_devices()
    except StormError as exc:
        st["devices"] = []
        st["refuse"] = str(exc)
    st["ok"] = bool(st.get("ok"))
    return st


def render_status(st: dict) -> str:
    lines = [
        "# STORM",
        "",
        "**Not Decide. Not Yes.** Developer review environments for the original sit.",
        "",
        f"sdk: `{st.get('sdk')}`",
        f"storm_home: `{st.get('storm_home')}`",
        f"sdk_ok: {st.get('ok')}",
        f"avds: {', '.join(st.get('avds') or []) or '(none)'}",
        f"devices: {', '.join(st.get('devices') or []) or '(none)'}",
        "",
        f"cap {st.get('cap')} · refuse `{st.get('refuse')}` · never Confirm",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "cmd",
        nargs="?",
        default="status",
        choices=("status", "probe", "create", "setup"),
    )
    ap.add_argument("--name", default="storm-0")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--serial", default="", help="refused if RZCW2038KHN")
    args = ap.parse_args(argv)
    try:
        if args.serial:
            refuse_serial(args.serial)
        if args.cmd in {"status", "probe"}:
            st = status()
            print(json.dumps(st, indent=2) if args.json else render_status(st), end="")
            return 0 if st.get("ok") else 2
        if args.cmd in {"create", "setup"}:
            out = create_avd(args.name)
            if args.json:
                print(json.dumps(out, indent=2))
            else:
                print(f"STORM AVD {out['name']} ready under {out['avd_home']}")
                print("Boot is separate. Never Confirm. Never A33.")
            return 0
    except StormError as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
