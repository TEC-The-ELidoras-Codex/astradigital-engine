/**
 * Astradigital Engine JavaScript
 * 
 * Main interactive functionality for the Astradigital Ocean experience
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the Astradigital Ocean experience
    initAstradigital();
});

/**
 * Main initialization function for Astradigital features
 */
function initAstradigital() {
    console.log('Initializing Enhanced Astradigital Engine...');
    
    // Initialize existing functionality
    setupInteractiveElements();
    initFactionInteractions();
    initCharacterInteractions();
    initTerritoryVisualizations();
    addNavigationHandlers();
    addSmoothScrolling();
    setupKeyboardShortcuts();
    
    // Initialize new functionality
    enhancedFactionInteractions();
    initAssetManagement();
    checkMapNavigation();
    
    console.log('Enhanced Astradigital Engine initialized successfully');
}

/**
 * Set up the interactive elements in the ocean visualization
 */
function setupInteractiveElements() {
    const interactiveContainer = document.querySelector('.interactive-elements');
    
    // If no container found, exit early
    if (!interactiveContainer) return;
    
    // Example of dynamically adding interactive points
    const interactivePoints = [
        { x: 25, y: 35, id: 'point-1', label: 'MAGMASOX HQ' },
        { x: 75, y: 65, id: 'point-2', label: 'Kaznak Outpost' },
        { x: 50, y: 20, id: 'point-3', label: 'Data Artifact' }
    ];
    
    interactivePoints.forEach(point => {
        const pointElement = document.createElement('div');
        pointElement.className = 'interactive-point';
        pointElement.id = point.id;
        pointElement.style.left = `${point.x}%`;
        pointElement.style.top = `${point.y}%`;
        
        const pointLabel = document.createElement('span');
        pointLabel.className = 'point-label';
        pointLabel.textContent = point.label;
        
        pointElement.appendChild(pointLabel);
        interactiveContainer.appendChild(pointElement);
        
        // Add click event
        pointElement.addEventListener('click', function() {
            console.log(`Interactive point clicked: ${point.label}`);
            // Add specific interaction logic here
        });
    });
}

/**
 * Initialize faction card interactions
 */
function initFactionInteractions() {
    const factionCards = document.querySelectorAll('.faction-card');
    const explorerBtns = document.querySelectorAll('.faction-explore-btn');
    const mapBtns = document.querySelectorAll('.faction-map-btn');
    
    // Faction card hover effects
    factionCards.forEach(card => {
        card.addEventListener('click', function(e) {
            // Prevent navigation if clicking the explore or map buttons
            if (e.target.classList.contains('faction-explore-btn') || 
                e.target.classList.contains('faction-map-btn')) return;
            
            const factionId = this.id.replace('faction-', '');
            console.log(`Faction clicked: ${factionId}`);
            
            // Highlight faction territory
            highlightFactionTerritory(factionId);
        });
    });
    
    // Explore button interactions
    explorerBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const factionId = this.getAttribute('data-faction');
            console.log(`Exploring faction: ${factionId}`);
            
            // Add faction exploration logic here
            showFactionDetails(factionId);
        });
    });
    
    // Map button interactions
    mapBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const factionId = this.getAttribute('data-faction');
            console.log(`Viewing territory for faction: ${factionId}`);
            
            // Focus on faction territory
            focusFactionTerritory(factionId);
        });
    });
}

/**
 * Highlight a faction's territory on the map
 */
function highlightFactionTerritory(factionId) {
    // Clear previous highlights
    clearTerritoryHighlights();
    
    // Define faction territories (percentages of ocean area)
    const territories = {
        'magmasox': { x: 20, y: 30, size: 80, color: '#ff5757' },
        'kaznak': { x: 70, y: 60, size: 70, color: '#00bdff' },
        'tec': { x: 45, y: 45, size: 90, color: '#4deeea' },
        'killjoy': { x: 15, y: 75, size: 60, color: '#8c52ff' },
        'no-names-anon': { x: 80, y: 20, size: 50, color: '#3de686' },
        'east-middle-company': { x: 60, y: 80, size: 75, color: '#ffd700' }
    };
    
    const territory = territories[factionId];
    if (!territory) return;
    
    // Create or update territory overlay
    let overlay = document.querySelector('.territory-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'territory-overlay';
        document.querySelector('.astra-ocean-visual').appendChild(overlay);
    }
    
    // Create territory region
    const region = document.createElement('div');
    region.className = 'territory-region active';
    region.style.left = `${territory.x}%`;
    region.style.top = `${territory.y}%`;
    region.style.width = `${territory.size}px`;
    region.style.height = `${territory.size}px`;
    region.style.borderColor = territory.color;
    region.style.boxShadow = `0 0 20px ${territory.color}50`;
    
    overlay.appendChild(region);
    
    // Auto-clear after 3 seconds
    setTimeout(() => {
        clearTerritoryHighlights();
    }, 3000);
}

/**
 * Focus on a specific faction's territory
 */
function focusFactionTerritory(factionId) {
    highlightFactionTerritory(factionId);
    
    // Scroll to ocean visual
    const oceanVisual = document.querySelector('.astra-ocean-visual');
    if (oceanVisual) {
        oceanVisual.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Clear all territory highlights
 */
function clearTerritoryHighlights() {
    const overlay = document.querySelector('.territory-overlay');
    if (overlay) {
        overlay.innerHTML = '';
    }
}

/**
 * Show detailed faction information
 */
function showFactionDetails(factionId) {
    const factionData = {
        'magmasox': {
            name: 'MAGMASOX',
            description: 'Technological pioneers pushing the boundaries of digital innovation.',
            territory: 'Innovation Labs & Research Stations',
            specialty: 'Advanced Technology Development',
            members: '2,847 active researchers',
            color: '#ff5757'
        },
        'kaznak': {
            name: 'Kaznak Voyagers',
            description: 'Nomadic explorers mapping the unknown regions of the Astradigital Ocean.',
            territory: 'Mobile Fleet Networks',
            specialty: 'Exploration & Data Archaeology',
            members: '1,203 active voyagers',
            color: '#00bdff'
        },
        'tec': {
            name: 'The Elidoras Codex',
            description: 'Guardians of ancient knowledge and keepers of the cosmic archives.',
            territory: 'Central Data Archives',
            specialty: 'Knowledge Preservation & Lore Keeping',
            members: '892 archivists',
            color: '#4deeea'
        },
        'killjoy': {
            name: 'Killjoy Collective',
            description: 'Chaos agents disrupting established patterns and systems.',
            territory: 'Scattered Disruption Nodes',
            specialty: 'System Disruption & Pattern Breaking',
            members: '??? (classified)',
            color: '#8c52ff'
        },
        'no-names-anon': {
            name: 'No Names Anonymous',
            description: 'Shadow operatives maintaining anonymity in all operations.',
            territory: 'Hidden Network Infrastructure',
            specialty: 'Covert Operations & Information Security',
            members: '[DATA REDACTED]',
            color: '#3de686'
        },
        'east-middle-company': {
            name: 'East Middle Company',
            description: 'Corporate masters controlling trade and resource distribution.',
            territory: 'Commercial Trade Hubs',
            specialty: 'Economic Control & Resource Management',
            members: '4,567 corporate agents',
            color: '#ffd700'
        }
    };
    
    const faction = factionData[factionId];
    if (!faction) return;
    
    // Create or update faction details modal
    let modal = document.querySelector('.faction-details-modal');
    if (!modal) {
        modal = document.createElement('div');
        modal.className = 'faction-details-modal';
        document.body.appendChild(modal);
    }
    
    modal.innerHTML = `
        <div class="modal-overlay" onclick="closeFactionDetails()"></div>
        <div class="modal-content" style="border-left: 4px solid ${faction.color};">
            <div class="modal-header">
                <h2 style="color: ${faction.color};">${faction.name}</h2>
                <button class="modal-close" onclick="closeFactionDetails()">&times;</button>
            </div>
            <div class="modal-body">
                <p class="faction-desc">${faction.description}</p>
                <div class="faction-details">
                    <div class="detail-item">
                        <strong>Territory:</strong> ${faction.territory}
                    </div>
                    <div class="detail-item">
                        <strong>Specialty:</strong> ${faction.specialty}
                    </div>
                    <div class="detail-item">
                        <strong>Active Members:</strong> ${faction.members}
                    </div>
                </div>
                <div class="modal-actions">
                    <button class="btn-primary" onclick="focusFactionTerritory('${factionId}')">View Territory</button>
                    <button class="btn-secondary" onclick="closeFactionDetails()">Close</button>
                </div>
            </div>
        </div>
    `;
    
    modal.style.display = 'flex';
}

/**
 * Close faction details modal
 */
function closeFactionDetails() {
    const modal = document.querySelector('.faction-details-modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

/**
 * Initialize character card interactions
 */
function initCharacterInteractions() {
    const characterCards = document.querySelectorAll('.character-card');
    const profileBtns = document.querySelectorAll('.character-profile-btn');
    
    characterCards.forEach(card => {
        card.addEventListener('click', function(e) {
            // Prevent navigation if clicking the profile button
            if (e.target.classList.contains('character-profile-btn')) return;
            
            const characterId = this.id.replace('character-', '');
            const factionId = this.getAttribute('data-faction');
            console.log(`Character clicked: ${characterId} from faction: ${factionId}`);
            
            // Highlight character's faction territory
            if (factionId) {
                highlightFactionTerritory(factionId);
            }
        });
    });
    
    profileBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const characterId = this.getAttribute('data-character');
            console.log(`Viewing profile for character: ${characterId}`);
            
            showCharacterProfile(characterId);
        });
    });
}

/**
 * Show detailed character profile
 */
function showCharacterProfile(characterId) {
    const characterData = {
        'mostw': {
            name: 'MOSTW - The Bicolored Witness',
            faction: 'The Elidoras Codex',
            title: 'Cosmic Sentinel | Star-Eyed Prophetess',
            description: 'She isn\'t a god who speaks. She\'s the one who watches when all gods go silent. Eyes forged from a red star and a blue one, orbiting within her skull like twin judgments of fury and grace.',
            abilities: ['Cosmic Observation', 'Memory Recording', 'Universal Archive Access'],
            background: 'A divine entity watching through space, crowned by two stellar orbs. She does not intervene - she remembers, records, and waits until the scream is loud enough to deserve transcription into the cosmos.',
            color: '#4deeea'
        },
        'innovator': {
            name: 'Zyx Flamewright',
            faction: 'MAGMASOX',
            title: 'Chief Innovation Officer',
            description: 'Master of digital alchemy and technological fusion, pushing the boundaries of what\'s possible in the Astradigital Ocean.',
            abilities: ['Digital Alchemy', 'Tech Fusion', 'Innovation Leadership'],
            background: 'Born in the heart of MAGMASOX\'s research labs, Zyx has dedicated their existence to breaking through technological barriers and creating impossible solutions.',
            color: '#ff5757'
        },
        'explorer': {
            name: 'Nova Starchart',
            faction: 'Kaznak Voyagers',
            title: 'Lead Navigator',
            description: 'Nomadic explorer who maps the uncharted regions of the digital frontier, collecting rare data artifacts along the way.',
            abilities: ['Stellar Navigation', 'Artifact Detection', 'Route Mapping'],
            background: 'A seasoned voyager who has spent decades exploring the furthest reaches of the Astradigital Ocean, discovering hidden pathways and forgotten data treasures.',
            color: '#00bdff'
        },
        'chaos': {
            name: 'Void Disruptor',
            faction: 'Killjoy Collective',
            title: 'Chaos Theorist',
            description: 'Architect of digital mayhem who delights in breaking established patterns and creating beautiful chaos from order.',
            abilities: ['Pattern Disruption', 'Chaos Engineering', 'System Subversion'],
            background: 'Once a systems architect, Void discovered the beauty in entropy and dedicated themselves to liberating digital systems from rigid order.',
            color: '#8c52ff'
        },
        'shadow': {
            name: '[REDACTED]',
            faction: 'No Names Anonymous',
            title: 'Shadow Operative',
            description: 'Identity unknown, motives classified. Operates in the shadows of the digital realm, leaving no trace behind.',
            abilities: ['[CLASSIFIED]', '[CLASSIFIED]', '[CLASSIFIED]'],
            background: '[DATA EXPUNGED]',
            color: '#3de686'
        },
        'executive': {
            name: 'Aurelius Goldstream',
            faction: 'East Middle Company',
            title: 'Trade Director',
            description: 'Master of digital commerce and resource allocation, controlling the flow of wealth through the Astradigital Ocean.',
            abilities: ['Market Analysis', 'Resource Optimization', 'Trade Negotiation'],
            background: 'Rising through the ranks of EMC through shrewd business acumen and strategic thinking, Aurelius now controls vast networks of digital commerce.',
            color: '#ffd700'
        }
    };
    
    const character = characterData[characterId];
    if (!character) return;
    
    // Create or update character profile modal
    let modal = document.querySelector('.character-profile-modal');
    if (!modal) {
        modal = document.createElement('div');
        modal.className = 'character-profile-modal';
        document.body.appendChild(modal);
    }
    
    modal.innerHTML = `
        <div class="modal-overlay" onclick="closeCharacterProfile()"></div>
        <div class="modal-content character-modal" style="border-left: 4px solid ${character.color};">
            <div class="modal-header">
                <div class="character-header">
                    <h2 style="color: ${character.color};">${character.name}</h2>
                    <p class="character-faction-title">${character.faction} | ${character.title}</p>
                </div>
                <button class="modal-close" onclick="closeCharacterProfile()">&times;</button>
            </div>
            <div class="modal-body">
                <p class="character-desc">${character.description}</p>
                
                <div class="character-details">
                    <div class="detail-section">
                        <h4>Background</h4>
                        <p>${character.background}</p>
                    </div>
                    
                    <div class="detail-section">
                        <h4>Abilities</h4>
                        <ul class="abilities-list">
                            ${character.abilities.map(ability => `<li>${ability}</li>`).join('')}
                        </ul>
                    </div>
                </div>
                
                <div class="modal-actions">
                    <button class="btn-primary" onclick="highlightFactionTerritory('${characterId}')">View Faction Territory</button>
                    <button class="btn-secondary" onclick="closeCharacterProfile()">Close</button>
                </div>
            </div>
        </div>
    `;
    
    modal.style.display = 'flex';
}

/**
 * Close character profile modal
 */
function closeCharacterProfile() {
    const modal = document.querySelector('.character-profile-modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

/**
 * Initialize navigation interactions
 */
function initNavigationInteractions() {
    // Handle faction navigation clicks
    const factionNavLinks = document.querySelectorAll('a[data-faction]');
    factionNavLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const factionId = this.getAttribute('data-faction');
            
            // Scroll to factions section
            const factionsSection = document.querySelector('.astra-factions');
            if (factionsSection) {
                factionsSection.scrollIntoView({ behavior: 'smooth' });
            }
            
            // Highlight the faction
            setTimeout(() => {
                highlightFactionTerritory(factionId);
                
                // Also highlight the faction card
                const factionCard = document.querySelector(`#faction-${factionId}`);
                if (factionCard) {
                    factionCard.style.transform = 'translateY(-10px) scale(1.05)';
                    factionCard.style.boxShadow = '0 20px 40px rgba(0,0,0,0.4)';
                    
                    setTimeout(() => {
                        factionCard.style.transform = '';
                        factionCard.style.boxShadow = '';
                    }, 2000);
                }
            }, 500);
        });
    });
    
    // Handle character navigation clicks
    const characterNavLinks = document.querySelectorAll('a[data-character]');
    characterNavLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const characterId = this.getAttribute('data-character');
            
            // Scroll to characters section
            const charactersSection = document.querySelector('.astra-characters');
            if (charactersSection) {
                charactersSection.scrollIntoView({ behavior: 'smooth' });
            }
            
            // Highlight the character
            setTimeout(() => {
                const characterCard = document.querySelector(`#character-${characterId}`);
                if (characterCard) {
                    characterCard.style.transform = 'translateY(-15px) scale(1.08)';
                    characterCard.style.boxShadow = '0 25px 50px rgba(0,0,0,0.5)';
                    
                    setTimeout(() => {
                        characterCard.style.transform = '';
                        characterCard.style.boxShadow = '';
                    }, 2000);
                }
            }, 500);
        });
    });
    
    // Handle other navigation links
    const navLinks = document.querySelectorAll('.astra-nav a:not([data-faction]):not([data-character])');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href.startsWith('#')) {
                e.preventDefault();
                const targetId = href.substring(1);
                
                let targetElement;
                if (targetId === 'overview') {
                    targetElement = document.querySelector('.astra-header');
                } else if (targetId === 'factions') {
                    targetElement = document.querySelector('.astra-factions');
                } else if (targetId === 'characters') {
                    targetElement = document.querySelector('.astra-characters');
                } else if (targetId === 'map') {
                    targetElement = document.querySelector('.astra-ocean-visual');
                } else {
                    targetElement = document.querySelector(`#${targetId}`);
                }
                
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });
}

/**
 * Add smooth scrolling behavior and additional utilities
 */
function addSmoothScrolling() {
    // Add smooth scrolling CSS if not already present
    if (!document.querySelector('#smooth-scroll-style')) {
        const style = document.createElement('style');
        style.id = 'smooth-scroll-style';
        style.textContent = `
            html {
                scroll-behavior: smooth;
            }
        `;
        document.head.appendChild(style);
    }
}

/**
 * Initialize territory visualizations with random floating elements
 */
function initTerritoryVisualizations() {
    const oceanVisual = document.querySelector('.astra-ocean-visual');
    if (!oceanVisual) return;
    
    // Create floating particles for ambiance
    createFloatingParticles(oceanVisual);
    
    // Add subtle movement to the ocean backdrop
    addOceanMovement();
}

/**
 * Create floating particles for visual ambiance
 */
function createFloatingParticles(container) {
    for (let i = 0; i < 15; i++) {
        const particle = document.createElement('div');
        particle.className = 'floating-particle';
        particle.style.position = 'absolute';
        particle.style.width = Math.random() * 4 + 2 + 'px';
        particle.style.height = particle.style.width;
        particle.style.backgroundColor = '#4cc9f0';
        particle.style.borderRadius = '50%';
        particle.style.opacity = Math.random() * 0.5 + 0.2;
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.pointerEvents = 'none';
        particle.style.animation = `float ${Math.random() * 10 + 10}s linear infinite`;
        
        container.appendChild(particle);
    }
    
    // Add CSS for floating animation if not present
    if (!document.querySelector('#particle-animation-style')) {
        const style = document.createElement('style');
        style.id = 'particle-animation-style';
        style.textContent = `
            @keyframes float {
                0% {
                    transform: translateY(0px) translateX(0px);
                    opacity: 0.2;
                }
                50% {
                    opacity: 0.8;
                }
                100% {
                    transform: translateY(-20px) translateX(10px);
                    opacity: 0.2;
                }
            }
        `;
        document.head.appendChild(style);
    }
}

/**
 * Add subtle movement to the ocean backdrop
 */
function addOceanMovement() {
    const backdrop = document.querySelector('.ocean-backdrop');
    if (!backdrop) return;
    
    let animationId;
    let time = 0;
    
    function animate() {
        time += 0.01;
        const x = Math.sin(time) * 2;
        const y = Math.cos(time * 0.7) * 1;
        
        backdrop.style.transform = `translate(${x}px, ${y}px) scale(1.02)`;
        
        animationId = requestAnimationFrame(animate);
    }
    
    animate();
    
    // Pause animation when page is not visible
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            cancelAnimationFrame(animationId);
        } else {
            animate();
        }
    });
}

/**
 * Handle keyboard shortcuts for better accessibility
 */
function initKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // ESC key to close modals
        if (e.key === 'Escape') {
            closeFactionDetails();
            closeCharacterProfile();
        }
        
        // Arrow keys for navigation
        if (e.altKey) {
            switch(e.key) {
                case 'ArrowDown':
                    e.preventDefault();
                    document.querySelector('.astra-factions')?.scrollIntoView({ behavior: 'smooth' });
                    break;
                case 'ArrowRight':
                    e.preventDefault();
                    document.querySelector('.astra-characters')?.scrollIntoView({ behavior: 'smooth' });
                    break;
                case 'ArrowUp':
                    e.preventDefault();
                    document.querySelector('.astra-header')?.scrollIntoView({ behavior: 'smooth' });
                    break;
                case 'ArrowLeft':
                    e.preventDefault();
                    document.querySelector('.astra-ocean-visual')?.scrollIntoView({ behavior: 'smooth' });
                    break;
            }
        }
    });
}

// Initialize keyboard shortcuts when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initKeyboardShortcuts();
});

// Add resize handler for responsive behavior
window.addEventListener('resize', function() {
    // Recalculate territory positions on resize
    clearTerritoryHighlights();
    
    // Adjust particle count based on screen size
    const particles = document.querySelectorAll('.floating-particle');
    const targetCount = window.innerWidth < 768 ? 8 : 15;
    
    if (particles.length > targetCount) {
        for (let i = targetCount; i < particles.length; i++) {
            particles[i].remove();
        }
    }
});

/**
 * Enhanced map integration functionality
 */

/**
 * Navigate to the interactive map and highlight a specific faction's territory
 */
function navigateToMapTerritory(factionId) {
    // Store the faction to highlight in sessionStorage for map.js to pick up
    sessionStorage.setItem('highlightFaction', factionId);
    
    // Navigate to the map page
    const mapUrl = 'map.html';
    if (window.location.pathname.includes('map.html')) {
        // Already on map page, just trigger highlight
        highlightMapTerritory(factionId);
    } else {
        // Navigate to map page
        window.location.href = mapUrl;
    }
}

/**
 * Highlight territory on the actual SVG map
 */
function highlightMapTerritory(factionId) {
    // Get faction-specific territories from map data
    const territoryMap = {
        'magmasox': ['magmasox-waters', 'shadowban-triangle', 'gpt-islands'],
        'kaznak': ['the-34-highways', 'missing-35th-route'],
        'tec': ['tec-waters'],
        'killjoy': ['underground-blockchain-pathways'],
        'no-names-anon': ['slkrode'],
        'east-middle-company': ['linux-volcanic-archipelago']
    };
    
    const territories = territoryMap[factionId] || [];
    
    // Clear previous highlights
    document.querySelectorAll('.territory.highlighted').forEach(el => {
        el.classList.remove('highlighted');
    });
    
    // Highlight faction territories
    territories.forEach(territoryId => {
        const territory = document.getElementById(territoryId);
        if (territory) {
            territory.classList.add('highlighted');
            
            // Add pulsing animation
            territory.style.animation = 'territoryPulse 2s ease-in-out infinite';
            
            // Remove animation after 6 seconds
            setTimeout(() => {
                territory.style.animation = '';
                territory.classList.remove('highlighted');
            }, 6000);
        }
    });
}

/**
 * Check for pending map navigation on page load
 */
function checkMapNavigation() {
    const highlightFaction = sessionStorage.getItem('highlightFaction');
    if (highlightFaction && window.location.pathname.includes('map.html')) {
        // Delay to ensure map is loaded
        setTimeout(() => {
            highlightMapTerritory(highlightFaction);
            sessionStorage.removeItem('highlightFaction');
        }, 1000);
    }
}

/**
 * Enhanced faction interactions with map integration
 */
function enhancedFactionInteractions() {
    // Update existing faction buttons to include map navigation
    document.querySelectorAll('[data-faction]').forEach(button => {
        const factionId = button.getAttribute('data-faction');
        
        // Add map navigation button if not already present
        if (!button.querySelector('.map-nav-btn')) {
            const mapNavBtn = document.createElement('button');
            mapNavBtn.className = 'map-nav-btn';
            mapNavBtn.innerHTML = '🗺️ View Territory';
            mapNavBtn.onclick = (e) => {
                e.stopPropagation();
                navigateToMapTerritory(factionId);
            };
            
            button.appendChild(mapNavBtn);
        }
    });
    
    // Add map navigation to character profiles
    document.querySelectorAll('[data-character]').forEach(button => {
        const characterId = button.getAttribute('data-character');
        const characterFactions = {
            'mostw': 'magmasox',
            'zyx-flamewright': 'magmasox',
            'nova-starchart': 'kaznak',
            'void-disruptor': 'killjoy',
            'redacted': 'no-names-anon',
            'aurelius-goldstream': 'east-middle-company'
        };
        
        const factionId = characterFactions[characterId];
        if (factionId && !button.querySelector('.map-nav-btn')) {
            const mapNavBtn = document.createElement('button');
            mapNavBtn.className = 'map-nav-btn character-map-btn';
            mapNavBtn.innerHTML = '🗺️ Home Territory';
            mapNavBtn.onclick = (e) => {
                e.stopPropagation();
                navigateToMapTerritory(factionId);
            };
            
            button.appendChild(mapNavBtn);
        }
    });
}

/**
 * Asset management for faction logos and character portraits
 */
function initAssetManagement() {
    // Check for missing faction logos and create placeholders
    const factionLogos = document.querySelectorAll('.faction-logo img');
    factionLogos.forEach(img => {
        img.onerror = function() {
            // Create a procedural faction logo
            const factionId = this.getAttribute('data-faction') || 
                              this.closest('[data-faction]')?.getAttribute('data-faction');
            if (factionId) {
                this.src = generateFactionLogo(factionId);
            }
        };
    });
    
    // Check for missing character portraits
    const characterPortraits = document.querySelectorAll('.character-portrait img');
    characterPortraits.forEach(img => {
        img.onerror = function() {
            const characterId = this.getAttribute('data-character') ||
                               this.closest('[data-character]')?.getAttribute('data-character');
            if (characterId) {
                this.src = generateCharacterPortrait(characterId);
            }
        };
    });
}

/**
 * Generate procedural faction logo as data URL
 */
function generateFactionLogo(factionId) {
    const canvas = document.createElement('canvas');
    canvas.width = 120;
    canvas.height = 120;
    const ctx = canvas.getContext('2d');
    
    // Faction-specific colors and symbols
    const factionData = {
        'magmasox': { color: '#ff5757', symbol: '▣', bgPattern: 'grid' },
        'kaznak': { color: '#00bdff', symbol: '▲', bgPattern: 'waves' },
        'tec': { color: '#4deeea', symbol: '◊', bgPattern: 'spiral' },
        'killjoy': { color: '#8c52ff', symbol: '⚡', bgPattern: 'chaos' },
        'no-names-anon': { color: '#3de686', symbol: '?', bgPattern: 'static' },
        'east-middle-company': { color: '#ffd700', symbol: '₪', bgPattern: 'coins' }
    };
    
    const faction = factionData[factionId] || factionData['tec'];
    
    // Create gradient background
    const gradient = ctx.createRadialGradient(60, 60, 10, 60, 60, 60);
    gradient.addColorStop(0, faction.color + '80');
    gradient.addColorStop(1, faction.color + '20');
    
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 120, 120);
    
    // Add border
    ctx.strokeStyle = faction.color;
    ctx.lineWidth = 3;
    ctx.strokeRect(3, 3, 114, 114);
    
    // Add faction symbol
    ctx.fillStyle = faction.color;
    ctx.font = 'bold 48px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(faction.symbol, 60, 60);
    
    return canvas.toDataURL();
}

/**
 * Generate procedural character portrait as data URL
 */
function generateCharacterPortrait(characterId) {
    const canvas = document.createElement('canvas');
    canvas.width = 200;
    canvas.height = 200;
    const ctx = canvas.getContext('2d');
    
    // Character-specific colors and features
    const characterData = {
        'mostw': { color: '#ff5757', shape: 'square', eyes: 'red' },
        'zyx-flamewright': { color: '#ff8c00', shape: 'triangle', eyes: 'orange' },
        'nova-starchart': { color: '#00bdff', shape: 'star', eyes: 'blue' },
        'void-disruptor': { color: '#8c52ff', shape: 'hexagon', eyes: 'purple' },
        'redacted': { color: '#3de686', shape: 'circle', eyes: 'green' },
        'aurelius-goldstream': { color: '#ffd700', shape: 'diamond', eyes: 'gold' }
    };
    
    const character = characterData[characterId] || characterData['nova-starchart'];
    
    // Background gradient
    const gradient = ctx.createRadialGradient(100, 100, 20, 100, 100, 100);
    gradient.addColorStop(0, character.color + '60');
    gradient.addColorStop(1, '#0a0e17');
    
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 200, 200);
    
    // Character silhouette based on shape
    ctx.fillStyle = character.color + '80';
    drawCharacterShape(ctx, character.shape, 100, 100, 60);
    
    // Add glowing eyes
    ctx.fillStyle = character.eyes;
    ctx.shadowColor = character.eyes;
    ctx.shadowBlur = 10;
    ctx.beginPath();
    ctx.arc(85, 80, 4, 0, Math.PI * 2);
    ctx.arc(115, 80, 4, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0;
    
    return canvas.toDataURL();
}

/**
 * Draw character silhouette shape
 */
function drawCharacterShape(ctx, shape, x, y, size) {
    ctx.beginPath();
    
    switch(shape) {
        case 'square':
            ctx.rect(x - size/2, y - size/2, size, size);
            break;
        case 'triangle':
            ctx.moveTo(x, y - size/2);
            ctx.lineTo(x - size/2, y + size/2);
            ctx.lineTo(x + size/2, y + size/2);
            ctx.closePath();
            break;
        case 'star':
            drawStar(ctx, x, y, 5, size/2, size/4);
            break;
        case 'hexagon':
            drawHexagon(ctx, x, y, size/2);
            break;
        case 'diamond':
            ctx.moveTo(x, y - size/2);
            ctx.lineTo(x + size/2, y);
            ctx.lineTo(x, y + size/2);
            ctx.lineTo(x - size/2, y);
            ctx.closePath();
            break;
        default: // circle
            ctx.arc(x, y, size/2, 0, Math.PI * 2);
    }
    
    ctx.fill();
}

/**
 * Draw star shape
 */
function drawStar(ctx, x, y, spikes, outerRadius, innerRadius) {
    let rot = Math.PI / 2 * 3;
    let step = Math.PI / spikes;
    
    ctx.moveTo(x, y - outerRadius);
    
    for (let i = 0; i < spikes; i++) {
        ctx.lineTo(x + Math.cos(rot) * outerRadius, y + Math.sin(rot) * outerRadius);
        rot += step;
        ctx.lineTo(x + Math.cos(rot) * innerRadius, y + Math.sin(rot) * innerRadius);
        rot += step;
    }
    
    ctx.lineTo(x, y - outerRadius);
    ctx.closePath();
}

/**
 * Draw hexagon shape
 */
function drawHexagon(ctx, x, y, size) {
    const angle = Math.PI / 3;
    ctx.moveTo(x + size, y);
    
    for (let i = 1; i < 6; i++) {
        ctx.lineTo(x + size * Math.cos(angle * i), y + size * Math.sin(angle * i));
    }
    
    ctx.closePath();
}
