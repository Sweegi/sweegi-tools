# Sweegi Tools

一个基于 Vue 3 的多功能工具集，包含 Markdown 查看器、HTML 转 PDF 等实用功能。

## 功能特性

- 📖 实时 Markdown 预览和编辑
- 📄 HTML 转 PDF 功能，支持多页分页
- 🎨 语法高亮支持
- 📱 响应式设计
- 🚀 支持离线使用
- 🎯 现代化 UI 界面
- 🔧 多种 DPI 质量选择
- 🖼️ Canvas 预览功能

## 开发环境

### 方式一：本地开发
```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 方式二：Docker 开发 (推荐)
```bash
# 拉取 Docker 镜像
make docker

# 安装依赖
make install

# 启动开发服务器
make dev
```

开发服务器将在 http://localhost:5173 上运行。

## 构建部署

### 方式一：本地构建
```bash
# 构建生产版本
npm run build
```

### 方式二：Docker 构建 (推荐)
```bash
# 使用 Docker 构建
make build
```

构建完成后会生成：
- `dist/` 目录包含所有构建文件
- `sweegi-tools-YYYYMMDD.zip` 压缩包（按日期命名）

构建的应用可以直接部署到任何静态文件服务器。

## 使用说明

### 部署后访问
1. 使用 `make build` 构建项目
2. 将生成的 `dist/` 目录部署到 Web 服务器
3. 或者解压 `sweegi-tools-YYYYMMDD.zip` 到服务器目录
4. 通过浏览器访问即可使用

### 主要功能
- **Markdown 查看器**: 支持实时预览和语法高亮
- **HTML 转 PDF**: 支持多种 DPI 质量选择和自动分页
- **文件管理**: 支持本地文件选择和预览

### Docker 快速开始
```bash
# 完整的开发流程
make docker     # 拉取镜像
make install    # 安装依赖  
make dev        # 启动开发服务器

# 生产构建
make build      # 构建并生成压缩包
```

## 可用的 Make 命令

```bash
make docker      # 拉取 node:18-alpine Docker 镜像
make install     # 使用 Docker 安装 npm 依赖
make dev         # 启动开发服务器 (localhost:5173)
make build       # 构建生产版本并生成日期命名的 zip 包
```

## 常见问题

### 端口被占用
如果 5173 端口被占用，Docker 开发命令会自动失败。请先停止占用该端口的进程。


### 构建文件位置
- 构建输出：`dist/` 目录
- 压缩包：`sweegi-tools-YYYYMMDD.zip`（项目根目录）

## 技术栈

- **前端框架**: Vue 3 + Vue Router
- **状态管理**: Pinia
- **UI 组件**: Element Plus
- **样式框架**: TailwindCSS
- **构建工具**: Vite
- **Markdown 解析**: Markdown-it
- **代码高亮**: Highlight.js
- **PDF 生成**: jsPDF + html2canvas
- **文件处理**: browser-fs-access
- **容器化**: Docker (node:18-alpine)

## 许可证

MIT License