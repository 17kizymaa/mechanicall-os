package com.mechanicall.pocket.demo.modules

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.mechanicall.pocket.demo.FaceBridge
import com.mechanicall.pocket.demo.FaceState
import com.mechanicall.pocket.demo.HunkRow
import com.mechanicall.pocket.demo.SeatPalette
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import kotlinx.coroutines.withTimeoutOrNull

const val DESK_OLLAMA =
    "http://myarch:11434,http://127.0.0.1:11434,http://192.168.0.51:11434,http://100.90.85.68:11434"
private const val SEND_TIMEOUT_MS = 28_000L

@Composable
fun ChatHome(
    face: FaceState,
    pocket: String,
    onReload: () -> Unit,
) {
    var composer by remember { mutableStateOf("") }
    var busy by remember { mutableStateOf(false) }
    var note by remember { mutableStateOf("Suggesting on PROPOSE. Accept is not Yes.") }
    var lastSay by remember { mutableStateOf("") }
    var hunks by remember { mutableStateOf(listOf<HunkRow>()) }
    var focus by remember { mutableStateOf("Objective") }
    val scope = rememberCoroutineScope()

    fun refresh() {
        hunks = FaceBridge.listHunks(pocket)
        if (hunks.none { it.id == focus }) {
            focus = hunks.firstOrNull()?.id ?: "Objective"
        }
        val hist = FaceBridge.chatHistory(pocket)
        lastSay = hist.lastOrNull { it.role != "user" }?.text.orEmpty()
    }

    LaunchedEffect(pocket, face.path, face.propose) {
        refresh()
    }

    val focused = hunks.firstOrNull { it.id == focus }

    Column(Modifier.fillMaxSize()) {
        Column(
            Modifier
                .weight(1f)
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 8.dp, vertical = 6.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            Text(
                note,
                fontFamily = FontFamily.Monospace,
                fontSize = 11.sp,
                color = SeatPalette.Ink,
            )
            Row(
                Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState()),
                horizontalArrangement = Arrangement.spacedBy(6.dp),
            ) {
                hunks.forEach { row ->
                    val on = row.id == focus
                    Text(
                        row.id.uppercase(),
                        fontFamily = FontFamily.Monospace,
                        fontSize = 10.sp,
                        fontWeight = FontWeight.Bold,
                        color = if (row.differs) SeatPalette.Suggest else SeatPalette.Ink,
                        modifier = Modifier
                            .border(
                                1.dp,
                                if (on) SeatPalette.Suggest else SeatPalette.BevelDark,
                            )
                            .background(if (on) SeatPalette.PanelDark else SeatPalette.Panel)
                            .clickable(enabled = !busy) { focus = row.id }
                            .padding(horizontal = 8.dp, vertical = 6.dp),
                    )
                }
            }
            Text(
                "LIVE",
                fontFamily = FontFamily.Monospace,
                fontSize = 10.sp,
                color = SeatPalette.Ink,
                fontWeight = FontWeight.Bold,
            )
            Text(
                focused?.live?.ifBlank { "(none)" } ?: "(none)",
                fontFamily = FontFamily.Monospace,
                fontSize = 12.sp,
                color = SeatPalette.Ink,
                modifier = Modifier
                    .fillMaxWidth()
                    .background(SeatPalette.PanelDark)
                    .padding(8.dp),
            )
            if (focused?.differs == true) {
                Text(
                    "DRAFT · not Yes",
                    fontFamily = FontFamily.Monospace,
                    fontSize = 10.sp,
                    color = SeatPalette.Suggest,
                    fontWeight = FontWeight.Bold,
                )
                Text(
                    focused.propose,
                    fontFamily = FontFamily.Monospace,
                    fontSize = 12.sp,
                    color = SeatPalette.Suggest,
                    modifier = Modifier
                        .fillMaxWidth()
                        .border(1.dp, SeatPalette.Suggest)
                        .padding(8.dp),
                )
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text(
                        "ACCEPT HUNK",
                        fontFamily = FontFamily.Monospace,
                        fontSize = 10.sp,
                        fontWeight = FontWeight.Bold,
                        color = SeatPalette.Ink,
                        modifier = Modifier
                            .border(1.dp, SeatPalette.BevelDark)
                            .background(SeatPalette.BevelLite)
                            .clickable(enabled = !busy) {
                                FaceBridge.acceptHunk(pocket, focus)
                                note = "Hunk kept on PROPOSE. Not Yes."
                                refresh()
                                onReload()
                            }
                            .padding(horizontal = 8.dp, vertical = 6.dp),
                    )
                    Text(
                        "REJECT HUNK",
                        fontFamily = FontFamily.Monospace,
                        fontSize = 10.sp,
                        fontWeight = FontWeight.Bold,
                        color = SeatPalette.Ink,
                        modifier = Modifier
                            .border(1.dp, SeatPalette.BevelDark)
                            .background(SeatPalette.PanelDark)
                            .clickable(enabled = !busy) {
                                FaceBridge.rejectHunk(pocket, focus)
                                note = "Hunk restored from live. Not Yes."
                                refresh()
                                onReload()
                            }
                            .padding(horizontal = 8.dp, vertical = 6.dp),
                    )
                }
            }
            Text(
                "Last desk say",
                fontFamily = FontFamily.Monospace,
                fontSize = 10.sp,
                color = SeatPalette.Ink,
            )
            Text(
                lastSay.ifBlank { "No desk say yet. GATE is the strip." },
                fontFamily = FontFamily.Monospace,
                fontSize = 13.sp,
                color = SeatPalette.Ink,
                modifier = Modifier
                    .fillMaxWidth()
                    .background(SeatPalette.PanelDark)
                    .padding(8.dp),
            )
        }
        Row(
            Modifier
                .fillMaxWidth()
                .padding(10.dp),
            verticalAlignment = Alignment.Bottom,
            horizontalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            OutlinedTextField(
                value = composer,
                onValueChange = { composer = it },
                label = { Text("Suggest $focus") },
                modifier = Modifier.weight(1f),
                enabled = !busy,
                minLines = 1,
                colors = OutlinedTextFieldDefaults.colors(
                    focusedTextColor = SeatPalette.Ink,
                    unfocusedTextColor = SeatPalette.Ink,
                    focusedBorderColor = SeatPalette.Suggest,
                    unfocusedBorderColor = SeatPalette.BevelDark,
                    focusedLabelColor = SeatPalette.Suggest,
                    unfocusedLabelColor = SeatPalette.Ink,
                    cursorColor = SeatPalette.Suggest,
                    focusedContainerColor = SeatPalette.Panel,
                    unfocusedContainerColor = SeatPalette.Panel,
                ),
            )
            Text(
                "SEND",
                fontFamily = FontFamily.Monospace,
                fontSize = 11.sp,
                fontWeight = FontWeight.Bold,
                color = SeatPalette.Ink,
                modifier = Modifier
                    .border(1.dp, SeatPalette.BevelDark)
                    .background(SeatPalette.BevelLite)
                    .clickable(enabled = !busy) {
                        val text = composer.trim()
                        if (text.isEmpty() || busy) return@clickable
                        composer = ""
                        scope.launch {
                            busy = true
                            note = "Desk thinking. GATE is the strip."
                            val result = withTimeoutOrNull(SEND_TIMEOUT_MS) {
                                withContext(Dispatchers.IO) {
                                    FaceBridge.draftChat(pocket, DESK_OLLAMA, text, focus)
                                }
                            }
                            if (result == null) {
                                note = "Desk quiet."
                                lastSay = "Desk quiet."
                            } else {
                                lastSay = result.reply.ifBlank { "Desk quiet." }
                                note = when {
                                    result.stage == "gate" -> "Use DECIDE to publish."
                                    result.ok -> "Suggestion on PROPOSE. Not Yes."
                                    else -> "Desk quiet."
                                }
                                refresh()
                            }
                            busy = false
                            onReload()
                        }
                    }
                    .padding(horizontal = 10.dp, vertical = 12.dp),
            )
        }
    }
}
