// Enhanced Daily AI News - Ranking System JavaScript
// 情報量を維持しつつエンジニア向けランキング機能を提供

document.addEventListener('DOMContentLoaded', function() {
    
    // 初期化
    initializeRankingSystem();
    setupEventListeners();
    loadUserPreferences();
    
    function initializeRankingSystem() {
        console.log('🚀 Enhanced Ranking System: Initialized');
        
        // 記事統計を更新
        updateArticleStats();
        
        // フィルター状態の復元
        restoreFilterState();
        
        // ブックマーク状態の復元
        restoreBookmarkState();
    }
    
    function setupEventListeners() {
        
        // 検索機能
        const searchBox = document.getElementById('searchBox');
        if (searchBox) {
            searchBox.addEventListener('input', debounce(handleSearch, 300));
            searchBox.addEventListener('keydown', handleSearchKeydown);
        }
        
        // 優先度フィルター
        const filterBtns = document.querySelectorAll('.filter-btn');
        filterBtns.forEach(btn => {
            btn.addEventListener('click', handlePriorityFilter);
        });
        
        // タブ切り替え
        const tabButtons = document.querySelectorAll('.tab');
        tabButtons.forEach(btn => {
            btn.addEventListener('click', handleTabSwitch);
        });
        
        // ブックマーク機能
        const bookmarkBtns = document.querySelectorAll('.action-btn.bookmark');
        bookmarkBtns.forEach(btn => {
            btn.addEventListener('click', handleBookmark);
        });
        
        // キーボードショートカット
        document.addEventListener('keydown', handleKeyboardShortcuts);
        
        // スクロール位置復元
        window.addEventListener('beforeunload', saveScrollPosition);
        
        // パフォーマンス監視
        if ('PerformanceObserver' in window) {
            observePerformance();
        }
    }
    
    function updateArticleStats() {
        const cards = document.querySelectorAll('.enhanced-card');
        const stats = {
            total: cards.length,
            hot: 0,
            high: 0,
            medium: 0,
            low: 0,
            minimal: 0
        };
        
        cards.forEach(card => {
            const priority = card.dataset.priority;
            if (priority in stats) {
                stats[priority]++;
            }
        });
        
        console.log('📊 Article Statistics:', stats);
        
        // 統計情報をUIに反映
        updateStatsDisplay(stats);
    }
    
    function updateStatsDisplay(stats) {
        // フィルターボタンのカウントを更新
        const filterBtns = document.querySelectorAll('.filter-btn');
        filterBtns.forEach(btn => {
            const filter = btn.dataset.filter;
            if (filter === 'all') {
                btn.textContent = `すべて (${stats.total})`;
            } else if (filter in stats) {
                const icon = getFilterIcon(filter);
                const label = getFilterLabel(filter);
                btn.textContent = `${icon} ${label} (${stats[filter]})`;
            }
        });
    }
    
    function handleSearch(event) {
        const searchTerm = event.target.value.toLowerCase().trim();
        const cards = document.querySelectorAll('.enhanced-card');
        let visibleCount = 0;
        
        cards.forEach(card => {
            const title = card.querySelector('.card-title')?.textContent.toLowerCase() || '';
            const summary = card.querySelector('.card-summary')?.textContent.toLowerCase() || '';
            const techTags = Array.from(card.querySelectorAll('.tech-tag'))
                .map(tag => tag.textContent.toLowerCase()).join(' ');
            
            const searchableContent = `${title} ${summary} ${techTags}`;
            const matches = !searchTerm || searchableContent.includes(searchTerm);
            
            if (matches) {
                card.style.display = '';
                card.classList.add('fade-in');
                visibleCount++;
            } else {
                card.style.display = 'none';
                card.classList.remove('fade-in');
            }
        });
        
        // 検索結果統計を表示
        showSearchStats(searchTerm, visibleCount);
        
        // 検索履歴を保存
        saveSearchHistory(searchTerm);
    }
    
    function handleSearchKeydown(event) {
        // Escキーで検索をクリア
        if (event.key === 'Escape') {
            event.target.value = '';
            handleSearch({ target: { value: '' } });
            event.target.blur();
        }
        
        // Enterキーで最初の検索結果にジャンプ
        if (event.key === 'Enter') {
            const firstVisible = document.querySelector('.enhanced-card:not([style*="display: none"])');
            if (firstVisible) {
                firstVisible.scrollIntoView({ behavior: 'smooth', block: 'center' });
                firstVisible.classList.add('pulse');
                setTimeout(() => firstVisible.classList.remove('pulse'), 2000);
            }
        }
    }
    
    function handlePriorityFilter(event) {
        const filterType = event.target.dataset.filter;
        const cards = document.querySelectorAll('.enhanced-card');
        
        // アクティブ状態を更新
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        event.target.classList.add('active');
        
        // フィルタリング実行
        let visibleCount = 0;
        cards.forEach(card => {
            const priority = card.dataset.priority;
            let shouldShow = false;
            
            switch(filterType) {
                case 'all':
                    shouldShow = true;
                    break;
                case 'hot':
                    shouldShow = priority === 'hot';
                    break;
                case 'high':
                    shouldShow = priority === 'high';
                    break;
                case 'medium':
                    shouldShow = priority === 'medium';
                    break;
                default:
                    shouldShow = true;
            }
            
            if (shouldShow) {
                card.style.display = '';
                card.classList.add('fade-in');
                visibleCount++;
            } else {
                card.style.display = 'none';
                card.classList.remove('fade-in');
            }
        });
        
        // フィルター状態を保存
        saveFilterState(filterType);
        
        // 結果を表示
        showFilterStats(filterType, visibleCount);
    }
    
    function handleTabSwitch(event) {
        const targetTab = event.target.dataset.target;
        if (!targetTab) return;
        
        // タブボタンの状態更新
        document.querySelectorAll('.tab').forEach(tab => {
            tab.classList.remove('active');
            tab.setAttribute('aria-selected', 'false');
        });
        event.target.classList.add('active');
        event.target.setAttribute('aria-selected', 'true');
        
        // タブコンテンツの表示切り替え
        document.querySelectorAll('.tab-panel').forEach(panel => {
            panel.classList.add('hidden');
        });
        
        const targetPanel = document.querySelector(targetTab);
        if (targetPanel) {
            targetPanel.classList.remove('hidden');
        }
        
        // アクティブタブを保存
        saveActiveTab(targetTab);
    }
    
    function handleBookmark(event) {
        const btn = event.target;
        const url = btn.dataset.url;
        const card = btn.closest('.enhanced-card');
        
        if (!url) return;
        
        const bookmarks = getBookmarks();
        const isBookmarked = bookmarks.includes(url);
        
        if (isBookmarked) {
            // ブックマーク削除
            const index = bookmarks.indexOf(url);
            bookmarks.splice(index, 1);
            btn.textContent = '🔖 ブックマーク';
            btn.classList.remove('bookmarked');
            showNotification('ブックマークを削除しました');
        } else {
            // ブックマーク追加
            bookmarks.push(url);
            btn.textContent = '📌 保存済み';
            btn.classList.add('bookmarked');
            showNotification('ブックマークに追加しました');
        }
        
        // ローカルストレージに保存
        localStorage.setItem('dailyai_bookmarks', JSON.stringify(bookmarks));
        
        // アニメーション効果
        btn.style.transform = 'scale(1.2)';
        setTimeout(() => {
            btn.style.transform = '';
        }, 200);
    }
    
    function handleKeyboardShortcuts(event) {
        // Ctrl/Cmd + F で検索ボックスにフォーカス
        if ((event.ctrlKey || event.metaKey) && event.key === 'f') {
            event.preventDefault();
            const searchBox = document.getElementById('searchBox');
            if (searchBox) {
                searchBox.focus();
                searchBox.select();
            }
        }
        
        // 数字キーでフィルター切り替え
        if (event.key >= '1' && event.key <= '4' && !event.ctrlKey && !event.metaKey) {
            const filterBtns = document.querySelectorAll('.filter-btn');
            const index = parseInt(event.key) - 1;
            if (filterBtns[index]) {
                filterBtns[index].click();
            }
        }
        
        // Escキーでフィルターをリセット
        if (event.key === 'Escape') {
            const allFilterBtn = document.querySelector('.filter-btn[data-filter="all"]');
            if (allFilterBtn && !allFilterBtn.classList.contains('active')) {
                allFilterBtn.click();
            }
        }
    }
    
    // ユーティリティ関数
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    function getFilterIcon(filter) {
        const icons = {
            'hot': '🔥',
            'high': '⚡',
            'medium': '📖',
            'low': '📰'
        };
        return icons[filter] || '📄';
    }
    
    function getFilterLabel(filter) {
        const labels = {
            'hot': '最高優先',
            'high': '高優先',
            'medium': '中優先',
            'low': '低優先'
        };
        return labels[filter] || '参考';
    }
    
    function showSearchStats(searchTerm, count) {
        const existing = document.querySelector('.search-stats');
        if (existing) existing.remove();
        
        if (!searchTerm) return;
        
        const stats = document.createElement('div');
        stats.className = 'search-stats';
        stats.innerHTML = `
            <small>🔍 「${searchTerm}」で ${count} 件見つかりました</small>
        `;
        stats.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--brand);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 12px;
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(stats);
        
        setTimeout(() => {
            stats.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => stats.remove(), 300);
        }, 3000);
    }
    
    function showFilterStats(filterType, count) {
        const filterLabel = getFilterLabel(filterType);
        const message = filterType === 'all' ? 
            `全 ${count} 件の記事を表示中` : 
            `${filterLabel}記事 ${count} 件を表示中`;
        
        showNotification(message);
    }
    
    function showNotification(message) {
        const existing = document.querySelector('.notification');
        if (existing) existing.remove();
        
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--success);
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: var(--shadow-lg);
            z-index: 1000;
            animation: slideIn 0.3s ease;
            font-size: 14px;
            font-weight: 500;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
    
    function getBookmarks() {
        try {
            return JSON.parse(localStorage.getItem('dailyai_bookmarks') || '[]');
        } catch {
            return [];
        }
    }
    
    function saveFilterState(filterType) {
        try {
            localStorage.setItem('dailyai_filter', filterType);
        } catch (e) {
            console.warn('Failed to save filter state:', e);
        }
    }
    
    function restoreFilterState() {
        try {
            const savedFilter = localStorage.getItem('dailyai_filter');
            if (savedFilter) {
                const filterBtn = document.querySelector(`[data-filter="${savedFilter}"]`);
                if (filterBtn) {
                    // 少し遅延させて初期化の衝突を避ける
                    setTimeout(() => filterBtn.click(), 100);
                }
            }
        } catch (e) {
            console.warn('Failed to restore filter state:', e);
        }
    }
    
    function restoreBookmarkState() {
        const bookmarks = getBookmarks();
        const bookmarkBtns = document.querySelectorAll('.action-btn.bookmark');
        
        bookmarkBtns.forEach(btn => {
            const url = btn.dataset.url;
            if (bookmarks.includes(url)) {
                btn.textContent = '📌 保存済み';
                btn.classList.add('bookmarked');
            }
        });
    }
    
    function saveActiveTab(tabId) {
        try {
            localStorage.setItem('dailyai_active_tab', tabId);
        } catch (e) {
            console.warn('Failed to save active tab:', e);
        }
    }
    
    function saveScrollPosition() {
        try {
            localStorage.setItem('dailyai_scroll', window.scrollY.toString());
        } catch (e) {
            console.warn('Failed to save scroll position:', e);
        }
    }
    
    function saveSearchHistory(searchTerm) {
        if (!searchTerm) return;
        
        try {
            const history = JSON.parse(localStorage.getItem('dailyai_search_history') || '[]');
            if (!history.includes(searchTerm)) {
                history.unshift(searchTerm);
                // 最新10件まで保持
                history.splice(10);
                localStorage.setItem('dailyai_search_history', JSON.stringify(history));
            }
        } catch (e) {
            console.warn('Failed to save search history:', e);
        }
    }
    
    function loadUserPreferences() {
        try {
            // スクロール位置復元
            const savedScroll = localStorage.getItem('dailyai_scroll');
            if (savedScroll) {
                setTimeout(() => {
                    window.scrollTo(0, parseInt(savedScroll));
                }, 100);
            }
            
            // アクティブタブ復元
            const savedTab = localStorage.getItem('dailyai_active_tab');
            if (savedTab) {
                const tabBtn = document.querySelector(`[data-target="${savedTab}"]`);
                if (tabBtn) {
                    setTimeout(() => tabBtn.click(), 50);
                }
            }
        } catch (e) {
            console.warn('Failed to load user preferences:', e);
        }
    }
    
    function observePerformance() {
        const perfObserver = new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
                if (entry.duration > 100) {
                    console.warn(`Slow operation: ${entry.name} took ${entry.duration}ms`);
                }
            }
        });
        
        try {
            perfObserver.observe({ entryTypes: ['measure', 'navigation'] });
        } catch (e) {
            console.warn('Performance observation not supported');
        }
    }
    
    // CSS animations追加
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
        
        .enhanced-card.fade-in {
            animation: fadeIn 0.4s ease-in-out;
        }
        
        .enhanced-card:focus-within {
            outline: 3px solid var(--brand-light);
            outline-offset: 2px;
        }
    `;
    document.head.appendChild(style);
    
    // 初期化完了メッセージ
    console.log('✅ Enhanced Daily AI News: Ready with ranking system');
    
    // パフォーマンス監視
    setTimeout(() => {
        const loadTime = performance.now();
        console.log(`🚀 Page loaded in ${loadTime.toFixed(2)}ms`);
    }, 0);
});

// エクスポート（他のスクリプトで使用可能）
window.DailyAINews = {
    version: '2.0.0',
    features: ['ranking', 'filtering', 'search', 'bookmarks'],
    initialized: true
};