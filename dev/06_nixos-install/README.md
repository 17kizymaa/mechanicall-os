# 06_nixos-install

ICM workspace created 2026-06-26T22:19:41

Description: Install NixOS as a new 300GB partition on /dev/sda by repurposing space from the current Alpine sda3 (overwriting ~300GB of the large Alpine root allocation), using the current session as mounting bridge where possible. Include full verification, safety, and bootstrap for the new NixOS system with awareness-agent.

See CONTEXT.md and each stage's CONTEXT.md.
Run the meta-agent skill (/meta-agent) and point it at this folder.

Stages are sequential with review gates at each output/ directory.
