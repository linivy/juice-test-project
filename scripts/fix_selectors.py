#!/usr/bin/env python
"""通用选择器修复工具 - 自动从 HTML 学习并修复测试代码"""

import re
import os
import glob
import json
from typing import Dict, List, Optional
from difflib import SequenceMatcher

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️ Playwright 未安装，将使用静态分析模式")


class SelectorLearner:
    """从 HTML 学习选择器映射"""
    
    def __init__(self, html_path: str):
        self.html_path = html_path
        self.actual_selectors = {}
        self.all_ids = []
        self.all_names = []
        self.all_texts = []
    
    def learn_from_html(self) -> Dict[str, str]:
        """从 HTML 文件学习实际的选择器"""
        
        if not os.path.exists(self.html_path):
            print(f"❌ HTML 文件不存在: {self.html_path}")
            return {}
        
        # 方法1: 静态解析 HTML
        with open(self.html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取所有 ID
        ids = re.findall(r'id=["\']([^"\']+)["\']', content, re.IGNORECASE)
        self.all_ids = list(set(ids))
        
        # 提取所有 name
        names = re.findall(r'name=["\']([^"\']+)["\']', content, re.IGNORECASE)
        self.all_names = list(set(names))
        
        # 提取按钮文本
        buttons = re.findall(r'<button[^>]*>([^<]+)</button>', content)
        self.all_texts = [b.strip() for b in buttons if b.strip()]
        
        # 智能映射：根据常见的命名模式建立映射
        mappings = self._build_intelligent_mappings()
        
        print(f"📚 从 HTML 学习到 {len(self.all_ids)} 个 ID, {len(self.all_names)} 个 name")
        
        return mappings
    
    def _build_intelligent_mappings(self) -> Dict[str, str]:
        """建立智能映射"""
        mappings = {}
        
        # 常见字段名映射规则
        field_rules = {
            # 活动相关
            'activityName': ['formName', 'activityName', 'actName', 'name'],
            'activityType': ['formType', 'activityType', 'actType', 'type'],
            'subActivityType': ['formSubType', 'subActivityType', 'subType'],
            'startTime': ['formStartTime', 'startTime', 'start_date', 'start'],
            'endTime': ['formEndTime', 'endTime', 'end_date', 'end'],
            'description': ['formDescription', 'description', 'desc', 'intro', 'remark'],
            
            # 地址相关
            'province': ['formProvince', 'province', 'pro'],
            'city': ['formCity', 'city'],
            'district': ['formDistrict', 'district', 'area'],
            'address': ['formAddress', 'address', 'detailAddress', 'addr', 'detail'],
            
            # 地点相关
            'platformName': ['formOnlinePlatform', 'platformName', 'platform', 'onlinePlatform'],
            'onlineLocation': ['onlineLocation', 'locationOnline', 'online'],
            'offlineLocation': ['offlineLocation', 'locationOffline', 'offline'],
            
            # 按钮相关
            'createBtn': ['btnCreate', 'createBtn', 'create', 'newBtn', 'addBtn'],
            'submitBtn': ['btnSubmit', 'submitBtn', 'submit', 'saveBtn', 'confirmBtn'],
            'saveBtn': ['btnSaveDraft', 'saveBtn', 'saveDraft', 'draftBtn'],
            'cancelBtn': ['btnCancel', 'cancelBtn', 'cancel', 'discardBtn'],
            'confirmCancelBtn': ['btnConfirmCancel', 'confirmCancelBtn', 'confirmCancel'],
            'closeModalBtn': ['btnCloseModal', 'closeModalBtn', 'closeModal', 'closeBtn'],
            
            # 其他
            'roleSelect': ['roleSelect', 'role', 'userRole'],
            'searchBtn': ['btnSearch', 'searchBtn', 'search'],
            'resetBtn': ['btnReset', 'resetBtn', 'reset'],
            'exportBtn': ['btnExport', 'exportBtn', 'export'],
        }
        
        # 根据规则匹配实际 ID
        for logical_name, possible_ids in field_rules.items():
            matched = None
            for possible_id in possible_ids:
                if possible_id in self.all_ids:
                    matched = f"#{possible_id}"
                    break
                # 也检查 name 属性
                if possible_id in self.all_names:
                    matched = f"[name='{possible_id}']"
                    break
            
            if matched:
                mappings[logical_name] = matched
                # 同时添加常见的变体
                camel_case = f"#{logical_name}"
                snake_case = f"#{re.sub(r'(?<!^)(?=[A-Z])', '_', logical_name).lower()}"
                mappings[camel_case] = matched
                mappings[snake_case] = matched
        
        # 添加按钮文本映射
        for text in self.all_texts:
            cleaned = text.strip()
            if len(cleaned) > 0 and len(cleaned) < 20:
                mappings[f"button:has-text('{cleaned}')"] = f"button:has-text('{cleaned}')"
                mappings[f"text={cleaned}"] = f"button:has-text('{cleaned}')"
        
        return mappings
    
    def learn_from_live_page(self, base_url: str) -> Dict[str, str]:
        """从实时页面学习（如果 Playwright 可用）"""
        if not PLAYWRIGHT_AVAILABLE:
            return {}
        
        print(f"🌐 从实时页面学习: {base_url}")
        
        mappings = {}
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(base_url, timeout=10000, wait_until="domcontentloaded")
                
                # 1. 获取所有表单字段
                inputs = page.locator('input, select, textarea').all()
                for inp in inputs[:30]:
                    try:
                        inp_id = inp.get_attribute('id')
                        inp_name = inp.get_attribute('name')
                        inp_type = inp.get_attribute('type')
                        
                        if inp_id:
                            # 根据元素类型推断逻辑名称
                            logical_name = self._infer_logical_name(inp_id, inp_type)
                            if logical_name:
                                mappings[f"#{logical_name}"] = f"#{inp_id}"
                                mappings[f"[name='{logical_name}']"] = f"#{inp_id}"
                    except:
                        pass
                
                # 2. 获取所有按钮
                buttons = page.locator('button').all()
                for btn in buttons[:20]:
                    try:
                        btn_id = btn.get_attribute('id')
                        btn_text = btn.inner_text().strip()
                        
                        if btn_id:
                            logical_name = self._infer_logical_name(btn_id, 'button')
                            if logical_name:
                                mappings[f"#{logical_name}"] = f"#{btn_id}"
                        
                        if btn_text and len(btn_text) < 20:
                            mappings[f"button:has-text('{btn_text}')"] = f"button:has-text('{btn_text}')"
                    except:
                        pass
                
                browser.close()
                print(f"  ✅ 从实时页面学习到 {len(mappings)} 个映射")
                
        except Exception as e:
            print(f"  ⚠️ 实时学习失败: {e}")
        
        return mappings
    
    def _infer_logical_name(self, element_id: str, element_type: str) -> Optional[str]:
        """从元素 ID 推断逻辑名称"""
        # 移除常见前缀
        prefixes = ['form', 'btn', 'input', 'select', 'txt']
        name = element_id
        for prefix in prefixes:
            if name.startswith(prefix):
                name = name[len(prefix):]
                break
        
        # 转换为驼峰命名
        words = re.findall(r'[A-Z][a-z]*|[a-z]+', name)
        if words:
            result = words[0].lower() + ''.join(w.capitalize() for w in words[1:])
            return result
        
        return None


class UniversalSelectorFixer:
    """通用选择器修复器"""
    
    def __init__(self, cache_file: str = "test/ai/selector_cache.json"):
        self.cache_file = cache_file
        self.mappings = {}
        self.load_cache()
    
    def load_cache(self):
        """加载缓存的选择器映射"""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                self.mappings = json.load(f)
            print(f"📦 从缓存加载 {len(self.mappings)} 个选择器映射")
    
    def save_cache(self):
        """保存选择器映射到缓存"""
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.mappings, f, ensure_ascii=False, indent=2)
        print(f"💾 保存 {len(self.mappings)} 个选择器映射到缓存")
    
    def learn_selectors(self, html_path: str, base_url: Optional[str] = None):
        """学习选择器"""
        learner = SelectorLearner(html_path)
        
        # 从 HTML 静态学习
        static_mappings = learner.learn_from_html()
        self.mappings.update(static_mappings)
        
        # 从实时页面学习（如果提供了 URL）
        if base_url:
            live_mappings = learner.learn_from_live_page(base_url)
            self.mappings.update(live_mappings)
        
        self.save_cache()
        return self.mappings
    
    def fix_file(self, file_path: str, dry_run: bool = False) -> int:
        """修复文件中的选择器"""
        
        print(f"\n🔧 修复文件: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        fixes_count = 0
        applied_fixes = []
        
        # 按长度排序，优先匹配长的
        sorted_mappings = sorted(self.mappings.items(), key=lambda x: len(x[0]), reverse=True)
        
        for wrong, correct in sorted_mappings:
            if wrong in content and wrong != correct:
                # 使用单词边界匹配
                pattern = rf'(?<![#\.\["\']) {re.escape(wrong)}(?![#\.\-"\'])'
                if re.search(pattern, content):
                    content = content.replace(wrong, correct)
                    fixes_count += 1
                    applied_fixes.append(f"{wrong} -> {correct}")
                # 也直接替换
                elif wrong in content:
                    content = content.replace(wrong, correct)
                    fixes_count += 1
                    applied_fixes.append(f"{wrong} -> {correct}")
        
        # 智能修复：尝试模糊匹配
        if fixes_count == 0:
            fixes_count = self._fuzzy_fix(content, file_path)
        
        if fixes_count > 0:
            print(f"\n  ✅ 应用 {fixes_count} 处修复:")
            for fix in applied_fixes[:10]:
                print(f"     {fix}")
            if len(applied_fixes) > 10:
                print(f"     ... 还有 {len(applied_fixes) - 10} 处")
            
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"\n  💾 已保存修复")
        else:
            print(f"  ℹ️ 无需修复")
        
        return fixes_count
    
    def _fuzzy_fix(self, content: str, file_path: str) -> int:
        """模糊匹配修复"""
        # 提取所有选择器
        selectors = re.findall(r'(?:#|\.|\[)[^\s"\']+', content)
        
        fixed = content
        fixes = 0
        
        for selector in set(selectors):
            # 查找相似的选择器
            for wrong, correct in self.mappings.items():
                ratio = SequenceMatcher(None, selector.lower(), wrong.lower()).ratio()
                if ratio > 0.7 and selector != correct:
                    fixed = fixed.replace(selector, correct)
                    fixes += 1
                    print(f"     🔍 模糊匹配: {selector} -> {correct}")
        
        if fixes > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed)
        
        return fixes


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="通用选择器修复工具")
    parser.add_argument("--html", default="demo/activity_management.html", help="HTML 文件路径")
    parser.add_argument("--url", help="实时页面 URL（用于学习）")
    parser.add_argument("--test-file", help="要修复的测试文件路径")
    parser.add_argument("--learn-only", action="store_true", help="仅学习，不修复")
    parser.add_argument("--dry-run", action="store_true", help="仅显示修复内容，不保存")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🔧 通用选择器修复工具")
    print("=" * 60)
    
    # 初始化修复器
    fixer = UniversalSelectorFixer()
    
    # 学习选择器
    print(f"\n📚 从 {args.html} 学习选择器...")
    base_url = args.url if args.url else f"file:///{os.path.abspath(args.html)}"
    fixer.learn_selectors(args.html, base_url)
    
    if args.learn_only:
        print("\n✅ 学习完成，映射已保存")
        print(f"\n可用的选择器映射:")
        for wrong, correct in list(fixer.mappings.items())[:20]:
            print(f"  {wrong} -> {correct}")
        return
    
    # 查找要修复的文件
    if args.test_file:
        test_files = [args.test_file]
    else:
        test_files = glob.glob("test/ai/generated/*/generated_test.py")
    
    if not test_files:
        print("❌ 未找到测试文件")
        return
    
    # 修复所有文件
    for test_file in test_files:
        fixer.fix_file(test_file, dry_run=args.dry_run)


if __name__ == "__main__":
    main()