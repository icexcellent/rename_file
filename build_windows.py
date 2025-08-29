#!/usr/bin/env python3
"""
Windows平台专用打包脚本
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def clean_output_directories():
    """清理输出目录"""
    print("清理输出目录...")
    
    # 清理dist和build目录
    for dir_name in ['dist', 'build']:
        if Path(dir_name).exists():
            import shutil
            shutil.rmtree(dir_name)
            print(f"✓ 清理 {dir_name} 目录")
    
    # 清理spec文件
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()
        print(f"✓ 删除 {spec_file}")

def build_windows_executable():
    """构建Windows可执行文件"""
    print("开始构建Windows可执行文件...")
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✓ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("✗ PyInstaller未安装")
        return False
    
    # 清理输出目录
    clean_output_directories()
    
    # 根据平台选择不同的构建参数
    if platform.system() == "Windows":
        # Windows平台
        build_cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--name=FileRenamer",
            "--hidden-import=PyQt6.QtCore",
            "--hidden-import=PyQt6.QtWidgets", 
            "--hidden-import=PyQt6.QtGui",
            "--hidden-import=pytesseract",
            "--hidden-import=pypdf",
            "--hidden-import=docx",
            "--hidden-import=chardet",
            "--hidden-import=requests",
            "--hidden-import=json",
            "--hidden-import=pathlib",
            "--hidden-import=shutil",
            "--hidden-import=datetime",
            "--hidden-import=re",
            "--hidden-import=base64",
            "--hidden-import=PIL",
            "--hidden-import=PIL.Image",
            "--hidden-import=pdfplumber",
            "file_renamer_gui.py"
        ]
    else:
        # macOS/Linux平台（用于交叉编译或测试）
        print("⚠ 检测到非Windows平台，使用兼容模式")
        build_cmd = [
            "pyinstaller",
            "--onefile",
            "--noconsole",
            "--name=FileRenamer",
            "--hidden-import=PyQt6.QtCore",
            "--hidden-import=PyQt6.QtWidgets", 
            "--hidden-import=PyQt6.QtGui",
            "--hidden-import=pytesseract",
            "--hidden-import=pypdf",
            "--hidden-import=docx",
            "--hidden-import=chardet",
            "--hidden-import=requests",
            "--hidden-import=json",
            "--hidden-import=pathlib",
            "--hidden-import=shutil",
            "--hidden-import=datetime",
            "--hidden-import=re",
            "--hidden-import=base64",
            "--hidden-import=PIL",
            "--hidden-import=PIL.Image",
            "--hidden-import=pdfplumber",
            "file_renamer_gui.py"
        ]
    
    print(f"执行命令: {' '.join(build_cmd)}")
    
    try:
        result = subprocess.run(build_cmd, check=True, capture_output=True, text=True)
        print("✓ 构建成功！")
        
        # 检查输出文件
        if platform.system() == "Windows":
            exe_path = Path("dist/FileRenamer.exe")
        else:
            exe_path = Path("dist/FileRenamer")
        
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"✓ 可执行文件: {exe_path}")
            print(f"✓ 文件大小: {size_mb:.1f} MB")
        else:
            print("✗ 可执行文件未生成")
            return False
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ 构建失败: {e}")
        if e.stderr:
            print("错误输出:")
            print(e.stderr)
        return False

def create_windows_readme():
    """创建Windows使用说明"""
    readme_content = '''# Windows版本使用说明

## 系统要求
- Windows 10 或更高版本
- 至少 4GB 内存
- 至少 500MB 可用磁盘空间

## 安装步骤
1. 下载 `FileRenamer.exe`
2. 双击运行即可，无需安装

## 首次运行
- 首次运行可能需要较长时间
- 系统可能会提示安全警告，选择"仍要运行"
- 如果被Windows Defender拦截，选择"允许"

## 常见问题

### 问题1：程序无法启动
**解决方案**：
- 右键点击exe文件，选择"以管理员身份运行"
- 检查是否被杀毒软件拦截
- 确保Windows版本兼容

### 问题2：缺少DLL文件
**解决方案**：
- 安装Microsoft Visual C++ Redistributable
- 下载地址：https://aka.ms/vs/17/release/vc_redist.x64.exe

### 问题3：权限错误
**解决方案**：
- 以管理员身份运行
- 检查文件权限设置
- 选择有写入权限的目录

---
版本：1.0.0
更新日期：2024年12月
'''
    
    with open('Windows使用说明.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✓ Windows使用说明创建成功")

def main():
    """主函数"""
    print("=" * 60)
    print("Windows平台专用打包工具")
    print("=" * 60)
    
    # 检查主程序文件
    if not Path("file_renamer_gui.py").exists():
        print("✗ 错误: 未找到 file_renamer_gui.py 文件")
        return
    
    # 显示平台信息
    print(f"当前平台: {platform.system()}")
    print(f"Python版本: {sys.version}")
    
    # 构建Windows可执行文件
    if not build_windows_executable():
        print("✗ 构建失败")
        return
    
    # 创建使用说明
    create_windows_readme()
    
    print("\n" + "=" * 60)
    print("构建完成！")
    print("=" * 60)
    
    if platform.system() == "Windows":
        print("✓ 可执行文件: dist/FileRenamer.exe")
    else:
        print("✓ 可执行文件: dist/FileRenamer")
        print("⚠ 注意: 在非Windows平台上构建的文件可能无法在Windows上运行")
    
    print("✓ 使用说明: Windows使用说明.txt")
    
    if platform.system() != "Windows":
        print("\n⚠ 重要提示:")
        print("1. 当前在非Windows平台上构建")
        print("2. 生成的文件可能无法在Windows上运行")
        print("3. 建议在Windows平台上重新构建")
        print("4. 或者使用虚拟机或Docker进行交叉编译")

if __name__ == "__main__":
    main()
