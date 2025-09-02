#!/usr/bin/env python3
"""
测试requests模块可用性的脚本
用于验证PyInstaller打包后requests模块是否正常工作
"""

import sys
import traceback

def test_requests_import():
    """测试requests模块导入"""
    try:
        import requests
        print(f"✅ requests模块导入成功，版本: {requests.__version__}")
        return True
    except ImportError as e:
        print(f"❌ requests模块导入失败: {e}")
        return False

def test_urllib3_import():
    """测试urllib3模块导入"""
    try:
        import urllib3
        print(f"✅ urllib3模块导入成功，版本: {urllib3.__version__}")
        return True
    except ImportError as e:
        print(f"❌ urllib3模块导入失败: {e}")
        return False

def test_requests_functionality():
    """测试requests功能"""
    try:
        import requests
        
        # 测试简单的HTTP请求
        response = requests.get("https://httpbin.org/get", timeout=5)
        if response.status_code == 200:
            print("✅ requests HTTP请求测试成功")
            return True
        else:
            print(f"❌ requests HTTP请求失败，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ requests功能测试失败: {e}")
        traceback.print_exc()
        return False

def test_api_key_functionality():
    """模拟API密钥测试功能"""
    try:
        import requests
        
        # 模拟API密钥测试
        headers = {
            "Authorization": "Bearer test_api_key",
            "Content-Type": "application/json"
        }
        
        # 测试API调用（使用httpbin作为测试端点）
        response = requests.post(
            "https://httpbin.org/post",
            json={"test": "api_key_test"},
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            print("✅ API密钥测试功能模拟成功")
            return True
        else:
            print(f"❌ API密钥测试功能模拟失败，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API密钥测试功能模拟失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("=== requests模块可用性测试 ===\n")
    
    # 测试模块导入
    requests_ok = test_requests_import()
    urllib3_ok = test_urllib3_import()
    
    if not requests_ok or not urllib3_ok:
        print("\n❌ 基础模块导入失败，无法进行功能测试")
        return
    
    print("\n" + "="*50)
    
    # 测试功能
    requests_func_ok = test_requests_functionality()
    api_test_ok = test_api_key_functionality()
    
    print("\n" + "="*50)
    
    # 总结
    if requests_ok and urllib3_ok and requests_func_ok and api_test_ok:
        print("🎉 所有测试通过！requests模块完全可用")
        print("✅ API功能应该能正常工作")
    else:
        print("⚠️ 部分测试失败，可能存在兼容性问题")
        print("请检查PyInstaller配置和模块依赖")

if __name__ == "__main__":
    main()
