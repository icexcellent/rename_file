#!/usr/bin/env python3
"""
Windows构建问题诊断脚本
用于本地测试和诊断PyInstaller构建问题
"""

import sys
import os
import subprocess
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    print(f"Python版本: {sys.version}")
    if sys.version_info < (3, 8):
        print("❌ Python版本过低，需要3.8+")
        return False
    print("✅ Python版本检查通过")
    return True

def check_dependencies():
    """检查依赖包"""
    required_packages = [
        'PyQt6', 'pytesseract', 'pypdf', 'docx', 'chardet', 'tqdm'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            print(f"❌ {package} 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n缺少的包: {', '.join(missing_packages)}")
        return False
    
    print("✅ 所有依赖包检查通过")
    return True

def check_pyinstaller():
    """检查PyInstaller"""
    try:
        import PyInstaller
        print(f"✅ PyInstaller 已安装，版本: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("❌ PyInstaller 未安装")
        return False

def test_basic_build():
    """测试基本构建"""
    print("\n🔨 测试基本构建...")
    
    # 清理之前的构建
    for path in ['build', 'dist', 'FileRenamer.spec']:
        if os.path.exists(path):
            if os.path.isdir(path):
                import shutil
                shutil.rmtree(path)
            else:
                os.remove(path)
    
    try:
        # 基本构建命令
        cmd = [
            'pyinstaller',
            '--onefile',
            '--windowed',
            '--name=FileRenamer',
            'file_renamer_gui.py'
        ]
        
        print(f"执行命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ 基本构建成功!")
            
            # 检查生成的文件
            exe_path = Path('dist/FileRenamer.exe')
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"生成文件大小: {size_mb:.2f} MB")
                return True
            else:
                print("❌ 构建成功但未找到exe文件")
                return False
        else:
            print(f"❌ 构建失败，返回码: {result.returncode}")
            print(f"错误输出: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ 构建超时")
        return False
    except Exception as e:
        print(f"❌ 构建异常: {e}")
        return False

def test_optimized_build():
    """测试优化构建"""
    print("\n🚀 测试优化构建...")
    
    # 清理之前的构建
    for path in ['build', 'dist', 'FileRenamer.spec']:
        if os.path.exists(path):
            if os.path.isdir(path):
                import shutil
                shutil.rmtree(path)
            else:
                os.remove(path)
    
    try:
        # 优化构建命令
        cmd = [
            'pyinstaller',
            '--onefile',
            '--windowed',
            '--name=FileRenamer',
            '--clean',
            '--optimize=2',
            '--exclude-module=numpy',
            '--exclude-module=pandas',
            '--exclude-module=matplotlib',
            '--exclude-module=scipy',
            '--exclude-module=sklearn',
            '--exclude-module=tensorflow',
            '--exclude-module=torch',
            '--exclude-module=cv2',
            '--exclude-module=opencv',
            '--exclude-module=rapidocr',
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
        
        print(f"执行命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print("✅ 优化构建成功!")
            
            # 检查生成的文件
            exe_path = Path('dist/FileRenamer.exe')
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"生成文件大小: {size_mb:.2f} MB")
                return True
            else:
                print("❌ 构建成功但未找到exe文件")
                return False
        else:
            print(f"❌ 优化构建失败，返回码: {result.returncode}")
            print(f"错误输出: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ 构建超时")
        return False
    except Exception as e:
        print(f"❌ 构建异常: {e}")
        return False

def main():
    """主函数"""
    print("=== Windows构建问题诊断 ===\n")
    
    # 检查环境
    if not check_python_version():
        return
    
    if not check_dependencies():
        print("\n请先安装缺失的依赖包:")
        print("pip install -r requirements_gui.txt")
        return
    
    if not check_pyinstaller():
        print("\n请先安装PyInstaller:")
        print("pip install pyinstaller")
        return
    
    # 测试构建
    print("\n" + "="*50)
    
    if test_basic_build():
        print("\n✅ 基本构建测试通过")
        
        print("\n" + "="*50)
        if test_optimized_build():
            print("\n✅ 优化构建测试通过")
        else:
            print("\n⚠️ 优化构建失败，但基本构建可用")
    else:
        print("\n❌ 基本构建失败，需要检查代码或环境问题")
    
    print("\n" + "="*50)
    print("诊断完成!")

if __name__ == "__main__":
    main()
