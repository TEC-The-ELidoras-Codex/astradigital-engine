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

// Make sure WordPress core is loaded
if (!function_exists('get_header')) {
    require_once(dirname(__FILE__) . '/../../../wp-load.php');
}

get_header(); ?>

<main class="tec-main-content">
    <!-- Page Hero Section -->
    <section class="tec-page-hero">
        <div class="tec-container">
            <h1 class="tec-page-title">
                <?php the_title(); ?>
            </h1>
            <?php if (has_excerpt()): ?>
                <p class="tec-page-excerpt">
                    <?php the_excerpt(); ?>
                </p>
            <?php endif; ?>
        </div>
    </section>    <!-- Page Content -->
    <section class="tec-content-section">
        <div class="tec-page-container">
            <?php while (have_posts()): the_post(); ?>
                <article id="post-<?php the_ID(); ?>" <?php post_class('tec-page-article'); ?>>
                    <div class="tec-page-content">
                        <?php
                        the_content();
                        
                        wp_link_pages(array(
                            'before' => '<div class="tec-page-links"><span class="tec-page-links-label">' . esc_html__('Pages:', 'tec-theme') . '</span>',
                            'after'  => '</div>',
                            'link_before' => '<span class="tec-page-number">',
                            'link_after'  => '</span>',
                        ));
                        ?>
                    </div>
                    
                    <?php if (comments_open() || get_comments_number()): ?>
                        <div class="tec-comments-section">
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
