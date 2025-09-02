# GitHub Actions 构建故障排除指南

## 🚨 常见问题及解决方案

### 1. Windows构建失败

#### 问题：Runner标签迁移警告
```
The windows-latest label will migrate from Windows Server 2022 to Windows Server 2025 beginning September 2, 2025
```

**解决方案**：
- 使用具体的Windows版本标签：`runs-on: windows-2022`
- 避免使用 `windows-latest` 标签

#### 问题：PyInstaller构建失败
**可能原因**：
- Python版本不兼容
- 依赖安装失败
- 权限问题

**解决方案**：
1. 检查Python版本（推荐3.11+）
2. 确保所有依赖正确安装
3. 使用简化的构建配置进行测试

### 2. macOS构建失败

#### 问题：UPX安装失败
**解决方案**：
- 确保使用 `macos-latest` runner
- 检查brew是否可用

#### 问题：权限问题
**解决方案**：
- 检查文件权限
- 确保工作目录正确

## 🔧 构建配置优化

### 推荐配置

#### Windows (稳定版)
```yaml
runs-on: windows-2022
python-version: '3.11'
```

#### macOS (稳定版)
```yaml
runs-on: macos-latest
python-version: '3.11'
```

### 构建策略

#### 策略1：渐进式优化
1. 先使用简单配置确保构建成功
2. 逐步添加优化参数
3. 测试每个优化步骤

#### 策略2：双配置
- 保留一个简单配置作为备用
- 使用优化配置进行瘦身构建

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

### 步骤3：简化配置
使用最基础的PyInstaller命令：
```bash
pyinstaller --onefile --windowed file_renamer_gui.py
```

### 步骤4：逐步添加优化
```bash
# 添加基本优化
pyinstaller --onefile --windowed --clean file_renamer_gui.py

# 添加模块排除
pyinstaller --onefile --windowed --clean \
  --exclude-module=numpy \
  --exclude-module=pandas \
  file_renamer_gui.py
```

## 🎯 当前配置状态

### 已配置的工作流
1. **build-windows-exe.yml** - 完整优化配置
2. **build-windows-exe-simple.yml** - 简化配置（备用）
3. **build-macos-app.yml** - macOS优化配置

### 建议使用顺序
1. 先测试简化配置确保基本构建成功
2. 成功后再使用优化配置进行瘦身
3. 如果优化配置失败，回退到简化配置

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
