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

#### 问题：PyInstaller构建失败 (Exit code 1)
**可能原因**：
- 优化参数过于激进
- 某些exclude-module参数不兼容
- 依赖包冲突

**解决方案**：
1. 使用渐进式构建策略
2. 先确保基础构建成功
3. 逐步添加优化参数

#### 问题：PowerShell语法错误
```
ParserError: Missing expression after unary operator '--'
```

**解决方案**：
- 已修复：使用单行命令格式
- 避免Unix风格的反斜杠换行
- 使用PowerShell兼容的语法

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
1. **build-windows-exe-progressive.yml** - Windows渐进式优化构建（已验证成功）
2. **build-macos-app.yml** - macOS优化构建

### 配置特点
- ✅ 使用稳定的runner标签
- ✅ 启用pip缓存加速
- ✅ 30分钟超时保护
- ✅ 渐进式优化策略
- ✅ 自动文件大小检查
- ✅ PowerShell语法兼容

## 🎯 渐进式构建策略

### 为什么使用渐进式构建？
- **基础构建成功**：确保基本环境正常
- **逐步优化**：避免一次性添加过多参数导致失败
- **问题定位**：容易找到导致失败的特定参数

### 构建级别
1. **Level 1**: 基础排除（numpy, pandas, matplotlib, scipy, sklearn）
2. **Level 2**: ML/AI排除（tensorflow, torch, cv2, opencv, rapidocr）
3. **Level 3**: 完全排除（所有不必要的模块）

## 📋 故障排除步骤

### 步骤1：检查构建日志
1. 访问GitHub Actions页面
2. 查看失败的构建
3. 分析错误信息

### 步骤2：本地测试
```bash
# 安装依赖
pip install -r requirements_gui.txt

# 测试基本构建
pyinstaller --onefile --windowed file_renamer_gui.py

# 运行诊断脚本
python debug_windows_build.py
```

### 步骤3：使用渐进式构建
如果优化构建失败，使用渐进式构建：
1. 先运行基础构建确保成功
2. 再运行渐进式构建逐步优化
3. 观察每个级别的构建结果

### 步骤4：检查依赖
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
- ✅ 渐进式优化策略
- ✅ 使用稳定的runner标签
- ✅ PowerShell语法兼容

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
- 删除了冗余的 `build-windows-exe.yml` 和 `build-windows-exe-basic.yml`
- 保留了最优化和稳定的工作流
- 添加了渐进式构建策略
- 统一了Windows和macOS的构建配置
- 添加了超时保护和pip缓存优化
- 修复了PowerShell语法问题

### Windows构建问题解决
- ✅ 基础构建已成功验证
- ✅ 优化构建使用渐进式策略
- ✅ 添加了详细的错误处理和日志
- ✅ 提供了多种构建选项
- ✅ 修复了PowerShell语法问题

### 配置简化
- ✅ 删除了功能重复的工作流
- ✅ 保留了最核心的构建配置
- ✅ 减少了维护复杂度
- ✅ 提高了构建成功率
