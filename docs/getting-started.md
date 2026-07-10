# Getting Started with aether

## Install / Activate (no installation needed)

The entire system is the files in this directory.

```bash
# From anywhere, using the repo directly:
PYTHONPATH=/home/awareness-agent python3 -m aether --help

# Recommended: add to your shell once
python3 /home/awareness-agent/scripts/emit_aether_snippet.py >> ~/.bashrc
source ~/.bashrc

aether --help
```

## Recommended: Develop on NixOS

This repository targets NixOS for contributor and agent development environments (reproducible toolchains, zero hidden state).

**Full transition instructions** (including quick "just install Nix" path and full OS install): see [docs/nixos-transition.md](./nixos-transition.md).

From the repo root:

```bash
nix develop
# Now entr + python3 are in PATH for aether watch / distill.

./aether status
./aether init   # in another folder you are making self-aware
```

With direnv (highly recommended on NixOS):

```bash
echo 'use flake' > .envrc
direnv allow
```

A classic `shell.nix` is also present for `nix-shell` users.

No other dependencies. The core `aether` script is pure POSIX sh.

## Bootstrap a new project

```bash
cd ~/my-cool-project
aether init
aether update
cat .context.md
```

## Keep it fresh

```bash
# One-shot
aether update

# Continuous
aether watch   # uses simple polling in v0
```

Edit `.context.md` or `.memory/*` yourself anytime — aether treats them as the source of truth.

## Inspect everything

```bash
ls -a
cat .context.md
cat .awareness.json
tree .memory || ls .memory
grep -r "TODO" .context.md .memory
```

No black boxes.
