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
    </section>    <!-- Navigation -->
    <section class="tec-page-navigation">
        <div class="tec-container">
            <div class="tec-nav-flex">
                <div class="tec-nav-left">
                    <?php
                    $prev_post = get_previous_post();
                    if ($prev_post): ?>
                        <a href="<?php echo get_permalink($prev_post->ID); ?>" class="tec-nav-link">
                            <i class="icon-chevron-left"></i>
                            <div>
                                <div class="tec-nav-label">Previous</div>
                                <div class="tec-nav-title"><?php echo esc_html($prev_post->post_title); ?></div>
                            </div>
                        </a>
                    <?php endif; ?>
                </div>
                
                <div class="tec-nav-center">
                    <a href="<?php echo home_url(); ?>" class="tec-btn tec-btn-primary">
                        <i class="icon-home"></i>Back to Hub
                    </a>
                </div>
                
                <div class="tec-nav-right">
                    <?php
                    $next_post = get_next_post();
                    if ($next_post): ?>
                        <a href="<?php echo get_permalink($next_post->ID); ?>" class="tec-nav-link">
                            <div class="tec-nav-content-right">
                                <div class="tec-nav-label">Next</div>
                                <div class="tec-nav-title"><?php echo esc_html($next_post->post_title); ?></div>
                            </div>
                            <i class="icon-chevron-right"></i>
                        </a>
                    <?php endif; ?>
                </div>
            </div>
        </div>
    </section>
</main>

<?php get_footer(); ?>
