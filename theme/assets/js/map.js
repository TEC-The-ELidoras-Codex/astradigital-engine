/**
 * Interactive Map for The Elidoras Codex
 * Enhanced Astradigital Ocean Map functionality with faction integration
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the map
    initAstradigitalMap();
    
    // Check for faction highlighting from navigation
    checkFactionHighlighting();
});

/**
 * Initialize the Astradigital Ocean Map
 */
function initAstradigitalMap() {
    // Load the map SVG
    loadMapSVG();
    
    // Setup map controls
    setupMapControls();
    
    // Generate faction legend
    generateFactionLegend();
}

/**
 * Load the SVG map into the container
 */
function loadMapSVG() {
    const mapContainer = document.getElementById('astradigital-map');
    
    // Fetch the SVG file
    fetch('../theme/assets/images/map/astradigital-map.svg')
        .then(response => response.text())
        .then(svg => {
            // Insert the SVG into the container
            mapContainer.innerHTML = svg;
            
            // Setup map event listeners after SVG is loaded
            setupMapEventListeners();
            
            // Draw connections between regions
            drawRegionConnections();
        })
        .catch(error => {
            console.error('Error loading map SVG:', error);
            mapContainer.innerHTML = '<p>Error loading map. Please try again later.</p>';
        });
}

/**
 * Setup map zoom and pan controls
 */
function setupMapControls() {
    const zoomIn = document.getElementById('zoom-in');
    const zoomOut = document.getElementById('zoom-out');
    const resetView = document.getElementById('reset-view');
    
    let scale = 1;
    let translateX = 0;
    let translateY = 0;
    
    // Zoom in button
    zoomIn.addEventListener('click', () => {
        scale += 0.1;
        updateMapTransform();
    });
    
    // Zoom out button
    zoomOut.addEventListener('click', () => {
        scale = Math.max(0.5, scale - 0.1);
        updateMapTransform();
    });
    
    // Reset view button
    resetView.addEventListener('click', () => {
        scale = 1;
        translateX = 0;
        translateY = 0;
        updateMapTransform();
    });
    
    // Function to update the map transformation
    function updateMapTransform() {
        const mapSvg = document.querySelector('#astradigital-map svg');
        if (mapSvg) {
            mapSvg.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
        }
    }
    
    // Setup pan functionality
    let isDragging = false;
    let startX, startY;
    
    document.addEventListener('mousedown', (e) => {
        if (e.target.closest('#astradigital-map')) {
            isDragging = true;
            startX = e.clientX - translateX;
            startY = e.clientY - translateY;
            document.body.style.cursor = 'grabbing';
        }
    });
    
    document.addEventListener('mousemove', (e) => {
        if (isDragging) {
            translateX = e.clientX - startX;
            translateY = e.clientY - startY;
            updateMapTransform();
        }
    });
    
    document.addEventListener('mouseup', () => {
        isDragging = false;
        document.body.style.cursor = 'default';
    });
    
    // Handle mouse wheel for zooming
    document.querySelector('#astradigital-map').addEventListener('wheel', (e) => {
        e.preventDefault();
        
        // Determine zoom direction
        if (e.deltaY < 0) {
            // Zoom in
            scale = Math.min(3, scale + 0.1);
        } else {
            // Zoom out
            scale = Math.max(0.5, scale - 0.1);
        }
        
        updateMapTransform();
    });
}

/**
 * Setup event listeners for map elements
 */
function setupMapEventListeners() {
    // Get all territories and markers
    const territories = document.querySelectorAll('.territory');
    const markers = document.querySelectorAll('.map-marker');
    
    // Add event listeners to territories
    territories.forEach(territory => {
        territory.addEventListener('click', () => {
            const regionId = territory.id;
            showRegionDetails(regionId);
        });
    });
    
    // Add event listeners to markers
    markers.forEach(marker => {
        marker.addEventListener('click', () => {
            const locationId = marker.getAttribute('data-id');
            showLocationDetails(locationId);
        });
    });
}

/**
 * Generate faction legend based on the map data
 */
function generateFactionLegend() {
    const factionLegend = document.querySelector('.faction-legend');
    
    // Fetch the map data
    fetch('../data/astradigital-map.json')
        .then(response => response.json())
        .then(data => {
            // Create legend items for each faction
            data.factions.forEach(faction => {
                const legendItem = document.createElement('div');
                legendItem.className = 'legend-item';
                
                const colorSwatch = document.createElement('div');
                colorSwatch.className = 'legend-color';
                colorSwatch.style.backgroundColor = faction.color;
                
                const factionName = document.createElement('span');
                factionName.textContent = faction.name;
                
                legendItem.appendChild(colorSwatch);
                legendItem.appendChild(factionName);
                factionLegend.appendChild(legendItem);
            });
        })
        .catch(error => {
            console.error('Error loading faction data:', error);
            factionLegend.innerHTML = '<p>Error loading faction data.</p>';
        });
}

/**
 * Draw connections between regions based on data
 */
function drawRegionConnections() {
    const connectionsGroup = document.querySelector('.connections');
    
    // Fetch the map data
    fetch('../data/astradigital-map.json')
        .then(response => response.json())
        .then(data => {
            // Process each region's connections
            data.regions.forEach(region => {
                const regionElement = document.getElementById(region.id);
                
                if (regionElement && region.connections && region.connections.length > 0) {
                    // Get the center point of this region
                    const regionCenter = getElementCenter(regionElement);
                    
                    // Draw connections to each connected region
                    region.connections.forEach(connectedRegionId => {
                        const connectedRegion = document.getElementById(connectedRegionId);
                        
                        if (connectedRegion) {
                            const connectedCenter = getElementCenter(connectedRegion);
                            
                            // Create a line connecting the regions
                            const connectionLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                            connectionLine.setAttribute('x1', regionCenter.x);
                            connectionLine.setAttribute('y1', regionCenter.y);
                            connectionLine.setAttribute('x2', connectedCenter.x);
                            connectionLine.setAttribute('y2', connectedCenter.y);
                            connectionLine.setAttribute('stroke', 'rgba(255, 255, 255, 0.2)');
                            connectionLine.setAttribute('stroke-width', '1');
                            connectionLine.setAttribute('stroke-dasharray', '5,3');
                            
                            connectionsGroup.appendChild(connectionLine);
                        }
                    });
                }
            });
        })
        .catch(error => {
            console.error('Error drawing region connections:', error);
        });
}

/**
 * Get the center point of an SVG element
 */
function getElementCenter(element) {
    const bbox = element.getBBox();
    return {
        x: bbox.x + bbox.width / 2,
        y: bbox.y + bbox.height / 2
    };
}

/**
 * Check for pending faction highlighting from cross-navigation
 */
function checkFactionHighlighting() {
    const highlightFaction = sessionStorage.getItem('highlightFaction');
    if (highlightFaction) {
        setTimeout(() => {
            highlightFactionTerritories(highlightFaction);
            sessionStorage.removeItem('highlightFaction');
            showMapIntegrationStatus(`Highlighting ${getFactionName(highlightFaction)} territories`);
        }, 1500); // Wait for map to load
    }
}

/**
 * Highlight specific faction territories on the map
 */
function highlightFactionTerritories(factionId) {
    // Territory mappings from the JSON data
    const factionTerritories = {
        'magmasox': ['magmasox-waters', 'shadowban-triangle', 'gpt-islands'],
        'kaznak': ['the-34-highways', 'missing-35th-route'],
        'tec': ['tec-waters'],
        'killjoy': ['underground-blockchain-pathways'],
        'no-names-anon': ['slkrode'],
        'east-middle-company': ['linux-volcanic-archipelago']
    };
    
    const territories = factionTerritories[factionId] || [];
    
    // Clear previous highlights
    clearAllHighlights();
    
    // Highlight faction territories
    territories.forEach(territoryId => {
        const territory = document.getElementById(territoryId);
        if (territory) {
            territory.classList.add('highlighted');
            territory.classList.add(`faction-${factionId}-highlight`);
            
            // Add pulsing animation
            territory.style.animation = 'territoryPulse 2s ease-in-out infinite';
            
            // Focus the view on the first territory
            if (territory === document.getElementById(territories[0])) {
                focusOnElement(territory);
            }
        }
    });
    
    // Auto-clear highlights after 8 seconds
    setTimeout(() => {
        clearFactionHighlights(factionId);
    }, 8000);
}

/**
 * Clear all territory highlights
 */
function clearAllHighlights() {
    document.querySelectorAll('.territory.highlighted').forEach(territory => {
        territory.classList.remove('highlighted');
        territory.style.animation = '';
        // Remove faction-specific highlight classes
        territory.classList.forEach(className => {
            if (className.includes('-highlight')) {
                territory.classList.remove(className);
            }
        });
    });
}

/**
 * Clear highlights for a specific faction
 */
function clearFactionHighlights(factionId) {
    document.querySelectorAll(`.faction-${factionId}-highlight`).forEach(territory => {
        territory.classList.remove('highlighted');
        territory.classList.remove(`faction-${factionId}-highlight`);
        territory.style.animation = '';
    });
}

/**
 * Focus the map view on a specific element
 */
function focusOnElement(element) {
    const bbox = element.getBBox();
    const mapSvg = document.querySelector('#astradigital-map svg');
    
    if (mapSvg && bbox) {
        const centerX = bbox.x + bbox.width / 2;
        const centerY = bbox.y + bbox.height / 2;
        
        // Calculate transform to center the element
        const mapRect = mapSvg.getBoundingClientRect();
        const translateX = (mapRect.width / 2) - centerX;
        const translateY = (mapRect.height / 2) - centerY;
        
        // Apply transform with animation
        mapSvg.style.transition = 'transform 1s ease-in-out';
        mapSvg.style.transform = `translate(${translateX}px, ${translateY}px) scale(1.2)`;
        
        // Reset after highlighting period
        setTimeout(() => {
            mapSvg.style.transform = 'translate(0px, 0px) scale(1)';
        }, 6000);
    }
}

/**
 * Get faction display name
 */
function getFactionName(factionId) {
    const factionNames = {
        'magmasox': 'MAGMASOX',
        'kaznak': 'Kaznak Voyagers',
        'tec': 'The Elidoras Codex',
        'killjoy': 'Killjoy Collective',
        'no-names-anon': 'No Names Anonymous',
        'east-middle-company': 'East Middle Company'
    };
    return factionNames[factionId] || factionId;
}

/**
 * Show map integration status message
 */
function showMapIntegrationStatus(message) {
    let statusDiv = document.querySelector('.map-integration-status');
    if (!statusDiv) {
        statusDiv = document.createElement('div');
        statusDiv.className = 'map-integration-status';
        document.body.appendChild(statusDiv);
    }
    
    statusDiv.textContent = message;
    statusDiv.classList.add('active');
    
    setTimeout(() => {
        statusDiv.classList.remove('active');
    }, 3000);
}

/**
 * Enhanced region details with faction information
 */
function enhancedShowRegionDetails(regionId) {
    fetch('../data/astradigital-map.json')
        .then(response => response.json())
        .then(data => {
            const region = data.regions.find(r => r.id === regionId);
            
            if (region) {
                const detailsPanel = document.getElementById('details-panel');
                const detailsTitle = document.getElementById('details-title');
                const detailsDescription = document.getElementById('details-description');
                const detailsImage = document.getElementById('details-image');
                const detailsFaction = document.getElementById('details-faction');
                const detailsConnections = document.getElementById('details-connections');
                
                // Update the details panel content
                detailsTitle.textContent = region.name;
                detailsDescription.textContent = region.description;
                
                // Determine controlling faction
                const controllingFaction = getRegionControllingFaction(regionId);
                if (controllingFaction) {
                    const faction = data.factions.find(f => f.id === controllingFaction);
                    if (faction) {
                        detailsFaction.innerHTML = `
                            <h4>Controlled by:</h4>
                            <div class="faction-control-info">
                                <span class="faction-name" style="color: ${faction.color}">${faction.name}</span>
                                <p class="faction-desc">${faction.shortDescription}</p>
                                <button class="view-faction-btn" onclick="navigateToFaction('${faction.id}')">
                                    View Faction Details
                                </button>
                            </div>
                        `;
                    }
                }
                
                // Enhanced connections display
                if (region.connections && region.connections.length > 0) {
                    const connectionsTitle = document.createElement('h4');
                    connectionsTitle.textContent = 'Connected Regions:';
                    detailsConnections.appendChild(connectionsTitle);
                    
                    const connectionsList = document.createElement('ul');
                    connectionsList.className = 'connections-list';
                    
                    region.connections.forEach(connectedId => {
                        const connectedRegion = data.regions.find(r => r.id === connectedId);
                        if (connectedRegion) {
                            const listItem = document.createElement('li');
                            listItem.className = 'connection-item';
                            
                            const connectedFaction = getRegionControllingFaction(connectedId);
                            const factionColor = connectedFaction ? 
                                data.factions.find(f => f.id === connectedFaction)?.color || '#ffffff' : '#ffffff';
                            

                            listItem.innerHTML = `
                                <span class="connection-name" style="border-left: 3px solid ${factionColor}">
                                    ${connectedRegion.name}
                                </span>
                                <button class="nav-to-region" onclick="highlightRegion('${connectedId}')">
                                    Navigate →
                                </button>
                            `;
                            connectionsList.appendChild(listItem);
                        }
                    });
                    
                    detailsConnections.appendChild(connectionsList);
                }
                
                // Show the details panel
                detailsPanel.classList.add('active');
            }
        })
        .catch(error => {
            console.error('Error showing region details:', error);
        });
}

/**
 * Get the controlling faction for a region
 */
function getRegionControllingFaction(regionId) {
    const factionTerritories = {
        'magmasox-waters': 'magmasox',
        'shadowban-triangle': 'magmasox',
        'gpt-islands': 'magmasox',
        'the-34-highways': 'kaznak',
        'missing-35th-route': 'kaznak',
        'tec-waters': 'tec',
        'underground-blockchain-pathways': 'killjoy',
        'slkrode': 'no-names-anon',
        'linux-volcanic-archipelago': 'east-middle-company'
    };
    
    return factionTerritories[regionId] || null;
}

/**
 * Navigate to faction details page
 */
function navigateToFaction(factionId) {
    sessionStorage.setItem('highlightFaction', factionId);
    window.location.href = '../index.html#factions';
}

/**
 * Highlight a specific region
 */
function highlightRegion(regionId) {
    clearAllHighlights();
    
    const region = document.getElementById(regionId);
    if (region) {
        region.classList.add('highlighted');
        region.style.animation = 'territoryPulse 2s ease-in-out infinite';
        focusOnElement(region);
        
        // Show region details
        enhancedShowRegionDetails(regionId);
        
        setTimeout(() => {
            region.classList.remove('highlighted');
            region.style.animation = '';
        }, 5000);
    }
}

// Override the original showRegionDetails function
window.showRegionDetails = enhancedShowRegionDetails;
