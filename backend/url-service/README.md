# URL Service

The core URL shortening microservice for the Links from Liliput project. This service handles URL shortening, storage, analytics, and redirection using FastAPI, PostgreSQL, and Redis.

## Architecture

The URL service is a FastAPI-based microservice that provides:
- URL shortening and validation
- Short code generation and management
- Click tracking and analytics
- Redis caching for performance optimization
- PostgreSQL storage with SQLAlchemy ORM

## Project Structure

```
url-service/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py              # Configuration settings
│   ├── database.py            # Database connection and session management
│   ├── models/
│   │   ├── __init__.py
│   │   └── url_model.py       # SQLAlchemy URL model
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── url_schema.py      # Pydantic request/response schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── redis_service.py   # Redis caching service
│   │   └── url_service.py     # Core URL business logic
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py            # Dependency injection
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── url_routes.py  # API endpoints
│   └── utils/
│       ├── __init__.py
│       └── helpers.py         # Utility functions
├── alembic/                   # Database migrations
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

- **URL Shortening**: Convert long URLs to short, memorable codes
- **Custom Short Codes**: Support for user-defined short codes
- **Click Analytics**: Track clicks, timestamps, and referrer information
- **URL Validation**: Comprehensive URL format validation
- **Redis Caching**: High-performance caching for frequently accessed URLs
- **Database Persistence**: PostgreSQL storage with proper indexing
- **Health Monitoring**: Built-in health check endpoints
- **Rate Limiting**: Protection against abuse (handled by API Gateway)
- **Async Operations**: Full async/await support for optimal performance

## Tech Stack

- **Framework**: FastAPI 0.104.1
- **Runtime**: Python 3.11
- **Database**: PostgreSQL with SQLAlchemy 2.0.23
- **Caching**: Redis 5.0.1
- **Migration**: Alembic 1.12.1
- **Validation**: Validators 0.22.0 + Pydantic 2.5.0
- **Testing**: pytest 7.4.3
- **ASGI Server**: Uvicorn

## API Endpoints

### Core Endpoints

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| `POST` | `/urls/` | Create short URL | `{"original_url": "string", "custom_code": "string?"}` |
| `GET` | `/urls/{short_code}/stats` | Get URL analytics | - |
| `DELETE` | `/urls/{short_code}` | Deactivate URL | - |
| `GET` | `/redirect/{short_code}` | Redirect to original URL | - |
| `GET` | `/health` | Service health check | - |

### Request/Response Examples

**Create Short URL:**
```json
POST /urls/
{
    "original_url": "https://example.com/very/long/url/path",
    "custom_code": "my-link"  // optional
}

Response:
{
    "short_code": "my-link",
    "original_url": "https://example.com/very/long/url/path",
    "short_url": "http://localhost/my-link",
    "created_at": "2025-08-15T10:30:00Z",
    "expires_at": null,
    "is_active": true
}
```

**Get URL Statistics:**
```json
GET /urls/my-link/stats

Response:
{
    "short_code": "my-link",
    "original_url": "https://example.com/very/long/url/path",
    "click_count": 42,
    "created_at": "2025-08-15T10:30:00Z",
    "last_accessed": "2025-08-15T15:45:30Z",
    "is_active": true,
    "recent_clicks": [
        {
            "timestamp": "2025-08-15T15:45:30Z",
            "ip_address": "192.168.1.100",
            "user_agent": "Mozilla/5.0...",
            "referrer": "https://google.com"
        }
    ]
}
```

## Configuration

### Environment Variables

Create a `.env` file in the url-service directory:

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/url_shortener_db

# Redis Configuration  
REDIS_URL=redis://localhost:6379/0

# Service Configuration
SERVICE_PORT=8001
ENVIRONMENT=development

# Optional Configuration
URL_EXPIRY_DAYS=365
SHORT_CODE_LENGTH=6
CUSTOM_DOMAIN=yourdomain.com
ENABLE_ANALYTICS=true
CACHE_TTL_SECONDS=3600
```

### Configuration Details

- **DATABASE_URL**: PostgreSQL connection string
- **REDIS_URL**: Redis connection string for caching
- **SERVICE_PORT**: Port number for the service (default: 8001)
- **ENVIRONMENT**: Runtime environment (development/staging/production)
- **URL_EXPIRY_DAYS**: Default URL expiration period
- **SHORT_CODE_LENGTH**: Length of generated short codes
- **CACHE_TTL_SECONDS**: Redis cache time-to-live

## Deployment

### Local Development

1. **Prerequisites**
   ```bash
   # Ensure you have Python 3.11+, PostgreSQL, and Redis installed
   python --version  # Should be 3.11+
   ```

2. **Setup Virtual Environment**
   ```bash
   cd url-service
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   ```bash
   # Create database
   createdb url_shortener_db
   
   # Run migrations
   alembic upgrade head
   ```

5. **Start Redis**
   ```bash
   redis-server
   ```

6. **Run the Service**
   ```bash
   # Development mode with auto-reload
   uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
   
   # Or using the Python module
   python -m app.main
   ```

### Docker Deployment

**Build and Run:**
```bash
# Build the container
docker build -t url-service .

# Run with environment variables
docker run -d \
  --name url-service \
  -p 8001:8001 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e REDIS_URL=redis://redis:6379/0 \
  url-service
```

**Using Docker Compose (Recommended):**
```bash
# From the root directory
docker-compose up -d url-service

# View logs
docker-compose logs -f url-service

# Stop service
docker-compose stop url-service
```

### Production Deployment

1. **Environment Setup**
   ```bash
   # Use production environment variables
   export ENVIRONMENT=production
   export DATABASE_URL=postgresql://prod_user:secure_pass@prod_host:5432/prod_db
   export REDIS_URL=redis://prod_redis:6379/0
   ```

2. **Database Migration**
   ```bash
   # Run migrations in production
   alembic upgrade head
   ```

3. **Service Deployment**
   ```bash
   # Production server with multiple workers
   uvicorn app.main:app \
     --host 0.0.0.0 \
     --port 8001 \
     --workers 4 \
     --access-log \
     --log-level info
   ```

4. **Health Check**
   ```bash
   curl http://localhost:8001/health
   ```

## Database Management

### Migrations

**Create Migration:**
```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Description of changes"

# Create empty migration
alembic revision -m "Manual migration"
```

**Apply Migrations:**
```bash
# Upgrade to latest
alembic upgrade head

# Upgrade to specific revision
alembic upgrade <revision_id>

# Downgrade one revision
alembic downgrade -1
```

**Migration History:**
```bash
# Show current revision
alembic current

# Show migration history
alembic history

# Show pending migrations
alembic show <revision_id>
```

### Database Schema

**URL Model:**
```sql
CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    short_code VARCHAR(50) UNIQUE NOT NULL,
    original_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    click_count INTEGER DEFAULT 0,
    creator_ip VARCHAR(45),
    custom_code BOOLEAN DEFAULT FALSE
);

CREATE TABLE url_clicks (
    id SERIAL PRIMARY KEY,
    url_id INTEGER REFERENCES urls(id),
    clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    referrer TEXT
);

-- Indexes for performance
CREATE INDEX idx_urls_short_code ON urls(short_code);
CREATE INDEX idx_urls_active ON urls(is_active);
CREATE INDEX idx_url_clicks_url_id ON url_clicks(url_id);
CREATE INDEX idx_url_clicks_clicked_at ON url_clicks(clicked_at);
```

## Testing

### Running Tests

```bash
# Install test dependencies (included in requirements.txt)
pip install pytest pytest-asyncio httpx

# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_url_service.py

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "test_create_url"
```

### Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Test configuration and fixtures
├── test_url_service.py      # URL service logic tests
├── test_url_routes.py       # API endpoint tests
├── test_redis_service.py    # Redis caching tests
└── test_database.py         # Database operation tests
```

### Example Tests

```python
# tests/test_url_service.py
import pytest
from app.services.url_service import URLService

@pytest.mark.asyncio
async def test_create_short_url():
    url_service = URLService()
    result = await url_service.create_short_url(
        original_url="https://example.com",
        custom_code=None
    )
    assert result.short_code is not None
    assert len(result.short_code) == 6
    assert result.original_url == "https://example.com"

@pytest.mark.asyncio 
async def test_custom_short_code():
    url_service = URLService()
    result = await url_service.create_short_url(
        original_url="https://example.com",
        custom_code="custom123"
    )
    assert result.short_code == "custom123"
```

## Debugging

### Logging Configuration

The service uses Python's built-in logging with the following levels:

```python
# Logging levels and usage
import logging

# Configure in app/main.py
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
```

### Debug Mode

**Enable Debug Logging:**
```bash
# Set environment variable
export LOG_LEVEL=DEBUG

# Or in .env file
LOG_LEVEL=DEBUG
```

**FastAPI Debug Mode:**
```python
# In app/main.py for development
app = FastAPI(debug=True)

# Run with reload for development
uvicorn app.main:app --reload --log-level debug
```

### Common Issues and Solutions

**1. Database Connection Issues**
```bash
# Check database connectivity
psql -h localhost -U username -d url_shortener_db

# Verify environment variables
echo $DATABASE_URL

# Test connection from Python
python -c "
import psycopg2
conn = psycopg2.connect('$DATABASE_URL')
print('Database connected successfully')
conn.close()
"
```

**2. Redis Connection Issues**
```bash
# Check Redis connectivity
redis-cli ping

# Test Redis from Python
python -c "
import redis
r = redis.from_url('$REDIS_URL')
r.ping()
print('Redis connected successfully')
"
```

**3. Migration Issues**
```bash
# Check current migration status
alembic current

# Reset migrations (DANGER: data loss)
alembic downgrade base
alembic upgrade head

# Manual database reset
dropdb url_shortener_db
createdb url_shortener_db
alembic upgrade head
```

**4. Port Conflicts**
```bash
# Check what's running on port 8001
lsof -i :8001

# Kill process on port
kill -9 $(lsof -t -i:8001)

# Use different port
uvicorn app.main:app --port 8002
```

### Performance Debugging

**Database Query Analysis:**
```python
# Enable SQLAlchemy query logging
import logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

**Redis Performance Monitoring:**
```bash
# Monitor Redis performance
redis-cli monitor

# Check Redis memory usage
redis-cli info memory

# Check cache hit ratio
redis-cli info stats | grep keyspace
```

**Application Metrics:**
```python
# Add timing middleware for performance monitoring
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### Development Tools

**Interactive API Documentation:**
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

**Database Administration:**
```bash
# PostgreSQL command line
psql $DATABASE_URL

# Useful queries
\dt                          # List tables
\d urls                      # Describe urls table
SELECT * FROM urls LIMIT 5;  # Sample data
```

**Redis Administration:**
```bash
# Redis command line
redis-cli

# Useful commands
KEYS url:*                   # List URL cache keys
GET url:short_code          # Get cached URL
FLUSHDB                     # Clear current database (development only)
```

## Maintenance

### Routine Tasks

**Database Cleanup:**
```bash
# Remove expired URLs (if expiry is implemented)
DELETE FROM urls WHERE expires_at < NOW() AND expires_at IS NOT NULL;

# Archive old click data (older than 1 year)
DELETE FROM url_clicks WHERE clicked_at < NOW() - INTERVAL '1 year';
```

**Cache Management:**
```bash
# Clear Redis cache
redis-cli FLUSHDB

# Monitor cache usage
redis-cli INFO memory
```

**Log Rotation:**
```bash
# Configure log rotation in production
# /etc/logrotate.d/url-service
/var/log/url-service/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    copytruncate
}
```

## Monitoring

### Health Checks

**Service Health:**
```bash
curl http://localhost:8001/health
```

**Database Health:**
```bash
# Custom health check endpoint (implement in code)
curl http://localhost:8001/health/database
```

**Redis Health:**
```bash
# Custom health check endpoint (implement in code)  
curl http://localhost:8001/health/redis
```

### Metrics Collection

**Application Metrics:**
- Request count and response times
- Database connection pool status
- Redis cache hit/miss ratio
- URL creation and click rates

**System Metrics:**
- CPU and memory usage
- Database query performance
- Redis memory usage
- Network I/O

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make changes and add tests
4. Run tests: `pytest`
5. Commit changes: `git commit -m "Add new feature"`
6. Push to branch: `git push origin feature/new-feature`
7. Create a Pull Request

## License

This project is part of the Links from Liliput URL shortener service.

---

**Service Status**: ✅ Active  
**Maintainer**: Dinesh Bhusal  
**Last Updated**: August 15, 2025