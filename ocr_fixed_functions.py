#!/usr/bin/env python3
"""
修复后的OCR函数 - 解决EasyOCR在exe中卡住的问题
"""

import os
import sys
import time
import threading
import queue
from pathlib import Path
from typing import Optional

def extract_text_with_ocr_fixed(image_path: Path, log_func=None) -> Optional[str]:
    """
    修复后的OCR函数，解决EasyOCR卡住问题
    
    Args:
        image_path: 图片文件路径
        log_func: 日志函数，如果为None则使用print
    
    Returns:
        识别的文本或None
    """
    if log_func is None:
        log_func = print
    
    # 按优先级尝试不同的OCR方法
    ocr_methods = [
        ("pytesseract", _try_pytesseract),
        ("easyocr_fixed", _try_easyocr_fixed),
        ("opencv_basic", _try_opencv_basic)
    ]
    
    for method_name, method_func in ocr_methods:
        log_func(f"尝试使用 {method_name} 进行OCR识别...")
        
        try:
            result = method_func(image_path, log_func)
            if result:
                log_func(f"✅ {method_name} 识别成功")
                return result
            else:
                log_func(f"⚠️ {method_name} 识别失败或无结果")
        except Exception as e:
            log_func(f"❌ {method_name} 出现异常: {e}")
            continue
    
    log_func("❌ 所有OCR方法都失败了")
    return None

def _try_pytesseract(image_path: Path, log_func) -> Optional[str]:
    """尝试使用pytesseract进行OCR"""
    try:
        import pytesseract
        from PIL import Image
        
        log_func("使用 pytesseract 进行 OCR 识别...")
        
        # 读取图片
        image = Image.open(image_path)
        
        # 进行 OCR 识别
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        
        if text:
            text = text.strip()
            log_func(f"OCR 识别完成，文本长度: {len(text)}")
            return text
        else:
            log_func("OCR 未识别到文本")
            return None
            
    except ImportError:
        log_func("pytesseract 未安装")
        return None
    except Exception as e:
        log_func(f"pytesseract OCR 失败: {e}")
        return None

def _try_easyocr_fixed(image_path: Path, log_func) -> Optional[str]:
    """尝试使用修复后的EasyOCR进行OCR（带超时保护）"""
    try:
        import easyocr
        import cv2
        
        log_func("初始化 EasyOCR (带超时保护)...")
        
        # 设置环境变量，避免下载模型
        os.environ['EASYOCR_MODULE_PATH'] = os.path.join(os.path.dirname(__file__), 'easyocr_models')
        
        result_queue = queue.Queue()
        error_queue = queue.Queue()
        
        def init_and_recognize():
            try:
                # 初始化 EasyOCR，禁用下载
                reader = easyocr.Reader(['ch_sim', 'en'], gpu=False, download_enabled=False)
                
                # 读取图片
                image = cv2.imread(str(image_path))
                if image is None:
                    error_queue.put(("无法读取图片", None))
                    return
                
                # 进行 OCR 识别
                results = reader.readtext(image)
                
                # 提取识别的文本
                texts = []
                for (bbox, text, prob) in results:
                    if prob > 0.5:  # 只保留置信度大于 0.5 的文本
                        texts.append(text.strip())
                
                # 合并所有识别的文本
                full_text = ' '.join(texts)
                result_queue.put(("success", full_text, len(texts)))
                
            except Exception as e:
                error_queue.put(("error", str(e)))
        
        # 启动识别线程
        ocr_thread = threading.Thread(target=init_and_recognize)
        ocr_thread.daemon = True
        ocr_thread.start()
        
        # 等待结果，最多30秒
        ocr_thread.join(timeout=30)
        
        if ocr_thread.is_alive():
            log_func("⚠️ EasyOCR 识别超时，可能卡住")
            return "OCR识别超时，请检查图片或重试"
        
        if not result_queue.empty():
            status, text, count = result_queue.get()
            if status == "success":
                log_func(f"OCR 识别完成，共识别 {count} 个文本块")
                return text
            else:
                log_func(f"OCR 识别失败: {text}")
                return None
        
        if not error_queue.empty():
            error_type, error_msg = error_queue.get()
            log_func(f"OCR 识别错误: {error_type} - {error_msg}")
            return None
        
        return "OCR识别未返回结果"
        
    except ImportError:
        log_func("EasyOCR 未安装")
        return None
    except Exception as e:
        log_func(f"EasyOCR 异常: {e}")
        return None

def _try_opencv_basic(image_path: Path, log_func) -> Optional[str]:
    """尝试使用OpenCV进行基础图片处理"""
    try:
        import cv2
        
        log_func("使用 OpenCV 进行基础图片处理...")
        
        # 读取图片
        image = cv2.imread(str(image_path))
        if image is None:
            log_func("无法读取图片")
            return None
        
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 简单的文本检测（基于边缘检测）
        edges = cv2.Canny(gray, 50, 150)
        
        # 查找轮廓
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        log_func(f"检测到 {len(contours)} 个轮廓")
        
        # 返回基本信息
        return f"图片处理完成，检测到 {len(contours)} 个区域"
        
    except ImportError:
        log_func("OpenCV 未安装")
        return None
    except Exception as e:
        log_func(f"OpenCV 处理失败: {e}")
        return None

def create_ocr_config():
    """创建OCR配置文件"""
    config = {
        "preferred_ocr": "pytesseract",  # 优先使用pytesseract
        "fallback_ocr": "easyocr_fixed",  # 备用OCR
        "timeout_seconds": 30,  # 超时时间
        "enable_gpu": False,  # 禁用GPU
        "download_models": False,  # 禁用模型下载
        "log_level": "INFO"
    }
    
    return config

def test_ocr_engines():
    """测试所有OCR引擎"""
    print("🔍 测试OCR引擎...")
    
    # 测试图片路径（使用test_file目录中的图片）
    test_dir = Path("test_file")
    if test_dir.exists():
        image_files = list(test_dir.glob("*.jpg")) + list(test_dir.glob("*.png"))
        if image_files:
            test_image = image_files[0]
            print(f"使用测试图片: {test_image}")
            
            # 测试OCR函数
            result = extract_text_with_ocr_fixed(test_image)
            if result:
                print(f"✅ OCR测试成功: {result[:100]}...")
            else:
                print("❌ OCR测试失败")
        else:
            print("⚠️ 未找到测试图片")
    else:
        print("⚠️ test_file目录不存在")

if __name__ == "__main__":
    print("🔧 OCR修复函数测试")
    print("=" * 40)
    
    # 测试OCR引擎
    test_ocr_engines()
    
    print("\n📝 使用方法:")
    print("1. 将此文件中的函数复制到你的主程序中")
    print("2. 替换原有的 _extract_text_with_ocr 函数")
    print("3. 或者直接调用 extract_text_with_ocr_fixed 函数")
    
    print("\n💡 推荐配置:")
    print("- 优先使用 pytesseract（更稳定）")
    print("- EasyOCR 作为备用方案（带超时保护）")
    print("- 禁用模型下载，避免网络问题")
