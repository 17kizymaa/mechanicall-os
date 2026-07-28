# Get SSH working over phone USB tether

**Goal:** Reach the small laptop (eMachine) from this PC using the phone’s USB connection.  
**Wi‑Fi can wait.** Tether first.

---

## On the small laptop

1. Plug the phone into the laptop with a USB cable.
2. On the phone, turn on **USB tethering** (sometimes under Hotspot / Network).
3. On the laptop (text screen is fine), type:

```sh
ip link
```

Look for a new name such as `usb0` or `rndis0`.

4. Bring it up and ask for an address:

```sh
ip link set usb0 up
udhcpc -i usb0
ip -4 addr show usb0
```

(If the name is not `usb0`, use the name you saw.)

5. Install and start SSH if needed:

```sh
apk add openssh
rc-update add sshd default
service sshd start
passwd
```

6. Write down the **IP address** (numbers like `192.168.42.61`).

---

## On this PC (operator)

```sh
ping -c 2 THE_IP_FROM_ABOVE
ssh root@THE_IP_FROM_ABOVE
```

If ping fails, the phone network may only be visible *on the laptop*. Then use one of:

- Sit at the laptop keyboard (still fine for install), or  
- Install Tailscale on the laptop over tether and connect by Tailscale IP, or  
- Ethernet cable between the two machines if you have one.

---

## Done when

- You can open a remote shell on the laptop, **or** you are working at its keyboard with internet via tether.

Wi‑Fi repair is a later step, not this one.
