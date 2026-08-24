import java.util.Properties

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("com.chaquo.python")
}

val playPropsFile = file("${System.getProperty("user.home")}/.mechanicall/play-upload.properties")
val playProps = Properties()
if (playPropsFile.isFile) {
    playPropsFile.inputStream().use { playProps.load(it) }
}

android {
    namespace = "com.mechanicall.pocket.demo"
    compileSdk = 36
    defaultConfig {
        applicationId = "com.mechanicall.pocket.demo"
        minSdk = 26
        targetSdk = 36
        versionCode = 22
        versionName = "0.17.1-api36"
        ndk {
            abiFilters += listOf("arm64-v8a", "x86_64")
        }
    }
    if (playPropsFile.isFile) {
        signingConfigs {
            create("play") {
                storeFile = file(playProps.getProperty("storeFile"))
                storePassword = playProps.getProperty("storePassword")
                keyAlias = playProps.getProperty("keyAlias")
                keyPassword = playProps.getProperty("keyPassword")
            }
        }
    }
    buildTypes {
        release {
            isMinifyEnabled = false
            if (playPropsFile.isFile) {
                signingConfig = signingConfigs.getByName("play")
            }
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
    buildFeatures { compose = true }
    composeOptions { kotlinCompilerExtensionVersion = "1.5.14" }
    packaging {
        jniLibs {
            useLegacyPackaging = false
        }
    }
}

chaquopy {
    defaultConfig {
        version = "3.11"
    }
}

dependencies {
    implementation(platform("androidx.compose:compose-bom:2024.06.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.activity:activity-compose:1.9.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.2")
}
