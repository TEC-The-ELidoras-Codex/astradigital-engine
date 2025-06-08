<?php
/**
 * Template for displaying comments
 *
 * @package TEC
 * @subpackage AstradigitalEngine
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

/*
 * If the current post is protected by a password and
 * the visitor has not yet entered the password we will
 * return early without loading the comments.
 */
if (post_password_required()) {
    return;
}
?>

<div id="comments" class="comments-area">
    <?php if (have_comments()): ?>        <h3 class="tec-comments-title">
            <i class="icon-comments"></i>
            <?php
            $comments_number = get_comments_number();
            if ($comments_number == 1) {
                echo '1 Transmission Received';
            } else {
                echo $comments_number . ' Transmissions Received';
            }
            ?>
        </h3>

        <ol class="comment-list space-y-6 mb-12">
            <?php
            wp_list_comments(array(
                'style'       => 'ol',
                'short_ping'  => true,
                'avatar_size' => 60,
                'callback'    => 'tec_custom_comment',
            ));
            ?>
        </ol>

        <?php
        // Display comment navigation
        $prev_link = get_previous_comments_link('← Previous Transmissions');
        $next_link = get_next_comments_link('Next Transmissions →');
        
        if ($prev_link || $next_link): ?>            <nav class="tec-comment-navigation">
                <div class="tec-nav-previous">
                    <?php if ($prev_link): ?>
                        <?php echo str_replace('<a ', '<a class="tec-nav-link" ', $prev_link); ?>
                    <?php endif; ?>
                </div>
                <div class="tec-nav-next">
                    <?php if ($next_link): ?>
                        <?php echo str_replace('<a ', '<a class="tec-nav-link" ', $next_link); ?>
                    <?php endif; ?>
                </div>
            </nav>
        <?php endif;
    endif; ?>

    <?php if (!comments_open() && get_comments_number() && post_type_supports(get_post_type(), 'comments')): ?>        <div class="tec-no-comments">
            <i class="icon-lock"></i>
            <p class="tec-no-comments-text">Transmission channels are currently closed for this dispatch.</p>
        </div>
    <?php endif; ?>

    <?php
    // Comment form
    if (comments_open()):
        $commenter = wp_get_current_commenter();
        $req = get_option('require_name_email');
        $aria_req = ($req ? ' aria-required="true"' : '');
          $comment_form_args = array(
            'title_reply' => '<i class="icon-broadcast-tower"></i>Transmit Your Signal',
            'title_reply_to' => 'Respond to %s',
            'cancel_reply_link' => 'Cancel Transmission',
            'label_submit' => 'Send Transmission',
            'comment_field' => '<div class="tec-comment-field">
                <label for="comment" class="tec-form-label">Your Message <span class="tec-required">*</span></label>
                <textarea id="comment" name="comment" rows="6" aria-required="true" placeholder="Encode your transmission..." class="tec-textarea"></textarea>
            </div>',
            'fields' => array(
                'author' => '<div class="tec-form-field">
                    <label for="author" class="tec-form-label">Agent ID ' . ($req ? '<span class="tec-required">*</span>' : '') . '</label>
                    <input id="author" name="author" type="text" value="' . esc_attr($commenter['comment_author']) . '" placeholder="Your callsign..." class="tec-input"' . $aria_req . ' />
                </div>',
                'email' => '<div class="tec-form-field">
                    <label for="email" class="tec-form-label">Secure Channel ' . ($req ? '<span class="tec-required">*</span>' : '') . '</label>
                    <input id="email" name="email" type="email" value="' . esc_attr($commenter['comment_author_email']) . '" placeholder="your.channel@astradigital.ocean" class="tec-input"' . $aria_req . ' />
                </div>',
                'url' => '<div class="tec-form-field">
                    <label for="url" class="tec-form-label">Data Node</label>
                    <input id="url" name="url" type="url" value="' . esc_attr($commenter['comment_author_url']) . '" placeholder="https://your.node.address" class="tec-input" />
                </div>',
            ),
            'class_submit' => 'tec-btn tec-btn-primary',
            'submit_button' => '<button type="submit" id="%2$s" class="%3$s"><i class="icon-satellite-dish"></i>%4$s</button>',
            'comment_notes_before' => '<div class="tec-comment-notes">
                <i class="icon-shield-alt"></i>
                <span class="tec-notes-text">Your transmission will be encrypted and verified before broadcast to the network.</span>
            </div>',
            'comment_notes_after' => '',
            'class_form' => 'tec-comment-form',
            'title_reply_before' => '<h3 id="reply-title" class="comment-reply-title text-2xl font-bold text-white mb-6 font-orbitron uppercase">',
            'title_reply_after' => '</h3>',
        );
        
        comment_form($comment_form_args);
    endif;
    ?>
</div>

<?php
// Custom comment callback function
if (!function_exists('tec_custom_comment')):
    function tec_custom_comment($comment, $args, $depth) {
        $GLOBALS['comment'] = $comment;
        ?>
        <li <?php comment_class('comment-item bg-tecPrimary/40 backdrop-blur-md rounded-xl p-6 border border-tecSecondary/30'); ?> id="comment-<?php comment_ID(); ?>">
            <article class="comment-body">
                <div class="comment-meta flex items-start gap-4 mb-4">
                    <div class="comment-avatar flex-shrink-0">
                        <?php 
                        $avatar = get_avatar($comment, 60, '', '', array('class' => 'rounded-lg border-2 border-tecGold/30'));
                        echo $avatar;
                        ?>
                    </div>
                    
                    <div class="comment-metadata flex-1">
                        <div class="comment-author-name text-white font-bold mb-1">
                            <?php 
                            $author_name = get_comment_author();
                            if (get_comment_author_url()) {
                                echo '<a href="' . esc_url(get_comment_author_url()) . '" class="text-tecGold hover:text-white transition">' . esc_html($author_name) . '</a>';
                            } else {
                                echo esc_html($author_name);
                            }
                            ?>
                            
                            <?php if (user_can(get_comment()->user_id, 'administrator')): ?>
                                <span class="admin-badge bg-tecGold text-tecDark px-2 py-1 rounded-full text-xs font-bold ml-2">
                                    <i class="fas fa-crown mr-1"></i>ADMIN
                                </span>
                            <?php elseif (get_comment()->user_id == get_post()->post_author): ?>
                                <span class="author-badge bg-tecAccent text-white px-2 py-1 rounded-full text-xs font-bold ml-2">
                                    <i class="fas fa-pen mr-1"></i>AUTHOR
                                </span>
                            <?php endif; ?>
                        </div>
                        
                        <div class="comment-date-link text-gray-400 text-sm flex items-center">
                            <i class="fas fa-satellite mr-1"></i>
                            <a href="<?php echo esc_url(get_comment_link($comment, $args)); ?>" class="hover:text-tecGold transition">
                                <time datetime="<?php comment_time('c'); ?>">
                                    <?php
                                    $time_difference = human_time_diff(get_comment_time('U'), current_time('timestamp'));
                                    echo $time_difference . ' ago';
                                    ?>
                                </time>
                            </a>
                            
                            <?php if (get_comment_meta(get_comment_ID(), 'location', true)): ?>
                                <span class="comment-location ml-4 text-tecGold">
                                    <i class="fas fa-map-marker-alt mr-1"></i>
                                    <?php echo esc_html(get_comment_meta(get_comment_ID(), 'location', true)); ?>
                                </span>
                            <?php endif; ?>
                        </div>
                    </div>
                    
                    <div class="comment-actions flex-shrink-0">
                        <?php
                        edit_comment_link(
                            '<i class="fas fa-edit"></i>',
                            '<span class="edit-link text-gray-400 hover:text-tecGold transition mr-2">',
                            '</span>'
                        );
                        
                        comment_reply_link(array_merge($args, array(
                            'add_below' => 'comment',
                            'depth'     => $depth,
                            'max_depth' => $args['max_depth'],
                            'before'    => '<span class="reply-link text-tecGold hover:text-white transition">',
                            'after'     => '</span>',
                            'reply_text' => '<i class="fas fa-reply mr-1"></i>Reply'
                        )));
                        ?>
                    </div>
                </div>
                
                <?php if (get_comment()->comment_approved == '0'): ?>
                    <div class="comment-awaiting-moderation bg-tecDark/50 p-3 rounded-lg mb-4 border border-yellow-500/30">
                        <i class="fas fa-clock text-yellow-500 mr-2"></i>
                        <span class="text-yellow-400 text-sm">Your transmission is being verified by TEC3 protocols.</span>
                    </div>
                <?php endif; ?>
                
                <div class="comment-content text-gray-300 leading-relaxed">
                    <?php comment_text(); ?>
                </div>
            </article>
        </li>
        <?php
    }
endif;
?>
