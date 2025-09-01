#!/usr/bin/env python3
"""逐步调试 DeepSeek 服务"""

import sys
from pathlib import Path

def debug_step_by_step():
    print("=== 逐步调试 DeepSeek 服务 ===")
    
    # 步骤1: 检查导入
    print("\n步骤1: 检查导入")
    try:
        from deepseek_api_service import deepseek_service
        print("✓ 导入成功")
    except Exception as e:
        print(f"✗ 导入失败: {e}")
        return
    
    # 步骤2: 检查 API Key
    print("\n步骤2: 检查 API Key")
    print(f"API Key 已加载: {bool(deepseek_service.api_key)}")
    if deepseek_service.api_key:
        print(f"API Key 前缀: {deepseek_service.api_key[:10]}...")
    else:
        print("✗ API Key 未加载")
        return
    
    # 步骤3: 测试 PDF 文本提取
    print("\n步骤3: 测试 PDF 文本提取")
    pdf_path = Path('test_file/20250822101923-0001.pdf')
    if not pdf_path.exists():
        print("✗ PDF 文件不存在")
        return
    
    print(f"PDF 文件: {pdf_path.name}")
    print(f"文件大小: {pdf_path.stat().st_size} bytes")
    
    try:
        content = deepseek_service._read_pdf_content(pdf_path)
        if content:
            print(f"✓ PDF 文本提取成功，长度: {len(content)}")
            print(f"前200字符: {content[:200]}...")
        else:
            print("✗ PDF 文本提取失败")
            return
    except Exception as e:
        print(f"✗ PDF 文本提取异常: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 步骤4: 测试 DeepSeek Chat API
    print("\n步骤4: 测试 DeepSeek Chat API")
    try:
        result = deepseek_service._call_deepseek_api(content, pdf_path.name)
        if result:
            print(f"✓ DeepSeek Chat API 调用成功!")
            print(f"结果: {result}")
        else:
            print("✗ DeepSeek Chat API 返回空结果")
            if deepseek_service.last_error:
                print(f"错误: {deepseek_service.last_error}")
    except Exception as e:
        print(f"✗ DeepSeek Chat API 异常: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 步骤5: 测试完整的重命名流程
    print("\n步骤5: 测试完整重命名流程")
    try:
        final_result = deepseek_service.extract_renaming_info(pdf_path)
        if final_result:
            print(f"✓ 完整流程成功!")
            print(f"最终结果: {final_result}")
        else:
            print("✗ 完整流程失败")
            if deepseek_service.last_error:
                print(f"错误: {deepseek_service.last_error}")
            if deepseek_service.last_suggestion:
                print(f"建议: {deepseek_service.last_suggestion}")
    except Exception as e:
        print(f"✗ 完整流程异常: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n=== 调试完成 ===")

if __name__ == '__main__':
    debug_step_by_step()
