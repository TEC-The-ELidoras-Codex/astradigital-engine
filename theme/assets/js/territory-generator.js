/**
 * SVG Territory Generator for The Elidoras Codex Map
 * 
 * This script helps generate SVG territory shapes with proper faction colors
 * for each region in the Astradigital Ocean map.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Fetch the map data
    fetch('../data/astradigital-map.json')
        .then(response => response.json())
        .then(data => {
            // Process faction territories
            processFactionTerritories(data);
        })
        .catch(error => {
            console.error('Error loading map data:', error);
        });
});

/**
 * Process faction territories and apply appropriate styling
 */
function processFactionTerritories(mapData) {
    // Create a map of regions to controlling factions
    const regionFactionMap = {};
    
    // For each faction, process their territories
    mapData.factions.forEach(faction => {
        // Parse the territory string to extract region names
        const territories = faction.territory.split(',').map(t => t.trim());
        
        // Match territory names to region IDs
        territories.forEach(territoryName => {
            // Find matching region by name similarity
            const matchingRegion = findMatchingRegion(territoryName, mapData.regions);
            
            if (matchingRegion) {
                regionFactionMap[matchingRegion.id] = faction.id;
            }
        });
    });
    
    // Now apply the faction classes to the territory SVG elements
    const territorySVGs = document.querySelectorAll('.territory');
    
    territorySVGs.forEach(territory => {
        const regionId = territory.id;
        const factionId = regionFactionMap[regionId];
        
        if (factionId) {
            // Add the faction-specific class
            territory.classList.add(`faction-${factionId}`);
            
            // Store the faction ID as data attribute for reference
            territory.setAttribute('data-faction', factionId);
        }
    });
}

/**
 * Find a region that best matches the given territory name
 */
function findMatchingRegion(territoryName, regions) {
    // Convert to lowercase for comparison
    const territoryLower = territoryName.toLowerCase();
    
    // Try to find an exact match first
    const exactMatch = regions.find(region => 
        region.name.toLowerCase() === territoryLower
    );
    
    if (exactMatch) return exactMatch;
    
    // Try to find a partial match
    const partialMatch = regions.find(region => 
        territoryLower.includes(region.name.toLowerCase()) || 
        region.name.toLowerCase().includes(territoryLower)
    );
    
    return partialMatch || null;
}
