#!/usr/bin/env python3
"""
GHOST-USER MODE Python Behaviour for creating portable Grok / awareness-agent USB installer.

This script verifies reality at every step, only targets the exact 2GB Flash Disk USB,
wipes it completely (as requested), and bootstraps a replica of the current working
environment (Alpine 3.24 + key tools + full awareness-agent repo + bootstrap script).

Run with python3 this-script.py --force-wipe  (user has consented to wipe).

All actions are printed with [GHOST-USER] prefix for verification.
"""

import os
import subprocess
import sys
import time

DEVICE = "/dev/sdb"
EXPECTED_SIZE_BYTES = 2004877312  # ~1.9G
EXPECTED_MODEL_CONTAINS = "Flash Disk"
MOUNT_POINT = "/mnt/grok-usb"

def run(cmd, check=True, capture=False):
    print(f"[GHOST-USER] EXEC: {cmd}")
    if capture:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout.strip())
        if result.stderr:
            print("STDERR:", result.stderr.strip())
        if check and result.returncode != 0:
            print(f"[GHOST-USER] FAILED with code {result.returncode}")
            sys.exit(1)
        return result
    else:
        result = subprocess.run(cmd, shell=True)
        if check and result.returncode != 0:
            print(f"[GHOST-USER] FAILED with code {result.returncode}")
            sys.exit(1)
        return result

def verify_device():
    print("\n[GHOST-USER] === REALITY VERIFICATION: IDENTIFYING USB ===")
    run(f"lsblk -o NAME,SIZE,TYPE,MODEL,TRAN,LABEL {DEVICE}")
    # Size check
    res = run(f"blockdev --getsize64 {DEVICE} 2>/dev/null || echo 0", capture=True)
    size = int(res.stdout.strip() or "0")
    print(f"[GHOST-USER] Detected size: {size} bytes (expected ~{EXPECTED_SIZE_BYTES})")
    if abs(size - EXPECTED_SIZE_BYTES) > 100*1024*1024:  # tolerance ~100MB
        print("[GHOST-USER] SIZE MISMATCH. ABORTING to protect wrong device.")
        sys.exit(1)
    # Model check via lsblk
    res = run(f"lsblk -d -o MODEL,TRAN {DEVICE}", capture=True)
    if EXPECTED_MODEL_CONTAINS.lower() not in res.stdout.lower() or "usb" not in res.stdout.lower():
        print("[GHOST-USER] MODEL/TRANSPORT MISMATCH. Not the expected Flash Disk usb. ABORT.")
        sys.exit(1)
    print("[GHOST-USER] DEVICE VERIFIED: /dev/sdb is the 2GB Flash Disk usb.")
    # Final human visible check
    run(f"lsblk {DEVICE}")

def main():
    if "--force-wipe" not in sys.argv:
        print("[GHOST-USER] DRY/GHOST MODE ONLY. Add --force-wipe to actually overwrite.")
        print("[GHOST-USER] This would wipe /dev/sdb and set up the portable bootstrap.")
        verify_device()
        print("[GHOST-USER] No changes made (no --force-wipe).")
        return

    print("\n[GHOST-USER] === GHOST-USER MODE: EXECUTING WIPE AND BOOTSTRAP ===")
    print("[GHOST-USER] USER HAS REQUESTED OVERWRITE OF 2GB USB CONTENTS.")
    verify_device()

    print("\n[GHOST-USER] 1. Unmounting any partitions (safety)")
    run(f"umount {DEVICE}* 2>/dev/null || true; sleep 1")

    print("\n[GHOST-USER] 2. Wiping beginning of device (clear partition table + boot sectors)")
    run(f"dd if=/dev/zero of={DEVICE} bs=1M count=10")
    run(f"wipefs -a {DEVICE} || true")
    run(f"sync; sleep 1")

    print("\n[GHOST-USER] 3. Creating new partition table and single large partition")
    run(f"parted -s {DEVICE} mklabel msdos")
    run(f"parted -s {DEVICE} mkpart primary ext4 4MiB 100%")
    run(f"parted -s {DEVICE} set 1 boot on || true")
    run(f"partprobe {DEVICE} || sleep 2; sync")

    PART = f"{DEVICE}1"
    print(f"[GHOST-USER] Partition created: {PART}")

    print("\n[GHOST-USER] 4. Formatting as ext4")
    run(f"mkfs.ext4 -F -L GROK-PORTABLE-DEV {PART}")
    run("sync; sleep 1")

    print("\n[GHOST-USER] 5. Mounting and preparing content")
    run(f"mkdir -p {MOUNT_POINT}")
    run(f"mount {PART} {MOUNT_POINT}")

    # Copy the awareness-agent repo (exclude heavy caches)
    print("[GHOST-USER] Copying awareness-agent source tree (the single source of truth)")
    run(f"mkdir -p {MOUNT_POINT}/awareness-agent")
    # Use tar to copy cleanly (rsync not present)
    run(f"tar --exclude='__pycache__' --exclude='.aether' --exclude='.git' --exclude='*.pyc' "
        f"-cf - -C /home/awareness-agent . | tar -xpf - -C {MOUNT_POINT}/awareness-agent")
    run(f"sync")

    # Place aether at root for easy access
    run(f"cp {MOUNT_POINT}/awareness-agent/aether {MOUNT_POINT}/aether")
    run(f"chmod +x {MOUNT_POINT}/aether")

    # Copy package list captured from current env
    print("[GHOST-USER] Writing captured package list from current environment")
    if os.path.exists("/tmp/installed-packages.txt"):
        run(f"cp /tmp/installed-packages.txt {MOUNT_POINT}/packages-from-current-env.txt")
    else:
        run(f"apk info -q | sort > {MOUNT_POINT}/packages-from-current-env.txt")

    # Write the bootstrap script
    print("[GHOST-USER] Writing bootstrap-replicate script")
    bootstrap_content = '''#!/bin/sh
# bootstrap-replicate-grok-env.sh
# Portable bootstrap from GROK-PORTABLE-DEV USB.
# Run this (as root) on a target Alpine Linux system to replicate the working
# environment that was used to develop awareness-agent.

set -e

echo "=== GROK PORTABLE USB - Replicating current working environment ==="
echo "USB content mounted at /media or /mnt. Adapt paths if needed."

USB_ROOT=$(dirname "$0")
if [ -d "$USB_ROOT/awareness-agent" ]; then
  REPO="$USB_ROOT/awareness-agent"
else
  REPO="/media/GROK-PORTABLE-DEV/awareness-agent"
fi

echo "1. Installing essential packages to replicate the dev tools..."
apk update || true
# Core set for awareness-agent + Grok dev work (curated from original env)
apk add --no-cache \\
  alpine-base bash python3 git curl wget entr \\
  apk-tools util-linux parted e2fsprogs tar dosfstools \\
  coreutils findutils grep sed awk

echo "2. Installing aether command"
cp "$REPO/aether" /usr/local/bin/aether 2>/dev/null || cp "$USB_ROOT/aether" /usr/local/bin/aether || true
chmod +x /usr/local/bin/aether || true

echo "3. Shell integration for aether (edit your ~/.profile or ~/.bashrc)"
python3 "$REPO/scripts/emit_aether_snippet.py" >> ~/.profile 2>/dev/null || true
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.profile 2>/dev/null || true

echo "4. Example: initialize awareness sidecars"
mkdir -p ~/grok-projects
cd ~/grok-projects || true
aether init || echo "Run 'aether init' manually after adjusting PATH."

echo "5. The full original package list is in packages-from-current-env.txt on the USB."
echo "   You can review and apk add additional ones if needed for your experimental env."

echo ""
echo "=== Environment bootstrapped. USB now contains the awareness-agent repo. ==="
echo "cd to the awareness-agent dir on the USB and use ./aether status etc."
echo "Filesystem is the source of truth. cat .context.md"
'''

    with open(f"{MOUNT_POINT}/bootstrap-replicate-grok-env.sh", "w") as f:
        f.write(bootstrap_content)
    run(f"chmod +x {MOUNT_POINT}/bootstrap-replicate-grok-env.sh")

    # Simple README on the USB root
    readme = """GROK-PORTABLE-DEV USB

This USB was created by overwriting a 2GB Flash Disk to replicate the working
environment for awareness-agent (Mechanicall OS) development.

Contents:
- awareness-agent/   : full source (aether script, docs, scripts, meta-agent skill)
- aether             : the main POSIX sh command (copy to PATH)
- bootstrap-replicate-grok-env.sh : run on target Alpine to set up tools + aether
- packages-from-current-env.txt : full list of packages from the original env

To continue development in another (experimental) environment:
1. Boot or mount this USB on the target machine.
2. Run the bootstrap script (as root on Alpine):
   sh /path/to/usb/bootstrap-replicate-grok-env.sh
3. Use ./aether (or the installed one) and the awareness-agent/ dir.
4. All state lives in plain files: .context.md , .aether/ etc.

This preserves the philosophy: filesystem = single source of truth.
No hidden databases. Markdown + Python + sh.

Created in ghost-user verified mode.
"""

    with open(f"{MOUNT_POINT}/README-GROK-PORTABLE.txt", "w") as f:
        f.write(readme)

    run(f"sync; sleep 1")
    run(f"df -h {MOUNT_POINT}")
    run(f"ls -l {MOUNT_POINT}/ | head -10")
    run(f"lsblk {DEVICE}")

    print("\n[GHOST-USER] === REALITY: USB SUCCESSFULLY OVERWRITTEN AND BOOTSTRAPPED ===")
    print("[GHOST-USER] The 2GB USB now contains the full awareness-agent and bootstrap for current env.")
    print("[GHOST-USER] Unmount when done: umount " + MOUNT_POINT)

    # Cleanup mount
    run(f"umount {MOUNT_POINT} || true")

if __name__ == "__main__":
    main()
