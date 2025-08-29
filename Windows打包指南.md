# Windows打包快速指南

## 🚀 快速开始

### 1. 环境准备
```cmd
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
.venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
pip install -r requirements_gui.txt
pip install pyinstaller
```

### 2. 打包应用
```cmd
# 方法1：使用Windows专用脚本（推荐）
python build_windows.py

# 方法2：使用spec文件
pyinstaller FileRenamer.spec

# 方法3：直接命令
pyinstaller --onefile --windowed --name=FileRenamer file_renamer_gui.py
```

### 3. 检查结果
```cmd
# 检查生成的文件
dir dist\

# 应该看到 FileRenamer.exe
```

## 📋 打包选项说明

### 基本选项
- `--onefile`: 打包成单个exe文件
- `--windowed`: 无控制台窗口
- `--name=FileRenamer`: 指定可执行文件名

### 重要隐藏导入
```cmd
--hidden-import=PyQt6.QtCore
--hidden-import=PyQt6.QtWidgets
--hidden-import=PyQt6.QtGui
--hidden-import=pytesseract
--hidden-import=pypdf
--hidden-import=docx
--hidden-import=chardet
--hidden-import=requests
--hidden-import=json
--hidden-import=pathlib
--hidden-import=shutil
--hidden-import=datetime
--hidden-import=re
--hidden-import=base64
--hidden-import=PIL
--hidden-import=PIL.Image
--hidden-import=pdfplumber
```

## 🔧 常见问题解决

### 问题1：打包失败
**解决方案**：
```cmd
# 清理缓存
pyinstaller --clean

# 重新安装PyInstaller
pip uninstall pyinstaller
pip install pyinstaller
```

### 问题2：缺少模块
**解决方案**：
```cmd
# 添加缺失的隐藏导入
--hidden-import=模块名

# 或者使用--collect-all
--collect-all=模块名
```

### 问题3：文件太大
**解决方案**：
```cmd
# 使用UPX压缩（需要安装UPX）
--upx-dir=path\to\upx

# 排除不需要的模块
--exclude-module=模块名
```

## 📦 优化建议

### 1. 减小文件大小
```cmd
# 排除不需要的模块
--exclude-module=matplotlib
--exclude-module=numpy
--exclude-module=scipy

# 使用UPX压缩
--upx-dir=C:\upx
```

### 2. 提高启动速度
```cmd
# 使用onedir模式（文件更小，启动更快）
--onedir

# 或者使用--runtime-tmpdir
--runtime-tmpdir=temp
```

### 3. 添加图标
```cmd
# 添加应用图标
--icon=icon.ico
```

## 🧪 测试验证

### 1. 基本功能测试
```cmd
# 启动程序
FileRenamer.exe

# 检查是否能正常显示界面
# 测试文件选择功能
# 测试配置选项
```

### 2. 重命名功能测试
```cmd
# 选择测试文件
# 设置目标目录
# 执行重命名操作
# 检查结果
```

### 3. 错误处理测试
```cmd
# 测试无效文件路径
# 测试权限不足情况
# 测试网络连接问题
```

## 📁 文件结构

打包后的文件结构：
```
dist/
└── FileRenamer.exe    # Windows可执行文件
```

## ⚠️ 注意事项

### 1. 系统要求
- Windows 10 或更高版本
- 至少 4GB 内存
- 至少 500MB 磁盘空间

### 2. 依赖要求
- Visual C++ Redistributable
- .NET Framework（如果需要）

### 3. 安全设置
- 可能被杀毒软件误报
- 需要添加到白名单
- 可能需要以管理员身份运行

## 🎯 部署建议

### 1. 分发方式
- 直接分发exe文件
- 打包成zip压缩包
- 创建安装程序

### 2. 用户指南
- 提供使用说明
- 包含故障排除指南
- 说明系统要求

### 3. 版本管理
- 记录版本号
- 保存打包配置
- 维护更新日志

---

**快速命令总结**：
```cmd
# 一键打包
python build_windows.py

# 手动打包
pyinstaller --onefile --windowed --name=FileRenamer file_renamer_gui.py

# 使用spec文件
pyinstaller FileRenamer.spec
```
