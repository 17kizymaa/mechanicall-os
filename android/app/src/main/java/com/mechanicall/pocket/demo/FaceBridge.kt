package com.mechanicall.pocket.demo

import com.chaquo.python.Python
import org.json.JSONArray
import org.json.JSONObject

val AUTHORITY_FIELDS = listOf(
    "Objective",
    "Phase",
    "Status",
    "Baseline",
    "Next",
    "Approval",
)

data class FaceState(
    val ok: Boolean = false,
    val refused: Boolean = false,
    val bound: Boolean = false,
    val path: String = "",
    val message: String = "This folder is bound.",
    val hasCurrent: Boolean = false,
    val objective: String = "",
    val next: String = "",
    val phase: String = "",
    val status: String = "",
    val approval: String = "",
    val baseline: String = "",
    val planText: String = "",
    val propose: String = "",
    val receipt: String = "",
    val said: String = "",
    val openIsYes: Boolean = false,
    val shortcuts: List<String> = emptyList(),
    val walk: String = "bind",
    val chatStage: String = "",
    val schema: Map<String, String> = emptyMap(),
    val schemaDraft: Map<String, String> = emptyMap(),
    val rawError: String = "",
)

data class ProjectShortcut(
    val name: String,
    val path: String = "",
    val kind: String = "",
)

data class ChatMessage(
    val role: String,
    val text: String,
    val stage: String = "",
)

data class DraftChatResult(
    val ok: Boolean = false,
    val reply: String = "",
    val propose: String = "",
    val stage: String = "",
    val history: List<ChatMessage> = emptyList(),
    val fields: Map<String, String> = emptyMap(),
    val schemaDraft: Map<String, String> = emptyMap(),
    val raw: String = "",
)

data class GateState(
    val state: String = "idle",
    val step: Int = 0,
    val steps: Int = 16,
    val desk: String = "",
    val queue: Int = 0,
)

data class DeskProbe(
    val ok: Boolean = false,
    val host: String = "",
    val state: String = "quiet",
)

data class HunkRow(
    val id: String,
    val live: String = "",
    val propose: String = "",
    val differs: Boolean = false,
)

data class JoinState(
    val status: String = "not-on-net",
    val kind: String = "",
    val fp: String = "",
    val desk: String = "",
    val note: String = "",
    val ok: Boolean = true,
)

data class WakeState(
    val ok: Boolean = false,
    val status: String = "sleeping",
    val note: String = "WAKE is not Yes.",
)

data class OfferState(
    val status: String = "none",
    val notify: Boolean = false,
    val kind: String = "",
    val note: String = "",
    val ok: Boolean = true,
)

object FaceBridge {
    fun pyCall(fn: String, vararg args: Any?): String {
        return try {
            val mod = Python.getInstance().getModule("aether_bridge")
            val result = mod.callAttr(fn, *args)
            result?.toString().orEmpty()
        } catch (e: Exception) {
            "ERROR: ${e.message}"
        }
    }

    fun isError(raw: String): Boolean = raw.startsWith("ERROR:")

    fun jsonObject(raw: String): JSONObject? {
        if (isError(raw)) return null
        val trimmed = raw.trim()
        if (!trimmed.startsWith("{")) return null
        return try {
            JSONObject(trimmed)
        } catch (_: Exception) {
            null
        }
    }

    fun jsonArray(raw: String, vararg keys: String): JSONArray {
        if (isError(raw)) return JSONArray()
        val trimmed = raw.trim()
        return try {
            when {
                trimmed.startsWith("[") -> JSONArray(trimmed)
                trimmed.startsWith("{") -> {
                    val o = JSONObject(trimmed)
                    val search = keys.toList() + listOf("items", "shortcuts", "history", "fields")
                    for (key in search) {
                        if (o.has(key) && o.get(key) is JSONArray) {
                            return o.getJSONArray(key)
                        }
                    }
                    JSONArray()
                }
                else -> JSONArray()
            }
        } catch (_: Exception) {
            JSONArray()
        }
    }

    fun asText(raw: String): String {
        if (isError(raw)) return raw
        val o = jsonObject(raw) ?: return raw
        return when {
            o.has("text") -> o.optString("text", raw)
            o.has("reply") -> o.optString("reply", raw)
            o.has("message") -> o.optString("message", raw)
            else -> raw
        }
    }

    fun bindFolder(path: String): FaceState {
        val raw = pyCall("bind_folder", path)
        return faceFromRaw(raw, path)
    }

    fun faceState(path: String): FaceState {
        val raw = pyCall("face_state", path)
        return faceFromRaw(raw, path)
    }

    private fun faceFromRaw(raw: String, path: String): FaceState {
        if (isError(raw)) {
            return FaceState(message = raw, rawError = raw, path = path)
        }
        val o = jsonObject(raw) ?: return FaceState(
            message = "Could not read this folder.",
            rawError = raw,
            path = path,
        )
        return FaceState(
            ok = o.optBoolean("ok", false),
            refused = o.optBoolean("refused", false),
            bound = o.optBoolean("bound", false),
            path = o.optString("path", path),
            message = o.optString("message", "This folder is bound."),
            hasCurrent = o.optBoolean("has_current", false),
            objective = o.optString("objective", ""),
            next = o.optString("next", ""),
            phase = o.optString("phase", ""),
            status = o.optString("status", ""),
            approval = o.optString("approval", ""),
            baseline = o.optString("baseline", ""),
            planText = o.optString("plan_text", ""),
            propose = o.optString("propose", ""),
            receipt = o.optString("receipt", ""),
            said = o.optString("said", ""),
            openIsYes = o.optBoolean("open_is_yes", false),
            shortcuts = namesFrom(o.opt("shortcuts")),
            walk = o.optString("walk", "bind"),
            chatStage = o.optString("chat_stage", ""),
            schema = parseFields(o.opt("schema")?.toString() ?: ""),
            schemaDraft = parseFields(o.opt("schema_draft")?.toString() ?: ""),
        )
    }

    fun schemaFields(path: String, fallback: FaceState = FaceState()): Map<String, String> {
        val parsed = parseFields(pyCall("schema_fields", path))
        return if (parsed.values.any { it.isNotBlank() }) parsed else fieldsFromFace(fallback)
    }

    fun readSchemaDraft(path: String, fallback: FaceState = FaceState()): Map<String, String> {
        val parsed = parseFields(pyCall("read_schema_draft", path))
        return if (parsed.values.any { it.isNotBlank() }) parsed else schemaFields(path, fallback)
    }

    fun writeSchemaDraft(path: String, fields: Map<String, String>): String {
        val payload = JSONObject()
        for (name in AUTHORITY_FIELDS) {
            payload.put(name, fields[name].orEmpty())
        }
        return pyCall("write_schema_draft", path, payload.toString())
    }

    fun projectShortcuts(path: String): List<ProjectShortcut> {
        val raw = pyCall("project_shortcuts", path)
        return parseShortcuts(raw)
    }

    fun mergedShortcuts(path: String, face: FaceState): List<ProjectShortcut> {
        val seen = linkedSetOf<String>()
        val out = mutableListOf<ProjectShortcut>()
        for (item in projectShortcuts(path)) {
            if (seen.add(item.name)) out.add(item)
        }
        for (name in face.shortcuts) {
            if (name.isNotBlank() && seen.add(name)) {
                out.add(ProjectShortcut(name = name))
            }
        }
        return out
    }

    fun chatHistory(path: String): List<ChatMessage> {
        return parseHistory(pyCall("chat_history", path))
    }

    fun clearChat(path: String): List<ChatMessage> {
        val raw = pyCall("clear_chat", path)
        if (isError(raw)) return emptyList()
        return parseHistory(raw)
    }

    fun eventsText(path: String): String {
        val raw = pyCall("events_text", path)
        val text = asText(raw)
        if (isError(raw) || text.isBlank() || text == "(no events)") return ""
        return text
    }

    fun gateState(path: String): GateState {
        val raw = pyCall("gate_state", path)
        val o = jsonObject(raw) ?: return GateState()
        return GateState(
            state = o.optString("state", "idle"),
            step = o.optInt("step", 0),
            steps = o.optInt("steps", 16),
            desk = o.optString("desk", ""),
            queue = o.optInt("queue", 0),
        )
    }

    fun deskProbe(path: String, host: String): DeskProbe {
        val raw = pyCall("desk_probe", path, host)
        val o = jsonObject(raw) ?: return DeskProbe()
        return DeskProbe(
            ok = o.optBoolean("ok", false),
            host = o.optString("host", ""),
            state = o.optString("state", "quiet"),
        )
    }

    fun draftChat(path: String, host: String, message: String, focus: String = ""): DraftChatResult {
        val raw = pyCall("draft_chat", path, host, message, focus)
        if (isError(raw)) {
            return DraftChatResult(ok = false, reply = raw, raw = raw)
        }
        val o = jsonObject(raw)
            ?: return DraftChatResult(ok = false, reply = raw, raw = raw)
        return DraftChatResult(
            ok = o.optBoolean("ok", true),
            reply = o.optString("reply", asText(raw)),
            propose = o.optString("propose", ""),
            stage = o.optString("stage", ""),
            history = parseHistoryFrom(o.opt("history")),
            fields = parseFields(o.opt("fields")?.toString() ?: ""),
            schemaDraft = parseFields(o.opt("schema_draft")?.toString() ?: ""),
            raw = raw,
        )
    }

    fun listHunks(path: String): List<HunkRow> {
        val raw = pyCall("list_hunks", path)
        val arr = jsonArray(raw)
        val src = if (arr.length() > 0) arr else {
            val o = jsonObject(raw)
            o?.optJSONArray("hunks") ?: JSONArray()
        }
        val list = if (src.length() == 0 && raw.trim().startsWith("[")) {
            try { JSONArray(raw.trim()) } catch (_: Exception) { JSONArray() }
        } else src
        val out = mutableListOf<HunkRow>()
        val use = if (list.length() > 0) list else arr
        for (i in 0 until use.length()) {
            val row = use.optJSONObject(i) ?: continue
            val id = row.optString("id", "")
            if (id.isBlank()) continue
            out.add(
                HunkRow(
                    id = id,
                    live = row.optString("live", ""),
                    propose = row.optString("propose", ""),
                    differs = row.optBoolean("differs", false),
                ),
            )
        }
        return out
    }

    fun applyHunk(path: String, heading: String, replacement: String): String =
        pyCall("apply_hunk", path, heading, replacement)

    fun rejectHunk(path: String, heading: String): String = pyCall("reject_hunk", path, heading)

    fun acceptHunk(path: String, heading: String): String = pyCall("accept_hunk", path, heading)

    fun joinStatus(path: String): JoinState {
        val raw = pyCall("join_status", path)
        val o = jsonObject(raw) ?: return JoinState(note = raw)
        return JoinState(
            status = o.optString("status", "not-on-net"),
            kind = o.optString("kind", ""),
            fp = o.optString("fp", ""),
            desk = o.optString("desk", ""),
            note = o.optString("note", ""),
            ok = o.optBoolean("ok", true),
        )
    }

    fun joinAccept(path: String, pasted: String): JoinState {
        val raw = pyCall("join_accept", path, pasted)
        if (isError(raw)) return JoinState(ok = false, note = raw)
        val o = jsonObject(raw) ?: return JoinState(ok = false, note = raw)
        return JoinState(
            status = o.optString("status", "invited"),
            kind = o.optString("kind", ""),
            fp = o.optString("fp", ""),
            desk = o.optString("desk", ""),
            note = o.optString("note", "JOIN is not Yes."),
            ok = o.optBoolean("ok", true),
        )
    }

    fun offerStatus(path: String): OfferState {
        val raw = pyCall("offer_status", path)
        val o = jsonObject(raw) ?: return OfferState(note = raw)
        return OfferState(
            status = o.optString("status", "none"),
            notify = o.optBoolean("notify", false),
            kind = o.optString("kind", ""),
            note = o.optString("note", ""),
            ok = o.optBoolean("ok", true),
        )
    }

    fun acceptOffer(path: String): OfferState {
        val raw = pyCall("accept_offer", path)
        if (isError(raw)) return OfferState(ok = false, note = raw)
        val o = jsonObject(raw) ?: return OfferState(ok = false, note = raw)
        return OfferState(
            status = "accepted",
            notify = false,
            note = o.optString("note", "Accepted. Not Yes."),
            ok = o.optBoolean("ok", true),
        )
    }

    fun declineOffer(path: String): OfferState {
        val raw = pyCall("decline_offer", path)
        if (isError(raw)) return OfferState(ok = false, note = raw)
        return OfferState(status = "declined", notify = false, note = "Declined. Not Yes.")
    }

    fun stageUpload(path: String): String = pyCall("stage_upload", path)

    fun wakeDesk(path: String, url: String = ""): WakeState {
        val raw = pyCall("wake_desk", path, url)
        if (isError(raw)) return WakeState(note = raw)
        val o = jsonObject(raw) ?: return WakeState(note = raw)
        return WakeState(
            ok = o.optBoolean("ok", false),
            status = o.optString("status", "sleeping"),
            note = o.optString("note", "WAKE is not Yes."),
        )
    }

    fun yes(path: String, reason: String): String = pyCall("yes", path, reason)

    fun notYet(path: String, reason: String): String = pyCall("not_yet", path, reason)

    fun planText(path: String): String = asText(pyCall("plan_text", path))

    fun receiptText(path: String): String {
        val raw = pyCall("receipt_text", path)
        val text = asText(raw)
        if (isError(raw) || text.isBlank() || text == "(no receipt yet)") return ""
        return text
    }

    fun shortcutBody(path: String, item: ProjectShortcut): String {
        val key = "${item.kind} ${item.name}".lowercase()
        val raw = when {
            "propose" in key -> pyCall("read_propose", path)
            "receipt" in key -> pyCall("receipt_text", path)
            "current" in key -> pyCall("plan_text", path)
            else -> {
                val named = pyCall("read_shortcut", path, item.name)
                if (isError(named) && item.path.isNotBlank()) {
                    pyCall("read_shortcut", path, item.path)
                } else {
                    named
                }
            }
        }
        val text = asText(raw)
        if (isError(raw) || text.isBlank()) {
            val where = item.path.ifBlank { item.name }
            return "This file is listed.\n\n$where"
        }
        return text
    }

    fun fieldsFromFaceOrEmpty(face: FaceState): Map<String, String> = fieldsFromFace(face)

    fun parseFields(raw: String): Map<String, String> {
        val map = linkedMapOf<String, String>()
        AUTHORITY_FIELDS.forEach { map[it] = "" }
        if (isError(raw)) return map
        val o = jsonObject(raw) ?: return map
        val src = if (o.opt("fields") is JSONObject) o.getJSONObject("fields") else o
        for (name in AUTHORITY_FIELDS) {
            when {
                src.has(name) -> map[name] = src.optString(name, "")
                src.has(name.lowercase()) -> map[name] = src.optString(name.lowercase(), "")
            }
        }
        return map
    }

    private fun fieldsFromFace(face: FaceState): Map<String, String> = linkedMapOf(
        "Objective" to face.objective,
        "Phase" to face.phase,
        "Status" to face.status,
        "Baseline" to face.baseline,
        "Next" to face.next,
        "Approval" to face.approval,
    )

    private fun namesFrom(value: Any?): List<String> {
        return when (value) {
            is JSONArray -> {
                val out = mutableListOf<String>()
                for (i in 0 until value.length()) {
                    when (val item = value.opt(i)) {
                        is JSONObject -> {
                            val name = item.optString("name", item.optString("path", ""))
                            if (name.isNotBlank()) out.add(name)
                        }
                        null, JSONObject.NULL -> Unit
                        else -> {
                            val name = item.toString()
                            if (name.isNotBlank()) out.add(name)
                        }
                    }
                }
                out
            }
            is String -> if (value.isNotBlank()) listOf(value) else emptyList()
            else -> emptyList()
        }
    }

    private fun parseShortcuts(raw: String): List<ProjectShortcut> {
        val arr = jsonArray(raw, "shortcuts", "items")
        val out = mutableListOf<ProjectShortcut>()
        for (i in 0 until arr.length()) {
            when (val item = arr.opt(i)) {
                is JSONObject -> {
                    val name = item.optString("name", item.optString("path", ""))
                    if (name.isNotBlank()) {
                        out.add(
                            ProjectShortcut(
                                name = name,
                                path = item.optString("path", ""),
                                kind = item.optString("kind", ""),
                            ),
                        )
                    }
                }
                null, JSONObject.NULL -> Unit
                else -> {
                    val name = item.toString()
                    if (name.isNotBlank()) out.add(ProjectShortcut(name = name))
                }
            }
        }
        return out
    }

    private fun parseHistory(raw: String): List<ChatMessage> {
        if (isError(raw)) return emptyList()
        val o = jsonObject(raw)
        if (o != null) return parseHistoryFrom(o.opt("history") ?: o.opt("items"))
        return parseHistoryFrom(jsonArray(raw, "history", "items"))
    }

    private fun parseHistoryFrom(value: Any?): List<ChatMessage> {
        val arr = value as? JSONArray ?: return emptyList()
        val out = mutableListOf<ChatMessage>()
        for (i in 0 until arr.length()) {
            when (val item = arr.opt(i)) {
                is JSONObject -> {
                    val role = item.optString("role", item.optString("host", "note"))
                    val text = when {
                        item.has("text") -> item.optString("text")
                        item.has("content") -> item.optString("content")
                        item.has("message") -> item.optString("message")
                        else -> item.toString()
                    }
                    if (text.isNotBlank()) {
                        out.add(
                            ChatMessage(
                                role = role,
                                text = text,
                                stage = item.optString("stage", ""),
                            ),
                        )
                    }
                }
                null, JSONObject.NULL -> Unit
                else -> {
                    val text = item.toString()
                    if (text.isNotBlank()) out.add(ChatMessage(role = "note", text = text))
                }
            }
        }
        return out
    }
}
