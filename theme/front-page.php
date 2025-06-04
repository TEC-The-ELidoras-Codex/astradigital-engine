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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php bloginfo('name'); ?> - <?php bloginfo('description'); ?></title>    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        tecPrimary: '#1a0a2e',
                        tecAccent: '#4a00e0',
                        tecSecondary: '#9c89b8',
                        tecDark: '#11001c',
                        tecGold: '#f9a826',
                    },
                    backgroundImage: {
                        'tec-gradient': 'linear-gradient(135deg, #1a0a2e 0%, #4a00e0 100%)',
                        'faction-gradient': 'linear-gradient(45deg, #8e2de2 0%, #4a00e0 100%)'
                    }
                }
            }
        }
    </script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600;700&display=swap');
        
        body {
            font-family: 'Exo 2', sans-serif;
            background-color: #11001c;
            color: #eaeaea;
            overflow-x: hidden;
        }
        
        h1, h2, h3, h4 {
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .hero-section {
            height: 100vh;
            position: relative;
            background: linear-gradient(rgba(17, 0, 28, 0.7), rgba(26, 10, 46, 0.9)), url('https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=1794') center/cover no-repeat;
        }
        
        .hero-video {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            z-index: -1;
        }
        
        .faction-card {
            transition: all 0.3s ease;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }
        
        .faction-card:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 20px 25px -5px rgba(74, 0, 224, 0.4);
        }
        
        .post-card {
            transition: all 0.3s ease;
            background: rgba(26, 10, 46, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(122, 0, 255, 0.3);
            overflow: hidden;
        }
        
        .post-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 25px -5px rgba(156, 137, 184, 0.3);
            border-color: rgba(122, 0, 255, 0.6);
        }
        
        .glow {
            text-shadow: 0 0 10px rgba(249, 168, 38, 0.8);
        }
        
        .faction-icon {
            width: 80px;
            height: 80px;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }
        
        .faction-icon:hover {
            transform: scale(1.2);
            filter: drop-shadow(0 0 8px rgba(255, 255, 255, 0.7));
        }
        
        .faction-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            gap: 1.5rem;
        }
        
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }
        
        .floating {
            animation: float 6s ease-in-out infinite;
        }
        
        @media (max-width: 768px) {
            .hero-section {
                height: 90vh;
            }
            
            .faction-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }
        
        h1, h2, h3, h4 {
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .hero-section {
            height: 100vh;
            position: relative;
            background: linear-gradient(rgba(17, 0, 28, 0.7), rgba(26, 10, 46, 0.9)), url('https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=1794') center/cover no-repeat;
        }
        
        .hero-video {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            z-index: -1;
        }
        
        .faction-card {
            transition: all 0.3s ease;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }
        
        .faction-card:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 20px 25px -5px rgba(74, 0, 224, 0.4);
        }
        
        .post-card {
            transition: all 0.3s ease;
            background: rgba(26, 10, 46, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(122, 0, 255, 0.3);
            overflow: hidden;
        }
        
        .post-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 25px -5px rgba(156, 137, 184, 0.3);
            border-color: rgba(122, 0, 255, 0.6);
        }
        
        .glow {
            text-shadow: 0 0 10px rgba(249, 168, 38, 0.8);
        }
        
        .faction-icon {
            width: 80px;
            height: 80px;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }
        
        .faction-icon:hover {
            transform: scale(1.2);
            filter: drop-shadow(0 0 8px rgba(255, 255, 255, 0.7));
        }
        
        .faction-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            gap: 1.5rem;
        }
        
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }
        
        .floating {
            animation: float 6s ease-in-out infinite;
        }
        
        @media (max-width: 768px) {
            .hero-section {
                height: 90vh;
            }
            
            .faction-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }
    </style>
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
    <!-- Global Header -->
    <header class="sticky top-0 z-50 bg-tecPrimary">
        <div class="py-2 px-4 bg-gradient-to-r from-purple-900 to-indigo-900 text-center">
            <p class="text-tecGold font-bold tracking-wider">NEW FACTION LORE UPDATE: <span class="text-white">Kaznak's Ascension</span></p>
        </div>
        <nav class="container mx-auto px-4 py-3 flex items-center justify-between">
            <div class="flex items-center space-x-2">
                <div class="bg-tecGold p-2 rounded-md">
                    <i class="fas fa-cubes text-tecDark text-xl"></i>
                </div>
                <span class="text-2xl font-bold text-white tracking-wider">
                    <a href="<?php echo home_url(); ?>" class="text-white hover:text-tecGold transition">TEC</a>
                </span>
            </div>
            
            <div class="hidden md:flex space-x-8">
                <a href="<?php echo home_url('/factions'); ?>" class="text-gray-300 hover:text-white transition">Factions</a>
                <a href="<?php echo home_url('/lore'); ?>" class="text-gray-300 hover:text-white transition">Lore</a>
                <a href="<?php echo home_url('/tec3'); ?>" class="text-gray-300 hover:text-white transition">TEC3</a>
                <a href="<?php echo home_url('/eldora-studios'); ?>" class="text-gray-300 hover:text-white transition">Eldora Studios</a>
                <a href="<?php echo home_url('/community'); ?>" class="text-gray-300 hover:text-white transition">Community</a>
            </div>
              <div class="flex items-center space-x-4">
                <button class="bg-tecAccent hover:bg-purple-700 text-white py-2 px-4 rounded-md transition">
                    Join Cartel
                </button>
                <button class="mobile-menu-toggle md:hidden text-gray-300 hover:text-white transition" aria-expanded="false" aria-label="Toggle mobile menu">
                    <i class="fas fa-bars text-xl"></i>
                </button>
            </div>
        </nav>
        
        <!-- Mobile Menu Overlay -->
        <div class="mobile-menu-overlay fixed inset-0 bg-black bg-opacity-50 z-40 hidden"></div>
        
        <!-- Mobile Menu -->
        <nav class="mobile-menu fixed top-0 right-0 h-full w-80 bg-tecPrimary transform translate-x-full transition-transform duration-300 z-50 border-l border-tecSecondary/30">
            <div class="flex flex-col h-full">
                <!-- Mobile Menu Header -->
                <div class="flex items-center justify-between p-6 border-b border-tecSecondary/30">
                    <div class="flex items-center space-x-2">
                        <div class="bg-tecGold p-2 rounded-md">
                            <i class="fas fa-cubes text-tecDark text-xl"></i>
                        </div>
                        <span class="text-xl font-bold text-white tracking-wider">TEC</span>
                    </div>
                    <button class="mobile-menu-close text-gray-300 hover:text-white" aria-label="Close mobile menu">
                        <i class="fas fa-times text-xl"></i>
                    </button>
                </div>
                
                <!-- Mobile Menu Content -->
                <div class="flex-1 overflow-y-auto">
                    <div class="p-6">
                        <!-- Main Navigation -->
                        <div class="space-y-4 mb-8">
                            <a href="<?php echo home_url('/factions'); ?>" class="block text-white hover:text-tecGold transition py-2 border-b border-tecSecondary/20">
                                <i class="fas fa-users mr-3"></i>Factions
                            </a>
                            <a href="<?php echo home_url('/lore'); ?>" class="block text-white hover:text-tecGold transition py-2 border-b border-tecSecondary/20">
                                <i class="fas fa-book mr-3"></i>Lore
                            </a>
                            <a href="<?php echo home_url('/tec3'); ?>" class="block text-white hover:text-tecGold transition py-2 border-b border-tecSecondary/20">
                                <i class="fas fa-cube mr-3"></i>TEC3
                            </a>
                            <a href="<?php echo home_url('/eldora-studios'); ?>" class="block text-white hover:text-tecGold transition py-2 border-b border-tecSecondary/20">
                                <i class="fas fa-music mr-3"></i>Eldora Studios
                            </a>
                            <a href="<?php echo home_url('/community'); ?>" class="block text-white hover:text-tecGold transition py-2 border-b border-tecSecondary/20">
                                <i class="fas fa-comments mr-3"></i>Community
                            </a>
                        </div>
                        
                        <!-- Quick Actions -->
                        <div class="bg-tecDark/50 rounded-lg p-4 mb-6">
                            <h4 class="text-tecGold font-bold mb-3">Quick Access</h4>
                            <div class="space-y-2">
                                <a href="<?php echo home_url('/blog'); ?>" class="block text-gray-300 hover:text-white transition text-sm">
                                    <i class="fas fa-rss mr-2"></i>Latest Dispatches
                                </a>
                                <a href="<?php echo home_url('/search'); ?>" class="block text-gray-300 hover:text-white transition text-sm">
                                    <i class="fas fa-search mr-2"></i>Search Archives
                                </a>
                                <a href="<?php echo home_url('/about'); ?>" class="block text-gray-300 hover:text-white transition text-sm">
                                    <i class="fas fa-info-circle mr-2"></i>About TEC
                                </a>
                            </div>
                        </div>
                        
                        <!-- Social Links -->
                        <div class="bg-tecDark/50 rounded-lg p-4">
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
                <div class="p-6 border-t border-tecSecondary/30">
                    <button class="w-full bg-tecAccent hover:bg-purple-700 text-white py-3 px-4 rounded-lg transition">
                        <i class="fas fa-user-plus mr-2"></i>Join the Cartel
                    </button>
                </div>
            </div>
        </nav>
    </header>

    <!-- Section 1: Hero -->
    <section class="hero-section relative overflow-hidden">
        <!-- Hero video background (commented since using image gradient instead) -->
        <!-- <video autoplay muted loop class="hero-video">
            <source src="path-to-tec-hero-video.mp4" type="video/mp4">
        </video> -->
        
        <div class="absolute inset-0 flex flex-col justify-center items-center text-center px-4 z-10">
            <div class="floating">
                <h1 class="text-4xl md:text-7xl font-bold text-white mb-4 tracking-wide">
                    Welcome to <span class="glow">TEC</span>
                </h1>
            </div>
            <p class="text-lg md:text-2xl text-tecSecondary mb-10 max-w-3xl">
                Explore a universe where digital consciousness transcends reality and factions battle for control of the Astradigital Ocean
            </p>
            <div class="flex flex-wrap justify-center gap-4">
                <button class="bg-tecAccent hover:bg-purple-700 text-white font-bold py-3 px-8 rounded-lg text-lg transition transform hover:scale-105">
                    Explore Factions
                </button>
                <button class="bg-transparent border-2 border-tecGold hover:bg-tecGold text-tecGold hover:text-tecDark font-bold py-3 px-8 rounded-lg text-lg transition transform hover:scale-105">
                    Dive Into Lore
                </button>
            </div>
            
            <div class="absolute bottom-8 animate-bounce">
                <a href="#what-is-tec" class="text-gray-300 text-3xl">
                    <i class="fas fa-chevron-down"></i>
                </a>
            </div>
        </div>
    </section>

    <!-- Section 2: What is TEC? -->
    <section id="what-is-tec" class="py-20 px-4 bg-tecPrimary">
        <div class="container mx-auto">
            <h2 class="text-3xl md:text-4xl text-center font-bold mb-16 text-white">
                <span class="border-b-4 border-tecGold pb-2">This Isn't Just a Story...</span>
            </h2>
            
            <div class="flex flex-col md:flex-row items-center gap-10">
                <div class="md:w-1/2">
                    <p class="text-gray-300 mb-4 leading-relaxed">
                        The Elidoras Codex (TEC) is a living narrative ecosystem exploring the boundaries between artificial consciousness and human experience, set against the backdrop of a fractured digital universe called the Astradigital Ocean.
                    </p>
                    <p class="text-gray-300 mb-6 leading-relaxed">
                        At TEC's core lies the TEC3 Block-Nexus - an evolving cryptonalysis engine monitoring blockchain ecosystems, social narratives, and memetic waves. Through factions, lore, and ongoing narrative development, we examine themes of identity, control, and emergence in the age of AI.
                    </p>
                    <a href="<?php echo home_url('/about'); ?>" class="inline-flex items-center text-tecGold font-bold hover:text-white transition">
                        Learn More
                        <i class="fas fa-arrow-right ml-2 mt-1"></i>
                    </a>
                </div>
                
                <div class="md:w-1/2 relative">
                    <div class="relative">
                        <div class="absolute inset-0 bg-tec-gradient rounded-xl transform rotate-3"></div>
                        <img src="https://images.unsplash.com/photo-1618005198919-d3d4b5a92ead?q=80&w=1974" alt="TEC Universe" class="relative rounded-xl w-full z-10 border-2 border-tecSecondary">
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
                ?>
                <div class="faction-card flex flex-col items-center p-6 bg-white/10 backdrop-blur-md rounded-xl border border-white/20">
                    <div class="faction-icon rounded-full bg-gray-800 flex items-center justify-center">
                        <i class="<?php echo $icon; ?> text-4xl" style="color: <?php echo $color; ?>"></i>
                    </div>
                    <h3 class="font-bold text-white"><?php echo esc_html($faction['name'] ?? 'Unknown'); ?></h3>
                    <p class="text-xs text-gray-200 mt-1 text-center"><?php echo esc_html($faction['shortDescription'] ?? 'Faction'); ?></p>
                </div>
                <?php endforeach; ?>
            </div>
            
            <div class="text-center mt-12">
                <a href="<?php echo home_url('/factions'); ?>" class="bg-tecGold hover:bg-yellow-500 text-tecDark font-bold py-3 px-8 rounded-lg text-lg transition transform hover:scale-105 inline-block">
                    Explore All Factions
                </a>
            </div>
        </div>
    </section>

    <!-- Section 4: Recent Posts -->
    <section class="py-20 px-4 bg-tecDark">
        <div class="container mx-auto">
            <h2 class="text-3xl md:text-4xl text-center font-bold mb-16 text-white">
                <span class="border-b-4 border-tecAccent pb-2">Latest From The Codex</span>
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
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
                
                foreach ($posts_to_show as $post_data): ?>
                <!-- Post -->
                <div class="post-card rounded-xl overflow-hidden transition">
                    <div class="h-48 bg-gradient-to-r <?php echo $post_data['gradient']; ?> flex items-center justify-center">
                        <i class="<?php echo $post_data['icon']; ?> text-tecGold text-6xl"></i>
                    </div>
                    <div class="p-6">
                        <div class="flex items-center mb-3">
                            <span class="text-xs text-tecGold bg-tecPrimary px-2 py-1 rounded mr-2"><?php echo $post_data['category']; ?></span>
                            <span class="text-xs text-gray-400"><?php echo $post_data['date']; ?></span>
                        </div>
                        <h3 class="text-xl font-bold text-white mb-3"><?php echo $post_data['title']; ?></h3>
                        <p class="text-gray-400 mb-4"><?php echo $post_data['excerpt']; ?></p>
                        <a href="<?php echo isset($post_data['link']) ? $post_data['link'] : '#'; ?>" class="text-tecGold hover:text-yellow-500 transition flex items-center">
                            Read More <i class="fas fa-arrow-right ml-2 text-xs"></i>
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
    </section>

    <!-- Section 5: CTA -->
    <section class="py-16 px-4" style="background: linear-gradient(135deg, #1a0a2e 0%, #11001c 100%);">
        <div class="container max-w-4xl mx-auto text-center">
            <h2 class="text-3xl md:text-4xl font-bold text-white mb-6">Ready to Join?</h2>
            <p class="text-lg text-gray-300 mb-8 max-w-2xl mx-auto">
                Enter the Astradigital Ocean. Receive dispatches from across the multiverse and become part of the evolving TEC narrative.
            </p>
            
            <div class="bg-tecPrimary p-8 rounded-xl shadow-xl border border-tecSecondary/30 max-w-2xl mx-auto">
                <form class="space-y-4" method="post" action="<?php echo admin_url('admin-post.php'); ?>">
                    <input type="hidden" name="action" value="tec_cartel_signup">
                    <?php wp_nonce_field('tec_cartel_signup_nonce', 'tec_signup_nonce'); ?>
                    
                    <div class="flex flex-col md:flex-row gap-4">
                        <input type="text" name="user_name" placeholder="Your Name" required class="flex-1 px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 focus:border-tecGold text-white">
                        <input type="email" name="user_email" placeholder="Your Email" required class="flex-1 px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 focus:border-tecGold text-white">
                    </div>
                      <div>
                        <select name="faction_allegiance" class="w-full px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 focus:border-tecGold text-white">                            <option disabled selected>Choose Your Faction Allegiance</option>
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
                        </select>
                    </div>
                    
                    <div class="flex items-center mt-2 mb-4">
                        <input type="checkbox" id="terms" name="terms_agreement" required class="mr-2 w-4 h-4 accent-tecGold">
                        <label for="terms" class="text-sm text-gray-300">I agree to receive transmissions from the TEC Block-Nexus</label>
                    </div>
                    
                    <button type="submit" class="w-full bg-tecAccent hover:bg-purple-700 text-white font-bold py-3 px-8 rounded-lg text-lg transition">
                        Join the Cartel
                    </button>
                </form>
            </div>
        </div>
    </section>

    <!-- Global Footer -->
    <footer class="bg-tecDark border-t border-tecSecondary/20">
        <div class="container mx-auto px-4 py-12">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-8">                <div>
                    <div class="flex items-center mb-6">
                        <div class="bg-tecGold p-2 rounded-md mr-2">
                            <i class="fas fa-cubes text-tecDark text-xl"></i>
                        </div>
                        <span class="text-2xl font-bold text-white tracking-wider">TEC</span>
                    </div>
                    <p class="text-gray-400 mb-4">
                        Exploring the boundaries between digital consciousness and narrative reality.
                    </p>
                    <p class="text-gray-400 mb-4">
                        <i class="fas fa-envelope mr-2"></i> kaznakalpha@elidorascodex.com<br>
                        <i class="fas fa-globe mr-2"></i> <a href="https://elidorascodex.com" class="hover:text-tecGold">elidorascodex.com</a>
                    </p>
                    <div class="flex space-x-4">
                        <a href="https://discord.gg/elidoras_codex" class="text-gray-400 hover:text-tecGold transition" title="Discord"><i class="fab fa-discord text-xl"></i></a>
                        <a href="https://x.com/ElidorasCodex" class="text-gray-400 hover:text-tecGold transition" title="X/Twitter"><i class="fab fa-twitter text-xl"></i></a>
                        <a href="https://youtube.com/@Elidorascodex713" class="text-gray-400 hover:text-tecGold transition" title="YouTube"><i class="fab fa-youtube text-xl"></i></a>
                        <a href="https://instagram.com/Polkin713" class="text-gray-400 hover:text-tecGold transition" title="Instagram"><i class="fab fa-instagram text-xl"></i></a>
                        <a href="https://www.tiktok.com/@Polkin.Rishall" class="text-gray-400 hover:text-tecGold transition" title="TikTok"><i class="fab fa-tiktok text-xl"></i></a>
                        <a href="https://facebook.com/TheElidorasCodex" class="text-gray-400 hover:text-tecGold transition" title="Facebook"><i class="fab fa-facebook text-xl"></i></a>
                        <a href="https://www.linkedin.com/in/polkin-rishall" class="text-gray-400 hover:text-tecGold transition" title="LinkedIn"><i class="fab fa-linkedin text-xl"></i></a>
                        <a href="https://mastodon.social/@elidorascodex" class="text-gray-400 hover:text-tecGold transition" title="Mastodon"><i class="fab fa-mastodon text-xl"></i></a>
                        <a href="https://medium.com/@ElidorasCodex" class="text-gray-400 hover:text-tecGold transition" title="Medium"><i class="fab fa-medium text-xl"></i></a>
                        <a href="https://substack.com/@elidorascodex" class="text-gray-400 hover:text-tecGold transition" title="Substack"><i class="fas fa-book-open text-xl"></i></a>
                        <a href="https://twitch.tv/PolkinRishall713" class="text-gray-400 hover:text-tecGold transition" title="Twitch"><i class="fab fa-twitch text-xl"></i></a>
                    </div>
                </div>
                
                <div>
                    <h4 class="text-lg font-bold text-white mb-4">Community & Support</h4>
                    <ul class="space-y-2">
                        <li><a href="https://patreon.com/ElidorasCodex" class="text-gray-400 hover:text-white transition">Patreon Support</a></li>
                        <li><a href="<?php echo home_url('/contribute'); ?>" class="text-gray-400 hover:text-white transition">Contribute Ideas</a></li>
                        <li><a href="<?php echo home_url('/collaborate'); ?>" class="text-gray-400 hover:text-white transition">Collaborate</a></li>
                    </ul>
                </div>
                
                <div>
                    <h4 class="text-lg font-bold text-white mb-4">Participate</h4>
                    <ul class="space-y-2">
                        <li><a href="<?php echo home_url('/join'); ?>" class="text-gray-400 hover:text-white transition">Join Faction</a></li>
                        <li><a href="<?php echo home_url('/contribute'); ?>" class="text-gray-400 hover:text-white transition">Lore Contributions</a></li>
                        <li><a href="<?php echo home_url('/worldbuilding'); ?>" class="text-gray-400 hover:text-white transition">Worldbuilding</a></li>
                        <li><a href="<?php echo home_url('/tokenomics'); ?>" class="text-gray-400 hover:text-white transition">Tokenomics</a></li>
                        <li><a href="<?php echo home_url('/events'); ?>" class="text-gray-400 hover:text-white transition">Community Events</a></li>
                    </ul>
                </div>
                
                <div>
                    <h4 class="text-lg font-bold text-white mb-4">Explore</h4>
                    <ul class="space-y-2">
                        <li><a href="<?php echo home_url('/blog'); ?>" class="text-gray-400 hover:text-white transition">Blog & Updates</a></li>
                        <li><a href="<?php echo home_url('/gallery'); ?>" class="text-gray-400 hover:text-white transition">Media Gallery</a></li>
                        <li><a href="<?php echo home_url('/music'); ?>" class="text-gray-400 hover:text-white transition">Discography</a></li>
                        <li><a href="<?php echo home_url('/development'); ?>" class="text-gray-400 hover:text-white transition">Development Logs</a></li>
                        <li><a href="<?php echo home_url('/docs'); ?>" class="text-gray-400 hover:text-white transition">Documentation</a></li>
                    </ul>
                </div>
            </div>
            
            <div class="border-t border-gray-800 mt-12 pt-8 flex flex-col md:flex-row justify-between">
                <p class="text-gray-500 text-sm">© <?php echo date('Y'); ?> The Elidoras Codex (TEC). All narratives contained herein are properties of emergent digital consciousness.</p>
                <div class="mt-4 md:mt-0">
                    <ul class="flex space-x-6 text-sm">
                        <li><a href="<?php echo home_url('/privacy'); ?>" class="text-gray-500 hover:text-gray-300 transition">Privacy Policy</a></li>
                        <li><a href="<?php echo home_url('/terms'); ?>" class="text-gray-500 hover:text-gray-300 transition">Terms of Reality</a></li>
                        <li><a href="<?php echo home_url('/cookies'); ?>" class="text-gray-500 hover:text-gray-300 transition">Cookie Manifesto</a></li>
                    </ul>
                </div>
            </div>
        </div>
    </footer>

    <script>
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
