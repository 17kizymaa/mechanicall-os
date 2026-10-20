/* Paper desk. Polls local book. Submit is a paper fill. Not Yes. */
const $ = (id) => document.getElementById(id);
let state = null;
let selected = "BOLT";
let side = "BUY";
let orderType = "MARKET";

function money(n) {
  const x = Number(n) || 0;
  return x.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function cls(n) {
  return n > 0 ? "up" : n < 0 ? "down" : "";
}

function rowOf(sym) {
  const w = state?.book?.watchlist || [];
  return w.find((r) => r.symbol === sym) || w[0];
}

function setApp(id) {
  document.body.dataset.app = id;
  document.querySelectorAll(".app").forEach((el) => el.classList.toggle("hidden", el.id !== "app-" + id));
  document.querySelectorAll(".dock-btn").forEach((el) => el.classList.toggle("on", el.dataset.app === id));
  $("strip").textContent =
    id === "trader" ? "Chat is a strip. The trader is the desk." : "Servant. Send is hello. Send is not Yes.";
}

async function api(path, body) {
  const opt = body
    ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }
    : {};
  const res = await fetch(path, opt);
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "refused");
  return data;
}

function render() {
  if (!state || !state.book) return;
  const b = state.book;
  $("disc").textContent = "Paper · simulated last · not live money";
  $("acct").innerHTML =
    `cash ${money(b.cash)} · equity ${money(b.equity)} · P&L <span class="${cls(b.day_pnl)}">${money(b.day_pnl)}</span>`;

  const watch = $("watch");
  watch.innerHTML = "<h2>Watch</h2>";
  b.watchlist.forEach((r) => {
    const div = document.createElement("div");
    div.className = "row" + (r.symbol === selected ? " on" : "");
    div.innerHTML = `<span>${r.symbol}</span><span class="${cls(r.change)}">${money(r.last)}</span><span class="${cls(r.change)}">${r.change >= 0 ? "+" : ""}${money(r.change)}</span>`;
    div.onclick = () => {
      selected = r.symbol;
      $("limit").value = r.last;
      render();
    };
    watch.appendChild(div);
  });
  const add = document.createElement("form");
  add.className = "add";
  add.innerHTML = `<input name="sym" maxlength="8" placeholder="ADD" /><button type="submit">+</button>`;
  add.onsubmit = async (e) => {
    e.preventDefault();
    const sym = add.sym.value.trim();
    if (!sym) return;
    state = await api("/api/watch", { symbol: sym });
    selected = sym.toUpperCase();
    render();
  };
  watch.appendChild(add);

  const r = rowOf(selected);
  if (r) {
    selected = r.symbol;
    $("sym").textContent = r.symbol;
    $("name").textContent = r.name || r.symbol;
    $("px").textContent = money(r.last);
    $("px").className = "px " + cls(r.change);
    $("chg").textContent = `${r.change >= 0 ? "+" : ""}${money(r.change)}  bid ${money(r.bid)}  ask ${money(r.ask)}`;
    $("chg").className = "chg " + cls(r.change);
    $("bid").textContent = "bid " + money(r.bid);
    $("ask").textContent = "ask " + money(r.ask);
  }

  $("tape").innerHTML = (b.fills || [])
    .slice(0, 14)
    .map(
      (f) =>
        `<div><span>${f.symbol}</span><span class="${f.side === "BUY" ? "up" : "down"}">${f.side}</span><span>${f.qty}</span><span>${money(f.price)}</span></div>`,
    )
    .join("") || "<div>no fills</div>";

  $("working").innerHTML = (b.orders || [])
    .filter((o) => o.status === "working")
    .map(
      (o) =>
        `<div><span>${o.symbol}</span><span>${o.side}</span><span>${o.qty} @ ${o.limit}</span><button type="button" class="x" data-id="${o.id}">x</button></div>`,
    )
    .join("") || "<div>none</div>";
  $("working").querySelectorAll(".x").forEach((btn) => {
    btn.onclick = async () => {
      state = await api("/api/cancel", { id: btn.dataset.id });
      render();
    };
  });

  const posHead =
    "<div class=\"pos dim\"><span>sym</span><span>qty</span><span>avg</span><span>last</span><span>uPnL</span><span></span></div>";
  const posRows = (b.positions || [])
    .map(
      (p) =>
        `<div class="pos"><span>${p.symbol}</span><span>${p.qty}</span><span>${money(p.avg)}</span><span>${money(p.last)}</span><span class="${cls(p.upnl)}">${money(p.upnl)}</span><button type="button" class="flat" data-sym="${p.symbol}">flat</button></div>`,
    )
    .join("");
  $("positions").innerHTML = posHead + (posRows || "<div>flat</div>");
  $("positions").querySelectorAll(".flat").forEach((btn) => {
    btn.onclick = async () => {
      state = await api("/api/flatten", { symbol: btn.dataset.sym });
      render();
    };
  });

  $("submit").classList.toggle("sell", side === "SELL");
  document.querySelector(".lim").classList.toggle("on", orderType === "LIMIT");

  const msgs = $("msgs");
  msgs.innerHTML = (state.serve?.messages || [])
    .map((m) => `<p class="msg ${m.from}">${escapeHtml(m.text)}</p>`)
    .join("");
  msgs.scrollTop = msgs.scrollHeight;
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

async function submitTicket() {
  const qty = Number($("qty").value);
  const limit = $("limit").value;
  $("ticket-note").textContent = "Working…";
  try {
    state = await api("/api/order", {
      symbol: selected,
      side,
      qty,
      type: orderType,
      limit: orderType === "LIMIT" ? Number(limit) : null,
    });
    $("ticket-note").textContent =
      state.book.orders[0]?.status === "filled" ? "Filled. Paper." : "Working. Paper.";
    render();
  } catch (err) {
    $("ticket-note").textContent = String(err.message || err);
  }
}

function bind() {
  document.querySelectorAll(".dock-btn").forEach((btn) => {
    btn.onclick = () => setApp(btn.dataset.app);
  });
  document.querySelectorAll(".side").forEach((btn) => {
    btn.onclick = () => {
      side = btn.dataset.side;
      document.querySelectorAll(".side").forEach((b) => b.classList.toggle("on", b === btn));
      render();
    };
  });
  document.querySelectorAll(".typ").forEach((btn) => {
    btn.onclick = () => {
      orderType = btn.dataset.type;
      document.querySelectorAll(".typ").forEach((b) => b.classList.toggle("on", b === btn));
      render();
    };
  });
  $("submit").onclick = submitTicket;
  $("serve-form").onsubmit = async (e) => {
    e.preventDefault();
    const text = $("serve-text").value.trim();
    if (!text) return;
    $("serve-text").value = "";
    state = await api("/api/serve", { text });
    render();
  };
}

async function loop() {
  try {
    state = await api("/api/state");
    render();
  } catch (_err) {
    /* quiet; next poll */
  }
  setTimeout(loop, 400);
}

bind();
setApp("trader");
loop();
