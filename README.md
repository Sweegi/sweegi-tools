# Markdown 查看器

一个简单而强大的本地 Markdown 文件查看工具，基于 Vue3、Element Plus 和 TailwindCSS 构建。

## 功能特点

- 📂 打开本地 Markdown 文件
- 📝 高性能渲染 Markdown 内容
- 🎨 美观的阅读界面
- 🔍 代码高亮显示
- 📱 响应式设计，适配各种设备
- 📋 最近文件记录功能

## 技术栈

- Vue 3
- Element Plus
- TailwindCSS
- Markdown-it
- Highlight.js
- Browser-fs-access

## 开发指南

### 安装依赖

```bash
# 使用Docker
docker-compose up

# 不使用Docker
npm install
```

### 开发运行

```bash
# 使用Docker
docker-compose up

# 不使用Docker
npm run dev
```

### 构建生产版本

```bash
# 使用Docker
docker-compose run --rm app npm run build

# 不使用Docker
npm run build
```

## Docker 支持

项目包含完整的 Docker 支持：

- `Dockerfile` - 定义构建环境
- `docker-compose.yml` - 简化容器管理
- 文件系统挂载 - 支持实时开发

### 使用 Docker 运行

```bash
docker-compose up
```

然后在浏览器中访问：http://localhost:5173 