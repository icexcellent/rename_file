#!/usr/bin/env python3
"""
GitHub Actions专用构建脚本
专门解决pyparsing包缺失问题
"""

import os
import sys
import subprocess
import shutil
import json

def check_environment():
    """检查构建环境"""
    print("🔍 检查构建环境...")
    
    # 检查是否在GitHub Actions中运行
    if os.getenv('GITHUB_ACTIONS'):
        print("✓ 运行在GitHub Actions环境中")
        print(f"   Runner OS: {os.getenv('RUNNER_OS')}")
        print(f"   Python版本: {sys.version}")
    else:
        print("⚠️  不在GitHub Actions环境中运行")
    
    # 检查Python版本
    if sys.version_info >= (3, 8):
        print("✓ Python版本符合要求")
    else:
        print("✗ Python版本过低，需要3.8+")
        return False
    
    return True

def install_dependencies():
    """安装依赖包"""
    print("\n📦 安装依赖包...")
    
    # 使用GitHub Actions专用的requirements文件
    requirements_file = "requirements_github_actions.txt"
    
    if os.path.exists(requirements_file):
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_file])
            print("✓ 依赖包安装成功")
            return True
        except subprocess.CalledProcessError:
            print("✗ 依赖包安装失败")
            return False
    else:
        print(f"⚠️  {requirements_file} 文件不存在，使用默认安装")
        # 安装核心包
        packages = ['pyparsing', 'packaging', 'setuptools', 'wheel', 'pyinstaller']
        for package in packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '--upgrade'])
                print(f"   ✓ {package} 安装成功")
            except subprocess.CalledProcessError:
                print(f"   ✗ {package} 安装失败")
                return False
        return True

def clean_build():
    """清理构建文件"""
    print("\n🧹 清理构建文件...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"   ✓ 清理 {dir_name}")
            except Exception as e:
                print(f"   ⚠️  清理 {dir_name} 时出现问题: {e}")

def build_executable():
    """构建可执行文件"""
    print("\n🔨 构建可执行文件...")
    
    # 优先使用修复后的spec文件
    spec_files = ['FileRenamer_fixed.spec', 'FileRenamer.spec']
    spec_file = None
    
    for sf in spec_files:
        if os.path.exists(sf):
            spec_file = sf
            break
    
    if spec_file:
        print(f"   使用spec文件: {spec_file}")
        try:
            cmd = [sys.executable, '-m', 'PyInstaller', '--clean', spec_file]
            subprocess.check_call(cmd)
            print("   ✓ 构建成功！")
            return True
        except subprocess.CalledProcessError as e:
            print(f"   ✗ 构建失败: {e}")
            return False
    else:
        print("   ⚠️  未找到spec文件，使用命令行构建")
        try:
            # 使用命令行参数构建，包含必要的hidden imports
            cmd = [
                sys.executable, '-m', 'PyInstaller',
                '--onefile',
                '--windowed',
                '--name=FileRenamer',
                '--clean',
                '--hidden-import=pkg_resources',
                '--hidden-import=pkg_resources.extern.pyparsing',
                '--hidden-import=pkg_resources.extern.packaging',
                '--hidden-import=pyparsing',
                '--hidden-import=packaging',
                '--hidden-import=packaging.requirements',
                'file_renamer_gui.py'
            ]
            subprocess.check_call(cmd)
            print("   ✓ 命令行构建成功！")
            return True
        except subprocess.CalledProcessError as e:
            print(f"   ✗ 命令行构建失败: {e}")
            return False

def verify_build():
    """验证构建结果"""
    print("\n✅ 验证构建结果...")
    
    exe_path = os.path.join('dist', 'FileRenamer.exe')
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"   ✓ EXE文件创建成功")
        print(f"   📏 文件大小: {size_mb:.2f} MB")
        
        # 检查文件大小是否合理
        if size_mb > 500:
            print("   ⚠️  文件大小较大，可能需要优化")
        elif size_mb > 200:
            print("   ⚠️  文件大小中等")
        else:
            print("   ✓ 文件大小合理")
        
        return True
    else:
        print("   ✗ EXE文件未找到")
        return False

def create_build_info():
    """创建构建信息文件"""
    print("\n📝 创建构建信息...")
    
    build_info = {
        "build_date": os.getenv('GITHUB_SHA', 'local'),
        "python_version": sys.version,
        "platform": sys.platform,
        "github_actions": bool(os.getenv('GITHUB_ACTIONS')),
        "runner_os": os.getenv('RUNNER_OS', 'unknown'),
        "pyparsing_fixed": True,
        "spec_file_used": "FileRenamer_fixed.spec" if os.path.exists('FileRenamer_fixed.spec') else "FileRenamer.spec"
    }
    
    try:
        with open('build_info.json', 'w', encoding='utf-8') as f:
            json.dump(build_info, f, indent=2, ensure_ascii=False)
        print("   ✓ 构建信息文件创建成功")
    except Exception as e:
        print(f"   ⚠️  创建构建信息文件失败: {e}")

def main():
    print("🚀 GitHub Actions专用构建脚本")
    print("=" * 50)
    
    # 检查环境
    if not check_environment():
        print("❌ 环境检查失败，退出构建")
        return
    
    # 安装依赖
    if not install_dependencies():
        print("❌ 依赖安装失败，退出构建")
        return
    
    # 清理构建文件
    clean_build()
    
    # 构建可执行文件
    if not build_executable():
        print("❌ 构建失败")
        return
    
    # 验证构建结果
    if not verify_build():
        print("❌ 构建验证失败")
        return
    
    # 创建构建信息
    create_build_info()
    
    print("\n🎉 构建完成！")
    print("📁 可执行文件位于: dist/FileRenamer.exe")
    
    if os.getenv('GITHUB_ACTIONS'):
        print("🔗 在GitHub Actions中运行，构建产物将自动上传")

if __name__ == '__main__':
    main()
