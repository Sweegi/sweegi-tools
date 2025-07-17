docker:
	docker pull node:18-alpine
install:
	docker run -it --rm -v $(PWD):/app/ -w /app/ node:18-alpine npm install
dev:
	docker run -it --rm -v $(PWD):/app/ -w /app/ -p 127.0.0.1:5173:5173/tcp  --name sweegi-tools node:18-alpine npm run dev
build:
	docker run -it --rm -v $(PWD):/app/ -w /app/ node:18-alpine --name sweegi-tools-builder npm run build
	@echo "Creating zip package..."
	@DATE=$$(date +%Y%m%d); \
	cd dist && zip -r ../sweegi-tools-$$DATE.zip . && cd .. && \
	echo "Build completed! Package created: sweegi-tools-$$DATE.zip"
