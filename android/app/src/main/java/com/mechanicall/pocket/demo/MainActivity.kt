package com.mechanicall.pocket.demo

import android.graphics.Color
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(this))
        }
        @Suppress("DEPRECATION")
        window.statusBarColor = Color.parseColor("#12100E")
        @Suppress("DEPRECATION")
        window.navigationBarColor = Color.parseColor("#12100E")
        setContent { SeatApp() }
    }
}

@Composable
fun SeatApp() {
    SeatTheme {
        Surface(
            modifier = Modifier.fillMaxSize(),
            color = MaterialTheme.colorScheme.background,
        ) {
            SeatNav()
        }
    }
}
