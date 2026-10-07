/* ONSPORTS.UZ service worker
   Faqat sahifa (navigation) so'rovlarini boshqaradi: avval internetdan (yangi versiya),
   internet bo'lmasa — oxirgi saqlangan sahifa. API, rasm, TV oqim (HLS) va boshqa
   so'rovlarga TEGMAYDI, shuning uchun ular avvalgidek ishlaydi. */
const CACHE = "onsports-shell-v1";
const SHELL = "/__shell";

self.addEventListener("install", () => self.skipWaiting());

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.mode !== "navigate" || req.method !== "GET") return;
  e.respondWith((async () => {
    try {
      const res = await fetch(req.url, { cache: "no-cache", credentials: "same-origin" });
      if (res && res.ok) {
        const c = await caches.open(CACHE);
        c.put(SHELL, res.clone());
      }
      return res;
    } catch (err) {
      const hit = await caches.match(SHELL);
      return hit || new Response("Internet yo'q. Ulanishni tekshirib, qayta urinib ko'ring.", {
        status: 503,
        headers: { "Content-Type": "text/plain; charset=utf-8" }
      });
    }
  })());
});
