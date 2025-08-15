# Streamlit Frontend

A modern, interactive web interface for the Links from Liliput URL shortener built with Streamlit. This frontend provides a clean, user-friendly interface for creating, managing, and analyzing short URLs with real-time analytics dashboards and responsive design.

## Overview

The Streamlit frontend serves as the primary user interface for the URL shortener platform. It's built with Python's Streamlit framework, offering a rapid development approach with built-in interactivity, responsive design, and seamless integration with the backend microservices.

## Architecture

```
Streamlit Frontend (Port 8501)
        ↓
    API Gateway (Port 8000)
   ↙️            ↘️
URL Service     Analytics Service
(Port 8001)     (Port 8002)
```

**Key Features:**
- **Multi-page Application**: Home, Dashboard, and Analytics pages
- **Real-time Updates**: Live data from microservices
- **Interactive Charts**: Plotly-powered visualizations
- **Responsive Design**: Works on desktop and mobile
- **Pure Python**: No HTML/CSS/JS required

## Project Structure

```
streamlit-frontend/
├── app.py                          # Main Streamlit application
├── pages/
│   ├── home.py                # Home page with URL shortener
│   ├── dashboard.py           # Dashboard for URL management
│   └── analytics.py           # Analytics and reporting page
├── services/
│   ├── __init__.py
│   ├── api_client.py               # API communication layer
│   └── utils.py                    # Utility functions and validators
├── components/
│   ├── __init__.py
│   ├── url_components.py           # URL-related UI components
│   └── analytics_components.py     # Analytics visualization components
├── config/
│   ├── __init__.py
│   └── settings.py                 # Configuration settings
├── requirements.txt
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
└── README.md
```

## Features

### URL Management
- **URL Shortening**: Create short URLs with optional custom codes
- **Real-time Validation**: Instant URL and custom code validation
- **Copy to Clipboard**: One-click copying of shortened URLs
- **URL Statistics**: View click counts and status information
- **Success Animations**: Visual feedback with balloons and notifications

### Analytics Dashboard
- **Global Analytics**: Platform-wide statistics and metrics
- **Individual URL Analytics**: Detailed analytics for specific URLs
- **Interactive Charts**: Timeline, geographic, and traffic source charts
- **Real-time Metrics**: Live click counts and visitor statistics
- **Top Performance Lists**: Most popular URLs and trending content

### Data Visualization
- **Click Timeline**: Time-series analysis of URL performance
- **Geographic Distribution**: World map of click locations
- **Traffic Sources**: Pie charts of referrer information
- **Performance Metrics**: KPI cards with formatted numbers
- **Responsive Charts**: Mobile-friendly interactive visualizations

### User Experience
- **Multi-page Navigation**: Organized content across logical pages
- **Sidebar Quick Actions**: Fast access to common functions
- **Loading Indicators**: Progress spinners for API calls
- **Error Handling**: User-friendly error messages
- **Responsive Design**: Optimized for all screen sizes

## Tech Stack

- **Framework**: Streamlit 1.28.1
- **HTTP Client**: Requests 2.31.0
- **Data Processing**: Pandas 2.1.4
- **Visualizations**: Plotly 5.17.0
- **Validation**: Validators 0.22.0
- **Date Handling**: python-dateutil 2.8.2
- **Runtime**: Python 3.11+

## Page Structure

### Home Page (`app.py`)
**Primary landing page with core functionality:**
- URL shortening form with validation
- Quick analytics display for new URLs
- Service health monitoring in sidebar
- Global statistics overview
- Feature highlights and platform information

### Dashboard Page (`pages/dashboard.py`)
**URL management and monitoring:**
- URL creation interface
- Individual URL statistics lookup
- URL performance cards
- Bulk operations interface (future)
- Recent URLs listing (when backend endpoint available)

### Analytics Page (`pages/analytics.py`)
**Comprehensive analytics and reporting:**
- Global platform analytics
- Individual URL deep-dive analytics
- Interactive charts and visualizations
- Performance metrics and KPIs
- Export capabilities (future)

## Configuration

### Environment Variables

Create a `.env` file in the streamlit-frontend directory:

```bash
# API Configuration
API_BASE_URL=http://localhost:8000

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Feature Flags
ENABLE_ANALYTICS=true
ENABLE_DASHBOARD=true
ENABLE_HEALTH_CHECKS=true

# UI Configuration
DEFAULT_THEME=light
ENABLE_WIDE_MODE=true
SHOW_SIDEBAR=true

# Performance Settings
API_TIMEOUT_SECONDS=10
CACHE_TTL_SECONDS=300
MAX_RETRIES=3
```

### Streamlit Configuration

Create `.streamlit/config.toml`:

```toml
[global]
developmentMode = false

[server]
port = 8501
address = "0.0.0.0"
maxUploadSize = 1
enableCORS = true
enableXsrfProtection = false

[browser]
gatherUsageStats = false
serverAddress = "localhost"
serverPort = 8501

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[client]
caching = true
displayEnabled = true
```

## Deployment

### Local Development

1. **Prerequisites**
   ```bash
   # Ensure Python 3.11+ is installed
   python --version  # Should be 3.11+
   
   # Ensure backend services are running
   curl http://localhost:8000/health/all
   ```

2. **Setup Virtual Environment**
   ```bash
   cd streamlit-frontend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Endpoint**
   ```bash
   # Set API base URL
   export API_BASE_URL=http://localhost:8000
   
   # Or create .env file
   echo "API_BASE_URL=http://localhost:8000" > .env
   ```

5. **Run Streamlit Application**
   ```bash
   # Standard run
   streamlit run app.py
   
   # With specific port
   streamlit run app.py --server.port 8501
   
   # With custom configuration
   streamlit run app.py --server.address 0.0.0.0 --server.port 8501
   ```

6. **Access Application**
   ```bash
   # Open browser to:
   # http://localhost:8501
   
   # Or if running on remote server:
   # http://your-server-ip:8501
   ```

### Docker Deployment

**Create Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create .streamlit directory and config
RUN mkdir -p .streamlit
COPY .streamlit/config.toml .streamlit/

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
```

**Build and Run:**
```bash
# Build container
docker build -t streamlit-frontend .

# Run with environment variables
docker run -d \
  --name streamlit-frontend \
  -p 8501:8501 \
  -e API_BASE_URL=http://api-gateway:8000 \
  streamlit-frontend
```

**Using Docker Compose:**
```yaml
# Add to main docker-compose.yml
services:
  streamlit-frontend:
    build: ./streamlit-frontend
    ports:
      - "8501:8501"
    environment:
      - API_BASE_URL=http://api-gateway:8000
    depends_on:
      - api-gateway
    networks:
      - microservices
```

### Production Deployment

1. **Environment Configuration**
   ```bash
   # Production environment variables
   export API_BASE_URL=https://api.yourdomain.com
   export STREAMLIT_SERVER_PORT=8501
   export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
   ```

2. **Security Configuration**
   ```toml
   # .streamlit/config.toml for production
   [server]
   enableCORS = false
   enableXsrfProtection = true
   
   [client]
   caching = true
   displayEnabled = false  # Disable development features
   ```

3. **Reverse Proxy Setup (Nginx)**
   ```nginx
   server {
       listen 80;
       server_name your-frontend-domain.com;
       
       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

4. **SSL/HTTPS Setup**
   ```bash
   # Using certbot for Let's Encrypt
   sudo certbot --nginx -d your-frontend-domain.com
   ```

## UI Components

### URL Components (`components/url_components.py`)

**URL Shortener Form:**
```python
def url_shortener_form():
    """Interactive form for creating short URLs"""
    # Features:
    # - Real-time URL validation
    # - Custom code validation
    # - Success animations
    # - Copy to clipboard functionality
    # - Error handling with user feedback
```

**URL Information Card:**
```python
def url_card(url_data):
    """Display URL information in card format"""
    # Features:
    # - Click metrics
    # - Status indicators
    # - Truncated URL display
    # - Action buttons
```

### Analytics Components (`components/analytics_components.py`)

**Metrics Dashboard:**
```python
def analytics_metrics(analytics_data):
    """Display key performance metrics"""
    # Features:
    # - KPI cards with formatted numbers
    # - Delta indicators
    # - Responsive column layout
    # - Icon integration
```

**Interactive Charts:**
```python
def click_timeline_chart(timeline_data):
    """Time-series chart of click activity"""
    # Features:
    # - Plotly line charts
    # - Hover information
    # - Responsive design
    # - Date formatting
```

**Geographic Visualization:**
```python
def top_countries_chart(countries_data):
    """Horizontal bar chart of top countries"""
    # Features:
    # - Interactive bars
    # - Sorted by frequency
    # - Color coding
    # - Mobile optimized
```

## Testing

### Manual Testing

**URL Shortening Flow:**
```bash
# 1. Access the application
open http://localhost:8501

# 2. Test URL shortening
# - Enter valid URL: https://example.com
# - Try custom code: test123
# - Verify success message and short URL generation

# 3. Test validation
# - Enter invalid URL: not-a-url
# - Try invalid custom code: ab (too short)
# - Verify error messages appear
```

**Analytics Testing:**
```bash
# 1. Create a short URL
# 2. Visit the short URL multiple times
# 3. Check analytics page
# 4. Verify metrics update
# 5. Test charts and visualizations
```

### Automated Testing

**Setup Test Environment:**
```bash
# Install testing dependencies
pip install pytest streamlit-test selenium

# Create test configuration
export API_BASE_URL=http://localhost:8000
export STREAMLIT_TEST_MODE=true
```

**Example Test Cases:**
```python
# tests/test_frontend.py
import pytest
import streamlit as st
from unittest.mock import patch, MagicMock

def test_url_validation():
    """Test URL validation function"""
    from services.utils import validate_url
    
    assert validate_url("https://example.com") == True
    assert validate_url("http://test.com") == True
    assert validate_url("not-a-url") == False
    assert validate_url("") == False

def test_custom_code_validation():
    """Test custom code validation"""
    from services.utils import validate_custom_code
    
    assert validate_custom_code("test123") == True
    assert validate_custom_code("my-code") == True
    assert validate_custom_code("ab") == False  # Too short
    assert validate_custom_code("a" * 25) == False  # Too long

@patch('services.api_client.requests.Session.request')
def test_api_client(mock_request):
    """Test API client functionality"""
    from services.api_client import api_client
    
    # Mock successful response
    mock_response = MagicMock()
    mock_response.json.return_value = {"short_code": "test123"}
    mock_response.raise_for_status.return_value = None
    mock_request.return_value = mock_response
    
    result = api_client.create_short_url("https://example.com")
    assert result["short_code"] == "test123"
```

**Run Tests:**
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=services --cov=components tests/

# Run specific test
pytest tests/test_frontend.py::test_url_validation -v
```

## Debugging

### Common Issues and Solutions

**1. API Connection Issues**
```bash
# Check API gateway status
curl http://localhost:8000/health/all

# Verify environment variables
echo $API_BASE_URL

# Test API endpoints manually
curl -X POST "http://localhost:8000/api/v1/shorten" \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://example.com"}'
```

**2. Streamlit Not Loading**
```bash
# Check if port is available
lsof -i :8501

# Check Streamlit configuration
streamlit config show

# Run with debug logging
streamlit run app.py --logger.level debug
```

**3. Chart Rendering Issues**
```bash
# Clear Streamlit cache
streamlit cache clear

# Check browser console for errors
# F12 -> Console tab in browser

# Verify Plotly installation
python -c "import plotly; print(plotly.__version__)"
```

**4. Import Errors**
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Verify all dependencies
pip list | grep -E "(streamlit|plotly|pandas|requests)"

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Debug Mode

**Enable Debug Logging:**
```python
# Add to app.py for debugging
import logging
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Debug session state
if st.checkbox("Show Debug Info"):
    st.write("Session State:", st.session_state)
    st.write("Query Params:", st.experimental_get_query_params())
```

**Streamlit Debug Mode:**
```bash
# Run with development mode
streamlit run app.py --server.runOnSave true

# Enable file watcher
streamlit run app.py --server.fileWatcherType poll
```

## Performance Optimization

### Caching Strategies

**API Response Caching:**
```python
import streamlit as st

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_global_analytics():
    """Cache global analytics data"""
    return api_client.get_global_analytics()

@st.cache_data(ttl=60)  # Cache for 1 minute
def get_url_analytics(short_code):
    """Cache URL-specific analytics"""
    return api_client.get_url_analytics(short_code)
```

**Chart Optimization:**
```python
@st.cache_data
def create_timeline_chart(timeline_data):
    """Cache chart generation"""
    # Chart creation logic here
    return fig
```

### Load Time Optimization

**Lazy Loading:**
```python
# Load charts only when needed
if st.button("Load Analytics"):
    with st.spinner("Loading..."):
        analytics_data = get_analytics()
        display_charts(analytics_data)
```

**Pagination:**
```python
# For large datasets
def paginate_data(data, page_size=20, page_number=1):
    start = (page_number - 1) * page_size
    end = start + page_size
    return data[start:end]
```

### Memory Management

**Session State Cleanup:**
```python
# Clear unnecessary session state
if 'large_data' in st.session_state:
    del st.session_state['large_data']
```

**Efficient Data Loading:**
```python
# Load only required data
@st.cache_data
def get_summary_stats():
    """Load only summary statistics, not raw data"""
    return api_client.get_global_analytics()
```

## Security Considerations

### Input Validation

**URL Sanitization:**
```python
def sanitize_url(url):
    """Sanitize URL input"""
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url
```

**XSS Prevention:**
```python
import html

def safe_display_text(text):
    """Escape HTML in user input"""
    return html.escape(text)
```

### API Security

**Request Timeout:**
```python
# Configure reasonable timeouts
self.session.timeout = 10  # 10 second timeout
```

**Error Handling:**
```python
def secure_api_call(func, *args, **kwargs):
    """Wrapper for secure API calls"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        # Log error without exposing sensitive info
        logger.error(f"API call failed: {type(e).__name__}")
        st.error("An error occurred. Please try again.")
        return None
```

## Mobile Responsiveness

### Responsive Layout

**Column Adaptation:**
```python
# Responsive column layout
if st.sidebar.button("Toggle Mobile View"):
    # Mobile layout
    st.write("Mobile optimized view")
    col1 = st.container()
    col2 = st.container()
else:
    # Desktop layout
    col1, col2 = st.columns(2)
```

**Chart Responsiveness:**
```python
# Mobile-friendly charts
fig.update_layout(
    height=400,  # Fixed height for mobile
    margin=dict(l=20, r=20, t=40, b=20),  # Reduced margins
    font=dict(size=12)  # Readable font size
)
```

## Future Enhancements

### Planned Features

**Advanced Analytics:**
- Real-time analytics dashboard
- A/B testing interface
- Custom date range selection
- Export functionality (PDF, CSV)
- Comparative analytics

**User Experience:**
- Dark/light theme toggle
- Keyboard shortcuts
- Bulk URL operations
- URL preview functionality
- Advanced filtering and search

**Technical Improvements:**
- WebSocket integration for real-time updates
- Progressive Web App (PWA) capabilities
- Offline functionality
- Advanced caching strategies
- Multi-language support

### Integration Opportunities

**External Services:**
- Social media sharing
- QR code generation
- Email integration
- Slack/Teams notifications
- Google Analytics integration

**API Enhancements:**
- Batch operations
- Webhook notifications
- Custom domains
- User authentication
- Role-based access control

## Contributing

### Development Setup

```bash
# Fork and clone repository
git clone https://github.com/yourusername/links-from-liliput.git
cd links-from-liliput/streamlit-frontend

# Create feature branch
git checkout -b feature/frontend-enhancement

# Setup development environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Code Standards

**File Organization:**
- Components in `components/` directory
- Services in `services/` directory
- Pages in `pages/` directory
- Configuration in `config/` directory

**Naming Conventions:**
- Use descriptive function names
- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Use type hints where applicable

**Testing Requirements:**
- Add tests for new functionality
- Ensure API integration tests pass
- Test on multiple screen sizes
- Validate all user inputs

### Pull Request Process

1. **Create Feature Branch**
2. **Implement Changes**
3. **Add/Update Tests**
4. **Update Documentation**
5. **Test Thoroughly**
6. **Submit Pull Request**

## Troubleshooting

### Quick Diagnostics

```bash
# Complete system check
echo "=== Streamlit Frontend Diagnostics ==="

echo "1. Python Version:"
python --version

echo "2. Streamlit Version:"
streamlit --version

echo "3. Backend API Health:"
curl -s http://localhost:8000/health/all | jq || echo "API not responding"

echo "4. Required Packages:"
pip list | grep -E "(streamlit|plotly|pandas|requests)"

echo "5. Port Availability:"
lsof -i :8501 | head -2

echo "6. Configuration:"
streamlit config show | head -10
```

### Common Error Solutions

**Import Errors:**
```bash
# Reinstall dependencies
pip uninstall streamlit plotly pandas requests
pip install -r requirements.txt
```

**Port Conflicts:**
```bash
# Use different port
streamlit run app.py --server.port 8502
```

**API Connection:**
```bash
# Check backend services
docker-compose ps
curl http://localhost:8000/health/all
```

---

**Application Status**: ✅ Active  
**Port**: 8501  
**Framework**: Streamlit  
**Backend Dependencies**: API Gateway, URL Service, Analytics Service  
**Maintainer**: Dinesh Bhusal  
**Last Updated**: August 15, 2025

The Streamlit frontend provides an intuitive, responsive interface for your URL shortener platform with comprehensive analytics and real-time updates.