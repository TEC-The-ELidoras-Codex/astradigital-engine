<?php
/**
 * The main template file for TEC Theme
 *
 * @package TEC
 * @subpackage AstradigitalEngine
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// If this is the front page, use the front-page template
if (is_front_page()) {
    get_template_part('front-page');
    return;
}

get_header(); ?>

<div class="tec-main-content min-h-screen bg-tecDark text-white py-20">
    <div class="container mx-auto px-4">
        <?php if (have_posts()) : ?>
            <div class="posts-grid grid gap-8">
                <?php while (have_posts()) : the_post(); ?>
                    <article id="post-<?php the_ID(); ?>" <?php post_class('post-card bg-tecPrimary rounded-xl p-8 border border-tecSecondary/30'); ?>>
                        <header class="post-header mb-6">
                            <h2 class="post-title text-2xl font-bold text-white mb-2">
                                <a href="<?php the_permalink(); ?>" class="text-white hover:text-tecGold transition">
                                    <?php the_title(); ?>
                                </a>
                            </h2>
                            <div class="post-meta text-sm text-gray-400">
                                <span class="post-date">
                                    <i class="fas fa-calendar mr-1"></i>
                                    <?php echo get_the_date(); ?>
                                </span>
                                <span class="post-author ml-4">
                                    <i class="fas fa-user mr-1"></i>
                                    <?php the_author(); ?>
                                </span>
                                <?php if (has_category()) : ?>
                                    <span class="post-categories ml-4">
                                        <i class="fas fa-folder mr-1"></i>
                                        <?php the_category(', '); ?>
                                    </span>
                                <?php endif; ?>
                            </div>
                        </header>
                        
                        <?php if (has_post_thumbnail()) : ?>
                            <div class="post-thumbnail mb-6">
                                <a href="<?php the_permalink(); ?>">
                                    <?php the_post_thumbnail('large', array('class' => 'w-full h-48 object-cover rounded-lg')); ?>
                                </a>
                            </div>
                        <?php endif; ?>
                        
                        <div class="post-content text-gray-300 leading-relaxed">
                            <?php
                            if (is_single()) {
                                the_content();
                            } else {
                                the_excerpt();
                            }
                            ?>
                        </div>
                        
                        <?php if (!is_single()) : ?>
                            <footer class="post-footer mt-6">
                                <a href="<?php the_permalink(); ?>" class="read-more-btn inline-flex items-center text-tecGold font-bold hover:text-white transition">
                                    Read More
                                    <i class="fas fa-arrow-right ml-2"></i>
                                </a>
                            </footer>
                        <?php endif; ?>
                    </article>
                <?php endwhile; ?>
            </div>
            
            <div class="pagination-wrapper mt-12 text-center">
                <?php
                the_posts_pagination(array(
                    'mid_size' => 2,
                    'prev_text' => '<i class="fas fa-chevron-left"></i> Previous',
                    'next_text' => 'Next <i class="fas fa-chevron-right"></i>',
                    'class' => 'tec-pagination'
                ));
                ?>
            </div>
            
        <?php else : ?>
            <div class="no-posts text-center py-20">
                <i class="fas fa-search text-6xl text-tecSecondary mb-6"></i>
                <h2 class="text-3xl font-bold text-white mb-4">No Content Found</h2>
                <p class="text-gray-400 mb-8">The Astradigital Ocean appears empty in this sector.</p>
                <a href="<?php echo home_url(); ?>" class="bg-tecAccent hover:bg-purple-700 text-white font-bold py-3 px-8 rounded-lg transition">
                    Return to Base
                </a>
            </div>
        <?php endif; ?>
    </div>
</div>

<style>
.post-card {
    transition: all 0.3s ease;
    background: rgba(26, 10, 46, 0.6);
    backdrop-filter: blur(10px);
}

.post-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 25px -5px rgba(156, 137, 184, 0.3);
    border-color: rgba(122, 0, 255, 0.6);
}

.tec-pagination .page-numbers {
    display: inline-block;
    padding: 8px 16px;
    margin: 0 4px;
    background: rgba(26, 10, 46, 0.6);
    color: #9c89b8;
    text-decoration: none;
    border-radius: 6px;
    border: 1px solid rgba(122, 0, 255, 0.3);
    transition: all 0.3s ease;
}

.tec-pagination .page-numbers:hover,
.tec-pagination .page-numbers.current {
    background: #4a00e0;
    color: white;
    border-color: #4a00e0;
}

.read-more-btn:hover {
    transform: translateX(5px);
}
</style>

<?php get_footer(); ?>
