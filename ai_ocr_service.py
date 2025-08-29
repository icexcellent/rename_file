#!/usr/bin/env python3
"""
AI OCR服务模块
集成多种OCR服务，提供更准确的文本识别
"""

import os
import json
import requests
from pathlib import Path
from typing import Optional, Dict, Any
import base64

class AIOCRService:
    """AI OCR服务类"""
    
    def __init__(self):
        self.api_keys = self._load_api_keys()
        self.services = ['baidu', 'tencent', 'aliyun', 'easyocr']
    
    def _load_api_keys(self) -> Dict[str, str]:
        """加载API密钥"""
        api_keys = {}
        
        # 从环境变量加载
        if os.getenv('BAIDU_OCR_API_KEY'):
            api_keys['baidu'] = os.getenv('BAIDU_OCR_API_KEY')
        if os.getenv('TENCENT_OCR_SECRET_ID'):
            api_keys['tencent'] = os.getenv('TENCENT_OCR_SECRET_ID')
        if os.getenv('ALIYUN_OCR_ACCESS_KEY'):
            api_keys['aliyun'] = os.getenv('ALIYUN_OCR_ACCESS_KEY')
        
        return api_keys
    
    def extract_text_from_image(self, image_path: Path) -> Optional[str]:
        """从图片中提取文本，优先使用AI服务"""
        try:
            # 1. 尝试百度OCR（免费额度较大）
            if 'baidu' in self.api_keys:
                text = self._baidu_ocr(image_path)
                if text and len(text.strip()) > 20:
                    return text
            
            # 2. 尝试腾讯OCR
            if 'tencent' in self.api_keys:
                text = self._tencent_ocr(image_path)
                if text and len(text.strip()) > 20:
                    return text
            
            # 3. 尝试阿里云OCR
            if 'aliyun' in self.api_keys:
                text = self._aliyun_ocr(image_path)
                if text and len(text.strip()) > 20:
                    return text
            
            # 4. 使用本地PaddleOCR（免费，无需API密钥）
            text = self._paddle_ocr(image_path)
            if text and len(text.strip()) > 20:
                return text
            
            return None
            
        except Exception as e:
            print(f"AI OCR服务调用失败: {e}")
            return None
    
    def _baidu_ocr(self, image_path: Path) -> Optional[str]:
        """百度OCR服务"""
        try:
            # 这里需要实现百度OCR API调用
            # 由于需要申请API密钥，这里提供示例代码
            print("百度OCR服务需要配置API密钥")
            return None
        except Exception as e:
            print(f"百度OCR失败: {e}")
            return None
    
    def _tencent_ocr(self, image_path: Path) -> Optional[str]:
        """腾讯OCR服务"""
        try:
            # 这里需要实现腾讯OCR API调用
            print("腾讯OCR服务需要配置API密钥")
            return None
        except Exception as e:
            print(f"腾讯OCR失败: {e}")
            return None
    
    def _aliyun_ocr(self, image_path: Path) -> Optional[str]:
        """阿里云OCR服务"""
        try:
            # 这里需要实现阿里云OCR API调用
            print("阿里云OCR服务需要配置API密钥")
            return None
        except Exception as e:
            print(f"阿里云OCR失败: {e}")
            return None
    
    def _paddle_ocr(self, image_path: Path) -> Optional[str]:
        """EasyOCR本地服务（免费，替代PaddleOCR）"""
        try:
            # 尝试导入EasyOCR
            try:
                import easyocr
                
                # 设置更长的超时时间和重试机制
                import time
                max_retries = 3
                
                for attempt in range(max_retries):
                    try:
                        print(f"尝试EasyOCR识别 (第{attempt + 1}次)...")
                        reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
                        result = reader.readtext(str(image_path))
                        
                        if result:
                            # 提取所有文本
                            texts = []
                            for detection in result:
                                if detection[1]:  # 文本内容
                                    texts.append(detection[1])
                            
                            extracted_text = '\n'.join(texts)
                            if extracted_text.strip():
                                print(f"EasyOCR识别成功，提取到{len(extracted_text)}个字符")
                                return extracted_text
                        
                        if attempt < max_retries - 1:
                            print(f"第{attempt + 1}次尝试失败，等待后重试...")
                            time.sleep(2)
                            
                    except Exception as e:
                        print(f"第{attempt + 1}次尝试失败: {e}")
                        if attempt < max_retries - 1:
                            time.sleep(2)
                        else:
                            raise e
                
                print("EasyOCR所有尝试都失败了")
                return None
                
            except ImportError:
                print("EasyOCR未安装，请运行: pip install easyocr")
                return None
                
        except Exception as e:
            print(f"EasyOCR最终失败: {e}")
            return None
    
    def extract_text_from_pdf(self, pdf_path: Path) -> Optional[str]:
        """从PDF中提取文本，包括扫描版PDF"""
        try:
            # 1. 尝试pdfplumber提取文本
            try:
                import pdfplumber
                with pdfplumber.open(pdf_path) as pdf:
                    text = ""
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    
                    if text.strip():
                        return text
            except ImportError:
                pass
            
            # 2. 尝试pypdf提取文本
            try:
                from pypdf import PdfReader
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    
                    if text.strip():
                        return text
            except ImportError:
                pass
            
            # 3. 如果文本提取失败，尝试将PDF页面转换为图片进行OCR
            text = self._pdf_to_image_ocr(pdf_path)
            if text:
                return text
            
            return None
            
        except Exception as e:
            print(f"PDF文本提取失败: {e}")
            return None
    
    def _pdf_to_image_ocr(self, pdf_path: Path) -> Optional[str]:
        """将PDF页面转换为图片进行OCR"""
        try:
            # 尝试使用PyMuPDF转换PDF页面为图片
            try:
                import fitz  # PyMuPDF
                doc = fitz.open(str(pdf_path))
                
                if len(doc) == 0:
                    print("PDF文件为空")
                    return None
                
                # 转换第一页为图片
                page = doc[0]
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2倍分辨率
                
                # 保存为临时图片
                import tempfile
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                    pix.save(tmp_file.name)
                    tmp_path = Path(tmp_file.name)
                
                try:
                    # 使用EasyOCR识别图片
                    ocr_text = self._paddle_ocr(tmp_path)
                    if ocr_text:
                        print(f"PDF转图片OCR成功，提取到{len(ocr_text)}个字符")
                        return ocr_text
                finally:
                    # 清理临时文件
                    if tmp_path.exists():
                        tmp_path.unlink()
                
                doc.close()
                return None
                
            except ImportError:
                print("PyMuPDF未安装，尝试pdf2image...")
                
                # 备选方案：使用pdf2image
                try:
                    from pdf2image import convert_from_path
                    images = convert_from_path(str(pdf_path), first_page=1, last_page=1)
                    
                    if images:
                        # 保存第一页为临时图片
                        import tempfile
                        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                            images[0].save(tmp_file.name, 'PNG')
                            tmp_path = Path(tmp_file.name)
                        
                        try:
                            # 使用EasyOCR识别图片
                            ocr_text = self._paddle_ocr(tmp_path)
                            if ocr_text:
                                print(f"PDF转图片OCR成功，提取到{len(ocr_text)}个字符")
                                return ocr_text
                        finally:
                            # 清理临时文件
                            if tmp_path.exists():
                                tmp_path.unlink()
                    
                    return None
                    
                except ImportError:
                    print("pdf2image也未安装")
                    return None
                    
        except Exception as e:
            print(f"PDF转图片OCR失败: {e}")
            return None

# 全局OCR服务实例
ai_ocr_service = AIOCRService()
