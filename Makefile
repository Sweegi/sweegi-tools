.PHONY: help dev dev-backend dev-front stop stop-backend stop-front

FRONT_DIR := front
BACKEND_DIR := backend
FRONT_PORT ?= 5174
BACKEND_PORT ?= 5001
FRONT_CONTAINER := sweegi-tools
BACKEND_CONTAINER := sweegi-tools-backend-dev
NODE_IMAGE := node:22.20.0-alpine3.22

help:
	@echo "Available commands:"
	@echo "  make dev           - Start frontend and backend dev servers (Docker)"
	@echo "  make dev-front     - Start frontend only"
	@echo "  make dev-backend   - Start backend only"
	@echo "  make stop          - Stop frontend and backend containers"
	@echo "  make stop-front    - Stop frontend container"
	@echo "  make stop-backend  - Stop backend container"
	@echo ""
	@echo "Ports:"
	@echo "  Frontend: http://localhost:$(FRONT_PORT)"
	@echo "  Backend:  http://localhost:$(BACKEND_PORT)"

dev: dev-backend dev-front
	@echo ""
	@echo "Development servers are running:"
	@echo "  Frontend: http://localhost:$(FRONT_PORT)"
	@echo "  Backend:  http://localhost:$(BACKEND_PORT)"

dev-backend:
	@echo "Starting backend..."
	@$(MAKE) -C $(BACKEND_DIR) run PORT=$(BACKEND_PORT)
	@if docker exec $(BACKEND_CONTAINER) pgrep -f "python app.py" >/dev/null 2>&1; then \
		echo "Backend Flask process already running"; \
	else \
		docker exec -d $(BACKEND_CONTAINER) python app.py; \
		echo "Backend Flask process started"; \
	fi

dev-front:
	@echo "Starting frontend..."
	@if ! docker image inspect $(NODE_IMAGE) >/dev/null 2>&1; then \
		echo "Pulling frontend base image..."; \
		docker pull $(NODE_IMAGE); \
	fi
	@if [ ! -d $(FRONT_DIR)/node_modules ]; then \
		echo "Installing frontend dependencies..."; \
		docker run --rm -v $(CURDIR)/$(FRONT_DIR):/app/ -w /app/ $(NODE_IMAGE) npm install --legacy-peer-deps; \
	fi
	@if docker ps --format '{{.Names}}' | grep -qx '$(FRONT_CONTAINER)'; then \
		echo "Frontend container already running"; \
	else \
		docker rm -f $(FRONT_CONTAINER) >/dev/null 2>&1 || true; \
		docker run -d \
			-v $(CURDIR)/$(FRONT_DIR):/app/ \
			-w /app/ \
			-p 127.0.0.1:$(FRONT_PORT):$(FRONT_PORT)/tcp \
			--name $(FRONT_CONTAINER) \
			$(NODE_IMAGE) npm run dev; \
		echo "Frontend container started"; \
	fi

stop: stop-front stop-backend

stop-front:
	@echo "Stopping frontend..."
	@docker rm -f $(FRONT_CONTAINER) >/dev/null 2>&1 || echo "Frontend container not running"

stop-backend:
	@echo "Stopping backend..."
	@$(MAKE) -C $(BACKEND_DIR) stop
