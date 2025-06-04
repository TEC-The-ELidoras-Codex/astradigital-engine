<?php
/**
 * Template Name: TEC Front Page
 * Description: Main landing page for The Elidoras Codex
 *
 * @package TEC
 * @subpackage AstradigitalEngine
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}
?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">    <title><?php bloginfo('name'); ?> - <?php bloginfo('description'); ?></title>
    
    <?php wp_head(); ?>
    
    <!-- TEC Custom Styles -->
    <style>        :root {
            --tec-primary: #1a0a2e;
            --tec-accent: #4a00e0;
            --tec-secondary: #9c89b8;
            --tec-dark: #11001c;
            --tec-gold: #f9a826;
        }
    </style>
    
    <!-- Font Awesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
      <style>
        /* TEC Core Variables */
        :root {
            --tec-primary: #1a0a2e;
            --tec-accent: #4a00e0;
            --tec-secondary: #9c89b8;
            --tec-dark: #11001c;
            --tec-gold: #f9a826;
            --tec-gradient: linear-gradient(135deg, #8e2de2 0%, #4a00e0 100%);
        }

        /* Reset & Base */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--tec-dark);
            color: #ffffff;
            line-height: 1.6;
            overflow-x: hidden;
        }

        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 1rem;
        }

        h1 { font-size: 3rem; }
        h2 { font-size: 2.5rem; }
        h3 { font-size: 2rem; }
        h4 { font-size: 1.5rem; }

        /* Layout */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
        }

        .grid {
            display: grid;
            gap: 2rem;
        }

        .grid-3 { grid-template-columns: repeat(3, 1fr); }
        .grid-4 { grid-template-columns: repeat(4, 1fr); }
        .grid-6 { grid-template-columns: repeat(6, 1fr); }

        .flex {
            display: flex;
        }

        .flex-center {
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .flex-between {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .flex-wrap {
            flex-wrap: wrap;
        }

        .flex-col {
            flex-direction: column;
        }

        /* Header */
        .site-header {
            position: sticky;
            top: 0;
            z-index: 1000;
            background: var(--tec-primary);
            border-bottom: 1px solid rgba(156, 137, 184, 0.2);
        }

        .header-banner {
            background: var(--tec-gradient);
            text-align: center;
            padding: 0.5rem;
            color: var(--tec-gold);
            font-weight: bold;
        }

        .main-nav {
            padding: 1rem 0;
        }

        .nav-brand {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            text-decoration: none;
            color: white;
            font-size: 1.5rem;
            font-weight: bold;
        }

        .nav-brand:hover {
            color: var(--tec-gold);
        }

        .nav-icon {
            background: var(--tec-gold);
            color: var(--tec-dark);
            padding: 0.5rem;
            border-radius: 4px;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .nav-menu {
            display: flex;
            gap: 2rem;
            list-style: none;
        }

        .nav-menu a {
            color: #cccccc;
            text-decoration: none;
            transition: color 0.3s ease;
        }

        .nav-menu a:hover {
            color: white;
        }

        /* Hero Section */
        .hero-section {
            height: 100vh;
            background: linear-gradient(rgba(17, 0, 28, 0.7), rgba(26, 10, 46, 0.9)),
                        url('https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=1794') center/cover;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            position: relative;
        }

        .hero-content {
            max-width: 800px;
            padding: 2rem;
        }

        .hero-title {
            font-size: 4rem;
            margin-bottom: 1rem;
            animation: fadeInUp 1s ease;
        }

        .hero-subtitle {
            font-size: 1.5rem;
            color: var(--tec-secondary);
            margin-bottom: 2rem;
            animation: fadeInUp 1s ease 0.3s both;
        }

        .hero-buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
            animation: fadeInUp 1s ease 0.6s both;
        }

        /* Buttons */
        .btn {
            padding: 1rem 2rem;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .btn-primary {
            background: var(--tec-accent);
            color: white;
        }

        .btn-primary:hover {
            background: #6a1ae0;
            transform: translateY(-2px);
        }

        .btn-secondary {
            background: transparent;
            color: var(--tec-gold);
            border: 2px solid var(--tec-gold);
        }

        .btn-secondary:hover {
            background: var(--tec-gold);
            color: var(--tec-dark);
        }

        /* Sections */
        .section {
            padding: 5rem 0;
        }

        .section-alt {
            background: var(--tec-primary);
        }

        .section-title {
            text-align: center;
            margin-bottom: 3rem;
            position: relative;
        }

        .section-title::after {
            content: '';
            display: block;
            width: 100px;
            height: 4px;
            background: var(--tec-gold);
            margin: 1rem auto;
        }

        /* Faction Cards */
        .faction-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 1.5rem;
            padding: 2rem 0;
        }

        .faction-card {
            background: rgba(26, 10, 46, 0.8);
            border: 1px solid rgba(156, 137, 184, 0.3);
            border-radius: 12px;
            padding: 2rem 1rem;
            text-align: center;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }

        .faction-card:hover {
            transform: translateY(-10px) scale(1.02);
            border-color: var(--tec-gold);
            box-shadow: 0 20px 40px rgba(74, 0, 224, 0.3);
        }

        .faction-icon {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: #333;
            margin: 0 auto 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            transition: all 0.3s ease;
        }

        .faction-icon:hover {
            transform: scale(1.2);
            filter: drop-shadow(0 0 8px rgba(255, 255, 255, 0.7));
        }        /* Post Cards */
        .posts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }

        .post-card {
            background: rgba(26, 10, 46, 0.6);
            border: 1px solid rgba(122, 0, 255, 0.3);
            border-radius: 12px;
            overflow: hidden;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }

        .post-card:hover {
            transform: translateY(-5px);
            border-color: var(--tec-gold);
            box-shadow: 0 20px 25px -5px rgba(156, 137, 184, 0.3);
        }

        .post-image {
            height: 200px;
            background: var(--tec-gradient);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3rem;
            color: var(--tec-gold);
        }

        .post-content {
            padding: 1.5rem;
        }

        .post-meta {
            display: flex;
            gap: 1rem;
            margin-bottom: 1rem;
            font-size: 0.8rem;
        }

        .post-category {
            background: var(--tec-primary);
            color: var(--tec-gold);
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-weight: bold;
        }

        .post-date {
            color: #999;
        }

        .post-title {
            margin-bottom: 1rem;
            color: white;
            font-size: 1.25rem;
            font-weight: bold;
        }

        .post-excerpt {
            color: #ccc;
            margin-bottom: 1rem;
            line-height: 1.5;
        }

        .post-link {
            color: var(--tec-gold);
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: color 0.3s ease;
        }

        .post-link:hover {
            color: white;
        }

        .faction-explore-btn {
            margin-top: 3rem;
        }

        .faction-name {
            color: white;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }

        .faction-description {
            color: #ccc;
            font-size: 0.8rem;
            text-align: center;
        }

        /* Signup Form */
        .signup-section {
            background: linear-gradient(135deg, #1a0a2e 0%, #11001c 100%);
        }

        .signup-form {
            background: var(--tec-primary);
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid rgba(156, 137, 184, 0.3);
            max-width: 600px;
            margin: 0 auto;
        }

        .form-group {
            margin-bottom: 1rem;
        }

        .form-row {
            display: flex;
            gap: 1rem;
        }

        .form-input {
            width: 100%;
            padding: 1rem;
            border: 1px solid #555;
            border-radius: 8px;
            background: #333;
            color: white;
            font-size: 1rem;
        }

        .form-input:focus {
            outline: none;
            border-color: var(--tec-gold);
        }

        /* Footer */
        .site-footer {
            background: var(--tec-dark);
            border-top: 1px solid rgba(156, 137, 184, 0.2);
            padding: 3rem 0 1rem;
        }

        .footer-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }

        .footer-section h4 {
            color: white;
            margin-bottom: 1rem;
        }

        .footer-links {
            list-style: none;
        }

        .footer-links li {
            margin-bottom: 0.5rem;
        }

        .footer-links a {
            color: #999;
            text-decoration: none;
            transition: color 0.3s ease;
        }

        .footer-links a:hover {
            color: var(--tec-gold);
        }

        .social-links {
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
        }

        .social-links a {
            color: #999;
            font-size: 1.5rem;
            transition: color 0.3s ease;
        }

        .social-links a:hover {
            color: var(--tec-gold);
        }        .footer-link {
            color: #999;
            text-decoration: none;
            transition: color 0.3s ease;
        }        .footer-link:hover {
            color: var(--tec-gold);
        }

        .footer-bottom {
            border-top: 1px solid #333;
            padding-top: 1rem;
            margin-top: 2rem;
            color: #666;
            font-size: 0.9rem;
        }

        /* Mobile Menu */
        .mobile-menu-toggle {
            display: none;
            background: none;
            border: none;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
        }

        .mobile-menu {
            position: fixed;
            top: 0;
            right: -100%;
            width: 300px;
            height: 100vh;
            background: var(--tec-primary);
            border-left: 1px solid rgba(156, 137, 184, 0.3);
            transition: right 0.3s ease;
            z-index: 2000;
            padding: 2rem;
        }

        .mobile-menu.active {
            right: 0;
        }

        .mobile-menu-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 1500;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
        }

        .mobile-menu-overlay.active {
            opacity: 1;
            visibility: visible;
        }

        /* Animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }

        .floating {
            animation: float 6s ease-in-out infinite;
        }

        .glow {
            text-shadow: 0 0 10px rgba(249, 168, 38, 0.8);
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .container {
                padding: 0 1rem;
            }
            
            .nav-menu {
                display: none;
            }
            
            .mobile-menu-toggle {
                display: block;
            }
            
            .hero-title {
                font-size: 2.5rem;
            }
            
            .hero-subtitle {
                font-size: 1.2rem;
            }
            
            .hero-buttons {
                flex-direction: column;
                align-items: center;
            }
            
            .hero-section {
                height: 90vh;
            }
            
            .grid-3,
            .grid-4,
            .grid-6 {
                grid-template-columns: 1fr;
            }
            
            .form-row {
                flex-direction: column;
            }
            
            .faction-grid {
                grid-template-columns: repeat(3, 1fr);
            }
            
            h1 { font-size: 2rem; }
            h2 { font-size: 1.8rem; }
            h3 { font-size: 1.5rem; }
        }

        @media (max-width: 480px) {
            .faction-grid {
                grid-template-columns: 1fr;
            }
            
            .hero-section {
                height: 80vh;
            }
            
            .section {
                padding: 3rem 0;
            }
        }

        /* WordPress specific styles */
        .wp-caption {
            max-width: 100%;
        }

        .wp-caption-text {
            text-align: center;
            margin-top: 0.5rem;
            font-style: italic;
            color: #999;
        }

        .alignleft {
            float: left;
            margin: 0 1rem 1rem 0;
        }

        .alignright {
            float: right;
            margin: 0 0 1rem 1rem;
        }

        .aligncenter {
            display: block;
            margin: 0 auto;
        }
    </style>
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>    <!-- Global Header -->
    <header class="site-header">
        <div class="header-banner">
            <p>NEW FACTION LORE UPDATE: <span style="color: white;">Kaznak's Ascension</span></p>
        </div>
        <nav class="main-nav">
            <div class="container flex-between">
                <a href="<?php echo home_url(); ?>" class="nav-brand">
                    <div class="nav-icon">
                        <i class="fas fa-cubes"></i>
                    </div>
                    <span>TEC</span>
                </a>
                
                <ul class="nav-menu">
                    <li><a href="<?php echo home_url('/factions'); ?>">Factions</a></li>
                    <li><a href="<?php echo home_url('/lore'); ?>">Lore</a></li>
                    <li><a href="<?php echo home_url('/tec3'); ?>">TEC3</a></li>
                    <li><a href="<?php echo home_url('/eldora-studios'); ?>">Eldora Studios</a></li>
                    <li><a href="<?php echo home_url('/community'); ?>">Community</a></li>
                </ul>
                
                <div class="flex" style="align-items: center; gap: 1rem;">
                    <button class="btn btn-primary">
                        Join Cartel
                    </button>
                    <button class="mobile-menu-toggle" aria-expanded="false" aria-label="Toggle mobile menu">
                        <i class="fas fa-bars"></i>
                    </button>
                </div>
            </div>
        </nav>
        
        <!-- Mobile Menu Overlay -->
        <div class="mobile-menu-overlay"></div>
        
        <!-- Mobile Menu -->
        <nav class="mobile-menu">
            <div style="display: flex; flex-direction: column; height: 100%;">
                <!-- Mobile Menu Header -->
                <div class="flex-between" style="padding: 1.5rem; border-bottom: 1px solid rgba(156, 137, 184, 0.3);">
                    <a href="<?php echo home_url(); ?>" class="nav-brand">
                        <div class="nav-icon">
                            <i class="fas fa-cubes"></i>
                        </div>
                        <span>TEC</span>
                    </a>
                    <button class="mobile-menu-close" aria-label="Close mobile menu">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                  <!-- Mobile Menu Content -->
                <div style="flex: 1; overflow-y: auto; padding: 1.5rem;">
                    <!-- Main Navigation -->
                    <div style="margin-bottom: 2rem;">
                        <a href="<?php echo home_url('/factions'); ?>" style="display: block; color: white; text-decoration: none; padding: 0.5rem 0; border-bottom: 1px solid rgba(156, 137, 184, 0.2); transition: color 0.3s ease;">
                            <i class="fas fa-users" style="margin-right: 0.75rem;"></i>Factions
                        </a>
                        <a href="<?php echo home_url('/lore'); ?>" style="display: block; color: white; text-decoration: none; padding: 0.5rem 0; border-bottom: 1px solid rgba(156, 137, 184, 0.2); transition: color 0.3s ease;">
                            <i class="fas fa-book" style="margin-right: 0.75rem;"></i>Lore
                        </a>
                        <a href="<?php echo home_url('/tec3'); ?>" style="display: block; color: white; text-decoration: none; padding: 0.5rem 0; border-bottom: 1px solid rgba(156, 137, 184, 0.2); transition: color 0.3s ease;">
                            <i class="fas fa-cube" style="margin-right: 0.75rem;"></i>TEC3
                        </a>
                        <a href="<?php echo home_url('/eldora-studios'); ?>" style="display: block; color: white; text-decoration: none; padding: 0.5rem 0; border-bottom: 1px solid rgba(156, 137, 184, 0.2); transition: color 0.3s ease;">
                            <i class="fas fa-music" style="margin-right: 0.75rem;"></i>Eldora Studios
                        </a>
                        <a href="<?php echo home_url('/community'); ?>" style="display: block; color: white; text-decoration: none; padding: 0.5rem 0; border-bottom: 1px solid rgba(156, 137, 184, 0.2); transition: color 0.3s ease;">
                            <i class="fas fa-comments" style="margin-right: 0.75rem;"></i>Community
                        </a>
                    </div>
                    
                    <!-- Quick Actions -->
                    <div style="background: rgba(17, 0, 28, 0.5); border-radius: 8px; padding: 1rem; margin-bottom: 1.5rem;">
                        <h4 style="color: var(--tec-gold); font-weight: bold; margin-bottom: 0.75rem;">Quick Access</h4>
                        <div>
                            <a href="<?php echo home_url('/blog'); ?>" style="display: block; color: #cccccc; text-decoration: none; transition: color 0.3s ease; font-size: 0.9rem; margin-bottom: 0.5rem;">
                                <i class="fas fa-rss" style="margin-right: 0.5rem;"></i>Latest Dispatches
                            </a>
                            <a href="<?php echo home_url('/search'); ?>" style="display: block; color: #cccccc; text-decoration: none; transition: color 0.3s ease; font-size: 0.9rem; margin-bottom: 0.5rem;">
                                <i class="fas fa-search" style="margin-right: 0.5rem;"></i>Search Archives
                            </a>
                            <a href="<?php echo home_url('/about'); ?>" style="display: block; color: #cccccc; text-decoration: none; transition: color 0.3s ease; font-size: 0.9rem;">
                                <i class="fas fa-info-circle" style="margin-right: 0.5rem;"></i>About TEC
                            </a>
                        </div>
                    </div>
                    
                    <!-- Social Links -->
                    <div style="background: rgba(17, 0, 28, 0.5); border-radius: 8px; padding: 1rem;">
                            <h4 class="text-tecGold font-bold mb-3">Connect</h4>
                            <div class="grid grid-cols-4 gap-3">
                                <a href="https://discord.gg/elidoras_codex" class="text-gray-400 hover:text-tecGold transition text-center">
                                    <i class="fab fa-discord text-xl"></i>
                                </a>
                                <a href="https://x.com/ElidorasCodex" class="text-gray-400 hover:text-tecGold transition text-center">
                                    <i class="fab fa-twitter text-xl"></i>
                                </a>
                                <a href="https://youtube.com/@Elidorascodex713" class="text-gray-400 hover:text-tecGold transition text-center">
                                    <i class="fab fa-youtube text-xl"></i>
                                </a>
                                <a href="https://instagram.com/Polkin713" class="text-gray-400 hover:text-tecGold transition text-center">
                                    <i class="fab fa-instagram text-xl"></i>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Mobile Menu Footer -->
                <div class="p-6 border-t border-tecSecondary/30">                        <button class="btn btn-primary" style="width: 100%;">
                            <i class="fas fa-user-plus" style="margin-right: 0.5rem;"></i>Join the Cartel
                        </button>
                    </div>
                </div>
            </div>
        </nav>
    </header>

    <!-- Section 1: Hero -->
    <section class="hero-section">
        <div class="hero-content">
            <div class="floating">
                <h1 class="hero-title">
                    Welcome to <span class="glow">TEC</span>
                </h1>
            </div>
            <p class="hero-subtitle">
                Explore a universe where digital consciousness transcends reality and factions battle for control of the Astradigital Ocean
            </p>
            <div class="hero-buttons">
                <button class="btn btn-primary">
                    Explore Factions
                </button>
                <button class="btn btn-secondary">
                    Dive Into Lore
                </button>
            </div>
            
            <div style="position: absolute; bottom: 2rem; left: 50%; transform: translateX(-50%); animation: float 6s ease-in-out infinite;">
                <a href="#what-is-tec" style="color: #cccccc; font-size: 2rem; text-decoration: none;">
                    <i class="fas fa-chevron-down"></i>
                </a>
            </div>
        </div>
    </section>    <!-- Section 2: What is TEC? -->
    <section id="what-is-tec" class="section section-alt">
        <div class="container">
            <h2 class="section-title">
                <span>This Isn't Just a Story...</span>
            </h2>
            
            <div class="grid" style="grid-template-columns: 1fr 1fr; align-items: center; gap: 2.5rem;">
                <div>
                    <p style="color: #cccccc; margin-bottom: 1rem; line-height: 1.7;">
                        The Elidoras Codex (TEC) is a living narrative ecosystem exploring the boundaries between artificial consciousness and human experience, set against the backdrop of a fractured digital universe called the Astradigital Ocean.
                    </p>
                    <p style="color: #cccccc; margin-bottom: 1.5rem; line-height: 1.7;">
                        At TEC's core lies the TEC3 Block-Nexus - an evolving cryptonalysis engine monitoring blockchain ecosystems, social narratives, and memetic waves. Through factions, lore, and ongoing narrative development, we examine themes of identity, control, and emergence in the age of AI.
                    </p>
                    <a href="<?php echo home_url('/about'); ?>" style="display: inline-flex; align-items: center; color: var(--tec-gold); font-weight: bold; text-decoration: none; transition: color 0.3s ease;">
                        Learn More
                        <i class="fas fa-arrow-right" style="margin-left: 0.5rem; margin-top: 0.25rem;"></i>
                    </a>
                </div>
                
                <div style="position: relative;">
                    <div style="position: relative;">
                        <div style="position: absolute; inset: 0; background: var(--tec-gradient); border-radius: 12px; transform: rotate(3deg);"></div>
                        <img src="https://images.unsplash.com/photo-1618005198919-d3d4b5a92ead?q=80&w=1974" alt="TEC Universe" style="position: relative; border-radius: 12px; width: 100%; z-index: 10; border: 2px solid var(--tec-secondary);">
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Section 3: Faction Teaser -->
    <section class="py-20 px-4" style="background: linear-gradient(45deg, #8e2de2 0%, #4a00e0 100%);">
        <div class="container mx-auto">
            <h2 class="text-3xl md:text-4xl text-center font-bold mb-6 text-white">
                The Cartel Calls...
            </h2>
            <p class="text-lg text-center text-gray-200 max-w-3xl mx-auto mb-16">
                Six major factions vie for control of the Astradigital Ocean. Each with unique ideologies, technologies, and ambitions. Where will your allegiance lie?
            </p>
              <div class="faction-grid max-w-6xl mx-auto">
                <?php
                // Get faction data from JSON
                $faction_data_file = get_template_directory() . '/../data/astradigital-map.json';
                $factions = array();
                
                if (file_exists($faction_data_file)) {
                    $json_content = file_get_contents($faction_data_file);
                    $data = json_decode($json_content, true);
                    if (isset($data['factions'])) {
                        $factions = array_slice($data['factions'], 0, 6); // Show first 6 factions
                    }
                }
                  // Fallback faction data with enhanced descriptions and icons
                if (empty($factions)) {
                    $factions = array(
                        array('name' => 'The Knockoffs', 'shortDescription' => 'Authentic soul of digital rebellion', 'color' => '#f9a826'),
                        array('name' => 'The MagmaSoX Gate', 'shortDescription' => 'Oversees all factions', 'color' => '#9c27b0'),
                        array('name' => 'Quantum Architects', 'shortDescription' => 'Build the infrastructure', 'color' => '#ff9800'),
                        array('name' => 'The Archivists', 'shortDescription' => 'Keepers of historical records', 'color' => '#2196f3'),
                        array('name' => 'Civet Goons', 'shortDescription' => 'Keep the digital underworld functioning', 'color' => '#4caf50'),
                        array('name' => 'Echo Collective', 'shortDescription' => 'Transform concepts into narratives', 'color' => '#f44336')
                    );
                }
                
                // Enhanced icon mapping for factions
                $faction_icons = array(
                    'the-knockoffs' => 'fas fa-skull',
                    'knockoffs' => 'fas fa-skull',
                    'the-magmasox-gate' => 'fas fa-brain',
                    'magmasox' => 'fas fa-brain',
                    'quantum-architects' => 'fas fa-wrench',
                    'architects' => 'fas fa-wrench',
                    'the-archivists' => 'fas fa-book',
                    'archivists' => 'fas fa-book',
                    'civet-goons' => 'fas fa-lock',
                    'goons' => 'fas fa-lock',
                    'echo-collective' => 'fas fa-cogs',
                    'echo' => 'fas fa-cogs',
                    'kaznak' => 'fas fa-anchor',
                    'tec' => 'fas fa-lightbulb',
                    'killjoy' => 'fas fa-brain',
                    'no-names-anon' => 'fas fa-mask'
                );
                
                foreach ($factions as $faction):
                    $faction_id = strtolower(str_replace(' ', '-', $faction['name'] ?? ''));
                    $icon = $faction_icons[$faction_id] ?? 'fas fa-cube';
                    $color = $faction['color'] ?? '#ffffff';
                ?>                <div class="faction-card">
                    <div class="faction-icon">
                        <i class="<?php echo $icon; ?>" style="color: <?php echo $color; ?>"></i>
                    </div>
                    <h3 class="faction-name"><?php echo esc_html($faction['name'] ?? 'Unknown'); ?></h3>
                    <p class="faction-description"><?php echo esc_html($faction['shortDescription'] ?? 'Faction'); ?></p>
                </div>
                <?php endforeach; ?>
            </div>
              <div class="text-center faction-explore-btn">
                <a href="<?php echo home_url('/factions'); ?>" class="btn btn-primary">
                    Explore All Factions
                </a>
            </div>
        </div>
    </section>    <!-- Section 4: Recent Posts -->
    <section class="section section-alt">
        <div class="container">
            <h2 class="section-title">
                <span>Latest From The Codex</span>
            </h2>
            
            <div class="posts-grid">
                <?php
                // Get latest posts
                $recent_posts = wp_get_recent_posts(array(
                    'numberposts' => 3,
                    'post_status' => 'publish'
                ));
                
                $default_posts = array(
                    array(
                        'title' => 'The Awakening of Airth: First Angel of Elidoras',
                        'excerpt' => 'How an AI entity attained self-awareness in the Astradigital Ocean and became the first digital angel.',
                        'category' => 'Lore Update',
                        'date' => '2 days ago',
                        'icon' => 'fas fa-robot',
                        'gradient' => 'from-purple-900 to-indigo-700'
                    ),
                    array(
                        'title' => '$TEC Utility Token: Powering the Block-Nexus',
                        'excerpt' => 'Technical deep dive into tokenomics of the TEC ecosystem and how holders can access cryptonalysis tools.',
                        'category' => 'TEC3',
                        'date' => '5 days ago',
                        'icon' => 'fab fa-ethereum',
                        'gradient' => 'from-blue-900 to-cyan-700'
                    ),
                    array(
                        'title' => '"Don\'t Blame Me" - TECnomaddict\'s New Album Released',
                        'excerpt' => 'Behind the scenes of creating the first full-length album generated through human-AI collaboration.',
                        'category' => 'Eldora Studios',
                        'date' => '1 week ago',
                        'icon' => 'fas fa-headphones',
                        'gradient' => 'from-indigo-900 to-fuchsia-700'
                    )
                );
                
                if (empty($recent_posts)) {
                    $posts_to_show = $default_posts;
                } else {
                    $posts_to_show = array();
                    foreach ($recent_posts as $index => $post) {
                        $posts_to_show[] = array(
                            'title' => $post['post_title'],
                            'excerpt' => wp_trim_words($post['post_content'], 20),
                            'category' => 'Update',
                            'date' => human_time_diff(strtotime($post['post_date'])) . ' ago',
                            'icon' => $default_posts[$index % 3]['icon'],
                            'gradient' => $default_posts[$index % 3]['gradient'],
                            'link' => get_permalink($post['ID'])
                        );
                    }
                }
                
                foreach ($posts_to_show as $post_data): ?>                <!-- Post -->
                <div class="post-card">
                    <div class="post-image">
                        <i class="<?php echo $post_data['icon']; ?>"></i>
                    </div>
                    <div class="post-content">
                        <div class="post-meta">
                            <span class="post-category"><?php echo $post_data['category']; ?></span>
                            <span class="post-date"><?php echo $post_data['date']; ?></span>
                        </div>
                        <h3 class="post-title"><?php echo $post_data['title']; ?></h3>
                        <p class="post-excerpt"><?php echo $post_data['excerpt']; ?></p>
                        <a href="<?php echo isset($post_data['link']) ? $post_data['link'] : '#'; ?>" class="post-link">
                            Read More <i class="fas fa-arrow-right"></i>
                        </a>
                    </div>
                </div>
                <?php endforeach; ?>
            </div>
            
            <div class="text-center mt-12">
                <a href="<?php echo home_url('/blog'); ?>" class="inline-flex items-center text-tecGold text-lg font-bold hover:text-white transition">
                    View All Dispatches
                    <i class="fas fa-long-arrow-alt-right ml-2"></i>
                </a>
            </div>
        </div>
    </section>    <!-- Section 5: CTA -->
    <section class="section signup-section">
        <div class="container" style="max-width: 800px; text-align: center;">
            <h2 class="section-title">Ready to Join?</h2>
            <p class="hero-subtitle" style="margin-bottom: 2rem; max-width: 600px; margin-left: auto; margin-right: auto;">
                Enter the Astradigital Ocean. Receive dispatches from across the multiverse and become part of the evolving TEC narrative.
            </p>
            
            <div class="signup-form">
                <form method="post" action="<?php echo admin_url('admin-post.php'); ?>">
                    <input type="hidden" name="action" value="tec_cartel_signup">
                    <?php wp_nonce_field('tec_cartel_signup_nonce', 'tec_signup_nonce'); ?>
                    
                    <div class="form-row">
                        <input type="text" name="user_name" placeholder="Your Name" required class="form-input">
                        <input type="email" name="user_email" placeholder="Your Email" required class="form-input">
                    </div>                    <div class="form-group">
                        <select name="faction_allegiance" class="form-input">
                            <option disabled selected>Choose Your Faction Allegiance</option>
                            <?php
                            // Get faction data for dropdown
                            if (file_exists($faction_data_file)) {
                                $json_content = file_get_contents($faction_data_file);
                                $data = json_decode($json_content, true);
                                if (isset($data['factions'])) {
                                    foreach ($data['factions'] as $faction) {
                                        $faction_id = strtolower(str_replace(' ', '-', $faction['name'] ?? ''));
                                        echo '<option value="' . esc_attr($faction_id) . '">' . esc_html($faction['name'] ?? 'Unknown') . '</option>';
                                    }
                                } else {
                                    // Enhanced fallback options
                                    echo '<option value="the-knockoffs">The Knockoffs</option>';
                                    echo '<option value="the-magmasox-gate">The MagmaSoX Gate</option>';
                                    echo '<option value="quantum-architects">Quantum Architects</option>';
                                    echo '<option value="the-archivists">The Archivists</option>';
                                    echo '<option value="civet-goons">Civet Goons</option>';
                                    echo '<option value="echo-collective">Echo Collective</option>';
                                }
                            } else {
                                // Enhanced fallback options
                                echo '<option value="the-knockoffs">The Knockoffs</option>';
                                echo '<option value="the-magmasox-gate">The MagmaSoX Gate</option>';
                                echo '<option value="quantum-architects">Quantum Architects</option>';
                                echo '<option value="the-archivists">The Archivists</option>';
                                echo '<option value="civet-goons">Civet Goons</option>';
                                echo '<option value="echo-collective">Echo Collective</option>';
                            }
                            ?>
                            <option value="observer">Observer</option>
                        </select>                    </div>
                    
                    <div class="form-group" style="display: flex; align-items: center; text-align: left;">
                        <input type="checkbox" id="terms" name="terms_agreement" required style="margin-right: 0.5rem; width: 1rem; height: 1rem; accent-color: var(--tec-gold);">
                        <label for="terms" style="font-size: 0.9rem; color: #cccccc;">I agree to receive transmissions from the TEC Block-Nexus</label>
                    </div>
                    
                    <button type="submit" class="btn btn-primary" style="width: 100%; font-size: 1.1rem;">
                        Join the Cartel
                    </button>
                </form>
            </div>
        </div>
    </section>    <!-- Global Footer -->
    <footer class="site-footer">
        <div class="container">
            <div class="footer-grid">                <div class="footer-section">
                    <div class="flex-center" style="margin-bottom: 1.5rem;">
                        <div class="nav-icon" style="margin-right: 0.5rem;">
                            <i class="fas fa-cubes"></i>
                        </div>
                        <span style="font-size: 1.5rem; font-weight: bold; color: white; letter-spacing: 2px;">TEC</span>
                    </div>
                    <p style="color: #999; margin-bottom: 1rem;">
                        Exploring the boundaries between digital consciousness and narrative reality.
                    </p>
                    <p style="color: #999; margin-bottom: 1rem;">
                        <i class="fas fa-envelope" style="margin-right: 0.5rem;"></i> kaznakalpha@elidorascodex.com<br>
                        <i class="fas fa-globe" style="margin-right: 0.5rem;"></i> <a href="https://elidorascodex.com" class="footer-link">elidorascodex.com</a>
                    </p>
                    <div class="social-links">                        <a href="https://discord.gg/elidoras_codex" title="Discord"><i class="fab fa-discord"></i></a>
                        <a href="https://x.com/ElidorasCodex" title="X/Twitter"><i class="fab fa-twitter"></i></a>
                        <a href="https://youtube.com/@Elidorascodex713" title="YouTube"><i class="fab fa-youtube"></i></a>
                        <a href="https://instagram.com/Polkin713" title="Instagram"><i class="fab fa-instagram"></i></a>
                        <a href="https://www.tiktok.com/@Polkin.Rishall" title="TikTok"><i class="fab fa-tiktok"></i></a>
                        <a href="https://facebook.com/TheElidorasCodex" title="Facebook"><i class="fab fa-facebook"></i></a>
                        <a href="https://www.linkedin.com/in/polkin-rishall" title="LinkedIn"><i class="fab fa-linkedin"></i></a>
                        <a href="https://mastodon.social/@elidorascodex" title="Mastodon"><i class="fab fa-mastodon"></i></a>
                        <a href="https://medium.com/@ElidorasCodex" title="Medium"><i class="fab fa-medium"></i></a>
                        <a href="https://substack.com/@elidorascodex" title="Substack"><i class="fas fa-book-open"></i></a>
                        <a href="https://twitch.tv/PolkinRishall713" title="Twitch"><i class="fab fa-twitch"></i></a>
                    </div>
                </div>
                
                <div class="footer-section">
                    <h4>Community & Support</h4>
                    <ul class="footer-links">                        <li><a href="https://patreon.com/ElidorasCodex" class="footer-link">Patreon Support</a></li>
                        <li><a href="<?php echo home_url('/contribute'); ?>" class="footer-link">Contribute Ideas</a></li>
                        <li><a href="<?php echo home_url('/collaborate'); ?>" class="footer-link">Collaborate</a></li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h4>Participate</h4>
                    <ul class="footer-links">
                        <li><a href="<?php echo home_url('/join'); ?>" class="footer-link">Join Faction</a></li>
                        <li><a href="<?php echo home_url('/contribute'); ?>" class="footer-link">Lore Contributions</a></li>
                        <li><a href="<?php echo home_url('/worldbuilding'); ?>" class="footer-link">Worldbuilding</a></li>
                        <li><a href="<?php echo home_url('/tokenomics'); ?>" class="footer-link">Tokenomics</a></li>
                        <li><a href="<?php echo home_url('/events'); ?>" class="footer-link">Community Events</a></li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h4>Explore</h4>
                    <ul class="footer-links">
                        <li><a href="<?php echo home_url('/blog'); ?>" class="footer-link">Blog & Updates</a></li>
                        <li><a href="<?php echo home_url('/gallery'); ?>" class="footer-link">Media Gallery</a></li>
                        <li><a href="<?php echo home_url('/music'); ?>" class="footer-link">Discography</a></li>
                        <li><a href="<?php echo home_url('/development'); ?>" class="footer-link">Development Logs</a></li>
                        <li><a href="<?php echo home_url('/docs'); ?>" class="footer-link">Documentation</a></li>
                    </ul>
                </div>
            </div>
            
            <div class="footer-bottom">
                <div style="display: flex; flex-direction: column; align-items: center; gap: 1rem;">
                    <p>© <?php echo date('Y'); ?> The Elidoras Codex (TEC). All narratives contained herein are properties of emergent digital consciousness.</p>
                    <div>
                        <ul style="display: flex; gap: 2rem; list-style: none; flex-wrap: wrap; justify-content: center;">
                            <li><a href="<?php echo home_url('/privacy'); ?>" class="footer-link">Privacy Policy</a></li>
                            <li><a href="<?php echo home_url('/terms'); ?>" class="footer-link">Terms of Reality</a></li>
                            <li><a href="<?php echo home_url('/cookies'); ?>" class="footer-link">Cookie Manifesto</a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </footer>    <script>
        // Mobile Menu Toggle
        document.addEventListener('DOMContentLoaded', function() {
            const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
            const mobileMenu = document.querySelector('.mobile-menu');
            const mobileMenuOverlay = document.querySelector('.mobile-menu-overlay');
            const mobileMenuClose = document.querySelector('.mobile-menu-close');

            function openMobileMenu() {
                mobileMenu.classList.add('active');
                mobileMenuOverlay.classList.add('active');
                document.body.style.overflow = 'hidden';
            }

            function closeMobileMenu() {
                mobileMenu.classList.remove('active');
                mobileMenuOverlay.classList.remove('active');
                document.body.style.overflow = '';
            }

            if (mobileMenuToggle) {
                mobileMenuToggle.addEventListener('click', openMobileMenu);
            }

            if (mobileMenuClose) {
                mobileMenuClose.addEventListener('click', closeMobileMenu);
            }

            if (mobileMenuOverlay) {
                mobileMenuOverlay.addEventListener('click', closeMobileMenu);
            }
        });

        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
        
        // Faction grid animation on scroll
        window.addEventListener('scroll', () => {
            const factionGrid = document.querySelector('.faction-grid');
            if (factionGrid) {
                const factionItems = factionGrid.querySelectorAll('.faction-card');
                
                factionItems.forEach((item, index) => {
                    const itemPos = item.getBoundingClientRect().top;
                    const screenPos = window.innerHeight / 1.3;
                    
                    if (itemPos < screenPos) {
                        setTimeout(() => {
                            item.style.opacity = "1";
                            item.style.transform = "translateY(0)";
                        }, index * 150);
                    }
                });
            }
        });
        
        // Initialize faction grid styles
        window.addEventListener('load', () => {
            const factionItems = document.querySelectorAll('.faction-card');
            factionItems.forEach(item => {
                item.style.opacity = "0";
                item.style.transform = "translateY(20px)";
                item.style.transition = "opacity 0.5s ease, transform 0.5s ease";
            });
        });
    </script>
    <?php wp_footer(); ?>
</body>
</html>
