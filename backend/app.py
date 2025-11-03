# -*- coding: utf-8 -*-
"""Flask应用主入口"""
from flask import Flask, jsonify
from flask_cors import CORS
from routes.video import video_bp
from config import Config
import os

def create_app():
    """创建Flask应用"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 启用CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # 注册蓝图
    app.register_blueprint(video_bp, url_prefix='/api/video')
    
    # 创建上传目录
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    
    @app.route('/')
    def index():
        return jsonify({
            'service': 'MP4 to Live Photo Converter',
            'version': '1.0.0',
            'status': 'running'
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        debug=Config.FLASK_DEBUG,
        host=Config.HOST,
        port=Config.PORT
    )
