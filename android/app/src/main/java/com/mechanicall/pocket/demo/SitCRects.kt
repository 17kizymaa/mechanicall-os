package com.mechanicall.pocket.demo

import android.graphics.Rect
import android.graphics.RectF

/** Pack pixels for 1080×2138 skins. Preview 576×1248 × (1080/576, 2138/1248). Paint wins. */
data class PackRect(val l: Int, val t: Int, val r: Int, val b: Int) {
    fun contains(x: Float, y: Float): Boolean = x >= l && x < r && y >= t && y < b
    fun toRect(): Rect = Rect(l, t, r, b)
    fun toRectF(): RectF = RectF(l.toFloat(), t.toFloat(), r.toFloat(), b.toFloat())
    val w: Int get() = r - l
    val h: Int get() = b - t

    fun row(n: Int, i: Int): PackRect {
        val span = h / n
        val top = t + i * span
        val bot = if (i == n - 1) b else top + span
        return PackRect(l, top, r, bot)
    }
}

enum class SitPlate { SPLASH, BIND, PLAN, DRAFT, DECIDE, NEXT, RECEIPT }

/** CRT dest = leftover-lab tube. DRAFT dest = paper writer. */
enum class IsolatedMode { NONE, CRT, DRAFT }

enum class SitHit {
    Lcd,
    LcdPrev,
    LcdNext,
    Gate,
    BankPlan,
    BankDraft,
    BankDecide,
    BankReceipt,
    BindPaper,
    FieldObjective,
    FieldNext,
    FieldKeep,
    FieldReject,
    FieldLimits,
    FieldAlpha,
    FieldBeta,
    FieldGamma,
    Tbc,
    Join,
    Send,
    Wake,
    DecidePaper,
    WhyStrip,
    DecideNotYet,
    DidIt,
    NotYetFeet,
    Files,
    DismissZoom,
    None,
}

/** Pack CRects from sit-ui-sprint WIRING.md. CRect is a cull; hit = topmost opaque. */
object SitCRects {
    const val PACK_W = 1080
    const val PACK_H = 2138
    const val ALPHA_HIT = 32

    /** MECHANICALL plaque. Never a control (U17). Dismiss fill. */
    val title = PackRect(131, 38, 949, 185)

    val lcd = PackRect(146, 254, 934, 767)
    /** Inner phosphor of the chassis STATUS hole. Peek text stays in this glass. */
    val lcdGlass = PackRect(176, 292, 904, 728)
    val lcdFill = PackRect(131, 185, 949, 1864)

    /**
     * Phosphor inset of a STATUS module dest.
     * sit_crt.png is crt-bezel-idle (504×382); glass src is (22,48)–(482,362).
     */
    fun glassIn(module: PackRect): PackRect {
        val w = module.w
        val h = module.h
        return PackRect(
            module.l + w * 22 / 504,
            module.t + h * 48 / 382,
            module.l + w * 482 / 504,
            module.t + h * 362 / 382,
        )
    }

    val join = PackRect(165, 877, 375, 1110)
    val send = PackRect(435, 870, 652, 1110)
    val wake = PackRect(705, 877, 922, 1110)

    val bankPlan = PackRect(165, 1158, 322, 1261)
    val bankDraft = PackRect(368, 1158, 525, 1261)
    val bankDecide = PackRect(570, 1158, 728, 1261)
    val bankReceipt = PackRect(772, 1158, 930, 1261)
    val banksDest = PackRect(135, 1144, 953, 1288)

    val well = PackRect(109, 1316, 971, 1836)
    /** Live receipt paper inside sit_well_receipt metal frame. Interchangeable inner. */
    val receiptPaper = PackRect(117, 1380, 965, 1813)
    /** Decide No / Not yet — blank plate under YES. */
    val decideNotYet = PackRect(160, 1688, 920, 1832)
    val bindPad = PackRect(262, 1405, 818, 1713)
    val files = PackRect(150, 1720, 938, 1830)

    val fieldObjective = well.row(5, 0)
    val fieldNext = well.row(5, 1)
    val fieldKeep = well.row(5, 2)
    val fieldReject = well.row(5, 3)
    val fieldLimits = well.row(5, 4)

    /** After Yes, Plan well: two feet. I did it is labour, not Yes. Not a 5th bank. */
    val didIt = well.row(2, 0)
    val notYetFeet = well.row(2, 1)

    val fieldAlpha = well.row(4, 0)
    val fieldBeta = well.row(4, 1)
    val fieldGamma = well.row(4, 2)
    val tbc = well.row(4, 3)

    val gate = PackRect(75, 1864, 1005, 2107)

    /** Full dest cull for isolated modes. Chassis stays off this dest (B11). */
    val isolatedGlass = PackRect(40, 40, 1040, 2098)

    /**
     * Dest CRT: sit_crt bezel borders the dest. Dark field, no chassis.
     * Glass is glassIn(this). Text pads inside that glass.
     */
    val isolatedCrt = PackRect(16, 48, 1064, 2040)

    /** Draft writer paper below the title plaque. Keyboard overlays chassis. */
    val isolatedScreen = PackRect(48, 196, 1032, 1860)
    /** IME field inside dest CRT glass (Why / peek). Keyboard overlays. */
    val isolatedEdit = PackRect(88, 360, 992, 620)
    val DraftPaper = 0xFFF3E6C8.toInt()
    val DraftInk = 0xFF2A2418.toInt()

    /** Send-folder settings panel. */
    val sendPanel = PackRect(70, 640, 1010, 1680)
    /** FOLDER plaque — tap to stage/send. Not Yes. */
    val folderSend = PackRect(110, 650, 970, 850)
    val folderList = PackRect(110, 860, 970, 1480)
    /** OEM FILES strip on the combined Send+FILES dest. */
    val folderOem = PackRect(110, 1508, 970, 1648)

    val Letterbox = 0xFF12100E.toInt()
    val IsolatedDark = 0xFF0A0A0C.toInt()
    val Dim = 0xCC0A0A0C.toInt()
    /** Darkened-room surround. Screen maximises over this night chassis. */
    val CrtRoom = 0xC80A0A0C.toInt()
    val LcdAmber = 0xFFE6C14A.toInt()
    val LcdFlash = 0x59E6C14A.toInt()
    val Hint = 0x99E6C14A.toInt()
    val TearRed = 0x80FF4444.toInt()
    val TearCyan = 0x8066DDFF.toInt()
    /** House ink on millwork paper. Violet = NOT ACTIVE. */
    val Violet = 0xFF5C3D8A.toInt()
    val QuietInk = 0xFF6A6458.toInt()
}
