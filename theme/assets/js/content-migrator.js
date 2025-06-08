/**
 * Content Migration System for Astradigital Engine
 * Migrates JSON data to WordPress custom post types
 */

class AstradigitalContentMigrator {
    constructor() {
        this.wpRestBase = '/wp-json/astradigital/v1';
        this.migrationStatus = {
            factions: { total: 0, migrated: 0, errors: [] },
            characters: { total: 0, migrated: 0, errors: [] },
            territories: { total: 0, migrated: 0, errors: [] }
        };
        
        this.init();
    }

    /**
     * Initialize content migration system
     */
    init() {
        console.log('🔄 Initializing Content Migration System...');
        
        this.loadSourceData();
        this.setupMigrationInterface();
        
        console.log('✅ Content Migration System ready');
    }

    /**
     * Load source JSON data
     */
    async loadSourceData() {
        try {
            // Load faction data from existing JSON
            const response = await fetch('./astrdigital_divide_factions.json');
            this.sourceData = await response.json();
            
            console.log('📁 Source data loaded:', {
                factions: this.sourceData.factions?.length || 0,
                characters: this.countCharacters(),
                territories: this.sourceData.territories?.length || 0
            });
            
        } catch (error) {
            console.error('❌ Failed to load source data:', error);
        }
    }

    /**
     * Count total characters across all factions
     */
    countCharacters() {
        if (!this.sourceData?.factions) return 0;
        
        return this.sourceData.factions.reduce((total, faction) => {
            return total + (faction.characters?.length || 0);
        }, 0);
    }

    /**
     * Setup migration interface
     */
    setupMigrationInterface() {
        // Create migration control panel
        this.createMigrationPanel();
        
        // Add keyboard shortcut for migration panel
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.shiftKey && e.key === 'M') {
                e.preventDefault();
                this.toggleMigrationPanel();
            }
        });
    }

    /**
     * Create migration control panel
     */
    createMigrationPanel() {
        const panel = document.createElement('div');
        panel.id = 'migration-panel';
        panel.innerHTML = `
            <div class="migration-panel-header">
                <h3>🔄 Content Migration Control</h3>
                <button class="close-btn" onclick="this.parentElement.parentElement.style.display='none'">×</button>
            </div>
            <div class="migration-panel-content">
                <div class="migration-section">
                    <h4>📊 Source Data Status</h4>
                    <div id="source-status">Loading...</div>
                </div>
                
                <div class="migration-section">
                    <h4>🎯 Migration Actions</h4>
                    <div class="migration-buttons">
                        <button onclick="astraContentMigrator.migrateFactions()" class="migration-btn faction-btn">
                            Migrate Factions
                        </button>
                        <button onclick="astraContentMigrator.migrateCharacters()" class="migration-btn character-btn">
                            Migrate Characters
                        </button>
                        <button onclick="astraContentMigrator.migrateTerritories()" class="migration-btn territory-btn">
                            Migrate Territories
                        </button>
                        <button onclick="astraContentMigrator.migrateAll()" class="migration-btn migrate-all-btn">
                            🚀 Migrate All
                        </button>
                    </div>
                </div>
                
                <div class="migration-section">
                    <h4>📈 Migration Progress</h4>
                    <div id="migration-progress">
                        <div class="progress-item">
                            <span>Factions:</span>
                            <div class="progress-bar">
                                <div class="progress-fill faction-progress" style="width: 0%"></div>
                            </div>
                            <span class="progress-text">0 / 0</span>
                        </div>
                        <div class="progress-item">
                            <span>Characters:</span>
                            <div class="progress-bar">
                                <div class="progress-fill character-progress" style="width: 0%"></div>
                            </div>
                            <span class="progress-text">0 / 0</span>
                        </div>
                        <div class="progress-item">
                            <span>Territories:</span>
                            <div class="progress-bar">
                                <div class="progress-fill territory-progress" style="width: 0%"></div>
                            </div>
                            <span class="progress-text">0 / 0</span>
                        </div>
                    </div>
                </div>
                
                <div class="migration-section">
                    <h4>📝 Migration Log</h4>
                    <div id="migration-log" class="migration-log"></div>
                    <button onclick="astraContentMigrator.clearLog()" class="clear-log-btn">Clear Log</button>
                </div>
            </div>
        `;

        // Add styles
        const styles = document.createElement('style');
        styles.textContent = `
            #migration-panel {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 90%;
                max-width: 600px;
                max-height: 80vh;
                background: var(--astra-background, #0a0e17);
                border: 2px solid var(--astra-highlight, #4deeea);
                border-radius: 10px;
                z-index: 10000;
                display: none;
                overflow: hidden;
                box-shadow: 0 20px 40px rgba(0,0,0,0.5);
            }
            
            .migration-panel-header {
                background: var(--astra-secondary, #1a2b4d);
                color: var(--astra-text, #ffffff);
                padding: 15px 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid var(--astra-highlight, #4deeea);
            }
            
            .migration-panel-header h3 {
                margin: 0;
                font-size: 1.2rem;
            }
            
            .close-btn {
                background: none;
                border: none;
                color: var(--astra-text, #ffffff);
                font-size: 1.5rem;
                cursor: pointer;
                padding: 5px;
                border-radius: 3px;
                transition: background 0.2s ease;
            }
            
            .close-btn:hover {
                background: rgba(255,255,255,0.1);
            }
            
            .migration-panel-content {
                padding: 20px;
                max-height: 60vh;
                overflow-y: auto;
                color: var(--astra-text, #ffffff);
            }
            
            .migration-section {
                margin-bottom: 25px;
                padding-bottom: 20px;
                border-bottom: 1px solid rgba(77, 238, 234, 0.3);
            }
            
            .migration-section:last-child {
                border-bottom: none;
            }
            
            .migration-section h4 {
                margin: 0 0 15px 0;
                color: var(--astra-highlight, #4deeea);
                font-size: 1rem;
            }
            
            .migration-buttons {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
            }
            
            .migration-btn {
                padding: 12px 20px;
                border: 2px solid;
                border-radius: 6px;
                background: transparent;
                color: var(--astra-text, #ffffff);
                cursor: pointer;
                transition: all 0.3s ease;
                font-weight: bold;
            }
            
            .faction-btn {
                border-color: #ff5757;
            }
            
            .faction-btn:hover {
                background: #ff5757;
                color: #ffffff;
            }
            
            .character-btn {
                border-color: #00bdff;
            }
            
            .character-btn:hover {
                background: #00bdff;
                color: #ffffff;
            }
            
            .territory-btn {
                border-color: #8c52ff;
            }
            
            .territory-btn:hover {
                background: #8c52ff;
                color: #ffffff;
            }
            
            .migrate-all-btn {
                grid-column: 1 / -1;
                border-color: var(--astra-highlight, #4deeea);
                font-size: 1.1rem;
            }
            
            .migrate-all-btn:hover {
                background: var(--astra-highlight, #4deeea);
                color: var(--astra-background, #0a0e17);
            }
            
            .progress-item {
                display: flex;
                align-items: center;
                margin-bottom: 10px;
                gap: 15px;
            }
            
            .progress-item span:first-child {
                min-width: 80px;
                font-weight: bold;
            }
            
            .progress-bar {
                flex: 1;
                height: 20px;
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                overflow: hidden;
            }
            
            .progress-fill {
                height: 100%;
                transition: width 0.3s ease;
            }
            
            .faction-progress {
                background: #ff5757;
            }
            
            .character-progress {
                background: #00bdff;
            }
            
            .territory-progress {
                background: #8c52ff;
            }
            
            .progress-text {
                min-width: 60px;
                text-align: right;
                font-size: 0.9rem;
            }
            
            .migration-log {
                background: rgba(0,0,0,0.3);
                border: 1px solid rgba(77, 238, 234, 0.3);
                border-radius: 6px;
                padding: 15px;
                height: 150px;
                overflow-y: auto;
                font-family: monospace;
                font-size: 0.85rem;
                line-height: 1.4;
                margin-bottom: 10px;
            }
            
            .clear-log-btn {
                background: #dc3545;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 0.9rem;
            }
            
            .clear-log-btn:hover {
                background: #c82333;
            }
            
            .log-entry {
                margin-bottom: 5px;
                padding: 2px 0;
            }
            
            .log-success {
                color: #28a745;
            }
            
            .log-error {
                color: #dc3545;
            }
            
            .log-info {
                color: var(--astra-highlight, #4deeea);
            }
            
            .log-warning {
                color: #ffc107;
            }
        `;

        document.head.appendChild(styles);
        document.body.appendChild(panel);

        // Update status when data is loaded
        this.updateSourceStatus();
    }

    /**
     * Toggle migration panel visibility
     */
    toggleMigrationPanel() {
        const panel = document.getElementById('migration-panel');
        if (panel.style.display === 'none' || !panel.style.display) {
            panel.style.display = 'block';
            this.updateSourceStatus();
        } else {
            panel.style.display = 'none';
        }
    }

    /**
     * Update source data status display
     */
    updateSourceStatus() {
        const statusDiv = document.getElementById('source-status');
        if (!statusDiv) return;

        if (!this.sourceData) {
            statusDiv.innerHTML = '<span class="log-error">❌ No source data loaded</span>';
            return;
        }

        const factionCount = this.sourceData.factions?.length || 0;
        const characterCount = this.countCharacters();
        const territoryCount = this.sourceData.territories?.length || 0;

        statusDiv.innerHTML = `
            <div class="status-item">📦 Factions: ${factionCount}</div>
            <div class="status-item">👥 Characters: ${characterCount}</div>
            <div class="status-item">🗺️ Territories: ${territoryCount}</div>
            <div class="status-item">📅 Last Updated: ${new Date().toLocaleString()}</div>
        `;

        // Update migration counts
        this.migrationStatus.factions.total = factionCount;
        this.migrationStatus.characters.total = characterCount;
        this.migrationStatus.territories.total = territoryCount;
    }

    /**
     * Migrate all factions to WordPress
     */
    async migrateFactions() {
        if (!this.sourceData?.factions) {
            this.log('❌ No faction data to migrate', 'error');
            return;
        }

        this.log('🚀 Starting faction migration...', 'info');
        
        const factions = this.sourceData.factions;
        let successCount = 0;

        for (const faction of factions) {
            try {
                const result = await this.migrateSingleFaction(faction);
                if (result.success) {
                    successCount++;
                    this.log(`✅ Migrated faction: ${faction.name}`, 'success');
                } else {
                    this.log(`❌ Failed to migrate faction: ${faction.name} - ${result.error}`, 'error');
                    this.migrationStatus.factions.errors.push(`${faction.name}: ${result.error}`);
                }
            } catch (error) {
                this.log(`❌ Error migrating faction: ${faction.name} - ${error.message}`, 'error');
                this.migrationStatus.factions.errors.push(`${faction.name}: ${error.message}`);
            }

            this.migrationStatus.factions.migrated = successCount;
            this.updateProgress('faction');
        }

        this.log(`🎉 Faction migration complete: ${successCount}/${factions.length}`, successCount === factions.length ? 'success' : 'warning');
    }

    /**
     * Migrate a single faction
     */
    async migrateSingleFaction(faction) {
        // Prepare faction data for WordPress
        const postData = {
            title: faction.name,
            content: faction.description || '',
            meta: {
                faction_color: faction.color || '#4deeea',
                faction_secondary_color: faction.secondaryColor || '#7df3f0',
                faction_symbol: faction.symbol || '◊',
                faction_pattern: faction.pattern || 'spiral',
                faction_territory_ids: (faction.territories || []).join(','),
                faction_character_ids: (faction.characters || []).map(c => c.id).join(','),
                faction_status: faction.status || 'active',
                faction_influence_level: faction.influenceLevel || 'medium'
            }
        };

        try {
            const response = await fetch(`${this.wpRestBase}/factions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-WP-Nonce': this.getWPNonce()
                },
                body: JSON.stringify(postData)
            });

            const result = await response.json();
            
            if (response.ok) {
                return { success: true, data: result };
            } else {
                return { success: false, error: result.message || 'Unknown error' };
            }
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    /**
     * Migrate all characters to WordPress
     */
    async migrateCharacters() {
        if (!this.sourceData?.factions) {
            this.log('❌ No character data to migrate', 'error');
            return;
        }

        this.log('🚀 Starting character migration...', 'info');
        
        let allCharacters = [];
        this.sourceData.factions.forEach(faction => {
            if (faction.characters) {
                faction.characters.forEach(character => {
                    character.factionId = faction.id;
                    allCharacters.push(character);
                });
            }
        });

        let successCount = 0;

        for (const character of allCharacters) {
            try {
                const result = await this.migrateSingleCharacter(character);
                if (result.success) {
                    successCount++;
                    this.log(`✅ Migrated character: ${character.name}`, 'success');
                } else {
                    this.log(`❌ Failed to migrate character: ${character.name} - ${result.error}`, 'error');
                    this.migrationStatus.characters.errors.push(`${character.name}: ${result.error}`);
                }
            } catch (error) {
                this.log(`❌ Error migrating character: ${character.name} - ${error.message}`, 'error');
                this.migrationStatus.characters.errors.push(`${character.name}: ${error.message}`);
            }

            this.migrationStatus.characters.migrated = successCount;
            this.updateProgress('character');
        }

        this.log(`🎉 Character migration complete: ${successCount}/${allCharacters.length}`, successCount === allCharacters.length ? 'success' : 'warning');
    }

    /**
     * Migrate a single character
     */
    async migrateSingleCharacter(character) {
        const postData = {
            title: character.name,
            content: character.description || character.bio || '',
            meta: {
                character_faction_id: character.factionId,
                character_primary_color: character.primaryColor || '#4deeea',
                character_secondary_color: character.secondaryColor || '#7df3f0',
                character_shape: character.shape || 'circle',
                character_features: (character.features || []).join(','),
                character_role: character.role || 'member',
                character_status: character.status || 'active',
                character_influence: character.influence || 'medium'
            }
        };

        try {
            const response = await fetch(`${this.wpRestBase}/characters`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-WP-Nonce': this.getWPNonce()
                },
                body: JSON.stringify(postData)
            });

            const result = await response.json();
            
            if (response.ok) {
                return { success: true, data: result };
            } else {
                return { success: false, error: result.message || 'Unknown error' };
            }
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    /**
     * Migrate territories to WordPress
     */
    async migrateTerritories() {
        if (!this.sourceData?.territories) {
            this.log('❌ No territory data to migrate', 'error');
            return;
        }

        this.log('🚀 Starting territory migration...', 'info');
        
        const territories = this.sourceData.territories;
        let successCount = 0;

        for (const territory of territories) {
            try {
                const result = await this.migrateSingleTerritory(territory);
                if (result.success) {
                    successCount++;
                    this.log(`✅ Migrated territory: ${territory.name}`, 'success');
                } else {
                    this.log(`❌ Failed to migrate territory: ${territory.name} - ${result.error}`, 'error');
                    this.migrationStatus.territories.errors.push(`${territory.name}: ${result.error}`);
                }
            } catch (error) {
                this.log(`❌ Error migrating territory: ${territory.name} - ${error.message}`, 'error');
                this.migrationStatus.territories.errors.push(`${territory.name}: ${error.message}`);
            }

            this.migrationStatus.territories.migrated = successCount;
            this.updateProgress('territory');
        }

        this.log(`🎉 Territory migration complete: ${successCount}/${territories.length}`, successCount === territories.length ? 'success' : 'warning');
    }

    /**
     * Migrate a single territory
     */
    async migrateSingleTerritory(territory) {
        const postData = {
            title: territory.name,
            content: territory.description || '',
            meta: {
                territory_controlling_faction: territory.controllingFaction || '',
                territory_coordinates: territory.coordinates || '',
                territory_connections: (territory.connections || []).join(','),
                territory_type: territory.type || 'neutral',
                territory_resources: (territory.resources || []).join(','),
                territory_status: territory.status || 'stable'
            }
        };

        try {
            const response = await fetch(`${this.wpRestBase}/territories`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-WP-Nonce': this.getWPNonce()
                },
                body: JSON.stringify(postData)
            });

            const result = await response.json();
            
            if (response.ok) {
                return { success: true, data: result };
            } else {
                return { success: false, error: result.message || 'Unknown error' };
            }
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    /**
     * Migrate all content types
     */
    async migrateAll() {
        this.log('🚀 Starting complete migration...', 'info');
        
        await this.migrateFactions();
        await this.migrateCharacters();
        await this.migrateTerritories();
        
        const totalMigrated = this.migrationStatus.factions.migrated + 
                             this.migrationStatus.characters.migrated + 
                             this.migrationStatus.territories.migrated;
        
        const totalItems = this.migrationStatus.factions.total + 
                          this.migrationStatus.characters.total + 
                          this.migrationStatus.territories.total;
        
        this.log(`🎉 Complete migration finished: ${totalMigrated}/${totalItems} items migrated`, 'info');
    }

    /**
     * Update progress display
     */
    updateProgress(type) {
        const status = this.migrationStatus[`${type}s`];
        const percentage = status.total > 0 ? (status.migrated / status.total) * 100 : 0;
        
        const progressFill = document.querySelector(`.${type}-progress`);
        const progressText = progressFill?.parentElement.nextElementSibling;
        
        if (progressFill) {
            progressFill.style.width = `${percentage}%`;
        }
        
        if (progressText) {
            progressText.textContent = `${status.migrated} / ${status.total}`;
        }
    }

    /**
     * Log message to migration panel
     */
    log(message, type = 'info') {
        console.log(message);
        
        const logDiv = document.getElementById('migration-log');
        if (!logDiv) return;

        const timestamp = new Date().toLocaleTimeString();
        const logEntry = document.createElement('div');
        logEntry.className = `log-entry log-${type}`;
        logEntry.textContent = `[${timestamp}] ${message}`;
        
        logDiv.appendChild(logEntry);
        logDiv.scrollTop = logDiv.scrollHeight;
    }

    /**
     * Clear migration log
     */
    clearLog() {
        const logDiv = document.getElementById('migration-log');
        if (logDiv) {
            logDiv.innerHTML = '';
        }
    }

    /**
     * Get WordPress nonce for API requests
     */
    getWPNonce() {
        // In a real WordPress environment, this would be localized
        return window.astradigitalData?.nonce || '';
    }

    /**
     * Get migration status summary
     */
    getMigrationStatus() {
        return {
            ...this.migrationStatus,
            totalMigrated: this.migrationStatus.factions.migrated + 
                          this.migrationStatus.characters.migrated + 
                          this.migrationStatus.territories.migrated,
            totalItems: this.migrationStatus.factions.total + 
                       this.migrationStatus.characters.total + 
                       this.migrationStatus.territories.total
        };
    }

    /**
     * Export migration report
     */
    exportMigrationReport() {
        const status = this.getMigrationStatus();
        const report = {
            timestamp: new Date().toISOString(),
            status: status,
            errors: {
                factions: this.migrationStatus.factions.errors,
                characters: this.migrationStatus.characters.errors,
                territories: this.migrationStatus.territories.errors
            }
        };

        const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `astradigital-migration-report-${Date.now()}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        this.log('📄 Migration report exported', 'info');
    }
}

// Export for use in other scripts
window.AstradigitalContentMigrator = AstradigitalContentMigrator;

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    window.astraContentMigrator = new AstradigitalContentMigrator();
});
