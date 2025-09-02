#!/usr/bin/env python3
"""
测试exe文件中requests模块的可用性
用于验证PyInstaller打包后requests模块是否被正确包含
"""

import subprocess
import sys
import os
from pathlib import Path

def test_exe_requests(exe_path):
    """测试exe文件中的requests模块"""
    if not os.path.exists(exe_path):
        print(f"❌ EXE文件不存在: {exe_path}")
        return False
    
    print(f"🔍 测试EXE文件: {exe_path}")
    
    # 创建一个测试脚本，在exe环境中运行
    test_script = """
import sys
import traceback

def test_requests():
    try:
        import requests
        print(f"✅ requests模块导入成功，版本: {requests.__version__}")
        
        # 测试基本功能
        response = requests.get("https://httpbin.org/get", timeout=5)
        if response.status_code == 200:
            print("✅ requests HTTP请求测试成功")
            return True
        else:
            print(f"❌ requests HTTP请求失败，状态码: {response.status_code}")
            return False
            
    except ImportError as e:
        print(f"❌ requests模块导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ requests功能测试失败: {e}")
        traceback.print_exc()
        return False

def test_urllib3():
    try:
        import urllib3
        print(f"✅ urllib3模块导入成功，版本: {urllib3.__version__}")
        return True
    except ImportError as e:
        print(f"❌ urllib3模块导入失败: {e}")
        return False

if __name__ == "__main__":
    print("=== EXE内部requests模块测试 ===")
    
    urllib3_ok = test_urllib3()
    requests_ok = test_requests()
    
    if urllib3_ok and requests_ok:
        print("🎉 所有测试通过！requests模块完全可用")
    else:
        print("⚠️ 部分测试失败，可能存在兼容性问题")
"""
    
    # 写入临时测试脚本
    test_file = "temp_test_requests.py"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_script)
    
    try:
        # 运行exe文件，执行测试脚本
        print("🚀 在EXE环境中运行测试...")
        result = subprocess.run(
            [exe_path, test_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ EXE执行成功")
            print("\n📋 测试输出:")
            print(result.stdout)
            
            if "requests模块导入成功" in result.stdout:
                print("\n🎉 requests模块测试通过！")
                return True
            else:
                print("\n❌ requests模块测试失败")
                return False
        else:
            print(f"❌ EXE执行失败，返回码: {result.returncode}")
            print(f"错误输出: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ EXE执行超时")
        return False
    except Exception as e:
        print(f"❌ 测试执行异常: {e}")
        return False
    finally:
        # 清理临时文件
        if os.path.exists(test_file):
            os.remove(test_file)

def main():
    """主函数"""
    print("=== EXE文件requests模块测试 ===\n")
    
    # 查找exe文件
    exe_paths = [
        "dist/FileRenamer.exe",
        "FileRenamer.exe",
        "./FileRenamer.exe"
    ]
    
    exe_found = False
    for exe_path in exe_paths:
        if os.path.exists(exe_path):
            exe_found = True
            if test_exe_requests(exe_path):
                print("\n✅ EXE文件中的requests模块测试完全通过！")
                print("API功能应该能正常工作")
            else:
                print("\n❌ EXE文件中的requests模块测试失败")
                print("需要检查PyInstaller配置")
            break
    
    if not exe_found:
        print("❌ 未找到FileRenamer.exe文件")
        print("请先运行PyInstaller构建，或检查exe文件路径")
        print("\n可能的路径:")
        for path in exe_paths:
            print(f"  - {path}")

if __name__ == "__main__":
    main()
