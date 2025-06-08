/**
 * Advanced SEO Optimizer for Astradigital Engine
 * Generates automated SEO metadata, schema markup, and social media optimization
 */

class AstradigitalSEOOptimizer {
    constructor() {
        this.siteData = {
            name: 'The Astradigital Ocean',
            description: 'An immersive digital ocean experience featuring interactive factions, territories, and characters in a cyberpunk universe.',
            url: window.location.origin,
            twitter: '@astradigital',
            facebook: 'astradigital',
            logo: '/assets/images/astradigital-logo.png'
        };
        
        this.currentPageData = {};
        this.schemas = [];
        
        this.init();
    }

    /**
     * Initialize SEO optimization
     */
    init() {
        console.log('🔍 Initializing SEO Optimizer...');
        
        this.detectPageType();
        this.generateBasicMetadata();
        this.generateOpenGraphMetadata();
        this.generateTwitterMetadata();
        this.generateSchemaMarkup();
        this.optimizeImages();
        this.setupDynamicUpdates();
        
        console.log('✅ SEO Optimizer initialized');
    }

    /**
     * Detect current page type and extract relevant data
     */
    detectPageType() {
        const path = window.location.pathname;
        const title = document.title;
        
        // Detect page type based on URL and content
        if (path.includes('/faction/') || document.querySelector('.faction-details')) {
            this.currentPageData.type = 'faction';
            this.extractFactionData();
        } else if (path.includes('/character/') || document.querySelector('.character-details')) {
            this.currentPageData.type = 'character';
            this.extractCharacterData();
        } else if (path.includes('/territory/') || document.querySelector('.territory-details')) {
            this.currentPageData.type = 'territory';
            this.extractTerritoryData();
        } else if (path.includes('/map') || document.querySelector('.astra-ocean-visual')) {
            this.currentPageData.type = 'map';
            this.extractMapData();
        } else {
            this.currentPageData.type = 'home';
            this.extractHomeData();
        }

        console.log(`📄 Detected page type: ${this.currentPageData.type}`);
    }

    /**
     * Extract faction-specific data for SEO
     */
    extractFactionData() {
        const factionElement = document.querySelector('.faction-details, .faction-card');
        if (!factionElement) return;

        const name = factionElement.querySelector('h1, h2, .faction-name')?.textContent?.trim() || 'Unknown Faction';
        const description = factionElement.querySelector('.faction-description, .description')?.textContent?.trim() || '';
        const image = factionElement.querySelector('img')?.src || '';
        const color = factionElement.getAttribute('data-color') || '#4deeea';

        this.currentPageData = {
            ...this.currentPageData,
            title: `${name} - Astradigital Faction`,
            description: description || `Explore the ${name} faction in the Astradigital Ocean. Discover their territories, characters, and influence in this digital universe.`,
            image: image,
            color: color,
            name: name,
            factionData: {
                name: name,
                description: description,
                territories: this.extractFactionTerritories(factionElement),
                characters: this.extractFactionCharacters(factionElement),
                influence: factionElement.getAttribute('data-influence') || 'medium'
            }
        };
    }

    /**
     * Extract character-specific data for SEO
     */
    extractCharacterData() {
        const characterElement = document.querySelector('.character-details, .character-card');
        if (!characterElement) return;

        const name = characterElement.querySelector('h1, h2, .character-name')?.textContent?.trim() || 'Unknown Character';
        const description = characterElement.querySelector('.character-description, .description, .bio')?.textContent?.trim() || '';
        const image = characterElement.querySelector('img')?.src || '';
        const faction = characterElement.querySelector('.faction-name')?.textContent?.trim() || '';

        this.currentPageData = {
            ...this.currentPageData,
            title: `${name} - Astradigital Character`,
            description: description || `Meet ${name}, a key character in the Astradigital Ocean${faction ? ` from the ${faction} faction` : ''}. Discover their story and role in this digital universe.`,
            image: image,
            name: name,
            characterData: {
                name: name,
                description: description,
                faction: faction,
                role: characterElement.getAttribute('data-role') || 'member',
                features: characterElement.getAttribute('data-features')?.split(',') || []
            }
        };
    }

    /**
     * Extract territory-specific data for SEO
     */
    extractTerritoryData() {
        const territoryElement = document.querySelector('.territory-details, .territory-card');
        if (!territoryElement) return;

        const name = territoryElement.querySelector('h1, h2, .territory-name')?.textContent?.trim() || 'Unknown Territory';
        const description = territoryElement.querySelector('.territory-description, .description')?.textContent?.trim() || '';
        const controllingFaction = territoryElement.querySelector('.controlling-faction')?.textContent?.trim() || '';

        this.currentPageData = {
            ...this.currentPageData,
            title: `${name} - Astradigital Territory`,
            description: description || `Explore ${name}, a territory in the Astradigital Ocean${controllingFaction ? ` controlled by ${controllingFaction}` : ''}. Discover its strategic importance and connections.`,
            name: name,
            territoryData: {
                name: name,
                description: description,
                controllingFaction: controllingFaction,
                type: territoryElement.getAttribute('data-type') || 'neutral',
                coordinates: territoryElement.getAttribute('data-coordinates') || ''
            }
        };
    }

    /**
     * Extract map-specific data for SEO
     */
    extractMapData() {
        this.currentPageData = {
            ...this.currentPageData,
            title: 'Interactive Map - Astradigital Ocean',
            description: 'Explore the interactive map of the Astradigital Ocean. Navigate between faction territories, discover characters, and uncover the connections in this digital universe.',
            keywords: ['interactive map', 'astradigital ocean', 'faction territories', 'digital universe', 'cyberpunk'],
            mapData: {
                territories: document.querySelectorAll('.territory').length,
                factions: document.querySelectorAll('.faction').length,
                isInteractive: true
            }
        };
    }

    /**
     * Extract home page data for SEO
     */
    extractHomeData() {
        const factionCount = document.querySelectorAll('.faction-card').length;
        const characterCount = document.querySelectorAll('.character-card').length;

        this.currentPageData = {
            ...this.currentPageData,
            title: 'Astradigital Ocean - Interactive Digital Universe',
            description: `Dive into the Astradigital Ocean, an immersive digital universe featuring ${factionCount} factions and ${characterCount} characters. Explore territories, uncover stories, and navigate the complex relationships in this cyberpunk world.`,
            keywords: ['astradigital ocean', 'digital universe', 'cyberpunk', 'interactive fiction', 'factions', 'territories'],
            homeData: {
                factionCount: factionCount,
                characterCount: characterCount,
                hasMap: !!document.querySelector('.astra-ocean-visual'),
                features: ['Interactive Map', 'Faction System', 'Character Profiles', 'Territory Control']
            }
        };
    }

    /**
     * Generate basic SEO metadata
     */
    generateBasicMetadata() {
        // Title
        this.updateMetaTag('title', this.currentPageData.title);
        document.title = this.currentPageData.title;

        // Description
        this.updateMetaTag('meta[name="description"]', this.currentPageData.description);

        // Keywords
        if (this.currentPageData.keywords) {
            this.updateMetaTag('meta[name="keywords"]', this.currentPageData.keywords.join(', '));
        }

        // Canonical URL
        this.updateLinkTag('link[rel="canonical"]', window.location.href);

        // Robots
        this.updateMetaTag('meta[name="robots"]', 'index, follow, max-image-preview:large');

        // Author
        this.updateMetaTag('meta[name="author"]', 'The Elidoras Codex');

        // Viewport (if not already set)
        if (!document.querySelector('meta[name="viewport"]')) {
            this.createMetaTag('name', 'viewport', 'width=device-width, initial-scale=1.0');
        }

        // Theme color
        this.updateMetaTag('meta[name="theme-color"]', this.currentPageData.color || '#4deeea');
    }

    /**
     * Generate Open Graph metadata
     */
    generateOpenGraphMetadata() {
        const ogData = {
            'og:title': this.currentPageData.title,
            'og:description': this.currentPageData.description,
            'og:type': this.getOGType(),
            'og:url': window.location.href,
            'og:site_name': this.siteData.name,
            'og:locale': 'en_US'
        };

        // Add image if available
        if (this.currentPageData.image) {
            ogData['og:image'] = this.currentPageData.image;
            ogData['og:image:alt'] = this.currentPageData.title;
            ogData['og:image:width'] = '1200';
            ogData['og:image:height'] = '630';
        }

        // Add type-specific data
        if (this.currentPageData.type === 'faction') {
            ogData['article:section'] = 'Factions';
            ogData['article:tag'] = this.currentPageData.factionData?.name;
        } else if (this.currentPageData.type === 'character') {
            ogData['profile:first_name'] = this.currentPageData.characterData?.name?.split(' ')[0] || '';
            ogData['profile:last_name'] = this.currentPageData.characterData?.name?.split(' ').slice(1).join(' ') || '';
        }

        // Apply Open Graph tags
        Object.entries(ogData).forEach(([property, content]) => {
            this.updateMetaTag(`meta[property="${property}"]`, content, 'property');
        });
    }

    /**
     * Generate Twitter metadata
     */
    generateTwitterMetadata() {
        const twitterData = {
            'twitter:card': 'summary_large_image',
            'twitter:site': this.siteData.twitter,
            'twitter:title': this.currentPageData.title,
            'twitter:description': this.currentPageData.description
        };

        if (this.currentPageData.image) {
            twitterData['twitter:image'] = this.currentPageData.image;
            twitterData['twitter:image:alt'] = this.currentPageData.title;
        }

        // Apply Twitter tags
        Object.entries(twitterData).forEach(([name, content]) => {
            this.updateMetaTag(`meta[name="${name}"]`, content);
        });
    }

    /**
     * Generate Schema.org markup
     */
    generateSchemaMarkup() {
        this.schemas = [];

        // Base organization schema
        this.schemas.push(this.createOrganizationSchema());

        // Base website schema
        this.schemas.push(this.createWebsiteSchema());

        // Page-specific schemas
        switch (this.currentPageData.type) {
            case 'faction':
                this.schemas.push(this.createFactionSchema());
                break;
            case 'character':
                this.schemas.push(this.createCharacterSchema());
                break;
            case 'territory':
                this.schemas.push(this.createTerritorySchema());
                break;
            case 'map':
                this.schemas.push(this.createMapSchema());
                break;
            case 'home':
                this.schemas.push(this.createHomePageSchema());
                break;
        }

        // Apply schemas to page
        this.applySchemas();
    }

    /**
     * Create organization schema
     */
    createOrganizationSchema() {
        return {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": this.siteData.name,
            "description": this.siteData.description,
            "url": this.siteData.url,
            "logo": this.siteData.url + this.siteData.logo,
            "sameAs": [
                `https://twitter.com/${this.siteData.twitter.replace('@', '')}`,
                `https://facebook.com/${this.siteData.facebook}`
            ]
        };
    }

    /**
     * Create website schema
     */
    createWebsiteSchema() {
        return {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": this.siteData.name,
            "description": this.siteData.description,
            "url": this.siteData.url,
            "publisher": {
                "@type": "Organization",
                "name": this.siteData.name,
                "url": this.siteData.url
            },
            "potentialAction": {
                "@type": "SearchAction",
                "target": `${this.siteData.url}/search?q={search_term_string}`,
                "query-input": "required name=search_term_string"
            }
        };
    }

    /**
     * Create faction-specific schema
     */
    createFactionSchema() {
        if (!this.currentPageData.factionData) return null;

        return {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": this.currentPageData.factionData.name,
            "description": this.currentPageData.factionData.description,
            "url": window.location.href,
            "memberOf": {
                "@type": "Organization",
                "name": "Astradigital Ocean Factions"
            },
            "subOrganization": this.currentPageData.factionData.territories?.map(territory => ({
                "@type": "Place",
                "name": territory
            })) || []
        };
    }

    /**
     * Create character-specific schema
     */
    createCharacterSchema() {
        if (!this.currentPageData.characterData) return null;

        return {
            "@context": "https://schema.org",
            "@type": "Person",
            "name": this.currentPageData.characterData.name,
            "description": this.currentPageData.characterData.description,
            "url": window.location.href,
            "memberOf": this.currentPageData.characterData.faction ? {
                "@type": "Organization",
                "name": this.currentPageData.characterData.faction
            } : undefined,
            "jobTitle": this.currentPageData.characterData.role,
            "image": this.currentPageData.image
        };
    }

    /**
     * Create territory-specific schema
     */
    createTerritorySchema() {
        if (!this.currentPageData.territoryData) return null;

        return {
            "@context": "https://schema.org",
            "@type": "Place",
            "name": this.currentPageData.territoryData.name,
            "description": this.currentPageData.territoryData.description,
            "url": window.location.href,
            "containedInPlace": {
                "@type": "Place",
                "name": "Astradigital Ocean"
            },
            "geo": this.currentPageData.territoryData.coordinates ? {
                "@type": "GeoCoordinates",
                "latitude": this.currentPageData.territoryData.coordinates.split(',')[0],
                "longitude": this.currentPageData.territoryData.coordinates.split(',')[1]
            } : undefined
        };
    }

    /**
     * Create map schema
     */
    createMapSchema() {
        return {
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": "Astradigital Ocean Interactive Map",
            "description": "Interactive map showing faction territories and character locations",
            "url": window.location.href,
            "applicationCategory": "Entertainment",
            "operatingSystem": "Web Browser",
            "browserRequirements": "HTML5, JavaScript",
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "USD"
            }
        };
    }

    /**
     * Create home page schema
     */
    createHomePageSchema() {
        return {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": this.currentPageData.title,
            "description": this.currentPageData.description,
            "url": window.location.href,
            "isPartOf": {
                "@type": "WebSite",
                "name": this.siteData.name,
                "url": this.siteData.url
            },
            "mainEntity": {
                "@type": "CreativeWork",
                "name": "Astradigital Ocean",
                "description": "Interactive digital universe",
                "genre": "Cyberpunk Fiction"
            }
        };
    }

    /**
     * Apply schemas to the page
     */
    applySchemas() {
        // Remove existing schema scripts
        document.querySelectorAll('script[type="application/ld+json"]').forEach(script => {
            if (script.getAttribute('data-astradigital-seo')) {
                script.remove();
            }
        });

        // Add new schemas
        this.schemas.forEach((schema, index) => {
            if (schema) {
                const script = document.createElement('script');
                script.type = 'application/ld+json';
                script.setAttribute('data-astradigital-seo', 'true');
                script.textContent = JSON.stringify(schema, null, 2);
                document.head.appendChild(script);
            }
        });

        console.log(`📊 Applied ${this.schemas.length} schema markup(s)`);
    }

    /**
     * Optimize images for SEO
     */
    optimizeImages() {
        document.querySelectorAll('img').forEach(img => {
            // Add alt text if missing
            if (!img.alt) {
                const figcaption = img.closest('figure')?.querySelector('figcaption');
                const title = img.title;
                const dataTitle = img.getAttribute('data-title');
                
                if (figcaption) {
                    img.alt = figcaption.textContent.trim();
                } else if (title) {
                    img.alt = title;
                } else if (dataTitle) {
                    img.alt = dataTitle;
                } else {
                    img.alt = this.generateImageAlt(img);
                }
            }

            // Add loading="lazy" for non-critical images
            if (!img.loading && !this.isCriticalImage(img)) {
                img.loading = 'lazy';
            }

            // Add decoding="async" for better performance
            if (!img.decoding) {
                img.decoding = 'async';
            }
        });
    }

    /**
     * Generate alt text for images
     */
    generateImageAlt(img) {
        const src = img.src;
        const className = img.className;
        
        if (className.includes('faction-logo')) {
            return 'Faction logo';
        } else if (className.includes('character-portrait')) {
            return 'Character portrait';
        } else if (className.includes('territory')) {
            return 'Territory map';
        } else if (src.includes('background')) {
            return 'Background image';
        } else {
            return 'Astradigital image';
        }
    }

    /**
     * Check if image is critical (above the fold)
     */
    isCriticalImage(img) {
        const rect = img.getBoundingClientRect();
        return rect.top < window.innerHeight;
    }

    /**
     * Setup dynamic SEO updates
     */
    setupDynamicUpdates() {
        // Update SEO when content changes
        const observer = new MutationObserver((mutations) => {
            let shouldUpdate = false;
            
            mutations.forEach(mutation => {
                if (mutation.type === 'childList' || mutation.type === 'attributes') {
                    shouldUpdate = true;
                }
            });
            
            if (shouldUpdate) {
                setTimeout(() => {
                    this.updateDynamicSEO();
                }, 500);
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ['data-faction', 'data-character', 'data-territory']
        });

        // Update SEO on hash changes
        window.addEventListener('hashchange', () => {
            this.updateDynamicSEO();
        });
    }

    /**
     * Update SEO for dynamic content changes
     */
    updateDynamicSEO() {
        console.log('🔄 Updating dynamic SEO...');
        
        this.detectPageType();
        this.generateBasicMetadata();
        this.generateOpenGraphMetadata();
        this.generateTwitterMetadata();
        this.generateSchemaMarkup();
        this.optimizeImages();
    }

    /**
     * Helper methods
     */
    updateMetaTag(selector, content, attribute = 'name') {
        let meta = document.querySelector(selector);
        if (!meta) {
            meta = document.createElement('meta');
            meta.setAttribute(attribute, selector.match(/\[.*?="(.+?)"/)?.[1] || '');
            document.head.appendChild(meta);
        }
        meta.content = content;
    }

    updateLinkTag(selector, href) {
        let link = document.querySelector(selector);
        if (!link) {
            link = document.createElement('link');
            link.rel = selector.match(/\[rel="(.+?)"/)?.[1] || '';
            document.head.appendChild(link);
        }
        link.href = href;
    }

    createMetaTag(attribute, name, content) {
        const meta = document.createElement('meta');
        meta.setAttribute(attribute, name);
        meta.content = content;
        document.head.appendChild(meta);
    }

    getOGType() {
        switch (this.currentPageData.type) {
            case 'character':
                return 'profile';
            case 'faction':
            case 'territory':
                return 'article';
            default:
                return 'website';
        }
    }

    extractFactionTerritories(element) {
        const territories = [];
        element.querySelectorAll('.territory-name, [data-territory]').forEach(el => {
            territories.push(el.textContent.trim() || el.getAttribute('data-territory'));
        });
        return territories;
    }

    extractFactionCharacters(element) {
        const characters = [];
        element.querySelectorAll('.character-name, [data-character]').forEach(el => {
            characters.push(el.textContent.trim() || el.getAttribute('data-character'));
        });
        return characters;
    }

    /**
     * Get SEO analysis report
     */
    getSEOReport() {
        return {
            pageType: this.currentPageData.type,
            title: document.title,
            description: document.querySelector('meta[name="description"]')?.content || '',
            schemas: this.schemas.length,
            images: {
                total: document.querySelectorAll('img').length,
                withAlt: document.querySelectorAll('img[alt]').length,
                lazy: document.querySelectorAll('img[loading="lazy"]').length
            },
            openGraph: {
                title: document.querySelector('meta[property="og:title"]')?.content || '',
                description: document.querySelector('meta[property="og:description"]')?.content || '',
                image: document.querySelector('meta[property="og:image"]')?.content || ''
            },
            twitter: {
                card: document.querySelector('meta[name="twitter:card"]')?.content || '',
                title: document.querySelector('meta[name="twitter:title"]')?.content || '',
                description: document.querySelector('meta[name="twitter:description"]')?.content || ''
            }
        };
    }
}

// Export for use in other scripts
window.AstradigitalSEOOptimizer = AstradigitalSEOOptimizer;

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    window.astraSEOOptimizer = new AstradigitalSEOOptimizer();
});
