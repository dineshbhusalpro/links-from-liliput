# Analytics Service

A comprehensive analytics and tracking microservice for the Links from Liliput URL shortener project. This service captures, processes, and provides detailed analytics on URL clicks, user behavior, and traffic patterns using FastAPI, PostgreSQL, and Redis.

## Overview

The Analytics service is a dedicated microservice that handles all tracking and analytics functionality for the URL shortener. It provides real-time click tracking, detailed analytics reports, and performance insights without impacting the core URL shortening functionality.

## Architecture

```
Analytics Service (Port 8002)
├── Click Event Recording
├── Real-time Analytics Processing
├── Geographic Data Analysis
├── Traffic Source Analysis
├── Redis Caching Layer
└── PostgreSQL Data Storage
```

The service operates independently and communicates with other services through HTTP APIs, ensuring loose coupling and high availability.

## Project Structure

```
analytics-service/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── config.py                  # Configuration settings
│   ├── database.py                # Database connection management
│   ├── models/
│   │   ├── __init__.py
│   │   └── analytics_model.py     # SQLAlchemy models for analytics data
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── analytics_schema.py    # Pydantic request/response schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── analytics_service.py   # Core analytics business logic
│   │   └── redis_service.py       # Redis caching service
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py                # Dependency injection
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── analytics_routes.py # API endpoints
│   └── utils/
│       ├── __init__.py
│       └── helpers.py             # Utility functions (user agent parsing, IP geolocation)
├── alembic/                       # Database migrations
│   ├── versions/
│   ├── env.py
│   ├── script.py.mako
│   └── alembic.ini
├── requirements.txt
├── .env
├── Dockerfile
└── README.md
```

## Features

### Core Analytics
- **Click Event Recording**: Capture every URL click with detailed metadata
- **Real-time Analytics**: Instant analytics updates with Redis caching
- **Unique Visitor Tracking**: Track unique visitors by IP address
- **Time-based Analytics**: Clicks today, this week, this month
- **Click Timeline**: Historical click data with time series analysis

### Geographic Intelligence
- **Country Detection**: Basic IP-to-country mapping
- **City Tracking**: Location-based analytics (configurable)
- **Geographic Distribution**: Top countries and regions analysis

### Traffic Source Analysis
- **Referrer Tracking**: Track traffic sources and referring websites
- **User Agent Analysis**: Browser, OS, and device information
- **Direct vs. Referred Traffic**: Comprehensive traffic source breakdown

### Performance & Insights
- **Global Analytics**: Cross-URL performance metrics
- **Top Performing URLs**: Most clicked and trending links
- **Traffic Patterns**: Peak usage times and patterns
- **Conversion Metrics**: Click-through rates and engagement

### Technical Features
- **Asynchronous Processing**: Non-blocking analytics recording
- **Redis Caching**: High-performance data caching (5-minute TTL)
- **Batch Processing**: Efficient bulk analytics operations
- **Health Monitoring**: Comprehensive service health checks
- **Database Optimization**: Proper indexing for fast queries

## Tech Stack

- **Framework**: FastAPI 0.104.1
- **Runtime**: Python 3.11
- **Database**: PostgreSQL with SQLAlchemy 2.0.23
- **Caching**: Redis 5.0.1 (separate database index)
- **Data Analysis**: Pandas 2.1.4
- **Visualization**: Plotly 5.17.0 (for future chart generation)
- **Migration**: Alembic 1.12.1
- **User Agent Parsing**: user-agents 2.2.0
- **Date Handling**: python-dateutil 2.8.2
- **Testing**: pytest with httpx
- **ASGI Server**: Uvicorn

## API Endpoints

### Core Analytics Endpoints

| Method | Endpoint | Description | Access Level |
|--------|----------|-------------|--------------|
| `POST` | `/analytics/events/` | Record click event | Internal |
| `GET` | `/analytics/stats/{short_code}` | Get URL analytics | Public |
| `GET` | `/analytics/global` | Get global analytics | Public |
| `GET` | `/health` | Service health check | Public |

### Detailed API Documentation

**Record Click Event (Internal):**
```json
POST /analytics/events/
Content-Type: application/json

{
    "short_code": "abc123",
    "ip_address": "192.168.1.100",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "referer": "https://google.com",
    "country": "US",
    "city": "New York"
}

Response: true
```

**Get URL Analytics:**
```json
GET /analytics/stats/abc123

Response:
{
    "short_code": "abc123",
    "total_clicks": 142,
    "unique_clicks": 89,
    "clicks_today": 12,
    "clicks_this_week": 67,
    "clicks_this_month": 142,
    "top_countries": [
        {"name": "US", "count": 85},
        {"name": "UK", "count": 23},
        {"name": "CA", "count": 18}
    ],
    "top_referers": [
        {"name": "google.com", "count": 45},
        {"name": "Direct", "count": 32},
        {"name": "twitter.com", "count": 18}
    ],
    "click_timeline": [
        {"date": "2025-08-10", "clicks": 8},
        {"date": "2025-08-11", "clicks": 15},
        {"date": "2025-08-12", "clicks": 23}
    ]
}
```

**Global Analytics Dashboard:**
```json
GET /analytics/global

Response:
{
    "total_clicks": 15234,
    "unique_visitors": 8967,
    "clicks_today": 234,
    "clicks_this_week": 1567,
    "top_urls": [
        {"short_code": "popular1", "clicks": 1234},
        {"short_code": "trending2", "clicks": 987},
        {"short_code": "viral3", "clicks": 756}
    ]
}
```

## Configuration

### Environment Variables

Create a `.env` file in the analytics-service directory:

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/url_shortener_db

# Redis Configuration (separate database index from URL service)
REDIS_URL=redis://localhost:6379/1

# Service Configuration
SERVICE_PORT=8002
ENVIRONMENT=development

# Analytics-Specific Settings
CACHE_TTL=300                    # Cache TTL in seconds (5 minutes)
BATCH_SIZE=1000                  # Batch processing size
ENABLE_GEOLOCATION=true          # Enable IP geolocation
ANALYTICS_RETENTION_DAYS=365     # Data retention period
TOP_RESULTS_LIMIT=10             # Number of top results to return

# Logging Configuration
LOG_LEVEL=INFO
ENABLE_DEBUG_LOGGING=false

# Performance Settings
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
REDIS_CONNECTION_POOL_SIZE=10
```

### Configuration Details

- **DATABASE_URL**: PostgreSQL connection string (shared with URL service)
- **REDIS_URL**: Redis connection with separate database index (1)
- **CACHE_TTL**: How long to cache analytics data in Redis
- **BATCH_SIZE**: Number of records to process in batches
- **ANALYTICS_RETENTION_DAYS**: How long to keep detailed click data

## Deployment

### Local Development

1. **Prerequisites**
   ```bash
   # Ensure Python 3.11+, PostgreSQL, and Redis are installed
   python --version  # Should be 3.11+
   redis-server --version
   psql --version
   ```

2. **Setup Virtual Environment**
   ```bash
   cd analytics-service
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   ```bash
   # The database should already exist from URL service setup
   # Run analytics-specific migrations
   alembic upgrade head
   ```

5. **Start Redis**
   ```bash
   # Redis should already be running for the URL service
   redis-cli ping  # Should return PONG
   ```

6. **Run the Service**
   ```bash
   # Development mode with auto-reload
   uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
   
   # Or using the Python module
   python -m app.main
   ```

7. **Verify Service**
   ```bash
   # Health check
   curl http://localhost:8002/health
   
   # Global analytics (should return empty data initially)
   curl http://localhost:8002/analytics/global
   ```

### Docker Deployment

**Standalone Container:**
```bash
# Build the container
docker build -t analytics-service .

# Run with environment variables
docker run -d \
  --name analytics-service \
  -p 8002:8002 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e REDIS_URL=redis://redis:6379/1 \
  analytics-service
```

**Using Docker Compose (Recommended):**
```bash
# From the root directory
docker-compose up -d analytics-service

# View logs
docker-compose logs -f analytics-service

# Check health
docker-compose exec analytics-service curl localhost:8002/health
```

### Production Deployment

1. **Environment Configuration**
   ```bash
   # Set production environment variables
   export ENVIRONMENT=production
   export DATABASE_URL=postgresql://prod_user:secure_pass@prod_host:5432/prod_db
   export REDIS_URL=redis://prod_redis:6379/1
   export CACHE_TTL=600  # Longer cache in production
   ```

2. **Database Migration**
   ```bash
   # Apply latest migrations
   alembic upgrade head
   ```

3. **Production Server**
   ```bash
   # Run with multiple workers for high load
   uvicorn app.main:app \
     --host 0.0.0.0 \
     --port 8002 \
     --workers 4 \
     --access-log \
     --log-level info
   ```

4. **Health Check & Monitoring**
   ```bash
   # Service health
   curl http://localhost:8002/health
   
   # Check if analytics are being recorded
   curl http://localhost:8002/analytics/global
   ```

## Database Management

### Database Schema

**Click Events Table:**
```sql
CREATE TABLE click_events (
    id SERIAL PRIMARY KEY,
    short_code VARCHAR(50) NOT NULL,
    user_agent TEXT,
    ip_address VARCHAR(45) NOT NULL,
    referer TEXT,
    country VARCHAR(2),
    city VARCHAR(100),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_click_events_short_code ON click_events(short_code);
CREATE INDEX idx_click_events_timestamp ON click_events(timestamp);
CREATE INDEX idx_click_events_ip_address ON click_events(ip_address);
CREATE INDEX idx_click_events_country ON click_events(country);
```

**Analytics Reports Table:**
```sql
CREATE TABLE analytics_reports (
    id SERIAL PRIMARY KEY,
    short_code VARCHAR(50) NOT NULL,
    report_type VARCHAR(50) NOT NULL,
    report_date TIMESTAMP WITH TIME ZONE NOT NULL,
    total_clicks INTEGER DEFAULT 0,
    unique_clicks INTEGER DEFAULT 0,
    top_countries TEXT,
    top_referers TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for reports
CREATE INDEX idx_analytics_reports_short_code ON analytics_reports(short_code);
CREATE INDEX idx_analytics_reports_type_date ON analytics_reports(report_type, report_date);
```

### Migration Management

**Create New Migration:**
```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add new analytics feature"

# Create empty migration for custom SQL
alembic revision -m "Custom analytics optimization"
```

**Apply Migrations:**
```bash
# Upgrade to latest
alembic upgrade head

# Upgrade to specific revision
alembic upgrade abc123

# Downgrade one revision
alembic downgrade -1

# Show current revision
alembic current
```

**Migration Best Practices:**
```bash
# Always backup before migration in production
pg_dump url_shortener_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Test migrations on staging first
alembic upgrade head --dry-run

# Apply with verbose output
alembic upgrade head --verbose
```

## Testing

### Test Setup

```bash
# Install test dependencies (included in requirements.txt)
pip install pytest pytest-asyncio httpx pytest-cov

# Create test database
createdb url_shortener_test_db

# Set test environment
export DATABASE_URL=postgresql://username:password@localhost:5432/url_shortener_test_db
export REDIS_URL=redis://localhost:6379/2  # Use different Redis DB for tests
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test categories
pytest tests/test_analytics_service.py  # Business logic tests
pytest tests/test_routes.py             # API endpoint tests
pytest tests/test_redis_service.py      # Cache tests

# Run tests with verbose output
pytest -v -s

# Run tests matching pattern
pytest -k "test_click_event"

# Run only failed tests from last run
pytest --lf
```

### Test Structure

```
tests/
├── __init__.py
├── conftest.py                    # Test configuration and fixtures
├── test_analytics_service.py      # Core service logic tests
├── test_analytics_routes.py       # API endpoint tests
├── test_redis_service.py          # Redis caching tests
├── test_models.py                 # Database model tests
├── test_helpers.py                # Utility function tests
└── integration/
    ├── __init__.py
    ├── test_full_workflow.py      # End-to-end tests
    └── test_performance.py        # Performance tests
```

### Example Test Cases

```python
# tests/test_analytics_service.py
import pytest
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics_schema import ClickEventCreate

@pytest.mark.asyncio
async def test_record_click_event(db_session):
    """Test recording a click event"""
    analytics_service = AnalyticsService(db_session)
    
    click_data = ClickEventCreate(
        short_code="test123",
        ip_address="192.168.1.100",
        user_agent="Mozilla/5.0 Test Browser",
        referer="https://google.com"
    )
    
    result = await analytics_service.record_click(click_data)
    assert result is True
    
    # Verify data was stored
    analytics = await analytics_service.get_analytics("test123")
    assert analytics.total_clicks == 1
    assert analytics.unique_clicks == 1

@pytest.mark.asyncio
async def test_get_analytics_with_cache(db_session, redis_client):
    """Test analytics retrieval with Redis caching"""
    analytics_service = AnalyticsService(db_session)
    
    # First call should hit database and cache result
    analytics1 = await analytics_service.get_analytics("test123")
    
    # Second call should use cache
    analytics2 = await analytics_service.get_analytics("test123")
    
    assert analytics1.short_code == analytics2.short_code
    # Verify cache was used (can check Redis directly)

def test_global_analytics(db_session):
    """Test global analytics calculation"""
    analytics_service = AnalyticsService(db_session)
    
    global_stats = analytics_service.get_global_analytics()
    
    assert "total_clicks" in global_stats
    assert "unique_visitors" in global_stats
    assert "top_urls" in global_stats
```

## Debugging

### Logging Configuration

**Enable Debug Logging:**
```bash
# In .env file
LOG_LEVEL=DEBUG
ENABLE_DEBUG_LOGGING=true

# Or via environment variable
export LOG_LEVEL=DEBUG
```

**Custom Logging:**
```python
# Add to app/main.py for detailed logging
import logging

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
)

# Enable SQLAlchemy query logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

### Common Issues and Solutions

**1. Redis Connection Issues**
```bash
# Check Redis connectivity
redis-cli -n 1 ping  # Should return PONG (note database 1)

# Check if analytics data is being cached
redis-cli -n 1 keys "analytics:*"

# Clear analytics cache if needed
redis-cli -n 1 flushdb

# Test Redis from Python
python -c "
import redis
r = redis.from_url('redis://localhost:6379/1')
r.ping()
print('Analytics Redis connected successfully')
"
```

**2. Database Performance Issues**
```bash
# Check database connection
psql $DATABASE_URL -c "SELECT COUNT(*) FROM click_events;"

# Analyze slow queries
psql $DATABASE_URL -c "SELECT query, mean_time, calls FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 5;"

# Check index usage
psql $DATABASE_URL -c "SELECT schemaname, tablename, indexname, idx_scan FROM pg_stat_user_indexes WHERE schemaname = 'public';"

# Analyze table sizes
psql $DATABASE_URL -c "SELECT tablename, pg_size_pretty(pg_total_relation_size(tablename::text)) FROM pg_tables WHERE schemaname = 'public';"
```

**3. Analytics Data Issues**
```bash
# Check if events are being recorded
curl -X POST "http://localhost:8002/analytics/events/" \
  -H "Content-Type: application/json" \
  -d '{
    "short_code": "test123",
    "ip_address": "127.0.0.1",
    "user_agent": "Test Browser"
  }'

# Verify data in database
psql $DATABASE_URL -c "SELECT * FROM click_events ORDER BY timestamp DESC LIMIT 5;"

# Check analytics calculation
curl http://localhost:8002/analytics/stats/test123
```

**4. Cache Performance Issues**
```bash
# Monitor Redis memory usage
redis-cli -n 1 info memory

# Check cache hit rates
redis-cli -n 1 info stats | grep keyspace

# Monitor cache keys
redis-cli -n 1 monitor

# Clear specific cache keys
redis-cli -n 1 del "analytics:stats:test123"
```

### Performance Debugging

**Database Query Optimization:**
```python
# Enable query logging in development
import logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Use EXPLAIN ANALYZE for slow queries
from sqlalchemy import text
result = db.execute(text("EXPLAIN ANALYZE SELECT ..."))
```

**Redis Performance Monitoring:**
```bash
# Monitor Redis operations
redis-cli -n 1 monitor | grep analytics

# Check memory usage
redis-cli -n 1 memory usage analytics:stats:abc123

# Monitor slow operations
redis-cli -n 1 config set slowlog-log-slower-than 1000
redis-cli -n 1 slowlog get 10
```

**Application Performance:**
```python
# Add timing middleware for endpoints
import time
from fastapi import Request

@app.middleware("http")
async def analytics_timing_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    if process_time > 0.5:  # Log slow requests
        logger.warning(f"Slow analytics request: {request.url} took {process_time:.2f}s")
    
    response.headers["X-Analytics-Process-Time"] = str(process_time)
    return response
```

### Development Tools

**Interactive API Documentation:**
- Swagger UI: `http://localhost:8002/docs`
- ReDoc: `http://localhost:8002/redoc`

**Database Administration:**
```bash
# Connect to database
psql $DATABASE_URL

# Useful analytics queries
\dt                                    # List tables

# View recent click events
SELECT short_code, ip_address, timestamp, referer 
FROM click_events 
ORDER BY timestamp DESC 
LIMIT 10;

# Top clicked URLs
SELECT short_code, COUNT(*) as clicks, COUNT(DISTINCT ip_address) as unique_clicks
FROM click_events 
GROUP BY short_code 
ORDER BY clicks DESC 
LIMIT 10;

# Analytics by country
SELECT country, COUNT(*) as clicks
FROM click_events 
WHERE country IS NOT NULL
GROUP BY country 
ORDER BY clicks DESC;

# Daily click trends
SELECT DATE(timestamp) as date, COUNT(*) as clicks
FROM click_events 
WHERE timestamp >= NOW() - INTERVAL '7 days'
GROUP BY DATE(timestamp)
ORDER BY date;
```

**Redis Administration:**
```bash
# Connect to analytics Redis database
redis-cli -n 1

# List analytics cache keys
KEYS analytics:*

# Check specific analytics cache
GET analytics:stats:abc123

# Monitor cache operations
MONITOR

# Check cache memory usage
INFO memory
```

## Monitoring & Maintenance

### Health Monitoring

**Service Health Checks:**
```bash
# Basic health check
curl http://localhost:8002/health

# Check through API Gateway
curl http://localhost:8000/health/all

# Database connectivity check
curl http://localhost:8002/analytics/global
```

**Application Metrics to Monitor:**
- Click event recording rate
- Analytics query response times
- Cache hit/miss ratios
- Database connection pool status
- Redis memory usage
- Top URLs performance

### Routine Maintenance

**Data Cleanup (Recommended Monthly):**
```sql
-- Remove old detailed click events (keep aggregated data)
DELETE FROM click_events 
WHERE timestamp < NOW() - INTERVAL '365 days';

-- Cleanup test data
DELETE FROM click_events 
WHERE short_code LIKE 'test%' 
AND timestamp < NOW() - INTERVAL '7 days';

-- Analyze table statistics
ANALYZE click_events;
ANALYZE analytics_reports;

-- Reindex if needed
REINDEX TABLE click_events;
```

**Cache Maintenance:**
```bash
# Clear expired cache entries (automatic, but can force)
redis-cli -n 1 flushdb

# Check cache memory usage
redis-cli -n 1 info memory

# Optimize Redis memory
redis-cli -n 1 memory purge
```

**Log Rotation:**
```bash
# Configure log rotation for production
# /etc/logrotate.d/analytics-service
/var/log/analytics-service/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    copytruncate
}
```

### Performance Optimization

**Database Optimizations:**
```sql
-- Create additional indexes for common queries
CREATE INDEX CONCURRENTLY idx_click_events_short_code_timestamp 
ON click_events(short_code, timestamp DESC);

CREATE INDEX CONCURRENTLY idx_click_events_country_timestamp 
ON click_events(country, timestamp) 
WHERE country IS NOT NULL;

-- Partition large tables by date (for high-volume deployments)
CREATE TABLE click_events_2025_08 PARTITION OF click_events
FOR VALUES FROM ('2025-08-01') TO ('2025-09-01');
```

**Redis Optimizations:**
```bash
# Configure Redis for analytics workload
redis-cli config set maxmemory-policy allkeys-lru
redis-cli config set maxmemory 1gb  # Adjust based on available memory
```

## Integration with Other Services

### API Gateway Integration

The Analytics service automatically integrates with the API Gateway for seamless click tracking:

```python
# Automatic click recording on redirects
# No additional configuration needed - handled by API Gateway
```

### URL Service Integration

While independent, the Analytics service shares the same database for URL metadata:

```python
# Analytics service can reference URL data for enhanced reporting
# Cross-service queries possible through shared database
```

### Frontend Integration

Future integration points for web dashboard:

```javascript
// JavaScript SDK for analytics dashboard
const analytics = new AnalyticsSDK('http://localhost:8000');

// Get URL analytics
const stats = await analytics.getUrlStats('abc123');

// Get global analytics
const global = await analytics.getGlobalStats();
```

## Contributing

1. **Development Setup**
   ```bash
   git checkout -b feature/analytics-enhancement
   cd analytics-service
   python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Make Changes**
   - Add new analytics features
   - Improve performance
   - Add tests for new functionality

3. **Testing**
   ```bash
   pytest --cov=app
   ```

4. **Submit Pull Request**
   - Ensure all tests pass
   - Update documentation
   - Follow commit conventions

## Data Privacy & Compliance

**IP Address Handling:**
- IP addresses are stored for analytics but can be anonymized
- Implement IP hashing for GDPR compliance if needed
- Configurable data retention periods

**Data Retention:**
```python
# Configure in .env
ANALYTICS_RETENTION_DAYS=365
ANONYMIZE_IPS_AFTER_DAYS=30
```

**GDPR Compliance Features:**
- Data export endpoints (implement as needed)
- Data deletion endpoints
- Anonymization utilities

## Future Enhancements

**Planned Features:**
- Real-time analytics dashboard
- Advanced geolocation with MaxMind integration
- Bot detection and filtering
- A/B testing support
- Custom event tracking
- Analytics API rate limiting
- Data export in multiple formats
- Advanced visualization with Plotly

**Scalability Improvements:**
- Event streaming with Apache Kafka
- ClickHouse for large-scale analytics
- Horizontal scaling with service mesh
- CDN integration for global analytics

---

**Service Status**: ✅ Active  
**Port**: 8002  
**Database**: Shared PostgreSQL  
**Cache**: Redis Database 1  
**Maintainer**: Dinesh Bhusal 
**Last Updated**: August 15, 2025

The Analytics service provides comprehensive, real-time analytics for your URL shortener while maintaining high performance and reliability.