# Nginx Load Balancer & Reverse Proxy

Nginx serves as the entry point for Links from Liliput, providing load balancing, reverse proxy, and SSL termination. It routes traffic between the Streamlit frontend and API Gateway while ensuring high performance and security.

## Architecture

```
Internet Users (Port 80/443)
        ↓
    Nginx Reverse Proxy
        ↓
┌─────────┴─────────┐
│                   │
Streamlit Frontend  API Gateway
(Port 8501)         (Port 8000)
```

## Project Structure

```
nginx/
├── nginx.conf          # Main configuration file
├── ssl/               # SSL certificates (production)
├── logs/              # Log files (Docker volume)
├── html/              # Error pages
└── Dockerfile
```

## Configuration

### Main Configuration (`nginx.conf`)

```nginx
events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    # Upstream definitions
    upstream api_gateway {
        least_conn;
        server api-gateway:8000 max_fails=3 fail_timeout=30s;
    }

    upstream frontend {
        least_conn;
        server frontend:8501 max_fails=3 fail_timeout=30s;
    }

    # Rate limiting zones
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=frontend:10m rate=30r/s;
    limit_req_zone $binary_remote_addr zone=redirect:10m rate=50r/s;

    server {
        listen 80;
        server_name localhost _;

        # Health check
        location = /health {
            return 200 "🏰 Links from Liliput Kingdom is healthy!\n";
        }

        # Frontend (Streamlit)
        location / {
            limit_req zone=frontend burst=50 nodelay;
            proxy_pass http://frontend;
            # WebSocket support
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }

        # API routes
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://api_gateway;
        }

        # Short URL redirects
        location ~ ^/[a-zA-Z0-9_-]+$ {
            limit_req zone=redirect burst=100 nodelay;
            proxy_pass http://api_gateway;
        }
    }
}
```

### Key Features

**Rate Limiting:**
- API: 10 requests/second (burst 20)
- Frontend: 30 requests/second (burst 50)
- Redirects: 50 requests/second (burst 100)

**Routing Priority:**
1. `/health` - Nginx health check
2. `/api/` - API Gateway routes
3. `/[code]` - Short URL redirects
4. `/` - Streamlit frontend

**Performance:**
- WebSocket support for Streamlit
- Gzip compression
- Static file caching
- Fast redirect timeouts

## Deployment

### Docker

```yaml
# docker-compose.yml
nginx:
  build: ./nginx
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - ./nginx/logs:/var/log/nginx
    - ./nginx/ssl:/etc/nginx/ssl:ro
  depends_on:
    - api-gateway
    - frontend
```

### Local Testing

```bash
# Test configuration
nginx -t

# Health check
curl http://localhost/health
# Response: 🏰 Links from Liliput Kingdom is healthy!

# Status monitoring
curl http://localhost/nginx-status
```

## Security

**Headers:**
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block
- Referrer-Policy: strict-origin-when-cross-origin

**Access Control:**
- Hidden files blocked (`.` files)
- Config files blocked (`.bak`, `.config`, etc.)
- Server tokens disabled

## Monitoring

```bash
# Service health
curl http://localhost/health

# Backend health
curl http://localhost/health/all

# Access logs
tail -f nginx/logs/access.log

# Error logs
tail -f nginx/logs/error.log
```

## SSL Setup (Production)

```bash
# Generate certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/key.pem \
  -out nginx/ssl/cert.pem

# Add SSL server block to nginx.conf
server {
    listen 443 ssl http2;
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    # ... same location blocks
}
```

## Troubleshooting

```bash
# Check upstream health
docker-compose ps

# Test direct access
curl http://localhost:8000/health  # API Gateway
curl http://localhost:8501/        # Frontend

# Configuration test
nginx -t

# Reload configuration
nginx -s reload
```

---

**Service**: Load Balancer & Reverse Proxy  
**Port**: 80 (HTTP), 443 (HTTPS)  
**Dependencies**: API Gateway, Frontend