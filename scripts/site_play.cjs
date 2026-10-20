#!/usr/bin/env node
/**
 * Play a You Decide room in chromium. Stills + walk log.
 * Never Send. Never BUY. Never Yes. Never deploy.
 */
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const url = process.argv[2];
const out = process.argv[3];
if (!url || !out) {
  console.error("usage: site_play.mjs <url> <out-dir>");
  process.exit(2);
}
fs.mkdirSync(out, { recursive: true });

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.SITE_PLAY_CHROMIUM || "/usr/bin/chromium",
    args: ["--no-sandbox", "--disable-gpu", "--hide-scrollbars"],
  });
  const wh = String(process.env.SITE_PLAY_VIEWPORT || "1440x900").split("x");
  const page = await browser.newPage({
    viewport: { width: Number(wh[0]) || 1440, height: Number(wh[1]) || 900 },
    colorScheme: "dark",
    isMobile: Number(wh[0]) <= 520,
    hasTouch: Number(wh[0]) <= 520,
  });
  const log = [];

  async function shot(name) {
    const file = path.join(out, `${name}.png`);
    await page.screenshot({ path: file, fullPage: false });
    const entry = {
      name,
      url: page.url(),
      app: await page.getAttribute("body", "data-app"),
      title: await page.title(),
    };
    log.push(entry);
    console.log("shot", name, entry.app);
  }

  await page.goto(url, { waitUntil: "networkidle", timeout: 30000 });
  await page.waitForSelector(".desk-dock", { timeout: 15000 });
  await sleep(500);
  await shot("01-boot");

  const paperBtn = page.locator("#dock-paper");
  if ((await paperBtn.count()) && (await paperBtn.isVisible())) {
    await paperBtn.click();
    await sleep(400);
  }
  await shot("02-paper");

  const row = page.locator("#trader-watch tr").first();
  if (await row.count()) {
    await row.click();
    await sleep(250);
    await shot("03-paper-picked");
  }

  await page.locator("#dock-chat").click();
  await sleep(400);
  await shot("04-chat");

  const draft = page.locator("#draft");
  if (await draft.count()) {
    await draft.fill("site-play: typed, not sent");
    await sleep(200);
    await shot("05-chat-typed");
    await draft.fill("");
  }

  const dump = await page.evaluate(() => ({
    title: document.title,
    app: document.body.dataset.app,
    text: document.body.innerText.slice(0, 8000),
    dock: [...document.querySelectorAll(".dock-btn")].map((b) => ({
      id: b.id,
      label: b.textContent.trim(),
      on: b.classList.contains("on"),
      hidden: b.classList.contains("hidden"),
    })),
    paperHidden: document.getElementById("app-paper")?.classList.contains("hidden"),
    chatHidden: document.getElementById("app-chat")?.classList.contains("hidden"),
  }));
  fs.writeFileSync(path.join(out, "innerText.txt"), dump.text || "");
  fs.writeFileSync(
    path.join(out, "WALK.json"),
    JSON.stringify({ url, log, dump: { ...dump, text: undefined }, title: dump.title }, null, 2)
  );
  await browser.close();
  console.log("ok", out);
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
