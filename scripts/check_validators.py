# scripts/check_validators.py
"""检查测试代码中的选择器是否有效"""

import re
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test.ai.test_validator import TestValidator

def check_test_file(file_path, base_url):
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    validator = TestValidator(base_url)
    results = validator.validate_selectors(code)
    
    print("\n" + "=" * 60)
    print("🔍 选择器验证报告")
    print("=" * 60)
    
    valid = []
    invalid = []
    
    for r in results:
        if r['valid']:
            valid.append(r['selector'])
        else:
            invalid.append(r['selector'])
    
    print(f"\n✅ 有效选择器 ({len(valid)}):")
    for sel in valid[:20]:
        print(f"   {sel}")
    
    print(f"\n❌ 无效选择器 ({len(invalid)}):")
    for sel in invalid[:20]:
        print(f"   {sel}")
    
    return invalid

if __name__ == "__main__":
    test_file = "test/ai/generated/activity/generated_test_活动管理_01_创建活动.py"
    base_url = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/demo/activity_management.html"
    
    invalid = check_test_file(test_file, base_url)
    
    if invalid:
        print(f"\n💡 建议修复的无效选择器:")
        for sel in invalid[:10]:
            if sel == "#formLocation":
                print(f"   {sel} → 应使用 #onlineLocation 或 #offlineLocation")