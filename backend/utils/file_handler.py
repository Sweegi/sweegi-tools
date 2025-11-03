# -*- coding: utf-8 -*-
"""文件处理工具"""
import os
import shutil
from werkzeug.utils import secure_filename

def allowed_file(filename, allowed_extensions):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_uploaded_file(file, upload_folder):
    """保存上传的文件"""
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    return file_path

def cleanup_file(file_path):
    """清理单个文件"""
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except OSError:
            pass

def cleanup_directory(dir_path):
    """清理整个目录"""
    if os.path.exists(dir_path):
        try:
            shutil.rmtree(dir_path)
        except OSError:
            pass
