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
    """DeepSeek API服务类"""
    
    def __init__(self):
        self.api_key = self._load_api_key()
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.vision_url = "https://api.deepseek.com/v1/chat/completions"  # Vision 也使用 chat completions 端点
        self.model = "deepseek-chat"
        self.max_retries = 3
        self.last_error: Optional[str] = None
        self.last_suggestion: Optional[str] = None

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
            print(f"加载配置文件失败: {e}")
            return None
        
    def is_available(self) -> bool:
        """检查API是否可用"""
        return bool(self.api_key)
    
    def analyze_document_content(self, file_path: Path) -> Optional[str]:
        """分析文档内容，提取关键信息用于重命名"""
        if not self.is_available():
            print("DeepSeek API密钥未配置")
            self._set_error("DeepSeek API密钥未配置", "请在应用配置页填写有效的 API Key 并点击‘测试API’")
            return None

        try:
            # 读取文件内容
            suffix = file_path.suffix.lower()
            if suffix in ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff']:
                # 图片 → Vision
                return self._analyze_image_directly(file_path)

            if suffix == '.pdf':
                content = self._read_pdf_content(file_path)
                if content:
                    return self._call_deepseek_api(content, file_path.name)
                # 若无文本，尝试渲染第一页为图片后走 Vision
                b64_png = self._render_pdf_first_page_base64(file_path)
                if b64_png:
                    return self._analyze_image_base64(b64_png, file_path)
                self._set_error(
                    "PDF为扫描版且缺少渲染依赖，无法提取文本",
                    "建议安装 PyMuPDF: pip install pymupdf；或提供文本版PDF后重试"
                )
                return None

            # 其他文本类文件 → 读取文本后走 Chat
            content = self._read_text_content(file_path)
            if content:
                return self._call_deepseek_api(content, file_path.name)
            self._set_error("无法读取文本内容", "请确认文件编码或改用 PDF/图片后重试")
            return None

        except Exception as e:
            print(f"DeepSeek API分析失败: {e}")
            return None
    
    def _read_pdf_content(self, pdf_path: Path) -> Optional[str]:
        """读取PDF内容"""
        try:
            # 尝试使用PyMuPDF
            import fitz
            doc = fitz.open(str(pdf_path))
            text = ""
            
            # 提取前几页文本
            for page_num in range(min(3, len(doc))):
                page = doc[page_num]
                page_text = page.get_text()
                if page_text:
                    text += page_text + "\n"
            
            doc.close()
            return text if text.strip() else None
            
        except ImportError:
            print("PyMuPDF未安装，尝试pdfplumber...")
            try:
                import pdfplumber
                with pdfplumber.open(pdf_path) as pdf:
                    text = ""
                    for page_num in range(min(3, len(pdf.pages))):
                        page = pdf.pages[page_num]
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    return text if text.strip() else None
            except ImportError:
                print("pdfplumber也未安装")
                return None
        except Exception as e:
            print(f"PDF读取失败: {e}")
            return None
    
    def _read_image_content(self, image_path: Path) -> Optional[str]:
        """读取图片内容（OCR）- 已禁用EasyOCR避免下载模型"""
        try:
            # 禁用EasyOCR，避免下载耗时模型
            # 对于图片文件，直接返回None，让DeepSeek API处理
            print("图片OCR已禁用，避免下载模型")
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
            print(f"图片OCR失败: {e}")
            return None
    
    def _analyze_image_directly(self, image_path: Path) -> Optional[str]:
        """直接使用DeepSeek API分析图片，不依赖本地OCR"""
        try:
            # 暂时禁用 Vision API，因为 DeepSeek 的 Vision 模型格式要求特殊
            # 根据错误信息，当前的请求格式不被支持
            msg = "DeepSeek Vision API 格式要求特殊，暂不可用"
            self._set_error(msg, "建议使用文本版文档或等待官方 Vision API 文档发布")
            print(msg)
            return None
            
            # 保留原代码供将来启用
            # with open(image_path, 'rb') as f:
            #     image_data = f.read()
            #     b64 = base64.b64encode(image_data).decode('utf-8')
            # return self._analyze_image_base64(b64, image_path)
        except Exception as e:
            msg = f"图片直接分析失败: {e}"
            print(msg)
            self._set_error(msg, "请确认网络可达且 API Key 有效；必要时重试")
            return None

    def _analyze_image_base64(self, base64_image: str, src_path: Path) -> Optional[str]:
        """通过 Vision 模型分析 base64 图片。"""
        try:
            # 简化提示词，避免复杂的格式要求
            prompt = "请分析这张图片，提取关键信息用于文件重命名。直接返回重命名后的文件名，格式为：基金名称-文档类型-日期"
            
            # 尝试多种 Vision API 格式
            # 格式1: 标准格式
            data1 = {
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
            
            # 格式2: 简化格式
            data2 = {
                "model": "deepseek-vl",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ],
                "max_tokens": 300,
                "temperature": 0.1
            }
            
            # 先尝试格式1，失败则尝试格式2
            data = data1
            
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

            for attempt in range(self.max_retries):
                try:
                    print(f"尝试调用 Vision API (第{attempt + 1}次)...")
                    
                    # 如果是第二次尝试且第一次失败，尝试格式2
                    if attempt == 1 and response.status_code == 422:
                        print("第一次尝试失败，切换到格式2...")
                        data = data2
                    
                    response = requests.post(self.vision_url, headers=headers, json=data, timeout=45)
                    
                    if response.status_code == 200:
                        result = response.json()
                        if 'choices' in result and result['choices']:
                            content = result['choices'][0]['message']['content'].strip()
                            print(f"Vision API 调用成功: {content}")
                            return content
                    else:
                        err = f"Vision调用失败[{response.status_code}]: {response.text[:200]}"
                        print(err)
                        self._set_error(err, "请确认已开通 Vision 权限且传参格式为 chat.completions")
                        
                        # 如果是格式错误，尝试调试
                        if response.status_code == 422:
                            print(f"请求数据: {data}")
                            print(f"完整错误: {response.text}")
                            
                except requests.exceptions.RequestException as e:
                    err = f"Vision请求异常: {e}"
                    print(err)
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
            print(f"文件名分析失败: {e}")
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
            print(f"文本文件读取失败: {e}")
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
                    print(f"调用DeepSeek API (第{attempt + 1}次)...")
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
                            print(f"DeepSeek API调用成功！")
                            return content.strip()
                    else:
                        print(f"API调用失败，状态码: {response.status_code}")
                        print(f"错误信息: {response.text}")
                        
                        # 设置错误信息
                        if response.status_code == 401:
                            self._set_error("API 密钥无效或已过期", "请检查并更新 API 密钥")
                        elif response.status_code == 429:
                            self._set_error("API 调用频率超限", "请稍后重试或检查配额使用情况")
                        elif response.status_code >= 500:
                            self._set_error("DeepSeek 服务器错误", "请稍后重试")
                        else:
                            self._set_error(f"API 调用失败 ({response.status_code})", "请检查网络连接和 API 状态")
                        
                except requests.exceptions.RequestException as e:
                    print(f"第{attempt + 1}次尝试失败: {e}")
                    if attempt < self.max_retries - 1:
                        time.sleep(2)
                    else:
                        self._set_error(f"网络请求失败: {e}", "请检查网络连接和代理设置")
                        raise e
            
            return None
            
        except Exception as e:
            print(f"DeepSeek API调用失败: {e}")
            return None
    
    def _build_analysis_prompt(self, content: str, filename: str) -> str:
        """构建分析提示词"""
        prompt = f"""
请分析以下文档内容，提取关键信息用于文件重命名。

文件名: {filename}
文档内容:
{content[:2000]}...

请按照以下格式提取信息：
1. 基金名称（如：展弘稳进1号7期私募基金）
2. 文档类型（如：临时开放日公告、打款凭证、基本信息表）
3. 相关日期（如：2025年8月22日）
4. 客户姓名（如果有）

请直接返回重命名后的文件名，格式为：
基金名称-文档类型-日期.扩展名

例如：展弘稳进1号7期私募基金-临时开放日公告-20250822.pdf

如果无法提取到足够信息，请返回"无法识别"。
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
            print(f"提取重命名信息失败: {e}")
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
