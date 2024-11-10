const CACHE_NAME = 'workout-tracker-v2';
const urlsToCache = [
    '/',
    '/static/manifest.json',
    'https://cdn.jsdelivr.net/npm/chart.js',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css'
];

// Clear old caches on activation
self.addEventListener('activate', function(event) {
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.map(function(cacheName) {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('fetch', function(event) {
    // Don't cache API requests or form submissions
    if (event.request.method !== 'GET') {
        return event.respondWith(fetch(event.request));
    }

    event.respondWith(
        fetch(event.request).catch(function() {
            return caches.match(event.request);
        })
    );
});