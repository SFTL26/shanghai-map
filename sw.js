// Офлайн-режим карты: страница, фото и шрифты — из кэша, тайлы Amap — из кэша «tiles».
// Тайлы скачивает кнопка «Скачать карту» в index.html; просмотренные онлайн тоже сохраняются.
const SHELL = "shell-v1", ASSETS = "assets-v1", TILES = "tiles", FONTS = "fonts-v1";
const CORE = ["./", "./manifest.webmanifest", "./icon-192.png", "./icon-512.png", "./icon-180.png"];

self.addEventListener("install", e => {
  self.skipWaiting();
  e.waitUntil(caches.open(SHELL).then(c => c.addAll(CORE)).catch(() => {}));
});
self.addEventListener("activate", e => {
  const keep = [SHELL, ASSETS, TILES, FONTS];
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => !keep.includes(k)).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

// все поддомены webrd01–04 сводим к одному ключу, чтобы тайл хранился один раз
const tileKey = u => u.replace(/^https:\/\/webrd0\d\./, "https://webrd01.");

async function cacheFirst(cacheName, key, init) {
  const c = await caches.open(cacheName);
  const hit = await c.match(key);
  if (hit) return hit;
  try {
    const r = await fetch(key, init);
    if (r.ok) c.put(key, r.clone());
    return r;
  } catch (err) {
    return new Response("", { status: 504, statusText: "offline" });
  }
}

// страница: при интернете — свежая (мимо HTTP-кэша, ждём до 3 с), иначе — сохранённая копия.
// Раньше было «сразу из кэша, свежая на следующий запуск»: обновления сайта на телефоне появлялись только со второго-третьего открытия.
const PAGE_WAIT = 3000;
async function page(req) {
  const c = await caches.open(SHELL);
  const hit = await c.match("./");
  const net = fetch(new URL("./", self.registration.scope).href, { cache: "no-store" })
    .then(r => { if (r.ok) { c.put("./", r.clone()); return r; } return null; }).catch(() => null);
  if (!hit) return (await net) || new Response("Нет интернета, а карта ещё не сохранена в телефон.", { status: 503, headers: { "Content-Type": "text/plain; charset=utf-8" } });
  const late = new Promise(res => setTimeout(() => res(null), PAGE_WAIT));
  return (await Promise.race([net, late])) || hit;
}

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const u = new URL(req.url);
  if (/^webrd0\d\.is\.autonavi\.com$/.test(u.hostname)) {
    e.respondWith(cacheFirst(TILES, tileKey(req.url), { mode: "cors" }));
  } else if (u.hostname === "fonts.googleapis.com" || u.hostname === "fonts.gstatic.com") {
    e.respondWith(cacheFirst(FONTS, req.url, { mode: "cors" }));
  } else if (u.origin === location.origin) {
    if (req.mode === "navigate" || /\/(index\.html)?$/.test(u.pathname)) e.respondWith(page(req));
    else e.respondWith(cacheFirst(ASSETS, u.origin + u.pathname));
  }
});
