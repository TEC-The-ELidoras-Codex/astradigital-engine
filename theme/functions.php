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
    
    // Enqueue mobile menu JavaScript
    wp_enqueue_script('tec-mobile-menu', get_template_directory_uri() . '/assets/js/mobile-menu.js', array('jquery'), '1.0.0', true);
    
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
      // Option 2: Send notification email to admin (if enabled)
    if (get_option('tec_enable_signup_notifications', true)) {
        $admin_email = get_option('tec_notification_email', get_option('admin_email'));
        $subject = 'New TEC Cartel Signup: ' . $user_name;
        $message = "New Cartel signup received:\n\n";
        $message .= "Name: " . $user_name . "\n";
        $message .= "Email: " . $user_email . "\n";
        $message .= "Faction: " . $faction_allegiance . "\n";
        $message .= "Date: " . current_time('mysql') . "\n";
        $message .= "IP: " . $_SERVER['REMOTE_ADDR'] . "\n\n";
        $message .= "View all signups: " . admin_url('admin.php?page=tec-cartel-signups');
        
        wp_mail($admin_email, $subject, $message);
    }
    
    // Redirect with success message
    wp_redirect(home_url('/?signup=success'));
    exit;
}
add_action('admin_post_tec_cartel_signup', 'handle_tec_cartel_signup');
add_action('admin_post_nopriv_tec_cartel_signup', 'handle_tec_cartel_signup');

/**
 * Add admin menu for TEC Cartel signups
 */
function tec_admin_menu() {
    add_menu_page(
        'TEC Cartel Signups',
        'TEC Cartel',
        'manage_options',
        'tec-cartel-signups',
        'tec_cartel_signups_page',
        'dashicons-groups',
        30
    );
    
    add_submenu_page(
        'tec-cartel-signups',
        'TEC Settings',
        'Settings',
        'manage_options',
        'tec-settings',
        'tec_settings_page'
    );
}
add_action('admin_menu', 'tec_admin_menu');

/**
 * TEC Cartel signups admin page
 */
function tec_cartel_signups_page() {
    $signups = get_option('tec_cartel_signups', array());
    $faction_data = get_tec_faction_data();
    
    // Handle actions
    if (isset($_POST['action']) && $_POST['action'] === 'delete_signup' && isset($_POST['signup_id'])) {
        if (wp_verify_nonce($_POST['_wpnonce'], 'delete_signup')) {
            $signup_id = intval($_POST['signup_id']);
            if (isset($signups[$signup_id])) {
                unset($signups[$signup_id]);
                $signups = array_values($signups); // Re-index array
                update_option('tec_cartel_signups', $signups);
                echo '<div class="notice notice-success"><p>Signup deleted successfully.</p></div>';
            }
        }
    }
    
    if (isset($_POST['action']) && $_POST['action'] === 'clear_all_signups') {
        if (wp_verify_nonce($_POST['_wpnonce'], 'clear_all_signups')) {
            update_option('tec_cartel_signups', array());
            $signups = array();
            echo '<div class="notice notice-success"><p>All signups cleared successfully.</p></div>';
        }
    }
    
    ?>
    <div class="wrap">
        <h1>TEC Cartel Signups</h1>
        
        <div class="tec-admin-stats" style="display: flex; gap: 20px; margin: 20px 0;">
            <div class="tec-stat-box" style="background: #fff; padding: 20px; border-radius: 8px; border-left: 4px solid #0073aa; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <h3 style="margin: 0 0 10px 0; color: #0073aa;">Total Signups</h3>
                <span style="font-size: 24px; font-weight: bold;"><?php echo count($signups); ?></span>
            </div>
            
            <?php
            // Count signups by faction
            $faction_counts = array();
            foreach ($signups as $signup) {
                $faction = $signup['faction'] ?? 'Unknown';
                $faction_counts[$faction] = ($faction_counts[$faction] ?? 0) + 1;
            }
            arsort($faction_counts);
            
            if (!empty($faction_counts)) {
                $top_faction = array_key_first($faction_counts);
                ?>
                <div class="tec-stat-box" style="background: #fff; padding: 20px; border-radius: 8px; border-left: 4px solid #00a32a; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <h3 style="margin: 0 0 10px 0; color: #00a32a;">Most Popular Faction</h3>
                    <span style="font-size: 18px; font-weight: bold;"><?php echo esc_html($top_faction); ?></span><br>
                    <small>(<?php echo $faction_counts[$top_faction]; ?> signups)</small>
                </div>
                <?php
            }
            ?>
        </div>
        
        <?php if (!empty($signups)): ?>
            <div style="margin: 20px 0;">
                <form method="post" style="display: inline;" onsubmit="return confirm('Are you sure you want to clear ALL signups? This cannot be undone.');">
                    <?php wp_nonce_field('clear_all_signups'); ?>
                    <input type="hidden" name="action" value="clear_all_signups">
                    <button type="submit" class="button button-secondary">Clear All Signups</button>
                </form>
                
                <button onclick="exportSignups()" class="button button-primary" style="margin-left: 10px;">Export to CSV</button>
            </div>
            
            <table class="wp-list-table widefat fixed striped">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Faction</th>
                        <th>Date</th>
                        <th>IP Address</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($signups as $index => $signup): ?>
                        <tr>
                            <td><strong><?php echo esc_html($signup['name']); ?></strong></td>
                            <td>
                                <a href="mailto:<?php echo esc_attr($signup['email']); ?>">
                                    <?php echo esc_html($signup['email']); ?>
                                </a>
                            </td>
                            <td>
                                <span class="faction-badge" style="display: inline-block; padding: 4px 8px; background: #f0f0f1; border-radius: 12px; font-size: 12px;">
                                    <?php echo esc_html($signup['faction'] ?? 'Unknown'); ?>
                                </span>
                            </td>
                            <td><?php echo esc_html(date('M j, Y g:i A', strtotime($signup['date']))); ?></td>
                            <td><code><?php echo esc_html($signup['ip'] ?? 'Unknown'); ?></code></td>
                            <td>
                                <form method="post" style="display: inline;" onsubmit="return confirm('Are you sure you want to delete this signup?');">
                                    <?php wp_nonce_field('delete_signup'); ?>
                                    <input type="hidden" name="action" value="delete_signup">
                                    <input type="hidden" name="signup_id" value="<?php echo $index; ?>">
                                    <button type="submit" class="button button-small">Delete</button>
                                </form>
                            </td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
            
            <script>
            function exportSignups() {
                const signups = <?php echo json_encode($signups); ?>;
                let csv = 'Name,Email,Faction,Date,IP Address\n';
                
                signups.forEach(signup => {
                    csv += `"${signup.name}","${signup.email}","${signup.faction || 'Unknown'}","${signup.date}","${signup.ip || 'Unknown'}"\n`;
                });
                
                const blob = new Blob([csv], { type: 'text/csv' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'tec-cartel-signups-' + new Date().toISOString().split('T')[0] + '.csv';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            }
            </script>
            
        <?php else: ?>
            <div class="notice notice-info">
                <p>No Cartel signups yet. Share the TEC homepage to start building your faction!</p>
            </div>
        <?php endif; ?>
        
        <h2>Faction Statistics</h2>
        <?php if (!empty($faction_counts)): ?>
            <div class="tec-faction-stats" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin: 20px 0;">
                <?php foreach ($faction_counts as $faction => $count): ?>
                    <div style="background: #fff; padding: 15px; border-radius: 8px; border-left: 4px solid #646970; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <h4 style="margin: 0 0 8px 0;"><?php echo esc_html($faction); ?></h4>
                        <div style="font-size: 24px; font-weight: bold; color: #0073aa;"><?php echo $count; ?></div>
                        <div style="font-size: 12px; color: #646970;">
                            <?php echo round(($count / count($signups)) * 100, 1); ?>% of total
                        </div>
                    </div>
                <?php endforeach; ?>
            </div>
        <?php endif; ?>
    </div>
    <?php
}

/**
 * TEC Settings admin page
 */
function tec_settings_page() {
    if (isset($_POST['submit'])) {
        if (wp_verify_nonce($_POST['_wpnonce'], 'tec_settings')) {
            update_option('tec_notification_email', sanitize_email($_POST['notification_email']));
            update_option('tec_enable_signup_notifications', isset($_POST['enable_notifications']));
            update_option('tec_cartel_welcome_message', wp_kses_post($_POST['welcome_message']));
            echo '<div class="notice notice-success"><p>Settings saved successfully!</p></div>';
        }
    }
    
    $notification_email = get_option('tec_notification_email', get_option('admin_email'));
    $enable_notifications = get_option('tec_enable_signup_notifications', true);
    $welcome_message = get_option('tec_cartel_welcome_message', 'Welcome to the Cartel! You\'ll receive transmissions from the TEC Block-Nexus soon.');
    ?>
    <div class="wrap">
        <h1>TEC Settings</h1>
        
        <form method="post">
            <?php wp_nonce_field('tec_settings'); ?>
            
            <table class="form-table">
                <tr>
                    <th scope="row">Notification Email</th>
                    <td>
                        <input type="email" name="notification_email" value="<?php echo esc_attr($notification_email); ?>" class="regular-text" />
                        <p class="description">Email address to receive Cartel signup notifications.</p>
                    </td>
                </tr>
                
                <tr>
                    <th scope="row">Enable Notifications</th>
                    <td>
                        <label>
                            <input type="checkbox" name="enable_notifications" <?php checked($enable_notifications); ?> />
                            Send email notifications for new signups
                        </label>
                    </td>
                </tr>
                
                <tr>
                    <th scope="row">Welcome Message</th>
                    <td>
                        <textarea name="welcome_message" rows="3" cols="50" class="large-text"><?php echo esc_textarea($welcome_message); ?></textarea>
                        <p class="description">Message shown to users after successful signup.</p>
                    </td>
                </tr>
            </table>
            
            <?php submit_button(); ?>
        </form>
    </div>
    <?php
}

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
            $welcome_message = get_option('tec_cartel_welcome_message', 'Welcome to the Cartel! You\'ll receive transmissions from the TEC Block-Nexus soon.');
            echo '<div class="tec-message tec-success fixed top-20 left-1/2 transform -translate-x-1/2 z-50 bg-green-600 text-white px-6 py-3 rounded-lg shadow-lg">
                <i class="fas fa-check-circle mr-2"></i>
                ' . esc_html($welcome_message) . '
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
