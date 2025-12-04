// Caches all static assets and basic webpages to be accessed offline, does not cache dynamic elements like updated notes, only displays notes present at caching time.
// This means no offline functionality as all fetch requests will fail and no data will be saved.
// Can be fixed adding a queue for offline actions and background sync API (allows tasks to be defered to service worker until connection is stable) to reconcile when the PWA comes back online
// Does not check for login when accessing cached since cache only stores plain html no template functionality

const assets = [
  "/",
  "/dashboard.html",
  "/addnote.html",
  "/menu.hmtl",
  "/layout.hmtl",
  "/login.html",
  "/add.html",
  "static/css/style.css",
  "static/js/app.js",
  "static/icons/logo.png",
  "static/icons/menu.png",
];

const CATALOGUE_ASSETS = "catalogue-assets";

self.addEventListener("install", (installEvt) => {
  installEvt.waitUntil(
    caches
      .open(CATALOGUE_ASSETS)
      .then((cache) => {
        console.log(cache);
        cache.addAll(assets);
      })
      .then(self.skipWaiting())
      .catch((e) => {
        console.log(e);
      })
  );
});

self.addEventListener("activate", function (evt) {
  evt.waitUntil(
    caches
      .keys()
      .then((keyList) => {
        return Promise.all(
          keyList.map((key) => {
            if (key === CATALOGUE_ASSETS) {
              console.log("Removed old cache from", key);
              return caches.delete(key);
            }
          })
        );
      })
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", function (evt) {
  evt.respondWith(
    fetch(evt.request).catch(() => {
      return caches.open(CATALOGUE_ASSETS).then((cache) => {
        return cache.match(evt.request);
      });
    })
  );
});
