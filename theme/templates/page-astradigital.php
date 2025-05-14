<?php
/**
 * Template Name: Astradigital Ocean
 * Description: Main page template for the Astradigital Ocean experience
 *
 * @package TEC
 * @subpackage AstradigitalEngine
 */

get_header(); ?>

<div class="astradigital-container">
    <div class="astra-header">
        <h1 class="astra-title"><?php echo get_the_title(); ?></h1>
        <div class="astra-navigation">
            <!-- Main navigation for Astradigital Ocean -->
            <?php get_template_part( 'templates/parts/navigation', 'astradigital' ); ?>
        </div>
    </div>
    
    <div class="astra-main-content">
        <div class="astra-ocean-visual">
            <!-- 3D visualization or imagery of the Astradigital Ocean -->
            <div class="ocean-backdrop"></div>
            <div class="interactive-elements">
                <!-- Interactive elements will be populated via JS -->
            </div>
        </div>
        
        <div class="astra-factions">
            <h2>Factions of the Astradigital Ocean</h2>
            <div class="faction-container">
                <!-- Faction elements will be loaded dynamically -->
                <?php get_template_part( 'templates/parts/content', 'factions' ); ?>
            </div>
        </div>
        
        <div class="astra-characters">
            <h2>Featured Characters</h2>
            <div class="character-container">
                <!-- Character profiles will be loaded dynamically -->
                <?php get_template_part( 'templates/parts/content', 'characters' ); ?>
            </div>
        </div>
    </div>
    
    <div class="astra-footer">
        <div class="footer-navigation">
            <?php get_template_part( 'templates/parts/navigation', 'footer' ); ?>
        </div>
        <div class="copyright">
            &copy; <?php echo date('Y'); ?> The Elidoras Codex | All rights reserved
        </div>
    </div>
</div>

<?php get_footer(); ?>
