#!/usr/bin/env python3
"""STORM walker helpers. Never Confirm. Never A33."""
from __future__ import annotations

import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

REFUSE = "RZCW2038KHN"
PKG = "com.mechanicall.pocket.demo"


def adb(serial: str, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    if serial == REFUSE:
        raise SystemExit("refused: live A33")
    return subprocess.run(
        ["adb", "-s", serial, *args],
        check=check,
        capture_output=True,
        text=True,
    )


def dump(serial: str, out: Path, name: str) -> Path:
    adb(serial, "shell", "uiautomator", "dump", "/sdcard/uidump.xml")
    xml_path = out / f"uidump-{name}.xml"
    adb(serial, "pull", "/sdcard/uidump.xml", str(xml_path))
    png = out / f"{name}.png"
    raw = subprocess.run(
        ["adb", "-s", serial, "exec-out", "screencap", "-p"],
        check=True,
        capture_output=True,
    )
    png.write_bytes(raw.stdout)
    return xml_path


def nodes(xml_path: Path) -> list[ET.Element]:
    tree = ET.parse(xml_path)
    return list(tree.iter("node"))


def bounds(node: ET.Element) -> tuple[int, int, int, int]:
    b = node.attrib.get("bounds") or "[0,0][0,0]"
    nums = [int(x) for x in b.replace("[", " ").replace("]", " ").replace(",", " ").split() if x]
    return nums[0], nums[1], nums[2], nums[3]


def center(node: ET.Element) -> tuple[int, int]:
    l, t, r, b = bounds(node)
    return (l + r) // 2, (t + b) // 2


def find_text(xml_path: Path, needle: str) -> ET.Element | None:
    want = needle.lower()
    for node in nodes(xml_path):
        blob = " ".join(
            [
                node.attrib.get("text") or "",
                node.attrib.get("content-desc") or "",
                node.attrib.get("resource-id") or "",
            ]
        ).lower()
        if want in blob:
            return node
    return None


def tap_text(serial: str, xml_path: Path, needle: str) -> bool:
    node = find_text(xml_path, needle)
    if node is None:
        return False
    x, y = center(node)
    adb(serial, "shell", "input", "tap", str(x), str(y))
    return True


def tap_xy(serial: str, x: int, y: int) -> None:
    adb(serial, "shell", "input", "tap", str(x), str(y))


def wait_boot(serial: str, tries: int = 30) -> None:
    for _ in range(tries):
        p = adb(serial, "shell", "getprop", "sys.boot_completed", check=False)
        if (p.stdout or "").strip() == "1":
            return
        time.sleep(1)
    raise SystemExit(f"not booted: {serial}")


if __name__ == "__main__":
    print("import walk_sit; never Confirm", file=sys.stderr)
