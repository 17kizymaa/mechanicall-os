#!/usr/bin/env python3
"""Paper book: watchlist, last, ticket, positions, P&L.

Not live money. Not a brokerage. Not IBKR-named.
Filesystem JSON is the book. Never writes CURRENT.md.
"""
from __future__ import annotations

import json
import random
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DISCLAIMER = (
    "Hypothetical paper book. Simulated last. Not live money. "
    "Not a brokerage. Simulated results are not actual trading."
)

STARTING_CASH = 10_000.0
CURRENCY = "GBP"

SEED_WATCH = (
    ("AAA", "Atlas", 102.40),
    ("BOLT", "Bolt", 41.20),
    ("COVE", "Cove", 18.75),
    ("DRIFT", "Drift", 256.00),
    ("EMBER", "Ember", 73.10),
    ("FORGE", "Forge", 9.42),
    ("GALE", "Gale", 14.88),
    ("HEX", "Hex", 188.25),
)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _round(px: float) -> float:
    return round(float(px), 4)


def empty_book() -> dict[str, Any]:
    watch = []
    for sym, name, last in SEED_WATCH:
        last = _round(last)
        watch.append(
            {
                "symbol": sym,
                "name": name,
                "last": last,
                "open": last,
                "bid": _round(last * 0.9998),
                "ask": _round(last * 1.0002),
                "change": 0.0,
            }
        )
    return {
        "label": "paper",
        "not_live": True,
        "not_ibkr": True,
        "disclaimer": DISCLAIMER,
        "currency": CURRENCY,
        "starting_cash": STARTING_CASH,
        "cash": STARTING_CASH,
        "realized": 0.0,
        "watchlist": watch,
        "orders": [],
        "fills": [],
        "positions": [],
        "seq": 1,
        "updated": _now(),
    }


def load(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return empty_book()
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return empty_book()
    if not isinstance(obj, dict):
        return empty_book()
    base = empty_book()
    if obj.get("watchlist"):
        base["watchlist"] = obj["watchlist"]
    for key in ("cash", "realized", "starting_cash", "seq"):
        if key in obj:
            try:
                base[key] = float(obj[key]) if key != "seq" else int(obj[key])
            except (TypeError, ValueError):
                pass
    for key in ("orders", "fills", "positions"):
        if isinstance(obj.get(key), list):
            base[key] = obj[key]
    base["not_live"] = True
    base["not_ibkr"] = True
    base["disclaimer"] = DISCLAIMER
    base["label"] = "paper"
    return mark(base)


def save(path: Path, book: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    book = mark(book)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(book, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def _row(book: dict[str, Any], symbol: str) -> dict[str, Any] | None:
    sym = symbol.strip().upper()
    for row in book["watchlist"]:
        if str(row.get("symbol") or "").upper() == sym:
            return row
    return None


def last_of(book: dict[str, Any], symbol: str) -> float:
    row = _row(book, symbol)
    if row is None:
        raise ValueError(f"unknown symbol {symbol}")
    return float(row["last"])


def mark(book: dict[str, Any]) -> dict[str, Any]:
    """Mark-to-market equity and unrealized. Mutates and returns book."""
    by_last = {str(r["symbol"]).upper(): float(r["last"]) for r in book["watchlist"]}
    unreal = 0.0
    mkt = 0.0
    for pos in book["positions"]:
        qty = float(pos.get("qty") or 0)
        avg = float(pos.get("avg") or 0)
        sym = str(pos.get("symbol") or "").upper()
        last = by_last.get(sym, avg)
        pos["last"] = _round(last)
        pos["upnl"] = _round((last - avg) * qty)
        unreal += (last - avg) * qty
        mkt += last * qty
    book["unrealized"] = _round(unreal)
    book["equity"] = _round(float(book["cash"]) + mkt)
    book["day_pnl"] = _round(float(book.get("realized") or 0) + unreal)
    book["updated"] = _now()
    book["not_live"] = True
    book["not_ibkr"] = True
    return book


def _set_last(row: dict[str, Any], last: float) -> None:
    last = _round(max(0.05, last))
    row["last"] = last
    row["bid"] = _round(last * 0.9998)
    row["ask"] = _round(last * 1.0002)
    opn = float(row.get("open") or last)
    row["change"] = _round(last - opn)


def tick(book: dict[str, Any], rng: random.Random | None = None) -> dict[str, Any]:
    rng = rng or random.Random()
    for row in book["watchlist"]:
        shock = rng.gauss(0.0, 0.0028)
        _set_last(row, float(row["last"]) * (1.0 + shock))
    _match_limits(book)
    return mark(book)


def add_symbol(book: dict[str, Any], symbol: str, name: str = "", last: float | None = None) -> dict[str, Any]:
    sym = symbol.strip().upper()
    if not sym or len(sym) > 8 or not sym.isalnum():
        raise ValueError("symbol must be 1–8 letters/digits")
    if _row(book, sym) is not None:
        return mark(book)
    px = _round(last if last is not None else 100.0)
    book["watchlist"].append(
        {
            "symbol": sym,
            "name": (name or sym).strip()[:24],
            "last": px,
            "open": px,
            "bid": _round(px * 0.9998),
            "ask": _round(px * 1.0002),
            "change": 0.0,
        }
    )
    return mark(book)


def _pos(book: dict[str, Any], symbol: str) -> dict[str, Any] | None:
    sym = symbol.upper()
    for p in book["positions"]:
        if str(p.get("symbol") or "").upper() == sym:
            return p
    return None


def _apply_fill(book: dict[str, Any], symbol: str, side: str, qty: float, price: float, oid: str) -> None:
    qty = float(qty)
    price = _round(price)
    signed = qty if side == "BUY" else -qty
    cash_delta = -signed * price
    book["cash"] = _round(float(book["cash"]) + cash_delta)
    pos = _pos(book, symbol)
    if pos is None:
        book["positions"].append({"symbol": symbol.upper(), "qty": signed, "avg": price})
    else:
        old_qty = float(pos["qty"])
        old_avg = float(pos["avg"])
        new_qty = old_qty + signed
        if old_qty == 0 or (old_qty > 0) == (signed > 0):
            pos["avg"] = _round((old_qty * old_avg + signed * price) / new_qty) if new_qty else 0.0
            pos["qty"] = _round(new_qty)
        else:
            closed = min(abs(old_qty), qty)
            realized = (price - old_avg) * closed * (1 if old_qty > 0 else -1)
            book["realized"] = _round(float(book["realized"]) + realized)
            if abs(new_qty) < 1e-9:
                book["positions"] = [p for p in book["positions"] if p is not pos]
            else:
                pos["qty"] = _round(new_qty)
                if (old_qty > 0) != (new_qty > 0):
                    pos["avg"] = price
    fill = {
        "id": oid,
        "symbol": symbol.upper(),
        "side": side,
        "qty": _round(qty),
        "price": price,
        "at": _now(),
        "paper": True,
    }
    book["fills"].insert(0, fill)
    book["fills"] = book["fills"][:80]


def _match_limits(book: dict[str, Any]) -> None:
    for order in book["orders"]:
        if order.get("status") != "working":
            continue
        if order.get("type") != "LIMIT":
            continue
        row = _row(book, str(order["symbol"]))
        if row is None:
            continue
        last = float(row["last"])
        limit = float(order["limit"])
        side = order["side"]
        hit = (side == "BUY" and last <= limit) or (side == "SELL" and last >= limit)
        if not hit:
            continue
        try:
            _apply_fill(book, order["symbol"], side, float(order["qty"]), last, order["id"])
        except ValueError:
            order["status"] = "rejected"
            order["note"] = "insufficient"
            continue
        order["status"] = "filled"
        order["fill_price"] = last
        order["filled_at"] = _now()


def place(
    book: dict[str, Any],
    *,
    symbol: str,
    side: str,
    qty: float,
    order_type: str = "MARKET",
    limit: float | None = None,
) -> dict[str, Any]:
    if not book.get("not_live", True):
        raise ValueError("refused: live book")
    side = side.strip().upper()
    order_type = order_type.strip().upper()
    if side not in {"BUY", "SELL"}:
        raise ValueError("side must be BUY or SELL")
    if order_type not in {"MARKET", "LIMIT"}:
        raise ValueError("type must be MARKET or LIMIT")
    qty = float(qty)
    if qty <= 0 or qty > 1_000_000:
        raise ValueError("qty out of range")
    row = _row(book, symbol)
    if row is None:
        raise ValueError(f"unknown symbol {symbol}")
    sym = str(row["symbol"]).upper()
    oid = f"p{int(book.get('seq') or 1)}"
    book["seq"] = int(book.get("seq") or 1) + 1
    order = {
        "id": oid,
        "symbol": sym,
        "side": side,
        "qty": _round(qty),
        "type": order_type,
        "limit": _round(limit) if limit is not None and order_type == "LIMIT" else None,
        "status": "working",
        "at": _now(),
        "paper": True,
        "not_ibkr": True,
    }
    if order_type == "LIMIT" and (limit is None or float(limit) <= 0):
        raise ValueError("limit required")
    if order_type == "MARKET":
        px = float(row["ask"] if side == "BUY" else row["bid"])
        if side == "BUY" and px * qty > float(book["cash"]) + 1e-9:
            raise ValueError("insufficient cash")
        _apply_fill(book, sym, side, qty, px, oid)
        order["status"] = "filled"
        order["fill_price"] = px
        order["filled_at"] = _now()
    else:
        last = float(row["last"])
        limit_px = float(limit)
        immediate = (side == "BUY" and last <= limit_px) or (side == "SELL" and last >= limit_px)
        if immediate:
            if side == "BUY" and last * qty > float(book["cash"]) + 1e-9:
                raise ValueError("insufficient cash")
            _apply_fill(book, sym, side, qty, last, oid)
            order["status"] = "filled"
            order["fill_price"] = last
            order["filled_at"] = _now()
        elif side == "BUY" and limit_px * qty > float(book["cash"]) + 1e-9:
            raise ValueError("insufficient cash")
    book["orders"].insert(0, order)
    book["orders"] = book["orders"][:80]
    return mark(book)


def cancel(book: dict[str, Any], oid: str) -> dict[str, Any]:
    for order in book["orders"]:
        if order.get("id") == oid and order.get("status") == "working":
            order["status"] = "cancelled"
            order["cancelled_at"] = _now()
            break
    return mark(book)


def flatten(book: dict[str, Any], symbol: str) -> dict[str, Any]:
    pos = _pos(book, symbol)
    if pos is None:
        return mark(book)
    qty = float(pos["qty"])
    if abs(qty) < 1e-9:
        return mark(book)
    side = "SELL" if qty > 0 else "BUY"
    return place(book, symbol=symbol, side=side, qty=abs(qty), order_type="MARKET")


def snapshot(book: dict[str, Any]) -> dict[str, Any]:
    return deepcopy(mark(book))
