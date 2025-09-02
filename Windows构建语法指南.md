# Windows构建语法指南

## 🚨 PowerShell语法问题

### 问题描述
在Windows GitHub Actions中，使用反斜杠 `\` 进行多行命令会导致语法错误：
```
ParserError: Missing expression after unary operator '--'
```

### 原因分析
- **PowerShell不支持反斜杠换行**：`\` 在PowerShell中不是有效的换行符
- **Unix风格语法**：反斜杠换行是Unix/Linux shell的语法
- **Windows兼容性**：Windows PowerShell需要不同的语法

## ✅ 正确的PowerShell语法

### 方法1：单行命令（推荐）
```powershell
pyinstaller --onefile --windowed --name=FileRenamer --clean --exclude-module=numpy --exclude-module=pandas file_renamer_gui.py
```

### 方法2：使用反引号 `` ` ``（PowerShell换行符）
```powershell
pyinstaller --onefile --windowed --name=FileRenamer `
  --clean `
  --exclude-module=numpy `
  --exclude-module=pandas `
  file_renamer_gui.py
```

### 方法3：使用分号分隔
```powershell
pyinstaller --onefile --windowed --name=FileRenamer --clean; pyinstaller --exclude-module=numpy --exclude-module=pandas file_renamer_gui.py
```

## 🔧 已修复的配置文件

### 1. build-windows-exe.yml
- ✅ 使用单行命令格式
- ✅ 所有参数在一行内
- ✅ 兼容Windows PowerShell

### 2. build-windows-exe-progressive.yml
- ✅ 使用单行命令格式
- ✅ 三个级别的构建都使用单行
- ✅ 避免语法错误

### 3. build-windows-exe-basic.yml
- ✅ 使用单行命令格式
- ✅ 已验证成功

## 📋 构建配置最佳实践

### Windows构建
- 使用单行命令格式
- 避免反斜杠换行
- 测试PowerShell语法

### macOS/Linux构建
- 可以使用反斜杠换行
- 支持多行命令格式
- 更灵活的语法

### 跨平台兼容
- 为不同平台创建专门的配置
- 使用条件语法
- 测试所有平台

## 🎯 当前状态

### 已修复
- ✅ 渐进式构建配置
- ✅ 主Windows构建配置
- ✅ PowerShell语法问题

### 预期效果
- Windows构建应该成功
- 渐进式优化可以正常工作
- 文件大小逐步减少

## 💡 使用建议

1. **优先使用单行命令**：避免语法问题
2. **测试PowerShell语法**：在本地验证
3. **保持配置简单**：减少出错概率
4. **使用渐进式构建**：逐步验证优化效果

## 🐛 故障排除

### 如果仍然失败
1. 检查PowerShell语法
2. 验证命令参数
3. 查看构建日志
4. 使用基础构建作为备用

### 常见错误
- **ParserError**: PowerShell语法错误
- **Exit code 1**: 构建失败
- **Missing expression**: 参数格式问题
