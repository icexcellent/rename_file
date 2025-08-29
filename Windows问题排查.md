# Windows可执行程序问题排查指南

## 🔍 常见问题及解决方案

### 问题1：程序无法启动

#### 症状
- 双击exe文件无反应
- 程序启动后立即关闭
- 显示"程序已停止工作"

#### 解决方案

**1. 以管理员身份运行**
```
右键点击 FileRenamer.exe
选择"以管理员身份运行"
```

**2. 检查杀毒软件**
- 将程序添加到杀毒软件白名单
- 临时关闭杀毒软件测试
- 在Windows Defender中添加排除项

**3. 安装Visual C++ Redistributable**
```
下载并安装：
https://aka.ms/vs/17/release/vc_redist.x64.exe
```

**4. 检查Windows版本兼容性**
- 确保Windows 10或更高版本
- 更新Windows到最新版本

### 问题2：缺少DLL文件

#### 症状
- 错误信息："找不到xxx.dll"
- "应用程序无法正常启动(0xc000007b)"

#### 解决方案

**1. 安装Visual C++ Redistributable**
```
x64版本：https://aka.ms/vs/17/release/vc_redist.x64.exe
x86版本：https://aka.ms/vs/17/release/vc_redist.x86.exe
```

**2. 安装.NET Framework**
```
下载并安装最新版本的.NET Framework
```

**3. 检查系统架构**
- 确保下载的版本与系统架构匹配
- 64位系统使用x64版本

### 问题3：权限错误

#### 症状
- "拒绝访问"
- "权限不足"
- 无法创建或修改文件

#### 解决方案

**1. 以管理员身份运行**
```
右键点击exe文件 → 以管理员身份运行
```

**2. 修改文件夹权限**
```
右键点击目标文件夹 → 属性 → 安全 → 编辑
添加当前用户的完全控制权限
```

**3. 选择有权限的目录**
- 使用桌面或文档文件夹
- 避免使用系统保护目录

### 问题4：程序启动缓慢

#### 症状
- 首次启动需要很长时间
- 程序响应缓慢

#### 解决方案

**1. 等待首次启动完成**
- 首次启动需要解压和初始化
- 耐心等待，不要强制关闭

**2. 检查磁盘空间**
- 确保有足够的磁盘空间
- 清理临时文件

**3. 关闭其他程序**
- 释放内存和CPU资源
- 关闭不必要的后台程序

### 问题5：界面显示异常

#### 症状
- 界面元素显示不完整
- 按钮无法点击
- 文字显示异常

#### 解决方案

**1. 检查显示设置**
- 调整显示缩放比例
- 确保分辨率足够

**2. 更新显卡驱动**
- 下载最新显卡驱动
- 重启计算机

**3. 使用兼容模式**
```
右键点击exe → 属性 → 兼容性
选择"以兼容模式运行此程序"
```

## 🛠️ 系统要求检查

### 最低要求
- **操作系统**：Windows 10 (版本 1903 或更高)
- **处理器**：1 GHz 或更快
- **内存**：4 GB RAM
- **存储空间**：500 MB 可用空间
- **网络**：互联网连接（用于API调用）

### 推荐配置
- **操作系统**：Windows 11
- **处理器**：2 GHz 或更快
- **内存**：8 GB RAM
- **存储空间**：1 GB 可用空间
- **网络**：稳定的互联网连接

## 🔧 重新打包步骤

如果问题持续存在，可以尝试重新打包：

### 1. 环境准备
```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
.venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
pip install -r requirements_gui.txt
pip install pyinstaller
```

### 2. 使用Windows专用脚本
```bash
# 运行Windows打包脚本
python build_windows.py
```

### 3. 使用spec文件
```bash
# 使用spec文件打包
pyinstaller FileRenamer.spec
```

### 4. 手动打包命令
```bash
pyinstaller --onefile --windowed --name=FileRenamer --hidden-import=PyQt6.QtCore --hidden-import=PyQt6.QtWidgets --hidden-import=PyQt6.QtGui --hidden-import=pytesseract --hidden-import=pypdf --hidden-import=docx --hidden-import=chardet --hidden-import=requests --hidden-import=json --hidden-import=pathlib --hidden-import=shutil --hidden-import=datetime --hidden-import=re --hidden-import=base64 --hidden-import=PIL --hidden-import=PIL.Image --hidden-import=pdfplumber file_renamer_gui.py
```

## 📋 测试步骤

### 1. 基本功能测试
1. 启动程序
2. 检查界面是否正常显示
3. 测试文件选择功能
4. 测试配置选项

### 2. 重命名功能测试
1. 选择测试文件
2. 设置目标目录
3. 执行重命名操作
4. 检查结果

### 3. 错误处理测试
1. 测试无效文件路径
2. 测试权限不足情况
3. 测试网络连接问题

## 📞 获取帮助

如果问题仍然存在，请提供以下信息：

### 系统信息
- Windows版本和构建号
- 系统架构（32位/64位）
- 可用内存和磁盘空间

### 错误信息
- 完整的错误消息
- 错误发生时的操作步骤
- 错误截图

### 环境信息
- 是否以管理员身份运行
- 杀毒软件类型和版本
- 是否安装了Visual C++ Redistributable

## ✅ 成功运行的标志

当程序正常运行时，你应该看到：

1. **程序启动**：双击exe文件后程序正常启动
2. **界面显示**：主界面正常显示，所有按钮可见
3. **功能正常**：文件选择、配置、重命名等功能正常
4. **无错误提示**：没有错误对话框或异常信息

---

**注意**：如果按照以上步骤仍然无法解决问题，可能需要检查具体的错误信息或系统环境配置。
