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
}

enum class SitPlate { SPLASH, BIND, PLAN, DRAFT, DECIDE, RECEIPT }

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
    DismissZoom,
    None,
}

object SitCRects {
    const val PACK_W = 1080
    const val PACK_H = 2138

    val title = PackRect(75, 41, 1005, 171)
    val bankPlan = PackRect(75, 41, 307, 171)
    val bankDraft = PackRect(307, 41, 540, 171)
    val bankDecide = PackRect(540, 41, 772, 171)
    val bankReceipt = PackRect(772, 41, 1005, 171)

    /** STATUS glass on plan/bind/draft/splash (measured on plan.png). */
    val lcd = PackRect(135, 302, 945, 774)
    /** Enlarged glass: below title, above GATE. Law text clips here. */
    val lcdZoom = PackRect(105, 188, 975, 1860)

    val join = PackRect(131, 857, 356, 1114)
    val send = PackRect(422, 857, 666, 1114)
    val wake = PackRect(722, 857, 966, 1114)
    val wakePlan = PackRect(788, 891, 1013, 1131)

    val bindPaper = PackRect(169, 908, 911, 1456)
    val paper = PackRect(90, 822, 990, 1884)

    val objective = PackRect(90, 822, 750, 1131)
    val next = PackRect(525, 925, 1005, 1268)
    val keep = PackRect(90, 1199, 750, 1508)
    val reject = PackRect(469, 1371, 1005, 1713)
    val limits = PackRect(90, 1713, 1005, 1902)

    val fieldAlpha = PackRect(131, 908, 949, 1114)
    val fieldBeta = PackRect(131, 1165, 949, 1371)
    val fieldGamma = PackRect(131, 1422, 949, 1627)
    val tbc = PackRect(131, 1679, 949, 1884)

    val gate = PackRect(75, 1919, 1005, 2121)

    val Letterbox = 0xFF12100E.toInt()
    val LcdAmber = 0xFFE6C14A.toInt()
    val LcdFlash = 0x59E6C14A.toInt()
    val Ink = 0xFF1B1814.toInt()
    val Hint = 0xFF8A8070.toInt()
    val TearRed = 0x80FF4444.toInt()
    val TearCyan = 0x8066DDFF.toInt()
}
