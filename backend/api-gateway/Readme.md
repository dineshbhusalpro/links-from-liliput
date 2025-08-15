# API Gateway

The central API Gateway for the Links from Liliput URL shortener microservices architecture. This service acts as the single entry point for all client requests, providing routing, authentication, rate limiting, load balancing, and service orchestration across the URL and Analytics services.

## Overview

The API Gateway serves as the unified interface between clients and the microservices backend. It handles cross-cutting concerns like authentication, rate limiting, logging, and service discovery while routing requests to appropriate downstream services. All external traffic flows through this gateway, ensuring consistent security, monitoring, and performance optimization.

## Architecture

```
Internet Users
        ↓
    Nginx (Port 80)
        ↓
API Gateway (Port 8000)
   ↙️            ↘️
URL Service     Analytics Service
(Port 8001)     (Port 8002)
```

**Request Flow:**
1. Client sends request to API Gateway
2. Gateway applies middleware (auth, rate limiting, logging)
3. Service discovery routes to appropriate microservice
4. Response aggregation and formatting
5. Analytics tracking (for redirects)
6. Return response to client

## Project Structure

```
api-gateway/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── config.py                  # Configuration settings
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth_middleware.py     # API key authentication
│   │   ├── rate_limiter.py        # Redis-based rate limiting
│   │   └── logging_middleware.py  # Request/response logging
│   ├── routes/
│   │   ├── __init__.py
│   │   └── gateway_routes.py      # API routing and forwarding
│   └── services/
│       ├── __init__.py
│       └── service_discovery.py   # Service discovery and health checks
├── requirements.txt
├── .env
├── Dockerfile
└── README.md
```

## Features

### Security & Authentication
- **API Key Authentication**: Secure endpoints with configurable API keys
- **Rate Limiting**: Redis-based distributed rate limiting
- **Request Validation**: Input validation and sanitization
- **CORS Management**: Configurable cross-origin resource sharing
- **Security Headers**: Automatic security header injection

### Traffic Management
- **Load Balancing**: Intelligent request distribution
- **Service Discovery**: Automatic service health monitoring
- **Request Routing**: Path-based routing to microservices
- **Retry Logic**: Automatic retry on service failures
- **Circuit Breaker**: Protection against cascade failures

### Monitoring & Observability
- **Request Logging**: Comprehensive request/response logging
- **Performance Metrics**: Response time tracking
- **Health Checks**: Individual and aggregate service health
- **Error Tracking**: Detailed error logging and reporting
- **Analytics Integration**: Automatic click tracking for URLs

### Performance Optimization
- **Redis Caching**: Distributed caching layer
- **Connection Pooling**: Efficient HTTP client management
- **Async Processing**: Full async/await implementation
- **Response Compression**: Automatic response compression
- **Timeout Management**: Configurable service timeouts

## Tech Stack

- **Framework**: FastAPI 0.104.1
- **Runtime**: Python 3.11
- **HTTP Client**: httpx 0.25.2 (async HTTP client)
- **Caching**: Redis 5.0.1
- **Rate Limiting**: slowapi 0.1.9 + Redis
- **Authentication**: Custom API key middleware
- **Configuration**: python-dotenv 1.0.0 + Pydantic
- **ASGI Server**: Uvicorn with standard extensions

## API Endpoints

### Core Gateway Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/health` | Gateway health check | No |
| `GET` | `/health/all` | All services health check | No |

### URL Management (Proxied to URL Service)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/v1/shorten` | Create short URL | No |
| `GET` | `/api/v1/urls/{short_code}/stats` | Get URL statistics | No |
| `DELETE` | `/api/v1/urls/{short_code}` | Deactivate URL | Yes |
| `GET` | `/{short_code}` | Redirect to original URL | No |

### Analytics (Proxied to Analytics Service)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/v1/analytics/{short_code}` | Get URL analytics | No |
| `GET` | `/api/v1/analytics/global` | Get global analytics | No |

### Detailed API Documentation

**Create Short URL:**
```bash
curl -X POST "http://localhost:8000/api/v1/shorten" \
  -H "Content-Type: application/json" \
  -d '{
    "original_url": "https://example.com/very/long/url",
    "custom_code": "my-link"
  }'

Response:
{
  "short_code": "my-link",
  "original_url": "https://example.com/very/long/url", 
  "short_url": "http://localhost:8000/my-link",
  "created_at": "2025-08-15T10:30:00Z",
  "expires_at": null,
  "is_active": true
}
```

**URL Redirect with Analytics:**
```bash
curl -L "http://localhost:8000/my-link"

# Automatically:
# 1. Records analytics event
# 2. Redirects to original URL
# 3. Returns 307 redirect response
```

**Health Check All Services:**
```bash
curl "http://localhost:8000/health/all"

Response:
{
  "gateway": "healthy",
  "services": {
    "url-service": true,
    "analytics-service": true
  },
  "overall_status": "healthy"
}
```

**Get URL Analytics:**
```bash
curl "http://localhost:8000/api/v1/analytics/my-link"

Response:
{
  "short_code": "my-link",
  "total_clicks": 42,
  "unique_clicks": 28,
  "clicks_today": 5,
  "clicks_this_week": 23,
  "clicks_this_month": 42,
  "top_countries": [...],
  "top_referers": [...],
  "click_timeline": [...]
}
```

**Protected Endpoint (Delete URL):**
```bash
curl -X DELETE "http://localhost:8000/api/v1/urls/my-link" \
  -H "Authorization: Bearer your-api-key"

Response:
{
  "message": "URL deactivated successfully",
  "short_code": "my-link"
}
```

## Configuration

### Environment Variables

Create a `.env` file in the api-gateway directory:

```bash
# Service Discovery Configuration
URL_SERVICE_URL=http://localhost:8001
ANALYTICS_SERVICE_URL=http://localhost:8002

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Security Configuration
API_KEY=your-secure-api-gateway-key-here
ENVIRONMENT=development

# Rate Limiting Configuration
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_BURST=10
RATE_LIMIT_WINDOW_SIZE=60

# Timeout Configuration
SERVICE_TIMEOUT_SECONDS=30
HTTP_CLIENT_TIMEOUT=30
CONNECTION_POOL_SIZE=100

# Logging Configuration
LOG_LEVEL=INFO
ENABLE_ACCESS_LOGS=true
ENABLE_ERROR_LOGS=true

# CORS Configuration
CORS_ORIGINS=["*"]
CORS_METHODS=["GET", "POST", "PUT", "DELETE"]
CORS_HEADERS=["*"]

# Performance Configuration
ENABLE_COMPRESSION=true
MAX_REQUEST_SIZE=10485760  # 10MB
```

### Configuration Details

- **URL_SERVICE_URL**: URL of the URL shortening microservice
- **ANALYTICS_SERVICE_URL**: URL of the analytics microservice  
- **API_KEY**: Secret key for protected endpoints
- **RATE_LIMIT_PER_MINUTE**: Maximum requests per IP per minute
- **SERVICE_TIMEOUT_SECONDS**: Timeout for downstream service calls
- **CORS_ORIGINS**: Allowed origins for CORS (use specific domains in production)

## Deployment

### Local Development

1. **Prerequisites**
   ```bash
   # Ensure Python 3.11+, Redis, and downstream services are running
   python --version  # Should be 3.11+
   redis-cli ping    # Should return PONG
   
   # Ensure URL and Analytics services are running
   curl http://localhost:8001/health  # URL service
   curl http://localhost:8002/health  # Analytics service
   ```

2. **Setup Virtual Environment**
   ```bash
   cd api-gateway
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Start the Gateway**
   ```bash
   # Development mode with auto-reload
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   
   # Or using the Python module
   python -m app.main
   ```

6. **Verify Gateway**
   ```bash
   # Health check
   curl http://localhost:8000/health
   
   # All services health
   curl http://localhost:8000/health/all
   
   # Test rate limiting
   for i in {1..5}; do curl http://localhost:8000/health; done
   ```

### Docker Deployment

**Standalone Container:**
```bash
# Build the container
docker build -t api-gateway .

# Run with environment variables
docker run -d \
  --name api-gateway \
  -p 8000:8000 \
  -e URL_SERVICE_URL=http://url-service:8001 \
  -e ANALYTICS_SERVICE_URL=http://analytics-service:8002 \
  -e REDIS_URL=redis://redis:6379/0 \
  -e API_KEY=your-secure-key \
  api-gateway
```

**Using Docker Compose (Recommended):**
```bash
# From the root directory
docker-compose up -d api-gateway

# View logs
docker-compose logs -f api-gateway

# Scale gateway instances
docker-compose up -d --scale api-gateway=3

# Check health
curl http://localhost:8000/health/all
```

### Production Deployment

1. **Environment Configuration**
   ```bash
   # Set production environment variables
   export ENVIRONMENT=production
   export API_KEY=super-secure-production-key
   export RATE_LIMIT_PER_MINUTE=100
   export CORS_ORIGINS='["https://yourdomain.com"]'
   export LOG_LEVEL=WARNING
   ```

2. **Production Server**
   ```bash
   # Run with multiple workers for high availability
   uvicorn app.main:app \
     --host 0.0.0.0 \
     --port 8000 \
     --workers 4 \
     --access-log \
     --log-level info \
     --proxy-headers \
     --forwarded-allow-ips='*'
   ```

3. **Load Balancer Configuration**
   ```bash
   # Configure Nginx upstream (example)
   upstream api_gateway {
       server api-gateway-1:8000;
       server api-gateway-2:8000;
       server api-gateway-3:8000;
   }
   ```

4. **Health Monitoring**
   ```bash
   # Set up health check monitoring
   curl -f http://localhost:8000/health || exit 1
   ```

## Security

### API Key Authentication

**Setup:**
```python
# In .env file
API_KEY=your-super-secure-api-key-here

# Protected endpoints require Authorization header
Authorization: Bearer your-super-secure-api-key-here
```

**Usage:**
```bash
# Accessing protected endpoint
curl -X DELETE "http://localhost:8000/api/v1/urls/test123" \
  -H "Authorization: Bearer your-super-secure-api-key-here"
```

### Rate Limiting

**Configuration:**
```python
# Redis-based distributed rate limiting
RATE_LIMIT_PER_MINUTE=60  # 60 requests per minute per IP
RATE_LIMIT_BURST=10       # Allow bursts up to 10 requests
```

**Rate Limit Headers:**
```bash
# Response includes rate limit information
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1692105600
```

**Rate Limit Exceeded:**
```json
HTTP 429 Too Many Requests
{
  "detail": "Rate limit exceeded. Please try again later."
}
```

### CORS Configuration

**Development:**
```python
CORS_ORIGINS=["*"]  # Allow all origins for development
```

**Production:**
```python
CORS_ORIGINS=["https://yourdomain.com", "https://app.yourdomain.com"]
```

## Monitoring & Logging

### Request Logging

**Log Format:**
```
2025-08-15 10:30:45 - gateway - INFO - Request: POST /api/v1/shorten from 192.168.1.100
2025-08-15 10:30:45 - gateway - INFO - Response: 200 processed in 0.1234s
```

**Custom Headers:**
```bash
# Response includes processing time
X-Process-Time: 0.1234
X-Service-Version: 1.0.0
```

### Health Monitoring

**Individual Service Health:**
```bash
# Check specific service
curl http://localhost:8000/health

Response:
{
  "status": "healthy",
  "service": "api-gateway"
}
```

**Aggregate Health Check:**
```bash
# Check all services
curl http://localhost:8000/health/all

Response:
{
  "gateway": "healthy",
  "services": {
    "url-service": true,
    "analytics-service": true
  },
  "overall_status": "healthy"
}
```

### Error Handling

**Service Unavailable:**
```json
HTTP 503 Service Unavailable
{
  "detail": "URL service unavailable"
}
```

**Internal Server Error:**
```json
HTTP 500 Internal Server Error
{
  "detail": "Internal server error"
}
```

## Testing

### Test Setup

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx pytest-mock

# Create test configuration
export API_KEY=test-api-key
export REDIS_URL=redis://localhost:6379/3  # Use test Redis DB
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test categories
pytest tests/test_gateway_routes.py    # Route tests
pytest tests/test_middleware.py        # Middleware tests
pytest tests/test_service_discovery.py # Service discovery tests

# Run integration tests
pytest tests/integration/ -v

# Test rate limiting
pytest tests/test_rate_limiting.py -v
```

### Test Structure

```
tests/
├── __init__.py
├── conftest.py                 # Test configuration and fixtures
├── test_gateway_routes.py      # API route tests
├── test_middleware.py          # Middleware functionality tests
├── test_service_discovery.py   # Service discovery tests
├── test_rate_limiting.py       # Rate limiting tests
├── test_auth_middleware.py     # Authentication tests
└── integration/
    ├── __init__.py
    ├── test_full_flow.py       # End-to-end tests
    └── test_service_health.py  # Health check tests
```

### Example Test Cases

```python
# tests/test_gateway_routes.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test gateway health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_shorten_url_proxy():
    """Test URL shortening through gateway"""
    response = client.post(
        "/api/v1/shorten",
        json={
            "original_url": "https://example.com",
            "custom_code": "test123"
        }
    )
    assert response.status_code == 200
    assert "short_code" in response.json()

def test_rate_limiting():
    """Test rate limiting functionality"""
    # Make multiple requests to trigger rate limit
    for i in range(65):  # Exceed 60 requests per minute
        response = client.get("/health")
        if i < 60:
            assert response.status_code == 200
        else:
            assert response.status_code == 429

def test_protected_endpoint():
    """Test API key authentication"""
    # Without API key
    response = client.delete("/api/v1/urls/test123")
    assert response.status_code == 401
    
    # With valid API key
    response = client.delete(
        "/api/v1/urls/test123",
        headers={"Authorization": "Bearer test-api-key"}
    )
    assert response.status_code in [200, 404]  # 404 if URL doesn't exist
```

## Debugging

### Logging Configuration

**Enable Debug Logging:**
```bash
# In .env file
LOG_LEVEL=DEBUG
ENABLE_ACCESS_LOGS=true
ENABLE_ERROR_LOGS=true

# Or via environment variable
export LOG_LEVEL=DEBUG
```

**Detailed Request Logging:**
```python
# Add to app/main.py for debugging
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
)

# Enable httpx request logging
logging.getLogger("httpx").setLevel(logging.DEBUG)
```

### Common Issues and Solutions

**1. Service Discovery Issues**
```bash
# Check downstream services
curl http://localhost:8001/health  # URL service
curl http://localhost:8002/health  # Analytics service

# Test service discovery manually
python -c "
from app.services.service_discovery import ServiceDiscovery
import asyncio

async def test():
    sd = ServiceDiscovery()
    health = await sd.health_check('url-service')
    print(f'URL Service Health: {health}')

asyncio.run(test())
"
```

**2. Rate Limiting Issues**
```bash
# Check Redis connectivity
redis-cli ping

# Check rate limit keys
redis-cli keys "rate_limit:*"

# Clear rate limit for IP
redis-cli del "rate_limit:192.168.1.100"

# Monitor rate limiting in real-time
redis-cli monitor | grep rate_limit
```

**3. Authentication Problems**
```bash
# Test API key validation
curl -X DELETE "http://localhost:8000/api/v1/urls/test" \
  -H "Authorization: Bearer wrong-key" \
  -v

# Check API key configuration
echo $API_KEY

# Test with correct API key
curl -X DELETE "http://localhost:8000/api/v1/urls/test" \
  -H "Authorization: Bearer $API_KEY" \
  -v
```

**4. Request Forwarding Issues**
```bash
# Enable debug logging and check logs
tail -f /var/log/api-gateway/debug.log

# Test direct service access
curl http://localhost:8001/urls/  # Direct to URL service
curl http://localhost:8000/api/v1/shorten  # Through gateway

# Check network connectivity
telnet localhost 8001
telnet localhost 8002
```

### Performance Debugging

**Response Time Analysis:**
```bash
# Check response times
curl -w "@curl-format.txt" http://localhost:8000/health

# curl-format.txt content:
#     time_namelookup:  %{time_namelookup}\n
#        time_connect:  %{time_connect}\n
#     time_appconnect:  %{time_appconnect}\n
#    time_pretransfer:  %{time_pretransfer}\n
#       time_redirect:  %{time_redirect}\n
#  time_starttransfer:  %{time_starttransfer}\n
#                     ----------\n
#          time_total:  %{time_total}\n
```

**Connection Pool Monitoring:**
```python
# Add to middleware for monitoring
@app.middleware("http")
async def connection_monitoring(request: Request, call_next):
    # Log connection pool status
    logger.info(f"Active connections: {httpx_client.pool_size}")
    response = await call_next(request)
    return response
```

**Redis Performance:**
```bash
# Monitor Redis performance
redis-cli monitor | grep -E "(rate_limit|analytics)"

# Check Redis memory usage
redis-cli info memory

# Monitor slow commands
redis-cli slowlog get 10
```

## Maintenance

### Routine Tasks

**Health Check Monitoring:**
```bash
# Set up cron job for health monitoring
*/5 * * * * curl -f http://localhost:8000/health/all || echo "Gateway unhealthy" | mail admin@yourdomain.com
```

**Log Rotation:**
```bash
# Configure log rotation
# /etc/logrotate.d/api-gateway
/var/log/api-gateway/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    copytruncate
}
```

**Cache Maintenance:**
```bash
# Clear rate limiting cache (if needed)
redis-cli -n 0 flushdb

# Monitor cache memory usage
redis-cli info memory | grep used_memory
```

**Security Updates:**
```bash
# Rotate API keys regularly
export NEW_API_KEY=$(openssl rand -base64 32)
# Update configuration and restart services
```

### Performance Tuning

**Connection Pool Optimization:**
```python
# In app/services/service_discovery.py
self.client = httpx.AsyncClient(
    timeout=30.0,
    limits=httpx.Limits(
        max_keepalive_connections=20,
        max_connections=100,
        keepalive_expiry=30.0
    )
)
```

**Rate Limiting Optimization:**
```python
# Adjust rate limiting based on traffic patterns
RATE_LIMIT_PER_MINUTE=120  # Increase for higher traffic
RATE_LIMIT_BURST=20        # Allow larger bursts
```

**Redis Optimization:**
```bash
# Configure Redis for API Gateway workload
redis-cli config set tcp-keepalive 60
redis-cli config set timeout 0
redis-cli config set maxclients 10000
```

## Scaling

### Horizontal Scaling

**Multiple Gateway Instances:**
```yaml
# docker-compose.yml
services:
  api-gateway-1:
    build: ./api-gateway
    ports: ["8000:8000"]
  
  api-gateway-2:
    build: ./api-gateway
    ports: ["8001:8000"]
  
  api-gateway-3:
    build: ./api-gateway
    ports: ["8002:8000"]
```

**Load Balancer Configuration:**
```nginx
# nginx.conf
upstream api_gateway {
    least_conn;
    server api-gateway-1:8000 weight=1;
    server api-gateway-2:8000 weight=1;
    server api-gateway-3:8000 weight=1;
}

server {
    listen 80;
    location / {
        proxy_pass http://api_gateway;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Vertical Scaling

**Resource Allocation:**
```yaml
# docker-compose.yml
api-gateway:
  deploy:
    resources:
      limits:
        cpus: '2.0'
        memory: 2G
      reservations:
        cpus: '1.0'
        memory: 1G
```

**Worker Configuration:**
```bash
# Production deployment with multiple workers
uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 8 \
  --worker-class uvicorn.workers.UvicornWorker
```

## Integration

### Service Discovery

The gateway automatically discovers and health-checks downstream services:

```python
# Automatic service registration
services = {
    "url-service": settings.url_service_url,
    "analytics-service": settings.analytics_service_url
}

# Automatic health checking
for service_name in services:
    health_status = await service_discovery.health_check(service_name)
```

### Analytics Integration

Automatic analytics tracking for all redirects:

```python
# Seamless analytics integration
# No additional configuration needed
# Every redirect automatically records analytics
```

### Frontend Integration

**JavaScript SDK Example:**
```javascript
// API Gateway client
class GatewayClient {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
    }
    
    async shortenUrl(originalUrl, customCode = null) {
        const response = await fetch(`${this.baseUrl}/api/v1/shorten`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ original_url: originalUrl, custom_code: customCode })
        });
        return response.json();
    }
    
    async getAnalytics(shortCode) {
        const response = await fetch(`${this.baseUrl}/api/v1/analytics/${shortCode}`);
        return response.json();
    }
}
```

## Contributing

1. **Development Setup**
   ```bash
   git checkout -b feature/gateway-enhancement
   cd api-gateway
   python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Testing Guidelines**
   ```bash
   # Ensure all tests pass
   pytest --cov=app
   
   # Test with real services
   pytest tests/integration/ -v
   ```

3. **Code Standards**
   - Follow FastAPI best practices
   - Maintain async/await patterns
   - Add comprehensive error handling
   - Update documentation

## Troubleshooting

### Quick Diagnostics

```bash
# Complete system health check
echo "=== Gateway Health ==="
curl -s http://localhost:8000/health | jq

echo "=== All Services Health ==="
curl -s http://localhost:8000/health/all | jq

echo "=== Rate Limiting Test ==="
for i in {1..3}; do 
    curl -s -w "Status: %{http_code}, Time: %{time_total}s\n" \
         -o /dev/null http://localhost:8000/health
done

echo "=== Service Discovery ==="
curl -s http://localhost:8001/health | jq  # URL Service
curl -s http://localhost:8002/health | jq  # Analytics Service

echo "=== Redis Connectivity ==="
redis-cli ping
```

---

**Service Status**: ✅ Active  
**Port**: 8000  
**Type**: API Gateway  
**Dependencies**: Redis, URL Service, Analytics Service  
**Maintainer**: Dinesh Bhusal   
**Last Updated**: August 15, 2025

The API Gateway serves as the intelligent entry point for your microservices architecture, providing security, performance, and reliability for all client interactions.