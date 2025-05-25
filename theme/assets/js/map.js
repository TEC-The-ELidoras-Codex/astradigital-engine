/**
 * Interactive Map for The Elidoras Codex
 * Astradigital Ocean Map functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the map
    initAstradigitalMap();
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
 * Show details for a selected region
 */
function showRegionDetails(regionId) {
    fetch('../data/astradigital-map.json')
        .then(response => response.json())
        .then(data => {
            // Find the region data
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
                
                // Set a default image for regions
                detailsImage.src = '../theme/assets/images/map/backgrounds/region-default.jpg';
                detailsImage.alt = region.name;
                
                // Clear previous faction and connection details
                detailsFaction.innerHTML = '';
                detailsConnections.innerHTML = '';
                
                // Show connected regions
                if (region.connections && region.connections.length > 0) {
                    const connectionsTitle = document.createElement('h4');
                    connectionsTitle.textContent = 'Connected Regions:';
                    detailsConnections.appendChild(connectionsTitle);
                    
                    const connectionsList = document.createElement('ul');
                    
                    region.connections.forEach(connectedId => {
                        const connectedRegion = data.regions.find(r => r.id === connectedId);
                        if (connectedRegion) {
                            const listItem = document.createElement('li');
                            listItem.textContent = connectedRegion.name;
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
 * Show details for a selected location marker
 */
function showLocationDetails(locationId) {
    // This is a simplified example - in a real implementation, you would have location data
    // For demonstration, we'll show some placeholder content
    
    const detailsPanel = document.getElementById('details-panel');
    const detailsTitle = document.getElementById('details-title');
    const detailsDescription = document.getElementById('details-description');
    const detailsImage = document.getElementById('details-image');
    const detailsFaction = document.getElementById('details-faction');
    const detailsConnections = document.getElementById('details-connections');
    
    // Convert the location ID to a readable name
    const locationName = locationId
        .split('-')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
    
    // Update the details panel content
    detailsTitle.textContent = locationName;
    detailsDescription.textContent = `This is a point of interest in the Astradigital Ocean. More detailed information about ${locationName} would be shown here.`;
    
    // Set a default image for locations
    detailsImage.src = '../theme/assets/images/map/backgrounds/location-default.jpg';
    detailsImage.alt = locationName;
    
    // Clear previous faction and connection details
    detailsFaction.innerHTML = '';
    detailsConnections.innerHTML = '';
    
    // Show the details panel
    detailsPanel.classList.add('active');
}
