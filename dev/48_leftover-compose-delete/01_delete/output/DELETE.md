# leftover-compose-delete — done

**When:** 2026-08-28  
**Next at start of sitting:** `leftover-compose-delete` APPROVED (clean slate for a new pocket APK).  
**Not Yes.** No sideload. No overlay-Compose assemble.

## Removed

```
android/app/src/main/java/com/mechanicall/pocket/demo/SeatNav.kt
android/app/src/main/java/com/mechanicall/pocket/demo/SeatTheme.kt
android/app/src/main/java/com/mechanicall/pocket/demo/LcdViewer.kt
android/app/src/main/java/com/mechanicall/pocket/demo/SkinLayout.kt
android/app/src/main/java/com/mechanicall/pocket/demo/modules/BindModule.kt
android/app/src/main/java/com/mechanicall/pocket/demo/modules/ChatHome.kt
android/app/src/main/java/com/mechanicall/pocket/demo/modules/DecideModule.kt
android/app/src/main/java/com/mechanicall/pocket/demo/modules/PlanModule.kt
android/app/src/main/java/com/mechanicall/pocket/demo/modules/ReceiptModule.kt
android/app/src/main/java/com/mechanicall/pocket/demo/modules/SplashScreen.kt
android/app/src/main/java/com/mechanicall/pocket/demo/modules/   (empty dir)
```

Script: `01_delete/scripts/delete_leftover_compose.py`

## Kept (native host)

`MainActivity.kt` `SitRackView.kt` `SitCRects.kt` `LawPages.kt` `FaceBridge.kt` `OpenBoundFolder.kt`

## Gradle

Compose BOM / ui / material3 / activity-compose / `buildFeatures { compose }` removed.  
`androidx.activity:activity-ktx:1.9.0` kept for `ComponentActivity`.

## Verify

- `python3 python/app_verify.py` → **10/10**
- `python3 tests/test_app_verify.py` → OK
- `:app:assembleDebug` **did not run** as a successful compile: Gradle 8.11 failed immediately on JDK **26.0.1** (`What went wrong: 26.0.1`). Not an overlay-Compose failure. Native compile proof still needs Temurin 17.

## After this sitting

Human already `aether next aether-mcp-projection` (PENDING). leftover-compose-delete is refused as Next. This factory **halts**; it does not implement the MCP.
