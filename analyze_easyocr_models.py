#!/usr/bin/env python3
"""
深入分析EasyOCR模型分发机制的脚本
了解模型文件是如何获取和存储的
"""

import os
import sys
from pathlib import Path

def analyze_easyocr_installation():
    """分析EasyOCR安装后的模型管理机制"""
    print("🔍 分析EasyOCR模型管理机制...")
    
    try:
        import easyocr
        print(f"✅ EasyOCR版本: {easyocr.__version__}")
        
        # 查看EasyOCR的源码结构
        easyocr_path = easyocr.__file__
        print(f"📁 EasyOCR安装路径: {easyocr_path}")
        
        # 查看EasyOCR包目录
        easyocr_dir = os.path.dirname(easyocr_path)
        print(f"📁 EasyOCR包目录: {easyocr_dir}")
        
        # 查看EasyOCR包内容
        if os.path.exists(easyocr_dir):
            files = os.listdir(easyocr_dir)
            print(f"📦 包内容: {files}")
            
            # 查找模型相关文件
            model_files = [f for f in files if 'model' in f.lower() or 'download' in f.lower()]
            if model_files:
                print(f"🎯 模型相关文件: {model_files}")
        
        # 查看用户目录下的.EasyOCR文件夹
        home_dir = os.path.expanduser("~")
        user_easyocr_dir = os.path.join(home_dir, ".EasyOCR")
        print(f"\n🏠 用户模型目录: {user_easyocr_dir}")
        
        if os.path.exists(user_easyocr_dir):
            if os.path.isdir(user_easyocr_dir):
                user_files = os.listdir(user_easyocr_dir)
                print(f"   用户目录内容: {user_files}")
                
                # 检查模型文件
                pth_files = [f for f in user_files if f.endswith('.pth')]
                if pth_files:
                    print(f"   🎯 找到.pth模型文件: {pth_files}")
                    for model in pth_files:
                        model_path = os.path.join(user_easyocr_dir, model)
                        size = os.path.getsize(model_path) / (1024*1024)
                        print(f"      {model}: {size:.1f} MB")
                else:
                    print("   ❌ 没有找到.pth模型文件")
            else:
                print("   ❌ 不是目录")
        else:
            print("   ❌ 目录不存在")
            
    except ImportError:
        print("❌ EasyOCR未安装")
        return False
    except Exception as e:
        print(f"❌ 分析失败: {e}")
        return False
    
    return True

def check_easyocr_download_mechanism():
    """检查EasyOCR的模型下载机制"""
    print("\n🔍 检查EasyOCR模型下载机制...")
    
    try:
        import easyocr
        
        # 尝试查看EasyOCR的下载逻辑
        print("🔍 查看EasyOCR Reader初始化过程...")
        
        # 检查是否有预定义的模型URL
        easyocr_path = easyocr.__file__
        easyocr_dir = os.path.dirname(easyocr_path)
        
        # 查找可能的配置文件
        config_files = ['config.py', 'constants.py', 'utils.py']
        for config_file in config_files:
            config_path = os.path.join(easyocr_dir, config_file)
            if os.path.exists(config_path):
                print(f"📄 找到配置文件: {config_file}")
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # 查找模型相关的URL或配置
                        if 'model' in content.lower() or 'url' in content.lower():
                            print(f"   🔍 {config_file} 包含模型相关配置")
                            # 提取可能的URL
                            lines = content.split('\n')
                            for line in lines:
                                if 'http' in line and ('model' in line.lower() or 'pth' in line.lower()):
                                    print(f"      📥 可能的模型URL: {line.strip()}")
                except Exception as e:
                    print(f"   ❌ 读取配置文件失败: {e}")
        
        # 检查是否有专门的模型管理模块
        model_modules = ['model_manager.py', 'download.py', 'models.py']
        for module in model_modules:
            module_path = os.path.join(easyocr_dir, module)
            if os.path.exists(module_path):
                print(f"📦 找到模型管理模块: {module}")
                
    except Exception as e:
        print(f"❌ 检查下载机制失败: {e}")

def test_easyocr_model_download():
    """测试EasyOCR的模型下载过程"""
    print("\n🔍 测试EasyOCR模型下载过程...")
    
    try:
        import easyocr
        
        print("🔍 尝试初始化EasyOCR Reader（观察下载过程）...")
        print("⚠️  这可能需要几分钟时间，请耐心等待...")
        
        # 尝试初始化，观察是否会自动下载模型
        try:
            print("   正在初始化中文简体模型...")
            reader = easyocr.Reader(['ch_sim'], gpu=False)
            print("✅ 中文简体模型初始化成功")
            
            # 检查是否下载了模型文件
            home_dir = os.path.expanduser("~")
            user_easyocr_dir = os.path.join(home_dir, ".EasyOCR")
            if os.path.exists(user_easyocr_dir):
                files = os.listdir(user_easyocr_dir)
                pth_files = [f for f in files if f.endswith('.pth')]
                if pth_files:
                    print(f"   🎯 模型文件已下载: {pth_files}")
                    for model in pth_files:
                        model_path = os.path.join(user_easyocr_dir, model)
                        size = os.path.getsize(model_path) / (1024*1024)
                        print(f"      {model}: {size:.1f} MB")
                else:
                    print("   ❌ 没有找到模型文件")
            
        except Exception as e:
            print(f"❌ 中文简体模型初始化失败: {e}")
            
    except Exception as e:
        print(f"❌ 测试模型下载失败: {e}")

def search_online_models():
    """搜索在线可用的EasyOCR模型"""
    print("\n🔍 搜索在线可用的EasyOCR模型...")
    
    # 基于EasyOCR的实际分发方式，搜索可能的模型源
    print("🔍 基于EasyOCR官方信息，可能的模型源：")
    
    # 1. 检查EasyOCR官方仓库的模型文件夹
    print("\n1️⃣ 检查EasyOCR官方仓库...")
    print("   GitHub: https://github.com/JaidedAI/EasyOCR")
    print("   可能的模型路径:")
    print("   - /models/")
    print("   - /easyocr/models/")
    print("   - /weights/")
    
    # 2. 检查EasyOCR的模型分发策略
    print("\n2️⃣ EasyOCR模型分发策略分析:")
    print("   - 模型文件通常不直接放在GitHub Releases中")
    print("   - 而是在运行时自动下载到用户目录")
    print("   - 或者通过专门的模型管理工具分发")
    
    # 3. 检查是否有专门的模型仓库
    print("\n3️⃣ 可能的专门模型仓库:")
    print("   - Hugging Face Model Hub")
    print("   - Model Zoo")
    print("   - 官方CDN或镜像")
    
    # 4. 建议的解决方案
    print("\n4️⃣ 建议的解决方案:")
    print("   - 使用EasyOCR的自动下载机制")
    print("   - 或者找到官方的模型分发地址")
    print("   - 或者使用预训练的本地模型")

def main():
    print("🚀 深入分析EasyOCR模型分发机制...")
    print("=" * 70)
    
    # 分析安装情况
    if analyze_easyocr_installation():
        # 检查下载机制
        check_easyocr_download_mechanism()
        
        # 测试模型下载
        test_easyocr_model_download()
    
    # 搜索在线模型
    search_online_models()
    
    print("\n" + "=" * 70)
    print("🎯 分析完成！基于以上信息，我们可以找到正确的解决方案。")

if __name__ == "__main__":
    main()
