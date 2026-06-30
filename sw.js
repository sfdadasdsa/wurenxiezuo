const CACHE = "wuren-v1";
const URLS = ["index.html","m1.html","m2.html","m3.html","m4.html","m5.html","samoyed.mp4","manifest.json","icon.svg"];
self.addEventListener("install",function(e){e.waitUntil(caches.open(CACHE).then(function(c){return c.addAll(URLS)}));self.skipWaiting()});
self.addEventListener("activate",function(e){e.waitUntil(clients.claim())});
self.addEventListener("fetch",function(e){e.respondWith(caches.match(e.request).then(function(r){return r||fetch(e.request)}))});
