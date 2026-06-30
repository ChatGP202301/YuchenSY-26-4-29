import { readdirSync, statSync, writeFileSync } from "node:fs";
import { join, relative } from "node:path";

const [, , portArg, baseUrl, siteRoot, device, outFile] = process.argv;
const port = Number(portArg);
const viewportMap = {
  mobile: { width: 390, height: 1000, deviceScaleFactor: 1, mobile: true },
  ipad: { width: 820, height: 1180, deviceScaleFactor: 1, mobile: true },
  pc: { width: 1440, height: 1000, deviceScaleFactor: 1, mobile: false },
};
const viewport = viewportMap[device];
if (!viewport) throw new Error(`Unknown device ${device}`);

function walk(dir, acc = []) {
  for (const name of readdirSync(dir)) {
    const fullPath = join(dir, name);
    const rel = relative(siteRoot, fullPath);
    if (/^(assets|scripts|scraped_data|screenshots|verify_fix)(\/|$)/.test(rel)) continue;
    const st = statSync(fullPath);
    if (st.isDirectory()) walk(fullPath, acc);
    else if (name.endsWith(".html")) acc.push(rel);
  }
  return acc.sort();
}

function urlFor(rel) {
  const cleanPath = rel.split("/").map(encodeURIComponent).join("/");
  return `${baseUrl}/${cleanPath}?qa=${Date.now()}`;
}

async function newTarget(url) {
  const response = await fetch(`http://127.0.0.1:${port}/json/new?${encodeURIComponent(url)}`, {
    method: "PUT",
  });
  return await response.json();
}

const target = await newTarget("about:blank");
const ws = new WebSocket(target.webSocketDebuggerUrl);
let id = 0;
let loadSeen = false;
let currentPage = "";
const pending = new Map();
const networkErrors = [];
const exceptions = [];

function send(method, params = {}) {
  return new Promise((resolve, reject) => {
    const current = ++id;
    pending.set(current, { resolve, reject });
    ws.send(JSON.stringify({ id: current, method, params }));
  });
}

ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);
  if (msg.id && pending.has(msg.id)) {
    const req = pending.get(msg.id);
    pending.delete(msg.id);
    if (msg.error) req.reject(new Error(msg.error.message));
    else req.resolve(msg.result);
  }
  if (msg.method === "Page.loadEventFired") loadSeen = true;
  if (msg.method === "Network.responseReceived") {
    const status = msg.params.response.status;
    if (status >= 400) {
      networkErrors.push({
        page: currentPage,
        status,
        url: msg.params.response.url,
      });
    }
  }
  if (msg.method === "Runtime.exceptionThrown") {
    exceptions.push({
      page: currentPage,
      text: msg.params.exceptionDetails?.text || "Runtime exception",
    });
  }
};

await new Promise((resolve) => {
  ws.onopen = resolve;
});

await send("Page.enable");
await send("Runtime.enable");
await send("Network.enable");
await send("Network.setCacheDisabled", { cacheDisabled: true });
await send("Emulation.setDeviceMetricsOverride", viewport);
if (viewport.mobile) {
  await send("Emulation.setUserAgentOverride", {
    userAgent:
      "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
  });
}

const files = walk(siteRoot);
const layoutIssues = [];
const startedAll = Date.now();

for (let index = 0; index < files.length; index += 1) {
  const rel = files[index];
  currentPage = rel;
  loadSeen = false;
  await send("Page.navigate", { url: urlFor(rel) });
  const started = Date.now();
  while (!loadSeen && Date.now() - started < 3500) {
    await new Promise((resolve) => setTimeout(resolve, 25));
  }
  await new Promise((resolve) => setTimeout(resolve, 35));

  const result = await send("Runtime.evaluate", {
    returnByValue: true,
    expression: `(() => {
      const vw = window.innerWidth;
      const scrollWidth = Math.max(
        document.documentElement ? document.documentElement.scrollWidth : 0,
        document.body ? document.body.scrollWidth : 0
      );
      const brokenImages = Array.from(document.images)
        .filter((img) => img.complete && img.naturalWidth === 0)
        .map((img) => img.getAttribute("src"))
        .slice(0, 8);
      const offenders = Array.from(document.body ? document.body.querySelectorAll("*") : [])
        .map((el) => {
          const r = el.getBoundingClientRect();
          return { el, r };
        })
        .filter(({ el, r }) => {
          if (r.width < 2 || r.height < 2) return false;
          const cs = getComputedStyle(el);
          if (cs.display === "none" || cs.visibility === "hidden") return false;
          if (cs.position === "fixed" && r.width <= vw) return false;
          if (!(r.left < -3 || r.right > vw + 3)) return false;
          let parent = el.parentElement;
          while (parent && parent !== document.body) {
            const pcs = getComputedStyle(parent);
            if (["auto", "scroll", "hidden", "clip"].includes(pcs.overflowX)) {
              return false;
            }
            parent = parent.parentElement;
          }
          return true;
        })
        .slice(0, 8)
        .map(({ el, r }) => ({
          tag: el.tagName.toLowerCase(),
          cls: el.className ? String(el.className).slice(0, 80) : "",
          text: (el.innerText || "").replace(/\\s+/g, " ").trim().slice(0, 80),
          left: Math.round(r.left),
          right: Math.round(r.right),
          width: Math.round(r.width)
        }));
      return {
        vw,
        scrollWidth,
        overflow: Math.round(scrollWidth - vw),
        brokenImages,
        offenders
      };
    })()`,
  });
  const value = result.result?.value || {};
  if ((value.overflow || 0) > 3 || (value.brokenImages || []).length || (value.offenders || []).length) {
    layoutIssues.push({ page: rel, ...value });
  }

  if ((index + 1) % 250 === 0) {
    console.log(`${device}: audited ${index + 1}/${files.length}`);
  }
}

const output = {
  device,
  viewport,
  pages: files.length,
  seconds: Math.round((Date.now() - startedAll) / 1000),
  layoutIssues,
  networkErrors,
  exceptions,
};
writeFileSync(outFile, JSON.stringify(output, null, 2));
console.log(`${device}: pages=${files.length} layoutIssues=${layoutIssues.length} networkErrors=${networkErrors.length} exceptions=${exceptions.length}`);
ws.close();
