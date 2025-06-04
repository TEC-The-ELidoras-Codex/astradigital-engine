<?php
/**
 * Template for displaying search results
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
    <!-- Search Hero Section -->
    <section class="py-20 px-4 bg-gradient-to-r from-tecPrimary to-tecAccent">
        <div class="container mx-auto text-center">
            <div class="mb-6">
                <i class="fas fa-search text-6xl text-tecGold floating"></i>
            </div>
            <h1 class="text-4xl md:text-6xl font-bold text-white mb-4 tracking-wide font-orbitron uppercase">
                Deep Scan Results
            </h1>
            <p class="text-lg md:text-xl text-tecSecondary max-w-3xl mx-auto mb-6">
                Scanning the Astradigital Ocean for: 
                <span class="text-tecGold font-bold">"<?php echo get_search_query(); ?>"</span>
            </p>
            
            <?php
            global $wp_query;
            $found_posts = $wp_query->found_posts;
            ?>
            <div class="text-tecGold font-bold">
                <i class="fas fa-satellite-dish mr-2"></i>
                <?php echo $found_posts; ?> 
                <?php echo ($found_posts == 1) ? 'signal detected' : 'signals detected'; ?>
            </div>
        </div>
    </section>

    <!-- Search Form Section -->
    <section class="py-8 px-4 bg-tecPrimary/30 border-b border-tecSecondary/20">
        <div class="container mx-auto max-w-2xl">
            <form role="search" method="get" action="<?php echo home_url('/'); ?>" class="flex">
                <input type="search" 
                       name="s" 
                       placeholder="Refine your search..." 
                       value="<?php echo get_search_query(); ?>"
                       class="flex-1 px-4 py-3 rounded-l-lg bg-gray-800 border border-gray-700 focus:border-tecGold text-white">
                <button type="submit" class="bg-tecAccent hover:bg-purple-700 text-white px-6 py-3 rounded-r-lg transition">
                    <i class="fas fa-search mr-2"></i>Scan
                </button>
            </form>
        </div>
    </section>

    <!-- Search Results -->
    <section class="py-16 px-4">
        <div class="container mx-auto">
            <?php if (have_posts()): ?>
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <!-- Main Results -->
                    <div class="lg:col-span-2">
                        <div class="space-y-8">
                            <?php while (have_posts()): the_post(); ?>
                                <article class="bg-tecPrimary/60 backdrop-blur-md rounded-xl p-6 border border-tecSecondary/30 hover:border-tecGold/50 transition">
                                    <div class="flex items-start gap-4">
                                        <?php if (has_post_thumbnail()): ?>
                                            <div class="flex-shrink-0 w-24 h-24 rounded-lg overflow-hidden">
                                                <a href="<?php the_permalink(); ?>">
                                                    <?php the_post_thumbnail('thumbnail', array('class' => 'w-full h-full object-cover')); ?>
                                                </a>
                                            </div>
                                        <?php else: ?>
                                            <div class="flex-shrink-0 w-24 h-24 rounded-lg bg-gradient-to-r from-purple-900 to-indigo-700 flex items-center justify-center">
                                                <i class="fas fa-file-alt text-tecGold text-2xl"></i>
                                            </div>
                                        <?php endif; ?>
                                        
                                        <div class="flex-1">
                                            <div class="flex items-center mb-2">
                                                <span class="text-xs text-tecGold bg-tecDark px-2 py-1 rounded mr-2">
                                                    <?php 
                                                    $categories = get_the_category();
                                                    if (!empty($categories)) {
                                                        echo esc_html($categories[0]->name);
                                                    } else {
                                                        echo get_post_type();
                                                    }
                                                    ?>
                                                </span>
                                                <span class="text-xs text-gray-400"><?php echo get_the_date(); ?></span>
                                            </div>
                                            
                                            <h3 class="text-xl font-bold text-white mb-2 hover:text-tecGold transition">
                                                <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                                            </h3>
                                            
                                            <p class="text-gray-400 mb-4">
                                                <?php 
                                                $excerpt = get_the_excerpt();
                                                if ($excerpt) {
                                                    echo wp_trim_words($excerpt, 25);
                                                } else {
                                                    echo wp_trim_words(get_the_content(), 25);
                                                }
                                                ?>
                                            </p>
                                            
                                            <div class="flex items-center justify-between">
                                                <a href="<?php the_permalink(); ?>" class="text-tecGold hover:text-yellow-500 transition flex items-center">
                                                    Access Signal <i class="fas fa-arrow-right ml-2 text-xs"></i>
                                                </a>
                                                
                                                <div class="flex items-center text-gray-500 text-sm">
                                                    <i class="fas fa-user mr-1"></i>
                                                    <a href="<?php echo get_author_posts_url(get_the_author_meta('ID')); ?>" class="hover:text-tecGold transition">
                                                        <?php the_author(); ?>
                                                    </a>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </article>
                            <?php endwhile; ?>
                        </div>

                        <!-- Pagination -->
                        <div class="mt-16">
                            <?php
                            $pagination_links = paginate_links(array(
                                'type' => 'array',
                                'prev_text' => '<i class="fas fa-chevron-left"></i> Previous',
                                'next_text' => 'Next <i class="fas fa-chevron-right"></i>',
                                'mid_size' => 2,
                            ));

                            if ($pagination_links):
                            ?>
                                <nav class="pagination flex justify-center items-center space-x-2">
                                    <?php foreach ($pagination_links as $link): ?>
                                        <div class="pagination-item">
                                            <?php echo str_replace('<a ', '<a class="bg-tecPrimary hover:bg-tecAccent text-white px-4 py-2 rounded-lg transition border border-tecSecondary/30" ', $link); ?>
                                            <?php echo str_replace('<span ', '<span class="bg-tecAccent text-white px-4 py-2 rounded-lg border border-tecSecondary/30" ', $link); ?>
                                        </div>
                                    <?php endforeach; ?>
                                </nav>
                            <?php endif; ?>
                        </div>
                    </div>

                    <!-- Sidebar -->
                    <div class="lg:col-span-1">
                        <div class="space-y-8">
                            <!-- Search Tips -->
                            <div class="bg-tecPrimary/60 backdrop-blur-md rounded-xl p-6 border border-tecSecondary/30">
                                <h3 class="text-lg font-bold text-white mb-4">
                                    <i class="fas fa-lightbulb mr-2 text-tecGold"></i>
                                    Search Tips
                                </h3>
                                <ul class="space-y-2 text-gray-400 text-sm">
                                    <li class="flex items-start">
                                        <i class="fas fa-quote-left text-tecGold mr-2 mt-1 text-xs"></i>
                                        Use quotes for exact phrases
                                    </li>
                                    <li class="flex items-start">
                                        <i class="fas fa-plus text-tecGold mr-2 mt-1 text-xs"></i>
                                        Use + to require terms
                                    </li>
                                    <li class="flex items-start">
                                        <i class="fas fa-minus text-tecGold mr-2 mt-1 text-xs"></i>
                                        Use - to exclude terms
                                    </li>
                                    <li class="flex items-start">
                                        <i class="fas fa-asterisk text-tecGold mr-2 mt-1 text-xs"></i>
                                        Use * as wildcard
                                    </li>
                                </ul>
                            </div>

                            <!-- Popular Tags -->
                            <div class="bg-tecPrimary/60 backdrop-blur-md rounded-xl p-6 border border-tecSecondary/30">
                                <h3 class="text-lg font-bold text-white mb-4">
                                    <i class="fas fa-tags mr-2 text-tecGold"></i>
                                    Popular Tags
                                </h3>
                                <div class="flex flex-wrap gap-2">
                                    <?php
                                    $popular_tags = get_tags(array(
                                        'orderby' => 'count',
                                        'order' => 'DESC',
                                        'number' => 10
                                    ));
                                    
                                    foreach ($popular_tags as $tag): ?>
                                        <a href="<?php echo get_tag_link($tag->term_id); ?>" 
                                           class="bg-tecDark/50 hover:bg-tecAccent text-white px-3 py-1 rounded-full text-xs transition">
                                            <?php echo esc_html($tag->name); ?>
                                        </a>
                                    <?php endforeach; ?>
                                </div>
                            </div>

                            <!-- Categories -->
                            <div class="bg-tecPrimary/60 backdrop-blur-md rounded-xl p-6 border border-tecSecondary/30">
                                <h3 class="text-lg font-bold text-white mb-4">
                                    <i class="fas fa-folder mr-2 text-tecGold"></i>
                                    Categories
                                </h3>
                                <ul class="space-y-2">
                                    <?php
                                    $categories = get_categories(array(
                                        'orderby' => 'count',
                                        'order' => 'DESC',
                                        'number' => 8
                                    ));
                                    
                                    foreach ($categories as $category): ?>
                                        <li>
                                            <a href="<?php echo get_category_link($category->term_id); ?>" 
                                               class="text-gray-400 hover:text-tecGold transition flex items-center justify-between">
                                                <span><?php echo esc_html($category->name); ?></span>
                                                <span class="text-xs bg-tecDark/50 px-2 py-1 rounded">
                                                    <?php echo $category->count; ?>
                                                </span>
                                            </a>
                                        </li>
                                    <?php endforeach; ?>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>

            <?php else: ?>
                <!-- No Results Found -->
                <div class="text-center py-20">
                    <div class="bg-tecPrimary/60 backdrop-blur-md rounded-xl p-12 max-w-2xl mx-auto border border-tecSecondary/30">
                        <i class="fas fa-satellite text-6xl text-tecGold mb-6"></i>
                        <h2 class="text-3xl font-bold text-white mb-4">No Signals Detected</h2>
                        <p class="text-gray-400 mb-8">
                            The search term "<span class="text-tecGold font-bold"><?php echo get_search_query(); ?></span>" 
                            yielded no results in the current data streams. The information may be:
                        </p>
                        
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                            <div class="bg-tecDark/50 p-4 rounded-lg">
                                <i class="fas fa-lock text-tecGold text-xl mb-2"></i>
                                <div class="text-sm text-gray-400">Classified</div>
                            </div>
                            <div class="bg-tecDark/50 p-4 rounded-lg">
                                <i class="fas fa-cloud text-tecGold text-xl mb-2"></i>
                                <div class="text-sm text-gray-400">In Transit</div>
                            </div>
                            <div class="bg-tecDark/50 p-4 rounded-lg">
                                <i class="fas fa-hourglass text-tecGold text-xl mb-2"></i>
                                <div class="text-sm text-gray-400">Not Yet Created</div>
                            </div>
                        </div>
                        
                        <div class="space-y-4">
                            <p class="text-gray-400">Try adjusting your search parameters:</p>
                            <form role="search" method="get" action="<?php echo home_url('/'); ?>" class="max-w-md mx-auto">
                                <div class="flex">
                                    <input type="search" 
                                           name="s" 
                                           placeholder="Try different keywords..." 
                                           class="flex-1 px-4 py-3 rounded-l-lg bg-gray-800 border border-gray-700 focus:border-tecGold text-white">
                                    <button type="submit" class="bg-tecAccent hover:bg-purple-700 text-white px-6 py-3 rounded-r-lg transition">
                                        <i class="fas fa-search"></i>
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            <?php endif; ?>
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
