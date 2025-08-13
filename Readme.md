```bash
make help           # See all available commands
make quick-start    # Get started guide
make dev           # Start with debug tools
make nginx-logs    # View web traffic
make monitor       # Resource usage
make backup-db     # Database backup

# Clean any old containers
make clean

# Build with new structure
make build

# Start everything
make up

# Initialize databases
make init-db

# Test all endpoints
make test
```

## Verify Nginx is Working
```bash
# Test direct access
curl http://localhost/health
# Should return: "🏰 Links from Liliput Kingdom is healthy!"

# Test frontend through Nginx
curl -I http://localhost
# Should return HTTP/1.1 200 OK

# Test API through Nginx
curl http://localhost/api/v1/analytics/global

# Check Nginx logs
make nginx-logs
```


## Access Points After Migration:

- **🏰 Frontend**: http://localhost (via Nginx) or http://localhost:8501 (direct)
- **🚪 API**: http://localhost/api/... (via Nginx) or http://localhost:8000 (direct)  
- **🔧 Debug Tools**: `make dev` then:
  - PgAdmin: http://localhost:8080
  - Redis Commander: http://localhost:8081
  - Portainer: http://localhost:9000

## Production Deployment:
```bash
# Set production environment variables
export POSTGRES_PASSWORD=secure-prod-password
export REDIS_PASSWORD=secure-redis-password
export API_KEY=super-secret-api-key

# Deploy with SSL and production settings
make prod
```



```bash
#### DEBUGGING

# 1. Check what's actually failing
make logs-service SERVICE=url-service

# 2. Clean everything
make clean

# 3. Rebuild specific service with verbose output
docker-compose build --no-cache url-service

# 4. Check if build succeeded
docker images | grep url-service

# 5. Try starting just that service
docker-compose up url-service

```