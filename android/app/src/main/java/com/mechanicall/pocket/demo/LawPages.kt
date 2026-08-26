package com.mechanicall.pocket.demo

data class LawPage(val id: String, val title: String, val body: String)

object LawPages {
    val order = listOf("objective", "next", "keep", "reject", "limits", "receipt")

    fun of(plan: String, receipt: String): List<LawPage> {
        return listOf(
            LawPage("objective", "OBJECTIVE", field(plan, "Objective").ifBlank { section(plan, "Product") }),
            LawPage("next", "NEXT", field(plan, "Next")),
            LawPage("keep", "KEEP", section(plan, "Keep")),
            LawPage("reject", "REJECT", section(plan, "Reject")),
            LawPage("limits", "LIMITS", section(plan, "Limits")),
            LawPage("receipt", "RECEIPT", receipt.trim().ifBlank { "(empty receipt)" }),
        )
    }

    fun field(plan: String, name: String): String {
        val prefix = "**$name:**"
        val line = plan.lineSequence().firstOrNull { it.trimStart().startsWith(prefix) } ?: return ""
        return line.trimStart().removePrefix(prefix).trim()
    }

    fun section(plan: String, header: String): String {
        val lines = plan.lines()
        val start = lines.indexOfFirst { it.trim() == "## $header" }
        if (start < 0) return ""
        val buf = StringBuilder()
        for (i in start + 1 until lines.size) {
            if (lines[i].startsWith("## ")) break
            buf.appendLine(lines[i])
        }
        return buf.toString().trim()
    }
}
