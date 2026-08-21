package com.mechanicall.pocket.demo

import android.content.Context
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import kotlinx.coroutines.delay
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.mechanicall.pocket.demo.modules.BindModule
import com.mechanicall.pocket.demo.modules.ChatHome
import com.mechanicall.pocket.demo.modules.DecideModule
import com.mechanicall.pocket.demo.modules.PlanModule
import com.mechanicall.pocket.demo.modules.ReceiptModule
import com.mechanicall.pocket.demo.modules.SplashScreen
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import androidx.compose.runtime.rememberCoroutineScope

sealed class SeatRoute(val title: String, val key: String) {
    data object Splash : SeatRoute("", "splash")
    data object Bind : SeatRoute("FOLDER", "bind")
    data object Plan : SeatRoute("PLAN", "plan")
    data object Home : SeatRoute("DRAFT", "draft")
    data object Decide : SeatRoute("DECIDE", "decide")
    data object Receipt : SeatRoute("RECEIPT", "receipt")

    companion object {
        val pages: List<SeatRoute> = listOf(Plan, Home, Decide, Receipt)
    }
}

fun landingFrom(face: FaceState): SeatRoute {
    if (!face.bound || face.refused) return SeatRoute.Bind
    return when (face.walk) {
        "decide" -> SeatRoute.Decide
        "receipt" -> SeatRoute.Receipt
        else -> SeatRoute.Plan
    }
}

private const val PREFS = "mechanicall_seat"
private const val PREF_POCKET = "pocket_one"

@Composable
fun SeatNav() {
    val context = LocalContext.current
    val prefs = remember { context.getSharedPreferences(PREFS, Context.MODE_PRIVATE) }
    var currentRoute by remember { mutableStateOf<SeatRoute>(SeatRoute.Splash) }
    var pocket by remember {
        mutableStateOf(prefs.getString(PREF_POCKET, "") ?: "")
    }
    var face by remember { mutableStateOf(FaceState()) }
    var bindOpen by remember { mutableStateOf(false) }
    var gate by remember { mutableStateOf(GateState()) }
    var deskOn by remember { mutableStateOf(false) }
    var join by remember { mutableStateOf(JoinState()) }
    var wake by remember { mutableStateOf(WakeState()) }
    var offer by remember { mutableStateOf(OfferState()) }
    var invitePaste by remember { mutableStateOf("") }
    var deskNote by remember { mutableStateOf("JOIN and WAKE are not Yes.") }
    val scope = rememberCoroutineScope()

    fun persistPocket(path: String) {
        pocket = path
        prefs.edit().putString(PREF_POCKET, path).apply()
    }

    fun reload(): FaceState {
        val next = FaceBridge.faceState(pocket)
        face = next
        if (next.bound && !next.refused && next.path.isNotBlank()) {
            persistPocket(next.path)
        }
        return next
    }

    val projectOn = face.bound && !face.refused

    fun go(route: SeatRoute) {
        currentRoute = route
        if (route != SeatRoute.Splash) reload()
    }

    if (currentRoute is SeatRoute.Splash) {
        SplashScreen(
            onFinished = {
                go(landingFrom(reload()))
            },
        )
        return
    }

    LaunchedEffect(pocket) {
        while (true) {
            gate = FaceBridge.gateState(pocket)
            offer = FaceBridge.offerStatus(pocket)
            delay(120)
        }
    }
    LaunchedEffect(pocket) {
        val probe = FaceBridge.deskProbe(
            pocket,
            "http://myarch:11434,http://127.0.0.1:11434,http://192.168.0.51:11434,http://100.90.85.68:11434",
        )
        deskOn = probe.ok
        join = FaceBridge.joinStatus(pocket)
        if (join.status == "connected") {
            deskOn = true
        }
    }

    PluginWindow {
        PluginTitleBar(
            title = if (projectOn) {
                pocket.substringAfterLast('/').ifBlank { currentRoute.title }
            } else {
                "FOLDER"
            },
            showSlots = projectOn,
            onFolder = { bindOpen = true },
            onFiles = { openBoundInFileManager(context, pocket) },
        )
        LcdStrip(
            if (projectOn) {
                val phase = when (gate.state) {
                    "load" -> "LOAD ${gate.step}/${gate.steps}"
                    "gate" -> "STREAM ${gate.step}/${gate.steps}"
                    "queued" -> "QUEUE ${gate.queue}"
                    "warm" -> "WARM"
                    "quiet" -> "QUIET"
                    else -> "IDLE"
                }
                "${face.next.ifBlank { "(no Next)" }} · $phase".take(72)
            } else {
                "Name your folder. One project."
            },
        )
        GateStrip(
            state = gate.state,
            step = gate.step,
            steps = gate.steps,
            deskOn = deskOn || gate.desk.isNotBlank() || join.status == "connected",
            queue = gate.queue,
        )
        if (projectOn) {
            DeskStrip(
                joinStatus = join.status,
                wakeStatus = wake.status,
                paste = invitePaste,
                onPaste = { invitePaste = it },
                onJoin = {
                    val pasted = invitePaste
                    scope.launch {
                        val next = withContext(Dispatchers.IO) {
                            FaceBridge.joinAccept(pocket, pasted)
                        }
                        join = next
                        deskNote = next.note.ifBlank { "JOIN is not Yes." }
                        invitePaste = ""
                        if (next.status == "connected") deskOn = true
                    }
                },
                onWake = {
                    scope.launch {
                        val next = withContext(Dispatchers.IO) {
                            FaceBridge.wakeDesk(pocket, "")
                        }
                        wake = next
                        deskNote = next.note
                    }
                },
                joinEnabled = invitePaste.isNotBlank(),
                wakeEnabled = join.status == "connected" || deskOn,
                note = deskNote,
                offerNotify = offer.notify,
                offerKind = offer.kind,
                onAcceptOffer = {
                    scope.launch {
                        val next = withContext(Dispatchers.IO) {
                            FaceBridge.acceptOffer(pocket)
                        }
                        offer = FaceBridge.offerStatus(pocket)
                        deskNote = next.note.ifBlank { "Accepted. Not Yes." }
                        reload()
                    }
                },
                onDeclineOffer = {
                    scope.launch {
                        withContext(Dispatchers.IO) { FaceBridge.declineOffer(pocket) }
                        offer = FaceBridge.offerStatus(pocket)
                        deskNote = "Declined. Not Yes."
                    }
                },
                onStageUpload = {
                    scope.launch {
                        val raw = withContext(Dispatchers.IO) {
                            FaceBridge.stageUpload(pocket)
                        }
                        deskNote = if (raw.startsWith("ERROR:")) raw else "Staged upload. Not Yes."
                    }
                },
            )
        }
        if (projectOn) {
            PluginTabs(
                items = SeatRoute.pages.map { it.key to it.title },
                selected = currentRoute.key,
                onSelect = { key ->
                    SeatRoute.pages.firstOrNull { it.key == key }?.let { go(it) }
                },
            )
        }
        androidx.compose.foundation.layout.Box(
            Modifier.weight(1f).fillMaxWidth(),
        ) {
            when {
                !projectOn || currentRoute is SeatRoute.Bind -> BindModule(
                    pocket = pocket,
                    face = face,
                    onPocketChange = { persistPocket(it) },
                    onBind = { named ->
                        persistPocket(named)
                        val next = FaceBridge.bindFolder(named)
                        face = next
                        if (next.bound && !next.refused && next.path.isNotBlank()) {
                            persistPocket(next.path)
                            go(landingFrom(next))
                        }
                    },
                )
                currentRoute is SeatRoute.Splash -> SplashScreen(
                    onFinished = { go(landingFrom(reload())) },
                )
                currentRoute is SeatRoute.Home -> ChatHome(
                    face = face,
                    pocket = pocket,
                    onReload = { reload() },
                )
                currentRoute is SeatRoute.Plan -> PlanModule(face = face, pocket = pocket)
                currentRoute is SeatRoute.Decide -> DecideModule(
                    pocket = pocket,
                    onReload = { reload() },
                )
                currentRoute is SeatRoute.Receipt -> ReceiptModule(face = face, pocket = pocket)
            }
        }
    }

    fun closeOverlays() {
        bindOpen = false
    }

    if (bindOpen) {
        Dialog(
            onDismissRequest = {
                if (face.bound && !face.refused) bindOpen = false
            },
            properties = DialogProperties(
                usePlatformDefaultWidth = false,
                dismissOnClickOutside = true,
            ),
        ) {
            PluginDialogFrame(
                title = "FOLDER",
                actionLabel = "CLOSE",
                onAction = {
                    if (face.bound && !face.refused) bindOpen = false
                },
                onScrim = {
                    if (face.bound && !face.refused) bindOpen = false
                },
            ) {
                BindModule(
                    pocket = pocket,
                    face = face,
                    onPocketChange = { persistPocket(it) },
                    onBind = { named ->
                        persistPocket(named)
                        val next = FaceBridge.bindFolder(named)
                        face = next
                        if (next.bound && !next.refused && next.path.isNotBlank()) {
                            persistPocket(next.path)
                            bindOpen = false
                            go(landingFrom(next))
                        }
                    },
                )
            }
        }
    }

}

