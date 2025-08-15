// Main JavaScript file for Mexican Trout Biodiversity Project

// Global configuration
const CONFIG = {
    API_BASE_URL: '',
    MAP_CENTER: [25.0, -105.0],
    MAP_ZOOM: 6,
    RECORDS_PER_PAGE: 25,
    MAX_MAP_POINTS: 1000
};

// Utility functions
const Utils = {
    // Format date
    formatDate: function(dateString) {
        if (!dateString) return 'Unknown';
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },

    // Format coordinates
    formatCoordinates: function(lat, lng) {
        if (!lat || !lng) return 'N/A';
        return `${lat.toFixed(6)}, ${lng.toFixed(6)}`;
    },

    // Validate coordinates
    validateCoordinates: function(lat, lng) {
        if (!lat || !lng) return false;
        return lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180;
    },

    // Debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Show notification
    showNotification: function(message, type = 'info') {
        const alertClass = `alert-${type}`;
        const alertHtml = `
            <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        // Create container if it doesn't exist
        let container = document.getElementById('notification-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'notification-container';
            container.style.position = 'fixed';
            container.style.top = '20px';
            container.style.right = '20px';
            container.style.zIndex = '9999';
            container.style.maxWidth = '400px';
            document.body.appendChild(container);
        }
        
        const alertElement = document.createElement('div');
        alertElement.innerHTML = alertHtml;
        container.appendChild(alertElement);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alertElement.parentNode) {
                alertElement.remove();
            }
        }, 5000);
    },

    // Format file size
    formatFileSize: function(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },

    // Download file
    downloadFile: function(data, filename, type = 'text/csv') {
        const blob = new Blob([data], { type: type });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    },

    // Generate CSV from data
    generateCSV: function(data, headers) {
        const csvContent = [
            headers.join(','),
            ...data.map(row => 
                headers.map(header => {
                    const value = row[header] || '';
                    return `"${value.toString().replace(/"/g, '""')}"`;
                }).join(',')
            )
        ].join('\n');
        
        return csvContent;
    },

    // Parse URL parameters
    getUrlParams: function() {
        const params = new URLSearchParams(window.location.search);
        const result = {};
        for (const [key, value] of params) {
            result[key] = value;
        }
        return result;
    },

    // Update URL parameters
    updateUrlParams: function(params) {
        const url = new URL(window.location);
        Object.keys(params).forEach(key => {
            if (params[key] !== null && params[key] !== undefined) {
                url.searchParams.set(key, params[key]);
            } else {
                url.searchParams.delete(key);
            }
        });
        window.history.replaceState({}, '', url);
    }
};

// API functions
const API = {
    // Make API request
    request: async function(endpoint, options = {}) {
        const url = CONFIG.API_BASE_URL + endpoint;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };
        
        try {
            const response = await fetch(url, { ...defaultOptions, ...options });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            Utils.showNotification('API request failed: ' + error.message, 'danger');
            throw error;
        }
    },

    // Get occurrence records
    getOccurrences: function(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.request(`/api/occurrences?${queryString}`);
    },

    // Get species data
    getSpecies: function() {
        return this.request('/api/species');
    },

    // Get statistics
    getStatistics: function() {
        return this.request('/api/statistics');
    },

    // Get map data
    getMapData: function() {
        return this.request('/api/map-data');
    },

    // Import Excel file
    importExcel: function(formData) {
        return this.request('/api/import-excel', {
            method: 'POST',
            body: formData,
            headers: {} // Let browser set content-type for FormData
        });
    },

    // Export data
    exportData: function(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return `${CONFIG.API_BASE_URL}/api/export-data?${queryString}`;
    }
};

// Map utilities
const MapUtils = {
    // Create map marker
    createMarker: function(lat, lng, options = {}) {
        const defaultOptions = {
            radius: 8,
            fillColor: '#007bff',
            color: '#fff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8
        };
        
        return L.circleMarker([lat, lng], { ...defaultOptions, ...options });
    },

    // Create popup content
    createPopupContent: function(data) {
        return `
            <div style="min-width: 200px;">
                <h6><strong>${data.species || 'Unknown'}</strong></h6>
                <p><strong>ID:</strong> ${data.unique_record_id}</p>
                <p><strong>Date:</strong> ${Utils.formatDate(data.collection_date)}</p>
                <p><strong>Locality:</strong> ${data.locality || 'Unknown'}</p>
                <p><strong>State:</strong> ${data.state || 'Unknown'}</p>
                <p><strong>Basin:</strong> ${data.basin || 'Unknown'}</p>
                <p><strong>Collectors:</strong> ${data.collectors || 'Unknown'}</p>
                <p><strong>Field #:</strong> ${data.field_number || 'Unknown'}</p>
            </div>
        `;
    },

    // Get species color
    getSpeciesColor: function(species, colorMap = {}) {
        if (colorMap[species]) {
            return colorMap[species];
        }
        
        // Generate color based on species name
        const colors = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
            '#a6cee3', '#fb9a99', '#fdbf6f', '#cab2d6', '#ff9896'
        ];
        
        const index = species.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0) % colors.length;
        colorMap[species] = colors[index];
        return colors[index];
    }
};

// Data validation
const DataValidator = {
    // Validate occurrence record
    validateRecord: function(record) {
        const errors = [];
        
        // Check required fields
        if (!record.unique_record_id) {
            errors.push('Missing unique record ID');
        }
        
        if (!record.species) {
            errors.push('Missing species information');
        }
        
        // Validate coordinates
        if (record.latitude && record.longitude) {
            if (!Utils.validateCoordinates(record.latitude, record.longitude)) {
                errors.push('Invalid coordinates');
            }
        }
        
        // Validate date
        if (record.collection_date) {
            const date = new Date(record.collection_date);
            if (isNaN(date.getTime())) {
                errors.push('Invalid collection date');
            }
        }
        
        return {
            isValid: errors.length === 0,
            errors: errors
        };
    },

    // Validate species data
    validateSpecies: function(species) {
        const errors = [];
        
        if (!species.scientific_name) {
            errors.push('Missing scientific name');
        }
        
        return {
            isValid: errors.length === 0,
            errors: errors
        };
    }
};

// Chart utilities
const ChartUtils = {
    // Create bar chart
    createBarChart: function(canvasId, data, options = {}) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;
        
        const defaultOptions = {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                }
            }
        };
        
        return new Chart(ctx, { ...defaultOptions, ...options });
    },

    // Create pie chart
    createPieChart: function(canvasId, data, options = {}) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;
        
        const defaultOptions = {
            type: 'pie',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'bottom'
                    }
                }
            }
        };
        
        return new Chart(ctx, { ...defaultOptions, ...options });
    }
};

// Event handlers
const EventHandlers = {
    // Handle form submission
    handleFormSubmit: function(formId, handler) {
        const form = document.getElementById(formId);
        if (form) {
            form.addEventListener('submit', handler);
        }
    },

    // Handle button clicks
    handleButtonClick: function(buttonId, handler) {
        const button = document.getElementById(buttonId);
        if (button) {
            button.addEventListener('click', handler);
        }
    },

    // Handle select changes
    handleSelectChange: function(selectId, handler) {
        const select = document.getElementById(selectId);
        if (select) {
            select.addEventListener('change', handler);
        }
    },

    // Handle input changes with debounce
    handleInputChange: function(inputId, handler, delay = 300) {
        const input = document.getElementById(inputId);
        if (input) {
            const debouncedHandler = Utils.debounce(handler, delay);
            input.addEventListener('input', debouncedHandler);
        }
    }
};

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Add loading states to buttons
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function() {
            if (!this.classList.contains('btn-loading')) {
                this.classList.add('btn-loading');
                this.disabled = true;
                
                setTimeout(() => {
                    this.classList.remove('btn-loading');
                    this.disabled = false;
                }, 2000);
            }
        });
    });
    
    console.log('Mexican Trout Biodiversity Project initialized');
});

// Export utilities for use in other scripts
window.MexicanTroutUtils = {
    Utils,
    API,
    MapUtils,
    DataValidator,
    ChartUtils,
    EventHandlers,
    CONFIG
}; 