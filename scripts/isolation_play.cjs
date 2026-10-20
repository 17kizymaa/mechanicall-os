#!/usr/bin/env node
/**
 * Isolation millwork walker. Never Send. Never BUY. Never Yes.
 */
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const origin = process.argv[2] || "http://127.0.0.1:8788";
const out = process.argv[3];
if (!out) {
  console.error("usage: isolation_play.cjs <origin> <out-dir>");
  process.exit(2);
}
fs.mkdirSync(out, { recursive: true });

const ROOMS = [
  {
    name: "birthday",
    id: "e9b16791a12ac1ef521891b6eac3bf68",
    expectPaper: true,
  },
  {
    name: "mum",
    id: "e745d275940fa06e191d9870ebbfa205",
    expectPaper: false,
  },
  {
    name: "merseyflush",
    id: "f4e969e647a841602dac2fd062bab3f8",
    expectPaper: false,
  },
  {
    name: "this-works",
    id: "2b48071dd97502c311b7c5d923df2874",
    expectPaper: false,
  },
];

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.SITE_PLAY_CHROMIUM || "/usr/bin/chromium",
    args: ["--no-sandbox", "--disable-gpu", "--hide-scrollbars"],
  });
  const log = [];
  for (const room of ROOMS) {
    const page = await browser.newPage({
      viewport: { width: 1440, height: 900 },
      colorScheme: "dark",
    });
    const url = `${origin}/you-decide/t/${room.id}`;
    await page.goto(url, { waitUntil: "networkidle", timeout: 30000 });
    await sleep(600);
    const dump = await page.evaluate(() => ({
      title: document.title,
      hasDock: Boolean(document.querySelector(".desk-dock")),
      hasTrader: Boolean(document.getElementById("trader")),
      dockPaperHidden: (() => {
        const el = document.getElementById("dock-paper");
        return !el || el.classList.contains("hidden") || el.offsetParent === null;
      })(),
      bodyApp: document.body.getAttribute("data-app"),
      bodyClass: document.body.className,
      hasComposer: Boolean(document.getElementById("composer")),
      sendLabel: (document.getElementById("send") || {}).textContent || "",
    }));
    const file = path.join(out, `${room.name}-boot.png`);
    await page.screenshot({ path: file, fullPage: false });
    let paperShot = null;
    let chatShot = null;
    if (room.expectPaper) {
      const paperBtn = page.locator("#dock-paper");
      if ((await paperBtn.count()) && (await paperBtn.isVisible())) {
        await paperBtn.click();
        await sleep(400);
      }
      paperShot = `${room.name}-paper.png`;
      await page.screenshot({
        path: path.join(out, paperShot),
        fullPage: false,
      });
      const chatBtn = page.locator("#dock-chat");
      if (await chatBtn.count()) {
        await chatBtn.click();
        await sleep(400);
      }
      chatShot = `${room.name}-chat.png`;
      await page.screenshot({
        path: path.join(out, chatShot),
        fullPage: false,
      });
    }
    const leak =
      !room.expectPaper && (dump.hasTrader || dump.hasDock);
    const missingPaper = room.expectPaper && !dump.hasTrader;
    log.push({
      room: room.name,
      url,
      expectPaper: room.expectPaper,
      leak,
      missingPaper,
      dump,
      stills: [path.basename(file), paperShot, chatShot].filter(Boolean),
    });
    console.log(
      room.name,
      leak ? "LEAK" : missingPaper ? "MISSING-PAPER" : "OK",
      dump.bodyClass,
      dump.hasTrader ? "trader" : "no-trader"
    );
    await page.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(out, "WALK.json"), JSON.stringify(log, null, 2));
  const bad = log.filter((x) => x.leak || x.missingPaper);
  if (bad.length) {
    console.error("isolation FAIL", bad.map((x) => x.room).join(","));
    process.exit(1);
  }
  console.log("isolation OK");
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
