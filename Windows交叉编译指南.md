# Windows交叉编译指南

## 🔍 问题分析

在macOS上构建的Windows可执行程序无法在Windows上运行，这是因为：

1. **平台差异**：macOS和Windows使用不同的可执行文件格式
2. **依赖库差异**：两个平台的系统库和依赖不同
3. **架构差异**：macOS ARM64 vs Windows x64

## 🛠️ 解决方案

### 方案1：在Windows上构建（推荐）

#### 1. 准备Windows环境
```cmd
# 在Windows机器上
# 1. 安装Python 3.8+
# 2. 创建虚拟环境
python -m venv .venv

# 3. 激活虚拟环境
.venv\Scripts\activate

# 4. 安装依赖
pip install -r requirements.txt
pip install -r requirements_gui.txt
pip install pyinstaller
```

#### 2. 在Windows上构建
```cmd
# 使用Windows专用脚本
python build_windows.py

# 或使用spec文件
pyinstaller FileRenamer.spec

# 或直接命令
pyinstaller --onefile --windowed --name=FileRenamer file_renamer_gui.py
```

### 方案2：使用Docker交叉编译

#### 1. 创建Dockerfile
```dockerfile
FROM python:3.11-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 安装PyInstaller
RUN pip install pyinstaller

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 安装Python依赖
RUN pip install -r requirements.txt
RUN pip install -r requirements_gui.txt

# 构建Windows可执行文件
RUN pyinstaller --onefile --windowed --name=FileRenamer \
    --hidden-import=PyQt6.QtCore \
    --hidden-import=PyQt6.QtWidgets \
    --hidden-import=PyQt6.QtGui \
    --hidden-import=pytesseract \
    --hidden-import=pypdf \
    --hidden-import=docx \
    --hidden-import=chardet \
    --hidden-import=requests \
    --hidden-import=json \
    --hidden-import=pathlib \
    --hidden-import=shutil \
    --hidden-import=datetime \
    --hidden-import=re \
    --hidden-import=base64 \
    --hidden-import=PIL \
    --hidden-import=PIL.Image \
    --hidden-import=pdfplumber \
    file_renamer_gui.py

# 输出目录
VOLUME /app/dist
```

#### 2. 构建Docker镜像
```bash
# 构建镜像
docker build -t file-renamer-builder .

# 运行容器并挂载输出目录
docker run -v $(pwd)/dist:/app/dist file-renamer-builder
```

### 方案3：使用虚拟机

#### 1. 安装Windows虚拟机
- 使用VirtualBox或VMware
- 安装Windows 10/11
- 安装Python和依赖

#### 2. 在虚拟机中构建
```cmd
# 在Windows虚拟机中
# 按照方案1的步骤进行
```

### 方案4：使用GitHub Actions

#### 1. 创建GitHub Actions工作流
```yaml
name: Build Windows Executable

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements_gui.txt
        pip install pyinstaller
    
    - name: Build executable
      run: |
        pyinstaller --onefile --windowed --name=FileRenamer file_renamer_gui.py
    
    - name: Upload artifact
      uses: actions/upload-artifact@v2
      with:
        name: FileRenamer-Windows
        path: dist/FileRenamer.exe
```

## 🔧 优化建议

### 1. 减小文件大小
```cmd
# 排除不需要的模块
--exclude-module=matplotlib
--exclude-module=numpy
--exclude-module=scipy

# 使用UPX压缩
--upx-dir=path\to\upx
```

### 2. 提高兼容性
```cmd
# 添加兼容性选项
--win-private-assemblies
--win-no-prefer-redirects
```

### 3. 添加图标和版本信息
```cmd
# 添加图标
--icon=icon.ico

# 添加版本信息
--version-file=version.txt
```

## 📋 测试验证

### 1. 在Windows上测试
```cmd
# 启动程序
FileRenamer.exe

# 检查功能
# - 界面显示
# - 文件选择
# - 重命名功能
# - 配置保存
```

### 2. 兼容性测试
- Windows 10 (64位)
- Windows 11 (64位)
- 不同分辨率
- 不同DPI设置

### 3. 性能测试
- 启动时间
- 内存使用
- 文件处理速度

## 🚀 部署建议

### 1. 分发方式
- 直接分发exe文件
- 打包成zip压缩包
- 创建安装程序

### 2. 用户指南
- 提供详细使用说明
- 包含故障排除指南
- 说明系统要求

### 3. 版本管理
- 记录版本号
- 保存构建配置
- 维护更新日志

## ⚠️ 注意事项

### 1. 平台限制
- 只能在Windows上构建Windows可执行文件
- macOS构建的文件无法在Windows上运行
- 需要确保所有依赖都兼容Windows

### 2. 依赖管理
- 确保所有依赖都有Windows版本
- 检查第三方库的兼容性
- 处理平台特定的代码

### 3. 测试要求
- 必须在Windows环境中测试
- 测试不同的Windows版本
- 验证所有功能正常工作

---

**总结**：要在Windows上运行，必须在Windows平台上构建。建议使用方案1（在Windows上构建）或方案4（GitHub Actions自动化构建）。
