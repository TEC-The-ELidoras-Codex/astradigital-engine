/**
 * Performance Optimizer for Astradigital Engine
 * Implements advanced caching, lazy loading, and optimization strategies
 */

class AstradigitalPerformanceOptimizer {
    constructor() {
        this.cachePrefix = 'astra_';
        this.cacheExpiry = 24 * 60 * 60 * 1000; // 24 hours in milliseconds
        this.intersectionObserver = null;
        this.loadedAssets = new Set();
        this.preloadQueue = [];
        this.performanceMetrics = {};
        
        this.init();
    }

    /**
     * Initialize performance optimizations
     */
    init() {
        console.log('🚀 Initializing Astradigital Performance Optimizer...');
        
        this.setupIntersectionObserver();
        this.enableLazyLoading();
        this.setupAssetPreloading();
        this.implementSmartCaching();
        this.optimizeAnimations();
        this.setupPerformanceMonitoring();
        
        console.log('✅ Performance Optimizer initialized');
    }

    /**
     * Setup Intersection Observer for lazy loading
     */
    setupIntersectionObserver() {
        if ('IntersectionObserver' in window) {
            this.intersectionObserver = new IntersectionObserver(
                (entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            this.loadAsset(entry.target);
                            this.intersectionObserver.unobserve(entry.target);
                        }
                    });
                },
                {
                    rootMargin: '50px 0px',
                    threshold: 0.1
                }
            );
        }
    }

    /**
     * Enable lazy loading for images and other assets
     */
    enableLazyLoading() {
        // Lazy load images
        const images = document.querySelectorAll('img[data-src], img[data-faction], img[data-character]');
        images.forEach(img => {
            if (!img.src || img.src.includes('placeholder')) {
                img.classList.add('lazy-load');
                if (this.intersectionObserver) {
                    this.intersectionObserver.observe(img);
                }
            }
        });

        // Lazy load background images
        const bgElements = document.querySelectorAll('[data-bg-src]');
        bgElements.forEach(el => {
            if (this.intersectionObserver) {
                this.intersectionObserver.observe(el);
            }
        });

        // Lazy load canvas elements
        const canvasElements = document.querySelectorAll('canvas[data-lazy]');
        canvasElements.forEach(canvas => {
            if (this.intersectionObserver) {
                this.intersectionObserver.observe(canvas);
            }
        });
    }

    /**
     * Load an asset when it becomes visible
     */
    loadAsset(element) {
        const startTime = performance.now();
        
        if (element.tagName === 'IMG') {
            this.loadImage(element);
        } else if (element.hasAttribute('data-bg-src')) {
            this.loadBackgroundImage(element);
        } else if (element.tagName === 'CANVAS') {
            this.loadCanvasAsset(element);
        }

        const loadTime = performance.now() - startTime;
        this.recordMetric('assetLoadTime', loadTime);
    }

    /**
     * Load image with error handling and fallback
     */
    loadImage(img) {
        const factionId = img.getAttribute('data-faction');
        const characterId = img.getAttribute('data-character');
        const dataSrc = img.getAttribute('data-src');

        if (factionId && !this.loadedAssets.has(`faction-${factionId}`)) {
            this.generateAndCacheFactionAsset(img, factionId);
        } else if (characterId && !this.loadedAssets.has(`character-${characterId}`)) {
            this.generateAndCacheCharacterAsset(img, characterId);
        } else if (dataSrc) {
            this.loadExternalImage(img, dataSrc);
        }
    }

    /**
     * Generate and cache faction asset
     */
    generateAndCacheFactionAsset(img, factionId) {
        const cacheKey = `${this.cachePrefix}faction_${factionId}`;
        const cached = this.getCachedAsset(cacheKey);

        if (cached) {
            img.src = cached;
            img.classList.add('cached-asset');
        } else if (window.AstradigitalAssetGenerator) {
            const generator = new AstradigitalAssetGenerator();
            const assetData = generator.generateFactionLogo(factionId);
            
            if (assetData) {
                img.src = assetData;
                img.classList.add('generated-asset');
                this.cacheAsset(cacheKey, assetData);
                this.loadedAssets.add(`faction-${factionId}`);
            }
        }

        this.addLoadingAnimation(img);
    }

    /**
     * Generate and cache character asset
     */
    generateAndCacheCharacterAsset(img, characterId) {
        const cacheKey = `${this.cachePrefix}character_${characterId}`;
        const cached = this.getCachedAsset(cacheKey);

        if (cached) {
            img.src = cached;
            img.classList.add('cached-asset');
        } else if (window.AstradigitalAssetGenerator) {
            const generator = new AstradigitalAssetGenerator();
            const assetData = generator.generateCharacterPortrait(characterId);
            
            if (assetData) {
                img.src = assetData;
                img.classList.add('generated-asset');
                this.cacheAsset(cacheKey, assetData);
                this.loadedAssets.add(`character-${characterId}`);
            }
        }

        this.addLoadingAnimation(img);
    }

    /**
     * Load external image with fallback
     */
    loadExternalImage(img, src) {
        img.onload = () => {
            img.classList.add('loaded');
            this.fadeInAsset(img);
        };
        
        img.onerror = () => {
            console.warn(`Failed to load image: ${src}`);
            this.handleImageError(img);
        };
        
        img.src = src;
    }

    /**
     * Handle image loading errors
     */
    handleImageError(img) {
        // Try to generate a procedural asset as fallback
        if (img.hasAttribute('data-faction') || img.hasAttribute('data-character')) {
            this.loadAsset(img);
        } else {
            // Set a default placeholder
            img.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjMGEwZTE3Ii8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZpbGw9IiM0ZGVlZWEiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiPkFzdHJhZGlnaXRhbDwvdGV4dD48L3N2Zz4=';
            img.classList.add('placeholder-asset');
        }
    }

    /**
     * Load background image
     */
    loadBackgroundImage(element) {
        const bgSrc = element.getAttribute('data-bg-src');
        const img = new Image();
        
        img.onload = () => {
            element.style.backgroundImage = `url(${bgSrc})`;
            element.classList.add('bg-loaded');
            this.fadeInAsset(element);
        };
        
        img.src = bgSrc;
    }

    /**
     * Load canvas asset
     */
    loadCanvasAsset(canvas) {
        const type = canvas.getAttribute('data-type');
        const id = canvas.getAttribute('data-id');

        if (type === 'territory-map' && window.renderTerritoryMap) {
            window.renderTerritoryMap(canvas, id);
        } else if (type === 'faction-emblem' && window.AstradigitalAssetGenerator) {
            const generator = new AstradigitalAssetGenerator();
            const ctx = canvas.getContext('2d');
            // Custom canvas rendering logic here
        }
    }

    /**
     * Setup asset preloading for critical resources
     */
    setupAssetPreloading() {
        // Preload critical assets
        const criticalAssets = [
            'faction-magmasox',
            'faction-kaznak',
            'faction-tec',
            'character-mostw',
            'character-airth'
        ];

        criticalAssets.forEach(assetId => {
            this.preloadQueue.push(assetId);
        });

        // Process preload queue gradually
        this.processPreloadQueue();
    }

    /**
     * Process preload queue with throttling
     */
    processPreloadQueue() {
        if (this.preloadQueue.length === 0) return;

        const batchSize = 2; // Process 2 assets at a time
        const currentBatch = this.preloadQueue.splice(0, batchSize);

        currentBatch.forEach(assetId => {
            this.preloadAsset(assetId);
        });

        // Process next batch after delay
        setTimeout(() => {
            this.processPreloadQueue();
        }, 100);
    }

    /**
     * Preload a specific asset
     */
    preloadAsset(assetId) {
        const [type, id] = assetId.split('-');
        const cacheKey = `${this.cachePrefix}${type}_${id}`;

        if (!this.getCachedAsset(cacheKey) && window.AstradigitalAssetGenerator) {
            const generator = new AstradigitalAssetGenerator();
            let assetData;

            if (type === 'faction') {
                assetData = generator.generateFactionLogo(id);
            } else if (type === 'character') {
                assetData = generator.generateCharacterPortrait(id);
            }

            if (assetData) {
                this.cacheAsset(cacheKey, assetData);
                console.log(`✅ Preloaded ${type} asset: ${id}`);
            }
        }
    }

    /**
     * Implement smart caching with expiration
     */
    implementSmartCaching() {
        // Clean expired cache entries on initialization
        this.cleanExpiredCache();

        // Set up periodic cache cleaning
        setInterval(() => {
            this.cleanExpiredCache();
        }, 60 * 60 * 1000); // Clean every hour
    }

    /**
     * Cache an asset with timestamp
     */
    cacheAsset(key, data) {
        try {
            const cacheEntry = {
                data: data,
                timestamp: Date.now(),
                expires: Date.now() + this.cacheExpiry
            };
            
            localStorage.setItem(key, JSON.stringify(cacheEntry));
        } catch (error) {
            console.warn('Failed to cache asset:', error);
            // Clear old cache if storage is full
            this.clearOldestCache();
        }
    }

    /**
     * Get cached asset if not expired
     */
    getCachedAsset(key) {
        try {
            const cached = localStorage.getItem(key);
            if (!cached) return null;

            const cacheEntry = JSON.parse(cached);
            if (Date.now() > cacheEntry.expires) {
                localStorage.removeItem(key);
                return null;
            }

            return cacheEntry.data;
        } catch (error) {
            console.warn('Failed to retrieve cached asset:', error);
            return null;
        }
    }

    /**
     * Clean expired cache entries
     */
    cleanExpiredCache() {
        const now = Date.now();
        const keysToRemove = [];

        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && key.startsWith(this.cachePrefix)) {
                try {
                    const cached = JSON.parse(localStorage.getItem(key));
                    if (cached.expires && now > cached.expires) {
                        keysToRemove.push(key);
                    }
                } catch (error) {
                    keysToRemove.push(key); // Remove corrupted entries
                }
            }
        }

        keysToRemove.forEach(key => {
            localStorage.removeItem(key);
        });

        if (keysToRemove.length > 0) {
            console.log(`🧹 Cleaned ${keysToRemove.length} expired cache entries`);
        }
    }

    /**
     * Clear oldest cache entries when storage is full
     */
    clearOldestCache() {
        const cacheEntries = [];

        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && key.startsWith(this.cachePrefix)) {
                try {
                    const cached = JSON.parse(localStorage.getItem(key));
                    cacheEntries.push({ key, timestamp: cached.timestamp });
                } catch (error) {
                    localStorage.removeItem(key);
                }
            }
        }

        // Sort by timestamp and remove oldest 25%
        cacheEntries.sort((a, b) => a.timestamp - b.timestamp);
        const toRemove = Math.ceil(cacheEntries.length * 0.25);

        for (let i = 0; i < toRemove; i++) {
            localStorage.removeItem(cacheEntries[i].key);
        }

        console.log(`🧹 Cleared ${toRemove} oldest cache entries`);
    }

    /**
     * Optimize animations for performance
     */
    optimizeAnimations() {
        // Reduce motion for users who prefer it
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            document.documentElement.style.setProperty('--animation-duration', '0.1s');
            document.documentElement.style.setProperty('--transition-duration', '0.1s');
        }

        // Pause animations when page is not visible
        document.addEventListener('visibilitychange', () => {
            const animatedElements = document.querySelectorAll('.animate, .floating-particle, .territory-highlight');
            
            if (document.hidden) {
                animatedElements.forEach(el => {
                    el.style.animationPlayState = 'paused';
                });
            } else {
                animatedElements.forEach(el => {
                    el.style.animationPlayState = 'running';
                });
            }
        });
    }

    /**
     * Setup performance monitoring
     */
    setupPerformanceMonitoring() {
        // Monitor Core Web Vitals
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                list.getEntries().forEach((entry) => {
                    this.recordMetric(entry.name, entry.value);
                });
            });

            observer.observe({ entryTypes: ['largest-contentful-paint', 'first-input', 'cumulative-layout-shift'] });
        }

        // Monitor asset loading performance
        window.addEventListener('load', () => {
            setTimeout(() => {
                this.analyzePerformance();
            }, 1000);
        });
    }

    /**
     * Record performance metric
     */
    recordMetric(name, value) {
        if (!this.performanceMetrics[name]) {
            this.performanceMetrics[name] = [];
        }
        
        this.performanceMetrics[name].push({
            value: value,
            timestamp: Date.now()
        });

        // Keep only last 100 entries per metric
        if (this.performanceMetrics[name].length > 100) {
            this.performanceMetrics[name] = this.performanceMetrics[name].slice(-100);
        }
    }

    /**
     * Analyze overall performance
     */
    analyzePerformance() {
        const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
        const domReady = performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart;
        
        console.log('📊 Astradigital Performance Analysis:');
        console.log(`  🚀 Page Load Time: ${loadTime}ms`);
        console.log(`  📄 DOM Ready: ${domReady}ms`);
        console.log(`  🖼️ Assets Generated: ${this.loadedAssets.size}`);
        console.log(`  💾 Cache Entries: ${this.getCacheSize()}`);

        // Log warnings for slow performance
        if (loadTime > 3000) {
            console.warn('⚠️ Page load time is slower than optimal (>3s)');
        }
        
        if (domReady > 1500) {
            console.warn('⚠️ DOM ready time is slower than optimal (>1.5s)');
        }
    }

    /**
     * Get current cache size
     */
    getCacheSize() {
        let count = 0;
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && key.startsWith(this.cachePrefix)) {
                count++;
            }
        }
        return count;
    }

    /**
     * Add loading animation to element
     */
    addLoadingAnimation(element) {
        element.style.opacity = '0';
        element.style.transform = 'scale(0.9)';
        element.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        
        // Fade in when loaded
        setTimeout(() => {
            this.fadeInAsset(element);
        }, 50);
    }

    /**
     * Fade in asset with smooth animation
     */
    fadeInAsset(element) {
        element.style.opacity = '1';
        element.style.transform = 'scale(1)';
        element.classList.add('loaded');
    }

    /**
     * Get performance summary
     */
    getPerformanceSummary() {
        return {
            metrics: this.performanceMetrics,
            cacheSize: this.getCacheSize(),
            loadedAssets: Array.from(this.loadedAssets),
            loadTime: performance.timing.loadEventEnd - performance.timing.navigationStart
        };
    }

    /**
     * Clear all performance cache
     */
    clearCache() {
        const keysToRemove = [];
        
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && key.startsWith(this.cachePrefix)) {
                keysToRemove.push(key);
            }
        }

        keysToRemove.forEach(key => {
            localStorage.removeItem(key);
        });

        console.log(`🧹 Cleared ${keysToRemove.length} cache entries`);
        return keysToRemove.length;
    }
}

// Export for use in other scripts
window.AstradigitalPerformanceOptimizer = AstradigitalPerformanceOptimizer;

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    window.astraPerformanceOptimizer = new AstradigitalPerformanceOptimizer();
});
