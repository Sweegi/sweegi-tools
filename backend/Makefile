.PHONY: help dev build run clean docker-build docker-run docker-stop shell

# Docker镜像名称
IMAGE_NAME = sweegi-tools-backend
CONTAINER_NAME = sweegi-tools-backend-dev

# 端口配置（默认5001，映射容器内的5000端口）
PORT ?= 5001

help:
	@echo "可用命令:"
	@echo "  make dev        - 构建并启动开发环境容器"
	@echo "  make build      - 构建Docker镜像"
	@echo "  make run        - 运行开发容器（默认端口5001）"
	@echo "  make stop       - 停止开发容器"
	@echo "  make clean      - 清理容器和镜像"
	@echo "  make shell      - 进入开发容器shell"
	@echo "  make logs       - 查看容器日志"
	@echo ""
	@echo "端口配置:"
	@echo "  默认端口: 5001（主机端口，容器内为5000）"
	@echo "  自定义端口: make run PORT=5002"
	@echo "  使用5000端口: make run PORT=5000（需先释放5000端口）"

dev: build run

build:
	@echo "构建Docker镜像..."
	docker build -t $(IMAGE_NAME):latest .
	@echo "镜像构建完成"

run:
	@echo "启动开发容器（端口: $(PORT):5000）..."
	@docker ps -a | grep $(CONTAINER_NAME) > /dev/null && \
		echo "容器已存在，正在启动..." && \
		docker start $(CONTAINER_NAME) || \
		docker run -d \
			--name $(CONTAINER_NAME) \
			-p $(PORT):5000 \
			-v $$(pwd):/app \
			-v $$(pwd)/uploads:/app/uploads \
			-e FLASK_ENV=development \
			-e FLASK_DEBUG=True \
			-e UPLOAD_FOLDER=uploads \
			-e MAX_FILE_SIZE=104857600 \
			-e PORT=5000 \
			-e HOST=0.0.0.0 \
			$(IMAGE_NAME):latest \
			tail -f /dev/null
	@echo "容器已启动，使用以下命令进入容器:"
	@echo "  docker exec -it $(CONTAINER_NAME) /bin/bash"
	@echo "服务将在 http://localhost:$(PORT) 上运行"

stop:
	@echo "停止开发容器..."
	docker stop $(CONTAINER_NAME) 2>/dev/null || echo "容器未运行"
	@echo "容器已停止"

clean: stop
	@echo "清理容器和镜像..."
	docker rm $(CONTAINER_NAME) 2>/dev/null || echo "容器不存在"
	docker rmi $(IMAGE_NAME):latest 2>/dev/null || echo "镜像不存在"
	@echo "清理完成"

shell:
	@echo "进入开发容器..."
	docker exec -it $(CONTAINER_NAME) /bin/bash

logs:
	docker logs -f $(CONTAINER_NAME)
