// API Configuration
// Update this after deploying backend to Render

const CONFIG = {
    // Change this to your Render API URL after deployment
    // Example: 'https://tesla-dashboard-api.onrender.com'
    API_URL: window.location.hostname === 'localhost' 
        ? 'http://localhost:5000'  // Local development
        : 'https://tesla-dashboard-api.onrender.com', // Production - UPDATE THIS!
    
    // Fallback to mock data if API is unavailable
    USE_MOCK_DATA_ON_ERROR: true
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}
