#!/usr/bin/env python3
"""
诊断exe文件中的模块可用性
用于定位PyInstaller打包后的问题
"""

import subprocess
import sys
import os
from pathlib import Path

def test_exe_module_availability(exe_path):
    """测试exe文件中关键模块的可用性"""
    if not os.path.exists(exe_path):
        print(f"❌ EXE文件不存在: {exe_path}")
        return False
    
    print(f"🔍 诊断EXE文件: {exe_path}")
    
    # 创建诊断脚本
    diagnostic_script = '''
import sys
import traceback

def test_core_modules():
    """测试核心模块"""
    print("=== 核心模块测试 ===")
    
    # 测试基本模块
    modules_to_test = [
        'PyQt6.QtCore', 'PyQt6.QtWidgets', 'PyQt6.QtGui',
        'pytesseract', 'PIL', 'pypdf', 'docx', 'chardet',
        'requests', 'urllib3', 'logging', 'tqdm'
    ]
    
    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {module_name} - 可用")
        except ImportError as e:
            print(f"❌ {module_name} - 不可用: {e}")
        except Exception as e:
            print(f"⚠️ {module_name} - 异常: {e}")

def test_tesseract():
    """测试tesseract功能"""
    print("\\n=== Tesseract功能测试 ===")
    try:
        import pytesseract
        print(f"✅ pytesseract模块可用")
        
        # 检查tesseract可执行文件
        try:
            version = pytesseract.get_tesseract_version()
            print(f"✅ tesseract版本: {version}")
        except Exception as e:
            print(f"❌ tesseract版本检查失败: {e}")
            
    except ImportError as e:
        print(f"❌ pytesseract模块不可用: {e}")

def test_pdf_processing():
    """测试PDF处理功能"""
    print("\\n=== PDF处理功能测试 ===")
    try:
        from pypdf import PdfReader
        print(f"✅ pypdf模块可用")
    except ImportError as e:
        print(f"❌ pypdf模块不可用: {e}")
    
    try:
        import pdfplumber
        print(f"✅ pdfplumber模块可用")
    except ImportError as e:
        print(f"❌ pdfplumber模块不可用: {e}")

def test_image_processing():
    """测试图像处理功能"""
    print("\\n=== 图像处理功能测试 ===")
    try:
        from PIL import Image
        print(f"✅ PIL.Image模块可用")
    except ImportError as e:
        print(f"❌ PIL.Image模块不可用: {e}")

def test_requests():
    """测试requests功能"""
    print("\\n=== Requests功能测试 ===")
    try:
        import requests
        print(f"✅ requests模块可用，版本: {requests.__version__}")
        
        # 测试基本HTTP请求
        try:
            response = requests.get("https://httpbin.org/get", timeout=5)
            if response.status_code == 200:
                print("✅ requests HTTP请求测试成功")
            else:
                print(f"❌ requests HTTP请求失败，状态码: {response.status_code}")
        except Exception as e:
            print(f"❌ requests HTTP请求测试失败: {e}")
            
    except ImportError as e:
        print(f"❌ requests模块不可用: {e}")

def test_file_operations():
    """测试文件操作功能"""
    print("\\n=== 文件操作功能测试 ===")
    try:
        from pathlib import Path
        print(f"✅ pathlib模块可用")
    except ImportError as e:
        print(f"❌ pathlib模块不可用: {e}")
    
    try:
        import shutil
        print(f"✅ shutil模块可用")
    except ImportError as e:
        print(f"❌ shutil模块不可用: {e}")

def main():
    """主测试函数"""
    print("=== EXE模块诊断报告 ===")
    
    test_core_modules()
    test_tesseract()
    test_pdf_processing()
    test_image_processing()
    test_requests()
    test_file_operations()
    
    print("\\n=== 诊断完成 ===")

if __name__ == "__main__":
    main()
'''
    
    # 写入临时诊断脚本
    diagnostic_file = "temp_diagnostic.py"
    with open(diagnostic_file, "w", encoding="utf-8") as f:
        f.write(diagnostic_script)
    
    try:
        # 运行exe文件，执行诊断脚本
        print("🚀 在EXE环境中运行诊断...")
        result = subprocess.run(
            [exe_path, diagnostic_file],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("✅ EXE执行成功")
            print("\n📋 诊断结果:")
            print(result.stdout)
            
            # 分析结果
            if "❌" in result.stdout:
                print("\n⚠️ 发现问题！某些模块不可用")
                return False
            else:
                print("\n🎉 所有模块测试通过！")
                return True
        else:
            print(f"❌ EXE执行失败，返回码: {result.returncode}")
            print(f"错误输出: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ EXE执行超时")
        return False
    except Exception as e:
        print(f"❌ 诊断执行异常: {e}")
        return False
    finally:
        # 清理临时文件
        if os.path.exists(diagnostic_file):
            os.remove(diagnostic_file)

def main():
    """主函数"""
    print("=== EXE模块诊断工具 ===\n")
    
    # 查找exe文件
    exe_paths = [
        "dist/FileRenamer.exe",
        "FileRenamer.exe",
        "./FileRenamer.exe"
    ]
    
    exe_found = False
    for exe_path in exe_paths:
        if os.path.exists(exe_path):
            exe_found = True
            if test_exe_module_availability(exe_path):
                print("\n✅ EXE文件模块诊断完全通过！")
                print("如果仍有问题，可能是运行时路径或配置问题")
            else:
                print("\n❌ EXE文件模块诊断发现问题")
                print("需要检查PyInstaller配置和依赖包含")
            break
    
    if not exe_found:
        print("❌ 未找到FileRenamer.exe文件")
        print("请先运行PyInstaller构建，或检查exe文件路径")
        print("\n可能的路径:")
        for path in exe_paths:
            print(f"  - {path}")

if __name__ == "__main__":
    main()
