# -*- coding: utf-8 -*-
"""视频处理路由"""
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from services.live_photo_generator import LivePhotoGenerator
from utils.file_handler import allowed_file, save_uploaded_file, cleanup_file
from utils.validators import validate_file_size
from config import Config
import os

video_bp = Blueprint('video', __name__)

@video_bp.route('/convert-to-live-photo', methods=['POST'])
def convert_to_live_photo():
    """转换视频为Live Photo"""
    try:
        # 检查文件是否存在
        if 'video' not in request.files:
            return jsonify({
                'success': False,
                'error': {'code': 'NO_FILE', 'message': '未上传文件'}
            }), 400
        
        file = request.files['video']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': {'code': 'NO_FILE', 'message': '未选择文件'}
            }), 400
        
        # 验证文件格式
        if not allowed_file(file.filename, Config.ALLOWED_EXTENSIONS):
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INVALID_FILE',
                    'message': f'不支持的文件格式，支持格式: {", ".join(Config.ALLOWED_EXTENSIONS)}'
                }
            }), 400
        
        # 验证文件大小
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        try:
            validate_file_size(file_size, Config.MAX_FILE_SIZE)
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': {'code': 'FILE_TOO_LARGE', 'message': str(e)}
            }), 400
        
        # 获取请求参数
        try:
            start_time = float(request.form.get('startTime', 0))
            end_time = float(request.form.get('endTime', 0))
            aspect_ratio = request.form.get('aspectRatio', '1:1')
        except ValueError:
            return jsonify({
                'success': False,
                'error': {'code': 'INVALID_PARAMS', 'message': '参数格式错误'}
            }), 400
        
        # 保存上传文件
        upload_path = save_uploaded_file(file, Config.UPLOAD_FOLDER)
        
        try:
            # 生成Live Photo
            generator = LivePhotoGenerator(upload_path, Config.UPLOAD_FOLDER)
            result = generator.generate(start_time, end_time, aspect_ratio)
            
            # 清理上传的原始文件
            cleanup_file(upload_path)
            
            return jsonify({
                'success': True,
                'data': {
                    'taskId': result['taskId'],
                    'videoUrl': f'/api/video/download/video/{result["taskId"]}',
                    'imageUrl': f'/api/video/download/image/{result["taskId"]}',
                    'zipUrl': f'/api/video/download/zip/{result["taskId"]}'
                },
                'message': '转换成功'
            })
        
        except Exception as e:
            # 清理上传文件
            cleanup_file(upload_path)
            raise
    
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': {'code': 'INVALID_PARAMS', 'message': str(e)}
        }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {'code': 'PROCESSING_ERROR', 'message': str(e)}
        }), 500

@video_bp.route('/status/<task_id>', methods=['GET'])
def get_status(task_id):
    """查询处理状态"""
    task_dir = os.path.join(Config.UPLOAD_FOLDER, task_id)
    video_path = os.path.join(task_dir, 'video.mov')
    image_path = os.path.join(task_dir, 'image.jpg')
    
    if os.path.exists(video_path) and os.path.exists(image_path):
        return jsonify({
            'success': True,
            'status': 'completed',
            'taskId': task_id
        })
    elif os.path.exists(task_dir):
        return jsonify({
            'success': True,
            'status': 'processing',
            'taskId': task_id
        })
    else:
        return jsonify({
            'success': False,
            'status': 'not_found',
            'taskId': task_id
        }), 404

@video_bp.route('/download/video/<task_id>', methods=['GET'])
def download_video(task_id):
    """下载MOV视频文件"""
    video_path = os.path.join(Config.UPLOAD_FOLDER, task_id, 'video.mov')
    if os.path.exists(video_path):
        return send_file(
            video_path,
            as_attachment=True,
            download_name=f'live_photo_{task_id}.mov',
            mimetype='video/quicktime'
        )
    return jsonify({'error': '文件不存在'}), 404

@video_bp.route('/download/image/<task_id>', methods=['GET'])
def download_image(task_id):
    """下载JPEG图片文件"""
    image_path = os.path.join(Config.UPLOAD_FOLDER, task_id, 'image.jpg')
    if os.path.exists(image_path):
        return send_file(
            image_path,
            as_attachment=True,
            download_name=f'live_photo_{task_id}.jpg',
            mimetype='image/jpeg'
        )
    return jsonify({'error': '文件不存在'}), 404

@video_bp.route('/download/zip/<task_id>', methods=['GET'])
def download_zip(task_id):
    """下载ZIP打包文件"""
    zip_path = os.path.join(Config.UPLOAD_FOLDER, task_id, 'live_photo.zip')
    if os.path.exists(zip_path):
        return send_file(
            zip_path,
            as_attachment=True,
            download_name=f'live_photo_{task_id}.zip',
            mimetype='application/zip'
        )
    return jsonify({'error': '文件不存在'}), 404

@video_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'service': 'video-to-live-photo'
    })
