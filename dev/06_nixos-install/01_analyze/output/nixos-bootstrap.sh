#!/bin/sh
# nixos-bootstrap.sh
# Run this on first boot of the new NixOS (as root or with sudo)
# It transfers "this project" (awareness-agent) from the USB and bootstraps
# the full environment (aether, meta-agent, sidecars) E2E.

set -e

USB_MOUNT="/media/usb"   # adjust if different, e.g. /mnt/usb when mounted
REPO_SRC="$USB_MOUNT/awareness-agent"
TARGET_REPO="/opt/awareness-agent"

echo "=== Transferring awareness-agent project to new NixOS environment (minimal headless) ==="

if [ ! -d "$REPO_SRC" ]; then
  echo "USB not mounted or awareness-agent not found at $REPO_SRC"
  echo "Mount your USB (the sdb one with GROK-PORTABLE-DE) and rerun."
  exit 1
fi

mkdir -p /opt
cp -a "$REPO_SRC" "$TARGET_REPO"
echo "Repo copied to $TARGET_REPO"

# Install aether globally
cp "$TARGET_REPO/aether" /usr/local/bin/aether
chmod +x /usr/local/bin/aether
echo "aether installed to /usr/local/bin"

# Shell integration (for the awareness user)
USER_HOME="/home/awareness"
mkdir -p "$USER_HOME"
python3 "$TARGET_REPO/scripts/emit_aether_snippet.py" >> "$USER_HOME/.bashrc" || true
echo 'export PATH="/usr/local/bin:$PATH"' >> "$USER_HOME/.bashrc" || true

# Initialize the project sidecars (E2E transfer) - minimal
cd "$TARGET_REPO"
./aether init || true
./aether distill || true

# Example project to make "alive" immediately (TTY/headless dev)
mkdir -p /home/awareness/projects/example
cd /home/awareness/projects/example
"$TARGET_REPO/aether" init || true
echo "# New NixOS project (mbp-nix, terminal-only)" > README.md
"$TARGET_REPO/aether" distill || true

echo ""
echo "=== E2E Complete ==="
echo "awareness-agent is now in $TARGET_REPO"
echo "Run: aether status"
echo "Edit .context.md files. The meta-agent skill is at $TARGET_REPO/.grok/skills/meta-agent/"
echo "Your Grok sessions on this new NixOS will have full filesystem awareness."
echo ""
echo "To continue development: cd $TARGET_REPO && source the shell integration."
echo "rEFInd should detect the NixOS install. Add manual entry if needed for /dev/sda4."
echo ""
echo "For Grok Build CLI reinstall: Connect Ethernet, then use curl/wget or nix for fast setup of tools."
