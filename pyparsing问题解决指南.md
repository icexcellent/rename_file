# pyparsing包缺失问题解决指南

## 问题描述
在PyInstaller打包过程中遇到以下错误：
```
ImportError: The 'pyparsing' package is required; normally this is bundled with this package so if this warning, consult the packager of your distribution.
```

## 问题原因
PyInstaller在打包时没有正确包含`pyparsing`和`packaging`等依赖包，这些包是`pkg_resources`模块正常工作所必需的。

## 解决方案

### 方案1：快速修复（推荐）
运行快速修复脚本：
```bash
python quick_fix.py
```

这个脚本会自动：
1. 安装必要的依赖包
2. 清理构建文件
3. 重新构建可执行文件

### 方案2：手动修复
1. 安装必要的包：
```bash
pip install pyparsing packaging setuptools --upgrade
```

2. 清理构建文件：
```bash
rm -rf build dist __pycache__
```

3. 重新构建：
```bash
python -m PyInstaller --clean FileRenamer.spec
```

### 方案3：使用修复后的spec文件
我已经修改了`FileRenamer.spec`文件，添加了必要的`hiddenimports`。现在可以直接使用：
```bash
python -m PyInstaller FileRenamer.spec
```

## 修复内容
在spec文件中添加了以下隐藏导入：
- `pkg_resources`及其相关模块
- `pkg_resources.extern.pyparsing`
- `pkg_resources.extern.packaging`
- `pyparsing`
- `packaging`

## 验证修复
构建完成后，运行生成的可执行文件，应该不再出现`pyparsing`相关的错误。

## 如果问题仍然存在
如果上述方法仍然无法解决问题，可以尝试：
1. 使用`build_fixed.py`脚本进行更全面的修复
2. 检查Python环境是否有冲突
3. 尝试在虚拟环境中重新安装依赖

## 注意事项
- 确保在构建前清理了之前的构建文件
- 如果使用虚拟环境，确保在正确的环境中运行
- 某些情况下可能需要重新安装PyInstaller
