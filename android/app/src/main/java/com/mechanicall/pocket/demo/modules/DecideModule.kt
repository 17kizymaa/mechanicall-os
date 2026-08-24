package com.mechanicall.pocket.demo.modules

import androidx.compose.animation.core.Animatable
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
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
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
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
    val armFill = remember { Animatable(0f) }

    LaunchedEffect(armed, dialog) {
        if (armed == null || dialog != null) {
            if (armed == null) armFill.snapTo(0f)
            return@LaunchedEffect
        }
        // Fast arm. Stay up so a second tap is anticipated. No gold-on-gold.
        armFill.snapTo(0f)
        repeat(5) { i ->
            armFill.snapTo((i + 1) / 5f)
            kotlinx.coroutines.delay(18)
        }
        kotlinx.coroutines.delay(2800)
        if (dialog == null) {
            for (i in 4 downTo 0) {
                armFill.snapTo(i / 5f)
                kotlinx.coroutines.delay(16)
            }
            if (dialog == null) armed = null
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
        Text(
            "Publish the proposal. Not hunk pick. Why is required.",
            fontFamily = FontFamily.Monospace,
            fontSize = 11.sp,
            fontWeight = FontWeight.Bold,
            color = SeatPalette.Ink,
            modifier = Modifier.semantics { contentDescription = "Publish the proposal" },
        )
        DecidePad(
            restLabel = "YES",
            armedLabel = "AGAIN",
            fillAmount = if (armed == "approve") armFill.value else 0f,
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
            fillAmount = if (armed == "reject") armFill.value else 0f,
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
                    "Publish the proposal. Why? (required).",
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
    fillAmount: Float,
    fill: Boolean,
    enabled: Boolean,
    modifier: Modifier,
    onClick: () -> Unit,
) {
    val t = fillAmount.coerceIn(0f, 1f)
    val restBg = if (fill) SeatPalette.LcdBg else SeatPalette.PanelDark
    val restFg = if (fill) SeatPalette.Lcd else SeatPalette.Ink
    val rise = if (fill) SeatPalette.Panel else SeatPalette.Purple
    val armed = t >= 0.99f
    Box(
        modifier
            .fillMaxWidth()
            .border(3.dp, SeatPalette.BevelDark)
            .padding(2.dp)
            .border(2.dp, SeatPalette.BevelLite)
            .padding(2.dp)
            .border(1.dp, SeatPalette.BevelDark)
            .background(restBg)
            .clickable(enabled = enabled, onClick = onClick),
        contentAlignment = Alignment.Center,
    ) {
        Box(
            Modifier
                .align(Alignment.BottomCenter)
                .fillMaxWidth()
                .fillMaxHeight(t)
                .background(rise),
        )
        Box(
            Modifier
                .background(if (armed) rise else restBg)
                .padding(horizontal = 18.dp, vertical = 10.dp),
        ) {
            Text(
                if (armed) armedLabel else restLabel,
                color = if (armed) SeatPalette.Ink else restFg,
                fontSize = 28.sp,
                fontFamily = FontFamily.Monospace,
                fontWeight = FontWeight.Bold,
            )
        }
    }
}
