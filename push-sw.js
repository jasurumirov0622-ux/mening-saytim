/* ONSPORTS.UZ: gol bildirishnomalari uchun alohida service worker (asosiy sw.js ga tegmaydi) */
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (e) => e.waitUntil(self.clients.claim()));
self.addEventListener("push", (e) => {
  let d = {}; try { d = e.data ? e.data.json() : {}; } catch (_) {}
  e.waitUntil(self.registration.showNotification(d.title || "ONSPORTS.UZ", {
    body: d.body || "", icon: "/favicon.png", badge: "/favicon.png",
    tag: d.tag || undefined, renotify: !!d.tag, data: { url: d.url || "/" }
  }));
});
self.addEventListener("notificationclick", (e) => {
  e.notification.close();
  const u = new URL((e.notification.data && e.notification.data.url) || "/", self.location.origin).href;
  e.waitUntil(self.clients.matchAll({ type: "window", includeUncontrolled: true }).then((l) => {
    for (const c of l) if (c.url.startsWith(self.location.origin) && "focus" in c) return c.focus().then(() => (c.navigate ? c.navigate(u) : null));
    return self.clients.openWindow(u);
  }));
});
