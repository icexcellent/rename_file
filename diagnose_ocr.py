#!/usr/bin/env python3
"""
OCR功能诊断脚本
用于检查exe中的OCR相关模块和功能
"""

import subprocess
import sys
import os
from pathlib import Path

def test_exe_ocr(exe_path):
    """测试exe文件中的OCR功能"""
    if not os.path.exists(exe_path):
        print(f"❌ EXE文件不存在: {exe_path}")
        return False
    
    print(f"🔍 诊断EXE文件OCR功能: {exe_path}")
    
    # 创建OCR诊断脚本
    ocr_diagnostic_script = '''
import sys
import traceback
import os
from pathlib import Path

def test_ocr_modules():
    """测试OCR相关模块"""
    print("=== OCR模块测试 ===")
    
    # 测试基本图像处理模块
    try:
        from PIL import Image
        print(f"✅ PIL.Image模块可用")
        
        # 测试图像打开功能
        try:
            # 创建一个简单的测试图像
            test_img = Image.new('RGB', (100, 100), color='white')
            print(f"✅ PIL图像创建成功")
        except Exception as e:
            print(f"❌ PIL图像创建失败: {e}")
            
    except ImportError as e:
        print(f"❌ PIL.Image模块不可用: {e}")
        return False
    
    # 测试pytesseract模块
    try:
        import pytesseract
        print(f"✅ pytesseract模块可用")
        
        # 测试tesseract版本
        try:
            version = pytesseract.get_tesseract_version()
            print(f"✅ tesseract版本: {version}")
        except Exception as e:
            print(f"❌ tesseract版本检查失败: {e}")
            
        # 测试tesseract可执行文件路径
        try:
            tesseract_cmd = pytesseract.pytesseract.tesseract_cmd
            print(f"✅ tesseract命令路径: {tesseract_cmd}")
            
            # 检查文件是否存在
            if os.path.exists(tesseract_cmd):
                print(f"✅ tesseract可执行文件存在")
            else:
                print(f"❌ tesseract可执行文件不存在: {tesseract_cmd}")
                
        except Exception as e:
            print(f"❌ tesseract命令路径检查失败: {e}")
            
    except ImportError as e:
        print(f"❌ pytesseract模块不可用: {e}")
        return False
    
    return True

def test_ocr_functionality():
    """测试OCR功能"""
    print("\\n=== OCR功能测试 ===")
    
    try:
        import pytesseract
        from PIL import Image
        
        # 创建一个包含文字的测试图像
        test_img = Image.new('RGB', (200, 50), color='white')
        
        # 尝试OCR识别
        try:
            text = pytesseract.image_to_string(test_img, lang='eng')
            print(f"✅ OCR识别成功，结果长度: {len(text)}")
            print(f"OCR结果: '{text.strip()}'")
        except Exception as e:
            print(f"❌ OCR识别失败: {e}")
            traceback.print_exc()
            
    except Exception as e:
        print(f"❌ OCR功能测试异常: {e}")
        traceback.print_exc()

def test_image_processing():
    """测试图像处理功能"""
    print("\\n=== 图像处理功能测试 ===")
    
    try:
        from PIL import Image
        
        # 测试图像格式支持
        formats = Image.OPEN.keys()
        print(f"✅ 支持的图像格式: {list(formats)[:10]}...")
        
        # 测试图像操作
        test_img = Image.new('RGB', (100, 100), color='red')
        print(f"✅ 图像创建和操作成功")
        
    except Exception as e:
        print(f"❌ 图像处理测试失败: {e}")
        traceback.print_exc()

def test_file_operations():
    """测试文件操作功能"""
    print("\\n=== 文件操作功能测试 ===")
    
    try:
        # 测试当前工作目录
        cwd = os.getcwd()
        print(f"✅ 当前工作目录: {cwd}")
        
        # 测试文件列表
        files = os.listdir('.')
        print(f"✅ 当前目录文件数量: {len(files)}")
        
        # 测试路径操作
        from pathlib import Path
        current_path = Path('.')
        print(f"✅ 路径操作正常")
        
    except Exception as e:
        print(f"❌ 文件操作测试失败: {e}")
        traceback.print_exc()

def test_system_info():
    """测试系统信息"""
    print("\\n=== 系统信息 ===")
    
    try:
        print(f"✅ Python版本: {sys.version}")
        print(f"✅ 系统平台: {sys.platform}")
        print(f"✅ 可执行文件: {sys.executable}")
        
        # 测试环境变量
        path_env = os.environ.get('PATH', '')
        print(f"✅ PATH环境变量长度: {len(path_env)}")
        
    except Exception as e:
        print(f"❌ 系统信息获取失败: {e}")

def main():
    """主测试函数"""
    print("=== EXE OCR功能诊断报告 ===")
    
    # 测试OCR模块
    ocr_ok = test_ocr_modules()
    
    if ocr_ok:
        # 测试OCR功能
        test_ocr_functionality()
    else:
        print("\\n⚠️ OCR模块不可用，跳过功能测试")
    
    # 测试其他功能
    test_image_processing()
    test_file_operations()
    test_system_info()
    
    print("\\n=== OCR诊断完成 ===")

if __name__ == "__main__":
    main()
'''
    
    # 写入临时OCR诊断脚本
    ocr_diagnostic_file = "temp_ocr_diagnostic.py"
    with open(ocr_diagnostic_file, "w", encoding="utf-8") as f:
        f.write(ocr_diagnostic_script)
    
    try:
        # 运行exe文件，执行OCR诊断脚本
        print("🚀 在EXE环境中运行OCR诊断...")
        result = subprocess.run(
            [exe_path, ocr_diagnostic_file],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print("✅ EXE执行成功")
            print("\n📋 OCR诊断结果:")
            print(result.stdout)
            
            # 分析结果
            if "❌" in result.stdout:
                print("\n⚠️ 发现OCR问题！")
                return False
            else:
                print("\n🎉 OCR功能测试通过！")
                return True
        else:
            print(f"❌ EXE执行失败，返回码: {result.returncode}")
            print(f"错误输出: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ EXE执行超时")
        return False
    except Exception as e:
        print(f"❌ OCR诊断执行异常: {e}")
        return False
    finally:
        # 清理临时文件
        if os.path.exists(ocr_diagnostic_file):
            os.remove(ocr_diagnostic_file)

def main():
    """主函数"""
    print("=== EXE OCR功能诊断工具 ===\n")
    
    # 查找exe文件
    exe_paths = [
        "FileRenamer",
        "./FileRenamer",
        "dist/FileRenamer"
    ]
    
    exe_found = False
    for exe_path in exe_paths:
        if os.path.exists(exe_path):
            exe_found = True
            if test_exe_ocr(exe_path):
                print("\n✅ EXE OCR功能诊断完全通过！")
                print("如果仍有问题，可能是运行时配置问题")
            else:
                print("\n❌ EXE OCR功能诊断发现问题")
                print("需要检查PyInstaller配置和OCR依赖")
            break
    
    if not exe_found:
        print("❌ 未找到FileRenamer文件")
        print("请先运行PyInstaller构建，或检查文件路径")

if __name__ == "__main__":
    main()
