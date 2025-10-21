// API Configuration
// Update this after deploying backend to Render

const CONFIG = {
    // Change this to your Render API URL after deployment
    // Example: '"https://tesla-dashboard-api.onrender.com"'
    API_URL: window.location.hostname === 'localhost' 
        ? 'http://localhost:5000'  // Local development
        : '"https://tesla-dashboard-api.onrender.com"', // Production - UPDATE THIS!
    
    // Finnhub API Key for real-time stock data
    // Get your free API key from: https://finnhub.io/
    // IMPORTANT: Add your Finnhub API key here from your .env file
    FINNHUB_API_KEY: 'd3rto2hr01qldtravv60d3rto2hr01qldtravv6g', // UPDATE THIS with your key from .env
    
    // Fallback to mock data if API is unavailable
    USE_MOCK_DATA_ON_ERROR: true
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}
