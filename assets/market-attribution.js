(() => {
  "use strict";

  const meta = document.querySelector('meta[name="market-attribution-endpoint"]');
  const endpoint = meta?.content?.trim();
  if (!endpoint || !/^https:\/\/[^/]+\/v1\/events$/.test(endpoint)) return;

  const lang = (document.documentElement.lang || "").slice(0, 2).toLowerCase();
  const market = document.body?.dataset?.market?.toLowerCase() || "";
  const supportedMarkets = new Set(["ru", "kz", "uz", "kg", "tj", "tm"]);
  const supportedLanguages = new Set(["ru", "kk", "uz", "ky", "tg", "tk"]);
  if (!supportedMarkets.has(market) || !supportedLanguages.has(lang)) return;

  const sessionKey = "yuchen_ru_cis_session";
  let sessionSeed = sessionStorage.getItem(sessionKey);
  if (!sessionSeed) {
    const bytes = crypto.getRandomValues(new Uint8Array(24));
    sessionSeed = Array.from(bytes, (value) => value.toString(16).padStart(2, "0")).join("");
    sessionStorage.setItem(sessionKey, sessionSeed);
  }

  const query = new URLSearchParams(location.search);
  const deviceClass = matchMedia("(max-width: 767px)").matches
    ? "mobile"
    : matchMedia("(max-width: 1100px)").matches
      ? "tablet"
      : "desktop";

  function destinationFor(link) {
    const explicit = link.dataset.attributionDestination;
    if (["telegram", "vk", "whatsapp", "inquiry"].includes(explicit)) return explicit;
    const href = link.href || "";
    if (/^https:\/\/t\.me\//i.test(href)) return "telegram";
    if (/^https:\/\/(?:vk\.com|m\.vk\.com)\//i.test(href)) return "vk";
    if (/^https:\/\/wa\.me\//i.test(href)) return "whatsapp";
    if (/\/contact\.html(?:[?#]|$)/i.test(href)) return "inquiry";
    return "";
  }

  function record(destination, link) {
    const payload = {
      session_seed: sessionSeed,
      market,
      language: lang,
      event_type: `${destination}_click`,
      page: location.pathname,
      destination,
      utm_source: query.get("utm_source") || "",
      utm_medium: query.get("utm_medium") || "",
      utm_campaign: query.get("utm_campaign") || "",
      utm_content: link.dataset.attributionContent || query.get("utm_content") || "",
      device_class: deviceClass,
    };
    fetch(endpoint, {
      method: "POST",
      mode: "cors",
      credentials: "omit",
      cache: "no-store",
      keepalive: true,
      headers: { "content-type": "application/json" },
      body: JSON.stringify(payload),
    }).catch(() => {});
  }

  document.addEventListener("click", (event) => {
    const link = event.target.closest("a[href]");
    if (!link) return;
    const destination = destinationFor(link);
    if (destination) record(destination, link);
  }, { capture: true });
})();
