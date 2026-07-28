# Direct Ethernet: MBP ↔ eMachine

Skip the USB WiFi partition. Use a normal Ethernet cable (auto-MDIX).

| End | Address |
|-----|---------|
| MBP `eth0` | **10.99.99.1/24** |
| eMachine `eth0` | **10.99.99.2/24** |

Kit on MBP: `/home/anphuni/emachine-eth-link/`

## eMachine (hand-copy)

```sh
ip link set eth0 up
ip addr flush dev eth0
ip addr add 10.99.99.2/24 dev eth0
ip link set eth0 up
ping -c 2 10.99.99.1
# sshd if available:
sshd 2>/dev/null || rc-service sshd start 2>/dev/null || true
```

## MBP

```sh
sudo sh /home/anphuni/emachine-eth-link/mbp-eth-up.sh
ping -c 2 10.99.99.2
ssh root@10.99.99.2
# then push WiFi:
sudo sh /home/anphuni/emachine-eth-link/push-wifi-over-eth.sh
```

From operator PC once both on WiFi later: use LAN IPs again.
