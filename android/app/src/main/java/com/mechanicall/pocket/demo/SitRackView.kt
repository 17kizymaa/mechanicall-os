package com.mechanicall.pocket.demo

import android.animation.ValueAnimator
import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Matrix
import android.graphics.Paint
import android.graphics.Rect
import android.graphics.RectF
import android.graphics.Typeface
import android.text.Editable
import android.text.InputType
import android.text.Layout
import android.text.StaticLayout
import android.text.TextPaint
import android.text.TextWatcher
import android.util.AttributeSet
import android.view.Gravity
import android.view.MotionEvent
import android.view.View
import android.view.animation.LinearInterpolator
import android.view.inputmethod.EditorInfo
import android.view.inputmethod.InputMethodManager
import android.widget.EditText
import android.widget.FrameLayout
import kotlin.math.roundToInt

/**
 * Overlay stack + alpha hits. Kotlin glyphs only on the CRT dest.
 * Not Compose. Not millwork-as-layout. Wiring: sit-ui-sprint WIRING.md.
 */
class SitRackView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
) : FrameLayout(context, attrs) {

    interface Host {
        fun onHit(hit: SitHit)
        fun onDraftChanged(fields: Map<String, String>)
        fun onDraftTextChanged(text: String)
        fun onWhyChanged(why: String)
    }

    var host: Host? = null

    var plate: SitPlate = SitPlate.SPLASH
        set(value) {
            if (field != value) {
                field = value
                zoomed = false
                if (value != SitPlate.DRAFT) isolated = IsolatedMode.NONE
                sendOverlay = false
                hideCrtEdit()
                syncEditors()
                invalidate()
            }
        }

    var isolated: IsolatedMode = IsolatedMode.NONE
        set(value) {
            if (field != value) {
                field = value
                if (value != IsolatedMode.NONE) {
                    zoomed = false
                    sendOverlay = false
                }
                if (value != IsolatedMode.DRAFT && plate != SitPlate.DECIDE) {
                    hideCrtEdit()
                }
                glitch()
                syncEditors()
                invalidate()
            }
        }

    var sendOverlay: Boolean = false
        set(value) {
            if (field != value) {
                field = value
                if (value) isolated = IsolatedMode.NONE
                invalidate()
            }
        }

    var sendStatus: String = "idle"
        set(value) {
            field = value
            invalidate()
        }
    var sendNote: String = ""
        set(value) {
            field = value
            invalidate()
        }
    var folderList: String = ""
        set(value) {
            field = value
            invalidate()
        }
    var gatePercent: Int = 0
        set(value) {
            if (field != value) {
                field = value
                invalidate()
            }
        }
    var gateDirection: String = ""
        set(value) {
            if (field != value) {
                field = value
                invalidate()
            }
        }
    var receiptBody: String = ""
    var liveFields: Map<String, String> = emptyMap()

    /** After Yes: stay on PLAN. Well is labour feet. Not SitPlate.NEXT. */
    var labour: Boolean = false
        set(value) {
            if (field != value) {
                field = value
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
            if (editKey == "Why" && crtEdit.hasFocus().not() && crtEdit.text.toString() != value) {
                crtEdit.setText(value)
            }
        }

    var draftFields: Map<String, String> = emptyMap()
        set(value) {
            field = value
            if (editKey != null && editKey != "Why" && !crtEdit.hasFocus()) {
                crtEdit.setText(value[editKey].orEmpty())
            }
        }

    private val blit = Matrix()
    private val inverse = Matrix()
    private val packPoint = FloatArray(2)
    private var dest = RectF()

    private var splashBmp: Bitmap? = null
    private var fieldBmp: Bitmap? = null
    private var chassisBmp: Bitmap? = null
    private var crtBmp: Bitmap? = null
    private var lampJoinBmp: Bitmap? = null
    private var lampSendBmp: Bitmap? = null
    private var lampWakeBmp: Bitmap? = null
    private var banksBmp: Bitmap? = null
    private var wellBindBmp: Bitmap? = null
    private var wellPlanBmp: Bitmap? = null
    private var wellDraftBmp: Bitmap? = null
    private var wellDecideBmp: Bitmap? = null
    private var wellNextBmp: Bitmap? = null
    private var wellReceiptBmp: Bitmap? = null
    private var folderDestBmp: Bitmap? = null
    private var gateBmp: Bitmap? = null
    private val crtGlassSrc = Rect()

    private val bitmapPaint = Paint(Paint.FILTER_BITMAP_FLAG)
    private val flashPaint = Paint()
    private val tearPaint = Paint()
    private val dimPaint = Paint()
    private val lcdPaint = TextPaint(Paint.ANTI_ALIAS_FLAG).apply {
        color = SitCRects.LcdAmber
        typeface = Typeface.MONOSPACE
        isFakeBoldText = true
    }
    private val paperPaint = TextPaint(Paint.ANTI_ALIAS_FLAG).apply {
        color = SitCRects.DraftInk
        typeface = Typeface.MONOSPACE
    }
    private val paperFill = Paint().apply { color = SitCRects.DraftPaper }
    private val graphitePaint = TextPaint(Paint.ANTI_ALIAS_FLAG).apply {
        color = SitCRects.QuietInk
        typeface = Typeface.MONOSPACE
    }

    private var glitchAmt = 0f
    private var tear = 0f
    private var animator: ValueAnimator? = null

    private var editKey: String? = null
    private var suppressEdit: Boolean = false
    private val crtEdit = editor()

    init {
        setWillNotDraw(false)
        setBackgroundColor(SitCRects.Letterbox)
        contentDescription = "sit millwork"
        importantForAccessibility = IMPORTANT_FOR_ACCESSIBILITY_YES
        isClickable = true
        addView(crtEdit)
        decodeSkins()
        syncEditors()
    }

    private fun editor(): EditText = EditText(context).apply {
        typeface = Typeface.MONOSPACE
        visibility = GONE
        setPadding(28, 24, 28, 24)
        styleWhyEditor(this)
        onFocusChangeListener = OnFocusChangeListener { _, has ->
            if (!has) emitDraft()
        }
        setOnEditorActionListener { _, actionId, _ ->
            if (editKey == "PROPOSE") return@setOnEditorActionListener false
            emitDraft()
            if (actionId == EditorInfo.IME_ACTION_DONE) {
                val imm = context.getSystemService(Context.INPUT_METHOD_SERVICE) as InputMethodManager
                imm.hideSoftInputFromWindow(windowToken, 0)
                clearFocus()
                true
            } else {
                false
            }
        }
        addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) = Unit
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) = Unit
            override fun afterTextChanged(s: Editable?) {
                if (suppressEdit) return
                if (editKey == "PROPOSE") host?.onDraftTextChanged(s?.toString().orEmpty())
            }
        })
    }

    private fun styleWhyEditor(ed: EditText = crtEdit) {
        ed.setBackgroundColor(0x00000000)
        ed.setTextColor(SitCRects.LcdAmber)
        ed.setHintTextColor(SitCRects.Hint)
        ed.highlightColor = 0x33E6C14A
        ed.textSize = 13f
        ed.gravity = Gravity.TOP or Gravity.START
        ed.imeOptions = EditorInfo.IME_ACTION_DONE
        ed.inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_FLAG_MULTI_LINE
        ed.setHorizontallyScrolling(false)
        ed.isVerticalScrollBarEnabled = false
    }

    private fun styleDraftWriter(ed: EditText = crtEdit) {
        ed.setBackgroundColor(SitCRects.DraftPaper)
        ed.setTextColor(SitCRects.DraftInk)
        ed.setHintTextColor(0x992A2418.toInt())
        ed.highlightColor = 0x332A2418
        ed.textSize = 15f
        ed.gravity = Gravity.TOP or Gravity.START
        ed.imeOptions = EditorInfo.IME_FLAG_NO_ENTER_ACTION
        ed.inputType = InputType.TYPE_CLASS_TEXT or
            InputType.TYPE_TEXT_FLAG_MULTI_LINE or
            InputType.TYPE_TEXT_FLAG_IME_MULTI_LINE
        ed.setHorizontallyScrolling(false)
        ed.isVerticalScrollBarEnabled = true
        ed.hint = "NOT ACTIVE — not the plan"
        ed.contentDescription = "draft NOT ACTIVE"
    }

    private fun decodeSkins() {
        splashBmp = decode(R.drawable.sit_splash)
        fieldBmp = decode(R.drawable.sit_field)
        chassisBmp = decode(R.drawable.sit_chassis)
        crtBmp = decode(R.drawable.sit_crt)
        lampJoinBmp = decode(R.drawable.sit_lamp_join)
        lampSendBmp = decode(R.drawable.sit_lamp_send)
        lampWakeBmp = decode(R.drawable.sit_lamp_wake)
        banksBmp = decode(R.drawable.sit_banks)
        wellBindBmp = decode(R.drawable.sit_well_bind)
        wellPlanBmp = decode(R.drawable.sit_well_plan)
        wellDraftBmp = decode(R.drawable.sit_well_draft)
        wellDecideBmp = decode(R.drawable.sit_well_decide)
        wellNextBmp = decode(R.drawable.sit_well_next)
        wellReceiptBmp = decode(R.drawable.sit_well_receipt)
        folderDestBmp = decode(R.drawable.sit_folder_dest)
        gateBmp = decode(R.drawable.sit_gate)
        crtBmp?.let { bmp ->
            crtGlassSrc.set(
                (22f / 504f * bmp.width).roundToInt(),
                (48f / 382f * bmp.height).roundToInt(),
                (482f / 504f * bmp.width).roundToInt(),
                (362f / 382f * bmp.height).roundToInt(),
            )
        }
    }

    private fun decode(id: Int): Bitmap? {
        val opts = BitmapFactory.Options().apply {
            inScaled = false
            inPreferredConfig = Bitmap.Config.ARGB_8888
        }
        val bmp = BitmapFactory.decodeResource(resources, id, opts) ?: return null
        return if (bmp.config == Bitmap.Config.ARGB_8888) {
            bmp
        } else {
            bmp.copy(Bitmap.Config.ARGB_8888, false)
        }
    }

    private fun wellBmp(): Bitmap? = when (plate) {
        SitPlate.BIND -> wellBindBmp
        SitPlate.PLAN -> if (labour) wellNextBmp else wellPlanBmp
        SitPlate.DRAFT -> wellDraftBmp
        SitPlate.DECIDE -> wellDecideBmp
        SitPlate.NEXT -> wellNextBmp
        SitPlate.RECEIPT -> wellReceiptBmp
        else -> null
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
        layoutPack(crtEdit, crtTypeDest())
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
        val show = editKey != null && plate != SitPlate.SPLASH
        when (editKey) {
            "PROPOSE" -> styleDraftWriter()
            "Why" -> {
                styleWhyEditor()
                crtEdit.hint = "why"
                crtEdit.contentDescription = "why"
                if (!crtEdit.hasFocus() && crtEdit.text.toString() != whyText) {
                    setEditText(whyText)
                }
            }
            else -> styleWhyEditor()
        }
        crtEdit.visibility = if (show) VISIBLE else GONE
        if (editKey != "PROPOSE") {
            crtEdit.textSize = if (isolated != IsolatedMode.NONE || zoomed) 14f else 13f
        }
        requestLayout()
    }

    private fun setEditText(text: String) {
        if (crtEdit.text.toString() == text) return
        suppressEdit = true
        crtEdit.setText(text)
        crtEdit.setSelection(0)
        suppressEdit = false
    }

    fun dismissEdit() {
        hideCrtEdit()
        syncEditors()
        invalidate()
    }

    fun editOnCrt(key: String, text: String, hint: String) {
        editKey = key
        styleWhyEditor()
        crtEdit.hint = hint
        crtEdit.contentDescription = hint
        if (!crtEdit.hasFocus()) setEditText(text)
        crtEdit.visibility = VISIBLE
        crtEdit.requestFocus()
        val imm = context.getSystemService(Context.INPUT_METHOD_SERVICE) as InputMethodManager
        imm.showSoftInput(crtEdit, InputMethodManager.SHOW_IMPLICIT)
        requestLayout()
        invalidate()
    }

    /** Whole-file PROPOSE editor. Not schema keys. Not CURRENT. Keyboard overlays. */
    fun editDraftWriter(text: String) {
        isolated = IsolatedMode.DRAFT
        editKey = "PROPOSE"
        styleDraftWriter()
        if (!crtEdit.hasFocus() || crtEdit.text.toString() != text) setEditText(text)
        crtEdit.visibility = VISIBLE
        crtEdit.requestFocus()
        val imm = context.getSystemService(Context.INPUT_METHOD_SERVICE) as InputMethodManager
        imm.showSoftInput(crtEdit, InputMethodManager.SHOW_IMPLICIT)
        requestLayout()
        invalidate()
    }

    private fun hideCrtEdit() {
        emitDraft()
        editKey = null
        crtEdit.visibility = GONE
        crtEdit.clearFocus()
        val imm = context.getSystemService(Context.INPUT_METHOD_SERVICE) as InputMethodManager
        imm.hideSoftInputFromWindow(crtEdit.windowToken, 0)
    }

    private fun emitDraft() {
        val typed = crtEdit.text.toString()
        when (editKey) {
            "Why" -> {
                whyText = typed
                host?.onWhyChanged(typed)
            }
            "PROPOSE" -> host?.onDraftTextChanged(typed)
            null -> host?.onWhyChanged(whyText)
            else -> {
                val next = draftFields.toMutableMap()
                next[editKey!!] = typed
                draftFields = next
                host?.onDraftChanged(next)
            }
        }
    }

    fun whyNow(): String {
        return if (editKey == "Why") crtEdit.text.toString() else whyText
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        canvas.drawColor(SitCRects.Letterbox)
        if (plate == SitPlate.SPLASH) {
            fieldBmp?.let { canvas.drawBitmap(it, blit, bitmapPaint) }
            splashBmp?.let { canvas.drawBitmap(it, blit, bitmapPaint) }
            blitLamps(canvas)
            return
        }
        if (isolated == IsolatedMode.CRT) {
            drawCrtDest(canvas)
            return
        }
        if (isolated == IsolatedMode.DRAFT) {
            drawDraftWriterDest(canvas)
            return
        }
        drawRackMillwork(canvas)
        drawCrtSurface(canvas)
        if (plate == SitPlate.DECIDE) drawDecideNotYet(canvas)
        if (plate == SitPlate.RECEIPT) drawReceiptWell(canvas)
        if (crtEdit.visibility != VISIBLE) {
            drawLcd(canvas, crtTypeDest())
        }
        if (sendOverlay) drawSendOverlay(canvas)
    }

    /** Dest CRT glass is inside sit_crt bezel. Draft writer fills isolatedScreen. */
    private fun crtTypeDest(): PackRect = when {
        isolated == IsolatedMode.CRT ->
            if (editKey != null) SitCRects.isolatedEdit else SitCRects.glassIn(SitCRects.isolatedCrt)
        isolated == IsolatedMode.DRAFT || editKey == "PROPOSE" -> SitCRects.isolatedScreen
        zoomed -> SitCRects.lcd
        else -> SitCRects.lcd
    }

    private fun blitLamps(canvas: Canvas) {
        lampJoinBmp?.let { canvas.drawBitmap(it, blit, bitmapPaint) }
        lampSendBmp?.let { canvas.drawBitmap(it, blit, bitmapPaint) }
        lampWakeBmp?.let { canvas.drawBitmap(it, blit, bitmapPaint) }
    }

    private fun drawRackMillwork(canvas: Canvas) {
        fieldBmp?.let { canvas.drawBitmap(it, blit, bitmapPaint) }
        chassisBmp?.let { canvas.drawBitmap(it, blit, bitmapPaint) }
        blitLamps(canvas)
        banksBmp?.let { canvas.drawBitmap(it, blit, bitmapPaint) }
        wellBmp()?.let { canvas.drawBitmap(it, blit, bitmapPaint) }
        gateBmp?.let { canvas.drawBitmap(it, blit, bitmapPaint) }
    }

    /** CRT module on the chassis. Not IsolatedDark flood. */
    private fun drawCrtDest(canvas: Canvas) {
        drawRackMillwork(canvas)
        val crt = crtBmp ?: return
        canvas.drawBitmap(crt, null, mapPack(SitCRects.isolatedCrt), bitmapPaint)
        if (crtEdit.visibility != VISIBLE) {
            drawLcd(canvas, SitCRects.glassIn(SitCRects.isolatedCrt))
        }
    }

    /** Draft dest: chassis + GATE millwork; paper is the text editor. Not a CRT dump. */
    private fun drawDraftWriterDest(canvas: Canvas) {
        drawRackMillwork(canvas)
        canvas.drawRect(mapPack(SitCRects.isolatedScreen), paperFill)
        if (crtEdit.visibility != VISIBLE) {
            drawPackText(
                canvas,
                SitCRects.isolatedScreen,
                "NOT ACTIVE\nnot the plan\ntap to write",
            )
        }
    }

    private fun drawCrtSurface(@Suppress("UNUSED_PARAMETER") canvas: Canvas) {
        // Chassis millwork already is the STATUS tube. Do not blit sit_crt (second bezel).
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
        if (isolated == IsolatedMode.CRT || isolated == IsolatedMode.DRAFT) {
            drawTerminalGlass(canvas, dst.width(), dst.height())
        } else {
            drawPreviewGlass(canvas, dst.width(), dst.height())
        }
        canvas.restore()
    }

    /** Chassis STATUS peek. Truncated. Clipped to visible glass. Same phosphor hue. */
    private fun drawPreviewGlass(canvas: Canvas, w: Float, h: Float) {
        lcdPaint.textSize = if (zoomed) sp(11f) else sp(13f)
        val pad = sp(10f)
        val innerW = (w - pad * 2).toInt().coerceAtLeast(8)
        val innerH = (h - pad * 2).coerceAtLeast(8f)
        val body = lcdBody()
        val layout = StaticLayout.Builder
            .obtain(body, 0, body.length, lcdPaint, innerW)
            .setAlignment(Layout.Alignment.ALIGN_NORMAL)
            .setIncludePad(false)
            .setMaxLines(((innerH / lcdPaint.textSize).toInt()).coerceAtLeast(1))
            .build()
        canvas.save()
        canvas.clipRect(pad, pad, w - pad, h - pad)
        canvas.translate(pad, pad)
        layout.draw(canvas)
        canvas.restore()
    }

    /** Isolated dest: caption + body in the glass. Keep glow, hue, glitch. Raster CRT is following. */
    private fun drawTerminalGlass(canvas: Canvas, w: Float, h: Float) {
        val scan = SitCRects.LcdAmber and 0x00FFFFFF or 0x22000000
        tearPaint.strokeWidth = 1f
        tearPaint.color = scan
        var y = 0f
        while (y < h) {
            canvas.drawLine(0f, y, w, y, tearPaint)
            y += 4f
        }
        val page = pages.getOrNull(pageIndex)
        val caption = page?.title.orEmpty().ifBlank { "STATUS" }
        val body = page?.body?.ifBlank { "(none)" } ?: "(none)"
        val pad = sp(22f)
        val innerW = (w - pad * 2).toInt().coerceAtLeast(8)
        lcdPaint.textSize = sp(16f)
        val capLayout = StaticLayout.Builder
            .obtain(caption, 0, caption.length, lcdPaint, innerW)
            .setAlignment(Layout.Alignment.ALIGN_NORMAL)
            .setIncludePad(false)
            .build()
        lcdPaint.textSize = sp(14f)
        val bodyLayout = StaticLayout.Builder
            .obtain(body, 0, body.length, lcdPaint, innerW)
            .setAlignment(Layout.Alignment.ALIGN_NORMAL)
            .setIncludePad(false)
            .build()
        canvas.save()
        canvas.clipRect(pad, pad, w - pad, h - pad)
        canvas.translate(pad, pad)
        capLayout.draw(canvas)
        canvas.translate(0f, capLayout.height + sp(12f))
        bodyLayout.draw(canvas)
        canvas.restore()
    }

    private fun lcdBody(): String {
        if (plate == SitPlate.RECEIPT && isolated == IsolatedMode.NONE) {
            return receiptStrip(receiptBody)
        }
        return idleLine
    }

    companion object {
        private const val PREVIEW_CHARS = 120

        fun clipPreview(raw: String, n: Int = PREVIEW_CHARS): String {
            val t = raw.replace('\n', ' ').trim()
            if (t.length <= n) return t
            return t.take(n - 1) + "…"
        }

        fun stripMd(raw: String): String =
            raw.replace("**", "").replace("#", "").replace('\n', ' ').trim()

        /** One said-line. Empty is empty. Not a leftover markdown dump. */
        fun receiptStrip(raw: String): String {
            val t = stripMd(raw)
            if (t.isBlank()) return "(empty receipt)"
            val said = Regex("You said:\\s*([^.]*)").find(t)?.groupValues?.get(1)?.trim().orEmpty()
            if (said.isNotBlank()) return "You said: $said"
            if (t.contains("I did it", ignoreCase = true) || t.contains("What happened", ignoreCase = true)) {
                return "I did it"
            }
            return clipPreview(t)
        }
    }

    private fun drawDecideNotYet(canvas: Canvas) {
        val saved = paperPaint.textSize
        paperPaint.textSize = sp(20f)
        paperPaint.isFakeBoldText = true
        drawPackText(canvas, SitCRects.decideNotYet, "Not yet", paperPaint, Layout.Alignment.ALIGN_CENTER)
        paperPaint.isFakeBoldText = false
        paperPaint.textSize = saved
    }

    private fun drawReceiptWell(canvas: Canvas) {
        canvas.drawRect(mapPack(SitCRects.receiptPaper), paperFill)
        drawPackText(canvas, SitCRects.receiptPaper, receiptStrip(receiptBody), graphitePaint)
    }

    private fun drawSendOverlay(canvas: Canvas) {
        // tap outside to dismiss. Send not Yes. OEM FILES strip is millwork.
        dimPaint.color = SitCRects.Dim
        canvas.drawRect(mapPack(PackRect(0, 0, SitCRects.PACK_W, SitCRects.PACK_H)), dimPaint)
        folderDestBmp?.let { canvas.drawBitmap(it, blit, bitmapPaint) }
        val listing = folderList.ifBlank { "(empty folder)" }
        drawPackText(canvas, SitCRects.folderList, listing, paperPaint)
    }

    private fun drawPackText(
        canvas: Canvas,
        pack: PackRect,
        body: String,
        paint: TextPaint = lcdPaint,
        align: Layout.Alignment = Layout.Alignment.ALIGN_NORMAL,
    ) {
        val dst = mapPack(pack)
        canvas.save()
        canvas.clipRect(dst)
        canvas.translate(dst.left, dst.top)
        val savedSize = paint.textSize
        if (paint.textSize < sp(12f) || paint === lcdPaint) {
            paint.textSize = sp(13f)
        }
        val pad = sp(10f)
        val innerW = (dst.width() - pad * 2).toInt().coerceAtLeast(8)
        val layout = StaticLayout.Builder
            .obtain(body, 0, body.length, paint, innerW)
            .setAlignment(align)
            .setIncludePad(false)
            .build()
        canvas.translate(pad, pad)
        layout.draw(canvas)
        canvas.restore()
        paint.textSize = savedSize
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

    private fun opaque(bmp: Bitmap?, x: Float, y: Float): Boolean {
        if (bmp == null) return false
        val ix = x.roundToInt()
        val iy = y.roundToInt()
        if (ix !in 0 until bmp.width || iy !in 0 until bmp.height) return false
        return Color.alpha(bmp.getPixel(ix, iy)) > SitCRects.ALPHA_HIT
    }

    private fun hitAt(x: Float, y: Float): SitHit {
        if (plate == SitPlate.SPLASH) return SitHit.None
        if (isolated == IsolatedMode.CRT) {
            val glass = SitCRects.glassIn(SitCRects.isolatedCrt)
            if (glass.contains(x, y)) {
                val w = glass.w.toFloat()
                val lx = x - glass.l
                return when {
                    lx < w * 0.18f -> SitHit.LcdPrev
                    lx > w * 0.82f -> SitHit.LcdNext
                    else -> SitHit.Lcd
                }
            }
            return SitHit.DismissZoom
        }
        if (isolated == IsolatedMode.DRAFT) {
            if (SitCRects.isolatedScreen.contains(x, y)) return SitHit.Lcd
            if (SitCRects.gate.contains(x, y) && (gateBmp == null || opaque(gateBmp, x, y))) {
                return SitHit.Gate
            }
            return SitHit.DismissZoom
        }
        if (sendOverlay) {
            if (SitCRects.folderOem.contains(x, y)) return SitHit.Files
            if (SitCRects.folderSend.contains(x, y)) return SitHit.Send
            if (SitCRects.sendPanel.contains(x, y)) return SitHit.None
            return SitHit.DismissZoom
        }
        if (zoomed) {
            val g = SitCRects.lcdFill
            if (g.contains(x, y)) {
                val w = g.w.toFloat()
                val lx = x - g.l
                return when {
                    lx < w * 0.18f -> SitHit.LcdPrev
                    lx > w * 0.82f -> SitHit.LcdNext
                    else -> SitHit.Lcd
                }
            }
            if (SitCRects.gate.contains(x, y) || opaque(gateBmp, x, y)) return SitHit.Gate
            if (SitCRects.title.contains(x, y)) return SitHit.DismissZoom
            return SitHit.DismissZoom
        }
        if (SitCRects.lcd.contains(x, y)) return SitHit.Lcd
        if (SitCRects.gate.contains(x, y) && (gateBmp == null || opaque(gateBmp, x, y))) return SitHit.Gate
        wellBmp()?.let { well ->
            if (opaque(well, x, y)) return wellHit(x, y)
        }
        if (SitCRects.banksDest.contains(x, y) && (banksBmp == null || opaque(banksBmp, x, y))) {
            bankHit(x, y)?.let { return it }
        }
        if (SitCRects.send.contains(x, y) && (lampSendBmp == null || opaque(lampSendBmp, x, y))) return SitHit.Send
        if (SitCRects.join.contains(x, y) && (lampJoinBmp == null || opaque(lampJoinBmp, x, y))) return SitHit.Join
        if (SitCRects.wake.contains(x, y) && (lampWakeBmp == null || opaque(lampWakeBmp, x, y))) return SitHit.Wake
        if (SitCRects.files.contains(x, y)) return SitHit.Files
        if (plate == SitPlate.BIND && SitCRects.bindPad.contains(x, y)) return SitHit.BindPaper
        return SitHit.None
    }

    private fun wellHit(x: Float, y: Float): SitHit = when (plate) {
        SitPlate.BIND -> SitHit.BindPaper
        SitPlate.PLAN -> when {
            labour ->
                if (SitCRects.didIt.contains(x, y)) SitHit.DidIt else SitHit.NotYetFeet
            SitCRects.fieldObjective.contains(x, y) -> SitHit.FieldObjective
            SitCRects.fieldNext.contains(x, y) -> SitHit.FieldNext
            SitCRects.fieldKeep.contains(x, y) -> SitHit.FieldKeep
            SitCRects.fieldReject.contains(x, y) -> SitHit.FieldReject
            SitCRects.fieldLimits.contains(x, y) -> SitHit.FieldLimits
            else -> SitHit.FieldObjective
        }
        SitPlate.DRAFT -> SitHit.Lcd
        SitPlate.DECIDE -> when {
            SitCRects.decideNotYet.contains(x, y) -> SitHit.DecideNotYet
            y < SitCRects.well.t + SitCRects.well.h * 0.38f -> SitHit.WhyStrip
            else -> SitHit.DecidePaper
        }
        SitPlate.NEXT ->
            if (SitCRects.didIt.contains(x, y)) SitHit.DidIt else SitHit.NotYetFeet
        else -> SitHit.None
    }

    private fun bankHit(x: Float, y: Float): SitHit? {
        if (x < SitCRects.banksDest.l || x >= SitCRects.banksDest.r) return null
        if (y < SitCRects.banksDest.t || y >= SitCRects.banksDest.b) return null
        return when {
            x < SitCRects.bankDraft.l -> SitHit.BankPlan
            x < SitCRects.bankDecide.l -> SitHit.BankDraft
            x < SitCRects.bankReceipt.l -> SitHit.BankDecide
            else -> SitHit.BankReceipt
        }
    }

    override fun onDetachedFromWindow() {
        animator?.cancel()
        super.onDetachedFromWindow()
    }
}
