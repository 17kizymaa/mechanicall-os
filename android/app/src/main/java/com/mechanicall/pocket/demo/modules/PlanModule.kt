package com.mechanicall.pocket.demo.modules

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
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
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.mechanicall.pocket.demo.AUTHORITY_FIELDS
import com.mechanicall.pocket.demo.FaceBridge
import com.mechanicall.pocket.demo.FaceState
import com.mechanicall.pocket.demo.HunkRow
import com.mechanicall.pocket.demo.SeatCard
import com.mechanicall.pocket.demo.SeatPalette

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun PlanModule(
    face: FaceState,
    pocket: String,
) {
    var plan by remember { mutableStateOf(face.planText) }
    var changes by remember { mutableStateOf(listOf<HunkRow>()) }
    var focus by remember { mutableStateOf("") }
    var draft by remember { mutableStateOf("") }

    fun reload() {
        val raw = FaceBridge.planText(pocket)
        plan = if (FaceBridge.isError(raw) || raw.isBlank()) face.planText else raw
        changes = FaceBridge.listHunks(pocket).filter { it.id in AUTHORITY_FIELDS }
        val first = changes.firstOrNull { it.differs } ?: changes.firstOrNull()
        if (focus.isBlank() || changes.none { it.id == focus }) {
            focus = first?.id.orEmpty()
        }
        val row = changes.firstOrNull { it.id == focus }
        draft = fieldValue(row?.propose.orEmpty(), focus).ifBlank { fieldValue(row?.live.orEmpty(), focus) }
    }

    LaunchedEffect(pocket, face.path, face.hasCurrent, face.propose) {
        reload()
    }

    val focused = changes.firstOrNull { it.id == focus }
    val differing = changes.filter { it.differs }

    Column(
        Modifier
            .fillMaxSize()
            .padding(8.dp),
    ) {
        if (face.refused) {
            Text(
                face.message,
                color = SeatPalette.Amber,
                fontFamily = FontFamily.Monospace,
                fontSize = 13.sp,
            )
        }
        Text(
            "CURRENT.md",
            color = SeatPalette.Ink,
            fontFamily = FontFamily.Monospace,
            fontSize = 11.sp,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.padding(bottom = 4.dp),
        )
        Box(Modifier.weight(1f).fillMaxWidth()) {
            SeatCard {
                Column(Modifier.verticalScroll(rememberScrollState())) {
                    Text(
                        plan.ifBlank { "No CURRENT.md in this folder." },
                        color = SeatPalette.Ink,
                        fontFamily = FontFamily.Monospace,
                        fontSize = 12.sp,
                        modifier = Modifier.fillMaxWidth(),
                    )
                }
            }
        }
        Text(
            "Changes",
            color = SeatPalette.Ink,
            fontFamily = FontFamily.Monospace,
            fontSize = 11.sp,
            fontWeight = FontWeight.Bold,
            modifier = Modifier
                .semantics { contentDescription = "Changes" }
                .padding(top = 8.dp, bottom = 4.dp),
        )
        FlowRow(
            modifier = Modifier.fillMaxWidth(),
        ) {
            if (differing.isEmpty()) {
                Text(
                    "None. Draft to propose.",
                    color = SeatPalette.BevelDark,
                    fontFamily = FontFamily.Monospace,
                    fontSize = 12.sp,
                )
            } else {
                differing.forEach { row ->
                    val on = row.id == focus
                    Text(
                        row.id,
                        color = if (on) SeatPalette.Lcd else SeatPalette.Suggest,
                        fontFamily = FontFamily.Monospace,
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier
                            .padding(end = 6.dp, bottom = 6.dp)
                            .semantics { contentDescription = "Change ${row.id}" }
                            .border(1.dp, if (on) SeatPalette.Suggest else SeatPalette.BevelDark)
                            .background(if (on) SeatPalette.PanelDark else SeatPalette.Panel)
                            .clickable {
                                focus = row.id
                                draft = fieldValue(row.propose, row.id).ifBlank { fieldValue(row.live, row.id) }
                            }
                            .padding(horizontal = 8.dp, vertical = 6.dp),
                    )
                }
            }
        }
        Text(
            "Proposal",
            color = SeatPalette.Suggest,
            fontFamily = FontFamily.Monospace,
            fontSize = 11.sp,
            fontWeight = FontWeight.Bold,
            modifier = Modifier
                .semantics { contentDescription = "Proposal" }
                .padding(top = 4.dp, bottom = 4.dp),
        )
        Column(
            Modifier
                .fillMaxWidth()
                .weight(1f)
                .verticalScroll(rememberScrollState()),
        ) {
            if (focused == null) {
                Text(
                    "No field selected. Draft still holds the workshop.",
                    color = SeatPalette.BevelDark,
                    fontFamily = FontFamily.Monospace,
                    fontSize = 12.sp,
                )
            } else {
                Text(
                    diffText(focused.live, focused.propose.ifBlank { focused.live }),
                    fontFamily = FontFamily.Monospace,
                    fontSize = 12.sp,
                    modifier = Modifier
                        .fillMaxWidth()
                        .semantics { contentDescription = "Proposal diff" }
                        .border(1.dp, if (focused.differs) SeatPalette.Suggest else SeatPalette.BevelDark)
                        .padding(8.dp),
                )
                OutlinedTextField(
                    value = draft,
                    onValueChange = { draft = it },
                    label = { Text("Edit ${focused.id} on PROPOSE") },
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 6.dp)
                        .semantics { contentDescription = "Edit proposal ${focused.id}" },
                    minLines = 2,
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
                    "KEEP ON PROPOSAL",
                    fontFamily = FontFamily.Monospace,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = SeatPalette.Ink,
                    modifier = Modifier
                        .padding(top = 8.dp)
                        .semantics { contentDescription = "Keep proposal edit" }
                        .border(1.dp, SeatPalette.BevelDark)
                        .background(SeatPalette.BevelLite)
                        .clickable {
                            val body = "**${focused.id}:** ${draft.trim()}\n"
                            FaceBridge.applyHunk(pocket, focused.id, body)
                            reload()
                        }
                        .padding(horizontal = 10.dp, vertical = 8.dp),
                )
            }
        }
    }
}

private fun fieldValue(text: String, id: String): String {
    val prefix = "**$id:**"
    val trimmed = text.trim()
    return if (trimmed.startsWith(prefix)) {
        trimmed.removePrefix(prefix).trim()
    } else {
        trimmed
    }
}

@Composable
private fun diffText(live: String, propose: String) = buildAnnotatedString {
    val liveLines = live.trim().lines()
    val propLines = propose.trim().lines()
    if (live.trim() == propose.trim()) {
        withStyle(SpanStyle(color = SeatPalette.Ink)) { append(propose.ifBlank { "(same as live)" }) }
        return@buildAnnotatedString
    }
    val liveSet = liveLines.toSet()
    val propSet = propLines.toSet()
    for (line in liveLines) {
        if (line !in propSet) {
            withStyle(
                SpanStyle(
                    color = SeatPalette.Amber,
                    textDecoration = TextDecoration.LineThrough,
                ),
            ) {
                append(line)
            }
            append("\n")
        }
    }
    for (line in propLines) {
        if (line !in liveSet) {
            withStyle(SpanStyle(color = SeatPalette.Suggest, fontWeight = FontWeight.Bold)) {
                append(line)
            }
            append("\n")
        } else {
            withStyle(SpanStyle(color = SeatPalette.Ink)) { append(line) }
            append("\n")
        }
    }
}
