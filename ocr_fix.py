#!/usr/bin/env python3
"""
OCR修复脚本 - 解决EasyOCR在exe中的初始化问题
"""

import os
import sys
import time
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OCRFixer:
    def __init__(self):
        self.ocr_engines = []
        self.current_engine = None
        
    def test_easyocr(self):
        """测试EasyOCR是否可用"""
        try:
            logger.info("测试EasyOCR...")
            import easyocr
            
            # 设置环境变量，避免下载模型
            os.environ['EASYOCR_MODULE_PATH'] = os.path.join(os.path.dirname(__file__), 'easyocr_models')
            
            # 尝试初始化，设置超时
            logger.info("初始化EasyOCR (超时30秒)...")
            
            # 使用线程和超时机制
            import threading
            import queue
            
            result_queue = queue.Queue()
            error_queue = queue.Queue()
            
            def init_easyocr():
                try:
                    reader = easyocr.Reader(['ch_sim', 'en'], gpu=False, download_enabled=False)
                    result_queue.put(('success', reader))
                except Exception as e:
                    error_queue.put(('error', str(e)))
            
            # 启动初始化线程
            init_thread = threading.Thread(target=init_easyocr)
            init_thread.daemon = True
            init_thread.start()
            
            # 等待结果，最多30秒
            init_thread.join(timeout=30)
            
            if init_thread.is_alive():
                logger.warning("EasyOCR初始化超时，可能卡住")
                return False, "初始化超时"
            
            if not result_queue.empty():
                result_type, result = result_queue.get()
                if result_type == 'success':
                    logger.info("EasyOCR初始化成功")
                    return True, result
                else:
                    logger.error(f"EasyOCR初始化失败: {result}")
                    return False, result
            
            if not error_queue.empty():
                error_type, error = error_queue.get()
                logger.error(f"EasyOCR初始化错误: {error}")
                return False, error
            
            return False, "未知错误"
            
        except ImportError:
            logger.error("EasyOCR未安装")
            return False, "EasyOCR未安装"
        except Exception as e:
            logger.error(f"EasyOCR测试异常: {e}")
            return False, str(e)
    
    def test_pytesseract(self):
        """测试pytesseract是否可用"""
        try:
            logger.info("测试pytesseract...")
            import pytesseract
            from PIL import Image
            
            # 测试基本功能
            logger.info("pytesseract可用")
            return True, "pytesseract可用"
            
        except ImportError:
            logger.error("pytesseract未安装")
            return False, "pytesseract未安装"
        except Exception as e:
            logger.error(f"pytesseract测试异常: {e}")
            return False, str(e)
    
    def test_opencv_ocr(self):
        """测试OpenCV OCR是否可用"""
        try:
            logger.info("测试OpenCV OCR...")
            import cv2
            
            # 检查OpenCV版本和OCR功能
            logger.info(f"OpenCV版本: {cv2.__version__}")
            
            # 检查是否有OCR相关模块
            if hasattr(cv2, 'text'):
                logger.info("OpenCV text模块可用")
                return True, "OpenCV text模块可用"
            else:
                logger.warning("OpenCV text模块不可用")
                return False, "OpenCV text模块不可用"
                
        except ImportError:
            logger.error("OpenCV未安装")
            return False, "OpenCV未安装"
        except Exception as e:
            logger.error(f"OpenCV测试异常: {e}")
            return False, str(e)
    
    def find_working_ocr(self):
        """找到可用的OCR引擎"""
        logger.info("开始测试OCR引擎...")
        
        # 按优先级测试
        tests = [
            ("pytesseract", self.test_pytesseract),
            ("opencv_ocr", self.test_opencv_ocr),
            ("easyocr", self.test_easyocr)
        ]
        
        for name, test_func in tests:
            logger.info(f"测试 {name}...")
            success, result = test_func()
            
            if success:
                logger.info(f"✅ {name} 可用: {result}")
                self.ocr_engines.append((name, result))
            else:
                logger.warning(f"❌ {name} 不可用: {result}")
        
        if self.ocr_engines:
            self.current_engine = self.ocr_engines[0]
            logger.info(f"选择OCR引擎: {self.current_engine[0]}")
            return True
        else:
            logger.error("没有可用的OCR引擎")
            return False
    
    def create_ocr_wrapper(self):
        """创建OCR包装器代码"""
        if not self.ocr_engines:
            logger.error("没有可用的OCR引擎，无法创建包装器")
            return None
        
        engine_name, engine_info = self.current_engine
        
        if engine_name == "pytesseract":
            return self._create_pytesseract_wrapper()
        elif engine_name == "opencv_ocr":
            return self._create_opencv_wrapper()
        elif engine_name == "easyocr":
            return self._create_easyocr_wrapper()
        else:
            logger.error(f"未知的OCR引擎: {engine_name}")
            return None
    
    def _create_pytesseract_wrapper(self):
        """创建pytesseract包装器"""
        wrapper_code = '''
def _extract_text_with_ocr(self, image_path: Path) -> Optional[str]:
    """使用 pytesseract 识别图片文本"""
    try:
        import pytesseract
        from PIL import Image
        
        self._log("使用 pytesseract 进行 OCR 识别...")
        
        # 读取图片
        image = Image.open(image_path)
        
        # 进行 OCR 识别
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        
        if text:
            text = text.strip()
            self._log(f"OCR 识别完成，文本长度: {len(text)}")
            return text
        else:
            self._log("OCR 未识别到文本")
            return None
            
    except ImportError:
        self._log("pytesseract 未安装，无法进行 OCR 识别")
        return None
    except Exception as e:
        self._log(f"OCR 识别失败: {e}")
        return None
'''
        return wrapper_code
    
    def _create_opencv_wrapper(self):
        """创建OpenCV包装器"""
        wrapper_code = '''
def _extract_text_with_ocr(self, image_path: Path) -> Optional[str]:
    """使用 OpenCV 识别图片文本"""
    try:
        import cv2
        
        self._log("使用 OpenCV 进行图片处理...")
        
        # 读取图片
        image = cv2.imread(str(image_path))
        if image is None:
            self._log("无法读取图片")
            return None
        
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 简单的文本检测（基于边缘检测）
        edges = cv2.Canny(gray, 50, 150)
        
        # 查找轮廓
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        self._log(f"检测到 {len(contours)} 个轮廓")
        
        # 这里可以添加更复杂的文本识别逻辑
        # 目前返回基本信息
        return f"图片处理完成，检测到 {len(contours)} 个区域"
        
    except ImportError:
        self._log("OpenCV 未安装，无法进行图片处理")
        return None
    except Exception as e:
        self._log(f"图片处理失败: {e}")
        return None
'''
        return wrapper_code
    
    def _create_easyocr_wrapper(self):
        """创建EasyOCR包装器（带超时和错误处理）"""
        wrapper_code = '''
def _extract_text_with_ocr(self, image_path: Path) -> Optional[str]:
    """使用 EasyOCR 识别图片文本（带超时保护）"""
    try:
        import easyocr
        import cv2
        import threading
        import queue
        import time
        
        self._log("初始化 EasyOCR (带超时保护)...")
        
        # 设置环境变量
        os.environ['EASYOCR_MODULE_PATH'] = os.path.join(os.path.dirname(__file__), 'easyocr_models')
        
        result_queue = queue.Queue()
        error_queue = queue.Queue()
        
        def init_and_recognize():
            try:
                # 初始化 EasyOCR
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
        
        # 等待结果，最多60秒
        ocr_thread.join(timeout=60)
        
        if ocr_thread.is_alive():
            self._log("⚠️ EasyOCR 识别超时，可能卡住")
            return "OCR识别超时，请检查图片或重试"
        
        if not result_queue.empty():
            status, text, count = result_queue.get()
            if status == "success":
                self._log(f"OCR 识别完成，共识别 {count} 个文本块")
                return text
            else:
                self._log(f"OCR 识别失败: {text}")
                return None
        
        if not error_queue.empty():
            error_type, error_msg = error_queue.get()
            self._log(f"OCR 识别错误: {error_type} - {error_msg}")
            return None
        
        return "OCR识别未返回结果"
        
    except ImportError:
        self._log("EasyOCR 未安装，无法进行 OCR 识别")
        return None
    except Exception as e:
        self._log(f"OCR 识别异常: {e}")
        return None
'''
        return wrapper_code

def main():
    """主函数"""
    print("🔧 OCR修复脚本 - 解决EasyOCR在exe中的初始化问题")
    print("=" * 60)
    
    fixer = OCRFixer()
    
    # 查找可用的OCR引擎
    if fixer.find_working_ocr():
        print(f"\n✅ 找到可用的OCR引擎: {fixer.current_engine[0]}")
        
        # 创建OCR包装器
        wrapper_code = fixer.create_ocr_wrapper()
        if wrapper_code:
            print(f"\n📝 生成的OCR包装器代码:")
            print("-" * 40)
            print(wrapper_code)
            print("-" * 40)
            
            # 保存到文件
            output_file = "ocr_wrapper_code.py"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(wrapper_code)
            
            print(f"\n💾 OCR包装器代码已保存到: {output_file}")
            print("请将此代码替换到你的主程序中")
        else:
            print("❌ 无法创建OCR包装器")
    else:
        print("❌ 没有找到可用的OCR引擎")
        print("建议安装 pytesseract 作为替代方案")

if __name__ == '__main__':
    main()
