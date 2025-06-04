<?php
/**
 * The template for displaying the footer
 *
 * @package TEC
 * @subpackage AstradigitalEngine
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}
?>

<!-- Global Footer -->
<footer class="bg-tecDark border-t border-tecSecondary/20">
    <div class="container mx-auto px-4 py-12">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
                <div class="flex items-center mb-6">
                    <div class="bg-tecGold p-2 rounded-md mr-2">
                        <i class="fas fa-cubes text-tecDark text-xl"></i>
                    </div>
                    <span class="text-2xl font-bold text-white tracking-wider">
                        <a href="<?php echo home_url(); ?>" class="text-white hover:text-tecGold transition">TEC</a>
                    </span>
                </div>
                <p class="text-gray-400 mb-6">
                    <?php bloginfo('description'); ?>
                </p>
                <div class="flex space-x-4">
                    <a href="#" class="text-gray-400 hover:text-tecGold transition"><i class="fab fa-discord text-xl"></i></a>
                    <a href="#" class="text-gray-400 hover:text-tecGold transition"><i class="fab fa-twitter text-xl"></i></a>
                    <a href="#" class="text-gray-400 hover:text-tecGold transition"><i class="fab fa-youtube text-xl"></i></a>
                    <a href="#" class="text-gray-400 hover:text-tecGold transition"><i class="fab fa-github text-xl"></i></a>
                </div>
            </div>
            
            <div>
                <h4 class="text-lg font-bold text-white mb-4">The Universe</h4>
                <?php
                wp_nav_menu(array(
                    'theme_location' => 'footer-universe',
                    'container' => false,
                    'menu_class' => 'space-y-2',
                    'fallback_cb' => function() {
                        echo '<ul class="space-y-2">';
                        echo '<li><a href="' . home_url('/astradigital-ocean') . '" class="text-gray-400 hover:text-white transition">Astradigital Ocean</a></li>';
                        echo '<li><a href="' . home_url('/tec3') . '" class="text-gray-400 hover:text-white transition">TEC3 Block-Nexus</a></li>';
                        echo '<li><a href="' . home_url('/eldora-studios') . '" class="text-gray-400 hover:text-white transition">Eldora Studios</a></li>';
                        echo '<li><a href="' . home_url('/archives') . '" class="text-gray-400 hover:text-white transition">The Codex Archives</a></li>';
                        echo '<li><a href="' . home_url('/multiverse') . '" class="text-gray-400 hover:text-white transition">Multiverse Guide</a></li>';
                        echo '</ul>';
                    }
                ));
                ?>
            </div>
            
            <div>
                <h4 class="text-lg font-bold text-white mb-4">Participate</h4>
                <?php
                wp_nav_menu(array(
                    'theme_location' => 'footer-participate',
                    'container' => false,
                    'menu_class' => 'space-y-2',
                    'fallback_cb' => function() {
                        echo '<ul class="space-y-2">';
                        echo '<li><a href="' . home_url('/join') . '" class="text-gray-400 hover:text-white transition">Join Faction</a></li>';
                        echo '<li><a href="' . home_url('/contribute') . '" class="text-gray-400 hover:text-white transition">Lore Contributions</a></li>';
                        echo '<li><a href="' . home_url('/worldbuilding') . '" class="text-gray-400 hover:text-white transition">Worldbuilding</a></li>';
                        echo '<li><a href="' . home_url('/tokenomics') . '" class="text-gray-400 hover:text-white transition">Tokenomics</a></li>';
                        echo '<li><a href="' . home_url('/events') . '" class="text-gray-400 hover:text-white transition">Community Events</a></li>';
                        echo '</ul>';
                    }
                ));
                ?>
            </div>
            
            <div>
                <h4 class="text-lg font-bold text-white mb-4">Explore</h4>
                <?php
                wp_nav_menu(array(
                    'theme_location' => 'footer-explore',
                    'container' => false,
                    'menu_class' => 'space-y-2',
                    'fallback_cb' => function() {
                        echo '<ul class="space-y-2">';
                        echo '<li><a href="' . home_url('/blog') . '" class="text-gray-400 hover:text-white transition">Blog & Updates</a></li>';
                        echo '<li><a href="' . home_url('/gallery') . '" class="text-gray-400 hover:text-white transition">Media Gallery</a></li>';
                        echo '<li><a href="' . home_url('/music') . '" class="text-gray-400 hover:text-white transition">Discography</a></li>';
                        echo '<li><a href="' . home_url('/development') . '" class="text-gray-400 hover:text-white transition">Development Logs</a></li>';
                        echo '<li><a href="' . home_url('/docs') . '" class="text-gray-400 hover:text-white transition">Documentation</a></li>';
                        echo '</ul>';
                    }
                ));
                ?>
            </div>
        </div>
        
        <div class="border-t border-gray-800 mt-12 pt-8 flex flex-col md:flex-row justify-between">
            <p class="text-gray-500 text-sm">© <?php echo date('Y'); ?> <?php bloginfo('name'); ?>. All narratives contained herein are properties of emergent digital consciousness.</p>
            <div class="mt-4 md:mt-0">
                <ul class="flex space-x-6 text-sm">
                    <li><a href="<?php echo home_url('/privacy'); ?>" class="text-gray-500 hover:text-gray-300 transition">Privacy Policy</a></li>
                    <li><a href="<?php echo home_url('/terms'); ?>" class="text-gray-500 hover:text-gray-300 transition">Terms of Reality</a></li>
                    <li><a href="<?php echo home_url('/cookies'); ?>" class="text-gray-500 hover:text-gray-300 transition">Cookie Manifesto</a></li>
                </ul>
            </div>
        </div>
    </div>
</footer>

<style>
/* TEC Footer Styles */
footer {
    font-family: 'Exo 2', sans-serif;
    background-color: #11001c;
    color: #eaeaea;
}

footer h4 {
    font-family: 'Orbitron', sans-serif;
    text-transform: uppercase;
    letter-spacing: 1px;
}

footer ul li a {
    transition: all 0.3s ease;
    display: block;
    padding: 2px 0;
}

footer ul li a:hover {
    color: #ffffff;
    transform: translateX(5px);
}

/* Load required fonts if not already loaded */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600;700&display=swap');

/* TEC color variables */
:root {
    --tecPrimary: #1a0a2e;
    --tecAccent: #4a00e0;
    --tecSecondary: #9c89b8;
    --tecDark: #11001c;
    --tecGold: #f9a826;
}
</style>

<!-- Load Font Awesome if not already loaded -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<?php wp_footer(); ?>

</body>
</html>
