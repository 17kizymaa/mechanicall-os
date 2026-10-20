#!/usr/bin/env node
/**
 * Chat composer sit. Type four lines. Enter = newline, not Send.
 * Never submit. Never BUY. Never Yes.
 */
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const origin = process.argv[2] || "http://127.0.0.1:8788";
const out = process.argv[3];
if (!out) {
  console.error("usage: composer_play.cjs <origin> <out-dir>");
  process.exit(2);
}
fs.mkdirSync(out, { recursive: true });

const ROOMS = [
  { name: "mum", id: "e745d275940fa06e191d9870ebbfa205", chatHash: false },
  { name: "birthday-chat", id: "e9b16791a12ac1ef521891b6eac3bf68", chatHash: true },
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
      viewport: { width: 390, height: 844 },
      colorScheme: "dark",
      isMobile: true,
      hasTouch: true,
    });
    const url =
      `${origin}/you-decide/t/${room.id}` + (room.chatHash ? "#chat" : "");
    await page.goto(url, { waitUntil: "networkidle", timeout: 30000 });
    if (room.chatHash) {
      const chatBtn = page.locator("#dock-chat");
      if (await chatBtn.count()) {
        await chatBtn.click();
        await sleep(300);
      }
    }
    const draft = page.locator("#draft");
    await draft.click();
    await draft.fill("line one\nline two\nline three\nline four last");
    await sleep(200);
    const file = path.join(out, `${room.name}-composer.png`);
    await page.screenshot({ path: file, fullPage: false });
    const before = await page.evaluate(() => ({
      value: document.getElementById("draft").value,
      rows: document.getElementById("draft").rows,
      hint: document.getElementById("draft").enterKeyHint,
      h: Math.round(document.getElementById("draft").getBoundingClientRect().height),
      lh: getComputedStyle(document.getElementById("draft")).lineHeight,
    }));
    await draft.press("Enter");
    await sleep(200);
    const after = await page.evaluate(() => ({
      value: document.getElementById("draft").value,
      threadN: document.querySelectorAll("#thread li:not(.sys)").length,
    }));
    const enterSent = after.threadN > 0 && !after.value.includes("line four");
    const enterNewlined = after.value.includes("\n") && after.value.endsWith("\n");
    log.push({
      room: room.name,
      url,
      enterSent,
      enterNewlined,
      before,
      afterValueTail: after.value.slice(-40),
      still: path.basename(file),
    });
    console.log(
      room.name,
      enterSent ? "ENTER-SENT" : "enter-kept",
      "h=" + before.h,
      "hint=" + before.hint,
      "rows=" + before.rows
    );
    await page.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(out, "COMPOSER.json"), JSON.stringify(log, null, 2));
  const bad = log.filter((x) => x.enterSent);
  if (bad.length) {
    console.error("composer FAIL", bad.map((x) => x.room).join(","));
    process.exit(1);
  }
  console.log("composer OK");
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
