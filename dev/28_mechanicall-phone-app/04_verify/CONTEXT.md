## Inputs
- Layer 4: ../03_implement/output/FACE-DONE.md
- Layer 3: ../../android/README.md

## Process
Assemble debug APK with JDK 17 + SDK 34. Do not claim APK exists if gradlew fails.

```
export JAVA_HOME="$HOME/.jdk/temurin-17"
export ANDROID_HOME="$HOME/.android-sdk-mechanicall"
cd android && ./gradlew :app:assembleDebug
```

## Outputs
- ASSEMBLE.md -> output/
