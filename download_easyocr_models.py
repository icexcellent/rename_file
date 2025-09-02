#!/usr/bin/env python3
"""
EasyOCR模型预下载脚本
用于在打包前下载模型文件，避免运行时下载超时
"""

import os
import sys
import shutil
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
    print("🚀 开始下载EasyOCR模型文件...")
    
    # 创建模型目录
    models_dir = Path("easyocr_models")
    models_dir.mkdir(exist_ok=True)
    
    # 模型文件列表（中文简体和英文）
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
    
    # 下载模型文件
    for model in models:
        model_path = models_dir / model["name"]
        
        if model_path.exists():
            print(f"✅ {model['name']} 已存在，跳过下载")
            continue
            
        print(f"⬇️  下载 {model['name']} ({model['size']})...")
        print(f"   从: {model['url']}")
        
        if download_file(model['url'], model_path):
            print(f"✅ {model['name']} 下载完成")
        else:
            print(f"❌ {model['name']} 下载失败")
            return False
    
    print("\n🎉 所有模型文件下载完成！")
    print(f"📁 模型目录: {models_dir.absolute()}")
    print(f"📏 总大小: {sum(f.stat().st_size for f in models_dir.glob('*.pth')) / (1024*1024):.1f} MB")
    
    # 创建模型配置文件
    config_content = f"""# EasyOCR模型配置文件
# 模型目录: {models_dir.absolute()}
# 生成时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

MODEL_PATH = "{models_dir.absolute()}"
CHINESE_MODEL = "chinese_sim.pth"
ENGLISH_MODEL = "english.pth"

# 使用说明:
# 1. 将此目录打包到EXE中
# 2. 设置环境变量 EASYOCR_MODULE_PATH 指向此目录
# 3. 或者在代码中指定模型路径
"""
    
    config_file = models_dir / "README.md"
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print(f"📝 配置文件已创建: {config_file}")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ 模型下载脚本执行成功！")
            print("💡 现在可以将 easyocr_models 目录打包到EXE中")
        else:
            print("\n❌ 模型下载脚本执行失败！")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  用户中断下载")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 脚本执行出错: {e}")
        sys.exit(1)
