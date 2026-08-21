package com.mechanicall.pocket.demo.modules

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Text
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.mechanicall.pocket.demo.PluginDialogFrame
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.lerp
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.mechanicall.pocket.demo.FaceBridge
import com.mechanicall.pocket.demo.SeatPalette
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

@Composable
fun DecideModule(
    pocket: String,
    onReload: () -> Unit,
) {
    var armed by remember { mutableStateOf<String?>(null) }
    var dialog by remember { mutableStateOf<String?>(null) }
    var why by remember { mutableStateOf("") }
    var busy by remember { mutableStateOf(false) }
    var note by remember { mutableStateOf("") }
    val scope = rememberCoroutineScope()
    val armFade = remember { Animatable(0f) }

    LaunchedEffect(armed, dialog) {
        if (armed == null || dialog != null) {
            if (armed == null) armFade.snapTo(0f)
            return@LaunchedEffect
        }
        armFade.snapTo(1f)
        armFade.animateTo(0f, animationSpec = tween(2000, easing = LinearEasing))
        if (dialog == null) {
            armed = null
        }
    }

    Column(
        Modifier
            .fillMaxSize()
            .padding(10.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp),
    ) {
        if (note.isNotBlank()) {
            Text(
                note,
                fontFamily = FontFamily.Monospace,
                fontSize = 11.sp,
                color = SeatPalette.Lcd,
            )
        }
        DecidePad(
            restLabel = "YES",
            armedLabel = "AGAIN",
            fade = if (armed == "approve") armFade.value else 0f,
            fill = true,
            enabled = !busy,
            modifier = Modifier.weight(1f),
            onClick = {
                if (armed == "approve") {
                    dialog = "approve"
                } else {
                    armed = "approve"
                    dialog = null
                }
            },
        )
        DecidePad(
            restLabel = "NOT YET",
            armedLabel = "AGAIN",
            fade = if (armed == "reject") armFade.value else 0f,
            fill = false,
            enabled = !busy,
            modifier = Modifier.weight(1f),
            onClick = {
                if (armed == "reject") {
                    dialog = "reject"
                } else {
                    armed = "reject"
                    dialog = null
                }
            },
        )
    }

    val open = dialog
    if (open != null) {
        val approve = open == "approve"
        Dialog(
            onDismissRequest = {
                dialog = null
                armed = null
            },
            properties = DialogProperties(
                usePlatformDefaultWidth = false,
                dismissOnClickOutside = true,
            ),
        ) {
            PluginDialogFrame(
                title = if (approve) "PUBLISH" else "NOT YET",
                actionLabel = "CANCEL",
                onAction = {
                    dialog = null
                    armed = null
                },
                onScrim = {
                    dialog = null
                    armed = null
                },
            ) {
                Text(
                    "Publish the proposal. Why? (required). JOIN, WAKE, Send, hunk accept are not Yes.",
                    fontFamily = FontFamily.Monospace,
                    fontSize = 12.sp,
                    color = SeatPalette.Lcd,
                )
                Spacer(Modifier.height(8.dp))
                OutlinedTextField(
                    value = why,
                    onValueChange = { why = it },
                    modifier = Modifier.fillMaxWidth(),
                    minLines = 3,
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedTextColor = SeatPalette.Lcd,
                        unfocusedTextColor = SeatPalette.Lcd,
                        focusedBorderColor = SeatPalette.Lcd,
                        unfocusedBorderColor = SeatPalette.BevelLite,
                        cursorColor = SeatPalette.Lcd,
                        focusedContainerColor = SeatPalette.LcdBg,
                        unfocusedContainerColor = SeatPalette.LcdBg,
                    ),
                )
                Spacer(Modifier.height(10.dp))
                Box(
                    Modifier
                        .fillMaxWidth()
                        .height(56.dp)
                        .border(2.dp, SeatPalette.BevelLite)
                        .background(
                            if (!busy && why.isNotBlank()) SeatPalette.LcdBg else SeatPalette.PanelDark,
                        )
                        .clickable(enabled = !busy && why.isNotBlank()) {
                            val reason = why
                            val kind = open
                            dialog = null
                            armed = null
                            scope.launch {
                                busy = true
                                val raw = withContext(Dispatchers.IO) {
                                    if (kind == "approve") {
                                        FaceBridge.yes(pocket, reason)
                                    } else {
                                        FaceBridge.notYet(pocket, reason)
                                    }
                                }
                                note = FaceBridge.asText(raw)
                                busy = false
                                onReload()
                            }
                        },
                    contentAlignment = Alignment.Center,
                ) {
                    Text(
                        "Confirm",
                        color = if (why.isNotBlank()) SeatPalette.Lcd else SeatPalette.BevelLite,
                        fontSize = 16.sp,
                        fontFamily = FontFamily.Monospace,
                        fontWeight = FontWeight.Bold,
                    )
                }
            }
        }
    }
}

@Composable
private fun DecidePad(
    restLabel: String,
    armedLabel: String,
    fade: Float,
    fill: Boolean,
    enabled: Boolean,
    modifier: Modifier,
    onClick: () -> Unit,
) {
    val t = fade.coerceIn(0f, 1f)
    val restBg = if (fill) SeatPalette.LcdBg else SeatPalette.PanelDark
    val restFg = if (fill) SeatPalette.Lcd else SeatPalette.BevelLite
    val bg = lerp(restBg, SeatPalette.Purple, t)
    val restFgMixed = lerp(restFg, SeatPalette.Lcd, t)
    Box(
        modifier
            .fillMaxWidth()
            .border(2.dp, SeatPalette.BevelLite)
            .background(bg)
            .clickable(enabled = enabled, onClick = onClick),
        contentAlignment = Alignment.Center,
    ) {
        Box(contentAlignment = Alignment.Center) {
            Text(
                restLabel,
                color = restFgMixed.copy(alpha = 1f - t),
                fontSize = 28.sp,
                fontFamily = FontFamily.Monospace,
                fontWeight = FontWeight.Bold,
            )
            Text(
                armedLabel,
                color = SeatPalette.Lcd.copy(alpha = t),
                fontSize = 28.sp,
                fontFamily = FontFamily.Monospace,
                fontWeight = FontWeight.Bold,
            )
        }
    }
}
