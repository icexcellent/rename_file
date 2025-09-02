# 智能文件重命名工具

一个基于 PyQt6 的智能文件重命名桌面应用，支持扫描件 OCR 识别和 DeepSeek AI 智能重命名。

## ✨ 主要功能

- **🔍 扫描件支持**：PDF 扫描件 → 图片转换 → OCR 识别 → AI 分析
- **🖼️ 图片文件处理**：直接 OCR 识别 → AI 分析
- **📄 多种文件格式**：PDF、图片、Word、文本文件等
- **🤖 AI 智能重命名**：基于 DeepSeek API 的智能分析
- **📝 实时日志监控**：完整的处理过程日志显示
- **🔄 批量处理**：支持文件夹批量重命名
- **📋 回滚功能**：支持重命名操作回滚

## 🚀 技术特性

- **OCR 引擎**：EasyOCR + OpenCV，支持中英文识别
- **PDF 处理**：PyMuPDF，支持扫描件转图片
- **AI 服务**：DeepSeek Chat API，智能内容分析
- **GUI 框架**：PyQt6，现代化桌面界面
- **跨平台**：支持 Windows、macOS、Linux

## 📦 安装依赖

```bash
pip install -r requirements.txt
pip install -r requirements_gui.txt
```

## 🎯 使用方法

1. 配置 DeepSeek API 密钥
2. 选择源文件或文件夹
3. 选择目标目录
4. 选择重命名或复制模式
5. 开始处理，实时监控进度

## 🔧 构建 Windows 可执行文件

项目已配置 GitHub Actions 自动构建：

1. 推送代码到 `main` 分支
2. GitHub Actions 自动触发构建
3. 在 Actions 页面下载生成的 `FileRenamer-windows.zip`

## 📁 项目结构

```
├── file_renamer_gui.py      # 主 GUI 应用
├── deepseek_api_service.py  # DeepSeek API 服务
├── requirements.txt         # 核心依赖
├── requirements_gui.txt     # GUI 依赖
├── config.json             # API 配置
├── app_config.json         # 应用配置
└── .github/workflows/      # GitHub Actions 配置
```

## 🎉 最新更新

- ✅ 修复 DeepSeek API 调用问题
- ✅ 完善扫描件 OCR 支持
- ✅ 优化 GitHub Actions 构建配置
- ✅ 增强错误处理和日志记录

## 📄 许可证

MIT License
智能重命名
