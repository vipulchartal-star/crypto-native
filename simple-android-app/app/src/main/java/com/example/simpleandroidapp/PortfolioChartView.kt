package com.example.simpleandroidapp

import android.content.Context
import android.graphics.Canvas
import android.graphics.LinearGradient
import android.graphics.Paint
import android.graphics.Path
import android.graphics.RectF
import android.graphics.Shader
import android.util.AttributeSet
import android.view.View
import kotlin.math.max

class PortfolioChartView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null
) : View(context, attrs) {

    private var chartValues = listOf(42f, 38f, 51f, 49f, 68f, 74f, 70f, 86f, 92f)
    private val linePath = Path()
    private val fillPath = Path()
    private val innerRect = RectF()
    private var lineColor = 0xFF79FFE1.toInt()
    private var glowColor = 0x8079FFE1.toInt()
    private var fillTopColor = 0x4479FFE1
    private var fillBottomColor = 0x0079FFE1

    private val gridPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = 0x22FFFFFF
        strokeWidth = dp(1f)
        style = Paint.Style.STROKE
    }

    private val linePaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        strokeWidth = dp(3f)
        style = Paint.Style.STROKE
        strokeCap = Paint.Cap.ROUND
        strokeJoin = Paint.Join.ROUND
    }

    private val glowPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        strokeWidth = dp(10f)
        style = Paint.Style.STROKE
        strokeCap = Paint.Cap.ROUND
        strokeJoin = Paint.Join.ROUND
    }

    private val fillPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.FILL
    }

    private val pointPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = 0xFFFFFFFF.toInt()
        style = Paint.Style.FILL
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        linePaint.color = lineColor
        glowPaint.color = glowColor

        val left = paddingLeft + dp(4f)
        val top = paddingTop + dp(8f)
        val right = width - paddingRight - dp(4f)
        val bottom = height - paddingBottom - dp(10f)
        innerRect.set(left, top, right, bottom)

        drawGrid(canvas)
        buildPaths()

        fillPaint.shader = LinearGradient(
            0f,
            innerRect.top,
            0f,
            innerRect.bottom,
            fillTopColor,
            fillBottomColor,
            Shader.TileMode.CLAMP
        )

        canvas.drawPath(fillPath, fillPaint)
        canvas.drawPath(linePath, glowPaint)
        canvas.drawPath(linePath, linePaint)

        val end = getPoint(chartValues.lastIndex)
        canvas.drawCircle(end.first, end.second, dp(5f), pointPaint)
    }

    private fun drawGrid(canvas: Canvas) {
        val rows = 3
        for (i in 0..rows) {
            val y = innerRect.top + (innerRect.height() / rows) * i
            canvas.drawLine(innerRect.left, y, innerRect.right, y, gridPaint)
        }
    }

    private fun buildPaths() {
        linePath.reset()
        fillPath.reset()

        val first = getPoint(0)
        linePath.moveTo(first.first, first.second)

        for (i in 1 until chartValues.size) {
            val previous = getPoint(i - 1)
            val current = getPoint(i)
            val controlX = (previous.first + current.first) / 2f
            linePath.cubicTo(
                controlX,
                previous.second,
                controlX,
                current.second,
                current.first,
                current.second
            )
        }

        fillPath.addPath(linePath)
        fillPath.lineTo(innerRect.right, innerRect.bottom)
        fillPath.lineTo(innerRect.left, innerRect.bottom)
        fillPath.close()
    }

    private fun getPoint(index: Int): Pair<Float, Float> {
        val maxValue = chartValues.maxOrNull() ?: 1f
        val minValue = chartValues.minOrNull() ?: 0f
        val range = max(1f, maxValue - minValue)
        val xStep = innerRect.width() / (chartValues.size - 1).coerceAtLeast(1)
        val x = innerRect.left + xStep * index
        val normalized = (chartValues[index] - minValue) / range
        val y = innerRect.bottom - normalized * innerRect.height()
        return x to y
    }

    private fun dp(value: Float): Float = value * resources.displayMetrics.density

    fun setChartValues(values: List<Float>, isLong: Boolean) {
        chartValues = values
        if (isLong) {
            lineColor = 0xFF79FFE1.toInt()
            glowColor = 0x8079FFE1.toInt()
            fillTopColor = 0x4479FFE1
            fillBottomColor = 0x0079FFE1
        } else {
            lineColor = 0xFFFF6B8A.toInt()
            glowColor = 0x80FF6B8A.toInt()
            fillTopColor = 0x44FF6B8A
            fillBottomColor = 0x00FF6B8A
        }
        invalidate()
    }
}
