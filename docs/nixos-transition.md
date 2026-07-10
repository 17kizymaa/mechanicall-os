# Transitioning Development to NixOS

This guide explains how to move development of **awareness-agent** (Mechanicall OS) from the current Alpine-based environment to a proper NixOS workflow.

The goal is reproducibility, declarative configuration, and alignment with the project's core principles: **filesystem as single source of truth** and **extremely low overhead**.

## Why NixOS?

- `flake.nix` + `shell.nix` now define the exact dev environment (entr for watch, python3 for optional distill).
- `nix develop` gives a hermetic shell with precisely the tools needed — no "works on my machine".
- Pairs perfectly with `.context.md` sidecars: both are declarative, versioned, and inspectable.
- Direnv makes the dev shell automatic on `cd`.

NixOS is the recommended host for contributors and for running agent sessions against this repo.

## Quick Win: Install Only the Nix Package Manager (No Full OS Change)

You can get `nix develop` working **immediately** on the current Alpine (or any Linux/macOS) machine without reinstalling the OS.

1. Install Nix (single-user is simplest for quick start):

   ```sh
   curl -L https://nixos.org/nix/install | sh
   ```

   Follow the on-screen instructions (usually source `~/.nix-profile/etc/profile.d/nix.sh` or restart your shell).

2. Enable flakes (if not already):

   ```sh
   mkdir -p ~/.config/nix
   echo "experimental-features = nix-command flakes" >> ~/.config/nix/nix.conf
   ```

3. Enter the dev shell for this repo:

   ```sh
   cd /path/to/awareness-agent
   nix develop
   ```

   You should see the shell hook: "awareness-agent (Mechanicall OS) — Nix dev shell active"

4. Test:

   ```sh
   ./aether status
   ./aether watch   # now has real entr
   ```

This gives you 90% of the benefit today.

## Full Transition: Install NixOS as Your Development OS

### 1. Download the ISO

Go to the official download page:

https://nixos.org/download/

Recommended:
- **Graphical ISO** (easier for first install, includes a desktop installer).
- Or **Minimal ISO** (smaller, console-only).

Current stable channel is usually 26.05 or newer (check the site).

### 2. Create Bootable Media

- Linux: use `dd` or a tool like `popsicle` / Ventoy.
- From another OS: use Rufus, balenaEtcher, or `dd` under WSL/macOS.

Example (Linux, replace `/dev/sdX` carefully):

```sh
sudo dd if=nixos-minimal-*.iso of=/dev/sdX bs=4M status=progress && sync
```

### 3. Boot the ISO and Install

Follow the official manual:

- https://nixos.org/manual/nixos/stable/#ch-installation
- Companion wiki guide: https://wiki.nixos.org/wiki/NixOS_Installation_Guide

Basic flow (minimal installer):
1. Partition the disk (e.g. with `cfdisk`).
2. Format (usually ext4 + optional swap or zfs/btrfs).
3. Mount under `/mnt`.
4. Generate initial config:

   ```sh
   nixos-generate-config --root /mnt
   ```

5. Edit `/mnt/etc/nixos/configuration.nix` (enable flakes here too).
6. Install:

   ```sh
   nixos-install
   ```

7. Reboot and set a password for your user.

### 4. Enable Flakes and Modern Nix

After first boot, as your user:

```sh
mkdir -p ~/.config/nix
echo "experimental-features = nix-command flakes" >> ~/.config/nix/nix.conf
```

(You can also declare this in `configuration.nix` under `nix.settings`.)

### 5. Set Up This Repository

```sh
git clone https://.../awareness-agent.git   # or copy your current tree
cd awareness-agent
```

### 6. Activate the Dev Shell (manual)

```sh
nix develop
```

Inside the shell you now have `entr`, `python3`, and the environment described in `flake.nix`.

### 7. Make It Automatic with direnv (Strongly Recommended)

1. Install direnv (via Nix or your system package):

   ```sh
   nix profile install nixpkgs#direnv
   ```

2. Hook direnv into your shell (example for bash/zsh — see https://direnv.net/docs/hook.html):

   ```sh
   # Add to ~/.bashrc or ~/.zshrc
   eval "$(direnv hook bash)"
   ```

3. In the repo root, create `.envrc`:

   ```sh
   echo 'use flake' > .envrc
   direnv allow
   ```

Now, every time you `cd` into the awareness-agent directory, direnv automatically loads the exact dev shell (entr + python3). Exit the directory and the environment is unloaded.

Create `.envrc` in any project you want to make self-aware later.

### 8. Verify Everything Works

Inside the (auto) dev shell:

```sh
./aether init
./aether distill
./aether watch   # should use real entr, not polling fallback
```

Edit files and watch sidecars update. Everything stays in the filesystem.

## Working with the Agent on NixOS

- Run your normal Grok / CLI sessions from a terminal inside the `nix develop` (or direnv) shell.
- The `flake.nix` ensures that `entr` (critical for `aether watch`) and Python are always the exact versions you expect.
- Your `.context.md`, `.aether/`, and project sidecars remain pure markdown + json — fully compatible.
- For long-running watch sessions, the dev shell keeps the tools alive.

## VM / Container Option (Keep Current Host)

If you don't want to replace your current OS yet:

- Run NixOS as a VM (QEMU + virt-manager on Linux, UTM on macOS, etc.).
- Or use `nix develop` + the package manager install above on your existing host.
- The repo's `flake.nix` works identically.

Full NixOS on the bare machine (or primary development VM) is the cleanest long-term match for the philosophy.

## Next Steps After Transition

- Commit `flake.nix`, `shell.nix`, and this guide.
- Add a `.envrc` (consider gitignoring it or committing a `.envrc.example`).
- Update any personal notes or other projects' sidecars.
- Optionally pin the flake input with `nix flake update` and commit `flake.lock` for exact reproducibility.

## References

- Official NixOS manual: https://nixos.org/manual/nixos/stable
- Download ISOs: https://nixos.org/download/
- direnv + flakes: https://determinate.systems/blog/nix-direnv/
- This project's philosophy: [CORE_PRINCIPLES.md](../CORE_PRINCIPLES.md) and [SPEC-v0.1.md](../SPEC-v0.1.md)

The infrastructure disappears. Your folders (and now your dev shells) just work.
