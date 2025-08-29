#!/usr/bin/env python3
"""
打包脚本：将PyQt6应用打包成可执行文件
"""

import os
import sys
import subprocess
from pathlib import Path

def build_app():
    """构建应用"""
    print("开始构建文件重命名应用...")
    
    # 检查PyInstaller是否安装
    try:
        import PyInstaller
        print(f"PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("错误: 未安装PyInstaller")
        print("请先运行: pip install pyinstaller")
        return False
    
    # 检查PyQt6是否安装
    try:
        import PyQt6
        print("PyQt6已安装")
    except ImportError:
        print("错误: 未安装PyQt6")
        print("请先运行: pip install PyQt6")
        return False
    
    # 构建命令
    build_cmd = [
        "pyinstaller",
        "--onefile",                    # 打包成单个文件
        "--windowed",                   # 无控制台窗口（Windows）
        "--noconsole",                  # 无控制台窗口（macOS/Linux）
        "--name=FileRenamer",           # 可执行文件名
        "--icon=icon.ico",              # 图标文件（如果有的话）
        "--add-data=requirements.txt;.", # 包含依赖文件
        "--hidden-import=PIL._tkinter_finder",  # 包含PIL相关模块
        "--hidden-import=pytesseract",
        "--hidden-import=pypdf",
        "--hidden-import=docx",
        "--hidden-import=chardet",
        "file_renamer_gui.py"           # 主程序文件
    ]
    
    # 移除不存在的参数
    if not Path("icon.ico").exists():
        build_cmd.remove("--icon=icon.ico")
    
    print(f"执行构建命令: {' '.join(build_cmd)}")
    
    try:
        # 执行构建
        result = subprocess.run(build_cmd, check=True, capture_output=True, text=True)
        print("构建成功！")
        print("输出文件位置: dist/FileRenamer")
        
        # 显示构建输出
        if result.stdout:
            print("构建输出:")
            print(result.stdout)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        if e.stderr:
            print("错误输出:")
            print(e.stderr)
        return False

def build_simple():
    """简化构建（适用于大多数情况）"""
    print("使用简化构建...")
    
    build_cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=FileRenamer",
        "file_renamer_gui.py"
    ]
    
    print(f"执行命令: {' '.join(build_cmd)}")
    
    try:
        result = subprocess.run(build_cmd, check=True)
        print("构建成功！")
        print("可执行文件位置: dist/FileRenamer")
        return True
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("文件重命名应用打包工具")
    print("=" * 50)
    
    # 检查当前目录
    if not Path("file_renamer_gui.py").exists():
        print("错误: 未找到 file_renamer_gui.py 文件")
        print("请确保在正确的目录中运行此脚本")
        return
    
    # 尝试完整构建
    if not build_app():
        print("\n完整构建失败，尝试简化构建...")
        if not build_simple():
            print("所有构建方式都失败了")
            return
    
    print("\n" + "=" * 50)
    print("构建完成！")
    print("可执行文件位于: dist/ 目录")
    print("=" * 50)

if __name__ == "__main__":
    main()
