<?php
/**
 * The Elidoras Codex functions and definitions
 *
 * @package The_Elidoras_Codex
 */

if (!defined('ABSPATH')) {
    exit; // Exit if accessed directly
}

/**
 * Define theme constants
 */
define('TEC_THEME_DIR', get_template_directory());
define('TEC_THEME_URI', get_template_directory_uri());
define('TEC_VERSION', '1.0.0');

/**
 * Theme setup
 */
function tec_setup() {
    /*
     * Make theme available for translation.
     */
    load_theme_textdomain('tec-theme', TEC_THEME_DIR . '/languages');

    /*
     * Register navigation menus
     */
    register_nav_menus(array(
        'primary' => esc_html__('Primary Menu', 'tec-theme'),
        'footer-universe' => esc_html__('Footer Universe Menu', 'tec-theme'),
        'footer-participate' => esc_html__('Footer Participate Menu', 'tec-theme'),
        'footer-explore' => esc_html__('Footer Explore Menu', 'tec-theme'),
        'mobile' => esc_html__('Mobile Menu', 'tec-theme'),
    ));

    /*
     * Let WordPress manage the document title.
     */
    add_theme_support('title-tag');

    /*
     * Enable support for Post Thumbnails on posts and pages.
     */
    add_theme_support('post-thumbnails');

    // Set up image sizes for factions and entities
    add_image_size('faction-hero', 1920, 800, true);
    add_image_size('faction-logo', 500, 500, false);
    add_image_size('entity-portrait', 400, 600, true);

    /*
     * Switch default core markup to output valid HTML5.
     */
    add_theme_support(
        'html5',
        array(
            'search-form',
            'comment-form',
            'comment-list',
            'gallery',
            'caption',
            'style',
            'script',
        )
    );

    // Add theme support for selective refresh for widgets.
    add_theme_support('customize-selective-refresh-widgets');

    /**
     * Add support for core custom logo.
     */
    add_theme_support(
        'custom-logo',
        array(
            'height' => 250,
            'width' => 250,
            'flex-width' => true,
            'flex-height' => true,
        )
    );

    // Add support for block styles
    add_theme_support('wp-block-styles');

    // Add support for full and wide align images
    add_theme_support('align-wide');

    // Add support for editor styles
    add_theme_support('editor-styles');

    // Editor styles
    add_editor_style('theme/assets/css/editor-style.css');
}
add_action('after_setup_theme', 'tec_setup');

/**
 * Enqueue scripts and styles
 */
function tec_scripts() {
    // Enqueue main stylesheet
    wp_enqueue_style('tec-style', get_stylesheet_uri(), array(), TEC_VERSION);
    
    // Enqueue Google Fonts
    wp_enqueue_style('tec-google-fonts', 'https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&display=swap', array(), TEC_VERSION);
    
    // Enqueue Astradigital specific CSS for the page template
    if (is_page_template('templates/page-astradigital.php')) {
        wp_enqueue_style('tec-astradigital', TEC_THEME_URI . '/assets/css/astradigital.css', array(), TEC_VERSION);
        wp_enqueue_script('tec-astradigital-js', TEC_THEME_URI . '/assets/js/astradigital.js', array('jquery'), TEC_VERSION, true);
    }
    
    // Enqueue custom scripts
    wp_enqueue_script('tec-navigation', TEC_THEME_URI . '/assets/js/main.js', array('jquery'), TEC_VERSION, true);

    // Enqueue Tailwind CSS for front page
    if (is_front_page()) {
        wp_enqueue_script('tailwind-css', 'https://cdn.tailwindcss.com', array(), null, false);
        wp_enqueue_style('font-awesome', 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css', array(), '6.4.0');
        wp_enqueue_style('google-fonts', 'https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600;700&display=swap', array(), null);
    }
    
    // Enqueue JavaScript for theme functionality
    wp_enqueue_script('tec-main', get_template_directory_uri() . '/assets/js/main.js', array('jquery'), '1.0.0', true);
    
    // Localize script for AJAX
    wp_localize_script('tec-main', 'tec_ajax', array(
        'ajax_url' => admin_url('admin-ajax.php'),
        'nonce' => wp_create_nonce('tec_nonce'),
        'home_url' => home_url(),
    ));

    if (is_singular() && comments_open() && get_option('thread_comments')) {
        wp_enqueue_script('comment-reply');
    }
}
add_action('wp_enqueue_scripts', 'tec_scripts');

/**
 * Register widget area
 */
function tec_widgets_init() {
    register_sidebar(
        array(
            'name'          => esc_html__('Sidebar', 'tec-theme'),
            'id'            => 'sidebar-1',
            'description'   => esc_html__('Add widgets here.', 'tec-theme'),
            'before_widget' => '<section id="%1$s" class="widget %2$s">',
            'after_widget'  => '</section>',
            'before_title'  => '<h2 class="widget-title">',
            'after_title'   => '</h2>',
        )
    );

    register_sidebar(
        array(
            'name'          => esc_html__('Footer Widget Area', 'tec-theme'),
            'id'            => 'footer-1',
            'description'   => esc_html__('Add footer widgets here.', 'tec-theme'),
            'before_widget' => '<section id="%1$s" class="widget %2$s">',
            'after_widget'  => '</section>',
            'before_title'  => '<h2 class="widget-title">',
            'after_title'   => '</h2>',
        )
    );
}
add_action('widgets_init', 'tec_widgets_init');

/**
 * Custom Post Types for Factions and Entities
 */
function tec_register_post_types() {
    // Register Factions post type
    register_post_type('faction',
        array(
            'labels' => array(
                'name' => __('Factions', 'tec-theme'),
                'singular_name' => __('Faction', 'tec-theme'),
                'menu_name' => __('Factions', 'tec-theme'),
            ),
            'public' => true,
            'has_archive' => true,
            'rewrite' => array('slug' => 'factions'),
            'menu_icon' => 'dashicons-groups',
            'supports' => array('title', 'editor', 'thumbnail', 'excerpt', 'custom-fields'),
            'show_in_rest' => true,
        )
    );

    // Register Entities post type (for characters, algorithms, etc.)
    register_post_type('entity',
        array(
            'labels' => array(
                'name' => __('Entities', 'tec-theme'),
                'singular_name' => __('Entity', 'tec-theme'),
                'menu_name' => __('Entities', 'tec-theme'),
            ),
            'public' => true,
            'has_archive' => true,
            'rewrite' => array('slug' => 'entities'),
            'menu_icon' => 'dashicons-businessman',
            'supports' => array('title', 'editor', 'thumbnail', 'excerpt', 'custom-fields'),
            'show_in_rest' => true,
        )
    );

    // Register Pathways post type (for routes, highways, etc.)
    register_post_type('pathway',
        array(
            'labels' => array(
                'name' => __('Pathways', 'tec-theme'),
                'singular_name' => __('Pathway', 'tec-theme'),
                'menu_name' => __('Pathways', 'tec-theme'),
            ),
            'public' => true,
            'has_archive' => true,
            'rewrite' => array('slug' => 'pathways'),
            'menu_icon' => 'dashicons-networking',
            'supports' => array('title', 'editor', 'thumbnail', 'excerpt', 'custom-fields'),
            'show_in_rest' => true,
        )
    );
}
add_action('init', 'tec_register_post_types');

/**
 * Add meta boxes for faction details
 */
function tec_faction_meta_boxes() {
    add_meta_box(
        'faction_details',
        __('Faction Details', 'tec-theme'),
        'tec_faction_details_callback',
        'faction',
        'normal',
        'high'
    );
}
add_action('add_meta_boxes', 'tec_faction_meta_boxes');

/**
 * Faction details meta box callback
 */
function tec_faction_details_callback($post) {
    wp_nonce_field('tec_faction_save', 'tec_faction_nonce');

    $faction_color = get_post_meta($post->ID, '_faction_color', true);
    $faction_leader = get_post_meta($post->ID, '_faction_leader', true);
    $faction_territory = get_post_meta($post->ID, '_faction_territory', true);

    ?>
    <p>
        <label for="faction_color"><?php _e('Faction Color (Hex code)', 'tec-theme'); ?></label>
        <input type="text" id="faction_color" name="faction_color" value="<?php echo esc_attr($faction_color); ?>" />
    </p>
    <p>
        <label for="faction_leader"><?php _e('Faction Leader', 'tec-theme'); ?></label>
        <input type="text" id="faction_leader" name="faction_leader" value="<?php echo esc_attr($faction_leader); ?>" />
    </p>
    <p>
        <label for="faction_territory"><?php _e('Territory in Astradigital Ocean', 'tec-theme'); ?></label>
        <textarea id="faction_territory" name="faction_territory"><?php echo esc_textarea($faction_territory); ?></textarea>
    </p>
    <?php
}

/**
 * Save faction meta box data
 */
function tec_save_faction_meta($post_id) {
    if (!isset($_POST['tec_faction_nonce']) || !wp_verify_nonce($_POST['tec_faction_nonce'], 'tec_faction_save')) {
        return;
    }

    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) {
        return;
    }

    if (!current_user_can('edit_post', $post_id)) {
        return;
    }

    if (isset($_POST['faction_color'])) {
        update_post_meta($post_id, '_faction_color', sanitize_text_field($_POST['faction_color']));
    }

    if (isset($_POST['faction_leader'])) {
        update_post_meta($post_id, '_faction_leader', sanitize_text_field($_POST['faction_leader']));
    }

    if (isset($_POST['faction_territory'])) {
        update_post_meta($post_id, '_faction_territory', sanitize_textarea_field($_POST['faction_territory']));
    }
}
add_action('save_post_faction', 'tec_save_faction_meta');

/**
 * Handle TEC Cartel signup form submission
 */
function handle_tec_cartel_signup() {
    // Verify nonce
    if (!wp_verify_nonce($_POST['tec_signup_nonce'], 'tec_cartel_signup_nonce')) {
        wp_die('Security check failed');
    }
    
    // Sanitize form data
    $user_name = sanitize_text_field($_POST['user_name']);
    $user_email = sanitize_email($_POST['user_email']);
    $faction_allegiance = sanitize_text_field($_POST['faction_allegiance']);
    $terms_agreement = isset($_POST['terms_agreement']) ? true : false;
    
    // Validate required fields
    if (empty($user_name) || empty($user_email) || !$terms_agreement) {
        wp_redirect(home_url('/?signup=error&msg=missing_fields'));
        exit;
    }
    
    // Store signup data (you can integrate with your preferred email service here)
    $signup_data = array(
        'name' => $user_name,
        'email' => $user_email,
        'faction' => $faction_allegiance,
        'date' => current_time('mysql'),
        'ip' => $_SERVER['REMOTE_ADDR']
    );
    
    // Option 1: Store in WordPress database
    $existing_signups = get_option('tec_cartel_signups', array());
    $existing_signups[] = $signup_data;
    update_option('tec_cartel_signups', $existing_signups);
    
    // Option 2: Send notification email to admin
    $admin_email = get_option('admin_email');
    $subject = 'New TEC Cartel Signup: ' . $user_name;
    $message = "New Cartel signup received:\n\n";
    $message .= "Name: " . $user_name . "\n";
    $message .= "Email: " . $user_email . "\n";
    $message .= "Faction: " . $faction_allegiance . "\n";
    $message .= "Date: " . current_time('mysql') . "\n";
    
    wp_mail($admin_email, $subject, $message);
    
    // Redirect with success message
    wp_redirect(home_url('/?signup=success'));
    exit;
}
add_action('admin_post_tec_cartel_signup', 'handle_tec_cartel_signup');
add_action('admin_post_nopriv_tec_cartel_signup', 'handle_tec_cartel_signup');

/**
 * Get faction data from JSON file
 */
function get_tec_faction_data() {
    $faction_file = get_template_directory() . '/data/astradigital-map.json';
    
    if (file_exists($faction_file)) {
        $json_content = file_get_contents($faction_file);
        $faction_data = json_decode($json_content, true);
        return $faction_data['factions'] ?? array();
    }
    
    return array();
}

/**
 * Display signup status messages
 */
function display_signup_messages() {
    if (isset($_GET['signup'])) {
        if ($_GET['signup'] === 'success') {
            echo '<div class="tec-message tec-success fixed top-20 left-1/2 transform -translate-x-1/2 z-50 bg-green-600 text-white px-6 py-3 rounded-lg shadow-lg">
                <i class="fas fa-check-circle mr-2"></i>
                Welcome to the Cartel! You\'ll receive transmissions from the TEC Block-Nexus soon.
            </div>';
        } elseif ($_GET['signup'] === 'error') {
            $error_msg = isset($_GET['msg']) && $_GET['msg'] === 'missing_fields' 
                ? 'Please fill in all required fields.' 
                : 'An error occurred. Please try again.';
            
            echo '<div class="tec-message tec-error fixed top-20 left-1/2 transform -translate-x-1/2 z-50 bg-red-600 text-white px-6 py-3 rounded-lg shadow-lg">
                <i class="fas fa-exclamation-triangle mr-2"></i>
                ' . $error_msg . '
            </div>';
        }
        
        // Add JavaScript to hide message after 5 seconds
        echo '<script>
            setTimeout(function() {
                const message = document.querySelector(".tec-message");
                if (message) {
                    message.style.opacity = "0";
                    setTimeout(() => message.remove(), 300);
                }
            }, 5000);
        </script>';
    }
}
add_action('wp_footer', 'display_signup_messages');

/**
 * Enqueue additional styles for TEC front page
 */
function tec_front_page_styles() {
    if (is_front_page()) {
        wp_enqueue_style('tec-front-page', get_template_directory_uri() . '/assets/css/front-page.css', array(), '1.0.0');
    }
}
add_action('wp_enqueue_scripts', 'tec_front_page_styles');

/**
 * Include template files
 */
require_once TEC_THEME_DIR . '/theme/inc/template-functions.php';
require_once TEC_THEME_DIR . '/theme/inc/template-tags.php';
require_once TEC_THEME_DIR . '/theme/inc/customizer.php';

/**
 * Load API functionality
 */
require_once TEC_THEME_DIR . '/api/api-init.php';

/**
 * Load Astradigital Ocean data
 */
function tec_load_astradigital_data() {
    $json_file = TEC_THEME_DIR . '/data/astradigital-map.json';
    
    if (file_exists($json_file)) {
        $json_data = file_get_contents($json_file);
        return json_decode($json_data, true);
    }
    
    return array();
}

/**
 * Add custom body classes
 */
function tec_body_classes($classes) {
    // Add a class for single faction pages
    if (is_singular('faction')) {
        $faction_slug = get_post_field('post_name', get_post());
        $classes[] = 'faction-' . $faction_slug;
    }

    return $classes;
}
add_filter('body_class', 'tec_body_classes');
