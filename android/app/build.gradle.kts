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
        versionCode = 29
        versionName = "0.19.4-dest-preview"
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
    implementation("androidx.activity:activity-ktx:1.9.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.2")
}
