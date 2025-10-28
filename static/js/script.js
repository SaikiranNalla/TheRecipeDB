/**
 * CookBook Frontend JavaScript
 * Handles recipe selection, AJAX requests, and UI interactions
 */

// Global variables
let selectedRecipesCount = 0;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    updateSelectedCount();
    initializeEventListeners();
});

// Initialize event listeners
function initializeEventListeners() {
    // Recipe selection buttons
    document.querySelectorAll('.select-recipe-btn').forEach(button => {
        // button.replaceWith(button.cloneNode(true));
        button.addEventListener('click', function(e) {
            e.preventDefault();
            // const recipeId = this.dataset.recipeId; // Ensure data-recipe-id is set
            // selectRecipe(recipeId); // ← Missing call
        });
    });
}

// Get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Update selected recipes count
function updateSelectedCount() {
    const badge = document.querySelector('.nav-link .badge');
    if (badge) {
        selectedRecipesCount = parseInt(badge.textContent) || 0;
    }
}

// Show notification toast
function showToast(message, type = 'success') {
    // Create toast container if doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    // Show and auto-hide toast
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { delay: 3000 });
    toast.show();
    
    // Remove after hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

// Smooth scroll animation
function smoothScroll(target) {
    target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

// Format date
function formatDate(date) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(date).toLocaleDateString('en-US', options);
}

// Debounce function for search
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

// Handle recipe card hover effects
document.querySelectorAll('.recipe-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-4px)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
    });
});

// Export functions for global use
window.showToast = showToast;
window.getCookie = getCookie;
window.smoothScroll = smoothScroll;
window.formatDate = formatDate;
