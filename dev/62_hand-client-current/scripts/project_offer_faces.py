#!/usr/bin/env python3
"""Project alias CURRENT.md onto anphuni.com public/offers/ (face, not law).

No zip. Site is the face. Files stay authority.
Usage:
  python3 project_offer_faces.py <src-clients-dir> <anphuni-public-dir>
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

ALIASES = (
    ("happy-birthday", "Paper trading", "room to try, no live money"),
    ("hi-its-mother", "Open invitation", "to collaborate"),
    ("this-works", "Kitchen “this works”", "the plate, not the person"),
)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="{title} — a product CURRENT. This page is not Yes." />
  <title>{title} — anphuni</title>
  <link rel="stylesheet" href="/assets/style.css" />
  <link rel="stylesheet" href="/assets/offer-face.css" />
</head>
<body>
  <header>
    <a class="brand" href="/">anphuni</a>
    <nav>
      <a href="/">Home</a>
      <a href="/you-decide">You Decide</a>
      <a href="/offers">Offers</a>
      <a href="/protocol">Protocol</a>
      <a href="/privacy">Privacy</a>
    </nav>
  </header>
  <main>
    <p class="tag">Product · not Yes</p>
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
    <p class="notice">
      This page <em>projects</em> a file. The file is law.
      Opening it is not Yes. A zip is not the product.
      <a href="/offers/{alias}/HOW-TO-ACCEPT.md">How to Yes</a>
      (still not this page).
    </p>
    <p class="meta" id="face-status">Loading CURRENT.md…</p>
    <pre class="current-face" id="current"></pre>
  </main>
  <footer>Filesystem is truth · this page is a face, not a second CURRENT</footer>
  <script src="/assets/offer-face.js" defer></script>
</body>
</html>
"""

INDEX = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="Three product CURRENTs. The site is the face. The files are law. Not Yes." />
  <title>Offers — anphuni</title>
  <link rel="stylesheet" href="/assets/style.css" />
</head>
<body>
  <header>
    <a class="brand" href="/">anphuni</a>
    <nav>
      <a href="/">Home</a>
      <a href="/you-decide">You Decide</a>
      <a href="/offers" aria-current="page">Offers</a>
      <a href="/protocol">Protocol</a>
      <a href="/privacy">Privacy</a>
    </nav>
  </header>
  <main>
    <p class="tag">Face · not zip</p>
    <h1>Three products</h1>
    <p class="lead">
      Each link is a CURRENT.md you can read. Edit Keep on your copy.
      This site is the face. The file is law. Opening is not Yes.
    </p>
    <div class="cards">
      <a class="card" href="/offers/happy-birthday" style="display:block;text-decoration:none">
        <div class="tag">happy-birthday</div>
        <h3>Paper trading</h3>
        <p>Room to try. No live money.</p>
      </a>
      <a class="card" href="/offers/hi-its-mother" style="display:block;text-decoration:none">
        <div class="tag">hi-its-mother</div>
        <h3>Open invitation</h3>
        <p>To collaborate. Door open.</p>
      </a>
      <a class="card" href="/offers/this-works" style="display:block;text-decoration:none">
        <div class="tag">this-works</div>
        <h3>Kitchen “this works”</h3>
        <p>The plate, not the person.</p>
      </a>
    </div>
  </main>
  <footer>No zip · web is not Yes · CORE_PRINCIPLES: interfaces project files</footer>
</body>
</html>
"""


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: project_offer_faces.py <src-clients-dir> <anphuni-public-dir>", file=sys.stderr)
        return 2
    src = Path(sys.argv[1]).resolve()
    public = Path(sys.argv[2]).resolve()
    offers = public / "offers"
    offers.mkdir(parents=True, exist_ok=True)
    (public / "offers.html").write_text(INDEX, encoding="utf-8")
    for alias, title, lead in ALIASES:
        pack = src / alias
        current = pack / "CURRENT.md"
        how = pack / "HOW-TO-ACCEPT.md"
        if not current.is_file():
            print(f"missing {current}", file=sys.stderr)
            return 1
        dest = offers / alias
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copy2(current, dest / "CURRENT.md")
        if how.is_file():
            shutil.copy2(how, dest / "HOW-TO-ACCEPT.md")
        (offers / f"{alias}.html").write_text(
            HTML.format(alias=alias, title=title, lead=lead),
            encoding="utf-8",
        )
        print(f"{alias}\t{dest / 'CURRENT.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
