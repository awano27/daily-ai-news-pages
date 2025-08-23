// AI Tech Radar - Interactive Features

document.addEventListener('DOMContentLoaded', function() {
    // Theme Toggle
    const themeToggle = document.querySelector('.theme-toggle');
    const body = document.body;
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme') || 'light';
    body.setAttribute('data-theme', savedTheme);
    
    themeToggle?.addEventListener('click', () => {
        const currentTheme = body.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        body.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        // Update toggle icon
        themeToggle.textContent = newTheme === 'dark' ? '☀️' : '🌓';
    });
    
    // Search Functionality
    const searchInput = document.getElementById('searchInput');
    const searchSuggestions = document.querySelector('.search-suggestions');
    
    searchInput?.addEventListener('focus', () => {
        searchSuggestions?.classList.remove('hidden');
    });
    
    searchInput?.addEventListener('blur', () => {
        setTimeout(() => {
            searchSuggestions?.classList.add('hidden');
        }, 200);
    });
    
    searchInput?.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        filterContent(searchTerm);
    });
    
    // Filter Tags
    const filterTags = document.querySelectorAll('.filter-tag');
    
    filterTags.forEach(tag => {
        tag.addEventListener('click', () => {
            // Remove active class from all tags
            filterTags.forEach(t => t.classList.remove('active'));
            // Add active class to clicked tag
            tag.classList.add('active');
            
            const filter = tag.getAttribute('data-filter');
            applyFilter(filter);
        });
    });
    
    // View Options
    const viewBtns = document.querySelectorAll('.view-btn');
    const cardsGrid = document.querySelector('.cards-grid');
    
    viewBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            viewBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const view = btn.getAttribute('data-view');
            changeView(view);
        });
    });
    
    // Tab Navigation
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');
            
            // Update buttons
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Update content
            tabContents.forEach(content => {
                if (content.id === targetTab) {
                    content.classList.add('active');
                } else {
                    content.classList.remove('active');
                }
            });
        });
    });
    
    // Bookmark Functionality
    const bookmarkBtns = document.querySelectorAll('.bookmark-btn');
    const savedBookmarks = JSON.parse(localStorage.getItem('bookmarks') || '[]');
    
    bookmarkBtns.forEach((btn, index) => {
        // Check if already bookmarked
        if (savedBookmarks.includes(index)) {
            btn.textContent = '📌';
        }
        
        btn.addEventListener('click', () => {
            const isBookmarked = savedBookmarks.includes(index);
            
            if (isBookmarked) {
                // Remove bookmark
                const idx = savedBookmarks.indexOf(index);
                savedBookmarks.splice(idx, 1);
                btn.textContent = '🔖';
            } else {
                // Add bookmark
                savedBookmarks.push(index);
                btn.textContent = '📌';
            }
            
            localStorage.setItem('bookmarks', JSON.stringify(savedBookmarks));
            
            // Show notification
            showNotification(isBookmarked ? 'ブックマークを削除しました' : 'ブックマークに追加しました');
        });
    });
    
    // Copy Code Functionality
    const copyBtns = document.querySelectorAll('.copy-btn');
    
    copyBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const codeBlock = btn.closest('.code-preview').querySelector('code');
            const code = codeBlock.textContent;
            
            navigator.clipboard.writeText(code).then(() => {
                const originalText = btn.textContent;
                btn.textContent = '✅ Copied!';
                setTimeout(() => {
                    btn.textContent = originalText;
                }, 2000);
            });
        });
    });
    
    // Notification System
    let notificationTimeout;
    
    function showNotification(message) {
        // Remove existing notification if any
        const existingNotification = document.querySelector('.notification');
        if (existingNotification) {
            existingNotification.remove();
        }
        
        // Create new notification
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        
        // Add styles
        notification.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--primary);
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        // Clear existing timeout
        if (notificationTimeout) {
            clearTimeout(notificationTimeout);
        }
        
        // Remove after 3 seconds
        notificationTimeout = setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }
    
    // Filter Content Function
    function filterContent(searchTerm) {
        const cards = document.querySelectorAll('.article-card');
        
        cards.forEach(card => {
            const title = card.querySelector('.card-title')?.textContent.toLowerCase() || '';
            const summary = card.querySelector('.card-summary')?.textContent.toLowerCase() || '';
            const tags = Array.from(card.querySelectorAll('.tech-tag')).map(tag => tag.textContent.toLowerCase()).join(' ');
            
            const content = title + ' ' + summary + ' ' + tags;
            
            if (content.includes(searchTerm)) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    }
    
    // Apply Filter Function
    function applyFilter(filter) {
        const cards = document.querySelectorAll('.article-card');
        
        if (filter === 'all') {
            cards.forEach(card => {
                card.style.display = '';
            });
            return;
        }
        
        // Filter logic based on content
        cards.forEach(card => {
            // This is a simplified filter - in production, you'd have data attributes
            const content = card.textContent.toLowerCase();
            
            switch(filter) {
                case 'llm':
                    card.style.display = content.includes('llm') || content.includes('gpt') || content.includes('claude') ? '' : 'none';
                    break;
                case 'computer-vision':
                    card.style.display = content.includes('vision') || content.includes('image') ? '' : 'none';
                    break;
                case 'mlops':
                    card.style.display = content.includes('deploy') || content.includes('production') ? '' : 'none';
                    break;
                case 'framework':
                    card.style.display = content.includes('framework') || content.includes('library') ? '' : 'none';
                    break;
                case 'research':
                    card.style.display = content.includes('paper') || content.includes('research') ? '' : 'none';
                    break;
                case 'production':
                    card.style.display = content.includes('production') || content.includes('deploy') ? '' : 'none';
                    break;
                default:
                    card.style.display = '';
            }
        });
    }
    
    // Change View Function
    function changeView(view) {
        const cardsGrid = document.querySelector('.cards-grid');
        if (!cardsGrid) return;
        
        switch(view) {
            case 'list':
                cardsGrid.style.gridTemplateColumns = '1fr';
                break;
            case 'compact':
                cardsGrid.style.gridTemplateColumns = 'repeat(auto-fill, minmax(300px, 1fr))';
                // Hide some elements for compact view
                document.querySelectorAll('.code-preview, .performance-metrics').forEach(el => {
                    el.style.display = 'none';
                });
                break;
            case 'card':
            default:
                cardsGrid.style.gridTemplateColumns = 'repeat(auto-fill, minmax(380px, 1fr))';
                // Show all elements
                document.querySelectorAll('.code-preview, .performance-metrics').forEach(el => {
                    el.style.display = '';
                });
                break;
        }
    }
    
    // Auto-refresh notification badge
    const notificationToggle = document.querySelector('.notification-toggle');
    let hasNewContent = false;
    
    // Simulate new content check (in production, this would be an API call)
    setInterval(() => {
        // Random chance of new content
        if (Math.random() > 0.8 && !hasNewContent) {
            hasNewContent = true;
            notificationToggle?.classList.add('has-notification');
            
            // Add red dot
            if (notificationToggle && !notificationToggle.querySelector('.notification-dot')) {
                const dot = document.createElement('span');
                dot.className = 'notification-dot';
                dot.style.cssText = `
                    position: absolute;
                    top: -4px;
                    right: -4px;
                    width: 8px;
                    height: 8px;
                    background: red;
                    border-radius: 50%;
                `;
                notificationToggle.style.position = 'relative';
                notificationToggle.appendChild(dot);
            }
        }
    }, 30000); // Check every 30 seconds
    
    notificationToggle?.addEventListener('click', () => {
        if (hasNewContent) {
            hasNewContent = false;
            notificationToggle.classList.remove('has-notification');
            const dot = notificationToggle.querySelector('.notification-dot');
            if (dot) dot.remove();
            
            showNotification('新しいコンテンツがあります！');
            
            // In production, this would load new content
            location.reload();
        } else {
            showNotification('新しいコンテンツはありません');
        }
    });
    
    // Intersection Observer for lazy loading and animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.5s ease forwards';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe all cards
    document.querySelectorAll('.article-card, .trend-card, .digest-card').forEach(card => {
        observer.observe(card);
    });
    
    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Progressive Enhancement - Check for JavaScript support
    document.body.classList.add('js-enabled');
    
    // Keyboard Navigation
    document.addEventListener('keydown', (e) => {
        // Press '/' to focus search
        if (e.key === '/' && document.activeElement !== searchInput) {
            e.preventDefault();
            searchInput?.focus();
        }
        
        // Press 'Escape' to clear search
        if (e.key === 'Escape' && document.activeElement === searchInput) {
            searchInput.value = '';
            filterContent('');
            searchInput.blur();
        }
        
        // Press 't' to toggle theme
        if (e.key === 't' && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
            themeToggle?.click();
        }
    });
    
    // Performance Monitoring
    if ('PerformanceObserver' in window) {
        const perfObserver = new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
                // Log slow network requests
                if (entry.duration > 1000) {
                    console.warn(`Slow request: ${entry.name} took ${entry.duration}ms`);
                }
            }
        });
        
        perfObserver.observe({ entryTypes: ['resource'] });
    }
    
    // Service Worker Registration (for offline support)
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js').catch(() => {
            // Service worker registration failed, app will work online only
        });
    }
});

// Utility function to format relative time
function formatRelativeTime(date) {
    const now = new Date();
    const diff = now - date;
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    
    if (days > 0) return `${days}日前`;
    if (hours > 0) return `${hours}時間前`;
    if (minutes > 0) return `${minutes}分前`;
    return '今';
}

// Export functions for use in other scripts
window.AITechRadar = {
    showNotification,
    formatRelativeTime,
    filterContent,
    applyFilter,
    changeView
};