#!/usr/bin/env python3
"""
本地EasyOCR模型下载脚本
在本地环境下载模型文件，然后打包到EXE中
"""

import os
import sys
from pathlib import Path
import requests
from tqdm import tqdm

def download_file(url, filepath, chunk_size=8192):
    """下载文件并显示进度条"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(filepath, 'wb') as f:
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=filepath.name) as pbar:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
        return True
    except Exception as e:
        print(f"下载失败: {e}")
        return False

def main():
    print("🚀 开始下载EasyOCR模型文件（本地环境）...")
    
    # 创建模型目录
    models_dir = Path("easyocr_models")
    models_dir.mkdir(exist_ok=True)
    
    # 模型文件列表
    models = [
        {
            "name": "chinese_sim.pth",
            "url": "https://github.com/JaidedAI/EasyOCR/releases/download/pre-v1.1.6/chinese_sim.pth",
            "size": "约50MB"
        },
        {
            "name": "english.pth",
            "url": "https://github.com/JaidedAI/EasyOCR/releases/download/pre-v1.1.6/english.pth", 
            "size": "约50MB"
        }
    ]
    
    print(f"📁 模型将保存到: {models_dir.absolute()}")
    print(f"📦 需要下载 {len(models)} 个模型文件")
    print("💡 下载完成后，这些文件将被打包到EXE中")
    
    # 下载模型文件
    for model in models:
        model_path = models_dir / model["name"]
        
        if model_path.exists():
            file_size = model_path.stat().st_size / (1024*1024)
            print(f"✅ {model['name']} 已存在 ({file_size:.1f} MB)，跳过下载")
            continue
            
        print(f"⬇️  下载 {model['name']} ({model['size']})...")
        print(f"   从: {model['url']}")
        
        if download_file(model['url'], model_path):
            file_size = model_path.stat().st_size / (1024*1024)
            print(f"✅ {model['name']} 下载完成 ({file_size:.1f} MB)")
        else:
            print(f"❌ {model['name']} 下载失败")
            return False
    
    print("\n🎉 所有模型文件下载完成！")
    print(f"📁 模型目录: {models_dir.absolute()}")
    
    total_size = sum(f.stat().st_size for f in models_dir.glob('*.pth')) / (1024*1024)
    print(f"📏 总大小: {total_size:.1f} MB")
    
    # 创建打包说明文件
    pack_instructions = f"""# EasyOCR模型打包说明

## 📁 模型文件
- chinese_sim.pth: 中文简体识别模型
- english.pth: 英文识别模型

## 🚀 打包到EXE
使用以下PyInstaller命令打包：

```bash
pyinstaller --onefile --windowed --name=FileRenamer --clean \\
  --add-data "easyocr_models;easyocr_models" \\
  file_renamer_gui.py
```

## 📋 注意事项
1. 模型文件总大小约 {total_size:.1f} MB
2. 打包后的EXE会包含这些模型文件
3. 运行时无需网络下载，直接使用本地模型
4. 初始化速度会大大提升

## 🔧 环境变量
代码会自动设置 EASYOCR_MODULE_PATH 环境变量指向模型目录
"""
    
    readme_file = models_dir / "PACKAGING_README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(pack_instructions)
    
    print(f"📝 打包说明已创建: {readme_file}")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ 模型下载完成！")
            print("💡 现在可以运行以下命令打包EXE：")
            print("   pyinstaller --onefile --windowed --name=FileRenamer --clean --add-data 'easyocr_models;easyocr_models' file_renamer_gui.py")
        else:
            print("\n❌ 模型下载失败！")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  用户中断下载")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 脚本执行出错: {e}")
        sys.exit(1)
