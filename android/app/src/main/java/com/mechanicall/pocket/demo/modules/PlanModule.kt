package com.mechanicall.pocket.demo.modules

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
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
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.mechanicall.pocket.demo.AUTHORITY_FIELDS
import com.mechanicall.pocket.demo.FaceBridge
import com.mechanicall.pocket.demo.FaceState
import com.mechanicall.pocket.demo.ModuleColumn
import com.mechanicall.pocket.demo.SeatCard
import com.mechanicall.pocket.demo.SeatPalette

private val PRIMARY_FIELDS = listOf("Objective", "Next")

@Composable
fun PlanModule(
    face: FaceState,
    pocket: String,
) {
    var live by remember { mutableStateOf(FaceBridge.fieldsFromFaceOrEmpty(face)) }
    var draft by remember { mutableStateOf(face.schemaDraft) }
    var edits by remember { mutableStateOf(linkedMapOf<String, String>()) }
    var detailed by remember { mutableStateOf(false) }
    var plan by remember { mutableStateOf(face.planText) }
    var note by remember { mutableStateOf("Published plan. Edit in Draft, or SAVE DRAFT here — not Yes.") }

    fun seedEdits(nextLive: Map<String, String>, nextDraft: Map<String, String>) {
        val seeded = linkedMapOf<String, String>()
        for (name in AUTHORITY_FIELDS) {
            seeded[name] = nextDraft[name].orEmpty().ifBlank { nextLive[name].orEmpty() }
        }
        edits = seeded
    }

    LaunchedEffect(pocket, face.path, face.hasCurrent, face.propose) {
        live = FaceBridge.schemaFields(pocket, face).ifBlankMap(face.schema)
        draft = FaceBridge.readSchemaDraft(pocket, face).ifBlankMap(face.schemaDraft)
        seedEdits(live, draft)
        val raw = FaceBridge.planText(pocket)
        plan = if (FaceBridge.isError(raw) || raw.isBlank()) face.planText else raw
    }

    fun saveDraft() {
        val payload = AUTHORITY_FIELDS.associate { it to edits[it].orEmpty() }
        FaceBridge.writeSchemaDraft(pocket, payload)
        draft = payload
        note = "Draft saved. Not Yes. Use DECIDE."
    }

    ModuleColumn {
        Text(
            "The published plan.",
            color = SeatPalette.Ink,
            fontFamily = FontFamily.Monospace,
            fontSize = 13.sp,
        )
        Text(
            note,
            color = SeatPalette.Ink,
            fontFamily = FontFamily.Monospace,
            fontSize = 11.sp,
        )
        if (!face.hasCurrent && !face.refused) {
            Text(
                "This folder has no plan yet.",
                color = SeatPalette.BevelLite,
                fontFamily = FontFamily.Monospace,
                fontSize = 12.sp,
            )
        }
        if (face.refused) {
            Text(
                face.message,
                color = SeatPalette.Amber,
                fontFamily = FontFamily.Monospace,
                fontSize = 13.sp,
            )
        }
        SeatCard {
            Text(
                plan.ifBlank { "No plan file in this folder." },
                color = SeatPalette.Ink,
                fontFamily = FontFamily.Monospace,
                fontSize = 12.sp,
            )
        }
        PRIMARY_FIELDS.forEach { name ->
            PlanField(
                name = name,
                live = live[name].orEmpty(),
                edit = edits[name].orEmpty(),
                prominent = true,
                onEdit = { value ->
                    edits = LinkedHashMap(edits).apply { put(name, value) }
                },
            )
        }
        Text(
            "SAVE DRAFT · not Yes",
            color = SeatPalette.Ink,
            fontFamily = FontFamily.Monospace,
            fontSize = 11.sp,
            fontWeight = FontWeight.Bold,
            modifier = Modifier
                .border(1.dp, SeatPalette.BevelDark)
                .background(SeatPalette.Lcd)
                .clickable(onClick = { saveDraft() })
                .padding(horizontal = 10.dp, vertical = 8.dp),
        )
        Text(
            if (detailed) "Hide the rest" else "Detailed plan",
            color = SeatPalette.Lcd,
            fontFamily = FontFamily.Monospace,
            fontSize = 11.sp,
            fontWeight = FontWeight.Bold,
            modifier = Modifier
                .border(1.dp, SeatPalette.BevelDark)
                .background(SeatPalette.PanelDark)
                .clickable { detailed = !detailed }
                .padding(horizontal = 10.dp, vertical = 6.dp),
        )
        if (detailed) {
            AUTHORITY_FIELDS.filter { it !in PRIMARY_FIELDS }.forEach { name ->
                PlanField(
                    name = name,
                    live = live[name].orEmpty(),
                    edit = edits[name].orEmpty(),
                    prominent = false,
                    onEdit = { value ->
                        edits = LinkedHashMap(edits).apply { put(name, value) }
                    },
                )
            }
            SeatCard {
                Text(
                    plan.ifBlank { "No plan file in this folder." },
                    color = SeatPalette.Lcd,
                    fontFamily = FontFamily.Monospace,
                    fontSize = 11.sp,
                )
            }
        }
    }
}

@Composable
private fun PlanField(
    name: String,
    live: String,
    edit: String,
    prominent: Boolean,
    onEdit: (String) -> Unit,
) {
    SeatCard {
        Text(
            name.uppercase(),
            color = SeatPalette.BevelLite,
            fontFamily = FontFamily.Monospace,
            fontSize = 10.sp,
            fontWeight = FontWeight.Bold,
        )
        Text(
            live.ifBlank { "(none)" },
            color = SeatPalette.Lcd,
            fontFamily = FontFamily.Monospace,
            fontSize = if (prominent) 16.sp else 13.sp,
            modifier = Modifier
                .fillMaxWidth()
                .background(SeatPalette.LcdBg)
                .padding(8.dp),
        )
        Text(
            "DRAFT · not Yes",
            color = SeatPalette.Purple,
            fontFamily = FontFamily.Monospace,
            fontSize = 10.sp,
        )
        OutlinedTextField(
            value = edit,
            onValueChange = onEdit,
            modifier = Modifier.fillMaxWidth(),
            minLines = if (prominent) 2 else 1,
            colors = OutlinedTextFieldDefaults.colors(
                focusedTextColor = SeatPalette.Purple,
                unfocusedTextColor = SeatPalette.Purple,
                focusedBorderColor = SeatPalette.Purple,
                unfocusedBorderColor = SeatPalette.BevelDark,
                cursorColor = SeatPalette.Purple,
                focusedContainerColor = SeatPalette.LcdBg,
                unfocusedContainerColor = SeatPalette.LcdBg,
            ),
        )
    }
}

private fun Map<String, String>.ifBlankMap(fallback: Map<String, String>): Map<String, String> {
    return if (values.any { it.isNotBlank() }) this else fallback
}
