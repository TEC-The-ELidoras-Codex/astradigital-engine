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
    console.log('Astradigital Engine Initialized');
    
    // Set up interactive elements
    setupInteractiveElements();
    
    // Initialize faction interactions
    initFactionInteractions();
    
    // Initialize character interactions
    initCharacterInteractions();
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
    
    factionCards.forEach(card => {
        card.addEventListener('click', function(e) {
            // Prevent navigation if clicking the explore button
            if (e.target.classList.contains('faction-explore-btn')) return;
            
            const factionId = this.id.replace('faction-', '');
            console.log(`Faction clicked: ${factionId}`);
            
            // Add faction-specific interactions here
        });
    });
}

/**
 * Initialize character card interactions
 */
function initCharacterInteractions() {
    const characterCards = document.querySelectorAll('.character-card');
    
    characterCards.forEach(card => {
        card.addEventListener('click', function(e) {
            // Prevent navigation if clicking the profile button
            if (e.target.classList.contains('character-profile-btn')) return;
            
            const characterId = this.id.replace('character-', '');
            console.log(`Character clicked: ${characterId}`);
            
            // Add character-specific interactions here
        });
    });
}
