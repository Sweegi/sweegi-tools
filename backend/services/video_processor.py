# -*- coding: utf-8 -*-
"""视频处理核心逻辑"""
import ffmpeg
import os

class VideoProcessor:
    """视频处理器"""
    
    def __init__(self, video_path):
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"视频文件不存在: {video_path}")
        
        self.video_path = video_path
        try:
            self.probe = ffmpeg.probe(video_path)
            self.video_info = next(
                s for s in self.probe['streams'] if s['codec_type'] == 'video'
            )
        except Exception as e:
            raise ValueError(f"无法读取视频文件信息: {str(e)}")
    
    def get_duration(self):
        """获取视频时长（秒）"""
        try:
            return float(self.probe['format']['duration'])
        except KeyError:
            raise ValueError("无法获取视频时长")
    
    def get_resolution(self):
        """获取视频分辨率"""
        return {
            'width': int(self.video_info['width']),
            'height': int(self.video_info['height'])
        }
    
    def get_frame_rate(self):
        """获取帧率"""
        try:
            frame_rate_str = self.video_info['r_frame_rate']
            num, den = map(int, frame_rate_str.split('/'))
            return num / den if den > 0 else 30.0
        except (KeyError, ValueError):
            return 30.0  # 默认帧率
    
    def extract_clip(self, start_time, end_time, output_path):
        """截取视频片段"""
        duration = end_time - start_time
        
        try:
            (
                ffmpeg
                .input(self.video_path, ss=start_time, t=duration)
                .output(
                    output_path,
                    vcodec='libx264',
                    acodec='aac',
                    preset='medium',
                    crf=23,
                    movflags='faststart'  # 优化MOV文件用于流媒体
                )
                .overwrite_output()
                .run(quiet=True, capture_stderr=True)
            )
        except ffmpeg.Error as e:
            raise RuntimeError(f"视频截取失败: {e.stderr.decode() if e.stderr else str(e)}")
    
    def crop_video(self, input_path, output_path, aspect_ratio):
        """裁剪视频到指定比例（保持中心区域）"""
        resolution = self.get_resolution()
        target_w, target_h, x, y = self._calculate_crop(
            resolution['width'],
            resolution['height'],
            aspect_ratio
        )
        
        try:
            (
                ffmpeg
                .input(input_path)
                .filter('crop', target_w, target_h, x, y)
                .output(
                    output_path,
                    vcodec='libx264',
                    acodec='aac',
                    preset='medium',
                    crf=23,
                    movflags='faststart'
                )
                .overwrite_output()
                .run(quiet=True, capture_stderr=True)
            )
        except ffmpeg.Error as e:
            raise RuntimeError(f"视频裁剪失败: {e.stderr.decode() if e.stderr else str(e)}")
    
    def extract_frame(self, timestamp, output_path, aspect_ratio=None):
        """提取视频帧为图片"""
        resolution = self.get_resolution()
        
        try:
            if aspect_ratio:
                target_w, target_h, x, y = self._calculate_crop(
                    resolution['width'],
                    resolution['height'],
                    aspect_ratio
                )
                (
                    ffmpeg
                    .input(self.video_path, ss=timestamp)
                    .filter('crop', target_w, target_h, x, y)
                    .output(output_path, vframes=1, q=2)
                    .overwrite_output()
                    .run(quiet=True, capture_stderr=True)
                )
            else:
                (
                    ffmpeg
                    .input(self.video_path, ss=timestamp)
                    .output(output_path, vframes=1, q=2)
                    .overwrite_output()
                    .run(quiet=True, capture_stderr=True)
                )
        except ffmpeg.Error as e:
            raise RuntimeError(f"图片提取失败: {e.stderr.decode() if e.stderr else str(e)}")
    
    def _calculate_crop(self, width, height, aspect_ratio):
        """计算裁剪尺寸和位置（保持中心）"""
        ratio_parts = aspect_ratio.split(':')
        if len(ratio_parts) != 2:
            raise ValueError(f"无效的宽高比格式: {aspect_ratio}")
        
        try:
            target_ratio = float(ratio_parts[0]) / float(ratio_parts[1])
        except (ValueError, ZeroDivisionError):
            raise ValueError(f"无效的宽高比值: {aspect_ratio}")
        
        current_ratio = width / height
        
        if current_ratio > target_ratio:
            # 视频更宽，需要裁剪宽度
            target_w = int(height * target_ratio)
            target_h = height
            x = (width - target_w) // 2  # 居中
            y = 0
        else:
            # 视频更高，需要裁剪高度
            target_w = width
            target_h = int(width / target_ratio)
            x = 0
            y = (height - target_h) // 2  # 居中
        
        return target_w, target_h, x, y
