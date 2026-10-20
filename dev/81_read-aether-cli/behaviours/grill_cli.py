#!/usr/bin/env python3
"""One v6 suggestion of what the aether CLI is. Retrieval is local Chroma.

Not a Yes. Does not write CURRENT.md. Does not call Onyx.
"""
from __future__ import annotations

import json
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/mnt/kingston-nixos-sync/opt/mechanicall-os")
RAG = Path.home() / "MODEL+RAG"
CHROMA = (
    RAG
    / "rag-archive-manager/artifacts/index/chroma-sampling-v1-nonclient"
)
COLLECTION = "project-sidecars-v1"
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "personal-llm-sft-v6:latest"
HOST = "http://127.0.0.1:11434"
QUERY = "aether CLI POSIX script CURRENT preflight approve verbs"
FORCE = (
    RAG / "personal-llm/CURRENT.md",
    RAG / "personal-llm/artifacts/MODEL-DEFINITION.md",
    RAG / "rag-archive-manager/artifacts/RAG-ROUTE-RESEARCH-20261016.md",
    RAG / "research/INTERESTING-RESEARCH/HARNESS-CONTRACT.md",
    RAG / "research/INTERESTING-RESEARCH/mechanicall-os-v0.2.handoff.md",
)
SYSTEM = (ROOT / "references/personal-llm-system.txt").read_text(encoding="utf-8")
OUT = ROOT / "dev/81_read-aether-cli/output/CLI-SUGGESTION.md"
RETRIEVAL = ROOT / "dev/81_read-aether-cli/output/RETRIEVAL.json"
K = 8


def ollama_json(path: str, payload: dict, timeout: float) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        HOST.rstrip("/") + path,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def embed(text: str) -> list[float]:
    data = ollama_json(
        "/api/embeddings",
        {"model": EMBED_MODEL, "prompt": text},
        timeout=90,
    )
    emb = data.get("embedding")
    if not isinstance(emb, list) or len(emb) < 8:
        raise SystemExit("embed failed")
    return emb


def read_force(path: Path, cap: int = 1400) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    kept = []
    for line in text.splitlines():
        low = line.lower()
        if any(w in low for w in ("password", "luks", "secret", "api_key", "encryption key")):
            continue
        kept.append(line)
    body = "\n".join(kept).strip()
    if len(body) > cap:
        body = body[:cap] + "\n…[truncated]\n"
    return body


def retrieve() -> list[dict]:
    import chromadb
    from chromadb.config import Settings

    client = chromadb.PersistentClient(
        path=str(CHROMA),
        settings=Settings(anonymized_telemetry=False),
    )
    col = client.get_collection(COLLECTION)
    res = col.query(
        query_embeddings=[embed(QUERY)],
        n_results=K,
        include=["documents", "metadatas", "distances"],
    )
    docs = (res.get("documents") or [[]])[0]
    metas = (res.get("metadatas") or [[]])[0]
    dists = (res.get("distances") or [[]])[0]
    hits = []
    for i, doc in enumerate(docs):
        meta = metas[i] if i < len(metas) else {}
        path = (meta or {}).get("path", "")
        if "/_seed/" in path or path.endswith("/examples/dev-task/CURRENT.md"):
            continue
        if path == "/home/anphuni/mechanicall-os/CURRENT.md":
            continue
        hits.append(
            {
                "path": path,
                "kind": (meta or {}).get("kind", ""),
                "chunk": (meta or {}).get("chunk", ""),
                "distance": dists[i] if i < len(dists) else None,
                "document": (doc or "")[:900],
            }
        )
    seen = {h["path"] for h in hits}
    for path in FORCE:
        if not path.is_file() or str(path) in seen:
            continue
        hits.append(
            {
                "path": str(path),
                "kind": "forced-tree",
                "chunk": 0,
                "distance": None,
                "document": read_force(path),
            }
        )
        seen.add(str(path))
    return hits


def live_verbs() -> str:
    out = subprocess.check_output(
        [str(ROOT / "aether"), "verbs"],
        cwd=str(ROOT),
        text=True,
    )
    return out.strip()


def main() -> None:
    hits = retrieve()
    paths = []
    for h in hits:
        p = h.get("path") or ""
        if p and p not in paths:
            paths.append(p)
    verbs = live_verbs()
    blocks = []
    for i, h in enumerate(hits, 1):
        doc = (h.get("document") or "")[:400]
        blocks.append(
            f"[{i}] {h.get('path')}\n{doc}"
        )
    evidence = "\n".join(blocks)
    prompt = f"""Evidence, not law. Collection {COLLECTION}.

{evidence}

Live facts: AETHER_VERSION 0.2. One POSIX script named aether.
Verbs now: {verbs}
Parked for a later prune, still installed: garden rival spark graph session seed.
CURRENT.md is authority. preflight allows only header Next.
apply is not a Yes. approve is the human Yes.
Models never approve, apply, next, or restore.
Bookmark copies bytes. A TTY Rename of the stem is not a Yes.
Weight stays outside the APK. versionCode 46. No Onyx. No APK build.

Write the suggestion of what the aether CLI is now.
Use these headings in order:
1. What the aether CLI is
2. What it is for
3. What it is not
4. Verbs now, and verbs parked
5. APK implication, names only
6. Holes that stay a human decision
Each section is two or three sentences. Propose only.
"""
    print(f"prompt_chars {len(prompt)}")
    text = ""
    raw: dict = {}
    for attempt in range(1, 3):
        raw = ollama_json(
            "/api/generate",
            {
                "model": CHAT_MODEL,
                "prompt": prompt,
                "stream": False,
                "system": SYSTEM,
                "options": {
                    "temperature": 0.3,
                    "num_predict": 1200,
                    "num_ctx": 8192,
                },
            },
            timeout=240,
        )
        text = (raw.get("response") or "").strip()
        if len(text) >= 700 and "What the aether CLI is" in text:
            raw["attempt"] = attempt
            break
        raw["attempt"] = attempt
    if not text:
        raise SystemExit("ollama returned empty suggestion")
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    RETRIEVAL.write_text(
        json.dumps(
            {
                "query": QUERY,
                "embed_model": EMBED_MODEL,
                "collection": COLLECTION,
                "store": str(CHROMA),
                "paths": paths,
                "hits": [
                    {k: h[k] for k in ("path", "kind", "chunk", "distance")}
                    for h in hits
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    path_lines = "\n".join(f"- `{p}`" for p in paths) or "- (no paths)"
    OUT.write_text(
        f"# CLI suggestion — not CURRENT, not a Yes\n\n"
        f"**Model:** `{CHAT_MODEL}`\n"
        f"**Host:** `{HOST}`\n"
        f"**When:** {ts}\n"
        f"**Embed:** `{EMBED_MODEL}`\n"
        f"**Store:** `{CHROMA}`\n"
        f"**Collection:** `{COLLECTION}`\n"
        f"**Prompt tokens / eval:** {raw.get('prompt_eval_count')} / {raw.get('eval_count')}\n"
        f"**Grill attempt:** {raw.get('attempt')}\n\n"
        f"This file is a suggestion. It does not write CURRENT.md. It is not a Yes. "
        f"It is not apply. The APK is not built.\n\n"
        f"## RAG paths read\n\n{path_lines}\n\n"
        f"## Model prose\n\n{text}\n",
        encoding="utf-8",
    )
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
    print(f"paths {len(paths)}")


if __name__ == "__main__":
    main()
