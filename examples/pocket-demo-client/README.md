# Pocket / brake sitting (template)

**LAB / example.** Copy this folder **outside** `mechanicall-os`.  
The brake face and the demo APK bind *that* copy — never this repo.

Sitting walk: [HOW-TO-SIT.md](./HOW-TO-SIT.md)  
Vision: `dev/23_mobile-planning-demo/output/BRAKE.md`

```bash
# URL first (host):
cp -a examples/pocket-demo-client/. ~/mechanicall-pocket
sh scripts/send-brake.sh
# send the printed URL

# Phone copy (optional, A33 via edge):
sh scripts/push-pocket-via-edge.sh
```

Host twin (dev): `~/mechanicall-pocket`

Do **not** bind `/sdcard/mechanicall` (existing sessions tree) or this git repo.

APK (second): sideload `android/` lab chrome; same pocket path. Not Play Store.
