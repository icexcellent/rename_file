# OCR编译问题解决指南

## 问题描述
在GitHub Actions构建过程中遇到编译错误：
```
error: command 'C:\\Program Files\\Microsoft Visual Studio\\2022\\Enterprise\\VC\\Tools\\MSVC\\14.44.35207\\bin\\HostX86\\x64\\cl.exe' failed with exit code 2
note: This error originates from a subprocess, and is likely not a problem with pip.
ERROR: Failed building wheel for tesseract-ocr
Failed to build tesseract-ocr
error: failed-wheel-build-for-install
```

## 问题原因
`tesseract-ocr`包需要C++编译器来构建，在GitHub Actions环境中：
1. **缺少C++编译器** - 需要Visual Studio Build Tools
2. **依赖复杂** - 包含大量C++代码需要编译
3. **构建时间长** - 编译过程耗时且容易失败
4. **平台限制** - Windows环境编译更复杂

## 解决方案

### 方案1：使用简化版工作流（推荐）
我已经创建了专门的工作流来避免编译问题：
`.github/workflows/build-windows-exe-ocr-simple.yml`

**特点**:
- 只安装预编译的包（pillow, opencv-python）
- 避免需要编译的包（tesseract-ocr, easyocr）
- 使用基本的图像处理功能
- 构建稳定，不会出现编译错误

### 方案2：使用系统级tesseract
如果确实需要完整的OCR功能：

1. **在GitHub Actions中安装预编译的tesseract**:
```yaml
- name: Install pre-built tesseract
  run: |
    # 下载预编译的tesseract
    Invoke-WebRequest -Uri "https://github.com/UB-Mannheim/tesseract/releases/download/v5.3.1.20230401/tesseract-ocr-w64-setup-5.3.1.20230401.exe" -OutFile "tesseract-installer.exe"
    # 静默安装
    Start-Process -FilePath "tesseract-installer.exe" -ArgumentList "/S" -Wait
    # 添加到PATH
    $env:PATH += ";C:\Program Files\Tesseract-OCR"
```

2. **只安装Python包装器**:
```yaml
- name: Install Python OCR packages
  run: |
    pip install pytesseract pillow opencv-python
    # 不安装tesseract-ocr包，使用系统级安装
```

### 方案3：使用Docker环境
创建自定义Docker镜像，预装所有依赖：

```dockerfile
FROM python:3.11-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-chi-sim \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装Python包
COPY requirements.txt .
RUN pip install -r requirements.txt

# 设置工作目录
WORKDIR /app
COPY . .

# 构建命令
CMD ["pyinstaller", "--onefile", "--windowed", "file_renamer_gui.py"]
```

## 推荐的构建策略

### 1. 简化版构建（稳定）
```bash
pyinstaller --onefile --windowed --name=FileRenamer --clean \
  --hidden-import=PIL \
  --hidden-import=PIL.Image \
  --hidden-import=cv2 \
  --exclude-module=easyocr \
  --exclude-module=tesseract-ocr \
  file_renamer_gui.py
```

### 2. 完整版构建（需要预编译环境）
```bash
# 先安装系统级tesseract
# 然后构建
pyinstaller --onefile --windowed --name=FileRenamer --clean \
  --hidden-import=pytesseract \
  --hidden-import=PIL \
  --hidden-import=cv2 \
  --hidden-import=easyocr \
  file_renamer_gui.py
```

## 当前可用的工作流

### 1. OCR简化版（推荐）
- **文件**: `.github/workflows/build-windows-exe-ocr-simple.yml`
- **特点**: 避免编译问题，构建稳定
- **功能**: 基本图像处理，无复杂OCR

### 2. OCR完整版
- **文件**: `.github/workflows/build-windows-exe-ocr-fixed.yml`
- **特点**: 包含完整OCR功能
- **问题**: 可能遇到编译错误

### 3. 基础修复版
- **文件**: `.github/workflows/build-windows-exe-fixed.yml`
- **特点**: 只修复pyparsing问题
- **功能**: 基础功能，无OCR

## 使用建议

### 立即使用
选择**OCR简化版工作流**：
1. 在GitHub Actions页面选择"Build Windows EXE (OCR Simple)"
2. 这个工作流专门避免编译问题
3. 构建稳定，不会出现编译错误

### 长期规划
如果需要完整OCR功能：
1. 使用Docker环境构建
2. 预装系统级tesseract
3. 创建自定义构建镜像

## 故障排除

### 如果仍然遇到编译问题
1. **检查包版本**: 使用兼容的包版本
2. **排除问题包**: 使用`--exclude-module`排除
3. **使用预编译包**: 优先选择wheel包
4. **简化依赖**: 只包含必要的模块

### 调试方法
1. 查看构建日志中的具体错误
2. 逐个测试包的安装
3. 使用虚拟环境隔离依赖
4. 检查包的兼容性

## 总结

OCR编译问题主要通过以下方式解决：
1. **使用简化版工作流** - 避免编译，确保构建成功
2. **预装系统级依赖** - 使用预编译的二进制文件
3. **排除问题包** - 使用`--exclude-module`参数
4. **Docker环境** - 创建预配置的构建环境

**推荐使用OCR简化版工作流**，这样可以确保构建成功，避免编译错误，同时保持基本的图像处理功能。
