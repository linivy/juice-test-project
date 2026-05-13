# test/ai/test_validator.py
"""测试用例验证器 - 验证选择器有效性和代码质量，支持自动修复"""

import os
import re
import ast
import shutil
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️ 未安装 playwright，选择器验证功能将不可用")


class TestValidator:
    """测试代码验证器"""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url
        self.issues = []
    
    def validate_syntax(self, code: str) -> Tuple[bool, Optional[SyntaxError]]:
        """验证语法，返回 (是否通过, 错误对象)"""
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            self.issues.append(f"语法错误: {e}")
            return False, e
    
    def validate_imports(self, code: str) -> List[str]:
        """验证导入"""
        missing = []
        required = ['pytest', 'allure', 'playwright']
        
        for imp in required:
            if imp not in code:
                missing.append(imp)
        
        return missing
    
    def validate_test_structure(self, code: str) -> List[str]:
        """验证测试结构"""
        issues = []
        
        if not re.search(r'class\s+Test\w+:', code):
            issues.append("缺少测试类定义")
        
        test_methods = re.findall(r'def test_\w+\(', code)
        if not test_methods:
            issues.append("未找到测试方法")
        
        if 'BASE_URL' not in code:
            issues.append("缺少 BASE_URL 定义")
        
        if 'if __name__ == "__main__"' not in code:
            issues.append("缺少主函数入口")
        
        return issues
    
    def validate_assertions(self, code: str) -> List[str]:
        """验证断言"""
        issues = []
        
        if 'expect(' not in code and 'assert ' not in code:
            issues.append("代码中缺少断言语句")
        
        js_patterns = [
            (r'\.toBeVisible\(', 'JavaScript风格断言，应改为 .to_be_visible()'),
            (r'\.toHaveText\(', 'JavaScript风格断言，应改为 .to_have_text()'),
        ]
        
        for pattern, msg in js_patterns:
            if re.search(pattern, code):
                issues.append(msg)
        
        return issues
    
    def validate_selectors(self, test_code: str) -> List[Dict]:
        """验证测试代码中的选择器是否有效"""
        if not PLAYWRIGHT_AVAILABLE or not self.base_url:
            return []
        
        selectors = self._extract_selectors(test_code)
        results = []
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(self.base_url, timeout=5000, wait_until="domcontentloaded")
                
                for selector in selectors[:30]:  # 限制数量
                    try:
                        count = page.locator(selector).count()
                        results.append({
                            "selector": selector,
                            "valid": count > 0,
                            "count": count
                        })
                        if count == 0:
                            self.issues.append(f"❌ 无效选择器: {selector}")
                    except Exception as e:
                        results.append({
                            "selector": selector,
                            "valid": False,
                            "count": 0
                        })
                browser.close()
        except Exception as e:
            print(f"  ⚠️ 选择器验证失败: {e}")
        
        return results
    
    def _extract_selectors(self, code: str) -> List[str]:
        """从代码中提取选择器"""
        patterns = [
            r'page\.locator\(["\']([^"\']+)["\']\)',
            r'page\.fill\(["\']([^"\']+)["\']',
            r'page\.click\(["\']([^"\']+)["\']',
            r'page\.select_option\(["\']([^"\']+)["\']',
            r'page\.wait_for_selector\(["\']([^"\']+)["\']',
        ]
        
        selectors = []
        for pattern in patterns:
            matches = re.findall(pattern, code)
            selectors.extend(matches)
        
        return list(set(selectors))
    
    def generate_report(self) -> str:
        """生成验证报告"""
        if not self.issues:
            return "✅ 所有验证通过！"
        
        report = "📋 验证报告:\n" + "=" * 50 + "\n"
        for issue in self.issues[:20]:
            report += f"  • {issue}\n"
        if len(self.issues) > 20:
            report += f"  ... 还有 {len(self.issues) - 20} 个问题\n"
        return report


class TestAutoFixer:
    """自动修复测试代码"""
    
    def __init__(self):
        self.fixes_applied = []
    
    def create_backup(self, file_path: str) -> str:
        """创建备份文件"""
        backup_path = file_path.replace('.py', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.py')
        shutil.copy(file_path, backup_path)
        return backup_path
    
    def fix_selectors(self, code: str) -> str:
        """修复选择器中的双井号和 .# 问题"""
        fixed = code
        
        # 修复双井号 ## -> #
        fixed = re.sub(r'##([a-zA-Z#])', r'#\1', fixed)
        fixed = fixed.replace('##', '#')
        
        # 修复 .# 问题
        fixed = fixed.replace('.#', '#')
        
        # 修复 wait_for_selector
        fixed = fixed.replace('page.wait_for_selector(".#toast-message, .#toast"', 'page.wait_for_selector("#toast"')
        
        if fixed != code:
            self.fixes_applied.append("修复选择器格式 (## -> #)")
        
        return fixed
    
    def fix_assertions(self, code: str) -> str:
        """修复断言语法"""
        fixed = code
        
        assertion_fixes = [
            (r'\.toBeVisible\(\)', '.to_be_visible()'),
            (r'\.toBeHidden\(\)', '.to_be_hidden()'),
            (r'\.toHaveText\(', '.to_have_text('),
            (r'\.toHaveValue\(', '.to_have_value('),
            (r'\.toHaveCount\(', '.to_have_count('),
            (r'\.toContainText\(', '.to_contain_text('),
        ]
        
        for old, new in assertion_fixes:
            fixed = fixed.replace(old, new)
        
        if fixed != code:
            self.fixes_applied.append("修复断言语法")
        
        return fixed
    
    def fix_missing_imports(self, code: str) -> str:
        """添加缺失的导入"""
        required_imports = [
            'import pytest',
            'import allure',
            'from playwright.sync_api import expect'
        ]
        
        lines = code.split('\n')
        existing_imports = set()
        
        for line in lines:
            if line.startswith('import ') or line.startswith('from '):
                existing_imports.add(line.strip())
        
        missing_imports = [imp for imp in required_imports if imp not in existing_imports]
        
        if missing_imports:
            # 在文件开头添加导入
            insert_at = 0
            for i, line in enumerate(lines):
                if line.strip() and not (line.startswith('import ') or line.startswith('from ')):
                    insert_at = i
                    break
            
            for imp in reversed(missing_imports):
                lines.insert(insert_at, imp)
            
            self.fixes_applied.append(f"添加缺失导入: {', '.join(missing_imports)}")
        
        return '\n'.join(lines)
    
    def fix_main_block(self, code: str) -> str:
        """修复主函数位置"""
        if 'if __name__ == "__main__"' in code:
            # 确保主函数在类外部
            lines = code.split('\n')
            new_lines = []
            main_block = []
            in_main = False
            
            for line in lines:
                if 'if __name__ == "__main__"' in line:
                    in_main = True
                    # 移除缩进
                    main_block.append(line.strip())
                elif in_main:
                    if line.strip() and not line.startswith('    '):
                        in_main = False
                        new_lines.append(line)
                    else:
                        main_block.append(line.strip() if line.strip() else '')
                else:
                    new_lines.append(line)
            
            if main_block:
                new_lines.append('')
                new_lines.extend(main_block)
                self.fixes_applied.append("移动主函数到类外部")
                return '\n'.join(new_lines)
        
        return code
    
    def fix_all(self, code: str) -> Tuple[str, List[str]]:
        """执行所有自动修复"""
        fixed = code
        self.fixes_applied = []
        
        fixed = self.fix_missing_imports(fixed)
        fixed = self.fix_assertions(fixed)
        fixed = self.fix_selectors(fixed)
        # fixed = self.fix_main_block(fixed)  # 暂时禁用主函数修复
        
        return fixed, self.fixes_applied


def validate_and_fix(file_path: str, base_url: Optional[str] = None, auto_fix: bool = True) -> Dict[str, Any]:
    """验证并自动修复测试代码"""
    
    print("\n" + "=" * 70)
    print("🔍 测试代码验证与自动修复")
    print("=" * 70)
    
    if not os.path.exists(file_path):
        return {"success": False, "error": f"文件不存在: {file_path}"}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        original_code = f.read()
    
    print(f"📄 文件: {file_path}")
    print(f"📊 原始大小: {len(original_code)} 字符, {len(original_code.splitlines())} 行")
    
    # 1. 验证
    print("\n" + "─" * 50)
    print("📋 第1步: 验证代码")
    print("─" * 50)
    
    validator = TestValidator(base_url)
    
    syntax_ok, syntax_error = validator.validate_syntax(original_code)
    print(f"  {'✅' if syntax_ok else '❌'} 语法检查: {'通过' if syntax_ok else f'失败 - {syntax_error}'}")
    
    missing_imports = validator.validate_imports(original_code)
    if missing_imports:
        print(f"  ⚠️ 缺失导入: {', '.join(missing_imports)}")
    
    structure_issues = validator.validate_test_structure(original_code)
    for issue in structure_issues:
        print(f"  ⚠️ {issue}")
    
    # 2. 自动修复
    if auto_fix:
        print("\n" + "─" * 50)
        print("🔧 第2步: 自动修复问题")
        print("─" * 50)
        
        fixer = TestAutoFixer()
        backup_path = fixer.create_backup(file_path)
        print(f"  📁 备份已创建: {backup_path}")
        
        fixed_code, fixes = fixer.fix_all(original_code)
        
        for fix in fixes:
            print(f"  ✅ {fix}")
        
        if not fixes:
            print("  ✅ 无需修复")
        
        if fixes or fixed_code != original_code:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_code)
            print(f"\n  💾 已保存修复后的代码")
            
            # 再次验证
            try:
                ast.parse(fixed_code)
                print(f"  ✅ 修复后语法正确")
            except SyntaxError as e:
                print(f"  ⚠️ 修复后仍有语法错误: {e}")
        else:
            print("  ℹ️ 无需保存")
    else:
        fixed_code = original_code
        fixes = []
    
    # 3. 报告
    print("\n" + "=" * 70)
    print("📊 第3步: 验证报告")
    print("=" * 70)
    
    final_syntax_ok, _ = validator.validate_syntax(fixed_code)
    
    result = {
        "success": final_syntax_ok,
        "original_size": len(original_code),
        "fixed_size": len(fixed_code),
        "fixes_applied": fixes,
        "backup_path": backup_path if auto_fix else None,
    }
    
    print(f"  • 语法正确: {'是' if final_syntax_ok else '否'}")
    print(f"  • 应用修复: {len(fixes)} 处")
    print(f"  • 代码变化: {len(original_code)} → {len(fixed_code)} 字符")
    
    if result["success"]:
        print("\n✅ 验证通过！可以运行测试了")
    else:
        print("\n⚠️ 验证未完全通过，建议手动检查")
    
    return result


def validate_generated_test(test_file_path: str, base_url: str) -> Dict[str, Any]:
    """兼容旧接口的验证函数"""
    return validate_and_fix(test_file_path, base_url, auto_fix=True)


if __name__ == "__main__":
    import glob
    
    files = glob.glob("test/ai/generated/*/generated_test.py")
    
    if not files:
        print("❌ 未找到生成的测试文件")
        print("\n请先运行生成器:")
        print("  python scripts/ai_generate_test.py -r Requirements/活动管理_01_创建活动.md -m ACTIVITY -f 创建活动 --project activity")
        exit(1)
    
    test_file = files[0]
    base_url = "file:///C:/Users/ivy.wang/Desktop/juice-test-project/demo/activity_management.html"
    
    result = validate_and_fix(test_file, base_url, auto_fix=True)
    exit(0 if result["success"] else 1)