#!/usr/bin/env python3
"""Minimal ADB helpers for House TV (Kodi / open URL). Stdlib only."""
from __future__ import annotations

import os
import subprocess
from typing import Optional

DEFAULT_IP = os.environ.get("EME640_IP", "192.168.1.235")
DEFAULT_PORT = os.environ.get("EME640_ADB_PORT", "5555")


def serial() -> str:
    return os.environ.get(
        "EME640_SERIAL",
        f"{os.environ.get('EME640_IP', DEFAULT_IP)}:{os.environ.get('EME640_ADB_PORT', DEFAULT_PORT)}",
    )


def adb(*args: str, timeout: int = 30) -> str:
    cmd = ["adb", "-s", serial(), *args]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or r.stdout.strip() or f"adb fail {args}")
    return (r.stdout or "").strip()


def ensure_connected() -> None:
    subprocess.run(
        ["adb", "connect", serial()],
        capture_output=True,
        text=True,
        timeout=15,
    )
    st = adb("get-state")
    if st != "device":
        raise RuntimeError(f"device state={st}")


def launch_kodi() -> str:
    ensure_connected()
    try:
        return adb(
            "shell",
            "monkey",
            "-p",
            "org.xbmc.kodi",
            "-c",
            "android.intent.category.LAUNCHER",
            "1",
        )
    except RuntimeError:
        return adb("shell", "am", "start", "-n", "org.xbmc.kodi/.Splash")


def open_url_on_device(url: str) -> str:
    """Open URL on TV. Prefer system WebView browser (ATV8 has org.chromium.webview_shell)."""
    ensure_connected()
    u = url.rstrip("/") + "/" if not url.endswith("/") else url
    try:
        return adb(
            "shell",
            "am",
            "start",
            "-a",
            "android.intent.action.VIEW",
            "-d",
            u,
            "-n",
            "org.chromium.webview_shell/.WebViewBrowserActivity",
        )
    except RuntimeError:
        return adb(
            "shell",
            "am",
            "start",
            "-a",
            "android.intent.action.VIEW",
            "-d",
            u,
        )


def device_available() -> bool:
    try:
        ensure_connected()
        return True
    except Exception:
        return False
