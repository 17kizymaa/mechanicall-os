package com.mechanicall.pocket.demo

import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.os.Handler
import android.os.Looper
import android.provider.DocumentsContract
import android.provider.Settings
import android.view.ViewGroup
import androidx.activity.ComponentActivity
import androidx.activity.result.contract.ActivityResultContracts
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import java.io.File
import java.util.concurrent.Executors

class MainActivity : ComponentActivity(), SitRackView.Host {
    companion object {
        private const val PREFS = "mechanicall_seat"
        private const val PREF_POCKET = "pocket_one"
    }

    private lateinit var rack: SitRackView
    private val io = Executors.newSingleThreadExecutor()
    private val ui = Handler(Looper.getMainLooper())
    private var pocket: String = ""
    private var face: FaceState = FaceState()
    private var gate: GateState = GateState()
    private var decideArmed: Boolean = false
    private var armToken: Int = 0
    private var why: String = ""

    private var awaitingAllFiles: Boolean = false

    private val picker = registerForActivityResult(ActivityResultContracts.OpenDocumentTree()) { uri: Uri? ->
        if (uri == null) return@registerForActivityResult
        try {
            contentResolver.takePersistableUriPermission(
                uri,
                Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION,
            )
        } catch (_: SecurityException) {
            rack.idleLine = "Could not keep folder access."
            return@registerForActivityResult
        }
        val path = treeUriToFolderPath(uri)
        if (path == null) {
            rack.idleLine = "Need a folder on this phone."
            return@registerForActivityResult
        }
        if (!hasAllFiles()) {
            rack.idleLine = "All files access. Allow, then bind."
            requestAllFiles()
            return@registerForActivityResult
        }
        bindPath(path)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(this))
        }
        @Suppress("DEPRECATION")
        window.statusBarColor = Color.parseColor("#12100E")
        @Suppress("DEPRECATION")
        window.navigationBarColor = Color.parseColor("#12100E")
        pocket = getSharedPreferences(PREFS, Context.MODE_PRIVATE).getString(PREF_POCKET, "").orEmpty()
        rack = SitRackView(this).apply {
            layoutParams = ViewGroup.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT,
            )
            host = this@MainActivity
            contentDescription = "sit millwork"
        }
        setContentView(rack)
        rack.plate = SitPlate.SPLASH
        rack.idleLine = "MECHANICALL"
        ui.postDelayed({ land() }, 2000)
        ui.post(gateTick)
    }

    override fun onResume() {
        super.onResume()
        if (awaitingAllFiles && hasAllFiles()) {
            awaitingAllFiles = false
            land()
        } else if (::rack.isInitialized && rack.plate == SitPlate.BIND && !hasAllFiles()) {
            rack.idleLine = "All files access. Allow, then bind."
        }
    }

    override fun onDestroy() {
        ui.removeCallbacks(gateTick)
        io.shutdownNow()
        super.onDestroy()
    }

    private val gateTick = object : Runnable {
        override fun run() {
            val p = pocket
            if (p.isNotBlank() && face.bound) {
                io.execute {
                    val g = FaceBridge.gateState(p)
                    ui.post {
                        gate = g
                        refreshLcd()
                    }
                }
            }
            ui.postDelayed(this, 400)
        }
    }

    private fun persist(path: String) {
        pocket = path
        getSharedPreferences(PREFS, Context.MODE_PRIVATE).edit().putString(PREF_POCKET, path).apply()
    }

    private fun hasAllFiles(): Boolean {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            Environment.isExternalStorageManager()
        } else {
            true
        }
    }

    private fun requestAllFiles() {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.R) return
        awaitingAllFiles = true
        val intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION).apply {
            data = Uri.parse("package:$packageName")
        }
        try {
            startActivity(intent)
        } catch (_: Exception) {
            startActivity(Intent(Settings.ACTION_MANAGE_ALL_FILES_ACCESS_PERMISSION))
        }
    }

    private fun startBind() {
        if (!hasAllFiles()) {
            rack.idleLine = "All files access. Allow, then bind."
            requestAllFiles()
            return
        }
        picker.launch(null)
    }

    private fun land() {
        if (!hasAllFiles()) {
            goBank(SitPlate.BIND)
            rack.idleLine = "All files access. Allow, then bind."
            return
        }
        io.execute {
            val next = if (pocket.isBlank()) FaceState() else FaceBridge.faceState(pocket)
            ui.post {
                face = next
                if (next.bound && !next.refused) {
                    persist(next.path.ifBlank { pocket })
                    goBank(SitPlate.PLAN)
                } else {
                    goBank(SitPlate.BIND)
                }
            }
        }
    }

    private fun bindPath(path: String) {
        persist(path)
        io.execute {
            val next = FaceBridge.bindFolder(path)
            ui.post {
                face = next
                if (next.bound && !next.refused && next.path.isNotBlank()) {
                    persist(next.path)
                    goBank(SitPlate.PLAN)
                } else {
                    goBank(SitPlate.BIND)
                    rack.idleLine = next.message.ifBlank { "Name your folder. One project. Not the operator tree." }
                }
            }
        }
    }

    private fun goBank(p: SitPlate) {
        decideArmed = false
        rack.zoomed = false
        rack.sendOverlay = false
        rack.dismissEdit()
        rack.plate = p
        rack.pages = LawPages.of(face.planText, face.receipt)
        rack.liveFields = mapOf(
            "Objective" to face.objective,
            "Next" to face.next,
            "Baseline" to face.baseline,
            "Tbc" to face.schema["Tbc"].orEmpty(),
        )
        if (p == SitPlate.DRAFT) {
            rack.draftFields = FaceBridge.readSchemaDraft(pocket, face)
            rack.isolated = IsolatedMode.DRAFT
            rack.contentDescription = "Field Objective DRAFT workshop live vs proposed"
        } else {
            rack.isolated = IsolatedMode.NONE
        }
        if (p == SitPlate.RECEIPT) {
            val path = pocket
            io.execute {
                val text = FaceBridge.receiptText(path)
                ui.post {
                    rack.receiptBody = text
                    refreshLcd()
                }
            }
        }
        refreshLcd()
        if (p != SitPlate.DRAFT) {
            rack.contentDescription = when (p) {
                SitPlate.BIND -> "Choose your folder"
                SitPlate.PLAN -> "PLAN published CURRENT.md in LCD. Field plates open zoom."
                SitPlate.DECIDE -> "DECIDE"
                SitPlate.RECEIPT -> "RECEIPT"
                SitPlate.SPLASH -> "sit millwork"
                else -> rack.contentDescription
            }
        }
    }

    private fun refreshLcd() {
        val phase = when (gate.state) {
            "load" -> "LOAD ${gate.step}/${gate.steps}"
            "gate" -> "STREAM ${gate.step}/${gate.steps}"
            "queued" -> "QUEUE ${gate.queue}"
            "warm" -> "WARM"
            "quiet" -> "QUIET"
            else -> "IDLE"
        }
        rack.pages = LawPages.of(face.planText, face.receipt)
        val instruction = when {
            rack.plate == SitPlate.BIND && !hasAllFiles() ->
                "All files access. Allow, then bind."
            rack.plate == SitPlate.BIND ->
                if (face.bound) "Tap the folder to rebind." else "Name a folder. One project."
            rack.plate == SitPlate.PLAN -> "tap glass to read"
            rack.plate == SitPlate.DRAFT -> "tap a field"
            rack.plate == SitPlate.DECIDE && decideArmed -> "Publish? tap plaque again."
            rack.plate == SitPlate.DECIDE -> "Why on glass. Two-tap plaque."
            rack.plate == SitPlate.RECEIPT -> SitRackView.clipPreview(face.receipt.ifBlank { "(empty receipt)" }, 48)
            else -> "MECHANICALL"
        }
        if (rack.isolated == IsolatedMode.NONE && !rack.zoomed) {
            val page = rack.pages.getOrNull(rack.pageIndex)
            val peek = SitRackView.clipPreview(
                page?.body?.ifBlank { face.next }.orEmpty().ifBlank { face.next },
            )
            val caption = page?.title?.ifBlank { "NEXT" } ?: "NEXT"
            rack.idleLine = when (rack.plate) {
                SitPlate.BIND ->
                    "${rack.plate.name}  $phase\n$instruction"
                SitPlate.DECIDE, SitPlate.RECEIPT ->
                    "${rack.plate.name}  $phase\n$instruction"
                else ->
                    "STATUS  $phase\n$caption\n$peek\n$instruction"
            }
        }
        if (rack.sendOverlay) {
            rack.contentDescription = "SEND overlay ${rack.sendStatus}"
        } else if (rack.isolated == IsolatedMode.CRT) {
            val id = rack.pages.getOrNull(rack.pageIndex)?.id ?: "law"
            rack.contentDescription = "LCD isolated $id"
        } else if (rack.isolated == IsolatedMode.DRAFT) {
            rack.contentDescription = "Field Objective DRAFT workshop live vs proposed"
        } else if (rack.zoomed) {
            val id = rack.pages.getOrNull(rack.pageIndex)?.id ?: "law"
            rack.contentDescription = "LCD zoom $id"
        } else if (rack.plate == SitPlate.RECEIPT) {
            rack.contentDescription = "RECEIPT"
        } else if (rack.plate != SitPlate.BIND) {
            rack.contentDescription = "LCD idle"
        }
    }

    override fun onHit(hit: SitHit) {
        when (hit) {
            SitHit.Lcd -> {
                when {
                    rack.plate == SitPlate.BIND -> startBind()
                    rack.plate == SitPlate.DECIDE ->
                        rack.editOnCrt("Why", why, "why")
                    rack.plate == SitPlate.RECEIPT -> refreshLcd()
                    rack.isolated == IsolatedMode.DRAFT -> rack.dismissEdit()
                    rack.isolated == IsolatedMode.CRT -> refreshLcd()
                    else -> openTerminal()
                }
            }
            SitHit.LcdPrev -> {
                if (rack.isolated == IsolatedMode.CRT) {
                    rack.pageIndex = rack.pageIndex - 1
                    refreshLcd()
                }
            }
            SitHit.LcdNext -> {
                if (rack.isolated == IsolatedMode.CRT) {
                    rack.pageIndex = rack.pageIndex + 1
                    refreshLcd()
                }
            }
            SitHit.Gate -> {
                refreshLcd()
            }
            SitHit.DismissZoom -> {
                rack.dismissEdit()
                rack.zoomed = false
                rack.isolated = IsolatedMode.NONE
                rack.sendOverlay = false
                refreshLcd()
            }
            SitHit.BankPlan -> if (face.bound) {
                rack.dismissEdit()
                goBank(SitPlate.PLAN)
            }
            SitHit.BankDraft -> if (face.bound) {
                rack.dismissEdit()
                goBank(SitPlate.DRAFT)
            }
            SitHit.BankDecide -> if (face.bound) {
                rack.dismissEdit()
                goBank(SitPlate.DECIDE)
            }
            SitHit.BankReceipt -> if (face.bound) {
                rack.dismissEdit()
                goBank(SitPlate.RECEIPT)
            }
            SitHit.BindPaper -> startBind()
            SitHit.FieldObjective -> peekPage(0)
            SitHit.FieldNext -> peekPage(1)
            SitHit.FieldKeep -> peekPage(2)
            SitHit.FieldReject -> peekPage(3)
            SitHit.FieldLimits -> peekPage(4)
            SitHit.FieldAlpha -> rack.editOnCrt("Objective", rack.draftFields["Objective"].orEmpty(), "Objective")
            SitHit.FieldBeta -> rack.editOnCrt("Next", rack.draftFields["Next"].orEmpty(), "Next")
            SitHit.FieldGamma -> rack.editOnCrt("Baseline", rack.draftFields["Baseline"].orEmpty(), "Baseline")
            SitHit.Tbc -> rack.editOnCrt("Tbc", rack.draftFields["Tbc"].orEmpty(), "TBC")
            SitHit.Join -> ioNote { FaceBridge.joinStatus(pocket).note.ifBlank { FaceBridge.joinStatus(pocket).status } }
            SitHit.Send -> openSendOverlay()
            SitHit.Wake -> ioNote { FaceBridge.wakeDesk(pocket).note.ifBlank { FaceBridge.wakeDesk(pocket).status } }
            SitHit.DecidePaper -> decideTap()
            SitHit.Files -> {
                rack.dismissEdit()
                if (rack.sendOverlay) {
                    openBoundInFileManager(this, pocket)
                } else {
                    openSendOverlay()
                }
            }
            SitHit.None -> Unit
        }
    }

    private fun peekPage(i: Int) {
        rack.pageIndex = i
        rack.zoomed = false
        if (rack.isolated != IsolatedMode.CRT) {
            rack.isolated = IsolatedMode.NONE
        }
        refreshLcd()
    }

    private fun openTerminal() {
        rack.zoomed = false
        rack.isolated = IsolatedMode.CRT
        val id = rack.pages.getOrNull(rack.pageIndex)?.id ?: "law"
        rack.contentDescription = "LCD isolated $id"
        refreshLcd()
    }

    private fun openSendOverlay() {
        val p = pocket
        rack.dismissEdit()
        rack.isolated = IsolatedMode.NONE
        rack.sendOverlay = true
        rack.sendStatus = "idle"
        rack.sendNote = if (p.isBlank()) "Name a folder first." else "Send folder module. Not Yes."
        rack.folderList = folderNames(p)
        rack.contentDescription = "SEND overlay ${rack.sendStatus}"
        if (p.isBlank()) return
        io.execute {
            val offer = try {
                FaceBridge.offerStatus(p)
            } catch (e: Exception) {
                OfferState(ok = false, note = e.message.orEmpty())
            }
            val preview = try {
                FaceBridge.projectPreview(p)
            } catch (_: Exception) {
                ProjectPreview(ok = false, note = "")
            }
            val status = offer.status.ifBlank { "idle" }
            val note = listOf(offer.note, preview.note)
                .filter { it.isNotBlank() }
                .joinToString("\n")
                .ifBlank { "idle · folder-out · not FILES" }
            ui.post {
                rack.sendStatus = status
                rack.sendNote = note
                rack.contentDescription = "SEND overlay $status"
            }
        }
    }

    private fun folderNames(path: String): String {
        if (path.isBlank()) return "(empty folder)"
        val dir = File(path)
        val names = dir.listFiles()?.map { it.name }?.sorted().orEmpty()
        if (names.isEmpty()) return "(empty folder)"
        return names.take(16).joinToString("\n")
    }

    private fun decideTap() {
        val reason = rack.whyNow().ifBlank { why }
        if (reason.isBlank()) {
            rack.editOnCrt("Why", "", "why")
            rack.idleLine = "why required"
            return
        }
        if (!decideArmed) {
            decideArmed = true
            armToken += 1
            val token = armToken
            rack.idleLine = "Publish? tap plaque again"
            ui.postDelayed({
                if (token == armToken) {
                    decideArmed = false
                    refreshLcd()
                }
            }, 2800)
            return
        }
        decideArmed = false
        val p = pocket
        io.execute {
            FaceBridge.yes(p, reason)
            val next = FaceBridge.faceState(p)
            ui.post {
                face = next
                goBank(SitPlate.RECEIPT)
            }
        }
    }

    private fun ioNote(block: () -> String) {
        val p = pocket
        if (p.isBlank()) return
        io.execute {
            val note = try {
                block()
            } catch (e: Exception) {
                e.message.orEmpty()
            }
            ui.post { rack.idleLine = note.take(72) }
        }
    }

    override fun onDraftChanged(fields: Map<String, String>) {
        val p = pocket
        if (p.isBlank()) return
        io.execute {
            val live = FaceBridge.readSchemaDraft(p, face).toMutableMap()
            live.putAll(fields)
            FaceBridge.writeSchemaDraft(p, live)
            val next = FaceBridge.faceState(p)
            ui.post { face = next }
        }
    }

    override fun onWhyChanged(why: String) {
        this.why = why
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
