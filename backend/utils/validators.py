# -*- coding: utf-8 -*-
"""参数验证工具"""

def validate_time_range(start_time, end_time, duration):
    """验证时间范围"""
    if start_time < 0:
        raise ValueError("开始时间不能小于0")
    if end_time > duration:
        raise ValueError("结束时间不能超过视频时长")
    if start_time >= end_time:
        raise ValueError("开始时间必须小于结束时间")
    
    clip_duration = end_time - start_time
    if clip_duration < 3:
        raise ValueError("Live Photo时长至少需要3秒")
    if clip_duration > 15:
        raise ValueError("Live Photo时长不能超过15秒")
    
    return True

def validate_aspect_ratio(aspect_ratio):
    """验证宽高比格式"""
    if not aspect_ratio or ':' not in aspect_ratio:
        raise ValueError("宽高比格式不正确，应为 '宽:高' 格式，如 '1:1'")
    
    try:
        parts = aspect_ratio.split(':')
        if len(parts) != 2:
            raise ValueError("宽高比格式不正确")
        width = float(parts[0])
        height = float(parts[1])
        
        if width <= 0 or height <= 0:
            raise ValueError("宽高比数值必须大于0")
        
        return True
    except ValueError as e:
        raise ValueError(f"宽高比格式错误: {str(e)}")

def validate_file_size(file_size, max_size):
    """验证文件大小"""
    if file_size > max_size:
        raise ValueError(f"文件大小超过限制（最大 {max_size / 1024 / 1024}MB）")
    return True
