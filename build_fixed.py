#!/usr/bin/env python3
"""
修复pyparsing包缺失问题的构建脚本
"""

import os
import sys
import subprocess
import shutil

def install_dependencies():
    """安装必要的依赖包"""
    print("正在安装必要的依赖包...")
    
    # 安装pyparsing和packaging
    packages = [
        'pyparsing',
        'packaging',
        'setuptools',
        'wheel'
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ {package} 安装成功")
        except subprocess.CalledProcessError:
            print(f"✗ {package} 安装失败")
            return False
    
    return True

def clean_build():
    """清理之前的构建文件"""
    print("正在清理构建文件...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ 清理 {dir_name}")

def build_executable():
    """构建可执行文件"""
    print("正在构建可执行文件...")
    
    try:
        # 使用修复后的spec文件构建
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            'FileRenamer_fixed.spec'
        ]
        
        subprocess.check_call(cmd)
        print("✓ 构建成功！")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ 构建失败: {e}")
        return False

def main():
    print("=== 修复pyparsing包缺失问题的构建脚本 ===")
    print()
    
    # 检查PyInstaller是否安装
    try:
        import PyInstaller
        print("✓ PyInstaller 已安装")
    except ImportError:
        print("✗ PyInstaller 未安装，正在安装...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PyInstaller'])
    
    # 安装依赖
    if not install_dependencies():
        print("依赖安装失败，退出构建")
        return
    
    # 清理构建文件
    clean_build()
    
    # 构建可执行文件
    if build_executable():
        print("\n🎉 构建完成！")
        print("可执行文件位于 dist/ 目录中")
    else:
        print("\n❌ 构建失败，请检查错误信息")

if __name__ == '__main__':
    main()
