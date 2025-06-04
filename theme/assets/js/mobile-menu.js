/**
 * TEC Theme Mobile Navigation & Interactive Features
 * Enhanced mobile menu functionality for The Elidoras Codex
 */

document.addEventListener('DOMContentLoaded', function() {
    // Mobile Menu Toggle
    const mobileMenuButton = document.querySelector('.mobile-menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    const mobileMenuOverlay = document.querySelector('.mobile-menu-overlay');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            const isOpen = mobileMenu.classList.contains('active');
            
            if (isOpen) {
                closeMobileMenu();
            } else {
                openMobileMenu();
            }
        });
    }
    
    // Close mobile menu when clicking overlay
    if (mobileMenuOverlay) {
        mobileMenuOverlay.addEventListener('click', closeMobileMenu);
    }
    
    // Close mobile menu when pressing Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeMobileMenu();
        }
    });
    
    function openMobileMenu() {
        mobileMenu.classList.add('active');
        mobileMenuOverlay.classList.add('active');
        document.body.classList.add('mobile-menu-open');
        mobileMenuButton.setAttribute('aria-expanded', 'true');
        
        // Focus management
        const firstMenuItem = mobileMenu.querySelector('a, button');
        if (firstMenuItem) {
            firstMenuItem.focus();
        }
    }
    
    function closeMobileMenu() {
        mobileMenu.classList.remove('active');
        mobileMenuOverlay.classList.remove('active');
        document.body.classList.remove('mobile-menu-open');
        mobileMenuButton.setAttribute('aria-expanded', 'false');
        mobileMenuButton.focus();
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Close mobile menu if open
                closeMobileMenu();
            }
        });
    });
    
    // Faction grid animation on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const factionObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                const factionCards = entry.target.querySelectorAll('.faction-card');
                factionCards.forEach((card, index) => {
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }, index * 150);
                });
                factionObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    const factionGrid = document.querySelector('.faction-grid');
    if (factionGrid) {
        // Initialize faction cards
        const factionCards = factionGrid.querySelectorAll('.faction-card');
        factionCards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        });
        
        factionObserver.observe(factionGrid);
    }
    
    // Post cards animation
    const postObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                postObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    const postCards = document.querySelectorAll('.post-card');
    postCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        postObserver.observe(card);
    });
    
    // Form enhancements
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            // Add focus/blur effects
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('field-focused');
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.classList.remove('field-focused');
                if (this.value) {
                    this.parentElement.classList.add('field-filled');
                } else {
                    this.parentElement.classList.remove('field-filled');
                }
            });
            
            // Check initial state
            if (input.value) {
                input.parentElement.classList.add('field-filled');
            }
        });
    });
    
    // TEC Cartel signup form handling
    const signupForm = document.querySelector('form[action*="admin-post.php"]');
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('button[type="submit"]');
            const originalText = submitButton.innerHTML;
            
            // Show loading state
            submitButton.innerHTML = '<i class="fas fa-satellite-dish fa-spin mr-2"></i>Transmitting...';
            submitButton.disabled = true;
            
            // Re-enable after a delay if form doesn't redirect
            setTimeout(() => {
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            }, 5000);
        });
    }
    
    // Search form enhancements
    const searchForms = document.querySelectorAll('form[role="search"]');
    searchForms.forEach(form => {
        const searchInput = form.querySelector('input[type="search"]');
        const searchButton = form.querySelector('button[type="submit"]');
        
        if (searchInput && searchButton) {
            searchInput.addEventListener('input', function() {
                if (this.value.length > 0) {
                    searchButton.classList.add('search-ready');
                } else {
                    searchButton.classList.remove('search-ready');
                }
            });
        }
    });
    
    // Parallax effect for hero sections
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const heroSections = document.querySelectorAll('.hero-section');
        
        heroSections.forEach(hero => {
            const rate = scrolled * -0.5;
            hero.style.transform = `translateY(${rate}px)`;
        });
    });
    
    // Dynamic header on scroll
    let lastScrollTop = 0;
    const header = document.querySelector('header');
    
    if (header) {
        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (scrollTop > lastScrollTop && scrollTop > 100) {
                // Scrolling down
                header.classList.add('header-hidden');
            } else {
                // Scrolling up
                header.classList.remove('header-hidden');
            }
            
            // Add background when scrolled
            if (scrollTop > 50) {
                header.classList.add('header-scrolled');
            } else {
                header.classList.remove('header-scrolled');
            }
            
            lastScrollTop = scrollTop;
        });
    }
    
    // Copy to clipboard functionality for code blocks
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(codeBlock => {
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-code-btn';
        copyButton.innerHTML = '<i class="fas fa-copy"></i>';
        copyButton.title = 'Copy to clipboard';
        
        copyButton.addEventListener('click', function() {
            navigator.clipboard.writeText(codeBlock.textContent).then(() => {
                this.innerHTML = '<i class="fas fa-check"></i>';
                setTimeout(() => {
                    this.innerHTML = '<i class="fas fa-copy"></i>';
                }, 2000);
            });
        });
        
        codeBlock.parentElement.style.position = 'relative';
        codeBlock.parentElement.appendChild(copyButton);
    });
    
    // Auto-hide notifications
    const notifications = document.querySelectorAll('.notification, .notice');
    notifications.forEach(notification => {
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 5000);
    });
});

// Utility functions
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

// Theme color mode toggle (if implemented)
function toggleThemeMode() {
    const body = document.body;
    const currentMode = body.classList.contains('light-mode') ? 'light' : 'dark';
    const newMode = currentMode === 'light' ? 'dark' : 'light';
    
    body.classList.toggle('light-mode');
    localStorage.setItem('tec-theme-mode', newMode);
    
    // Update toggle button if exists
    const modeToggle = document.querySelector('.theme-mode-toggle');
    if (modeToggle) {
        const icon = modeToggle.querySelector('i');
        if (icon) {
            icon.className = newMode === 'light' ? 'fas fa-moon' : 'fas fa-sun';
        }
    }
}

// Initialize theme mode from localStorage
function initThemeMode() {
    const savedMode = localStorage.getItem('tec-theme-mode');
    if (savedMode === 'light') {
        document.body.classList.add('light-mode');
    }
}
