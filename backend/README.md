# MP4转Live Photo后端服务

Python Flask后端服务，用于将MP4视频转换为iPhone Live Photo格式。

## 功能特性

- 视频截取（时间范围选择）
- 视频裁剪（比例调整）
- Live Photo生成（MOV + JPEG配对）
- ZIP打包下载

## 环境要求

- Python 3.12.2
- FFmpeg
- Docker（用于开发环境）

## 快速开始

### 使用Docker开发环境（推荐）

1. **构建并启动开发环境**
```bash
make dev
```

2. **进入容器**
```bash
make shell
# 或
docker exec -it sweegi-tools-backend-dev /bin/bash
```

3. **在容器内启动服务**
```bash
./start-dev.sh
```

服务将在 `http://localhost:5001` 上运行（容器内端口5000映射到主机端口5001）。

### 本地开发（不使用Docker）

1. **安装系统依赖**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y ffmpeg python3-pip

# macOS
brew install ffmpeg
```

2. **安装Python依赖**
```bash
pip install -r requirements.txt
```

3. **启动服务**
```bash
./start-dev.sh
```

## 项目结构

```
backend/
├── app.py                    # Flask应用主入口
├── config.py                 # 配置文件
├── requirements.txt          # Python依赖
├── Dockerfile                # Docker镜像定义
├── Makefile                  # 开发命令
├── start-dev.sh              # 开发启动脚本
├── routes/
│   └── video.py             # 视频处理路由
├── services/
│   ├── video_processor.py   # 视频处理核心逻辑
│   └── live_photo_generator.py  # Live Photo生成逻辑
├── utils/
│   ├── file_handler.py      # 文件处理工具
│   └── validators.py        # 参数验证工具
└── uploads/                 # 上传文件临时目录
```

## API端点

### POST /api/video/convert-to-live-photo

转换视频为Live Photo

**请求参数：**
- `video`: 视频文件（multipart/form-data）
- `startTime`: 开始时间（秒，float）
- `endTime`: 结束时间（秒，float）
- `aspectRatio`: 目标比例（如 "1:1", "16:9"）

**响应：**
```json
{
  "success": true,
  "data": {
    "taskId": "uuid-string",
    "videoUrl": "/api/video/download/video/{id}",
    "imageUrl": "/api/video/download/image/{id}",
    "zipUrl": "/api/video/download/zip/{id}"
  },
  "message": "转换成功"
}
```

### GET /api/video/status/{taskId}

查询处理状态

### GET /api/video/download/video/{taskId}

下载MOV视频文件

### GET /api/video/download/image/{taskId}

下载JPEG图片文件

### GET /api/video/download/zip/{taskId}

下载ZIP打包文件

## Makefile命令

- `make dev` - 构建并启动开发环境
- `make build` - 构建Docker镜像
- `make run` - 运行开发容器
- `make stop` - 停止开发容器
- `make clean` - 清理容器和镜像
- `make shell` - 进入容器shell
- `make logs` - 查看容器日志

## 配置

配置文件：`config.py`

环境变量（可选，创建`.env`文件）：
- `FLASK_ENV`: 运行环境（development/production）
- `FLASK_DEBUG`: 调试模式（True/False）
- `HOST`: 服务主机（默认：0.0.0.0）
- `PORT`: 服务端口（默认：5001，容器内为5000）
- `UPLOAD_FOLDER`: 上传文件目录（默认：uploads）
- `MAX_FILE_SIZE`: 最大文件大小（字节，默认：100MB）

## 注意事项

1. **FFmpeg必需**：确保系统已正确安装FFmpeg
2. **文件大小限制**：默认最大支持100MB视频文件
3. **时长限制**：Live Photo建议时长3-15秒
4. **格式支持**：主要支持MP4、MOV、AVI、MKV、WEBM格式
5. **内存使用**：处理大文件时可能占用较多内存

## 故障排查

### FFmpeg未找到

确保FFmpeg已正确安装：
```bash
ffmpeg -version
```

在Docker容器中，FFmpeg已包含在镜像中。

### 权限问题

确保uploads目录有写权限：
```bash
chmod 755 uploads
```

### 端口被占用

如果5001端口也被占用，可以修改端口：
```bash
make run PORT=5002
```

或修改`config.py`中的默认端口，以及`.env.example`中的配置。

## 开发

### 代码风格

遵循PEP 8 Python代码规范。

### 测试

待添加测试用例。

## 许可证

MIT License
