/**
 * Asset Generator for Astradigital Engine
 * Automatically generates faction logos and character portraits
 */

class AstradigitalAssetGenerator {
    constructor() {
        this.factionData = {
            'magmasox': {
                color: '#ff5757',
                secondaryColor: '#ff8c8c',
                symbol: '▣',
                pattern: 'grid',
                description: 'Industrial titans with corporate dominance'
            },
            'kaznak': {
                color: '#00bdff',
                secondaryColor: '#4dd0ff',
                symbol: '▲',
                pattern: 'waves',
                description: 'Rebellious voyagers seeking freedom'
            },
            'tec': {
                color: '#4deeea',
                secondaryColor: '#7df3f0',
                symbol: '◊',
                pattern: 'spiral',
                description: 'Beacon of digital sovereignty'
            },
            'killjoy': {
                color: '#8c52ff',
                secondaryColor: '#a875ff',
                symbol: '⚡',
                pattern: 'chaos',
                description: 'Disruptive collective of chaos agents'
            },
            'no-names-anon': {
                color: '#3de686',
                secondaryColor: '#6beb9f',
                symbol: '?',
                pattern: 'static',
                description: 'Anonymous collective of digital phantoms'
            },
            'east-middle-company': {
                color: '#ffd700',
                secondaryColor: '#ffdf4d',
                symbol: '₪',
                pattern: 'coins',
                description: 'Corporate pirates of the digital seas'
            }
        };

        this.characterData = {
            'mostw': {
                name: 'MOSTW',
                faction: 'magmasox',
                primaryColor: '#ff5757',
                secondaryColor: '#ff8c00',
                shape: 'square',
                features: ['corporate', 'authoritative', 'red-eyes']
            },
            'zyx-flamewright': {
                name: 'Zyx Flamewright',
                faction: 'magmasox',
                primaryColor: '#ff8c00',
                secondaryColor: '#ffb84d',
                shape: 'triangle',
                features: ['flame', 'intense', 'orange-eyes']
            },
            'nova-starchart': {
                name: 'Nova Starchart',
                faction: 'kaznak',
                primaryColor: '#00bdff',
                secondaryColor: '#4dd0ff',
                shape: 'star',
                features: ['navigator', 'wise', 'blue-eyes']
            },
            'void-disruptor': {
                name: 'Void Disruptor',
                faction: 'killjoy',
                primaryColor: '#8c52ff',
                secondaryColor: '#a875ff',
                shape: 'hexagon',
                features: ['chaotic', 'disruptive', 'purple-eyes']
            },
            'redacted': {
                name: '[REDACTED]',
                faction: 'no-names-anon',
                primaryColor: '#3de686',
                secondaryColor: '#6beb9f',
                shape: 'circle',
                features: ['anonymous', 'mysterious', 'green-eyes']
            },
            'aurelius-goldstream': {
                name: 'Aurelius Goldstream',
                faction: 'east-middle-company',
                primaryColor: '#ffd700',
                secondaryColor: '#ffdf4d',
                shape: 'diamond',
                features: ['wealthy', 'corporate', 'gold-eyes']
            }
        };
    }

    /**
     * Generate all faction logos as data URLs
     */
    generateAllFactionLogos() {
        const logos = {};
        Object.keys(this.factionData).forEach(factionId => {
            logos[factionId] = this.generateFactionLogo(factionId);
        });
        return logos;
    }

    /**
     * Generate all character portraits as data URLs
     */
    generateAllCharacterPortraits() {
        const portraits = {};
        Object.keys(this.characterData).forEach(characterId => {
            portraits[characterId] = this.generateCharacterPortrait(characterId);
        });
        return portraits;
    }

    /**
     * Generate a specific faction logo
     */
    generateFactionLogo(factionId, size = 200) {
        const faction = this.factionData[factionId];
        if (!faction) return null;

        const canvas = document.createElement('canvas');
        canvas.width = size;
        canvas.height = size;
        const ctx = canvas.getContext('2d');

        // Background with faction pattern
        this.drawFactionBackground(ctx, faction, size);
        
        // Main emblem
        this.drawFactionEmblem(ctx, faction, size);
        
        // Border and finishing touches
        this.drawFactionBorder(ctx, faction, size);

        return canvas.toDataURL('image/png');
    }

    /**
     * Generate a specific character portrait
     */
    generateCharacterPortrait(characterId, size = 300) {
        const character = this.characterData[characterId];
        if (!character) return null;

        const canvas = document.createElement('canvas');
        canvas.width = size;
        canvas.height = size;
        const ctx = canvas.getContext('2d');

        // Background
        this.drawCharacterBackground(ctx, character, size);
        
        // Character silhouette
        this.drawCharacterSilhouette(ctx, character, size);
        
        // Facial features
        this.drawCharacterFeatures(ctx, character, size);
        
        // Faction affiliation indicator
        this.drawFactionIndicator(ctx, character, size);

        return canvas.toDataURL('image/png');
    }

    /**
     * Draw faction background pattern
     */
    drawFactionBackground(ctx, faction, size) {
        // Gradient background
        const gradient = ctx.createRadialGradient(
            size/2, size/2, size/8,
            size/2, size/2, size/2
        );
        gradient.addColorStop(0, faction.color + '80');
        gradient.addColorStop(0.7, faction.color + '40');
        gradient.addColorStop(1, '#0a0e17');

        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, size, size);

        // Pattern overlay
        this.drawPattern(ctx, faction.pattern, faction.secondaryColor, size);
    }

    /**
     * Draw faction emblem
     */
    drawFactionEmblem(ctx, faction, size) {
        const centerX = size / 2;
        const centerY = size / 2;
        const emblemSize = size * 0.4;

        // Glow effect
        ctx.shadowColor = faction.color;
        ctx.shadowBlur = 20;
        
        // Main symbol
        ctx.fillStyle = faction.color;
        ctx.font = `bold ${emblemSize}px Arial, sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(faction.symbol, centerX, centerY);

        // Reset shadow
        ctx.shadowBlur = 0;

        // Accent lines
        ctx.strokeStyle = faction.secondaryColor;
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(centerX, centerY, emblemSize * 0.8, 0, Math.PI * 2);
        ctx.stroke();
    }

    /**
     * Draw faction border
     */
    drawFactionBorder(ctx, faction, size) {
        // Outer border
        ctx.strokeStyle = faction.color;
        ctx.lineWidth = 4;
        ctx.strokeRect(2, 2, size - 4, size - 4);

        // Inner accent border
        ctx.strokeStyle = faction.secondaryColor;
        ctx.lineWidth = 2;
        ctx.strokeRect(8, 8, size - 16, size - 16);
    }

    /**
     * Draw character background
     */
    drawCharacterBackground(ctx, character, size) {
        const faction = this.factionData[character.faction];
        
        // Atmospheric background
        const gradient = ctx.createLinearGradient(0, 0, size, size);
        gradient.addColorStop(0, character.primaryColor + '30');
        gradient.addColorStop(0.5, faction.color + '20');
        gradient.addColorStop(1, '#0a0e17');

        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, size, size);

        // Character aura
        const auraGradient = ctx.createRadialGradient(
            size/2, size/2, size/6,
            size/2, size/2, size/3
        );
        auraGradient.addColorStop(0, character.primaryColor + '60');
        auraGradient.addColorStop(1, 'transparent');

        ctx.fillStyle = auraGradient;
        ctx.fillRect(0, 0, size, size);
    }

    /**
     * Draw character silhouette
     */
    drawCharacterSilhouette(ctx, character, size) {
        const centerX = size / 2;
        const centerY = size / 2;
        const headSize = size * 0.25;

        ctx.fillStyle = character.primaryColor + '80';
        ctx.shadowColor = character.primaryColor;
        ctx.shadowBlur = 15;

        // Draw head shape based on character
        this.drawCharacterShape(ctx, character.shape, centerX, centerY - size * 0.1, headSize);

        // Body silhouette
        ctx.fillStyle = character.secondaryColor + '60';
        ctx.shadowBlur = 10;
        ctx.fillRect(centerX - headSize * 0.6, centerY + headSize * 0.4, headSize * 1.2, size * 0.3);

        ctx.shadowBlur = 0;
    }

    /**
     * Draw character features
     */
    drawCharacterFeatures(ctx, character, size) {
        const centerX = size / 2;
        const centerY = size / 2 - size * 0.1;
        const eyeColor = character.features.find(f => f.includes('-eyes'))?.replace('-eyes', '') || 'white';

        // Eyes with glow effect
        ctx.fillStyle = this.getColorFromName(eyeColor);
        ctx.shadowColor = this.getColorFromName(eyeColor);
        ctx.shadowBlur = 8;

        // Left eye
        ctx.beginPath();
        ctx.arc(centerX - size * 0.08, centerY - size * 0.02, size * 0.015, 0, Math.PI * 2);
        ctx.fill();

        // Right eye
        ctx.beginPath();
        ctx.arc(centerX + size * 0.08, centerY - size * 0.02, size * 0.015, 0, Math.PI * 2);
        ctx.fill();

        ctx.shadowBlur = 0;

        // Additional features based on character traits
        this.drawCharacterTraits(ctx, character, centerX, centerY, size);
    }

    /**
     * Draw faction affiliation indicator
     */
    drawFactionIndicator(ctx, character, size) {
        const faction = this.factionData[character.faction];
        if (!faction) return;

        // Small faction symbol in corner
        ctx.fillStyle = faction.color;
        ctx.font = `${size * 0.08}px Arial`;
        ctx.textAlign = 'right';
        ctx.textBaseline = 'bottom';
        ctx.fillText(faction.symbol, size - 20, size - 20);
    }

    /**
     * Draw various patterns
     */
    drawPattern(ctx, pattern, color, size) {
        ctx.strokeStyle = color + '20';
        ctx.lineWidth = 1;

        switch (pattern) {
            case 'grid':
                this.drawGridPattern(ctx, size);
                break;
            case 'waves':
                this.drawWavePattern(ctx, size);
                break;
            case 'spiral':
                this.drawSpiralPattern(ctx, size);
                break;
            case 'chaos':
                this.drawChaosPattern(ctx, size);
                break;
            case 'static':
                this.drawStaticPattern(ctx, size);
                break;
            case 'coins':
                this.drawCoinPattern(ctx, size);
                break;
        }
    }

    /**
     * Pattern drawing methods
     */
    drawGridPattern(ctx, size) {
        const spacing = size / 10;
        for (let i = 0; i < size; i += spacing) {
            ctx.beginPath();
            ctx.moveTo(i, 0);
            ctx.lineTo(i, size);
            ctx.moveTo(0, i);
            ctx.lineTo(size, i);
            ctx.stroke();
        }
    }

    drawWavePattern(ctx, size) {
        const waves = 5;
        const amplitude = size / 20;
        for (let w = 0; w < waves; w++) {
            ctx.beginPath();
            const y = (size / waves) * w;
            ctx.moveTo(0, y);
            for (let x = 0; x < size; x += 5) {
                const waveY = y + Math.sin(x / 20) * amplitude;
                ctx.lineTo(x, waveY);
            }
            ctx.stroke();
        }
    }

    drawSpiralPattern(ctx, size) {
        const centerX = size / 2;
        const centerY = size / 2;
        const maxRadius = size / 3;
        
        ctx.beginPath();
        for (let angle = 0; angle < Math.PI * 8; angle += 0.1) {
            const radius = (angle / (Math.PI * 8)) * maxRadius;
            const x = centerX + Math.cos(angle) * radius;
            const y = centerY + Math.sin(angle) * radius;
            if (angle === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }
        ctx.stroke();
    }

    drawChaosPattern(ctx, size) {
        for (let i = 0; i < 20; i++) {
            ctx.beginPath();
            ctx.moveTo(Math.random() * size, Math.random() * size);
            ctx.lineTo(Math.random() * size, Math.random() * size);
            ctx.stroke();
        }
    }

    drawStaticPattern(ctx, size) {
        for (let i = 0; i < 100; i++) {
            ctx.fillStyle = '#3de686' + Math.floor(Math.random() * 50).toString(16);
            ctx.fillRect(
                Math.random() * size, 
                Math.random() * size, 
                Math.random() * 3, 
                Math.random() * 3
            );
        }
    }

    drawCoinPattern(ctx, size) {
        const coins = 8;
        for (let i = 0; i < coins; i++) {
            const x = (Math.random() * size * 0.8) + size * 0.1;
            const y = (Math.random() * size * 0.8) + size * 0.1;
            const radius = size / 30;
            
            ctx.beginPath();
            ctx.arc(x, y, radius, 0, Math.PI * 2);
            ctx.stroke();
        }
    }

    /**
     * Draw character shapes
     */
    drawCharacterShape(ctx, shape, x, y, size) {
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
                this.drawStar(ctx, x, y, 5, size/2, size/4);
                break;
            case 'hexagon':
                this.drawHexagon(ctx, x, y, size/2);
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
     * Helper methods
     */
    drawStar(ctx, x, y, spikes, outerRadius, innerRadius) {
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

    drawHexagon(ctx, x, y, size) {
        const angle = Math.PI / 3;
        ctx.moveTo(x + size, y);
        
        for (let i = 1; i < 6; i++) {
            ctx.lineTo(x + size * Math.cos(angle * i), y + size * Math.sin(angle * i));
        }
        
        ctx.closePath();
    }

    drawCharacterTraits(ctx, character, centerX, centerY, size) {
        // Add special visual traits based on character features
        character.features.forEach(trait => {
            switch(trait) {
                case 'flame':
                    this.drawFlameEffect(ctx, centerX, centerY - size * 0.15, size * 0.1);
                    break;
                case 'corporate':
                    this.drawCorporateInsignia(ctx, centerX, centerY + size * 0.05, size * 0.05);
                    break;
                case 'navigator':
                    this.drawCompass(ctx, centerX, centerY + size * 0.08, size * 0.04);
                    break;
                case 'chaotic':
                    this.drawChaosSymbol(ctx, centerX, centerY + size * 0.06, size * 0.03);
                    break;
                case 'anonymous':
                    this.drawMask(ctx, centerX, centerY, size * 0.15);
                    break;
                case 'wealthy':
                    this.drawCrown(ctx, centerX, centerY - size * 0.18, size * 0.08);
                    break;
            }
        });
    }

    drawFlameEffect(ctx, x, y, size) {
        ctx.fillStyle = '#ff8c00';
        for (let i = 0; i < 5; i++) {
            const flameX = x + (Math.random() - 0.5) * size;
            const flameY = y + Math.random() * size;
            ctx.beginPath();
            ctx.arc(flameX, flameY, Math.random() * 3, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    drawCorporateInsignia(ctx, x, y, size) {
        ctx.strokeStyle = '#ff5757';
        ctx.lineWidth = 2;
        ctx.strokeRect(x - size/2, y - size/2, size, size);
        ctx.strokeRect(x - size/4, y - size/4, size/2, size/2);
    }

    drawCompass(ctx, x, y, size) {
        ctx.strokeStyle = '#00bdff';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(x, y, size, 0, Math.PI * 2);
        ctx.moveTo(x, y - size);
        ctx.lineTo(x, y + size);
        ctx.moveTo(x - size, y);
        ctx.lineTo(x + size, y);
        ctx.stroke();
    }

    drawChaosSymbol(ctx, x, y, size) {
        ctx.strokeStyle = '#8c52ff';
        ctx.lineWidth = 2;
        for (let i = 0; i < 6; i++) {
            const angle = (i / 6) * Math.PI * 2;
            ctx.beginPath();
            ctx.moveTo(x, y);
            ctx.lineTo(x + Math.cos(angle) * size, y + Math.sin(angle) * size);
            ctx.stroke();
        }
    }

    drawMask(ctx, x, y, size) {
        ctx.fillStyle = '#3de68660';
        ctx.beginPath();
        ctx.arc(x, y, size, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#3de686';
        ctx.lineWidth = 2;
        ctx.stroke();
    }

    drawCrown(ctx, x, y, size) {
        ctx.fillStyle = '#ffd700';
        ctx.beginPath();
        ctx.moveTo(x - size, y + size/2);
        ctx.lineTo(x - size/2, y - size/2);
        ctx.lineTo(x, y);
        ctx.lineTo(x + size/2, y - size/2);
        ctx.lineTo(x + size, y + size/2);
        ctx.closePath();
        ctx.fill();
    }

    getColorFromName(colorName) {
        const colors = {
            'red': '#ff5757',
            'orange': '#ff8c00',
            'blue': '#00bdff',
            'purple': '#8c52ff',
            'green': '#3de686',
            'gold': '#ffd700',
            'white': '#ffffff'
        };
        return colors[colorName] || colors.white;
    }
}

// Export for use in other scripts
window.AstradigitalAssetGenerator = AstradigitalAssetGenerator;

// Auto-initialize and generate assets when page loads
document.addEventListener('DOMContentLoaded', function() {
    const generator = new AstradigitalAssetGenerator();
    
    // Store generated assets in sessionStorage for performance
    if (!sessionStorage.getItem('astradigital-assets-generated')) {
        console.log('Generating Astradigital assets...');
        
        const factionLogos = generator.generateAllFactionLogos();
        const characterPortraits = generator.generateAllCharacterPortraits();
        
        sessionStorage.setItem('astradigital-faction-logos', JSON.stringify(factionLogos));
        sessionStorage.setItem('astradigital-character-portraits', JSON.stringify(characterPortraits));
        sessionStorage.setItem('astradigital-assets-generated', 'true');
        
        console.log('Astradigital assets generated successfully');
    }
    
    // Apply generated assets to page elements
    applyGeneratedAssets();
});

/**
 * Apply generated assets to page elements
 */
function applyGeneratedAssets() {
    const factionLogos = JSON.parse(sessionStorage.getItem('astradigital-faction-logos') || '{}');
    const characterPortraits = JSON.parse(sessionStorage.getItem('astradigital-character-portraits') || '{}');
    
    // Apply faction logos
    document.querySelectorAll('.faction-logo img, img[data-faction]').forEach(img => {
        const factionId = img.getAttribute('data-faction') || 
                         img.closest('[data-faction]')?.getAttribute('data-faction');
        
        if (factionId && factionLogos[factionId]) {
            img.src = factionLogos[factionId];
            img.classList.add('generated-asset');
        }
    });
    
    // Apply character portraits
    document.querySelectorAll('.character-portrait img, img[data-character]').forEach(img => {
        const characterId = img.getAttribute('data-character') ||
                           img.closest('[data-character]')?.getAttribute('data-character');
        
        if (characterId && characterPortraits[characterId]) {
            img.src = characterPortraits[characterId];
            img.classList.add('generated-asset');
        }
    });
}
