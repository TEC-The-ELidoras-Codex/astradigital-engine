<?php
/**
 * Template for displaying archive pages (categories, tags, etc.)
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
    <!-- Archive Hero Section -->
    <section class="py-20 px-4 bg-gradient-to-r from-tecPrimary to-tecDark">
        <div class="container mx-auto text-center">
            <h1 class="text-4xl md:text-6xl font-bold text-white mb-4 tracking-wide font-orbitron uppercase">
                <?php
                if (is_category()) {
                    echo 'Category: ' . single_cat_title('', false);
                } elseif (is_tag()) {
                    echo 'Tag: ' . single_tag_title('', false);
                } elseif (is_author()) {
                    echo 'Author: ' . get_the_author();
                } elseif (is_date()) {
                    echo 'Archive: ' . get_the_date('F Y');
                } else {
                    echo 'Archives';
                }
                ?>
            </h1>
            <?php if (category_description() || tag_description()): ?>
                <div class="text-lg text-tecSecondary max-w-3xl mx-auto">
                    <?php echo category_description() . tag_description(); ?>
                </div>
            <?php endif; ?>
            
            <div class="mt-6 text-tecGold">
                <i class="fas fa-folder-open mr-2"></i>
                <?php
                global $wp_query;
                echo $wp_query->found_posts . ' ' . ($wp_query->found_posts == 1 ? 'dispatch' : 'dispatches');
                ?>
            </div>
        </div>
    </section>

    <!-- Archive Content -->
    <section class="py-16 px-4">
        <div class="container mx-auto">
            <?php if (have_posts()): ?>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
                    <?php while (have_posts()): the_post(); ?>
                        <article class="post-card rounded-xl overflow-hidden transition bg-tecPrimary/60 backdrop-blur-md border border-tecSecondary/30">
                            <?php if (has_post_thumbnail()): ?>
                                <div class="h-48 overflow-hidden">
                                    <a href="<?php the_permalink(); ?>">
                                        <?php the_post_thumbnail('large', array('class' => 'w-full h-full object-cover hover:scale-105 transition-transform duration-300')); ?>
                                    </a>
                                </div>
                            <?php else: ?>
                                <div class="h-48 bg-gradient-to-r from-purple-900 to-indigo-700 flex items-center justify-center">
                                    <i class="fas fa-file-alt text-tecGold text-6xl"></i>
                                </div>
                            <?php endif; ?>
                            
                            <div class="p-6">
                                <div class="flex items-center mb-3">
                                    <span class="text-xs text-tecGold bg-tecDark px-2 py-1 rounded mr-2">
                                        <?php 
                                        $categories = get_the_category();
                                        if (!empty($categories)) {
                                            echo esc_html($categories[0]->name);
                                        } else {
                                            echo 'Dispatch';
                                        }
                                        ?>
                                    </span>
                                    <span class="text-xs text-gray-400"><?php echo get_the_date(); ?></span>
                                </div>
                                
                                <h3 class="text-xl font-bold text-white mb-3 hover:text-tecGold transition">
                                    <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                                </h3>
                                
                                <p class="text-gray-400 mb-4">
                                    <?php echo wp_trim_words(get_the_excerpt(), 20); ?>
                                </p>
                                
                                <div class="flex items-center justify-between">
                                    <a href="<?php the_permalink(); ?>" class="text-tecGold hover:text-yellow-500 transition flex items-center">
                                        Read More <i class="fas fa-arrow-right ml-2 text-xs"></i>
                                    </a>
                                    
                                    <div class="flex items-center text-gray-500 text-sm">
                                        <i class="fas fa-user mr-1"></i>
                                        <a href="<?php echo get_author_posts_url(get_the_author_meta('ID')); ?>" class="hover:text-tecGold transition">
                                            <?php the_author(); ?>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </article>
                    <?php endwhile; ?>
                </div>

                <!-- Pagination -->
                <div class="mt-16 text-center">
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

            <?php else: ?>
                <!-- No Posts Found -->
                <div class="text-center py-20">
                    <div class="bg-tecPrimary/60 backdrop-blur-md rounded-xl p-12 max-w-2xl mx-auto border border-tecSecondary/30">
                        <i class="fas fa-search text-6xl text-tecGold mb-6"></i>
                        <h2 class="text-3xl font-bold text-white mb-4">No Dispatches Found</h2>
                        <p class="text-gray-400 mb-8">
                            The Astradigital Ocean seems quiet in this sector. Perhaps the data streams have shifted elsewhere.
                        </p>
                        <a href="<?php echo home_url(); ?>" class="bg-tecAccent hover:bg-purple-700 text-white px-8 py-3 rounded-lg transition inline-flex items-center">
                            <i class="fas fa-home mr-2"></i>Return to Hub
                        </a>
                    </div>
                </div>
            <?php endif; ?>
        </div>
    </section>
</main>

<?php get_footer(); ?>
