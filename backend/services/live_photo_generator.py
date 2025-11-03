# -*- coding: utf-8 -*-
"""Live Photo生成逻辑"""
import os
import uuid
import zipfile
from services.video_processor import VideoProcessor
from utils.validators import validate_time_range, validate_aspect_ratio
from utils.file_handler import cleanup_file

class LivePhotoGenerator:
    """Live Photo生成器"""
    
    def __init__(self, video_path, output_dir='uploads'):
        self.video_path = video_path
        self.output_dir = output_dir
        self.task_id = str(uuid.uuid4())
        self.processor = VideoProcessor(video_path)
        os.makedirs(output_dir, exist_ok=True)
    
    def generate(self, start_time, end_time, aspect_ratio):
        """生成Live Photo文件
        
        Args:
            start_time: 开始时间（秒）
            end_time: 结束时间（秒）
            aspect_ratio: 目标宽高比（如 '1:1', '16:9'）
        
        Returns:
            dict: 包含taskId、videoPath、imagePath的字典
        """
        # 验证参数
        duration = self.processor.get_duration()
        validate_time_range(start_time, end_time, duration)
        validate_aspect_ratio(aspect_ratio)
        
        # 创建任务输出目录
        task_dir = os.path.join(self.output_dir, self.task_id)
        os.makedirs(task_dir, exist_ok=True)
        
        try:
            # 1. 截取视频片段
            clip_path = os.path.join(task_dir, 'clip.mp4')
            self.processor.extract_clip(start_time, end_time, clip_path)
            
            # 2. 裁剪视频到目标比例并转换为MOV格式
            mov_path = os.path.join(task_dir, 'video.mov')
            self.processor.crop_video(clip_path, mov_path, aspect_ratio)
            
            # 3. 提取静态图片（时间范围的中点）
            image_timestamp = start_time + (end_time - start_time) / 2
            jpg_path = os.path.join(task_dir, 'image.jpg')
            self.processor.extract_frame(image_timestamp, jpg_path, aspect_ratio)
            
            # 4. 创建ZIP文件（可选）
            zip_path = os.path.join(task_dir, 'live_photo.zip')
            self._create_zip(mov_path, jpg_path, zip_path)
            
            # 5. 清理临时文件
            cleanup_file(clip_path)
            
            return {
                'taskId': self.task_id,
                'videoPath': mov_path,
                'imagePath': jpg_path,
                'zipPath': zip_path
            }
        
        except Exception as e:
            # 出错时清理任务目录
            from utils.file_handler import cleanup_directory
            cleanup_directory(task_dir)
            raise
    
    def _create_zip(self, mov_path, jpg_path, zip_path):
        """创建ZIP打包文件"""
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(mov_path, 'video.mov')
                zipf.write(jpg_path, 'image.jpg')
        except Exception as e:
            # ZIP创建失败不影响主要功能
            pass
