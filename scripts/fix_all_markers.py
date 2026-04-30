#!/usr/bin/env python
"""批量修复测试文件中的规范标记格式"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
TEST_DIR = PROJECT_ROOT / "test"


def fix_file(file_path: Path) -> bool:
    """修复单个文件"""
    content = file_path.read_text(encoding="utf-8")
    original = content
    
    # 模式1: 匹配 """ ... """ 格式的标记块
    pattern1 = r'"""\s*\n# ==================== 规范同步信息 ====================\n(.*?)\n# ===================================================\n\s*"""'
    
    def replacement(match):
        inner = match.group(1)
        return f'# ==================== 规范同步信息 ====================\n{inner}\n# ===================================================\n'
    
    content = re.sub(pattern1, replacement, content, flags=re.DOTALL)
    
    # 确保每行都有 # 前缀（除了空行）
    lines = content.split('\n')
    new_lines = []
    in_spec_block = False
    
    for line in lines:
        if '# ==================== 规范同步信息 ====================' in line:
            in_spec_block = True
            new_lines.append(line)
        elif '# ===================================================' in line:
            in_spec_block = False
            new_lines.append(line)
        elif in_spec_block and line.strip() and not line.strip().startswith('#'):
            # 添加 # 前缀
            new_lines.append(f'# {line}')
        else:
            new_lines.append(line)
    
    content = '\n'.join(new_lines)
    
    if content != original:
        file_path.write_text(content, encoding="utf-8")
        print(f"✅ 修复: {file_path.relative_to(PROJECT_ROOT)}")
        return True
    
    return False


def find_test_files():
    """查找所有测试文件"""
    test_files = []
    for pattern in ["test_*.py", "*_test.py"]:
        for file_path in TEST_DIR.rglob(pattern):
            if any(exclude in file_path.parts for exclude in ["__pycache__", "venv", ".venv", "templates"]):
                continue
            # 排除非测试文件
            if file_path.name in ["generator.py"]:
                continue
            test_files.append(file_path)
    return test_files


def main():
    print("🔧 开始修复测试文件...\n")
    
    test_files = find_test_files()
    print(f"找到 {len(test_files)} 个文件\n")
    
    fixed = 0
    for file_path in test_files:
        if fix_file(file_path):
            fixed += 1
    
    print(f"\n✅ 修复了 {fixed} 个文件")


if __name__ == "__main__":
    main()