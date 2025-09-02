#!/usr/bin/env python3
"""
详细的exe诊断脚本
用于检查exe文件中的具体错误信息和模块状态
"""

import subprocess
import sys
import os
from pathlib import Path

def test_exe_detailed(exe_path):
    """详细测试exe文件"""
    if not os.path.exists(exe_path):
        print(f"❌ EXE文件不存在: {exe_path}")
        return False
    
    print(f"🔍 详细诊断EXE文件: {exe_path}")
    
    # 创建详细诊断脚本
    detailed_diagnostic_script = '''
import sys
import traceback
import os

def test_basic_imports():
    """测试基本导入"""
    print("=== 基本导入测试 ===")
    
    try:
        import sys
        print(f"✅ sys模块可用")
    except Exception as e:
        print(f"❌ sys模块不可用: {e}")
    
    try:
        import os
        print(f"✅ os模块可用")
    except Exception as e:
        print(f"❌ os模块不可用: {e}")

def test_setuptools_dependencies():
    """测试setuptools相关依赖"""
    print("\\n=== setuptools依赖测试 ===")
    
    # 测试pyparsing
    try:
        import pyparsing
        print(f"✅ pyparsing模块可用")
    except ImportError as e:
        print(f"❌ pyparsing模块不可用: {e}")
    except Exception as e:
        print(f"⚠️ pyparsing模块异常: {e}")
    
    # 测试packaging
    try:
        import packaging
        print(f"✅ packaging模块可用")
    except ImportError as e:
        print(f"❌ packaging模块不可用: {e}")
    except Exception as e:
        print(f"⚠️ packaging模块异常: {e}")
    
    # 测试pkg_resources
    try:
        import pkg_resources
        print(f"✅ pkg_resources模块可用")
    except ImportError as e:
        print(f"❌ pkg_resources模块不可用: {e}")
    except Exception as e:
        print(f"⚠️ pkg_resources模块异常: {e}")

def test_ocr_dependencies():
    """测试OCR相关依赖"""
    print("\\n=== OCR依赖测试 ===")
    
    # 测试PIL
    try:
        from PIL import Image
        print(f"✅ PIL.Image模块可用")
    except ImportError as e:
        print(f"❌ PIL.Image模块不可用: {e}")
    except Exception as e:
        print(f"⚠️ PIL.Image模块异常: {e}")
    
    # 测试pytesseract
    try:
        import pytesseract
        print(f"✅ pytesseract模块可用")
    except ImportError as e:
        print(f"❌ pytesseract模块不可用: {e}")
    except Exception as e:
        print(f"⚠️ pytesseract模块异常: {e}")
    
    # 测试EasyOCR
    try:
        import easyocr
        print(f"✅ easyocr模块可用")
    except ImportError as e:
        print(f"❌ easyocr模块不可用: {e}")
    except Exception as e:
        print(f"⚠️ easyocr模块异常: {e}")

def test_pdf_dependencies():
    """测试PDF相关依赖"""
    print("\\n=== PDF依赖测试 ===")
    
    # 测试pypdf
    try:
        from pypdf import PdfReader
        print(f"✅ pypdf模块可用")
    except ImportError as e:
        print(f"❌ pypdf模块不可用: {e}")
    except Exception as e:
        print(f"⚠️ pypdf模块异常: {e}")
    
    # 测试PyMuPDF
    try:
        import fitz
        print(f"✅ PyMuPDF (fitz)模块可用")
    except ImportError as e:
        print(f"❌ PyMuPDF (fitz)模块不可用: {e}")
    except Exception as e:
        print(f"⚠️ PyMuPDF (fitz)模块异常: {e}")

def test_network_dependencies():
    """测试网络相关依赖"""
    print("\\n=== 网络依赖测试 ===")
    
    # 测试requests
    try:
        import requests
        print(f"✅ requests模块可用")
    except ImportError as e:
        print(f"❌ requests模块不可用: {e}")
    except Exception as e:
        print(f"⚠️ requests模块异常: {e}")
    
    # 测试urllib3
    try:
        import urllib3
        print(f"✅ urllib3模块可用")
    except ImportError as e:
        print(f"❌ urllib3模块不可用: {e}")
    except Exception as e:
        print(f"⚠️ urllib3模块异常: {e}")

def test_gui_dependencies():
    """测试GUI相关依赖"""
    print("\\n=== GUI依赖测试 ===")
    
    # 测试PyQt6
    try:
        from PyQt6.QtCore import QCoreApplication
        print(f"✅ PyQt6.QtCore模块可用")
    except ImportError as e:
        print(f"❌ PyQt6.QtCore模块不可用: {e}")
    except Exception as e:
        print(f"⚠️ PyQt6.QtCore模块异常: {e}")

def test_system_info():
    """测试系统信息"""
    print("\\n=== 系统信息 ===")
    
    try:
        print(f"✅ Python版本: {sys.version}")
        print(f"✅ 系统平台: {sys.platform}")
        print(f"✅ 可执行文件: {sys.executable}")
        print(f"✅ 当前工作目录: {os.getcwd()}")
        
        # 测试环境变量
        path_env = os.environ.get('PATH', '')
        print(f"✅ PATH环境变量长度: {len(path_env)}")
        
    except Exception as e:
        print(f"❌ 系统信息获取失败: {e}")

def main():
    """主测试函数"""
    print("=== EXE详细诊断报告 ===")
    
    test_basic_imports()
    test_setuptools_dependencies()
    test_ocr_dependencies()
    test_pdf_dependencies()
    test_network_dependencies()
    test_gui_dependencies()
    test_system_info()
    
    print("\\n=== 详细诊断完成 ===")

if __name__ == "__main__":
    main()
'''
    
    # 写入临时详细诊断脚本
    detailed_diagnostic_file = "temp_detailed_diagnostic.py"
    with open(detailed_diagnostic_file, "w", encoding="utf-8") as f:
        f.write(detailed_diagnostic_script)
    
    try:
        # 运行exe文件，执行详细诊断脚本
        print("🚀 在EXE环境中运行详细诊断...")
        result = subprocess.run(
            [exe_path, detailed_diagnostic_file],
            capture_output=True,
            text=True,
            timeout=180
        )
        
        if result.returncode == 0:
            print("✅ EXE执行成功")
            print("\n📋 详细诊断结果:")
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
        print(f"❌ 详细诊断执行异常: {e}")
        return False
    finally:
        # 清理临时文件
        if os.path.exists(detailed_diagnostic_file):
            os.remove(detailed_diagnostic_file)

def main():
    """主函数"""
    print("=== EXE详细诊断工具 ===\n")
    
    # 查找exe文件
    exe_paths = [
        "FileRenamer.exe",
        "./FileRenamer.exe",
        "dist/FileRenamer.exe"
    ]
    
    exe_found = False
    for exe_path in exe_paths:
        if os.path.exists(exe_path):
            exe_found = True
            if test_exe_detailed(exe_path):
                print("\n✅ EXE详细诊断完全通过！")
                print("如果仍有问题，可能是运行时配置问题")
            else:
                print("\n❌ EXE详细诊断发现问题")
                print("需要进一步检查PyInstaller配置")
            break
    
    if not exe_found:
        print("❌ 未找到FileRenamer.exe文件")
        print("请先下载新构建的exe文件，或检查文件路径")

if __name__ == "__main__":
    main()
