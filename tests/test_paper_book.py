#!/usr/bin/env python3
"""Paper book: ticket bites, P&L moves, CURRENT untouched."""
from __future__ import annotations

import random
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from paper_book import (  # noqa: E402
    add_symbol,
    cancel,
    empty_book,
    flatten,
    last_of,
    load,
    place,
    save,
    tick,
)


class TestPaperBook(unittest.TestCase):
    def setUp(self) -> None:
        self.book = empty_book()
        self.current = ROOT / "CURRENT.md"
        self.before = self.current.read_text(encoding="utf-8") if self.current.is_file() else ""

    def tearDown(self) -> None:
        if self.current.is_file():
            self.assertEqual(self.current.read_text(encoding="utf-8"), self.before)

    def test_seed_is_paper_not_ibkr(self) -> None:
        self.assertTrue(self.book["not_live"])
        self.assertTrue(self.book["not_ibkr"])
        self.assertEqual(self.book["cash"], 10_000)
        self.assertGreaterEqual(len(self.book["watchlist"]), 6)
        disc = str(self.book["disclaimer"]).lower()
        self.assertNotIn("interactive brokers", disc)
        self.assertIn("not live", disc)

    def test_market_buy_fills_and_moves_position(self) -> None:
        last = last_of(self.book, "BOLT")
        place(self.book, symbol="BOLT", side="BUY", qty=10, order_type="MARKET")
        self.assertEqual(self.book["positions"][0]["symbol"], "BOLT")
        self.assertEqual(self.book["positions"][0]["qty"], 10)
        self.assertLess(self.book["cash"], 10_000)
        self.assertEqual(self.book["fills"][0]["side"], "BUY")
        self.assertGreaterEqual(self.book["fills"][0]["price"], last * 0.99)
        self.assertEqual(self.book["orders"][0]["status"], "filled")

    def test_pnl_moves_when_last_moves(self) -> None:
        place(self.book, symbol="BOLT", side="BUY", qty=20, order_type="MARKET")
        before = self.book["unrealized"]
        rng = random.Random(1)
        for _ in range(40):
            tick(self.book, rng=rng)
        self.assertNotEqual(self.book["unrealized"], before)
        self.assertAlmostEqual(
            self.book["equity"],
            self.book["cash"] + last_of(self.book, "BOLT") * 20,
            places=2,
        )

    def test_limit_rests_then_fills(self) -> None:
        last = last_of(self.book, "COVE")
        place(
            self.book,
            symbol="COVE",
            side="BUY",
            qty=5,
            order_type="LIMIT",
            limit=round(last * 0.5, 4),
        )
        self.assertEqual(self.book["orders"][0]["status"], "working")
        self.assertEqual(self.book["positions"], [])
        self.book["watchlist"][2]["last"] = round(last * 0.4, 4)
        from paper_book import _match_limits, mark

        _match_limits(self.book)
        mark(self.book)
        self.assertEqual(self.book["orders"][0]["status"], "filled")
        self.assertEqual(self.book["positions"][0]["qty"], 5)

    def test_flatten_exits(self) -> None:
        place(self.book, symbol="AAA", side="BUY", qty=8, order_type="MARKET")
        flatten(self.book, "AAA")
        self.assertEqual(self.book["positions"], [])
        self.assertEqual(self.book["orders"][0]["side"], "SELL")

    def test_cancel_working(self) -> None:
        last = last_of(self.book, "HEX")
        place(
            self.book,
            symbol="HEX",
            side="BUY",
            qty=1,
            order_type="LIMIT",
            limit=round(last * 0.1, 4),
        )
        oid = self.book["orders"][0]["id"]
        cancel(self.book, oid)
        self.assertEqual(self.book["orders"][0]["status"], "cancelled")

    def test_insufficient_cash(self) -> None:
        with self.assertRaises(ValueError):
            place(self.book, symbol="DRIFT", side="BUY", qty=1_000_000, order_type="MARKET")

    def test_atomic_save_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "paper-book.json"
            place(self.book, symbol="GALE", side="BUY", qty=3, order_type="MARKET")
            save(path, self.book)
            again = load(path)
            self.assertEqual(again["positions"][0]["qty"], 3)
            self.assertTrue(again["not_live"])

    def test_add_symbol(self) -> None:
        add_symbol(self.book, "ZINC", name="Zinc", last=12.5)
        self.assertEqual(last_of(self.book, "ZINC"), 12.5)


if __name__ == "__main__":
    unittest.main()
