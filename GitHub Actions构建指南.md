# GitHub Actions构建指南

## 概述
本项目提供了多个GitHub Actions工作流来构建Windows exe文件，专门解决了pyparsing包缺失的问题。

## 可用的工作流

### 1. 修复版构建 (推荐)
**文件**: `.github/workflows/build-windows-exe-fixed.yml`

**特点**:
- 专门解决pyparsing包缺失问题
- 使用修复后的spec文件
- 强制安装必要的依赖包
- 构建过程简单可靠

**触发方式**:
- 推送到main分支
- 创建Pull Request
- 手动触发 (workflow_dispatch)

### 2. 渐进式优化构建
**文件**: `.github/workflows/build-windows-exe-progressive.yml`

**特点**:
- 三级渐进式优化
- 自动排除不必要的模块
- 已集成pyparsing修复
- 生成更小的exe文件

**构建级别**:
- Level 1: 基础排除 (numpy, pandas等)
- Level 2: ML/AI模块排除 (tensorflow, torch等)
- Level 3: 强制包含requests相关模块

## 使用方法

### 自动构建
1. 推送代码到main分支
2. GitHub Actions自动触发构建
3. 在Actions标签页查看构建进度
4. 构建完成后下载exe文件

### 手动构建
1. 进入GitHub仓库
2. 点击Actions标签页
3. 选择对应的工作流
4. 点击"Run workflow"
5. 选择分支并运行

## 构建产物

### 文件下载
- **EXE文件**: 位于`dist/FileRenamer.exe`
- **构建报告**: 包含构建信息和文件大小
- **构建信息**: JSON格式的详细构建数据

### 文件大小
- 基础版本: 通常50-100MB
- 优化版本: 通常30-80MB
- 具体大小取决于包含的模块

## 故障排除

### 常见问题

#### 1. pyparsing包缺失
**错误信息**:
```
ImportError: The 'pyparsing' package is required
```

**解决方案**:
- 使用修复版构建工作流
- 确保spec文件包含正确的hiddenimports
- 检查依赖包是否正确安装

#### 2. 构建失败
**可能原因**:
- 依赖包版本冲突
- Python版本不兼容
- 内存不足

**解决方案**:
- 检查构建日志
- 更新依赖包版本
- 使用更小的构建配置

#### 3. 文件过大
**解决方案**:
- 使用渐进式优化构建
- 排除不必要的模块
- 使用UPX压缩

## 本地测试

### 在macOS上测试构建脚本
```bash
# 运行GitHub Actions专用构建脚本
python build_github_actions.py

# 运行快速修复脚本
python quick_fix.py

# 运行完整修复脚本
python build_fixed.py
```

### 验证构建结果
```bash
# 检查文件是否存在
ls -la dist/

# 检查文件大小
du -h dist/FileRenamer.exe

# 查看构建信息
cat build_info.json
```

## 配置优化

### 自定义构建参数
在`.github/workflows/`目录下的yml文件中修改:

```yaml
# 修改Python版本
python-version: '3.11'

# 修改超时时间
timeout-minutes: 30

# 添加更多依赖
pip install additional-package
```

### 环境变量
```yaml
env:
  PYTHONPATH: ${{ github.workspace }}
  BUILD_TYPE: production
```

## 最佳实践

1. **定期更新依赖**: 保持依赖包版本最新
2. **使用缓存**: 启用pip缓存加速构建
3. **并行构建**: 可以同时运行多个工作流
4. **监控构建**: 设置构建失败通知
5. **版本管理**: 为每个构建添加版本标签

## 技术支持

如果遇到问题:
1. 检查GitHub Actions构建日志
2. 查看构建报告和错误信息
3. 尝试使用不同的构建工作流
4. 检查依赖包兼容性

## 更新日志

- **v1.0**: 基础构建工作流
- **v1.1**: 添加pyparsing修复
- **v1.2**: 渐进式优化构建
- **v1.3**: GitHub Actions专用脚本
