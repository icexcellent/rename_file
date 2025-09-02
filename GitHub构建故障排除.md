# GitHub Actions 构建故障排除指南

## 🚨 常见问题及解决方案

### 1. Windows构建失败

#### 问题：Runner标签迁移警告
```
The windows-latest label will migrate from Windows Server 2022 to Windows Server 2025 beginning September 2, 2025
```

**解决方案**：
- 已修复：使用具体的Windows版本标签：`runs-on: windows-2022`
- 避免使用 `windows-latest` 标签

#### 问题：PyInstaller构建失败
**可能原因**：
- Python版本不兼容
- 依赖安装失败
- 权限问题

**解决方案**：
1. 检查Python版本（推荐3.11+）
2. 确保所有依赖正确安装
3. 查看构建日志获取详细错误信息

### 2. macOS构建失败

#### 问题：UPX安装失败
**解决方案**：
- 确保使用 `macos-latest` runner
- 检查brew是否可用

#### 问题：权限问题
**解决方案**：
- 检查文件权限
- 确保工作目录正确

## 🔧 当前构建配置

### 已优化的工作流
1. **build-windows-exe.yml** - Windows优化构建
2. **build-macos-app.yml** - macOS优化构建

### 配置特点
- ✅ 使用稳定的runner标签
- ✅ 启用pip缓存加速
- ✅ 30分钟超时保护
- ✅ 完整的瘦身优化
- ✅ 自动文件大小检查

## 📋 故障排除步骤

### 步骤1：检查构建日志
1. 访问GitHub Actions页面
2. 查看失败的构建
3. 分析错误信息

### 步骤2：本地测试
```bash
# 安装依赖
pip install -r requirements_gui.txt

# 测试PyInstaller
pyinstaller --onefile --windowed file_renamer_gui.py
```

### 步骤3：检查依赖
```bash
# 查看已安装的包
pip list

# 检查特定包
pip show PyQt6
pip show pytesseract
```

## 🎯 构建优化状态

### 已实现的优化
- ✅ 移除未使用的依赖 (rapidocr-onnxruntime)
- ✅ 排除不必要的Python模块
- ✅ 启用PyInstaller优化 (--strip, --optimize=2)
- ✅ 启用UPX压缩 (macOS)
- ✅ 使用稳定的runner标签

### 预期效果
- **原大小**: ~500MB
- **优化后**: 100-200MB
- **减少幅度**: 60-80%

## 📞 获取帮助

### 检查项目状态
- 查看 [Actions页面](https://github.com/icexcellent/rename_file/actions)
- 检查构建日志和错误信息

### 常见错误代码
- **Exit code 1**: 通常表示构建失败
- **Exit code 2**: 通常表示配置错误
- **Exit code 127**: 通常表示命令未找到

### 联系支持
1. 查看构建日志获取详细错误信息
2. 在GitHub Issues中报告问题
3. 提供完整的错误日志和配置信息

## 🔄 工作流更新历史

### 最新更新
- 删除了冗余的 `windows-build.yml` 和 `build-windows-exe-simple.yml`
- 保留了最优化和稳定的两个工作流
- 统一了Windows和macOS的构建配置
- 添加了超时保护和pip缓存优化
