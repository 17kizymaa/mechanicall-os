package com.mechanicall.pocket.demo.modules

import android.content.Intent
import android.net.Uri
import android.provider.DocumentsContract
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.mechanicall.pocket.demo.FaceState
import com.mechanicall.pocket.demo.SeatPalette

@Composable
fun BindModule(
    pocket: String,
    face: FaceState,
    onPocketChange: (String) -> Unit,
    onBind: (String) -> Unit,
) {
    val context = LocalContext.current
    val picker = rememberLauncherForActivityResult(
        ActivityResultContracts.OpenDocumentTree(),
    ) { uri: Uri? ->
        if (uri == null) return@rememberLauncherForActivityResult
        try {
            context.contentResolver.takePersistableUriPermission(
                uri,
                Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION,
            )
        } catch (_: SecurityException) {
            // Support path still usable if persist fails.
        }
        val path = treeUriToFolderPath(uri)
        if (path != null) {
            onPocketChange(path)
            onBind(path)
        }
    }

    Column(
        Modifier
            .fillMaxSize()
            .padding(10.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp),
    ) {
        Text(
            "This sit holds one folder. Name it. Not the operator tree.",
            color = SeatPalette.Lcd,
            fontFamily = FontFamily.Monospace,
            fontSize = 14.sp,
        )
        OutlinedTextField(
            value = pocket,
            onValueChange = onPocketChange,
            label = { Text("Your folder") },
            placeholder = { Text("/sdcard/my-afternoon") },
            modifier = Modifier.fillMaxWidth(),
            colors = OutlinedTextFieldDefaults.colors(
                focusedTextColor = SeatPalette.Lcd,
                unfocusedTextColor = SeatPalette.Lcd,
                focusedBorderColor = SeatPalette.Lcd,
                unfocusedBorderColor = SeatPalette.BevelLite,
                focusedLabelColor = SeatPalette.Lcd,
                unfocusedLabelColor = SeatPalette.BevelLite,
                cursorColor = SeatPalette.Lcd,
                focusedContainerColor = SeatPalette.LcdBg,
                unfocusedContainerColor = SeatPalette.LcdBg,
            ),
        )
        if (face.refused) {
            Text(
                face.message,
                color = SeatPalette.Amber,
                fontFamily = FontFamily.Monospace,
                fontSize = 13.sp,
            )
        }
        BindPad(
            label = "Bind this folder",
            fill = true,
            modifier = Modifier.height(56.dp),
            onClick = { onBind(pocket) },
        )
        BindPad(
            label = "Choose your folder",
            fill = false,
            modifier = Modifier.height(48.dp),
            onClick = { picker.launch(null) },
        )
        Text(
            "Picker is support. Binding replaces the last project.",
            color = SeatPalette.BevelLite,
            fontFamily = FontFamily.Monospace,
            fontSize = 11.sp,
        )
    }
}

@Composable
private fun BindPad(
    label: String,
    fill: Boolean,
    modifier: Modifier,
    onClick: () -> Unit,
) {
    val bg = if (fill) SeatPalette.LcdBg else SeatPalette.PanelDark
    val fg = if (fill) SeatPalette.Lcd else SeatPalette.BevelLite
    Box(
        modifier
            .fillMaxWidth()
            .border(2.dp, SeatPalette.BevelLite)
            .background(bg)
            .clickable(onClick = onClick),
        contentAlignment = Alignment.Center,
    ) {
        Text(
            label,
            color = fg,
            fontSize = 22.sp,
            fontFamily = FontFamily.Monospace,
            fontWeight = FontWeight.Bold,
        )
    }
}

fun treeUriToFolderPath(uri: Uri): String? {
    val id = try {
        DocumentsContract.getTreeDocumentId(uri)
    } catch (_: Exception) {
        return null
    }
    val parts = id.split(":", limit = 2)
    if (parts.size < 2) return null
    val volume = parts[0]
    val rel = parts[1].trimStart('/')
    return if (volume == "primary") {
        "/storage/emulated/0/$rel"
    } else {
        "/storage/$volume/$rel"
    }
}
