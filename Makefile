docker:
	docker pull node:20.19.4-alpine3.22
install:
	docker run -it --rm -v $(PWD):/app/ -w /app/ node:20.19.4-alpine3.22 npm install
dev:
	docker run -it --rm -v $(PWD):/app/ -w /app/ -p 127.0.0.1:5173:5173/tcp  --name sweegi-tools node:20.19.4-alpine3.22 npm run dev
env:
	docker run -it --rm -v $(PWD):/app/ -w /app/ node:20.19.4-alpine3.22 /bin/sh
build:
	docker run -it --rm -v $(PWD):/app/ -w /app/ --name sweegi-tools-builder node:20.19.4-alpine3.22 npm run build
	@echo "Creating zip package..."
	@DATE=$$(date +%Y%m%d-%H%M); \
	cd dist && zip -r ../sweegi-tools-$$DATE.zip . && cd .. && \
	echo "Build completed! Package created: sweegi-tools-$$DATE.zip"
