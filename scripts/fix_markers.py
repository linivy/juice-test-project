#!/usr/bin/env python
"""修复测试文件中的规范标记格式"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
TEST_DIR = PROJECT_ROOT / "test"

# 排除的目录
EXCLUDE_DIRS = ["__pycache__", "venv", ".venv", "templates"]


def fix_marker_format(file_path: Path):
    """将字符串格式的标记改为注释格式"""
    try:
        content = file_path.read_text(encoding="utf-8")
    except PermissionError:
        print(f"  ⚠️ 跳过（文件被占用）: {file_path.relative_to(PROJECT_ROOT)}")
        return False
    
    # 匹配字符串格式的标记块
    pattern = r'"""\n# ==================== 规范同步信息 ====================\n(.*?)\n# ===================================================\n"""'
    
    def replace_match(match):
        inner_content = match.group(1)
        return f'# ==================== 规范同步信息 ====================\n{inner_content}\n# ===================================================\n'
    
    new_content = re.sub(pattern, replace_match, content, flags=re.DOTALL)
    
    if new_content != content:
        file_path.write_text(new_content, encoding="utf-8")
        print(f"  ✅ 修复: {file_path.relative_to(PROJECT_ROOT)}")
        return True
    return False


def find_test_files():
    """查找所有测试文件"""
    test_files = []
    for pattern in ["test_*.py", "*_test.py"]:
        for file_path in TEST_DIR.rglob(pattern):
            # 排除特定目录
            parts = file_path.parts
            if any(exclude in parts for exclude in EXCLUDE_DIRS):
                continue
            test_files.append(file_path)
    return test_files


def main():
    print("🔧 开始修复测试文件中的规范标记格式...\n")
    
    test_files = find_test_files()
    print(f"找到 {len(test_files)} 个测试文件\n")
    
    fixed_count = 0
    for file_path in test_files:
        if fix_marker_format(file_path):
            fixed_count += 1
    
    print(f"\n✅ 修复了 {fixed_count} 个文件的标记格式")


if __name__ == "__main__":
    main()