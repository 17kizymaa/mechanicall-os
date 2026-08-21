# How to sit (brake face)

**Copy this folder off mechanicall-os first.** Bind the copy, never the git repo.

## You (host)

```bash
# from mechanicall-os
export POCKET_HOST_TWIN="$HOME/mechanicall-pocket"   # or ~/brake-<friend>
# copy this example into that twin if it is empty
# export POCKET_FACE_HOST=<your Tailscale IP>        # if they are not on LAN
sh scripts/send-brake.sh
```

Send the printed URL. Stay on the host until they tap.

## Them (any phone browser)

1. Open the link.
2. Read the **plan**. Opening the page is not a yes.
3. Edit the **draft** if you want. Save does not change the plan.
4. Tap **Yes** or **Not yet**.
5. Tomorrow open `RECEIPT.md` in this folder (or the file they forward you).

## After

Forward `RECEIPT.md`. Do not send them the mechanicall-os tree.

Phone `adb` sync is off unless you set `POCKET_SYNC=1`.
