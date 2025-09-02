#!/usr/bin/env python3
"""
查找EasyOCR模型正确下载地址的脚本
分析官方仓库，找到可用的模型下载链接
"""

import requests
import json
from pathlib import Path

def check_github_releases():
    """检查GitHub Releases中的模型文件"""
    print("🔍 检查GitHub Releases...")
    
    # EasyOCR官方仓库
    repo_url = "https://api.github.com/repos/JaidedAI/EasyOCR/releases"
    
    try:
        response = requests.get(repo_url)
        if response.status_code == 200:
            releases = response.json()
            print(f"✅ 找到 {len(releases)} 个发布版本")
            
            for release in releases[:5]:  # 只检查最新的5个版本
                tag = release['tag_name']
                print(f"\n📦 版本: {tag}")
                print(f"   发布时间: {release['published_at']}")
                
                # 检查assets
                if 'assets' in release:
                    for asset in release['assets']:
                        name = asset['name']
                        size = asset['size'] / (1024*1024)  # MB
                        if '.pth' in name:
                            print(f"   🔍 模型文件: {name} ({size:.1f} MB)")
                            download_url = asset['browser_download_url']
                            print(f"   📥 下载链接: {download_url}")
                else:
                    print("   ❌ 没有assets")
        else:
            print(f"❌ GitHub API请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 检查GitHub Releases失败: {e}")

def check_huggingface():
    """检查Hugging Face上的模型"""
    print("\n🔍 检查Hugging Face...")
    
    # EasyOCR在Hugging Face上的空间
    hf_url = "https://huggingface.co/api/spaces/jaidedai/easyocr"
    
    try:
        response = requests.get(hf_url)
        if response.status_code == 200:
            space_info = response.json()
            print(f"✅ 找到Hugging Face空间: {space_info.get('name', 'Unknown')}")
            print(f"   描述: {space_info.get('description', 'No description')}")
            
            # 尝试访问模型文件
            model_files = [
                "https://huggingface.co/spaces/jaidedai/easyocr/resolve/main/chinese_sim.pth",
                "https://huggingface.co/spaces/jaidedai/easyocr/resolve/main/english.pth"
            ]
            
            for url in model_files:
                try:
                    head_response = requests.head(url, timeout=10)
                    print(f"   🔍 {url}")
                    print(f"      状态码: {head_response.status_code}")
                    if head_response.status_code == 200:
                        size = head_response.headers.get('content-length')
                        if size:
                            size_mb = int(size) / (1024*1024)
                            print(f"      文件大小: {size_mb:.1f} MB")
                        else:
                            print("      文件大小: 未知")
                    else:
                        print(f"      ❌ 不可访问")
                except Exception as e:
                    print(f"      ❌ 检查失败: {e}")
                    
        else:
            print(f"❌ Hugging Face API请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 检查Hugging Face失败: {e}")

def check_easyocr_installation():
    """检查EasyOCR安装后的模型路径"""
    print("\n🔍 检查EasyOCR安装信息...")
    
    try:
        import easyocr
        print(f"✅ EasyOCR版本: {easyocr.__version__}")
        
        # 尝试获取模型路径
        try:
            # 查看EasyOCR的模型存储位置
            import os
            home_dir = os.path.expanduser("~")
            easyocr_dir = os.path.join(home_dir, ".EasyOCR")
            
            if os.path.exists(easyocr_dir):
                print(f"📁 默认模型目录: {easyocr_dir}")
                if os.path.isdir(easyocr_dir):
                    files = os.listdir(easyocr_dir)
                    print(f"   目录内容: {files}")
                    
                    # 检查是否有模型文件
                    model_files = [f for f in files if f.endswith('.pth')]
                    if model_files:
                        print(f"   🎯 找到模型文件: {model_files}")
                        for model in model_files:
                            model_path = os.path.join(easyocr_dir, model)
                            size = os.path.getsize(model_path) / (1024*1024)
                            print(f"      {model}: {size:.1f} MB")
                    else:
                        print("   ❌ 没有找到.pth模型文件")
            else:
                print(f"📁 默认模型目录不存在: {easyocr_dir}")
                
        except Exception as e:
            print(f"❌ 检查模型目录失败: {e}")
            
    except ImportError:
        print("❌ EasyOCR未安装")
    except Exception as e:
        print(f"❌ 检查EasyOCR失败: {e}")

def test_download_urls():
    """测试各种可能的下载URL"""
    print("\n🔍 测试可能的下载URL...")
    
    # 收集到的可能URL
    test_urls = [
        # GitHub相关
        "https://github.com/JaidedAI/EasyOCR/releases/download/pre-v1.1.6/chinese_sim.pth",
        "https://github.com/JaidedAI/EasyOCR/releases/download/v1.7.0/chinese_sim.pth",
        "https://github.com/JaidedAI/EasyOCR/releases/latest/download/chinese_sim.pth",
        
        # Hugging Face相关
        "https://huggingface.co/spaces/jaidedai/easyocr/resolve/main/chinese_sim.pth",
        "https://huggingface.co/jaidedai/easyocr/resolve/main/chinese_sim.pth",
        
        # 其他可能的源
        "https://www.dropbox.com/s/8n02xqv3l9d5ziw/chinese_sim.pth?dl=1",
        "https://drive.google.com/uc?id=1nV57qKuy--d5u1yvkR9KJMs7BH3Ub6cm&export=download"
    ]
    
    for i, url in enumerate(test_urls, 1):
        try:
            print(f"\n🔍 测试URL {i}: {url}")
            response = requests.head(url, timeout=10)
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 200:
                size = response.headers.get('content-length')
                if size:
                    size_mb = int(size) / (1024*1024)
                    print(f"   文件大小: {size_mb:.1f} MB")
                    
                    # 判断是否可能是正确的模型文件
                    if size_mb > 40:
                        print(f"   ✅ 可能是正确的模型文件！")
                    else:
                        print(f"   ❌ 文件大小异常，可能不是模型文件")
                else:
                    print(f"   文件大小: 未知")
                    
                # 检查Content-Type
                content_type = response.headers.get('content-type', '')
                print(f"   内容类型: {content_type}")
                
            elif response.status_code == 404:
                print(f"   ❌ 文件不存在")
            elif response.status_code == 401:
                print(f"   ❌ 需要认证")
            elif response.status_code == 403:
                print(f"   ❌ 访问被拒绝")
            else:
                print(f"   ❌ 其他错误")
                
        except Exception as e:
            print(f"   ❌ 请求失败: {e}")

def main():
    print("🚀 开始分析EasyOCR模型下载问题...")
    print("=" * 60)
    
    check_github_releases()
    check_huggingface()
    check_easyocr_installation()
    test_download_urls()
    
    print("\n" + "=" * 60)
    print("🎯 分析完成！请查看上面的结果来找到正确的下载源。")

if __name__ == "__main__":
    main()
