package com.mechanicall.pocket.demo

import android.content.ActivityNotFoundException
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Environment
import android.widget.Toast
import java.io.File

/** FILES → the device file manager on the bound directory. Not an in-app overlay. Not Yes. */
fun openBoundInFileManager(context: Context, path: String) {
    val dir = File(path)
    if (path.isBlank() || !dir.exists()) {
        Toast.makeText(context, "Name a folder first.", Toast.LENGTH_SHORT).show()
        return
    }
    val intents = ArrayList<Intent>()
    intents.add(
        Intent(Intent.ACTION_VIEW).apply {
            setDataAndType(Uri.fromFile(dir), "resource/folder")
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        },
    )
    intents.add(
        Intent(Intent.ACTION_VIEW).apply {
            setDataAndType(Uri.fromFile(dir), "vnd.android.document/directory")
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        },
    )
    val ext = Environment.getExternalStorageDirectory()
    if (ext != null && dir.absolutePath.startsWith(ext.absolutePath)) {
        val rel = dir.absolutePath.removePrefix(ext.absolutePath).trimStart('/')
        val encoded = Uri.encode(rel).replace("%2F", "%2F")
        val doc = Uri.parse(
            "content://com.android.externalstorage.documents/document/primary%3A$encoded",
        )
        intents.add(
            Intent(Intent.ACTION_VIEW).apply {
                data = doc
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            },
        )
    }
    for (intent in intents) {
        try {
            context.startActivity(Intent.createChooser(intent, "FILES"))
            return
        } catch (_: ActivityNotFoundException) {
        } catch (_: Exception) {
        }
    }
    Toast.makeText(context, "No file manager for this folder.", Toast.LENGTH_SHORT).show()
}
