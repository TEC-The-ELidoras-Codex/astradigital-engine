<?php
/**
 * Template for displaying 404 error pages
 *
 * @package TEC
 * @subpackage AstradigitalEngine
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

get_header(); ?>

<main class="min-h-screen bg-tecDark">
    <!-- 404 Hero Section -->
    <section class="py-20 px-4 bg-gradient-to-r from-tecDark to-tecPrimary">
        <div class="container mx-auto text-center">
            <div class="floating">
                <div class="text-9xl font-bold text-tecGold mb-4 font-orbitron">
                    404
                </div>
            </div>
            <h1 class="text-4xl md:text-6xl font-bold text-white mb-6 tracking-wide font-orbitron uppercase">
                Signal Lost in the Void
            </h1>
            <p class="text-lg md:text-xl text-tecSecondary max-w-3xl mx-auto mb-8">
                The data stream you're seeking has been scattered across the Astradigital Ocean. 
                This sector of the Block-Nexus appears to be experiencing temporal flux.
            </p>
        </div>
    </section>

    <!-- Error Content -->
    <section class="py-16 px-4">
        <div class="container mx-auto max-w-4xl text-center">
            <div class="bg-tecPrimary/60 backdrop-blur-md rounded-xl p-12 border border-tecSecondary/30 mb-12">
                <i class="fas fa-satellite-dish text-6xl text-tecGold mb-6"></i>
                <h2 class="text-3xl font-bold text-white mb-6">Attempting Signal Recovery...</h2>
                <p class="text-gray-400 mb-8 leading-relaxed">
                    The requested narrative fragment may have been:
                </p>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <div class="bg-tecDark/50 p-4 rounded-lg border border-tecSecondary/20">
                        <i class="fas fa-unlink text-tecGold text-2xl mb-2"></i>
                        <div class="text-white font-bold">Disconnected</div>
                        <div class="text-gray-400 text-sm">Link severed by faction interference</div>
                    </div>
                    <div class="bg-tecDark/50 p-4 rounded-lg border border-tecSecondary/20">
                        <i class="fas fa-eye-slash text-tecGold text-2xl mb-2"></i>
                        <div class="text-white font-bold">Classified</div>
                        <div class="text-gray-400 text-sm">Access restricted by TEC3 protocols</div>
                    </div>
                    <div class="bg-tecDark/50 p-4 rounded-lg border border-tecSecondary/20">
                        <i class="fas fa-ghost text-tecGold text-2xl mb-2"></i>
                        <div class="text-white font-bold">Erased</div>
                        <div class="text-gray-400 text-sm">Wiped from existence</div>
                    </div>
                </div>
            </div>

            <!-- Search Section -->
            <div class="bg-tecPrimary/40 backdrop-blur-md rounded-xl p-8 border border-tecSecondary/30 mb-12">
                <h3 class="text-2xl font-bold text-white mb-6">
                    <i class="fas fa-search mr-2 text-tecGold"></i>
                    Initiate Deep Scan
                </h3>
                <form role="search" method="get" action="<?php echo home_url('/'); ?>" class="max-w-md mx-auto">
                    <div class="flex">
                        <input type="search" 
                               name="s" 
                               placeholder="Search the Codex..." 
                               value="<?php echo get_search_query(); ?>"
                               class="flex-1 px-4 py-3 rounded-l-lg bg-gray-800 border border-gray-700 focus:border-tecGold text-white">
                        <button type="submit" class="bg-tecAccent hover:bg-purple-700 text-white px-6 py-3 rounded-r-lg transition">
                            <i class="fas fa-search"></i>
                        </button>
                    </div>
                </form>
            </div>

            <!-- Navigation Options -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <a href="<?php echo home_url(); ?>" class="bg-tecAccent hover:bg-purple-700 text-white p-6 rounded-xl transition transform hover:scale-105 group">
                    <i class="fas fa-home text-3xl mb-4 group-hover:text-tecGold transition"></i>
                    <div class="font-bold text-lg mb-2">Return to Hub</div>
                    <div class="text-sm opacity-80">Navigate back to the main terminal</div>
                </a>

                <a href="<?php echo home_url('/factions'); ?>" class="bg-tecPrimary hover:bg-tecSecondary/20 text-white p-6 rounded-xl transition transform hover:scale-105 group border border-tecSecondary/30">
                    <i class="fas fa-users text-3xl mb-4 group-hover:text-tecGold transition"></i>
                    <div class="font-bold text-lg mb-2">Explore Factions</div>
                    <div class="text-sm opacity-80">Discover the major players</div>
                </a>

                <a href="<?php echo home_url('/blog'); ?>" class="bg-tecPrimary hover:bg-tecSecondary/20 text-white p-6 rounded-xl transition transform hover:scale-105 group border border-tecSecondary/30">
                    <i class="fas fa-file-alt text-3xl mb-4 group-hover:text-tecGold transition"></i>
                    <div class="font-bold text-lg mb-2">Recent Dispatches</div>
                    <div class="text-sm opacity-80">Browse latest transmissions</div>
                </a>
            </div>

            <!-- Recent Posts -->
            <div class="mt-16">
                <h3 class="text-2xl font-bold text-white mb-8">
                    <i class="fas fa-broadcast-tower mr-2 text-tecGold"></i>
                    Recent Transmissions
                </h3>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <?php
                    $recent_posts = wp_get_recent_posts(array(
                        'numberposts' => 3,
                        'post_status' => 'publish'
                    ));

                    if ($recent_posts):
                        foreach ($recent_posts as $post): ?>
                            <a href="<?php echo get_permalink($post['ID']); ?>" class="post-card bg-tecPrimary/60 backdrop-blur-md rounded-xl p-6 border border-tecSecondary/30 hover:border-tecGold/50 transition group">
                                <div class="text-tecGold text-sm mb-2"><?php echo get_the_date('M j, Y', $post['ID']); ?></div>
                                <h4 class="text-white font-bold mb-2 group-hover:text-tecGold transition"><?php echo esc_html($post['post_title']); ?></h4>
                                <p class="text-gray-400 text-sm"><?php echo wp_trim_words($post['post_content'], 15); ?></p>
                            </a>
                        <?php endforeach;
                    else: ?>
                        <div class="col-span-3 text-center text-gray-400">
                            <i class="fas fa-satellite text-4xl mb-4"></i>
                            <p>No recent transmissions detected...</p>
                        </div>
                    <?php endif; ?>
                </div>
            </div>
        </div>
    </section>
</main>

<style>
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}

.floating {
    animation: float 6s ease-in-out infinite;
}
</style>

<?php get_footer(); ?>
