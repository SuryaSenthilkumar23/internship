// =============================================================================
// SML Isuzu Inventory Management System - Main JavaScript
// =============================================================================

// Global variables
let searchTimeout;
let currentPage = document.body.dataset.page || 'unknown';

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeCommonFeatures();
    initializePageSpecificFeatures();
});

// Common features initialization
function initializeCommonFeatures() {
    // Add active class to current navigation item
    highlightActiveNavItem();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize flash message auto-dismiss
    initializeFlashMessages();
    
    // Initialize keyboard shortcuts
    initializeKeyboardShortcuts();
    
    // Initialize loading states
    initializeLoadingStates();
}

// Page-specific features initialization
function initializePageSpecificFeatures() {
    switch(currentPage) {
        case 'inventory':
            initializeInventoryFeatures();
            break;
        case 'dashboard':
            initializeDashboardFeatures();
            break;
        case 'transactions':
            initializeTransactionFeatures();
            break;
        case 'forms':
            initializeFormFeatures();
            break;
    }
}

// Navigation highlighting
function highlightActiveNavItem() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

// Tooltip initialization
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[title]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

// Flash messages auto-dismiss
function initializeFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        // Auto-dismiss success messages after 5 seconds
        if (message.classList.contains('flash-success')) {
            setTimeout(() => {
                message.style.display = 'none';
            }, 5000);
        }
        
        // Auto-dismiss error messages after 10 seconds
        if (message.classList.contains('flash-error')) {
            setTimeout(() => {
                message.style.display = 'none';
            }, 10000);
        }
    });
}

// Keyboard shortcuts
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Alt + D: Go to Dashboard
        if (e.altKey && e.key === 'd') {
            e.preventDefault();
            window.location.href = '/';
        }
        
        // Alt + I: Go to Inventory
        if (e.altKey && e.key === 'i') {
            e.preventDefault();
            window.location.href = '/inventory';
        }
        
        // Alt + T: Go to Transactions
        if (e.altKey && e.key === 't') {
            e.preventDefault();
            window.location.href = '/transactions';
        }
        
        // Alt + A: Add new item
        if (e.altKey && e.key === 'a') {
            e.preventDefault();
            window.location.href = '/inventory/add';
        }
        
        // Alt + N: Add new transaction
        if (e.altKey && e.key === 'n') {
            e.preventDefault();
            window.location.href = '/transactions/add';
        }
        
        // Escape: Close modals
        if (e.key === 'Escape') {
            closeAllModals();
        }
    });
}

// Loading states for buttons
function initializeLoadingStates() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.type === 'submit') {
                addLoadingState(this);
            }
        });
    });
}

// Dashboard specific features
function initializeDashboardFeatures() {
    // Auto-refresh dashboard data
    setInterval(refreshDashboardStats, 30000);
    
    // Initialize chart animations if any
    animateStatCards();
}

// Inventory specific features
function initializeInventoryFeatures() {
    // Enhanced search functionality
    initializeInventorySearch();
    
    // Bulk operations
    initializeBulkOperations();
    
    // Quick actions
    initializeQuickActions();
}

// Transaction specific features
function initializeTransactionFeatures() {
    // Real-time validation
    initializeTransactionValidation();
    
    // Auto-complete for remarks
    initializeRemarksAutocomplete();
}

// Form specific features
function initializeFormFeatures() {
    // Real-time validation
    initializeFormValidation();
    
    // Auto-save drafts
    initializeAutoSave();
}

// Enhanced search functionality
function initializeInventorySearch() {
    const searchInput = document.querySelector('.search-input');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        if (query.length === 0) {
            clearSearchResults();
            return;
        }
        
        searchTimeout = setTimeout(() => {
            performSearch(query);
        }, 300);
    });
}

// Perform search
function performSearch(query) {
    showSearchLoading();
    
    fetch(`/api/inventory/search?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            hideSearchLoading();
            displaySearchResults(data);
        })
        .catch(error => {
            hideSearchLoading();
            console.error('Search error:', error);
            showSearchError();
        });
}

// Display search results
function displaySearchResults(results) {
    const tbody = document.querySelector('.inventory-table tbody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    if (results.length === 0) {
        showNoResults();
        return;
    }
    
    results.forEach(item => {
        const row = createInventoryRow(item);
        tbody.appendChild(row);
    });
}

// Create inventory row
function createInventoryRow(item) {
    const row = document.createElement('tr');
    row.className = `inventory-row stock-${item.stock_status}`;
    
    const stockStatusBadge = getStockStatusBadge(item.stock_status);
    const quantityBadge = getQuantityBadge(item.quantity, item.reorder_level);
    
    row.innerHTML = `
        <td class="item-name">${item.name}</td>
        <td class="item-category">${item.category}</td>
        <td class="item-quantity">${quantityBadge}</td>
        <td class="reorder-level">${item.reorder_level}</td>
        <td class="cost-per-unit">₹${item.cost_per_unit.toFixed(2)}</td>
        <td class="total-value">₹${item.total_value.toFixed(2)}</td>
        <td class="stock-status">${stockStatusBadge}</td>
        <td class="actions">
            <a href="/inventory/edit/${item.id}" class="btn btn-sm btn-edit" title="Edit Item">
                <i class="fas fa-edit"></i>
            </a>
            <button class="btn btn-sm btn-transaction transaction-btn" 
                    data-item-id="${item.id}"
                    data-item-name="${item.name}"
                    data-current-stock="${item.quantity}"
                    title="Quick Transaction">
                <i class="fas fa-exchange-alt"></i>
            </button>
        </td>
    `;
    
    return row;
}

// Get stock status badge
function getStockStatusBadge(status) {
    const badges = {
        'low': '<span class="status-badge low-stock"><i class="fas fa-exclamation-triangle"></i> Low Stock</span>',
        'medium': '<span class="status-badge medium-stock"><i class="fas fa-minus-circle"></i> Medium Stock</span>',
        'high': '<span class="status-badge high-stock"><i class="fas fa-check-circle"></i> Good Stock</span>'
    };
    
    return badges[status] || badges['high'];
}

// Get quantity badge
function getQuantityBadge(quantity, reorderLevel) {
    let badgeClass = 'good-stock';
    
    if (quantity === 0) {
        badgeClass = 'out-of-stock';
    } else if (quantity <= reorderLevel) {
        badgeClass = 'low-stock';
    }
    
    return `<span class="quantity-badge ${badgeClass}">${quantity}</span>`;
}

// Bulk operations
function initializeBulkOperations() {
    // Add checkboxes to table rows
    addBulkCheckboxes();
    
    // Initialize bulk action handlers
    initializeBulkActions();
}

// Add loading state to button
function addLoadingState(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
    button.disabled = true;
    
    // Remove loading state after 5 seconds (fallback)
    setTimeout(() => {
        button.innerHTML = originalText;
        button.disabled = false;
    }, 5000);
}

// Refresh dashboard stats
function refreshDashboardStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            updateDashboardStats(data);
        })
        .catch(error => {
            console.error('Stats refresh error:', error);
        });
}

// Update dashboard statistics
function updateDashboardStats(data) {
    const elements = {
        totalItems: document.querySelector('.stats-grid .stat-card:nth-child(1) h3'),
        lowStockCount: document.querySelector('.stats-grid .stat-card:nth-child(2) h3'),
        totalTransactions: document.querySelector('.stats-grid .stat-card:nth-child(4) h3')
    };
    
    if (elements.totalItems) {
        animateNumber(elements.totalItems, data.total_items);
    }
    
    if (elements.lowStockCount) {
        animateNumber(elements.lowStockCount, data.low_stock_count);
    }
    
    if (elements.totalTransactions) {
        animateNumber(elements.totalTransactions, data.transaction_summary.total_transactions);
    }
}

// Animate number changes
function animateNumber(element, targetValue) {
    const currentValue = parseInt(element.textContent) || 0;
    const increment = targetValue > currentValue ? 1 : -1;
    let current = currentValue;
    
    const animation = setInterval(() => {
        current += increment;
        element.textContent = current;
        
        if (current === targetValue) {
            clearInterval(animation);
        }
    }, 50);
}

// Animate stat cards
function animateStatCards() {
    const statCards = document.querySelectorAll('.stat-card');
    
    statCards.forEach((card, index) => {
        setTimeout(() => {
            card.style.transform = 'translateY(-2px)';
            card.style.transition = 'transform 0.3s ease';
        }, index * 100);
    });
}

// Form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                showValidationErrors();
            }
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
        });
    });
}

// Validate form
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            markFieldInvalid(field);
            isValid = false;
        } else {
            markFieldValid(field);
        }
    });
    
    return isValid;
}

// Validate individual field
function validateField(field) {
    if (field.hasAttribute('required') && !field.value.trim()) {
        markFieldInvalid(field);
        return false;
    }
    
    markFieldValid(field);
    return true;
}

// Mark field as invalid
function markFieldInvalid(field) {
    field.style.borderColor = 'var(--danger-color)';
    field.classList.add('invalid');
}

// Mark field as valid
function markFieldValid(field) {
    field.style.borderColor = 'var(--success-color)';
    field.classList.remove('invalid');
}

// Auto-save functionality
function initializeAutoSave() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                saveFormData(form);
            });
        });
        
        // Load saved data on page load
        loadFormData(form);
    });
}

// Save form data to localStorage
function saveFormData(form) {
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    localStorage.setItem(`form_${form.id || 'default'}`, JSON.stringify(data));
}

// Load form data from localStorage
function loadFormData(form) {
    const savedData = localStorage.getItem(`form_${form.id || 'default'}`);
    
    if (savedData) {
        const data = JSON.parse(savedData);
        
        Object.keys(data).forEach(key => {
            const field = form.querySelector(`[name="${key}"]`);
            if (field) {
                field.value = data[key];
            }
        });
    }
}

// Utility functions
function showSearchLoading() {
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        searchInput.style.backgroundImage = 'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'20\' height=\'20\' viewBox=\'0 0 20 20\'%3E%3Cg fill=\'%23999\'%3E%3Cpath d=\'M10 2a8 8 0 1 1 0 16 8 8 0 0 1 0-16zm0 2a6 6 0 1 0 0 12 6 6 0 0 0 0-12z\'/%3E%3C/g%3E%3C/svg%3E")';
        searchInput.style.backgroundRepeat = 'no-repeat';
        searchInput.style.backgroundPosition = 'right 10px center';
        searchInput.style.paddingRight = '35px';
    }
}

function hideSearchLoading() {
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        searchInput.style.backgroundImage = '';
        searchInput.style.paddingRight = '10px';
    }
}

function showSearchError() {
    // Show error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'flash-message flash-error';
    errorDiv.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Search failed. Please try again.';
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(errorDiv, container.firstChild);
        
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }
}

function showNoResults() {
    const tbody = document.querySelector('.inventory-table tbody');
    if (tbody) {
        tbody.innerHTML = `
            <tr>
                <td colspan="8" class="no-data">
                    <i class="fas fa-search"></i>
                    <h3>No items found</h3>
                    <p>Try adjusting your search terms.</p>
                </td>
            </tr>
        `;
    }
}

function clearSearchResults() {
    // Reload the page to show all items
    window.location.reload();
}

function closeAllModals() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.style.display = 'none';
    });
}

function showTooltip(e) {
    // Simple tooltip implementation
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = e.target.getAttribute('title');
    tooltip.style.cssText = `
        position: absolute;
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 5px 10px;
        border-radius: 4px;
        font-size: 12px;
        z-index: 1000;
        pointer-events: none;
        left: ${e.pageX + 10}px;
        top: ${e.pageY - 30}px;
    `;
    
    document.body.appendChild(tooltip);
    e.target.tooltipElement = tooltip;
    
    // Remove the title attribute temporarily
    e.target.setAttribute('data-original-title', e.target.getAttribute('title'));
    e.target.removeAttribute('title');
}

function hideTooltip(e) {
    if (e.target.tooltipElement) {
        e.target.tooltipElement.remove();
        e.target.tooltipElement = null;
    }
    
    // Restore the title attribute
    if (e.target.getAttribute('data-original-title')) {
        e.target.setAttribute('title', e.target.getAttribute('data-original-title'));
        e.target.removeAttribute('data-original-title');
    }
}

// Error handling
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    // Could send error to logging service here
});

// Performance monitoring
window.addEventListener('load', function() {
    const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
    console.log(`Page loaded in ${loadTime}ms`);
});

// Export functions for global use
window.InventoryApp = {
    showSearchLoading,
    hideSearchLoading,
    performSearch,
    refreshDashboardStats,
    closeAllModals,
    addLoadingState
};