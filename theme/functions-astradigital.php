<?php
/**
 * Astradigital Engine WordPress Integration
 * Custom post types and fields for dynamic content management
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

class AstradigitalWordPressIntegration {
    
    public function __construct() {
        add_action('init', array($this, 'register_custom_post_types'));
        add_action('init', array($this, 'register_custom_fields'));
        add_action('wp_enqueue_scripts', array($this, 'enqueue_astradigital_assets'));
        add_action('rest_api_init', array($this, 'register_rest_endpoints'));
        add_filter('the_content', array($this, 'enhance_astradigital_content'));
        add_shortcode('astradigital_factions', array($this, 'render_factions_shortcode'));
        add_shortcode('astradigital_characters', array($this, 'render_characters_shortcode'));
        add_shortcode('astradigital_map', array($this, 'render_map_shortcode'));
    }
    
    /**
     * Register custom post types for factions and characters
     */
    public function register_custom_post_types() {
        // Register Factions post type
        register_post_type('astra_faction', array(
            'labels' => array(
                'name' => 'Factions',
                'singular_name' => 'Faction',
                'add_new' => 'Add New Faction',
                'add_new_item' => 'Add New Faction',
                'edit_item' => 'Edit Faction',
                'new_item' => 'New Faction',
                'view_item' => 'View Faction',
                'search_items' => 'Search Factions',
                'not_found' => 'No factions found',
                'not_found_in_trash' => 'No factions found in trash'
            ),
            'public' => true,
            'has_archive' => true,
            'menu_icon' => 'dashicons-groups',
            'supports' => array('title', 'editor', 'thumbnail', 'excerpt', 'custom-fields'),
            'show_in_rest' => true,
            'rest_base' => 'astra-factions',
            'capability_type' => 'post',
            'rewrite' => array('slug' => 'factions')
        ));
        
        // Register Characters post type
        register_post_type('astra_character', array(
            'labels' => array(
                'name' => 'Characters',
                'singular_name' => 'Character',
                'add_new' => 'Add New Character',
                'add_new_item' => 'Add New Character',
                'edit_item' => 'Edit Character',
                'new_item' => 'New Character',
                'view_item' => 'View Character',
                'search_items' => 'Search Characters',
                'not_found' => 'No characters found',
                'not_found_in_trash' => 'No characters found in trash'
            ),
            'public' => true,
            'has_archive' => true,
            'menu_icon' => 'dashicons-admin-users',
            'supports' => array('title', 'editor', 'thumbnail', 'excerpt', 'custom-fields'),
            'show_in_rest' => true,
            'rest_base' => 'astra-characters',
            'capability_type' => 'post',
            'rewrite' => array('slug' => 'characters')
        ));
        
        // Register Territories post type
        register_post_type('astra_territory', array(
            'labels' => array(
                'name' => 'Territories',
                'singular_name' => 'Territory',
                'add_new' => 'Add New Territory',
                'add_new_item' => 'Add New Territory',
                'edit_item' => 'Edit Territory',
                'new_item' => 'New Territory',
                'view_item' => 'View Territory',
                'search_items' => 'Search Territories',
                'not_found' => 'No territories found',
                'not_found_in_trash' => 'No territories found in trash'
            ),
            'public' => true,
            'has_archive' => true,
            'menu_icon' => 'dashicons-location-alt',
            'supports' => array('title', 'editor', 'thumbnail', 'excerpt', 'custom-fields'),
            'show_in_rest' => true,
            'rest_base' => 'astra-territories',
            'capability_type' => 'post',
            'rewrite' => array('slug' => 'territories')
        ));
    }
    
    /**
     * Register custom fields using Advanced Custom Fields (ACF) or custom meta boxes
     */
    public function register_custom_fields() {
        // Faction custom fields
        add_action('add_meta_boxes', function() {
            add_meta_box(
                'astra_faction_details',
                'Faction Details',
                array($this, 'faction_details_meta_box'),
                'astra_faction',
                'normal',
                'high'
            );
            
            add_meta_box(
                'astra_character_details',
                'Character Details',
                array($this, 'character_details_meta_box'),
                'astra_character',
                'normal',
                'high'
            );
            
            add_meta_box(
                'astra_territory_details',
                'Territory Details',
                array($this, 'territory_details_meta_box'),
                'astra_territory',
                'normal',
                'high'
            );
        });
        
        // Save custom fields
        add_action('save_post', array($this, 'save_custom_fields'));
    }
    
    /**
     * Faction details meta box
     */
    public function faction_details_meta_box($post) {
        wp_nonce_field('astra_faction_nonce', 'astra_faction_nonce_field');
        
        $faction_color = get_post_meta($post->ID, '_faction_color', true);
        $faction_leader = get_post_meta($post->ID, '_faction_leader', true);
        $faction_territory = get_post_meta($post->ID, '_faction_territory', true);
        $faction_short_desc = get_post_meta($post->ID, '_faction_short_description', true);
        $faction_port = get_post_meta($post->ID, '_faction_port', true);
        $faction_port_desc = get_post_meta($post->ID, '_faction_port_description', true);
        
        echo '<table class="form-table">';
        echo '<tr><th><label for="faction_color">Faction Color</label></th>';
        echo '<td><input type="color" id="faction_color" name="faction_color" value="' . esc_attr($faction_color) . '" /></td></tr>';
        
        echo '<tr><th><label for="faction_leader">Leader</label></th>';
        echo '<td><input type="text" id="faction_leader" name="faction_leader" value="' . esc_attr($faction_leader) . '" class="regular-text" /></td></tr>';
        
        echo '<tr><th><label for="faction_territory">Territory</label></th>';
        echo '<td><input type="text" id="faction_territory" name="faction_territory" value="' . esc_attr($faction_territory) . '" class="regular-text" /></td></tr>';
        
        echo '<tr><th><label for="faction_short_desc">Short Description</label></th>';
        echo '<td><textarea id="faction_short_desc" name="faction_short_description" rows="3" class="large-text">' . esc_textarea($faction_short_desc) . '</textarea></td></tr>';
        
        echo '<tr><th><label for="faction_port">Port Name</label></th>';
        echo '<td><input type="text" id="faction_port" name="faction_port" value="' . esc_attr($faction_port) . '" class="regular-text" /></td></tr>';
        
        echo '<tr><th><label for="faction_port_desc">Port Description</label></th>';
        echo '<td><textarea id="faction_port_desc" name="faction_port_description" rows="4" class="large-text">' . esc_textarea($faction_port_desc) . '</textarea></td></tr>';
        
        echo '</table>';
    }
    
    /**
     * Character details meta box
     */
    public function character_details_meta_box($post) {
        wp_nonce_field('astra_character_nonce', 'astra_character_nonce_field');
        
        $character_faction = get_post_meta($post->ID, '_character_faction', true);
        $character_title = get_post_meta($post->ID, '_character_title', true);
        $character_abilities = get_post_meta($post->ID, '_character_abilities', true);
        $character_background = get_post_meta($post->ID, '_character_background', true);
        $character_quote = get_post_meta($post->ID, '_character_quote', true);
        
        // Get all factions for dropdown
        $factions = get_posts(array(
            'post_type' => 'astra_faction',
            'numberposts' => -1,
            'post_status' => 'publish'
        ));
        
        echo '<table class="form-table">';
        echo '<tr><th><label for="character_faction">Faction</label></th>';
        echo '<td><select id="character_faction" name="character_faction">';
        echo '<option value="">Select Faction</option>';
        foreach ($factions as $faction) {
            $selected = ($character_faction == $faction->ID) ? 'selected' : '';
            echo '<option value="' . $faction->ID . '" ' . $selected . '>' . esc_html($faction->post_title) . '</option>';
        }
        echo '</select></td></tr>';
        
        echo '<tr><th><label for="character_title">Title/Role</label></th>';
        echo '<td><input type="text" id="character_title" name="character_title" value="' . esc_attr($character_title) . '" class="regular-text" /></td></tr>';
        
        echo '<tr><th><label for="character_abilities">Abilities</label></th>';
        echo '<td><textarea id="character_abilities" name="character_abilities" rows="3" class="large-text">' . esc_textarea($character_abilities) . '</textarea></td></tr>';
        
        echo '<tr><th><label for="character_background">Background</label></th>';
        echo '<td><textarea id="character_background" name="character_background" rows="4" class="large-text">' . esc_textarea($character_background) . '</textarea></td></tr>';
        
        echo '<tr><th><label for="character_quote">Signature Quote</label></th>';
        echo '<td><input type="text" id="character_quote" name="character_quote" value="' . esc_attr($character_quote) . '" class="large-text" /></td></tr>';
        
        echo '</table>';
    }
    
    /**
     * Territory details meta box
     */
    public function territory_details_meta_box($post) {
        wp_nonce_field('astra_territory_nonce', 'astra_territory_nonce_field');
        
        $territory_controlling_faction = get_post_meta($post->ID, '_territory_controlling_faction', true);
        $territory_coordinates = get_post_meta($post->ID, '_territory_coordinates', true);
        $territory_connections = get_post_meta($post->ID, '_territory_connections', true);
        $territory_type = get_post_meta($post->ID, '_territory_type', true);
        
        // Get all factions for dropdown
        $factions = get_posts(array(
            'post_type' => 'astra_faction',
            'numberposts' => -1,
            'post_status' => 'publish'
        ));
        
        echo '<table class="form-table">';
        echo '<tr><th><label for="territory_controlling_faction">Controlling Faction</label></th>';
        echo '<td><select id="territory_controlling_faction" name="territory_controlling_faction">';
        echo '<option value="">No Faction Control</option>';
        foreach ($factions as $faction) {
            $selected = ($territory_controlling_faction == $faction->ID) ? 'selected' : '';
            echo '<option value="' . $faction->ID . '" ' . $selected . '>' . esc_html($faction->post_title) . '</option>';
        }
        echo '</select></td></tr>';
        
        echo '<tr><th><label for="territory_type">Territory Type</label></th>';
        echo '<td><select id="territory_type" name="territory_type">';
        $types = array('waters', 'islands', 'highways', 'pathways', 'triangle', 'archipelago');
        foreach ($types as $type) {
            $selected = ($territory_type == $type) ? 'selected' : '';
            echo '<option value="' . $type . '" ' . $selected . '>' . ucfirst($type) . '</option>';
        }
        echo '</select></td></tr>';
        
        echo '<tr><th><label for="territory_coordinates">SVG Coordinates (Path)</label></th>';
        echo '<td><textarea id="territory_coordinates" name="territory_coordinates" rows="3" class="large-text" placeholder="M100,100 L300,50 L400,150 Z">' . esc_textarea($territory_coordinates) . '</textarea></td></tr>';
        
        echo '<tr><th><label for="territory_connections">Connected Territories (IDs, comma-separated)</label></th>';
        echo '<td><input type="text" id="territory_connections" name="territory_connections" value="' . esc_attr($territory_connections) . '" class="regular-text" placeholder="territory-1, territory-2" /></td></tr>';
        
        echo '</table>';
    }
    
    /**
     * Save custom fields
     */
    public function save_custom_fields($post_id) {
        // Check if this is an autosave
        if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) return;
        
        // Verify nonces
        if (isset($_POST['astra_faction_nonce_field']) && 
            wp_verify_nonce($_POST['astra_faction_nonce_field'], 'astra_faction_nonce')) {
            
            // Save faction fields
            $fields = array(
                'faction_color', 'faction_leader', 'faction_territory',
                'faction_short_description', 'faction_port', 'faction_port_description'
            );
            
            foreach ($fields as $field) {
                if (isset($_POST[$field])) {
                    update_post_meta($post_id, '_' . $field, sanitize_text_field($_POST[$field]));
                }
            }
        }
        
        if (isset($_POST['astra_character_nonce_field']) && 
            wp_verify_nonce($_POST['astra_character_nonce_field'], 'astra_character_nonce')) {
            
            // Save character fields
            $fields = array(
                'character_faction', 'character_title', 'character_abilities',
                'character_background', 'character_quote'
            );
            
            foreach ($fields as $field) {
                if (isset($_POST[$field])) {
                    update_post_meta($post_id, '_' . $field, sanitize_text_field($_POST[$field]));
                }
            }
        }
        
        if (isset($_POST['astra_territory_nonce_field']) && 
            wp_verify_nonce($_POST['astra_territory_nonce_field'], 'astra_territory_nonce')) {
            
            // Save territory fields
            $fields = array(
                'territory_controlling_faction', 'territory_coordinates',
                'territory_connections', 'territory_type'
            );
            
            foreach ($fields as $field) {
                if (isset($_POST[$field])) {
                    update_post_meta($post_id, '_' . $field, sanitize_text_field($_POST[$field]));
                }
            }
        }
    }
    
    /**
     * Enqueue Astradigital assets
     */
    public function enqueue_astradigital_assets() {
        // Check if we're on an Astradigital page
        if (is_page_template('page-astradigital.php') || 
            is_post_type_archive(array('astra_faction', 'astra_character', 'astra_territory')) ||
            is_singular(array('astra_faction', 'astra_character', 'astra_territory'))) {
            
            wp_enqueue_style('astradigital-css', 
                get_template_directory_uri() . '/assets/css/astradigital.css', 
                array(), '1.0.0');
            
            wp_enqueue_style('astradigital-map-css', 
                get_template_directory_uri() . '/assets/css/map.css', 
                array('astradigital-css'), '1.0.0');
            
            wp_enqueue_script('astradigital-asset-generator', 
                get_template_directory_uri() . '/assets/js/asset-generator.js', 
                array(), '1.0.0', true);
            
            wp_enqueue_script('astradigital-js', 
                get_template_directory_uri() . '/assets/js/astradigital.js', 
                array('jquery', 'astradigital-asset-generator'), '1.0.0', true);
            
            wp_enqueue_script('astradigital-map-js', 
                get_template_directory_uri() . '/assets/js/map.js', 
                array('astradigital-js'), '1.0.0', true);
            
            // Localize script with REST API data
            wp_localize_script('astradigital-js', 'astradigital_ajax', array(
                'ajax_url' => admin_url('admin-ajax.php'),
                'rest_url' => rest_url('wp/v2/'),
                'nonce' => wp_create_nonce('wp_rest'),
                'faction_endpoint' => rest_url('wp/v2/astra-factions'),
                'character_endpoint' => rest_url('wp/v2/astra-characters'),
                'territory_endpoint' => rest_url('wp/v2/astra-territories')
            ));
        }
    }
    
    /**
     * Register REST API endpoints for dynamic content
     */
    public function register_rest_endpoints() {
        register_rest_route('astradigital/v1', '/map-data', array(
            'methods' => 'GET',
            'callback' => array($this, 'get_map_data'),
            'permission_callback' => '__return_true'
        ));
        
        register_rest_route('astradigital/v1', '/faction/(?P<id>\d+)', array(
            'methods' => 'GET',
            'callback' => array($this, 'get_faction_details'),
            'permission_callback' => '__return_true'
        ));
        
        register_rest_route('astradigital/v1', '/character/(?P<id>\d+)', array(
            'methods' => 'GET',
            'callback' => array($this, 'get_character_details'),
            'permission_callback' => '__return_true'
        ));
    }
    
    /**
     * Get comprehensive map data for JavaScript
     */
    public function get_map_data() {
        $factions = get_posts(array(
            'post_type' => 'astra_faction',
            'numberposts' => -1,
            'post_status' => 'publish'
        ));
        
        $territories = get_posts(array(
            'post_type' => 'astra_territory',
            'numberposts' => -1,
            'post_status' => 'publish'
        ));
        
        $characters = get_posts(array(
            'post_type' => 'astra_character',
            'numberposts' => -1,
            'post_status' => 'publish'
        ));
        
        $map_data = array(
            'factions' => array(),
            'territories' => array(),
            'characters' => array()
        );
        
        // Format faction data
        foreach ($factions as $faction) {
            $map_data['factions'][] = array(
                'id' => $faction->ID,
                'slug' => $faction->post_name,
                'name' => $faction->post_title,
                'description' => $faction->post_content,
                'short_description' => get_post_meta($faction->ID, '_faction_short_description', true),
                'color' => get_post_meta($faction->ID, '_faction_color', true),
                'leader' => get_post_meta($faction->ID, '_faction_leader', true),
                'territory' => get_post_meta($faction->ID, '_faction_territory', true),
                'port' => get_post_meta($faction->ID, '_faction_port', true),
                'port_description' => get_post_meta($faction->ID, '_faction_port_description', true),
                'logo' => get_the_post_thumbnail_url($faction->ID, 'medium'),
                'background' => get_the_post_thumbnail_url($faction->ID, 'large')
            );
        }
        
        // Format territory data
        foreach ($territories as $territory) {
            $connections = get_post_meta($territory->ID, '_territory_connections', true);
            $connections_array = $connections ? array_map('trim', explode(',', $connections)) : array();
            
            $map_data['territories'][] = array(
                'id' => $territory->post_name,
                'name' => $territory->post_title,
                'description' => $territory->post_content,
                'coordinates' => get_post_meta($territory->ID, '_territory_coordinates', true),
                'controlling_faction' => get_post_meta($territory->ID, '_territory_controlling_faction', true),
                'type' => get_post_meta($territory->ID, '_territory_type', true),
                'connections' => $connections_array
            );
        }
        
        // Format character data
        foreach ($characters as $character) {
            $faction_id = get_post_meta($character->ID, '_character_faction', true);
            $faction = $faction_id ? get_post($faction_id) : null;
            
            $map_data['characters'][] = array(
                'id' => $character->ID,
                'slug' => $character->post_name,
                'name' => $character->post_title,
                'description' => $character->post_content,
                'title' => get_post_meta($character->ID, '_character_title', true),
                'abilities' => get_post_meta($character->ID, '_character_abilities', true),
                'background' => get_post_meta($character->ID, '_character_background', true),
                'quote' => get_post_meta($character->ID, '_character_quote', true),
                'faction' => $faction ? array(
                    'id' => $faction->ID,
                    'name' => $faction->post_title,
                    'color' => get_post_meta($faction->ID, '_faction_color', true)
                ) : null,
                'portrait' => get_the_post_thumbnail_url($character->ID, 'medium')
            );
        }
        
        return rest_ensure_response($map_data);
    }
    
    /**
     * Get detailed faction information
     */
    public function get_faction_details($request) {
        $faction_id = $request['id'];
        $faction = get_post($faction_id);
        
        if (!$faction || $faction->post_type !== 'astra_faction') {
            return new WP_Error('faction_not_found', 'Faction not found', array('status' => 404));
        }
        
        $faction_data = array(
            'id' => $faction->ID,
            'name' => $faction->post_title,
            'description' => $faction->post_content,
            'short_description' => get_post_meta($faction->ID, '_faction_short_description', true),
            'color' => get_post_meta($faction->ID, '_faction_color', true),
            'leader' => get_post_meta($faction->ID, '_faction_leader', true),
            'territory' => get_post_meta($faction->ID, '_faction_territory', true),
            'port' => get_post_meta($faction->ID, '_faction_port', true),
            'port_description' => get_post_meta($faction->ID, '_faction_port_description', true),
            'logo' => get_the_post_thumbnail_url($faction->ID, 'medium'),
            'background' => get_the_post_thumbnail_url($faction->ID, 'large')
        );
        
        return rest_ensure_response($faction_data);
    }
    
    /**
     * Get detailed character information
     */
    public function get_character_details($request) {
        $character_id = $request['id'];
        $character = get_post($character_id);
        
        if (!$character || $character->post_type !== 'astra_character') {
            return new WP_Error('character_not_found', 'Character not found', array('status' => 404));
        }
        
        $faction_id = get_post_meta($character->ID, '_character_faction', true);
        $faction = $faction_id ? get_post($faction_id) : null;
        
        $character_data = array(
            'id' => $character->ID,
            'name' => $character->post_title,
            'description' => $character->post_content,
            'title' => get_post_meta($character->ID, '_character_title', true),
            'abilities' => get_post_meta($character->ID, '_character_abilities', true),
            'background' => get_post_meta($character->ID, '_character_background', true),
            'quote' => get_post_meta($character->ID, '_character_quote', true),
            'faction' => $faction ? array(
                'id' => $faction->ID,
                'name' => $faction->post_title,
                'color' => get_post_meta($faction->ID, '_faction_color', true)
            ) : null,
            'portrait' => get_the_post_thumbnail_url($character->ID, 'medium')
        );
        
        return rest_ensure_response($character_data);
    }
    
    /**
     * Enhance content with Astradigital features
     */
    public function enhance_astradigital_content($content) {
        if (is_singular(array('astra_faction', 'astra_character', 'astra_territory'))) {
            // Add interactive elements to single post pages
            $enhanced_content = '<div class="astradigital-content">';
            $enhanced_content .= $content;
            $enhanced_content .= '<div class="astradigital-actions">';
            
            if (is_singular('astra_faction')) {
                $enhanced_content .= '<button class="map-nav-btn" onclick="navigateToMapTerritory(\'' . get_post_field('post_name') . '\')">🗺️ View Territory on Map</button>';
            } elseif (is_singular('astra_character')) {
                $faction_id = get_post_meta(get_the_ID(), '_character_faction', true);
                if ($faction_id) {
                    $faction = get_post($faction_id);
                    $enhanced_content .= '<button class="map-nav-btn" onclick="navigateToMapTerritory(\'' . $faction->post_name . '\')">🗺️ View Home Territory</button>';
                }
            }
            
            $enhanced_content .= '</div></div>';
            return $enhanced_content;
        }
        
        return $content;
    }
    
    /**
     * Factions shortcode
     */
    public function render_factions_shortcode($atts) {
        $atts = shortcode_atts(array(
            'limit' => -1,
            'layout' => 'grid'
        ), $atts);
        
        ob_start();
        include get_template_directory() . '/templates/parts/content-factions.php';
        return ob_get_clean();
    }
    
    /**
     * Characters shortcode
     */
    public function render_characters_shortcode($atts) {
        $atts = shortcode_atts(array(
            'limit' => -1,
            'faction' => '',
            'layout' => 'grid'
        ), $atts);
        
        ob_start();
        include get_template_directory() . '/templates/parts/content-characters.php';
        return ob_get_clean();
    }
    
    /**
     * Map shortcode
     */
    public function render_map_shortcode($atts) {
        $atts = shortcode_atts(array(
            'height' => '600px',
            'controls' => 'true'
        ), $atts);
        
        ob_start();
        echo '<div class="astradigital-map-container" style="height: ' . esc_attr($atts['height']) . '">';
        include get_template_directory() . '/templates/parts/content-map.php';
        echo '</div>';
        return ob_get_clean();
    }
}

// Initialize the WordPress integration
new AstradigitalWordPressIntegration();

/**
 * Template loader for Astradigital pages
 */
function astradigital_template_loader($template) {
    if (is_page_template('page-astradigital.php')) {
        $new_template = locate_template(array('page-astradigital.php'));
        if (!empty($new_template)) {
            return $new_template;
        }
    }
    
    return $template;
}
add_filter('template_include', 'astradigital_template_loader');

/**
 * Add Astradigital admin menu
 */
function astradigital_admin_menu() {
    add_menu_page(
        'Astradigital Engine',
        'Astradigital',
        'manage_options',
        'astradigital-engine',
        'astradigital_admin_page',
        'dashicons-location',
        30
    );
    
    add_submenu_page(
        'astradigital-engine',
        'Import/Export',
        'Import/Export',
        'manage_options',
        'astradigital-import-export',
        'astradigital_import_export_page'
    );
}
add_action('admin_menu', 'astradigital_admin_menu');

/**
 * Astradigital admin page
 */
function astradigital_admin_page() {
    echo '<div class="wrap">';
    echo '<h1>Astradigital Engine</h1>';
    echo '<p>Manage your Astradigital Ocean content, factions, characters, and territories.</p>';
    
    // Display stats
    $faction_count = wp_count_posts('astra_faction')->publish;
    $character_count = wp_count_posts('astra_character')->publish;
    $territory_count = wp_count_posts('astra_territory')->publish;
    
    echo '<div class="astradigital-admin-stats">';
    echo '<div class="stats-grid">';
    echo '<div class="stat-card"><h3>' . $faction_count . '</h3><p>Factions</p></div>';
    echo '<div class="stat-card"><h3>' . $character_count . '</h3><p>Characters</p></div>';
    echo '<div class="stat-card"><h3>' . $territory_count . '</h3><p>Territories</p></div>';
    echo '</div>';
    echo '</div>';
    
    echo '<h2>Quick Actions</h2>';
    echo '<p><a href="' . admin_url('post-new.php?post_type=astra_faction') . '" class="button button-primary">Add New Faction</a> ';
    echo '<a href="' . admin_url('post-new.php?post_type=astra_character') . '" class="button button-primary">Add New Character</a> ';
    echo '<a href="' . admin_url('post-new.php?post_type=astra_territory') . '" class="button button-primary">Add New Territory</a></p>';
    
    echo '</div>';
}

/**
 * Import/Export page
 */
function astradigital_import_export_page() {
    echo '<div class="wrap">';
    echo '<h1>Astradigital Import/Export</h1>';
    echo '<p>Import or export Astradigital content in JSON format.</p>';
    
    if (isset($_POST['export_data'])) {
        $integration = new AstradigitalWordPressIntegration();
        $map_data = $integration->get_map_data();
        
        header('Content-Type: application/json');
        header('Content-Disposition: attachment; filename="astradigital-export-' . date('Y-m-d') . '.json"');
        echo json_encode($map_data->data, JSON_PRETTY_PRINT);
        exit;
    }
    
    echo '<form method="post">';
    echo '<h2>Export Data</h2>';
    echo '<p>Export all Astradigital content as JSON:</p>';
    echo '<p><input type="submit" name="export_data" value="Export JSON" class="button button-primary" /></p>';
    echo '</form>';
    
    echo '<h2>Import Data</h2>';
    echo '<p>Import Astradigital content from JSON file:</p>';
    echo '<form method="post" enctype="multipart/form-data">';
    echo '<p><input type="file" name="import_file" accept=".json" /></p>';
    echo '<p><input type="submit" name="import_data" value="Import JSON" class="button button-primary" /></p>';
    echo '</form>';
    
    echo '</div>';
}
?>
