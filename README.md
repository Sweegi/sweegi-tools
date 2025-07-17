# Markdown 查看器

一个基于 Vue 3 的现代化 Markdown 查看器，支持语法高亮、实时预览等功能。

## 功能特性

- 📖 实时 Markdown 预览
- 🎨 语法高亮支持
- 📱 响应式设计
- 🚀 支持离线使用
- 🎯 现代化 UI 界面

## 开发环境

### 本地开发
```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### Docker 开发
```bash
# 启动开发环境
docker-compose up

# 构建项目
npm run docker:build
```

## 构建部署

### 在线版本（需要服务器）
```bash
npm run build
```

### 离线版本（推荐）
```bash
npm run build:offline
```

构建完成后，可以直接打开 `dist/index.html` 文件在浏览器中使用，无需任何服务器环境。

## 离线使用说明

### 方式一：直接打开文件（推荐）
1. 运行 `npm run build:offline` 构建离线版本
2. 直接打开 `dist/index.html` 文件即可使用
3. 支持所有主流浏览器
4. 无需网络连接，完全本地运行

### 方式二：本地服务器（备选方案）
如果遇到浏览器CORS限制，可以使用内置的本地服务器：

```bash
# 先构建离线版本
npm run build:offline

# 启动本地服务器
npm run serve:offline
```

然后在浏览器中访问：http://localhost:3000

### Docker 离线构建
```bash
# 使用Docker构建离线版本
npm run docker:build:offline
```

## 常见问题

### CORS错误解决方案
如果直接打开HTML文件时遇到CORS错误，请使用以下解决方案：

1. **推荐方案**：使用内置服务器
   ```bash
   npm run serve:offline
   ```

2. **Chrome浏览器**：启动时添加参数（不推荐）
   ```bash
   chrome.exe --allow-file-access-from-files --disable-web-security
   ```

3. **Firefox浏览器**：在地址栏输入 `about:config`，搜索并设置：
   - `security.fileuri.strict_origin_policy` = false

## 技术栈

- Vue 3
- Vue Router
- Pinia
- Element Plus
- TailwindCSS
- Vite
- Markdown-it
- Highlight.js

## 许可证

MIT License