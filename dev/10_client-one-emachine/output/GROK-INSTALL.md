# Install Grok (the AI you talk to)

**What this is:** a program you run in the terminal to chat with the AI and edit the project.  
**What this is not:** the written plan or the approve buttons (that is `aether panel`).

---

## Before you start

- Internet on the laptop (phone USB tether is fine).
- You can type commands (text screen is fine).

---

## Install

```sh
apk add curl bash ca-certificates
curl -fsSL https://x.ai/cli/install.sh | bash
```

Then make sure the program is on your path (open a new shell, or):

```sh
export PATH="$HOME/.local/bin:$HOME/.grok/bin:$PATH"
grok --version
```

You should see a version number. If not, say so and stop.

---

## Log in (text laptop — use your phone’s browser)

```sh
grok login --device-auth
```

1. The laptop shows a **link** and a **code**.
2. Open the link on your **phone** (or another computer).
3. Sign in and enter the code.
4. Return to the laptop — you are logged in.

(If the laptop has a normal browser, plain `grok login` is also fine.)

---

## Work

```sh
cd /path/to/your/project
grok
```

Talk to the AI there. Stay in the project folder.

---

## Two tools (remember this)

| Tool | Job |
|------|-----|
| **grok** | Talk to the AI and do the work |
| **aether panel** | See the written plan; human yes / no |

Same keyboard and screen is fine. They are still two programs — that is intentional.

See also: `SAME-TTY.md` for a simple split-screen layout.
