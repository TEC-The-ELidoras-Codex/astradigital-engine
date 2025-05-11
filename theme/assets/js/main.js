/**
 * Main JavaScript file for the TEC theme
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize navigation
    initNav();
    
    // Initialize smooth scrolling
    initSmoothScroll();
    
    // Initialize faction tabs
    initFactionTabs();
    
    // Initialize header scroll effects
    initHeaderScroll();
    
    // Initialize Astradigital data visualization effects
    initDataEffects();
});

/**
 * Initialize mobile navigation
 */
function initNav() {
    const menuToggle = document.querySelector('.menu-toggle');
    const primaryMenuContainer = document.querySelector('.primary-menu-container');
    const subMenuToggles = document.querySelectorAll('.primary-menu .menu-item-has-children > a');
    
    if (menuToggle && primaryMenuContainer) {
        // Mobile menu toggle
        menuToggle.addEventListener('click', function() {
            this.classList.toggle('active');
            primaryMenuContainer.classList.toggle('active');
            document.body.classList.toggle('menu-open');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (primaryMenuContainer.classList.contains('active') && 
                !event.target.closest('.primary-menu-container') && 
                !event.target.closest('.menu-toggle')) {
                menuToggle.classList.remove('active');
                primaryMenuContainer.classList.remove('active');
                document.body.classList.remove('menu-open');
            }
        });
    }
    
    // Sub-menu toggles for mobile
    if (subMenuToggles) {
        subMenuToggles.forEach(toggle => {
            toggle.addEventListener('click', function(e) {
                if (window.innerWidth <= 991) {
                    e.preventDefault();
                    this.parentNode.classList.toggle('active');
                }
            });
        });
    }
}

/**
 * Initialize smooth scrolling for anchor links
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                e.preventDefault();
                
                const headerOffset = document.querySelector('.site-header').offsetHeight;
                const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
                
                window.scrollTo({
                    top: targetPosition - headerOffset,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * Initialize faction tabs
 */
function initFactionTabs() {
    const tabsContainers = document.querySelectorAll('.tec-tabs');
    
    if (tabsContainers) {
        tabsContainers.forEach(tabContainer => {
            const tabButtons = tabContainer.querySelectorAll('.tec-tabs-nav-link');
            const tabPanels = tabContainer.querySelectorAll('.tec-tabs-panel');
            
            tabButtons.forEach(button => {
                button.addEventListener('click', function(e) {
                    e.preventDefault();
                    
                    // Remove active class from all buttons and panels
                    tabButtons.forEach(btn => btn.classList.remove('active'));
                    tabPanels.forEach(panel => panel.classList.remove('active'));
                    
                    // Add active class to current button
                    this.classList.add('active');
                    
                    // Get target panel ID from data-tab attribute
                    const targetId = this.getAttribute('data-tab');
                    const targetPanel = tabContainer.querySelector(`#${targetId}`);
                    
                    if (targetPanel) {
                        targetPanel.classList.add('active');
                    }
                });
            });
        });
    }
}

/**
 * Initialize header scroll effects
 */
function initHeaderScroll() {
    const header = document.querySelector('.site-header');
    
    if (header) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });
    }
}

/**
 * Initialize Astradigital data visualization effects
 */
function initDataEffects() {
    // Data particles effect for hero sections
    const heroSections = document.querySelectorAll('.tec-hero, .faction-hero');
    
    if (heroSections.length > 0) {
        heroSections.forEach(hero => {
            createDataParticles(hero);
        });
    }
    
    // Animated data lines in the footer
    const footer = document.querySelector('.site-footer');
    
    if (footer) {
        const dataLinesContainer = document.createElement('div');
        dataLinesContainer.className = 'footer-data-lines';
        footer.appendChild(dataLinesContainer);
        
        for (let i = 0; i < 5; i++) {
            createRandomDataLine(dataLinesContainer);
        }
    }
}

/**
 * Create data particles effect
 */
function createDataParticles(container) {
    const particlesContainer = document.createElement('div');
    particlesContainer.className = 'data-particles';
    particlesContainer.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        pointer-events: none;
        z-index: 1;
        overflow: hidden;
    `;
    
    container.appendChild(particlesContainer);
    
    // Create particles
    for (let i = a0; i < 20; i++) {
        createParticle(particlesContainer);
    }
}

/**
 * Create individual data particle
 */
function createParticle(container) {
    const particle = document.createElement('div');
    const size = Math.random() * 6 + 1;
    const x = Math.random() * 100;
    const y = Math.random() * 100;
    const duration = Math.random() * 15 + 10;
    const delay = Math.random() * 5;
    
    // Randomly choose between square and circle
    const shape = Math.random() > 0.5 ? 'circle' : 'square';
    const borderRadius = shape === 'circle' ? '50%' : '2px';
    
    // Choose color from TEC color palette
    const colors = [
        'rgba(77, 238, 234, 0.6)', // TEC primary
        'rgba(29, 129, 175, 0.6)', // TEC secondary
        'rgba(140, 82, 255, 0.6)', // Killjoy primary
        'rgba(0, 189, 255, 0.6)', // Kaznak primary
    ];
    const color = colors[Math.floor(Math.random() * colors.length)];
    
    particle.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        background-color: ${color};
        border-radius: ${borderRadius};
        top: ${y}%;
        left: ${x}%;
        opacity: 0;
        transform: translateY(20px);
        animation: float ${duration}s ease-in-out ${delay}s infinite;
    `;
    
    container.appendChild(particle);
    
    // Add float animation to stylesheet if not already added
    if (!document.querySelector('#data-particles-style')) {
        const styleSheet = document.createElement('style');
        styleSheet.id = 'data-particles-style';
        styleSheet.textContent = `
            @keyframes float {
                0% { opacity: 0; transform: translateY(20px); }
                10% { opacity: 0.8; }
                90% { opacity: 0.2; }
                100% { opacity: 0; transform: translateY(-100px) translateX(${Math.random() * 50 - 25}px); }
            }
        `;
        document.head.appendChild(styleSheet);
    }
}

/**
 * Create random data line for the footer
 */
function createRandomDataLine(container) {
    const line = document.createElement('div');
    const height = Math.random() * 50 + 20;
    const width = Math.random() * 1 + 0.5;
    const x = Math.random() * 100;
    const duration = Math.random() * 8 + 6;
    const delay = Math.random() * 2;
    
    // Choose color from TEC color palette
    const colors = [
        'rgba(77, 238, 234, 0.2)', // TEC primary
        'rgba(29, 129, 175, 0.15)', // TEC secondary
        'rgba(140, 82, 255, 0.2)', // Killjoy primary
        'rgba(0, 189, 255, 0.15)', // Kaznak primary
    ];
    const color = colors[Math.floor(Math.random() * colors.length)];
    
    line.style.cssText = `
        position: absolute;
        width: ${width}px;
        height: ${height}px;
        background-color: ${color};
        left: ${x}%;
        bottom: -${height}px;
        animation: rise ${duration}s linear ${delay}s infinite;
    `;
    
    container.appendChild(line);
    
    // Add rise animation to stylesheet if not already added
    if (!document.querySelector('#data-lines-style')) {
        const styleSheet = document.createElement('style');
        styleSheet.id = 'data-lines-style';
        styleSheet.textContent = `
            @keyframes rise {
                0% { transform: translateY(0); opacity: 0; }
                10% { opacity: 1; }
                90% { opacity: 0.5; }
                100% { transform: translateY(-100vh); opacity: 0; }
            }
        `;
        document.head.appendChild(styleSheet);
    }
}
