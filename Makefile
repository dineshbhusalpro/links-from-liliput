# Colors for output
RED=\033[0;31m
GREEN=\033[0;32m
YELLOW=\033[1;33m
BLUE=\033[0;34m
PURPLE=\033[0;35m
CYAN=\033[0;36m
NC=\033[0m # No Color

help: ## Show available commands for Links from Liliput
	@echo "$(CYAN)🏰 Links from Liliput - Available Commands:$(NC)"
	@echo "================================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

build: ## Build all Liliput services
	@echo "$(BLUE)🏗️ Building the magical kingdom...$(NC)"
	docker-compose build --parallel
	@echo "$(GREEN)✅ Kingdom built successfully!$(NC)"

up: ## Start the Liliput kingdom
	@echo "$(BLUE)🏰 Starting Links from Liliput...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✅ Kingdom is now running!$(NC)"
	@echo "$(CYAN)🌐 Access points:$(NC)"
	@echo "  Frontend: http://localhost:8501"
	@echo "  API:      http://localhost:8000"
	@echo "  Full App: http://localhost"

down: ## Stop all services
	@echo "$(YELLOW)🌙 Putting the kingdom to sleep...$(NC)"
	docker-compose down
	@echo "$(GREEN)✅ Kingdom is now sleeping$(NC)"

logs: ## Show logs for all services
	@echo "$(BLUE)📜 Viewing kingdom chronicles...$(NC)"
	docker-compose logs -f

logs-service: ## Show logs for specific service (usage: make logs-service SERVICE=frontend)
	@echo "$(BLUE)📜 Viewing logs for $(SERVICE)...$(NC)"
	docker-compose logs -f $(SERVICE)

restart: ## Restart all services
	@echo "$(YELLOW)🔄 Restarting the magical realm...$(NC)"
	docker-compose restart
	@echo "$(GREEN)✅ Kingdom restarted!$(NC)"

restart-service: ## Restart specific service (usage: make restart-service SERVICE=frontend)
	@echo "$(YELLOW)🔄 Restarting $(SERVICE)...$(NC)"
	docker-compose restart $(SERVICE)
	@echo "$(GREEN)✅ $(SERVICE) restarted!$(NC)"

clean: ## Clean up everything
	@echo "$(RED)🧹 Cleaning up the kingdom...$(NC)"
	docker-compose down -v --remove-orphans
	docker system prune -af --volumes
	@echo "$(GREEN)✅ Kingdom cleaned!$(NC)"

init-db: ## Initialize the royal databases
	@echo "$(BLUE)📚 Initializing the royal libraries...$(NC)"
	docker-compose exec url-service alembic upgrade head
	docker-compose exec analytics-service alembic upgrade head
	@echo "$(GREEN)✅ Royal libraries initialized!$(NC)"

migrate: ## Run database migrations
	@echo "$(PURPLE)🔮 Casting database transformation spells...$(NC)"
	docker-compose exec url-service alembic revision --autogenerate -m "Kingdom migration"
	docker-compose exec url-service alembic upgrade head
	docker-compose exec analytics-service alembic revision --autogenerate -m "Analytics migration"
	docker-compose exec analytics-service alembic upgrade head
	@echo "$(GREEN)✅ Database spells cast successfully!$(NC)"

test: ## Run health checks across the kingdom
	@echo "$(BLUE)🏥 Checking the health of the realm...$(NC)"
	@echo "Testing API Gateway..."
	@curl -f http://localhost:8000/health/all >/dev/null 2>&1 && echo "$(GREEN)✅ API Gateway healthy$(NC)" || echo "$(RED)❌ API Gateway needs attention$(NC)"
	@echo "Testing Frontend Palace..."
	@curl -f http://localhost:8501/_stcore/health >/dev/null 2>&1 && echo "$(GREEN)✅ Frontend Palace healthy$(NC)" || echo "$(RED)❌ Frontend Palace needs attention$(NC)"
	@echo "Testing Nginx Gateway..."
	@curl -f http://localhost/health >/dev/null 2>&1 && echo "$(GREEN)✅ Nginx Gateway healthy$(NC)" || echo "$(RED)❌ Nginx Gateway needs attention$(NC)"
	@echo "$(GREEN)🎉 Health check complete!$(NC)"

dev: ## Start with magical debugging tools
	@echo "$(PURPLE)🔧 Starting kingdom with wizard's tools...$(NC)"
	docker-compose --profile debug up -d
	@echo "$(GREEN)✅ Kingdom started with debug tools!$(NC)"
	@echo "$(CYAN)🔧 Debug tools available:$(NC)"
	@echo "  PgAdmin:          http://localhost:8080"
	@echo "  Redis Commander:  http://localhost:8081"
	@echo "  Portainer:        http://localhost:9000"

prod: ## Deploy to the production realm
	@echo "$(PURPLE)🚀 Deploying to the production kingdom...$(NC)"
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
	@echo "$(GREEN)✅ Production kingdom deployed!$(NC)"

status: ## Check status of all services
	@echo "$(CYAN)👑 Kingdom Status Report:$(NC)"
	@echo "========================"
	@docker-compose ps

shell: ## Access service shell (usage: make shell SERVICE=frontend)
	@echo "$(BLUE)🐚 Entering $(SERVICE) shell...$(NC)"
	@docker-compose exec $(SERVICE) bash || docker-compose exec $(SERVICE) sh

db-shell: ## Access PostgreSQL shell
	@echo "$(BLUE)🗄️ Entering royal database...$(NC)"
	docker-compose exec postgres psql -U username -d url_shortener_db

redis-shell: ## Access Redis shell
	@echo "$(BLUE)⚡ Entering Redis cache...$(NC)"
	docker-compose exec redis redis-cli

nginx-logs: ## View Nginx access logs
	@echo "$(BLUE)📊 Viewing Nginx traffic logs...$(NC)"
	docker-compose exec nginx tail -f /var/log/nginx/access.log

nginx-reload: ## Reload Nginx configuration
	@echo "$(YELLOW)🔄 Reloading Nginx configuration...$(NC)"
	docker-compose exec nginx nginx -s reload
	@echo "$(GREEN)✅ Nginx configuration reloaded!$(NC)"

backup-db: ## Backup the database
	@echo "$(BLUE)💾 Creating database backup...$(NC)"
	mkdir -p backups
	docker-compose exec postgres pg_dump -U username url_shortener_db > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)✅ Database backup created!$(NC)"

quick-start: ## Quick start guide
	@echo "$(CYAN)🚀 Quick Start Guide for Links from Liliput:$(NC)"
	@echo "=============================================="
	@echo "$(YELLOW)1.$(NC) make build     - Build the kingdom"
	@echo "$(YELLOW)2.$(NC) make up        - Start all services"
	@echo "$(YELLOW)3.$(NC) make init-db   - Initialize databases"
	@echo "$(YELLOW)4.$(NC) make test      - Verify everything works"
	@echo ""
	@echo "$(CYAN)🌐 Access your kingdom:$(NC)"
	@echo "  $(GREEN)Frontend:$(NC) http://localhost:8501"
	@echo "  $(GREEN)API:$(NC)      http://localhost:8000"
	@echo "  $(GREEN)Full App:$(NC) http://localhost"
	@echo ""
	@echo "$(CYAN)🔧 Development commands:$(NC)"
	@echo "  $(GREEN)make dev$(NC)          - Start with debug tools"
	@echo "  $(GREEN)make logs$(NC)         - View all logs"
	@echo "  $(GREEN)make status$(NC)       - Check service status"

# File watching for development
watch-logs: ## Watch logs with automatic refresh
	@echo "$(BLUE)👁️ Watching kingdom activity...$(NC)"
	watch -n 2 'docker-compose logs --tail=20'

# Performance monitoring
monitor: ## Show system resource usage
	@echo "$(CYAN)📊 Kingdom Resource Monitor:$(NC)"
	@echo "=============================="
	@docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

# Migration helper
migrate-create: ## Create new migration (usage: make migrate-create SERVICE=url-service MSG="your message")
	@echo "$(PURPLE)🔮 Creating new migration for $(SERVICE)...$(NC)"
	docker-compose exec $(SERVICE) alembic revision --autogenerate -m "$(MSG)"
	@echo "$(GREEN)✅ Migration created!$(NC)"