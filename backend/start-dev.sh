#!/bin/bash
# 开发环境启动脚本

set -e

echo "================================"
echo "启动开发环境"
echo "================================"

# 检查FFmpeg是否可用
if ! command -v ffmpeg &> /dev/null; then
    echo "错误: FFmpeg未安装或不可用"
    exit 1
fi

echo "FFmpeg版本:"
ffmpeg -version | head -n 1

# 检查Python版本
echo ""
echo "Python版本:"
python --version

# 检查依赖是否安装
echo ""
echo "检查Python依赖..."
if ! python -c "import flask" 2>/dev/null; then
    echo "安装Python依赖..."
    pip install --no-cache-dir -r requirements.txt
fi

# 创建必要目录
mkdir -p uploads
mkdir -p logs

# 设置环境变量
export FLASK_ENV=development
export FLASK_DEBUG=True
export UPLOAD_FOLDER=uploads
export MAX_FILE_SIZE=104857600
export HOST=0.0.0.0
export PORT=5001

echo ""
echo "================================"
echo "启动Flask应用..."
echo "================================"
echo "服务将在 http://0.0.0.0:5001 上运行"
echo "（如果在Docker容器中，实际映射端口请查看Makefile配置）"
echo "按 Ctrl+C 停止服务"
echo ""

# 启动Flask应用
python app.py
