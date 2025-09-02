# OCR问题解决指南

## 问题描述
exe文件在初始化EasyOCR时卡住，显示：
```
[14:33:11] 处理图片文件...
[14:33:11] 开始处理扫描件...
[14:33:11] 使用 OCR 识别图片文本...
[14:33:17] 初始化 EasyOCR...
```

## 问题原因
EasyOCR在打包后的exe文件中经常出现以下问题：
1. **模型下载卡住** - 无法下载OCR模型文件
2. **初始化超时** - 模型加载过程卡住
3. **依赖缺失** - 某些必要的模块未正确打包
4. **网络问题** - 模型下载需要网络连接

## 解决方案

### 方案1：使用修复后的OCR函数（推荐）
我已经创建了修复后的OCR函数，包含：
- 超时保护机制
- 多引擎备用方案
- 错误处理优化

**文件**: `ocr_fixed_functions.py`

**使用方法**:
```python
from ocr_fixed_functions import extract_text_with_ocr_fixed

# 替换原有的OCR调用
result = extract_text_with_ocr_fixed(image_path, self._log)
```

### 方案2：使用pytesseract替代
pytesseract更稳定，不会出现卡住问题：

```python
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
```

### 方案3：EasyOCR超时保护
如果必须使用EasyOCR，添加超时保护：

```python
def _extract_text_with_ocr(self, image_path: Path) -> Optional[str]:
    """使用 EasyOCR 识别图片文本（带超时保护）"""
    try:
        import easyocr
        import cv2
        import threading
        import queue
        
        self._log("初始化 EasyOCR (带超时保护)...")
        
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
```

## 构建修复

### 使用OCR修复版工作流
我已经创建了专门的GitHub Actions工作流：
`.github/workflows/build-windows-exe-ocr-fixed.yml`

**特点**:
- 包含所有OCR相关模块
- 添加超时保护机制
- 多引擎备用方案
- 优化依赖管理

### 手动构建修复
如果手动构建，添加以下参数：

```bash
pyinstaller --onefile --windowed --name=FileRenamer --clean \
  --hidden-import=pytesseract \
  --hidden-import=PIL \
  --hidden-import=cv2 \
  --hidden-import=easyocr \
  --hidden-import=threading \
  --hidden-import=queue \
  --collect-all=pytesseract \
  --collect-all=PIL \
  --collect-all=cv2 \
  --collect-all=easyocr \
  file_renamer_gui.py
```

## 测试验证

### 运行OCR测试脚本
```bash
python ocr_fix.py
python ocr_fixed_functions.py
```

### 检查OCR引擎
脚本会自动测试：
1. pytesseract
2. EasyOCR（带超时保护）
3. OpenCV基础处理

## 最佳实践

### 推荐配置
1. **主要OCR引擎**: pytesseract（稳定、快速）
2. **备用引擎**: EasyOCR（带超时保护）
3. **禁用模型下载**: 避免网络问题
4. **设置超时时间**: 30-60秒

### 环境变量设置
```python
# 避免EasyOCR下载模型
os.environ['EASYOCR_MODULE_PATH'] = os.path.join(os.path.dirname(__file__), 'easyocr_models')
os.environ['EASYOCR_DOWNLOAD_ENABLED'] = 'false'
```

### 错误处理
- 添加超时机制
- 实现多引擎备用
- 记录详细日志
- 优雅降级处理

## 故障排除

### 常见问题
1. **pytesseract未安装**: `pip install pytesseract`
2. **tesseract-ocr缺失**: 需要安装系统级tesseract
3. **PIL模块错误**: `pip install pillow`
4. **OpenCV问题**: `pip install opencv-python`

### 调试方法
1. 检查日志输出
2. 测试单个OCR引擎
3. 验证模块导入
4. 检查文件路径

## 总结

EasyOCR卡住问题主要通过以下方式解决：
1. **使用pytesseract替代** - 更稳定可靠
2. **添加超时保护** - 避免无限等待
3. **多引擎备用** - 提高成功率
4. **优化构建配置** - 确保模块完整

推荐使用修复后的OCR函数和专门的构建工作流，这样可以彻底解决OCR卡住问题。
