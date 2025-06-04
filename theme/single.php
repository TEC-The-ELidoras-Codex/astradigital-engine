<?php
/**
 * The template for displaying single posts
 *
 * @package TEC
 * @subpackage AstradigitalEngine
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

get_header(); ?>

<div class="single-post-container min-h-screen bg-tecDark text-white">
    <!-- Hero Section -->
    <section class="post-hero py-20 px-4" style="background: linear-gradient(135deg, #1a0a2e 0%, #4a00e0 100%);">
        <div class="container mx-auto max-w-4xl text-center">
            <?php if (have_posts()) : the_post(); ?>
                <div class="post-meta mb-6">
                    <span class="text-tecGold font-bold">
                        <i class="fas fa-calendar mr-2"></i>
                        <?php echo get_the_date(); ?>
                    </span>
                    <span class="text-gray-200 mx-4">•</span>
                    <span class="text-gray-200">
                        <i class="fas fa-user mr-2"></i>
                        <?php the_author(); ?>
                    </span>
                    <?php if (has_category()) : ?>
                        <span class="text-gray-200 mx-4">•</span>
                        <span class="text-gray-200">
                            <i class="fas fa-folder mr-2"></i>
                            <?php the_category(', '); ?>
                        </span>
                    <?php endif; ?>
                </div>
                
                <h1 class="text-3xl md:text-5xl font-bold text-white mb-6 leading-tight">
                    <?php the_title(); ?>
                </h1>
                
                <?php if (has_excerpt()) : ?>
                    <p class="text-lg text-gray-200 max-w-2xl mx-auto">
                        <?php the_excerpt(); ?>
                    </p>
                <?php endif; ?>
            <?php endif; ?>
        </div>
    </section>
    
    <!-- Post Content -->
    <section class="post-content py-16 px-4">
        <div class="container mx-auto max-w-4xl">
            <article class="prose prose-lg prose-invert max-w-none">
                <?php if (has_post_thumbnail()) : ?>
                    <div class="featured-image mb-8">
                        <?php the_post_thumbnail('large', array('class' => 'w-full h-64 md:h-96 object-cover rounded-xl')); ?>
                    </div>
                <?php endif; ?>
                
                <div class="post-body text-gray-300 leading-relaxed">
                    <?php the_content(); ?>
                </div>
                
                <?php if (has_tag()) : ?>
                    <div class="post-tags mt-8 pt-8 border-t border-gray-700">
                        <h4 class="text-lg font-bold text-white mb-4">Tags</h4>
                        <div class="flex flex-wrap gap-2">
                            <?php
                            $tags = get_the_tags();
                            if ($tags) {
                                foreach ($tags as $tag) {
                                    echo '<span class="bg-tecPrimary text-tecGold px-3 py-1 rounded-full text-sm border border-tecSecondary/30">' . esc_html($tag->name) . '</span>';
                                }
                            }
                            ?>
                        </div>
                    </div>
                <?php endif; ?>
            </article>
            
            <!-- Author Bio -->
            <?php $author_bio = get_the_author_meta('description'); ?>
            <?php if ($author_bio) : ?>
                <div class="author-bio mt-12 p-8 bg-tecPrimary rounded-xl border border-tecSecondary/30">
                    <div class="flex items-start gap-6">
                        <div class="author-avatar">
                            <?php echo get_avatar(get_the_author_meta('ID'), 80, '', '', array('class' => 'rounded-full')); ?>
                        </div>
                        <div>
                            <h4 class="text-xl font-bold text-white mb-2">About <?php the_author(); ?></h4>
                            <p class="text-gray-300"><?php echo esc_html($author_bio); ?></p>
                        </div>
                    </div>
                </div>
            <?php endif; ?>
            
            <!-- Navigation -->
            <div class="post-navigation mt-12 grid md:grid-cols-2 gap-6">
                <?php
                $prev_post = get_previous_post();
                $next_post = get_next_post();
                ?>
                
                <?php if ($prev_post) : ?>
                    <div class="prev-post bg-tecPrimary p-6 rounded-xl border border-tecSecondary/30 hover:border-tecGold/50 transition">
                        <div class="text-sm text-gray-400 mb-2">
                            <i class="fas fa-chevron-left mr-2"></i>Previous Post
                        </div>
                        <a href="<?php echo get_permalink($prev_post); ?>" class="text-white hover:text-tecGold transition">
                            <h5 class="font-bold"><?php echo get_the_title($prev_post); ?></h5>
                        </a>
                    </div>
                <?php endif; ?>
                
                <?php if ($next_post) : ?>
                    <div class="next-post bg-tecPrimary p-6 rounded-xl border border-tecSecondary/30 hover:border-tecGold/50 transition text-right">
                        <div class="text-sm text-gray-400 mb-2">
                            Next Post<i class="fas fa-chevron-right ml-2"></i>
                        </div>
                        <a href="<?php echo get_permalink($next_post); ?>" class="text-white hover:text-tecGold transition">
                            <h5 class="font-bold"><?php echo get_the_title($next_post); ?></h5>
                        </a>
                    </div>
                <?php endif; ?>
            </div>
            
            <!-- Comments -->
            <?php if (comments_open() || get_comments_number()) : ?>
                <div class="comments-section mt-12 p-8 bg-tecPrimary rounded-xl border border-tecSecondary/30">
                    <?php comments_template(); ?>
                </div>
            <?php endif; ?>
        </div>
    </section>
    
    <!-- Related Posts -->
    <section class="related-posts py-16 px-4 bg-tecPrimary">
        <div class="container mx-auto max-w-6xl">
            <h3 class="text-2xl font-bold text-white text-center mb-12">Related Transmissions</h3>
            
            <div class="grid md:grid-cols-3 gap-8">
                <?php
                // Get related posts by category
                $categories = get_the_category();
                if ($categories) {
                    $category_ids = array();
                    foreach ($categories as $category) {
                        $category_ids[] = $category->term_id;
                    }
                    
                    $related_posts = get_posts(array(
                        'category__in' => $category_ids,
                        'post__not_in' => array(get_the_ID()),
                        'numberposts' => 3,
                        'post_status' => 'publish'
                    ));
                    
                    if ($related_posts) {
                        foreach ($related_posts as $related_post) {
                            setup_postdata($related_post);
                            ?>
                            <div class="related-post bg-tecDark rounded-xl overflow-hidden border border-tecSecondary/30 hover:border-tecGold/50 transition">
                                <?php if (has_post_thumbnail($related_post->ID)) : ?>
                                    <div class="post-thumbnail">
                                        <a href="<?php echo get_permalink($related_post); ?>">
                                            <?php echo get_the_post_thumbnail($related_post->ID, 'medium', array('class' => 'w-full h-48 object-cover')); ?>
                                        </a>
                                    </div>
                                <?php endif; ?>
                                
                                <div class="p-6">
                                    <h4 class="text-lg font-bold text-white mb-3">
                                        <a href="<?php echo get_permalink($related_post); ?>" class="hover:text-tecGold transition">
                                            <?php echo get_the_title($related_post); ?>
                                        </a>
                                    </h4>
                                    <p class="text-gray-400 text-sm mb-4">
                                        <?php echo wp_trim_words(get_the_excerpt($related_post), 15); ?>
                                    </p>
                                    <a href="<?php echo get_permalink($related_post); ?>" class="text-tecGold hover:text-white transition text-sm font-bold">
                                        Read More <i class="fas fa-arrow-right ml-1"></i>
                                    </a>
                                </div>
                            </div>
                            <?php
                        }
                        wp_reset_postdata();
                    }
                }
                ?>
            </div>
        </div>
    </section>
</div>

<style>
/* Single Post Styles */
.prose {
    color: inherit;
}

.prose h1,
.prose h2,
.prose h3,
.prose h4,
.prose h5,
.prose h6 {
    font-family: 'Orbitron', sans-serif;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #ffffff;
    margin-top: 2rem;
    margin-bottom: 1rem;
}

.prose p {
    margin-bottom: 1.5rem;
    line-height: 1.7;
}

.prose blockquote {
    border-left: 4px solid #f9a826;
    background: rgba(26, 10, 46, 0.5);
    padding: 1rem 1.5rem;
    margin: 2rem 0;
    border-radius: 0 8px 8px 0;
}

.prose code {
    background: rgba(26, 10, 46, 0.8);
    color: #f9a826;
    padding: 0.2rem 0.4rem;
    border-radius: 4px;
    font-size: 0.9em;
}

.prose pre {
    background: rgba(26, 10, 46, 0.8);
    padding: 1.5rem;
    border-radius: 8px;
    overflow-x: auto;
    border: 1px solid rgba(122, 0, 255, 0.3);
}

.prose a {
    color: #f9a826;
    text-decoration: none;
    transition: color 0.3s ease;
}

.prose a:hover {
    color: #ffffff;
}

.prose ul,
.prose ol {
    margin: 1.5rem 0;
    padding-left: 2rem;
}

.prose li {
    margin-bottom: 0.5rem;
}

/* Comment styles */
.comments-section .comment-list {
    list-style: none;
    padding: 0;
}

.comments-section .comment {
    background: rgba(26, 10, 46, 0.3);
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    border: 1px solid rgba(122, 0, 255, 0.2);
}

.comments-section .comment-author {
    font-weight: bold;
    color: #f9a826;
    margin-bottom: 0.5rem;
}

.comments-section .comment-content {
    color: #e5e5e5;
    line-height: 1.6;
}

/* Load fonts if not already loaded */
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

<?php get_footer(); ?>
