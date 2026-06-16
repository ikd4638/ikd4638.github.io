// sw.js - Service Worker for Indu Kalpa Dihingia PWA

const CACHE_NAME = 'ikd-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/research.html',
  '/publications.html',
  '/teaching.html',
  '/talks.html',
  '/group.html',
  '/news.html',
  '/cv.html',
  '/contact.html',
  '/join.html',
  '/css/style.css',
  '/js/main.js',
  '/js/publications.js',
  '/images/DP.png',
  '/images/icon-192.png',
  '/images/icon-512.png'
];

// Install event - cache essential files
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

// Fetch event - serve cached content when offline
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cache => {
          if (cache !== CACHE_NAME) {
            return caches.delete(cache);
          }
        })
      );
    })
  );
});
