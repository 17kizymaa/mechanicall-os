package com.mechanicall.pocket.demo.modules

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import com.mechanicall.pocket.demo.FaceBridge
import com.mechanicall.pocket.demo.FaceState
import com.mechanicall.pocket.demo.ModuleColumn
import com.mechanicall.pocket.demo.SeatCard

@Composable
fun ReceiptModule(
    face: FaceState,
    pocket: String,
) {
    var body by remember { mutableStateOf(face.receipt) }
    var events by remember { mutableStateOf("") }

    LaunchedEffect(pocket, face.path, face.receipt) {
        val raw = FaceBridge.receiptText(pocket)
        body = raw.ifBlank { face.receipt }
        events = FaceBridge.eventsText(pocket)
    }

    val empty = "No decision recorded yet. The machine did not pretend you agreed."
    ModuleColumn {
        Text(
            "What you decided. Open this tomorrow.",
            style = MaterialTheme.typography.bodyMedium,
        )
        if (face.said.isNotBlank()) {
            SeatCard {
                Text("YOU SAID", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.secondary)
                Text(face.said, style = MaterialTheme.typography.bodyLarge)
            }
        }
        SeatCard {
            Text(
                body.ifBlank { empty },
                style = MaterialTheme.typography.bodyMedium,
            )
        }
        SeatCard {
            Text(
                "EVENTS",
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.secondary,
            )
            Text(
                events.ifBlank { "(no events yet)" },
                style = MaterialTheme.typography.bodySmall,
            )
        }
    }
}
