# FileRenamer 构建说明

## 🚀 自动构建

本项目已配置GitHub Actions自动构建，每次推送到main分支都会自动生成可执行文件。

### 构建状态
- **Windows EXE**: [![Build Windows](https://github.com/icexcellent/rename_file/workflows/Build%20Windows%20EXE/badge.svg)](https://github.com/icexcellent/rename_file/actions)
- **macOS App**: [![Build macOS](https://github.com/icexcellent/rename_file/workflows/Build%20macOS%20App/badge.svg)](https://github.com/icexcellent/rename_file/actions)

### 下载构建产物
1. 访问 [Actions页面](https://github.com/icexcellent/rename_file/actions)
2. 选择最新的构建
3. 下载对应的构建产物：
   - Windows: `FileRenamer-Windows` (FileRenamer.exe)
   - macOS: `FileRenamer-macOS` (FileRenamer)

## 🔧 本地构建

### 环境要求
- Python 3.11+
- PyInstaller 5.0+
- UPX压缩器 (macOS: `brew install upx`)

### 快速构建
```bash
# 使用优化脚本
python build_optimized.py
```

### 手动构建
```bash
# Windows
pyinstaller --onefile --windowed --name=FileRenamer \
  --clean --optimize=2 --strip \
  [排除模块参数...] \
  file_renamer_gui.py

# macOS
pyinstaller --onefile --windowed --name=FileRenamer \
  --clean --optimize=2 --strip --upx-dir=/usr/local/bin \
  [排除模块参数...] \
  file_renamer_gui.py
```

## 📦 瘦身优化

### 已实现的优化
- ✅ 移除未使用的依赖 (rapidocr-onnxruntime)
- ✅ 排除不必要的Python模块
- ✅ 启用PyInstaller优化 (--strip, --optimize=2)
- ✅ 启用UPX压缩 (macOS)

### 预期效果
- **原大小**: ~500MB
- **优化后**: 100-200MB
- **减少幅度**: 60-80%

## 🐛 故障排除

### 构建失败
1. 检查Python版本 (需要3.11+)
2. 确认所有依赖已安装
3. 查看GitHub Actions日志

### 程序无法运行
1. 检查excludes列表是否排除了必要模块
2. 确认hidden-imports包含所有必需依赖
3. 逐步减少excludes，找到问题模块

### 文件仍然过大
1. 检查是否有新的未使用依赖
2. 使用`pip list`查看已安装包
3. 考虑使用更轻量的替代方案

## 📋 依赖说明

### 核心依赖
- **PyQt6**: GUI框架 (必需，但较大)
- **pytesseract**: OCR引擎 (必需)
- **pypdf**: PDF处理 (必需)
- **python-docx**: Word文档处理 (必需)
- **chardet**: 编码检测 (必需)

### 可选依赖
- **tqdm**: 进度条显示
- **pdfplumber**: PDF文本提取增强

## 🔄 更新流程

1. 修改代码
2. 测试功能
3. 提交并推送
4. GitHub Actions自动构建
5. 下载新版本

## 📞 支持

如有问题，请：
1. 查看GitHub Actions构建日志
2. 检查Issues页面
3. 提交新的Issue描述问题
