#!/usr/bin/env python3
"""
优化的PyInstaller打包脚本
用于减少打包后的程序大小
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def clean_build_dirs():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已清理目录: {dir_name}")

def build_optimized():
    """执行优化的打包"""
    cmd = [
        'pyinstaller',
        '--onefile',                    # 单文件模式
        '--windowed',                   # 无控制台窗口
        '--name=FileRenamer',           # 程序名称
        '--clean',                      # 清理临时文件
        '--optimize=2',                 # Python优化级别
        '--strip',                      # 去除调试信息
        '--upx-dir=/usr/local/bin',    # UPX压缩器路径（macOS）
        
        # 排除不必要的模块
        '--exclude-module=matplotlib',
        '--exclude-module=numpy',
        '--exclude-module=pandas',
        '--exclude-module=scipy',
        '--exclude-module=sklearn',
        '--exclude-module=tensorflow',
        '--exclude-module=torch',
        '--exclude-module=jax',
        '--exclude-module=onnxruntime',
        '--exclude-module=cv2',
        '--exclude-module=opencv',
        '--exclude-module=rapidocr',
        '--exclude-module=tkinter',
        '--exclude-module=wx',
        '--exclude-module=kivy',
        '--exclude-module=IPython',
        '--exclude-module=jupyter',
        '--exclude-module=notebook',
        '--exclude-module=sphinx',
        '--exclude-module=docutils',
        '--exclude-module=pytest',
        '--exclude-module=unittest',
        '--exclude-module=email',
        '--exclude-module=http',
        '--exclude-module=urllib3',
        '--exclude-module=requests',
        '--exclude-module=sqlite3',
        '--exclude-module=xml',
        '--exclude-module=html',
        '--exclude-module=xmlrpc',
        '--exclude-module=multiprocessing',
        '--exclude-module=concurrent',
        '--exclude-module=asyncio',
        '--exclude-module=logging',
        '--exclude-module=argparse',
        '--exclude-module=getopt',
        '--exclude-module=doctest',
        '--exclude-module=pdb',
        '--exclude-module=profile',
        '--exclude-module=cProfile',
        
        # 只包含必要的隐藏导入
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtWidgets',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=pytesseract',
        '--hidden-import=pypdf',
        '--hidden-import=docx',
        '--hidden-import=chardet',
        '--hidden-import=PIL',
        '--hidden-import=PIL.Image',
        
        'file_renamer_gui.py'
    ]
    
    print("开始执行优化的打包...")
    print(f"命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("打包成功完成!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"打包失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def check_file_size():
    """检查生成文件的大小"""
    exe_path = Path('dist/FileRenamer')
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"生成文件大小: {size_mb:.2f} MB")
        return size_mb
    return 0

def main():
    """主函数"""
    print("=== 文件重命名器优化打包脚本 ===")
    
    # 清理构建目录
    clean_build_dirs()
    
    # 执行打包
    if build_optimized():
        # 检查文件大小
        size = check_file_size()
        print(f"\n打包完成! 文件大小: {size:.2f} MB")
        
        if size < 100:
            print("✅ 优化成功! 文件大小显著减少")
        elif size < 200:
            print("⚠️  文件大小有所减少，但仍有优化空间")
        else:
            print("❌ 文件大小仍然较大，可能需要进一步优化")
    else:
        print("打包失败，请检查错误信息")

if __name__ == "__main__":
    main()
