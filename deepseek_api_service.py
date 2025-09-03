#!/usr/bin/env python3
"""
DeepSeek API服务模块
用于智能文档内容分析和重命名
"""

import os
import json
import requests
import base64
from pathlib import Path
from typing import Optional, Dict, Any
import time

class DeepSeekAPIService:
    """DeepSeek API 服务类"""
    
    def __init__(self):
        self.api_key = None
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.vision_url = "https://api.deepseek.com/v1/chat/completions"
        self.model = "deepseek-chat"
        self.max_retries = 3
        self.last_error = None
        self.last_suggestion = None
        self.log_callback = None  # 添加日志回调函数
        
        # 初始化时加载 API 密钥
        self.api_key = self._load_api_key()
    
    def set_log_callback(self, callback):
        """设置日志回调函数"""
        self.log_callback = callback
    
    def _log(self, message):
        """统一的日志输出方法"""
        if self.log_callback:
            self.log_callback(message)
        print(message)  # 同时输出到控制台
    
    def _set_error(self, error: str, suggestion: Optional[str] = None) -> None:
        self.last_error = error
        self.last_suggestion = suggestion
    
    def _load_api_key(self) -> Optional[str]:
        """从配置文件加载API密钥"""
        try:
            # 首先尝试从环境变量读取（向后兼容）
            env_key = os.getenv('DEEPSEEK_API_KEY')
            if env_key and env_key != "your_api_key_here":
                return env_key
            
            # 从配置文件读取
            config_path = Path(__file__).parent / "config.json"
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    api_key = config.get('deepseek_api_key', '')
                    if api_key and api_key != "your_api_key_here":
                        return api_key
            
            return None
            
        except Exception as e:
            self._log(f"加载配置文件失败: {e}")
            return None
    
    def reload_api_key(self) -> None:
        """重新加载API密钥"""
        self.api_key = self._load_api_key()
        if self.api_key:
            self._log("API密钥已重新加载")
        else:
            self._log("API密钥加载失败")
        
    def is_available(self) -> bool:
        """检查API是否可用"""
        return bool(self.api_key)
    
    def analyze_document_content(self, file_path: Path) -> Optional[str]:
        """分析文档内容，提取关键信息用于重命名"""
        if not self.is_available():
            self._log("DeepSeek API密钥未配置")
            self._set_error("DeepSeek API密钥未配置", "请在应用配置页填写有效的 API Key 并点击'测试API'")
            return None

        try:
            # 读取文件内容
            suffix = file_path.suffix.lower()
            
            if suffix == '.pdf':
                self._log("处理 PDF 文件...")
                # 先尝试提取文本
                content = self._extract_pdf_text(file_path)
                if content and len(content.strip()) > 10:
                    self._log(f"PDF 文本提取成功，长度: {len(content)}")
                    # 有文本内容，使用 DeepSeek Chat API
                    return self._call_deepseek_api(content, file_path.name)
                else:
                    self._log("PDF 文本提取失败或内容为空，尝试 OCR 识别...")
                    # 文本提取失败，可能是扫描件，使用 OCR
                    return self._process_scanned_document(file_path)
            
            elif suffix in ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff']:
                self._log("处理图片文件...")
                # 图片文件直接使用 OCR
                return self._process_scanned_document(file_path)
            
            elif suffix in ['.txt', '.doc', '.docx', '.rtf']:
                self._log("处理文本文件...")
                # 其他文本类文件 → 读取文本后走 Chat
                content = self._read_text_content(file_path)
                if content:
                    return self._call_deepseek_api(content, file_path.name)
                self._set_error("无法读取文本内容", "请确认文件编码或改用 PDF/图片后重试")
                return None
            
            else:
                self._log("使用启发式命名...")
                return self._extract_from_filename(file_path)

        except Exception as e:
            self._log(f"DeepSeek API分析失败: {e}")
            return self._extract_from_filename(file_path)
    
    def _extract_pdf_text(self, pdf_path: Path) -> Optional[str]:
        """提取 PDF 文本内容"""
        try:
            # 尝试使用 PyMuPDF 提取文本
            import fitz
            doc = fitz.open(str(pdf_path))
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text.strip()
        except ImportError:
            self._log("PyMuPDF 未安装，尝试其他方法...")
            return None
        except Exception as e:
            self._log(f"PDF 文本提取失败: {e}")
            return None
    
    def _read_pdf_content(self, pdf_path: Path) -> Optional[str]:
        """读取 PDF 内容（兼容性方法）"""
        return self._extract_pdf_text(pdf_path)
    
    def _read_image_content(self, image_path: Path) -> Optional[str]:
        """读取图片内容（OCR）- 已禁用EasyOCR避免下载模型"""
        try:
            # 禁用EasyOCR，避免下载耗时模型
            # 对于图片文件，直接返回None，让DeepSeek API处理
            self._log("图片OCR已禁用，避免下载模型")
            return None
            
            # 原EasyOCR代码已注释
            # import easyocr
            # reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
            # result = reader.readtext(str(image_path))
            # 
            # if result:
            #     texts = []
            #     for detection in result:
            #         if detection[1]:
            #             texts.append(detection[1])
            #     return '\n'.join(texts) if texts else None
            # 
            # return None
            
        except Exception as e:
            self._log(f"图片OCR失败: {e}")
            return None
    
    def _analyze_image_directly(self, image_path: Path) -> Optional[str]:
        """直接使用DeepSeek API分析图片，不依赖本地OCR"""
        try:
            # 检查图片大小
            file_size = image_path.stat().st_size
            if file_size > 10 * 1024 * 1024:  # 10MB 限制
                msg = f"图片文件过大 ({file_size / 1024 / 1024:.1f}MB)，超过 API 限制"
                self._set_error(msg, "请使用小于 10MB 的图片文件")
                self._log(msg)
                return None
            
            # 读取图片并转为base64
            with open(image_path, 'rb') as f:
                image_data = f.read()
                b64 = base64.b64encode(image_data).decode('utf-8')
                
            # 验证 base64 数据
            if len(b64) > 5000000:  # 5MB base64 限制
                msg = f"base64 数据过大 ({len(b64)} 字符)，可能超出 API 限制"
                self._set_error(msg, "请使用较小的图片文件")
                self._log(msg)
                return None
                
            return self._analyze_image_base64(b64, image_path)
        except Exception as e:
            msg = f"图片直接分析失败: {e}"
            self._log(msg)
            self._set_error(msg, "请确认网络可达且 API Key 有效；必要时重试")
            return None

    def _analyze_image_base64(self, base64_image: str, src_path: Path) -> Optional[str]:
        """通过 Vision 模型分析 base64 图片。"""
        try:
            # 简化提示词，避免复杂的格式要求
            prompt = "请分析这张图片，提取关键信息用于文件重命名。直接返回重命名后的文件名，格式为：基金名称-文档类型-日期"
            
            # 使用简化的 Vision API 格式
            data = {
                "model": "deepseek-vl",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ],
                "max_tokens": 300,
                "temperature": 0.1
            }
            
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

            for attempt in range(self.max_retries):
                try:
                    self._log(f"尝试调用 Vision API (第{attempt + 1}次)...")
                    response = requests.post(self.vision_url, headers=headers, json=data, timeout=45)
                    
                    if response.status_code == 200:
                        result = response.json()
                        if 'choices' in result and result['choices']:
                            content = result['choices'][0]['message']['content'].strip()
                            self._log(f"Vision API 调用成功: {content}")
                            return content
                    else:
                        err = f"Vision调用失败[{response.status_code}]: {response.text[:200]}"
                        self._log(err)
                        self._set_error(err, "请确认已开通 Vision 权限且传参格式为 chat.completions")
                        
                        # 如果是格式错误，尝试调试
                        if response.status_code == 422:
                            self._log(f"请求数据: {data}")
                            self._log(f"完整错误: {response.text}")
                            
                except requests.exceptions.RequestException as e:
                    err = f"Vision请求异常: {e}"
                    self._log(err)
                    self._set_error(err, "检查网络与代理设置，稍后重试")
                    
                if attempt < self.max_retries - 1:
                    time.sleep(2)
                    
            return None
            
        except Exception as e:
            self._set_error(f"Vision内部错误: {e}")
            return None

    def _render_pdf_first_page_base64(self, pdf_path: Path) -> Optional[str]:
        """将PDF第一页渲染为PNG并返回base64，需要PyMuPDF。"""
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(str(pdf_path))
            if len(doc) == 0:
                return None
            page = doc[0]
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img_bytes = pix.tobytes("png")
            doc.close()
            return base64.b64encode(img_bytes).decode('utf-8')
        except ImportError:
            return None
        except Exception:
            return None
    
    def _process_scanned_document(self, file_path: Path) -> Optional[str]:
        """处理扫描件：转换为图片，OCR 识别，然后调用 DeepSeek API"""
        try:
            self._log("开始处理扫描件...")
            
            # 如果是 PDF，先转换为图片
            if file_path.suffix.lower() == '.pdf':
                self._log("将 PDF 转换为图片...")
                image_path = self._convert_pdf_to_image(file_path)
                if not image_path:
                    self._log("PDF 转图片失败")
                    return self._extract_from_filename(file_path)
            else:
                image_path = file_path
            
            # 使用 OCR 识别图片文本
            self._log("使用 OCR 识别图片文本...")
            ocr_text = self._extract_text_with_ocr(image_path)
            
            if ocr_text and len(ocr_text.strip()) > 10:
                self._log(f"OCR 识别成功，文本长度: {len(ocr_text)}")
                self._log(f"OCR 识别内容: {ocr_text[:200]}...")
                
                # 将识别出的文本发送给 DeepSeek API
                return self._call_deepseek_api(ocr_text, file_path.name)
            else:
                self._log("OCR 识别失败或内容为空")
                return self._extract_from_filename(file_path)
                
        except Exception as e:
            self._log(f"扫描件处理失败: {e}")
            return self._extract_from_filename(file_path)
    
    def _convert_pdf_to_image(self, pdf_path: Path) -> Optional[Path]:
        """将 PDF 第一页转换为图片"""
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(str(pdf_path))
            if len(doc) == 0:
                return None
            
            # 渲染第一页为高分辨率图片
            page = doc[0]
            mat = fitz.Matrix(3, 3)  # 3倍分辨率
            pix = page.get_pixmap(matrix=mat)
            
            # 保存为临时图片文件
            temp_image_path = pdf_path.parent / f"{pdf_path.stem}_temp.png"
            pix.save(str(temp_image_path))
            doc.close()
            
            self._log(f"PDF 已转换为图片: {temp_image_path}")
            return temp_image_path
            
        except ImportError:
            self._log("PyMuPDF 未安装，无法转换 PDF")
            return None
        except Exception as e:
            self._log(f"PDF 转换失败: {e}")
            return None
    
    def _extract_text_with_ocr(self, image_path: Path) -> Optional[str]:
        """使用 EasyOCR 识别图片文本"""
        try:
            # 添加全局异常保护
            import sys
            import traceback
            
            self._log("开始导入 EasyOCR 模块...")
            
            # 检查模型文件位置（优先级：EXE内 > 当前目录 > 用户目录）
            model_dirs = []
            
            try:
                # 1. 检查EXE内的模型文件（最高优先级）
                if getattr(sys, 'frozen', False):
                    # 如果是打包后的EXE
                    exe_dir = os.path.dirname(sys.executable)
                    self._log(f"检测到EXE运行，EXE目录: {exe_dir}")
                    
                    # 1.1 检查EXE同级目录的easyocr_models
                    exe_models_dir = os.path.join(exe_dir, "easyocr_models")
                    model_dirs.append(("EXE内模型目录", exe_models_dir))
                    self._log(f"检查EXE内模型: {exe_models_dir}")
                    
                    # 1.2 检查PyInstaller临时目录（_MEIPASS）- 这是关键位置
                    if hasattr(sys, '_MEIPASS'):
                        meipass_models = os.path.join(sys._MEIPASS, "easyocr_models")
                        model_dirs.append(("PyInstaller临时目录", meipass_models))
                        self._log(f"检查PyInstaller临时目录: {meipass_models}")
                    
                    # 1.3 检查EXE目录的父目录
                    try:
                        exe_parent = os.path.dirname(exe_dir)
                        exe_parent_models = os.path.join(exe_parent, "easyocr_models")
                        model_dirs.append(("EXE父目录模型", exe_parent_models))
                    except Exception as e:
                        self._log(f"检查EXE父目录时出错: {e}")
                
                # 2. 检查当前工作目录的模型文件
                try:
                    current_models_dir = Path("easyocr_models")
                    model_dirs.append(("当前目录模型", str(current_models_dir.absolute())))
                except Exception as e:
                    self._log(f"检查当前目录时出错: {e}")
                
                # 3. 检查用户目录的模型文件
                try:
                    home_dir = os.path.expanduser("~")
                    user_models_dir = os.path.join(home_dir, ".EasyOCR")
                    model_dirs.append(("用户目录模型", user_models_dir))
                except Exception as e:
                    self._log(f"检查用户目录时出错: {e}")
                
                # 4. 检查系统临时目录（简化版本）
                try:
                    import tempfile
                    temp_dir = tempfile.gettempdir()
                    temp_models_dir = os.path.join(temp_dir, "easyocr_models")
                    model_dirs.append(("系统临时目录", temp_models_dir))
                except Exception as e:
                    self._log(f"检查系统临时目录时出错: {e}")
                
            except Exception as e:
                self._log(f"模型目录检查过程中出错: {e}")
                # 如果出错，使用最基本的检查
                model_dirs = []
                if getattr(sys, 'frozen', False):
                    exe_dir = os.path.dirname(sys.executable)
                    exe_models_dir = os.path.join(exe_dir, "easyocr_models")
                    model_dirs.append(("EXE内模型目录", exe_models_dir))
                model_dirs.append(("当前目录模型", "easyocr_models"))
            
            # 查找可用的模型文件
            local_models_dir = None
            self._log("=" * 50)
            self._log("🔍 开始搜索EasyOCR模型文件...")
            self._log("=" * 50)
            
            try:
                for desc, model_dir in model_dirs:
                    try:
                        self._log(f"检查{desc}: {model_dir}")
                        if os.path.exists(model_dir):
                            if os.path.isdir(model_dir):
                                model_files = list(Path(model_dir).glob("*.pth"))
                                if model_files:
                                    self._log(f"✅ 在{desc}找到模型文件: {[f.name for f in model_files]}")
                                    # 显示文件大小
                                    total_size = sum(f.stat().st_size for f in model_files) / (1024*1024)
                                    self._log(f"   模型文件总大小: {total_size:.1f} MB")
                                    local_models_dir = Path(model_dir)
                                    break
                                else:
                                    self._log(f"❌ {desc}存在但无模型文件")
                            else:
                                self._log(f"❌ {desc}存在但不是目录")
                        else:
                            self._log(f"❌ {desc}不存在")
                    except Exception as e:
                        self._log(f"检查{desc}时出错: {e}")
                        continue
            except Exception as e:
                self._log(f"模型文件搜索过程中出错: {e}")
            
            self._log("=" * 50)
            if local_models_dir:
                self._log(f"🎯 使用模型目录: {local_models_dir.absolute()}")
                try:
                    # 设置环境变量指向本地模型目录
                    os.environ['EASYOCR_MODULE_PATH'] = str(local_models_dir.absolute())
                    self._log("已设置EASYOCR_MODULE_PATH环境变量")
                except Exception as e:
                    self._log(f"设置环境变量时出错: {e}")
            else:
                self._log("❌ 未发现任何本地模型文件，将使用默认下载")
                self._log("💡 建议：检查EXE是否包含模型文件，或手动下载模型到用户目录")
                self._log("📋 解决方案：")
                self._log("   1. 重新构建EXE（确保包含模型文件）")
                self._log("   2. 手动下载模型文件到 ~/.EasyOCR 目录")
                self._log("   3. 将模型文件放在EXE同级的 easyocr_models 目录")
                self._log("   4. 检查网络连接，确保可以访问EasyOCR服务器")
            
            # 使用线程和超时机制来防止EasyOCR初始化卡住
            reader = None
            init_error = None
            
            def init_easyocr():
                nonlocal reader, init_error
                try:
                    self._log("正在初始化 EasyOCR Reader...")
                    if local_models_dir and list(local_models_dir.glob("*.pth")):
                        self._log("使用本地模型文件初始化...")
                        reader = easyocr.Reader(['ch_sim', 'en'], gpu=False, model_storage_directory=str(local_models_dir.absolute()))
                    else:
                        self._log("使用默认模型下载初始化...")
                        # 设置更长的超时时间和重试机制
                        reader = easyocr.Reader(['ch_sim', 'en'], gpu=False, download_enabled=True)
                    self._log("EasyOCR Reader 初始化成功")
                except Exception as e:
                    init_error = e
                    self._log(f"EasyOCR Reader 初始化失败: {e}")
                    self._log(f"异常类型: {type(e).__name__}")
                    self._log(f"异常详情: {str(e)}")
                    # 添加详细的异常堆栈信息
                    self._log("异常堆栈:")
                    for line in traceback.format_exc().split('\n'):
                        if line.strip():
                            self._log(f"  {line}")
            
            # 启动初始化线程
            init_thread = threading.Thread(target=init_easyocr)
            init_thread.daemon = True
            init_thread.start()
            
            # 等待初始化完成，本地模型60秒，网络下载120秒
            timeout = 120 if not (local_models_dir and list(local_models_dir.glob("*.pth"))) else 60
            start_time = time.time()
            while init_thread.is_alive() and (time.time() - start_time) < timeout:
                time.sleep(1)
                # 每10秒显示一次进度
                elapsed = int(time.time() - start_time)
                if elapsed % 10 == 0 and elapsed > 0:
                    self._log(f"EasyOCR 初始化进行中... ({elapsed}/{timeout}秒)")
            
            if init_thread.is_alive():
                # 超时，记录超时信息
                self._log(f"EasyOCR 初始化超时（{timeout}秒）")
                if local_models_dir:
                    self._log("本地模型存在但初始化超时，可能是模型文件损坏")
                else:
                    self._log("建议：检查网络连接或使用本地模型文件")
                return None
            
            if init_error:
                self._log(f"EasyOCR 初始化出错，停止执行")
                self._log(f"错误类型: {type(init_error).__name__}")
                self._log(f"错误信息: {str(init_error)}")
                
                # 如果是网络错误，提供具体建议
                if "WinError 10060" in str(init_error) or "timeout" in str(init_error).lower():
                    self._log("网络连接超时，建议：")
                    self._log("1. 检查网络连接")
                    self._log("2. 使用代理或VPN")
                    self._log("3. 下载模型文件到本地")
                
                return None
            
            if reader is None:
                self._log("EasyOCR Reader 初始化失败，停止执行")
                return None
            
            self._log("开始 OCR 识别...")
            
            # 读取图片
            try:
                image = cv2.imread(str(image_path))
                if image is None:
                    self._log("无法读取图片")
                    return None
                self._log(f"图片读取成功，尺寸: {image.shape}")
            except Exception as e:
                self._log(f"图片读取失败: {e}")
                return None
            
            # 进行 OCR 识别，也添加超时保护
            ocr_results = None
            ocr_error = None
            
            def run_ocr():
                nonlocal ocr_results, ocr_error
                try:
                    self._log("开始执行OCR识别...")
                    ocr_results = reader.readtext(image)
                    self._log(f"OCR识别完成，结果数量: {len(ocr_results)}")
                except Exception as e:
                    ocr_error = e
                    self._log(f"OCR识别失败: {e}")
                    self._log(f"异常类型: {type(e).__name__}")
                    self._log(f"异常详情: {str(e)}")
                    # 添加详细的异常堆栈信息
                    self._log("异常堆栈:")
                    for line in traceback.format_exc().split('\n'):
                        if line.strip():
                            self._log(f"  {line}")
            
            # 启动OCR线程
            ocr_thread = threading.Thread(target=run_ocr)
            ocr_thread.daemon = True
            ocr_thread.start()
            
            # 等待OCR完成，设置超时
            ocr_timeout = 120
            ocr_start_time = time.time()
            while ocr_thread.is_alive() and (time.time() - ocr_start_time) < ocr_timeout:
                time.sleep(1)
                # 每10秒显示一次进度
                elapsed = int(time.time() - ocr_start_time)
                if elapsed % 10 == 0 and elapsed > 0:
                    self._log(f"OCR 识别进行中... ({elapsed}/{ocr_timeout}秒)")
            
            if ocr_thread.is_alive():
                self._log(f"OCR 识别超时（{ocr_timeout}秒）")
                return None
            
            if ocr_error:
                self._log(f"OCR 识别出错: {ocr_error}")
                return None
            
            if ocr_results is None:
                self._log("OCR 识别未返回结果")
                return None
            
            # 提取文本内容
            try:
                text_parts = []
                for bbox, text, prob in ocr_results:
                    if text.strip() and prob > 0.1:  # 过滤低置信度的结果
                        text_parts.append(text.strip())
                
                if not text_parts:
                    self._log("OCR 识别结果为空或置信度过低")
                    return None
                
                full_text = " ".join(text_parts)
                self._log(f"OCR 识别成功，文本长度: {len(full_text)}")
                self._log(f"OCR 识别内容: {full_text[:200]}{'...' if len(full_text) > 200 else ''}")
                
                return full_text
                
            except Exception as e:
                self._log(f"文本提取失败: {e}")
                return None
                
        except Exception as e:
            # 全局异常保护
            self._log(f"OCR处理过程中发生未预期的异常: {e}")
            self._log(f"异常类型: {type(e).__name__}")
            self._log(f"异常详情: {str(e)}")
            # 添加详细的异常堆栈信息
            self._log("异常堆栈:")
            for line in traceback.format_exc().split('\n'):
                if line.strip():
                    self._log(f"  {line}")
            return None
        except KeyboardInterrupt:
            # 处理用户中断
            self._log("OCR处理被用户中断")
            return None
        except SystemExit:
            # 处理系统退出
            self._log("OCR处理被系统中断")
            return None
        except:
            # 捕获所有其他异常
            self._log("OCR处理过程中发生未知异常")
            import traceback
            self._log("异常堆栈:")
            for line in traceback.format_exc().split('\n'):
                if line.strip():
                    self._log(f"  {line}")
            return None
    
    def _extract_text_with_tesseract(self, image_path: Path) -> Optional[str]:
        """使用 Tesseract 作为 EasyOCR 的替代方案"""
        try:
            import pytesseract
            from PIL import Image
            
            self._log("使用 Tesseract 进行 OCR 识别...")
            
            # 使用PIL打开图片
            image = Image.open(image_path)
            
            # 使用Tesseract进行OCR识别
            text = pytesseract.image_to_string(image, lang='chi_sim+eng')
            
            if text and text.strip():
                self._log("Tesseract OCR 识别成功")
                return text.strip()
            else:
                self._log("Tesseract OCR 识别结果为空")
                return None
                
        except ImportError as e:
            self._log(f"Tesseract 模块导入失败: {e}")
            return None
        except Exception as e:
            self._log(f"Tesseract OCR 识别失败: {e}")
            return None
    
    def _extract_from_filename(self, file_path: Path) -> Optional[str]:
        """从文件名提取信息（通用启发式，无硬编码样本）。"""
        try:
            filename = file_path.stem
            suffix = file_path.suffix

            # 使用通用启发式从文件名中提取字段
            doc_type = self._extract_doc_type(filename)
            date_str = self._extract_date(filename)
            fund_name = self._extract_fund_name(filename)

            parts = []
            if fund_name:
                parts.append(fund_name)
            if doc_type:
                parts.append(doc_type)
            if date_str:
                parts.append(date_str)

            if not parts:
                return None

            candidate = "-".join(parts) + suffix
            return self._sanitize_filename(candidate)

        except Exception as e:
            self._log(f"文件名分析失败: {e}")
            return None
    
    def _read_text_content(self, file_path: Path) -> Optional[str]:
        """读取文本文件内容"""
        try:
            # 尝试不同编码
            encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        return file.read()
                except UnicodeDecodeError:
                    continue
            return None
        except Exception as e:
            self._log(f"文本文件读取失败: {e}")
            return None
    
    def _call_deepseek_api(self, content: str, filename: str) -> Optional[str]:
        """调用DeepSeek API分析内容"""
        try:
            # 构建提示词
            prompt = self._build_analysis_prompt(content, filename)
            
            # 准备请求数据
            data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 500,
                "temperature": 0.1
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # 发送请求
            for attempt in range(self.max_retries):
                try:
                    self._log(f"调用DeepSeek API (第{attempt + 1}次)...")
                    response = requests.post(
                        self.base_url,
                        headers=headers,
                        json=data,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if 'choices' in result and len(result['choices']) > 0:
                            content = result['choices'][0]['message']['content']
                            self._log(f"DeepSeek API调用成功！")
                            self._log(f"API 返回内容: {content}")
                            
                            # 检查返回内容是否有效
                            if content and content.strip() and content.strip() != "无法识别":
                                return content.strip()
                            else:
                                self._log("API 返回内容无效或为空，使用启发式命名")
                                return None
                        else:
                            self._log("API 响应格式异常")
                            return None
                    else:
                        self._log(f"API调用失败，状态码: {response.status_code}")
                        self._log(f"错误信息: {response.text}")
                        
                        # 设置错误信息
                        if response.status_code == 401:
                            self._set_error("API 密钥无效或已过期", "请检查并更新 API 密钥")
                        elif response.status_code == 429:
                            self._set_error("API 调用频率超限", "请稍后重试或检查配额使用情况")
                        elif response.status_code == 402:
                            err = f"API 余额不足: {response.text[:100]}"
                            self._set_error(err, "请充值 DeepSeek API 账户或等待下月重置")
                            return None
                        elif response.status_code >= 500:
                            self._set_error("DeepSeek 服务器错误", "请稍后重试")
                        else:
                            self._set_error(f"API 调用失败 ({response.status_code})", "请检查网络连接和 API 状态")
                        
                except requests.exceptions.RequestException as e:
                    self._log(f"第{attempt + 1}次尝试失败: {e}")
                    if attempt < self.max_retries - 1:
                        time.sleep(2)
                    else:
                        self._set_error(f"网络请求失败: {e}", "请检查网络连接和代理设置")
                        raise e
            
            return None
            
        except Exception as e:
            self._log(f"DeepSeek API调用失败: {e}")
            return None
    
    def _build_analysis_prompt(self, content: str, filename: str) -> str:
        """构建分析提示词"""
        prompt = f"""
请分析以下文档内容，提取关键信息用于文件重命名。

文件名: {filename}
文档内容:
{content[:2000]}...

请仔细分析文档内容，提取以下信息：
1. 基金名称或产品名称（如：展弘稳进1号7期私募基金、浦发银行产品等）
2. 文档类型（如：临时开放日公告、打款凭证、基本信息表、业务凭证、回单等）
3. 相关日期（如：2025年8月22日、2025-06-06等）
4. 客户姓名或相关方（如果有）

请直接返回重命名后的文件名，格式为：
基金名称-文档类型-日期.扩展名

例如：
- 展弘稳进1号7期私募基金-临时开放日公告-20250822.pdf
- 浦发银行-业务凭证回单-仇健鸣-20250606.pdf
- 打款凭证-仇健鸣-20250606.pdf

如果确实无法提取到足够信息，请返回"无法识别"。

请确保返回的文件名有意义且包含关键信息。
"""
        return prompt.strip()
    
    def extract_renaming_info(self, file_path: Path) -> Optional[str]:
        """提取重命名信息"""
        try:
            # 调用DeepSeek API分析
            result = self.analyze_document_content(file_path)
            
            if result and result != "无法识别":
                # 清理结果，确保格式正确
                result = result.strip()
                if result.endswith(file_path.suffix):
                    return result
                else:
                    # 添加文件扩展名
                    return f"{result}{file_path.suffix}"
            
            # 当API无法返回结果时，使用启发式从文件名进行构造
            heuristic_from_name = self._extract_from_filename(file_path)
            if heuristic_from_name:
                return heuristic_from_name

            return None
            
        except Exception as e:
            self._log(f"提取重命名信息失败: {e}")
            return None

    # ===== 以下为通用启发式提取函数（无硬编码特殊样本） =====
    def _extract_date(self, text: str) -> Optional[str]:
        """从文本中提取日期，统一为YYYYMMDD。"""
        import re
        # 1) 8位数字
        m = re.search(r'(19|20)\d{2}[./-]?\s?(0?[1-9]|1[0-2])[./-]?\s?([0-2]?\d|3[01])', text)
        if m:
            year = m.group(0)[0:4]
            # 兼容分隔符与不补零
            g = m.groups()
            month = f"{int(g[1]):02d}"
            day = f"{int(g[2]):02d}"
            return f"{year}{month}{day}"

        # 2) 汉字日期
        m2 = re.search(r'(19|20)\d{2}年\s*(0?[1-9]|1[0-2])月\s*([0-2]?\d|3[01])日?', text)
        if m2:
            year = text[m2.start():m2.start()+4]
            month = f"{int(m2.group(2)):02d}"
            day = f"{int(m2.group(3)):02d}"
            return f"{year}{month}{day}"
        return None

    def _extract_doc_type(self, text: str) -> Optional[str]:
        """从文本中识别文档类型关键字，返回规范化名称。"""
        mapping = {
            '临时开放日公告': ['临时开放日公告', '开放日公告', '开放公告'],
            '打款凭证': ['打款凭证', '付款凭证', '汇款回单', '转账回单'],
            '基本信息表': ['基本信息表', '信息表'],
            '确认函': ['确认函', '确认书'],
            '合同': ['合同', '协议'],
            '说明书': ['说明书', '产品说明书', '募集说明书'],
            '年度报告': ['年度报告', '年报'],
            '季度报告': ['季度报告', '季报'],
            '月度报告': ['月度报告', '月报'],
        }
        for canonical, keywords in mapping.items():
            for kw in keywords:
                if kw in text:
                    return canonical
        # 兜底：若包含图片常见词
        if '微信图片' in text:
            return '打款凭证'
        return None

    def _extract_fund_name(self, text: str) -> Optional[str]:
        """从文本中提取看起来像“xxx基金/xxx私募基金/xxx私募证券投资基金”的名称。"""
        import re
        # 典型基金名称尾缀
        candidates = re.findall(r'[\u4e00-\u9fa5A-Za-z0-9]+?(?:\d+号)?(?:\d+期)?(?:私募(?:证券)?投资)?基金', text)
        if candidates:
            # 选择最长的匹配，通常信息更完整
            candidates.sort(key=len, reverse=True)
            return candidates[0]
        # 次级：任意以“基金”结尾的短语
        candidates = re.findall(r'[\u4e00-\u9fa5A-Za-z0-9]+基金', text)
        if candidates:
            candidates.sort(key=len, reverse=True)
            return candidates[0]
        return None

    def _sanitize_filename(self, name: str) -> str:
        """清理非法字符并压缩多余分隔符。"""
        import re
        # Windows非法字符: \ / : * ? " < > |
        cleaned = re.sub(r'[\\/:*?"<>|]', '-', name)
        # 去除多余空白
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        # 合并多个连续的'-'
        cleaned = re.sub(r'-{2,}', '-', cleaned)
        return cleaned

# 全局DeepSeek服务实例
deepseek_service = DeepSeekAPIService()
