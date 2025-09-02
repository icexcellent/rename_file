#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试setuptools依赖的脚本
专门用于诊断pyparsing导入问题
"""

import sys
import traceback

def test_basic_imports():
    """测试基本导入"""
    print("=== 测试基本导入 ===")
    
    try:
        import os
        print("✅ os 导入成功")
    except Exception as e:
        print(f"❌ os 导入失败: {e}")
    
    try:
        import sys
        print("✅ sys 导入成功")
    except Exception as e:
        print(f"❌ sys 导入失败: {e}")

def test_setuptools_chain():
    """测试setuptools依赖链"""
    print("\n=== 测试setuptools依赖链 ===")
    
    # 测试pyparsing
    try:
        import pyparsing
        print("✅ pyparsing 导入成功")
        print(f"   版本: {pyparsing.__version__}")
    except Exception as e:
        print(f"❌ pyparsing 导入失败: {e}")
        traceback.print_exc()
    
    # 测试packaging
    try:
        import packaging
        print("✅ packaging 导入成功")
        print(f"   版本: {packaging.__version__}")
    except Exception as e:
        print(f"❌ packaging 导入失败: {e}")
        traceback.print_exc()
    
    # 测试pkg_resources
    try:
        import pkg_resources
        print("✅ pkg_resources 导入成功")
        print(f"   版本: {pkg_resources.__version__}")
    except Exception as e:
        print(f"❌ pkg_resources 导入失败: {e}")
        traceback.print_exc()
    
    # 测试setuptools
    try:
        import setuptools
        print("✅ setuptools 导入成功")
        print(f"   版本: {setuptools.__version__}")
    except Exception as e:
        print(f"❌ setuptools 导入失败: {e}")
        traceback.print_exc()

def test_pkg_resources_functionality():
    """测试pkg_resources功能"""
    print("\n=== 测试pkg_resources功能 ===")
    
    try:
        import pkg_resources
        
        # 测试获取已安装包
        installed_packages = list(pkg_resources.working_set)
        print(f"✅ 获取已安装包成功，共 {len(installed_packages)} 个包")
        
        # 测试查找特定包
        try:
            pyparsing_dist = pkg_resources.get_distribution('pyparsing')
            print(f"✅ 找到pyparsing包: {pyparsing_dist.version}")
        except Exception as e:
            print(f"❌ 查找pyparsing包失败: {e}")
            
    except Exception as e:
        print(f"❌ pkg_resources功能测试失败: {e}")
        traceback.print_exc()

def test_packaging_functionality():
    """测试packaging功能"""
    print("\n=== 测试packaging功能 ===")
    
    try:
        import packaging.requirements
        print("✅ packaging.requirements 导入成功")
        
        import packaging.specifiers
        print("✅ packaging.specifiers 导入成功")
        
        import packaging.version
        print("✅ packaging.version 导入成功")
        
        import packaging.markers
        print("✅ packaging.markers 导入成功")
        
    except Exception as e:
        print(f"❌ packaging功能测试失败: {e}")
        traceback.print_exc()

def test_requests_chain():
    """测试requests依赖链"""
    print("\n=== 测试requests依赖链 ===")
    
    try:
        import requests
        print("✅ requests 导入成功")
        print(f"   版本: {requests.__version__}")
        
        import urllib3
        print("✅ urllib3 导入成功")
        print(f"   版本: {urllib3.__version__}")
        
    except Exception as e:
        print(f"❌ requests依赖链测试失败: {e}")
        traceback.print_exc()

def main():
    """主函数"""
    print("🔍 setuptools依赖诊断工具")
    print("=" * 50)
    
    test_basic_imports()
    test_setuptools_chain()
    test_pkg_resources_functionality()
    test_packaging_functionality()
    test_requests_chain()
    
    print("\n" + "=" * 50)
    print("诊断完成！")

if __name__ == "__main__":
    main()
