# CONSOLE — Play **internal** upload pack

**Not production. Not Funnel. Not Yes.** Agent does not log in. Human uploads.

## Artifact

- File (gitignored): `android/app/build/outputs/bundle/release/app-release.aab` (23M)
- SHA-256: `5442e4557b81ac9c7b011b9174a09372dda0b8bbeaa530cc214c0720e5b5c952`
- versionName `0.17.1-api36` · versionCode **22** · targetSdk **36**
- Signed with off-git PKCS12 **upload** key: `~/.mechanicall/play-upload.jks`
- Cert SHA-256: `51:AE:5D:F0:11:E4:0B:B5:EE:25:32:56:43:2D:D8:D0:4E:C0:9F:3B:21:22:F3:68:09:37:0C:E8:C4:65:A8:58`
- Rebuild: `sh scripts/play-bundle.sh` (needs `~/.mechanicall/play-upload.properties`)

**Backup** `~/.mechanicall/play-upload.jks` + `play-upload.properties` before first upload. Losing them means you cannot update this listing. Password is only in that properties file. Not in git. Not in this receipt.

## Listing files in git

- Copy: `android/play-listing/STORE-COPY.md`
- Privacy text: `android/play-listing/PRIVACY.md` (host it, then paste the URL in Console)
- Icon 512: `android/play-listing/icon-512.png`
- Feature 1024×500: `android/play-listing/feature-1024x500.png`
- Limitations testers must see: `android/KNOWN-LIMITATIONS.md`

## Human Console steps

1. play.google.com/console → create app `com.mechanicall.pocket.demo` if needed ($25).
2. Testing → **Internal testing** (or Closed if you need an email list). Not production.
3. Upload the **signed** AAB above. First upload **locks** the upload key to this cert.
4. Paste store copy. Data safety from STORE-COPY.md. Declare All files access as core (folder bind). Declare cleartext LAN desk as optional / not encrypted.
5. Add testers. Do **not** list LTE folder-send.
6. CURRENT still wants an LTE sideload receipt before you click upload (`04_lte-receipt` is BLOCKED this sitting). That is your call vs law — this agent will not recant it.

Production rollout stays Reject.
