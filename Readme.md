# Links from Liliput 🏰

A modern, scalable URL shortener built with microservices architecture. Transform long URLs into short, memorable links with comprehensive analytics and real-time monitoring.

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                   Nginx (Port 80)              │
│              Load Balancer + Proxy             │
└─────────────────┬───────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
┌───────▼────────┐  ┌──────▼─────────┐
│   Streamlit    │  │  API Gateway   │
│   Frontend     │  │   (Port 8000)  │
│  (Port 8501)   │  └──────┬─────────┘
└────────────────┘         │
                   ┌───────┴────────┐
                   │                │
          ┌────────▼──────┐ ┌──────▼──────────┐
          │ URL Service   │ │ Analytics Service│
          │ (Port 8001)   │ │  (Port 8002)    │
          └───────┬───────┘ └─────────┬───────┘
                  │                   │
        ┌─────────┴──────────────────┴─────────┐
        │                                      │
   ┌────▼──────┐                    ┌─────────▼─┐
   │PostgreSQL │                    │   Redis   │
   │(Port 5432)│                    │(Port 6379)│
   └───────────┘                    └───────────┘
```

## Project Structure

```
links-from-liliput/
├── backend/
│   ├── api-gateway/           # API Gateway service
│   ├── url-service/           # URL shortening service
│   └── analytics-service/     # Analytics and tracking service
├── frontend/                  # Streamlit web interface
├── nginx/                     # Load balancer configuration
│   ├── nginx.conf
│   ├── ssl/
│   └── logs/
├── docker-compose.yml         # Main orchestration file
├── docker-compose.prod.yml    # Production configuration
├── Makefile                   # Build and deployment commands
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Git
- 4GB+ RAM recommended

### 1. Clone Repository

```bash
git clone https://github.com/dineshbhusalpro/links-from-liliput.git
cd links-from-liliput
```

### 2. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit configuration (optional for development)
nano .env
```

### 3. Start All Services

```bash
# Start all services
docker-compose up -d

# Check service health
docker-compose ps

# View logs
docker-compose logs -f
```

### 4. Access Applications

- **Web Interface**: http://localhost (via Nginx)
- **API Gateway**: http://localhost/api/v1/
- **Direct Frontend**: http://localhost:8501 (Streamlit)
- **Health Check**: http://localhost/health

### 5. Create Your First Short URL

```bash
# Via API
curl -X POST "http://localhost/api/v1/shorten" \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://example.com", "custom_code": "test123"}'

# Test redirect
curl -L "http://localhost/test123"
```

## Service Documentation

Each service has comprehensive documentation:

### [API Gateway](./backend/api-gateway/README.md)
**Port**: 8000 | **Container**: `liliput_api_gateway`
- Central entry point for all API requests
- Authentication and rate limiting
- Service discovery and health monitoring
- Request routing and load balancing

### [URL Service](./backend/url-service/README.md)
**Port**: 8001 | **Container**: `liliput_url_service`
- Core URL shortening functionality
- PostgreSQL integration with Alembic migrations
- Redis caching for performance
- Custom short code support

### [Analytics Service](./backend/analytics-service/README.md)
**Port**: 8002 | **Container**: `liliput_analytics_service`
- Click tracking and analytics
- Geographic and traffic source analysis
- Real-time metrics and reporting
- Redis caching for analytics data

### [Streamlit Frontend](./frontend/README.md)
**Port**: 8501 | **Container**: `liliput_frontend`
- Interactive web interface
- Real-time analytics dashboards
- URL management and creation
- Responsive design for mobile/desktop

### [Nginx Load Balancer](./nginx/README.md)
**Port**: 80/443 | **Container**: `liliput_nginx`
- Reverse proxy and load balancing
- SSL termination and security headers
- Rate limiting and DDoS protection
- Static file serving and caching

## Development

### Available Commands

```bash
# Start all services
make up

# Stop all services  
make down

# View logs
make logs

# Restart specific service
make restart service=url-service

# Build without cache
make build

# Run tests
make test

# Clean up everything
make clean
```

### Development Tools (Optional)

Start with debug profile for additional tools:

```bash
# Start with development tools
docker-compose --profile debug up -d

# Access tools:
# - Redis Commander: http://localhost:8081 (admin/admin123)
# - pgAdmin: http://localhost:8080 (admin@liliput.com/admin123)  
# - Portainer: http://localhost:9000
```

### Service Health Monitoring

```bash
# Check all services
curl http://localhost/health/all

# Individual service health
curl http://localhost:8001/health  # URL Service
curl http://localhost:8002/health  # Analytics Service
curl http://localhost:8000/health  # API Gateway
curl http://localhost:8501/_stcore/health  # Frontend
```

## Configuration

### Environment Variables

Key configuration options in `.env`:

```bash
# Database
POSTGRES_DB=url_shortener_db
POSTGRES_USER=username
POSTGRES_PASSWORD=password

# API Gateway
API_KEY=secure-api-key-change-in-production
RATE_LIMIT_PER_MINUTE=100

# Environment
ENVIRONMENT=development  # or production
```

### Service Scaling

Scale individual services:

```bash
# Scale API Gateway
docker-compose up -d --scale api-gateway=3

# Scale Frontend
docker-compose up -d --scale frontend=2

# Update Nginx upstream configuration accordingly
```

## Production Deployment

### 1. Production Configuration

```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# Or with environment override
ENVIRONMENT=production docker-compose up -d
```

### 2. SSL Setup

```bash
# Generate SSL certificates
mkdir -p nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/key.pem \
  -out nginx/ssl/cert.pem

# Update nginx.conf for HTTPS
```

### 3. Security Checklist

- [ ] Change default passwords
- [ ] Set strong API keys
- [ ] Configure SSL certificates
- [ ] Update CORS origins
- [ ] Set up log rotation
- [ ] Configure backup strategy

## Monitoring & Analytics

### Health Checks

```bash
# System overview
curl http://localhost/health

# Detailed service health
curl http://localhost/health/all

# Nginx status
curl http://localhost/nginx-status
```

### Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs url-service

# Follow logs
docker-compose logs -f --tail=100
```

### Performance Metrics

```bash
# Database connections
docker-compose exec postgres psql -U username -d url_shortener_db -c "SELECT count(*) FROM pg_stat_activity;"

# Redis memory usage
docker-compose exec redis redis-cli info memory

# Nginx status
curl http://localhost/nginx-status
```

## Testing

### API Testing

```bash
# Create short URL
curl -X POST "http://localhost/api/v1/shorten" \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://google.com"}'

# Get analytics
curl "http://localhost/api/v1/analytics/global"

# Test redirect
curl -I "http://localhost/abc123"
```

### Load Testing

```bash
# Install Apache Bench
apt-get install apache2-utils

# Test frontend
ab -n 1000 -c 10 http://localhost/

# Test API
ab -n 1000 -c 10 -H "Content-Type: application/json" \
   -p test_data.json http://localhost/api/v1/shorten
```

## Troubleshooting

### Common Issues

**Services not starting:**
```bash
# Check service status
docker-compose ps

# View service logs
docker-compose logs service-name

# Restart problematic service
docker-compose restart service-name
```

**Database connection issues:**
```bash
# Check PostgreSQL
docker-compose exec postgres pg_isready -U username

# Check database exists
docker-compose exec postgres psql -U username -l
```

**Redis connection issues:**
```bash
# Test Redis
docker-compose exec redis redis-cli ping

# Check Redis memory
docker-compose exec redis redis-cli info memory
```

**Nginx routing issues:**
```bash
# Test configuration
docker-compose exec nginx nginx -t

# Check upstream health
curl http://localhost/health/all
```

### Debug Mode

```bash
# Start with debug logging
ENVIRONMENT=debug docker-compose up -d

# Enable specific service debug
docker-compose exec url-service python -c "import logging; logging.basicConfig(level=logging.DEBUG)"
```

## Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes and add tests**
4. **Commit changes**: `git commit -m 'Add amazing feature'`
5. **Push to branch**: `git push origin feature/amazing-feature`
6. **Open Pull Request**

### Development Guidelines

- Each service should have comprehensive tests
- Follow API documentation standards
- Update relevant README files
- Ensure Docker health checks pass
- Test with both development and production configurations


## Acknowledgments

- FastAPI for the excellent async framework
- Streamlit for the intuitive web interface
- PostgreSQL and Redis for reliable data storage
- Nginx for robust load balancing
- Docker for containerization simplicity

## Support

- **Documentation**: Individual service README files
- **Issues**: [GitHub Issues](https://github.com/dineshbhusalpro/links-from-liliput/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/links-from-liliput/discussions)

---

**🏰 Welcome to Links from Liliput Kingdom!**  
*Where big URLs become small, and small links make big impacts.*

**Last Updated**: August 15, 2025