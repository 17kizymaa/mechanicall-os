package com.mechanicall.pocket.demo

import android.animation.ValueAnimator
import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Canvas
import android.graphics.Matrix
import android.graphics.Paint
import android.graphics.Rect
import android.graphics.RectF
import android.graphics.Typeface
import android.text.Layout
import android.text.StaticLayout
import android.text.TextPaint
import android.util.AttributeSet
import android.view.MotionEvent
import android.view.View
import android.view.animation.LinearInterpolator
import android.widget.EditText
import android.widget.FrameLayout
import kotlin.math.roundToInt

/**
 * One CBitmap + CRect hits. LCD text clipped to STATUS glass.
 * Not Compose. Not millwork-as-layout.
 */
class SitRackView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
) : FrameLayout(context, attrs) {

    interface Host {
        fun onHit(hit: SitHit)
        fun onDraftChanged(fields: Map<String, String>)
        fun onWhyChanged(why: String)
    }

    var host: Host? = null

    var plate: SitPlate = SitPlate.SPLASH
        set(value) {
            if (field != value) {
                field = value
                zoomed = false
                syncEditors()
                invalidate()
            }
        }

    var idleLine: String = ""
        set(value) {
            field = value
            invalidate()
        }

    var pages: List<LawPage> = emptyList()
        set(value) {
            field = value
            invalidate()
        }

    var pageIndex: Int = 0
        set(value) {
            val n = pages.size.coerceAtLeast(1)
            val next = ((value % n) + n) % n
            if (field != next) {
                field = next
                glitch()
                invalidate()
            }
        }

    var zoomed: Boolean = false
        set(value) {
            if (field != value) {
                field = value
                glitch()
                syncEditors()
                invalidate()
            }
        }

    var whyText: String = ""
        set(value) {
            field = value
            if (why.hasFocus().not() && why.text.toString() != value) {
                why.setText(value)
            }
        }

    var draftFields: Map<String, String> = emptyMap()
        set(value) {
            field = value
            if (!alpha.hasFocus()) alpha.setText(value["Objective"].orEmpty())
            if (!beta.hasFocus()) beta.setText(value["Next"].orEmpty())
            if (!gamma.hasFocus()) gamma.setText(value["Baseline"].orEmpty())
        }

    private val blit = Matrix()
    private val inverse = Matrix()
    private val packPoint = FloatArray(2)
    private var dest = RectF()

    private var splashBmp: Bitmap? = null
    private var bindBmp: Bitmap? = null
    private var planBmp: Bitmap? = null
    private var draftBmp: Bitmap? = null

    private val bitmapPaint = Paint(Paint.FILTER_BITMAP_FLAG)
    private val flashPaint = Paint()
    private val tearPaint = Paint()
    private val lcdPaint = TextPaint(Paint.ANTI_ALIAS_FLAG).apply {
        color = SitCRects.LcdAmber
        typeface = Typeface.MONOSPACE
        isFakeBoldText = true
    }

    private var glitchAmt = 0f
    private var tear = 0f
    private var animator: ValueAnimator? = null

    private val alpha = editor("Field Objective")
    private val beta = editor("Field Next")
    private val gamma = editor("Field Baseline")
    private val why = editor("Why")

    init {
        setWillNotDraw(false)
        setBackgroundColor(SitCRects.Letterbox)
        contentDescription = "sit millwork"
        importantForAccessibility = IMPORTANT_FOR_ACCESSIBILITY_YES
        isClickable = true
        addView(alpha)
        addView(beta)
        addView(gamma)
        addView(why)
        decodeSkins()
        syncEditors()
    }

    private fun editor(desc: String): EditText = EditText(context).apply {
        setBackgroundColor(0x00000000)
        setTextColor(SitCRects.Ink)
        setHintTextColor(SitCRects.Hint)
        typeface = Typeface.MONOSPACE
        textSize = 13f
        hint = desc
        contentDescription = desc
        visibility = GONE
        setPadding(12, 8, 12, 8)
        onFocusChangeListener = OnFocusChangeListener { _, has ->
            if (!has) emitDraft()
        }
    }

    private fun decodeSkins() {
        val opts = BitmapFactory.Options().apply { inScaled = false }
        splashBmp = BitmapFactory.decodeResource(resources, R.drawable.sit_splash, opts)
        bindBmp = BitmapFactory.decodeResource(resources, R.drawable.sit_bind, opts)
        planBmp = BitmapFactory.decodeResource(resources, R.drawable.sit_plan, opts)
            ?: BitmapFactory.decodeResource(resources, R.drawable.sit_skin, opts)
        draftBmp = BitmapFactory.decodeResource(resources, R.drawable.sit_draft, opts)
    }

    private fun skin(): Bitmap? = when (plate) {
        SitPlate.SPLASH -> splashBmp
        SitPlate.BIND -> bindBmp
        SitPlate.DRAFT -> draftBmp
        SitPlate.PLAN, SitPlate.DECIDE, SitPlate.RECEIPT -> planBmp
    }

    override fun onSizeChanged(w: Int, h: Int, oldw: Int, oldh: Int) {
        super.onSizeChanged(w, h, oldw, oldh)
        val pack = RectF(0f, 0f, SitCRects.PACK_W.toFloat(), SitCRects.PACK_H.toFloat())
        dest = RectF(0f, 0f, w.toFloat(), h.toFloat())
        blit.setRectToRect(pack, dest, Matrix.ScaleToFit.CENTER)
        blit.invert(inverse)
        requestLayout()
    }

    override fun onLayout(changed: Boolean, left: Int, top: Int, right: Int, bottom: Int) {
        super.onLayout(changed, left, top, right, bottom)
        layoutPack(alpha, SitCRects.fieldAlpha)
        layoutPack(beta, SitCRects.fieldBeta)
        layoutPack(gamma, SitCRects.fieldGamma)
        layoutPack(why, SitCRects.tbc)
    }

    private fun layoutPack(child: View, r: PackRect) {
        val d = mapPack(r)
        val l = d.left.roundToInt()
        val t = d.top.roundToInt()
        val rr = d.right.roundToInt()
        val b = d.bottom.roundToInt()
        child.measure(
            MeasureSpec.makeMeasureSpec((rr - l).coerceAtLeast(0), MeasureSpec.EXACTLY),
            MeasureSpec.makeMeasureSpec((b - t).coerceAtLeast(0), MeasureSpec.EXACTLY),
        )
        child.layout(l, t, rr, b)
    }

    private fun mapPack(r: PackRect): RectF {
        val pts = floatArrayOf(r.l.toFloat(), r.t.toFloat(), r.r.toFloat(), r.b.toFloat())
        blit.mapPoints(pts)
        return RectF(pts[0], pts[1], pts[2], pts[3])
    }

    private fun syncEditors() {
        val draftOn = plate == SitPlate.DRAFT && !zoomed
        val decideOn = plate == SitPlate.DECIDE && !zoomed
        alpha.visibility = if (draftOn) VISIBLE else GONE
        beta.visibility = if (draftOn) VISIBLE else GONE
        gamma.visibility = if (draftOn) VISIBLE else GONE
        why.visibility = if (decideOn) VISIBLE else GONE
        if (decideOn) why.hint = "why"
        if (draftOn) {
            alpha.hint = "Objective"
            beta.hint = "Next"
            gamma.hint = "Baseline"
        }
    }

    private fun emitDraft() {
        host?.onDraftChanged(
            mapOf(
                "Objective" to alpha.text.toString(),
                "Next" to beta.text.toString(),
                "Baseline" to gamma.text.toString(),
            ),
        )
        host?.onWhyChanged(why.text.toString())
    }

    fun whyNow(): String = why.text.toString()

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        canvas.drawColor(SitCRects.Letterbox)
        val bmp = skin() ?: return
        canvas.drawBitmap(bmp, blit, bitmapPaint)
        val glass = if (zoomed) SitCRects.lcdZoom else SitCRects.lcd
        if (zoomed) {
            val src = SitCRects.lcd.toRect()
            val dst = mapPack(SitCRects.lcdZoom)
            canvas.drawBitmap(bmp, src, dst, bitmapPaint)
        }
        drawLcd(canvas, glass)
    }

    private fun drawLcd(canvas: Canvas, glass: PackRect) {
        val dst = mapPack(glass)
        canvas.save()
        canvas.clipRect(dst)
        canvas.translate(dst.left + tear, dst.top)
        if (glitchAmt > 0f) {
            flashPaint.color = SitCRects.LcdFlash
            canvas.drawRect(0f, 0f, dst.width(), dst.height(), flashPaint)
            val y = dst.height() * 0.4f
            tearPaint.strokeWidth = 2f
            tearPaint.color = SitCRects.TearRed
            canvas.drawLine(0f, y, dst.width(), y, tearPaint)
            tearPaint.color = SitCRects.TearCyan
            canvas.drawLine(0f, y + 3f, dst.width(), y + 3f, tearPaint)
        }
        val body = lcdBody()
        lcdPaint.textSize = if (zoomed) sp(11f) else sp(13f)
        val pad = sp(8f)
        val innerW = (dst.width() - pad * 2).toInt().coerceAtLeast(8)
        val layout = StaticLayout.Builder
            .obtain(body, 0, body.length, lcdPaint, innerW)
            .setAlignment(Layout.Alignment.ALIGN_NORMAL)
            .setIncludePad(false)
            .build()
        canvas.translate(pad, pad)
        layout.draw(canvas)
        canvas.restore()
    }

    private fun lcdBody(): String {
        if (!zoomed) return idleLine
        val page = pages.getOrNull(pageIndex)
        val text = page?.body?.ifBlank { "(none)" } ?: "(none)"
        return "LAW · ${page?.title.orEmpty()}\n$text"
    }

    private fun sp(v: Float): Float = v * resources.displayMetrics.scaledDensity

    private fun glitch() {
        animator?.cancel()
        glitchAmt = 1f
        tear = 4f
        animator = ValueAnimator.ofFloat(1f, 0f).apply {
            duration = 150
            interpolator = LinearInterpolator()
            addUpdateListener {
                glitchAmt = it.animatedValue as Float
                tear = if (glitchAmt > 0.5f) 5f else if (glitchAmt > 0.2f) -4f else 0f
                invalidate()
            }
            start()
        }
    }

    override fun onTouchEvent(event: MotionEvent): Boolean {
        if (event.actionMasked == MotionEvent.ACTION_DOWN) return true
        if (event.actionMasked != MotionEvent.ACTION_UP) return true
        packPoint[0] = event.x
        packPoint[1] = event.y
        inverse.mapPoints(packPoint)
        val x = packPoint[0]
        val y = packPoint[1]
        val hit = hitAt(x, y)
        if (hit != SitHit.None) {
            host?.onHit(hit)
        }
        return true
    }

    private fun hitAt(x: Float, y: Float): SitHit {
        if (zoomed) {
            val g = SitCRects.lcdZoom
            if (g.contains(x, y)) {
                val w = g.w.toFloat()
                val lx = x - g.l
                return when {
                    lx < w * 0.18f -> SitHit.LcdPrev
                    lx > w * 0.82f -> SitHit.LcdNext
                    else -> SitHit.Lcd
                }
            }
            if (SitCRects.gate.contains(x, y)) return SitHit.Gate
            bankHit(x, y)?.let { return it }
            return SitHit.DismissZoom
        }
        if (SitCRects.lcd.contains(x, y)) return SitHit.Lcd
        if (SitCRects.gate.contains(x, y)) return SitHit.Gate
        bankHit(x, y)?.let { return it }
        return when (plate) {
            SitPlate.SPLASH -> SitHit.None
            SitPlate.BIND -> if (SitCRects.bindPaper.contains(x, y) || SitCRects.paper.contains(x, y)) {
                SitHit.BindPaper
            } else SitHit.None
            SitPlate.PLAN -> when {
                SitCRects.wakePlan.contains(x, y) -> SitHit.Wake
                SitCRects.objective.contains(x, y) -> SitHit.FieldObjective
                SitCRects.next.contains(x, y) -> SitHit.FieldNext
                SitCRects.keep.contains(x, y) -> SitHit.FieldKeep
                SitCRects.reject.contains(x, y) -> SitHit.FieldReject
                SitCRects.limits.contains(x, y) -> SitHit.FieldLimits
                else -> SitHit.None
            }
            SitPlate.DRAFT -> when {
                SitCRects.fieldAlpha.contains(x, y) -> SitHit.FieldAlpha
                SitCRects.fieldBeta.contains(x, y) -> SitHit.FieldBeta
                SitCRects.fieldGamma.contains(x, y) -> SitHit.FieldGamma
                SitCRects.tbc.contains(x, y) -> SitHit.Tbc
                SitCRects.join.contains(x, y) -> SitHit.Join
                SitCRects.send.contains(x, y) -> SitHit.Send
                SitCRects.wake.contains(x, y) -> SitHit.Wake
                else -> SitHit.None
            }
            SitPlate.DECIDE -> when {
                SitCRects.paper.contains(x, y) -> SitHit.DecidePaper
                else -> SitHit.None
            }
            SitPlate.RECEIPT -> SitHit.None
        }
    }

    private fun bankHit(x: Float, y: Float): SitHit? = when {
        SitCRects.bankPlan.contains(x, y) -> SitHit.BankPlan
        SitCRects.bankDraft.contains(x, y) -> SitHit.BankDraft
        SitCRects.bankDecide.contains(x, y) -> SitHit.BankDecide
        SitCRects.bankReceipt.contains(x, y) -> SitHit.BankReceipt
        else -> null
    }

    override fun onDetachedFromWindow() {
        animator?.cancel()
        super.onDetachedFromWindow()
    }
}
