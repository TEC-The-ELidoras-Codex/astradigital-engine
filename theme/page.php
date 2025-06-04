<?php
/**
 * Template for displaying individual pages
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
    <!-- Page Hero Section -->
    <section class="py-20 px-4 bg-gradient-to-r from-tecPrimary to-tecAccent">
        <div class="container mx-auto text-center">
            <h1 class="text-4xl md:text-6xl font-bold text-white mb-4 tracking-wide font-orbitron uppercase">
                <?php the_title(); ?>
            </h1>
            <?php if (has_excerpt()): ?>
                <p class="text-lg md:text-xl text-tecSecondary max-w-3xl mx-auto">
                    <?php the_excerpt(); ?>
                </p>
            <?php endif; ?>
        </div>
    </section>

    <!-- Page Content -->
    <section class="py-16 px-4">
        <div class="container mx-auto max-w-4xl">
            <?php while (have_posts()): the_post(); ?>
                <article id="post-<?php the_ID(); ?>" <?php post_class('bg-tecPrimary/60 backdrop-blur-md rounded-xl p-8 border border-tecSecondary/30'); ?>>
                    <div class="prose prose-lg prose-invert max-w-none">
                        <?php
                        the_content();
                        
                        wp_link_pages(array(
                            'before' => '<div class="page-links mt-8 p-4 bg-tecDark/50 rounded-lg"><span class="text-tecGold font-bold">' . esc_html__('Pages:', 'tec-theme') . '</span>',
                            'after'  => '</div>',
                            'link_before' => '<span class="page-number bg-tecAccent text-white px-3 py-1 rounded mr-2 hover:bg-purple-700 transition">',
                            'link_after'  => '</span>',
                        ));
                        ?>
                    </div>
                    
                    <?php if (comments_open() || get_comments_number()): ?>
                        <div class="mt-12">
                            <?php comments_template(); ?>
                        </div>
                    <?php endif; ?>
                </article>
            <?php endwhile; ?>
        </div>
    </section>

    <!-- Navigation -->
    <section class="py-8 px-4 border-t border-tecSecondary/20">
        <div class="container mx-auto">
            <div class="flex justify-between items-center">
                <div class="text-left">
                    <?php
                    $prev_post = get_previous_post();
                    if ($prev_post): ?>
                        <a href="<?php echo get_permalink($prev_post->ID); ?>" class="inline-flex items-center text-tecGold hover:text-white transition">
                            <i class="fas fa-chevron-left mr-2"></i>
                            <div>
                                <div class="text-sm text-gray-400">Previous</div>
                                <div class="font-bold"><?php echo esc_html($prev_post->post_title); ?></div>
                            </div>
                        </a>
                    <?php endif; ?>
                </div>
                
                <div class="text-center">
                    <a href="<?php echo home_url(); ?>" class="bg-tecAccent hover:bg-purple-700 text-white px-6 py-2 rounded-lg transition">
                        <i class="fas fa-home mr-2"></i>Back to Hub
                    </a>
                </div>
                
                <div class="text-right">
                    <?php
                    $next_post = get_next_post();
                    if ($next_post): ?>
                        <a href="<?php echo get_permalink($next_post->ID); ?>" class="inline-flex items-center text-tecGold hover:text-white transition">
                            <div class="text-right">
                                <div class="text-sm text-gray-400">Next</div>
                                <div class="font-bold"><?php echo esc_html($next_post->post_title); ?></div>
                            </div>
                            <i class="fas fa-chevron-right ml-2"></i>
                        </a>
                    <?php endif; ?>
                </div>
            </div>
        </div>
    </section>
</main>

<?php get_footer(); ?>
