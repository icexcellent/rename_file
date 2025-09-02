# FileRenamer - 智能文件重命名工具

## 项目简介
FileRenamer是一个基于Python的智能文件重命名工具，支持多种文件格式的智能识别和重命名。

## 功能特性
- **多格式支持**: PDF、图片、文档等
- **OCR识别**: 支持中英文文本识别
- **智能分析**: 基于AI的文件内容分析
- **批量处理**: 支持批量文件重命名
- **跨平台**: 支持Windows、macOS、Linux

## 技术架构
- **前端**: PyQt6 GUI界面
- **后端**: Python 3.11+
- **OCR引擎**: Tesseract + EasyOCR
- **AI服务**: DeepSeek API集成
- **构建工具**: PyInstaller + Docker

## 快速开始

### 使用Docker构建（推荐）

1. **确保Docker运行**
```bash
docker --version
```

2. **运行构建脚本**
```bash
chmod +x docker_build.sh
./docker_build.sh
```

3. **构建完成后**
- 可执行文件: `./FileRenamer`
- 支持跨平台运行

### 手动构建

1. **安装依赖**
```bash
pip install -r requirements.txt
pip install -r requirements_gui.txt
pip install pyinstaller
```

2. **构建应用**
```bash
pyinstaller --onefile --windowed --name=FileRenamer file_renamer_gui.py
```

## 项目结构
```
file_name_demo/
├── file_renamer_gui.py          # 主程序GUI
├── deepseek_api_service.py      # AI服务集成
├── requirements.txt              # 基础依赖
├── requirements_gui.txt          # GUI依赖
├── Dockerfile                    # Docker构建配置
├── docker_build.sh              # Docker构建脚本
├── .dockerignore                 # Docker忽略文件
├── test_file/                    # 测试文件目录
├── app_config.json              # 应用配置
└── config.json                  # 配置文件
```

## 依赖说明
- **PyQt6**: GUI框架
- **pytesseract**: OCR文本识别
- **opencv-python**: 图像处理
- **easyocr**: 深度学习OCR
- **requests**: HTTP客户端
- **PyInstaller**: 应用打包

## 构建说明
项目使用Docker容器化构建，确保：
- 环境一致性
- 依赖完整性
- 跨平台兼容性
- 构建稳定性

## 许可证
本项目仅供学习和研究使用。
