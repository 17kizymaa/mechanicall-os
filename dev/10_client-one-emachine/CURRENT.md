# CURRENT

**Objective:** Android TV is the default power-on experience on client-one (entertainment + light dev); GRUB must stop hijacking every boot.
**Phase:** SELECT
**Status:** READY-FOR-REVIEW
**Baseline:** android-tv-exists-grub-wins
**Next:** inventory-boot
**Approval:** PENDING

## Keep
- Existing Android TV / Android-x86 system and data if mountable
- Win7 archive until explicitly backed up
- Live USB only as recovery tool (no casual grub-install)
- Documented client playbook for next entertainment-device client

## Reject
- Treating Alpine quiet-chat live as the permanent client OS
- Blind partition wipe “to migrate”
- Another Linux install as the easy default without boot inventory

## Limits
- No wipe of android-data or win7 without a named Next
- Ethernet is for logs/SSH when up, not required to fix EFI order
- One boot change per power cycle test

## Next allowed action
Boot live USB (no grub-install), run Phase A inventory (`efibootmgr -v`, `lsblk`, `blkid`, ESP file list), paste results. Action id: `inventory-boot`.

## Approval condition
Optional. Prefer successful cold boot into Android TV over ceremony.

## Prohibited
- wipe-win7-archive
- reformat-android-data
- blind-grub-install
- nag-approve
