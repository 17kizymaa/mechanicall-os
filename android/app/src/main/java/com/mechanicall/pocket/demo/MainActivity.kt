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
    /** Plan well key is a TOC peek, not a form. */
    private var planToc: Boolean = false

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
        val debugPocket = intent.getStringExtra("pocket").orEmpty()
        if (debugPocket.isNotBlank()) {
            pocket = debugPocket
        }
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
        if (debugPocket.isNotBlank()) {
            ui.postDelayed({ bindPath(debugPocket) }, 2200)
        } else {
            ui.postDelayed({ land() }, 2000)
        }
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
        planToc = false
        rack.zoomed = false
        rack.sendOverlay = false
        rack.dismissEdit()
        if (p != SitPlate.PLAN) rack.labour = false
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
        }
        // Bank selects the suggestion well. Well tap opens the writer dest.
        rack.isolated = IsolatedMode.NONE
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
        rack.contentDescription = when (p) {
            SitPlate.BIND -> "Choose your folder"
            SitPlate.PLAN ->
                if (rack.labour) "PLAN. I did it or Not yet."
                else "PLAN. This is the plan."
            SitPlate.DRAFT -> "DRAFT. NOT ACTIVE. not the plan."
            SitPlate.DECIDE -> "DECIDE. Why, then Yes."
            SitPlate.NEXT -> "PLAN. I did it or Not yet."
            SitPlate.RECEIPT -> "RECEIPT. What happened."
            SitPlate.SPLASH -> "sit millwork"
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
        rack.gatePercent = gate.percent
        rack.gateDirection = gate.direction
        val wait = if (phase == "IDLE") "" else phase
        val proposed = rack.draftFields["Next"].orEmpty().ifBlank { "(none)" }
        val instruction = when {
            rack.plate == SitPlate.BIND && !hasAllFiles() ->
                "All files access. Allow, then bind."
            rack.plate == SitPlate.BIND ->
                if (face.bound) houseName() else "Name a folder."
            rack.plate == SitPlate.PLAN && rack.labour ->
                face.next.ifBlank { "(unset)" }
            rack.plate == SitPlate.PLAN -> {
                val page = rack.pages.getOrNull(rack.pageIndex)
                if (planToc && page != null) {
                    SitRackView.clipPreview("${page.title} ${page.body}")
                } else {
                    listOf(
                        "This is the plan.",
                        SitRackView.clipPreview("Next ${face.next.ifBlank { "(unset)" }}", 48),
                        SitRackView.clipPreview(face.objective, 72),
                        wait,
                    ).filter { it.isNotBlank() }.joinToString("\n")
                }
            }
            rack.plate == SitPlate.DRAFT ->
                listOf(
                    "NOT ACTIVE",
                    "live ${SitRackView.clipPreview(face.next.ifBlank { "(none)" }, 40)}",
                    "proposed ${SitRackView.clipPreview(proposed, 40)}",
                    wait,
                ).filter { it.isNotBlank() }.joinToString("\n")
            rack.plate == SitPlate.DECIDE && decideArmed -> "Yes? tap again."
            rack.plate == SitPlate.DECIDE -> "Why. Then Yes. Not yet is enough."
            rack.plate == SitPlate.NEXT ->
                face.next.ifBlank { "(unset)" }
            rack.plate == SitPlate.RECEIPT ->
                SitRackView.receiptStrip(face.receipt)
            else -> "MECHANICALL"
        }
        if ((rack.isolated == IsolatedMode.NONE || rack.isolated == IsolatedMode.DRAFT) && !rack.zoomed) {
            rack.idleLine = instruction
        }
        if (rack.sendOverlay) {
            rack.contentDescription = "SEND overlay ${rack.sendStatus}"
        } else if (rack.isolated == IsolatedMode.CRT) {
            val id = rack.pages.getOrNull(rack.pageIndex)?.id ?: "law"
            rack.contentDescription = "LCD isolated $id"
        } else if (rack.isolated == IsolatedMode.DRAFT) {
            rack.contentDescription = "DRAFT writer NOT ACTIVE. PROPOSE-CURRENT.md. Not the plan."
        } else if (rack.zoomed) {
            val id = rack.pages.getOrNull(rack.pageIndex)?.id ?: "law"
            rack.contentDescription = "LCD zoom $id"
        } else if (rack.plate == SitPlate.PLAN) {
            rack.contentDescription =
                if (rack.labour) "PLAN. I did it or Not yet." else "PLAN. This is the plan."
        } else if (rack.plate == SitPlate.DECIDE) {
            rack.contentDescription = "DECIDE. Why, then Yes."
        } else if (rack.plate == SitPlate.NEXT) {
            rack.contentDescription = "PLAN. I did it or Not yet."
        } else if (rack.plate == SitPlate.RECEIPT) {
            rack.contentDescription = "RECEIPT. What happened."
        } else if (rack.plate == SitPlate.DRAFT) {
            rack.contentDescription = "DRAFT. NOT ACTIVE. not the plan."
        } else if (rack.plate != SitPlate.BIND) {
            rack.contentDescription = "LCD idle"
        }
    }

    override fun onHit(hit: SitHit) {
        when (hit) {
            SitHit.Lcd -> {
                when {
                    rack.plate == SitPlate.BIND -> startBind()
                    rack.plate == SitPlate.DRAFT -> openDraftWriter()
                    rack.plate == SitPlate.DECIDE ->
                        rack.editOnCrt("Why", why, "why")
                    rack.plate == SitPlate.NEXT -> refreshLcd()
                    rack.plate == SitPlate.PLAN && rack.labour -> refreshLcd()
                    rack.plate == SitPlate.RECEIPT -> refreshLcd()
                    rack.plate == SitPlate.PLAN -> {
                        planToc = false
                        peekPage(0)
                    }
                    rack.isolated == IsolatedMode.DRAFT -> openDraftWriter()
                    rack.isolated == IsolatedMode.CRT -> refreshLcd()
                    else -> peekPage(0)
                }
            }
            SitHit.LcdPrev -> {
                if (rack.isolated == IsolatedMode.CRT) {
                    rack.pageIndex = rack.pageIndex - 1
                    refreshLcd()
                } else if (rack.isolated == IsolatedMode.DRAFT) {
                    openDraftWriter()
                }
            }
            SitHit.LcdNext -> {
                if (rack.isolated == IsolatedMode.CRT) {
                    rack.pageIndex = rack.pageIndex + 1
                    refreshLcd()
                } else if (rack.isolated == IsolatedMode.DRAFT) {
                    openDraftWriter()
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
            SitHit.FieldObjective -> {
                planToc = true
                draftOrPeek("Objective", 0)
            }
            SitHit.FieldNext -> {
                planToc = true
                draftOrPeek("Next", 1)
            }
            SitHit.FieldKeep -> {
                planToc = true
                draftOrPeek("Keep", 2)
            }
            SitHit.FieldReject -> {
                planToc = true
                draftOrPeek("Reject", 3)
            }
            SitHit.FieldLimits -> {
                planToc = true
                draftOrPeek("Limits", 4)
            }
            SitHit.FieldAlpha, SitHit.FieldBeta, SitHit.FieldGamma, SitHit.Tbc -> Unit
            SitHit.Join, SitHit.Wake -> Unit
            SitHit.Send -> if (rack.sendOverlay) stageSendFolder() else openSendOverlay()
            SitHit.DecidePaper -> decideTap()
            SitHit.DecideNotYet -> {
                leaveDecideWithoutYes()
                if (face.bound) goBank(SitPlate.PLAN)
            }
            SitHit.DidIt -> didItTap()
            SitHit.NotYetFeet -> notYetFeet()
            SitHit.WhyStrip -> rack.editOnCrt("Why", why, "why")
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

    private fun draftOrPeek(_key: String, page: Int) {
        if (rack.plate == SitPlate.DRAFT) {
            openDraftWriter()
            return
        }
        peekPage(page)
    }

    private fun openDraftWriter() {
        val p = pocket
        rack.isolated = IsolatedMode.DRAFT
        rack.contentDescription = "DRAFT writer NOT ACTIVE. PROPOSE-CURRENT.md. Not the plan."
        if (p.isBlank()) {
            rack.editDraftWriter("")
            return
        }
        io.execute {
            val text = try {
                FaceBridge.readPropose(p)
            } catch (_: Exception) {
                ""
            }
            ui.post { rack.editDraftWriter(text) }
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
        rack.sendNote = if (p.isBlank()) {
            "Name a folder first."
        } else {
            "Tap FOLDER to send."
        }
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
            val status = offer.status.ifBlank { "idle" }.let { if (it == "none") "idle" else it }
            val note = listOf(offer.note, preview.note)
                .filter { it.isNotBlank() }
                .joinToString("\n")
                .ifBlank { "Tap FOLDER to send. Files only. Not the live plan. Not Yes." }
            ui.post {
                rack.sendStatus = status
                rack.sendNote = note
                rack.contentDescription = "SEND overlay $status"
            }
        }
    }

    /** Dest FOLDER plaque. Stages the bound pocket. Not Yes. Quiet drop is honest. */
    private fun stageSendFolder() {
        val p = pocket
        if (p.isBlank()) {
            rack.sendStatus = "idle"
            rack.sendNote = "Name a folder first. Not Yes."
            rack.contentDescription = "SEND overlay idle"
            return
        }
        rack.sendStatus = "staging"
        rack.sendNote = "Staging folder. Not Yes."
        rack.contentDescription = "SEND overlay staging"
        io.execute {
            val r = try {
                FaceBridge.sendFolder(p)
            } catch (e: Exception) {
                SendFolderResult(ok = false, note = e.message.orEmpty(), notYes = true)
            }
            ui.post {
                rack.sendStatus = when {
                    r.drop.isNotBlank() -> "offered"
                    r.ok -> "staged"
                    else -> "idle"
                }
                rack.sendNote = r.note.ifBlank { "Staged locally. Not Yes." }
                rack.folderList = folderNames(p)
                rack.contentDescription = "SEND overlay ${rack.sendStatus}"
            }
        }
    }

    private fun houseName(): String {
        val p = face.path.ifBlank { pocket }
        val n = File(p).name.trim()
        return n.ifBlank { "Name a folder." }
    }

    private fun folderNames(path: String): String {
        if (path.isBlank()) return "(empty folder)"
        val dir = File(path)
        val names = dir.listFiles()?.map { it.name }?.sorted().orEmpty()
        if (names.isEmpty()) return "(empty folder)"
        return names.take(16).joinToString("\n")
    }

    /** Decide Not yet: receipt only. Banks are not this. Never Confirm. Never CURRENT. */
    private fun leaveDecideWithoutYes() {
        if (rack.plate != SitPlate.DECIDE) return
        val p = pocket
        if (p.isBlank()) return
        val reason = rack.whyNow().ifBlank { why }.ifBlank { "not yet" }
        io.execute { FaceBridge.notYet(p, reason) }
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
            rack.idleLine = "Yes? tap plaque again"
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
                rack.labour = true
                goBank(SitPlate.PLAN)
            }
        }
    }

    /** Labour after Yes. Never FaceBridge.yes. Never Confirm. */
    private fun didItTap() {
        if (!rack.labour || rack.plate != SitPlate.PLAN) return
        val p = pocket
        if (p.isBlank()) return
        val nxt = face.next.ifBlank { "(unset)" }
        io.execute {
            FaceBridge.didIt(p, nxt)
            val next = FaceBridge.faceState(p)
            ui.post {
                face = next
                rack.labour = false
                goBank(SitPlate.RECEIPT)
            }
        }
    }

    /** After Yes, Not yet does not un-stamp. The Next stays. */
    private fun notYetFeet() {
        if (!rack.labour || rack.plate != SitPlate.PLAN) return
        rack.idleLine = "Not yet. The Next stays."
        refreshLcd()
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

    override fun onDraftTextChanged(text: String) {
        val p = pocket
        if (p.isBlank()) return
        io.execute {
            FaceBridge.savePropose(p, text)
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
