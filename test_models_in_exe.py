#!/usr/bin/env python3
"""
测试EXE中是否包含EasyOCR模型文件的脚本
"""

import os
import sys
from pathlib import Path

def test_models_in_exe():
    """测试EXE中的模型文件"""
    print("🔍 测试EXE中的模型文件...")
    
    # 检查是否在EXE中运行
    if getattr(sys, 'frozen', False):
        print(f"✅ 检测到EXE运行")
        exe_path = sys.executable
        exe_dir = os.path.dirname(exe_path)
        print(f"EXE路径: {exe_path}")
        print(f"EXE目录: {exe_dir}")
        
        # 检查EXE目录下的模型文件
        exe_models_dir = os.path.join(exe_dir, "easyocr_models")
        print(f"EXE模型目录: {exe_models_dir}")
        
        if os.path.exists(exe_models_dir):
            print(f"✅ EXE模型目录存在")
            if os.path.isdir(exe_models_dir):
                files = os.listdir(exe_models_dir)
                print(f"目录内容: {files}")
                
                # 查找.pth文件
                pth_files = [f for f in files if f.endswith('.pth')]
                if pth_files:
                    print(f"✅ 找到模型文件: {pth_files}")
                    total_size = 0
                    for model in pth_files:
                        model_path = os.path.join(exe_models_dir, model)
                        size = os.path.getsize(model_path) / (1024*1024)
                        total_size += size
                        print(f"   {model}: {size:.1f} MB")
                    print(f"总大小: {total_size:.1f} MB")
                    return True
                else:
                    print(f"❌ 没有找到.pth模型文件")
                    return False
            else:
                print(f"❌ 不是目录")
                return False
        else:
            print(f"❌ EXE模型目录不存在")
            return False
    else:
        print(f"❌ 不在EXE中运行")
        return False

def test_current_directory():
    """测试当前目录的模型文件"""
    print("\n🔍 测试当前目录的模型文件...")
    
    current_dir = Path.cwd()
    print(f"当前目录: {current_dir}")
    
    # 检查easyocr_models目录
    models_dir = current_dir / "easyocr_models"
    if models_dir.exists():
        print(f"✅ 当前目录模型目录存在: {models_dir}")
        if models_dir.is_dir():
            files = list(models_dir.glob("*.pth"))
            if files:
                print(f"✅ 找到模型文件: {[f.name for f in files]}")
                total_size = sum(f.stat().st_size for f in files) / (1024*1024)
                print(f"总大小: {total_size:.1f} MB")
                return True
            else:
                print(f"❌ 没有找到.pth模型文件")
                return False
        else:
            print(f"❌ 不是目录")
            return False
    else:
        print(f"❌ 当前目录模型目录不存在")
        return False

def test_user_directory():
    """测试用户目录的模型文件"""
    print("\n🔍 测试用户目录的模型文件...")
    
    home_dir = os.path.expanduser("~")
    user_models_dir = os.path.join(home_dir, ".EasyOCR")
    print(f"用户模型目录: {user_models_dir}")
    
    if os.path.exists(user_models_dir):
        print(f"✅ 用户模型目录存在")
        if os.path.isdir(user_models_dir):
            files = os.listdir(user_models_dir)
            print(f"目录内容: {files}")
            
            # 查找.pth文件
            pth_files = [f for f in files if f.endswith('.pth')]
            if pth_files:
                print(f"✅ 找到模型文件: {pth_files}")
                total_size = 0
                for model in pth_files:
                    model_path = os.path.join(user_models_dir, model)
                    size = os.path.getsize(model_path) / (1024*1024)
                    total_size += size
                    print(f"   {model}: {size:.1f} MB")
                print(f"总大小: {total_size:.1f} MB")
                return True
            else:
                print(f"❌ 没有找到.pth模型文件")
                return False
        else:
            print(f"❌ 不是目录")
            return False
    else:
        print(f"❌ 用户模型目录不存在")
        return False

def main():
    print("🚀 开始测试EasyOCR模型文件...")
    print("=" * 60)
    
    # 测试EXE中的模型文件
    exe_has_models = test_models_in_exe()
    
    # 测试当前目录的模型文件
    current_has_models = test_current_directory()
    
    # 测试用户目录的模型文件
    user_has_models = test_user_directory()
    
    print("\n" + "=" * 60)
    print("📊 测试结果总结:")
    print(f"EXE中包含模型: {'✅ 是' if exe_has_models else '❌ 否'}")
    print(f"当前目录包含模型: {'✅ 是' if current_has_models else '❌ 否'}")
    print(f"用户目录包含模型: {'✅ 是' if user_has_models else '❌ 否'}")
    
    if exe_has_models:
        print("\n🎉 EXE中包含模型文件，应该能正常工作！")
    elif current_has_models:
        print("\n⚠️  EXE中不包含模型文件，但当前目录有模型文件")
    elif user_has_models:
        print("\n⚠️  EXE中不包含模型文件，但用户目录有模型文件")
    else:
        print("\n❌ 没有找到任何模型文件，需要重新构建EXE")

if __name__ == "__main__":
    main()
