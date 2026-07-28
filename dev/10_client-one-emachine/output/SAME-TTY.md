# Grok + Panel on the same screen (ops only)

This is a **teaching convenience**, not a new product.  
You still have two programs: **plan/approve** vs **AI chat**.

---

## Option A — one at a time (simplest)

```sh
cd /path/to/project
aether panel    # plan, check allowed, approve
# quit panel (q)
grok            # talk to the AI
# quit grok
aether panel    # check plan again
```

From the panel menu you can also choose **Open Grok in this folder** (if present): it leaves the panel, runs Grok, then comes back. Same terminal, still not “one product.”

---

## Option B — split screen with tmux

If `tmux` is installed:

```sh
cd /path/to/project
tmux new -s work
# Ctrl-b then "  → split top/bottom
# top:    aether panel
# bottom: grok
# Ctrl-b then arrow keys to move between panes
```

Install tmux on Alpine: `apk add tmux`.

---

## What to tell a client

> Top (or first): the **plan** and the **yes/no** buttons.  
> Bottom (or second): the **AI** you talk to.  
> Both look at the same project folder. The AI does not press Approve for you.
