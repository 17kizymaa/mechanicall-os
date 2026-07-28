# Dev workflow: rebuild in a **VM on Arch**, not on the Kingston stick

## Why

Stick rebuilds hit submodule `.git`, hostname/attr mismatches, and tight disk.  
The VM exists so you fix NixOS **here**, then deploy to the stick when green.

```text
Arch (myarch)  ──KVM──►  NixOS guest #portable-kingston-vm
   edit flake                    aether panel / test
   scripts/vm/dev-up.sh

Physical Kingston  =  deploy target only (sync + rare rebuild when known-good)
```

## One command

```bash
cd ~/mechanicall-os
sh scripts/vm/dev-eval.sh    # optional, fast
sh scripts/vm/dev-up.sh      # build + boot guest (long first time)
```

Login: **`operator` / `operator`**  
Shared tree: **`/mnt/host/mechanicall-os`**  
Then: `aether panel` or `aether panel --dump`

## After module/flake changes

Re-run `dev-up.sh` (rebuilds the runner). No USB required.

## Stick (only when VM is good)

```bash
# from Arch, stick mounted:
sh scripts/sync-to-kingston.sh
# boot stick, then:
sudo /opt/mechanicall-os/scripts/rebuild-portable-kingston.sh
```

## Optional extras

| Script | Role |
|--------|------|
| `create-qcow.sh` | Persistent 40G disk (later) |
| `arch-guest-*.sh` | If NixOS is host and Arch is guest (role swap) |
| `run-build-vm.sh` | Alias-ish; prefer `dev-up.sh` |

## Flake attrs

| Attr | Use |
|------|-----|
| `portable-kingston-vm` | This dev guest |
| `portable-kingston` / `mechanicall-portable` | Physical stick |
