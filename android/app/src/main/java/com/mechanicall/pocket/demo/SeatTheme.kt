package com.mechanicall.pocket.demo

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.systemBarsPadding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

object SeatPalette {
    val Host = Color(0xFFE8E0D0)
    val Panel = Color(0xFFF3ECDD)
    val PanelDark = Color(0xFFE2D8C6)
    val Title = Color(0xFF2E2E2C)
    val BevelLite = Color(0xFFC8C4BC)
    val BevelDark = Color(0xFF1A1A18)
    val LcdBg = Color(0xFF14120A)
    val Lcd = Color(0xFFE6C14A)
    val Purple = Color(0xFF6A3EA1)
    val PurpleDim = Color(0xFF3A245A)
    val Amber = Color(0xFFE6C14A)
    val Ink = Color(0xFF1B1814)
    val Cream = Color(0xFFF3ECDD)
    val Navy = Color(0xFF2E2E2C)
    val Surface = Color(0xFFF3ECDD)
    val Suggest = Color(0xFF6A3EA1)
    val Strike = Color(0xFF8A4030)
}

@Composable
fun SeatTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = darkColorScheme(
            primary = SeatPalette.Lcd,
            onPrimary = SeatPalette.Ink,
            secondary = SeatPalette.Purple,
            background = SeatPalette.Host,
            surface = SeatPalette.Panel,
            onBackground = SeatPalette.Lcd,
            onSurface = SeatPalette.Ink,
            error = Color(0xFFC45A4A),
        ),
        content = content,
    )
}

@Composable
fun PluginWindow(content: @Composable ColumnScope.() -> Unit) {
    // Fill the activity. Painted letterbox (360×560 on a black host) was a fake
    // window: cramped, IME ate Send, and it is not OS freeform. resizeableActivity
    // stays in the manifest so Samsung pop-up / split-screen can still shrink us.
    Column(
        Modifier
            .fillMaxSize()
            .background(SeatPalette.Host)
            .systemBarsPadding()
            .imePadding()
            .padding(6.dp)
            .border(1.dp, SeatPalette.BevelLite)
            .border(2.dp, SeatPalette.BevelDark)
            .background(SeatPalette.Panel),
        content = content,
    )
}

@Composable
fun PluginTitleBar(
    title: String,
    showSlots: Boolean,
    onFolder: () -> Unit,
    onFiles: () -> Unit,
) {
    Row(
        Modifier
            .fillMaxWidth()
            .height(36.dp)
            .background(SeatPalette.Title)
            .border(1.dp, SeatPalette.BevelDark)
            .padding(horizontal = 8.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(6.dp),
    ) {
        Text(
            "MECHANICALL",
            color = SeatPalette.BevelLite,
            fontSize = 11.sp,
            fontFamily = FontFamily.Monospace,
            fontWeight = FontWeight.Bold,
        )
        Text(
            title,
            color = SeatPalette.Lcd,
            fontSize = 11.sp,
            fontFamily = FontFamily.Monospace,
            modifier = Modifier.weight(1f),
        )
        if (showSlots) {
            ChromeBtn("DIR", onFolder)
            ChromeBtn("FILES", onFiles)
        }
    }
}

@Composable
fun DeskStrip(
    joinStatus: String,
    wakeStatus: String,
    paste: String,
    onPaste: (String) -> Unit,
    onJoin: () -> Unit,
    onWake: () -> Unit,
    joinEnabled: Boolean,
    wakeEnabled: Boolean,
    note: String,
    offerNotify: Boolean = false,
    offerKind: String = "",
    onAcceptOffer: () -> Unit = {},
    onDeclineOffer: () -> Unit = {},
    onStageUpload: () -> Unit = {},
) {
    Column(
        Modifier
            .fillMaxWidth()
            .background(SeatPalette.PanelDark)
            .border(1.dp, SeatPalette.BevelDark)
            .padding(6.dp),
        verticalArrangement = Arrangement.spacedBy(4.dp),
    ) {
        Row(
            Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(6.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text(
                "JOIN ${joinStatus.uppercase()}",
                color = SeatPalette.Ink,
                fontSize = 10.sp,
                fontFamily = FontFamily.Monospace,
                fontWeight = FontWeight.Bold,
                modifier = Modifier
                    .border(1.dp, SeatPalette.BevelDark)
                    .background(if (joinEnabled) SeatPalette.BevelLite else SeatPalette.Panel)
                    .clickable(enabled = joinEnabled, onClick = onJoin)
                    .padding(horizontal = 8.dp, vertical = 6.dp),
            )
            Text(
                "WAKE ${wakeStatus.uppercase()}",
                color = SeatPalette.Ink,
                fontSize = 10.sp,
                fontFamily = FontFamily.Monospace,
                fontWeight = FontWeight.Bold,
                modifier = Modifier
                    .border(1.dp, SeatPalette.BevelDark)
                    .background(if (wakeEnabled) SeatPalette.Lcd else SeatPalette.Panel)
                    .clickable(enabled = wakeEnabled, onClick = onWake)
                    .padding(horizontal = 8.dp, vertical = 6.dp),
            )
        }
        androidx.compose.material3.OutlinedTextField(
            value = paste,
            onValueChange = onPaste,
            label = { Text("preauth / login-server · not stored") },
            modifier = Modifier.fillMaxWidth(),
            minLines = 1,
            colors = androidx.compose.material3.OutlinedTextFieldDefaults.colors(
                focusedTextColor = SeatPalette.Ink,
                unfocusedTextColor = SeatPalette.Ink,
                focusedBorderColor = SeatPalette.BevelDark,
                unfocusedBorderColor = SeatPalette.BevelDark,
                cursorColor = SeatPalette.Ink,
                focusedLabelColor = SeatPalette.Ink,
                unfocusedLabelColor = SeatPalette.BevelDark,
                focusedContainerColor = SeatPalette.Panel,
                unfocusedContainerColor = SeatPalette.Panel,
            ),
        )
        if (offerNotify) {
            Text(
                "OFFER ${offerKind.ifBlank { "folder" }.uppercase()} · Accept is not Yes",
                color = SeatPalette.Suggest,
                fontSize = 10.sp,
                fontFamily = FontFamily.Monospace,
                fontWeight = FontWeight.Bold,
            )
            Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                Text(
                    "ACCEPT",
                    color = SeatPalette.Ink,
                    fontSize = 10.sp,
                    fontFamily = FontFamily.Monospace,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier
                        .border(1.dp, SeatPalette.BevelDark)
                        .background(SeatPalette.Lcd)
                        .clickable(onClick = onAcceptOffer)
                        .padding(horizontal = 8.dp, vertical = 6.dp),
                )
                Text(
                    "DECLINE",
                    color = SeatPalette.Ink,
                    fontSize = 10.sp,
                    fontFamily = FontFamily.Monospace,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier
                        .border(1.dp, SeatPalette.BevelDark)
                        .background(SeatPalette.BevelLite)
                        .clickable(onClick = onDeclineOffer)
                        .padding(horizontal = 8.dp, vertical = 6.dp),
                )
            }
        }
        Text(
            "SEND FOLDER · depreciated · not Yes",
            color = SeatPalette.BevelDark,
            fontSize = 10.sp,
            fontFamily = FontFamily.Monospace,
            fontWeight = FontWeight.Bold,
            modifier = Modifier
                .border(1.dp, SeatPalette.BevelDark)
                .clickable(onClick = onStageUpload)
                .padding(horizontal = 8.dp, vertical = 6.dp),
        )
        if (note.isNotBlank()) {
            Text(
                note,
                color = SeatPalette.Ink,
                fontSize = 10.sp,
                fontFamily = FontFamily.Monospace,
            )
        }
    }
}

@Composable
private fun ChromeBtn(label: String, onClick: () -> Unit) {
    Text(
        label,
        color = SeatPalette.Ink,
        fontSize = 11.sp,
        fontFamily = FontFamily.Monospace,
        fontWeight = FontWeight.Bold,
        modifier = Modifier
            .border(1.dp, SeatPalette.BevelDark)
            .background(SeatPalette.BevelLite)
            .clickable(onClick = onClick)
            .padding(horizontal = 8.dp, vertical = 4.dp),
    )
}

@Composable
fun PluginTabs(
    items: List<Pair<String, String>>,
    selected: String,
    onSelect: (String) -> Unit,
) {
    Row(
        Modifier
            .fillMaxWidth()
            .height(32.dp)
            .background(SeatPalette.PanelDark)
            .padding(horizontal = 4.dp, vertical = 3.dp),
        horizontalArrangement = Arrangement.spacedBy(3.dp),
    ) {
        items.forEach { (key, label) ->
            val on = key == selected
            Text(
                label,
                color = if (on) SeatPalette.Lcd else SeatPalette.BevelLite,
                fontSize = 11.sp,
                fontFamily = FontFamily.Monospace,
                fontWeight = if (on) FontWeight.Bold else FontWeight.Normal,
                textAlign = TextAlign.Center,
                modifier = Modifier
                    .weight(1f)
                    .fillMaxHeight()
                    .border(1.dp, if (on) SeatPalette.Lcd else SeatPalette.BevelDark)
                    .background(if (on) SeatPalette.LcdBg else SeatPalette.Panel)
                    .clickable { onSelect(key) }
                    .padding(top = 3.dp),
            )
        }
    }
}

@Composable
fun LcdStrip(text: String) {
    Box(
        Modifier
            .fillMaxWidth()
            .height(28.dp)
            .background(SeatPalette.LcdBg)
            .border(1.dp, SeatPalette.BevelDark)
            .padding(horizontal = 6.dp),
        contentAlignment = Alignment.CenterStart,
    ) {
        Text(
            text,
            color = SeatPalette.Lcd,
            fontSize = 13.sp,
            fontFamily = FontFamily.Monospace,
            maxLines = 1,
        )
    }
}

@Composable
fun GateStrip(
    state: String,
    step: Int,
    steps: Int = 16,
    deskOn: Boolean,
    queue: Int = 0,
) {
    val phase = when (state) {
        "load" -> "LOAD"
        "gate" -> "STREAM"
        "queued" -> "QUEUE"
        else -> state.uppercase()
    }
    val loading = state == "load"
    val streaming = state == "gate"
    Column(
        Modifier
            .fillMaxWidth()
            .background(SeatPalette.LcdBg)
            .border(1.dp, SeatPalette.BevelDark)
            .padding(horizontal = 6.dp, vertical = 3.dp),
    ) {
        Row(
            Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
        ) {
            Text(
                "GATE $phase",
                color = when {
                    streaming -> SeatPalette.Purple
                    loading -> SeatPalette.Lcd
                    else -> SeatPalette.Lcd
                },
                fontSize = 11.sp,
                fontFamily = FontFamily.Monospace,
                fontWeight = FontWeight.Bold,
            )
            Text(
                when {
                    queue > 0 -> "QUEUE $queue"
                    deskOn -> "DESK"
                    else -> "QUIET"
                },
                color = if (deskOn || queue > 0) SeatPalette.Lcd else SeatPalette.BevelLite,
                fontSize = 11.sp,
                fontFamily = FontFamily.Monospace,
            )
        }
        Row(
            Modifier.fillMaxWidth().padding(top = 2.dp),
            horizontalArrangement = Arrangement.spacedBy(2.dp),
        ) {
            val lit = when (state) {
                "gate" -> step.coerceIn(0, steps)
                "load" -> step.coerceIn(0, steps).coerceAtLeast(1)
                "warm" -> (steps / 4).coerceAtLeast(1)
                else -> 0
            }
            val onColor = if (loading) SeatPalette.Lcd else SeatPalette.Purple
            val offColor = if (loading) SeatPalette.LcdBg else SeatPalette.PurpleDim
            repeat(steps) { i ->
                Box(
                    Modifier
                        .weight(1f)
                        .height(8.dp)
                        .border(1.dp, SeatPalette.BevelDark)
                        .background(if (i < lit) onColor else offColor),
                )
            }
        }
    }
}

@Composable
fun ModuleColumn(content: @Composable ColumnScope.() -> Unit) {
    Column(
        Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp),
        content = content,
    )
}

@Composable
fun SeatCard(
    modifier: Modifier = Modifier,
    content: @Composable ColumnScope.() -> Unit,
) {
    Column(
        modifier
            .fillMaxWidth()
            .border(1.dp, SeatPalette.BevelDark)
            .background(SeatPalette.PanelDark)
            .padding(8.dp),
        verticalArrangement = Arrangement.spacedBy(4.dp),
        content = content,
    )
}

@Composable
fun PluginDialogFrame(
    title: String,
    actionLabel: String = "CLOSE",
    onAction: () -> Unit,
    onScrim: () -> Unit = onAction,
    content: @Composable ColumnScope.() -> Unit,
) {
    Box(
        Modifier
            .fillMaxSize()
            .background(Color.Black.copy(alpha = 0.55f))
            .clickable(
                indication = null,
                interactionSource = remember { MutableInteractionSource() },
                onClick = onScrim,
            ),
        contentAlignment = Alignment.Center,
    ) {
        Column(
            Modifier
                .fillMaxWidth(0.86f)
                .fillMaxHeight(0.70f)
                .shadow(8.dp)
                .border(2.dp, SeatPalette.BevelDark)
                .background(SeatPalette.Panel)
                .clickable(
                    indication = null,
                    interactionSource = remember { MutableInteractionSource() },
                    onClick = {},
                ),
        ) {
            Row(
                Modifier
                    .fillMaxWidth()
                    .height(32.dp)
                    .background(SeatPalette.Title)
                    .padding(horizontal = 8.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text(
                    title,
                    color = SeatPalette.Lcd,
                    fontFamily = FontFamily.Monospace,
                    fontSize = 12.sp,
                    modifier = Modifier.weight(1f),
                )
                if (actionLabel.isNotBlank()) {
                    Text(
                        actionLabel,
                        color = SeatPalette.Ink,
                        fontSize = 11.sp,
                        fontFamily = FontFamily.Monospace,
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier
                            .border(1.dp, SeatPalette.BevelDark)
                            .background(SeatPalette.BevelLite)
                            .clickable(onClick = onAction)
                            .padding(horizontal = 8.dp, vertical = 4.dp),
                    )
                }
            }
            Column(
                Modifier
                    .fillMaxWidth()
                    .verticalScroll(rememberScrollState())
                    .padding(8.dp),
                verticalArrangement = Arrangement.spacedBy(6.dp),
                content = content,
            )
        }
    }
}
