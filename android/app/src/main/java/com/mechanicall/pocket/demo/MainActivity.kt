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
        ui.postDelayed({ land() }, 1100)
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
        rack.plate = p
        rack.pages = LawPages.of(face.planText, face.receipt)
        if (p == SitPlate.DRAFT) {
            rack.draftFields = FaceBridge.readSchemaDraft(pocket, face)
        }
        refreshLcd()
        rack.contentDescription = when (p) {
            SitPlate.BIND -> "Choose your folder"
            SitPlate.PLAN -> "PLAN published CURRENT.md in LCD. Field plates open zoom."
            SitPlate.DRAFT -> "DRAFT"
            SitPlate.DECIDE -> "DECIDE"
            SitPlate.RECEIPT -> "RECEIPT"
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
        rack.idleLine = when {
            rack.plate == SitPlate.BIND && !hasAllFiles() ->
                "All files access. Allow, then bind."
            rack.plate == SitPlate.BIND || !face.bound || face.refused ->
                "Name your folder. One project. Not the operator tree."
            rack.zoomed -> rack.idleLine
            rack.plate == SitPlate.DECIDE && decideArmed ->
                "Publish? tap paper again · why required"
            rack.plate == SitPlate.RECEIPT ->
                face.receipt.ifBlank { "(empty receipt)" }.take(72)
            else -> "${rack.plate.name} · ${face.next.ifBlank { "(no Next)" }} · $phase".take(72)
        }
        if (rack.zoomed) {
            val id = rack.pages.getOrNull(rack.pageIndex)?.id ?: "law"
            rack.contentDescription = "LCD zoom $id"
        } else if (rack.plate != SitPlate.BIND) {
            rack.contentDescription = "LCD idle"
        }
    }

    override fun onHit(hit: SitHit) {
        when (hit) {
            SitHit.Lcd -> {
                if (rack.plate == SitPlate.BIND) {
                    startBind()
                } else {
                    rack.zoomed = true
                    refreshLcd()
                }
            }
            SitHit.LcdPrev -> {
                rack.pageIndex = rack.pageIndex - 1
                refreshLcd()
            }
            SitHit.LcdNext, SitHit.Gate -> {
                rack.pageIndex = rack.pageIndex + 1
                refreshLcd()
            }
            SitHit.DismissZoom -> {
                rack.zoomed = false
                refreshLcd()
            }
            SitHit.BankPlan -> if (face.bound) goBank(SitPlate.PLAN)
            SitHit.BankDraft -> if (face.bound) goBank(SitPlate.DRAFT)
            SitHit.BankDecide -> if (face.bound) goBank(SitPlate.DECIDE)
            SitHit.BankReceipt -> if (face.bound) goBank(SitPlate.RECEIPT)
            SitHit.BindPaper -> startBind()
            SitHit.FieldObjective -> openPage(0)
            SitHit.FieldNext -> openPage(1)
            SitHit.FieldKeep -> openPage(2)
            SitHit.FieldReject -> openPage(3)
            SitHit.FieldLimits -> openPage(4)
            SitHit.FieldAlpha, SitHit.FieldBeta, SitHit.FieldGamma, SitHit.Tbc -> Unit
            SitHit.Join -> ioNote { FaceBridge.joinStatus(pocket).note.ifBlank { FaceBridge.joinStatus(pocket).status } }
            SitHit.Send -> ioNote { FaceBridge.asText(FaceBridge.sendProject(pocket)) }
            SitHit.Wake -> ioNote { FaceBridge.wakeDesk(pocket).note.ifBlank { FaceBridge.wakeDesk(pocket).status } }
            SitHit.DecidePaper -> decideTap()
            SitHit.None -> Unit
        }
    }

    private fun openPage(i: Int) {
        rack.pageIndex = i
        rack.zoomed = true
        refreshLcd()
    }

    private fun decideTap() {
        val reason = rack.whyNow().ifBlank { why }
        if (reason.isBlank()) {
            rack.idleLine = "why required"
            return
        }
        if (!decideArmed) {
            decideArmed = true
            armToken += 1
            val token = armToken
            rack.idleLine = "Publish? tap paper again"
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
