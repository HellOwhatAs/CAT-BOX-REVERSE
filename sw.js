const CACHE_NAME = 'catbox-reader-v1';
const ASSETS = [
    './',
    './index.html',
    './chapter.html',
    './style.css',
    './data.js',
    './icon.png' 
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(ASSETS);
        })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        // Network First strategy: try network, then fallback to cache
        fetch(event.request)
            .then((response) => {
                // Update cache with new response
                if (event.request.method === 'GET' && response.ok) {
                    const responseClone = response.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, responseClone);
                    });
                }
                return response;
            })
            .catch(() => {
                // If offline, try cache
                return caches.match(event.request);
            })
    );
});
