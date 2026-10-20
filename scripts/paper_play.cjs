#!/usr/bin/env node
/**
 * Paper mobile sit: logs readable, Reset works. Never BUY as a live order.
 * Never Yes. Never deploy.
 */
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const origin = process.argv[2] || "http://127.0.0.1:8788";
const out = process.argv[3];
if (!out) {
  console.error("usage: paper_play.cjs <origin> <out-dir>");
  process.exit(2);
}
fs.mkdirSync(out, { recursive: true });
const id = "e9b16791a12ac1ef521891b6eac3bf68";

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.SITE_PLAY_CHROMIUM || "/usr/bin/chromium",
    args: ["--no-sandbox", "--disable-gpu", "--hide-scrollbars"],
  });
  const page = await browser.newPage({
    viewport: { width: 390, height: 844 },
    colorScheme: "dark",
    isMobile: true,
    hasTouch: true,
  });
  await page.goto(`${origin}/you-decide/t/${id}`, {
    waitUntil: "networkidle",
    timeout: 30000,
  });
  await sleep(700);
  const paperBtn = page.locator("#dock-paper");
  if ((await paperBtn.count()) && (await paperBtn.isVisible())) {
    await paperBtn.click();
    await sleep(400);
  }
  const dump1 = await page.evaluate(() => {
    const panel = document.querySelector(".tv-panel");
    const fills = document.getElementById("trader-fills");
    const reset = document.getElementById("paper-reset");
    return {
      hasReset: Boolean(reset),
      resetLabel: reset ? reset.textContent : "",
      panelH: panel ? Math.round(panel.getBoundingClientRect().height) : 0,
      fillsH: fills ? Math.round(fills.getBoundingClientRect().height) : 0,
      fillN: fills ? fills.children.length : 0,
      fillText: fills ? fills.innerText.slice(0, 240) : "",
      posN: (document.getElementById("trader-pos") || {}).children
        ? document.getElementById("trader-pos").children.length
        : 0,
    };
  });
  await page.screenshot({
    path: path.join(out, "paper-mobile-logs.png"),
    fullPage: false,
  });
  await page.evaluate(() => {
    const el = document.getElementById("paper-reset");
    if (el) el.click();
  });
  await sleep(800);
  const dump2 = await page.evaluate(() => ({
    status: (document.getElementById("trader-status") || {}).textContent || "",
    fillN: document.getElementById("trader-fills").children.length,
    posText: document.getElementById("trader-pos").innerText,
    cash: (document.getElementById("trader-cash") || {}).textContent || "",
  }));
  await page.screenshot({
    path: path.join(out, "paper-mobile-reset.png"),
    fullPage: false,
  });
  await browser.close();
  const okReset =
    /reset/i.test(dump2.status) && /flat/i.test(dump2.posText);
  const okLogs = dump1.panelH >= 160 && dump1.hasReset;
  const report = { dump1, dump2, okLogs, okReset };
  fs.writeFileSync(path.join(out, "PAPER.json"), JSON.stringify(report, null, 2));
  console.log(
    okLogs ? "logs-ok" : "LOGS-FAIL",
    "panelH=" + dump1.panelH,
    dump1.fillN + " fills"
  );
  console.log(okReset ? "reset-ok" : "RESET-FAIL", dump2.status, dump2.posText);
  if (!okLogs || !okReset) process.exit(1);
  console.log("paper OK");
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
