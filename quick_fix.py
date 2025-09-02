#!/usr/bin/env python3
"""
快速修复pyparsing包缺失问题
"""

import subprocess
import sys
import os

def main():
    print("🔧 快速修复pyparsing包缺失问题")
    print("=" * 50)
    
    # 1. 安装必要的包
    print("\n1. 安装必要的依赖包...")
    packages = ['pyparsing', 'packaging', 'setuptools']
    
    for package in packages:
        try:
            print(f"   正在安装 {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '--upgrade'])
            print(f"   ✓ {package} 安装成功")
        except subprocess.CalledProcessError:
            print(f"   ✗ {package} 安装失败")
    
    # 2. 清理构建文件
    print("\n2. 清理构建文件...")
    for dir_name in ['build', 'dist', '__pycache__']:
        if os.path.exists(dir_name):
            try:
                import shutil
                shutil.rmtree(dir_name)
                print(f"   ✓ 清理 {dir_name}")
            except:
                print(f"   ✗ 清理 {dir_name} 失败")
    
    # 3. 重新构建
    print("\n3. 重新构建可执行文件...")
    try:
        cmd = [sys.executable, '-m', 'PyInstaller', '--clean', 'FileRenamer.spec']
        subprocess.check_call(cmd)
        print("   ✓ 构建成功！")
        print("\n🎉 修复完成！可执行文件位于 dist/ 目录中")
    except subprocess.CalledProcessError as e:
        print(f"   ✗ 构建失败: {e}")
        print("\n💡 如果仍有问题，请尝试运行: python build_fixed.py")

if __name__ == '__main__':
    main()
