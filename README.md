# 🚀 FileRenamer - 智能文件重命名工具

一个基于Python和PyQt6的智能文件重命名工具，支持OCR文字识别和AI智能重命名。

## ✨ 主要功能

- 🔍 **OCR文字识别**: 支持中文和英文图片文字识别
- 🤖 **AI智能重命名**: 集成DeepSeek API，智能生成文件名
- 📁 **多格式支持**: 支持PDF、图片、文档等多种文件格式
- 🎨 **现代化界面**: 基于PyQt6的直观用户界面
- 🌍 **跨平台**: 支持Windows、macOS、Linux

## 🛠️ 构建方法

### 🍎 macOS版本 (Docker构建)

```bash
# 进入macOS构建目录
cd build/macos

# 确保Docker已启动
./docker_build.sh
```

构建完成后，可执行文件将保存在项目根目录。

### 🐧 Linux版本 (Docker构建)

```bash
# 进入macOS构建目录（Linux版本也使用相同的构建脚本）
cd build/macos

# 确保Docker已启动
./docker_build.sh
```

### 🪟 Windows版本 (GitHub Actions)

Windows版本通过GitHub Actions自动构建：

1. **推送代码到main/master分支** - 自动触发构建
2. **手动触发构建** - 在GitHub仓库Actions页面手动运行
3. **下载构建产物** - 在Actions页面下载FileRenamer.exe

构建完成后，Windows EXE文件将作为GitHub Release发布。

## 📋 系统要求

### macOS/Linux
- Docker Desktop
- 至少4GB内存
- 支持ARM64/x64架构

### Windows
- Windows 10/11 (64位)
- 至少4GB内存
- 支持中文和英文OCR识别

## 🔧 依赖项

主要Python依赖：
- PyQt6 - GUI框架
- EasyOCR - OCR文字识别
- OpenCV - 图像处理
- PyMuPDF - PDF处理
- python-docx - Word文档处理

## 📁 项目结构

```
file_name_demo/
├── .github/workflows/       # GitHub Actions工作流
├── build/                   # 构建相关文件
│   └── macos/              # macOS构建文件
│       ├── Dockerfile      # Docker构建配置
│       ├── docker_build.sh # 构建脚本
│       ├── .dockerignore   # Docker忽略文件
│       └── README.md       # 构建说明
├── file_renamer_gui.py      # 主程序
├── deepseek_api_service.py  # AI服务
├── app_config.json          # 应用配置
├── config.json              # API配置
├── requirements.txt          # Python依赖
├── requirements_gui.txt      # GUI依赖
└── test_file/               # 测试文件
```

## 🚀 使用方法

1. **启动应用**: 双击可执行文件或运行Python脚本
2. **选择文件**: 点击"选择文件"按钮选择要重命名的文件
3. **OCR识别**: 对于图片文件，应用会自动进行OCR识别
4. **AI重命名**: 基于识别内容，AI会生成智能文件名
5. **确认重命名**: 查看生成的文件名并确认重命名

## 🔑 API配置

在`config.json`中配置你的DeepSeek API密钥：

```json
{
    "deepseek_api_key": "your_api_key_here",
    "description": "请将your_api_key_here替换为你的DeepSeek API密钥"
}
```

## 📝 许可证

本项目采用MIT许可证。

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

**注意**: Windows版本需要通过GitHub Actions构建，无法在macOS/Linux上直接构建Windows EXE。
