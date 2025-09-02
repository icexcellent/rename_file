#!/usr/bin/env python3
"""
智能OCR依赖安装脚本 - 避免编译问题
"""

import subprocess
import sys
import os
import platform

def run_command(cmd, description):
    """运行命令并处理结果"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(f"✅ {description} 成功")
            return True
        else:
            print(f"❌ {description} 失败: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} 超时")
        return False
    except Exception as e:
        print(f"💥 {description} 异常: {e}")
        return False

def install_basic_dependencies():
    """安装基础依赖"""
    print("📦 安装基础依赖...")
    
    basic_packages = [
        "pillow",  # PIL图像处理
        "opencv-python",  # OpenCV
        "requests",  # HTTP请求
        "urllib3"  # HTTP客户端
    ]
    
    for package in basic_packages:
        if not run_command(f"{sys.executable} -m pip install {package}", f"安装 {package}"):
            print(f"⚠️ {package} 安装失败，继续安装其他包")

def install_ocr_engines():
    """安装OCR引擎"""
    print("\n🔍 安装OCR引擎...")
    
    # 1. 尝试安装pytesseract（推荐）
    print("1. 安装 pytesseract...")
    if run_command(f"{sys.executable} -m pip install pytesseract", "安装 pytesseract"):
        print("✅ pytesseract 安装成功")
    else:
        print("❌ pytesseract 安装失败")
    
    # 2. 尝试安装EasyOCR（备用）
    print("\n2. 安装 EasyOCR...")
    if run_command(f"{sys.executable} -m pip install easyocr", "安装 EasyOCR"):
        print("✅ EasyOCR 安装成功")
    else:
        print("❌ EasyOCR 安装失败")
    
    # 3. 尝试安装预编译的tesseract（Windows）
    if platform.system() == "Windows":
        print("\n3. 尝试安装预编译的tesseract...")
        # 尝试不同的预编译版本
        tesseract_packages = [
            "tesseract-ocr-windows",
            "tesseract-ocr-win64",
            "tesseract-ocr"
        ]
        
        tesseract_installed = False
        for package in tesseract_packages:
            if run_command(f"{sys.executable} -m pip install {package}", f"安装 {package}"):
                print(f"✅ {package} 安装成功")
                tesseract_installed = True
                break
            else:
                print(f"❌ {package} 安装失败，尝试下一个")
        
        if not tesseract_installed:
            print("⚠️ 所有tesseract包安装失败，将使用系统级tesseract")
    
    # 4. 安装其他必要的包
    print("\n4. 安装其他必要包...")
    other_packages = [
        "numpy",  # 数值计算
        "scikit-image",  # 图像处理
        "imageio"  # 图像IO
    ]
    
    for package in other_packages:
        if not run_command(f"{sys.executable} -m pip install {package}", f"安装 {package}"):
            print(f"⚠️ {package} 安装失败，继续安装其他包")

def test_ocr_installation():
    """测试OCR安装"""
    print("\n🧪 测试OCR安装...")
    
    # 测试pytesseract
    try:
        import pytesseract
        print("✅ pytesseract 导入成功")
    except ImportError:
        print("❌ pytesseract 导入失败")
    
    # 测试PIL
    try:
        from PIL import Image
        print("✅ PIL 导入成功")
    except ImportError:
        print("❌ PIL 导入失败")
    
    # 测试OpenCV
    try:
        import cv2
        print(f"✅ OpenCV 导入成功，版本: {cv2.__version__}")
    except ImportError:
        print("❌ OpenCV 导入失败")
    
    # 测试EasyOCR
    try:
        import easyocr
        print("✅ EasyOCR 导入成功")
    except ImportError:
        print("❌ EasyOCR 导入失败")

def create_requirements_file():
    """创建requirements文件"""
    print("\n📝 创建requirements文件...")
    
    requirements = """# OCR依赖文件 - 自动生成
# 基础依赖
pillow>=10.0.0
opencv-python>=4.8.0
requests>=2.31.0
urllib3>=2.0.0

# OCR引擎
pytesseract>=0.3.10
easyocr>=1.7.0

# 图像处理
numpy>=1.24.0
scikit-image>=0.21.0
imageio>=2.31.0

# 其他必要包
pyparsing>=3.0.0
packaging>=23.0
setuptools>=65.0.0
"""
    
    try:
        with open("requirements_ocr.txt", "w", encoding="utf-8") as f:
            f.write(requirements)
        print("✅ requirements_ocr.txt 创建成功")
    except Exception as e:
        print(f"❌ 创建requirements文件失败: {e}")

def main():
    """主函数"""
    print("🚀 智能OCR依赖安装脚本")
    print("=" * 50)
    print(f"Python版本: {sys.version}")
    print(f"平台: {platform.system()} {platform.release()}")
    print(f"架构: {platform.machine()}")
    print("=" * 50)
    
    # 升级pip
    print("🔄 升级pip...")
    run_command(f"{sys.executable} -m pip install --upgrade pip", "升级pip")
    
    # 安装依赖
    install_basic_dependencies()
    install_ocr_engines()
    
    # 测试安装
    test_ocr_installation()
    
    # 创建requirements文件
    create_requirements_file()
    
    print("\n🎉 安装完成！")
    print("\n📋 下一步操作:")
    print("1. 如果使用Windows，请安装系统级tesseract:")
    print("   - 下载: https://github.com/UB-Mannheim/tesseract/wiki")
    print("   - 安装到默认路径: C:\\Program Files\\Tesseract-OCR")
    print("2. 使用 requirements_ocr.txt 安装依赖:")
    print("   pip install -r requirements_ocr.txt")
    print("3. 测试OCR功能:")
    print("   python ocr_fixed_functions.py")

if __name__ == "__main__":
    main()
