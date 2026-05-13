#!/usr/bin/env python
"""从 HTML 文件中提取所有 ID 和选择器"""

import re
import os

HTML_FILE = "demo/activity_management.html"

def extract_from_html():
    """从 HTML 文件提取所有有用的选择器"""
    
    if not os.path.exists(HTML_FILE):
        print(f"❌ 文件不存在: {HTML_FILE}")
        return
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("=" * 70)
    print("🔍 分析 HTML 文件: activity_management.html")
    print("=" * 70)
    
    # 1. 提取所有 ID
    ids = re.findall(r'id=["\']([^"\']+)["\']', content, re.IGNORECASE)
    unique_ids = sorted(set(ids))
    
    print(f"\n📋 找到 {len(unique_ids)} 个 ID 属性:")
    print("-" * 50)
    for aid in unique_ids:
        print(f"  #{aid}")
    
    # 2. 提取所有 name 属性
    names = re.findall(r'name=["\']([^"\']+)["\']', content, re.IGNORECASE)
    unique_names = sorted(set(names))
    
    print(f"\n📋 找到 {len(unique_names)} 个 name 属性:")
    print("-" * 50)
    for name in unique_names[:20]:
        print(f"  [name='{name}']")
    if len(unique_names) > 20:
        print(f"  ... 还有 {len(unique_names) - 20} 个")
    
    # 3. 提取按钮文本
    buttons = re.findall(r'<button[^>]*>([^<]+)</button>', content, re.IGNORECASE)
    unique_buttons = list(dict.fromkeys([b.strip() for b in buttons if b.strip()]))
    
    print(f"\n📋 找到 {len(unique_buttons)} 个按钮:")
    print("-" * 50)
    for btn in unique_buttons:
        print(f"  button:has-text('{btn}')")
    
    # 4. 提取 select 选项
    selects = re.findall(r'<select[^>]*id=["\']([^"\']+)["\'][^>]*>.*?</select>', content, re.DOTALL)
    
    print(f"\n📋 找到 {len(selects)} 个 select 下拉框:")
    print("-" * 50)
    for sel in set(selects):
        # 获取该 select 下的选项
        pattern = rf'<select[^>]*id=["\']{sel}["\'][^>]*>(.*?)</select>'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            options = re.findall(r'<option[^>]*>([^<]+)</option>', match.group(1))
            print(f"  #{sel} -> {', '.join(options[:3])}")
            if len(options) > 3:
                print(f"      ... 还有 {len(options) - 3} 个选项")
    
    # 5. 生成测试代码可用的选择器映射
    print("\n" + "=" * 70)
    print("📝 生成的选择器映射（用于测试代码）:")
    print("=" * 70)
    
    selector_map = {
        "活动名称": "#formName" if "formName" in unique_ids else "#activityName" if "activityName" in unique_ids else None,
        "活动类型": "#formType" if "formType" in unique_ids else "#activityType" if "activityType" in unique_ids else None,
        "二级类型": "#formSubType" if "formSubType" in unique_ids else "#subActivityType" if "subActivityType" in unique_ids else None,
        "开始时间": "#formStartTime" if "formStartTime" in unique_ids else "#startTime" if "startTime" in unique_ids else None,
        "结束时间": "#formEndTime" if "formEndTime" in unique_ids else "#endTime" if "endTime" in unique_ids else None,
        "活动简介": "#formDescription" if "formDescription" in unique_ids else "#description" if "description" in unique_ids else None,
        "地点类型": "#formLocationType" if "formLocationType" in unique_ids else "#locationType" if "locationType" in unique_ids else None,
        "平台名称": "#formPlatformName" if "formPlatformName" in unique_ids else "#platformName" if "platformName" in unique_ids else None,
        "省份": "#formProvince" if "formProvince" in unique_ids else "#province" if "province" in unique_ids else None,
        "城市": "#formCity" if "formCity" in unique_ids else "#city" if "city" in unique_ids else None,
        "区县": "#formDistrict" if "formDistrict" in unique_ids else "#district" if "district" in unique_ids else None,
        "详细地址": "#formDetailAddress" if "formDetailAddress" in unique_ids else "#detailAddress" if "detailAddress" in unique_ids else None,
        "新建按钮": "#btnCreate" if "btnCreate" in unique_ids else "#createBtn" if "createBtn" in unique_ids else None,
        "提交按钮": "#btnSubmit" if "btnSubmit" in unique_ids else "#submitBtn" if "submitBtn" in unique_ids else None,
        "保存按钮": "#btnSave" if "btnSave" in unique_ids else "#saveBtn" if "saveBtn" in unique_ids else None,
        "取消按钮": "#btnCancel" if "btnCancel" in unique_ids else "#cancelBtn" if "cancelBtn" in unique_ids else None,
        "角色切换": "#roleSelect" if "roleSelect" in unique_ids else "#role" if "role" in unique_ids else None,
    }
    
    for key, value in selector_map.items():
        if value:
            print(f"  {key}: {value}")
        else:
            print(f"  {key}: ❌ 未找到")
    
    # 6. 生成更新后的选择器字典
    print("\n" + "=" * 70)
    print("💡 建议在 config.py 中更新以下选择器:")
    print("=" * 70)
    print("\nselectors = {")
    for key, value in selector_map.items():
        if value:
            print(f'    "{key}": "{value}",')
    print("}")

if __name__ == "__main__":
    extract_from_html()