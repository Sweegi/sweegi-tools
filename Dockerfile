FROM node:18-alpine

WORKDIR /app

# 安装必要的依赖
RUN apk add --no-cache git

# 复制package.json和package-lock.json (如果存在)
COPY package*.json ./

# 设置npm镜像为淘宝镜像，加速依赖下载
RUN npm config set registry https://registry.npmmirror.com

# 安装依赖
RUN npm install

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 5173

# 默认命令
CMD ["npm", "run", "dev"] 