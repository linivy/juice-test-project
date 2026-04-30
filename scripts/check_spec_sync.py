#!/usr/bin/env python
"""
检查测试文件与规范的同步状态

使用方法:
    python scripts/check_spec_sync.py
    python scripts/check_spec_sync.py --add-markers
    python scripts/check_spec_sync.py --add-markers --force
"""

import re
import hashlib
from pathlib import Path
import sys
import platform

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
SPEC_FILE = PROJECT_ROOT / "test" / "cases" / "ui-testing-patterns.md"
TEST_DIR = PROJECT_ROOT / "test"

# 需要检查的文件模式
TEST_PATTERNS = [
    "test_*.py",
    "*_test.py",
]

# 排除的目录
EXCLUDE_DIRS = ["__pycache__", "venv", ".venv", "templates"]


def get_spec_hash() -> str:
    """获取规范文件的哈希值"""
    if not SPEC_FILE.exists():
        print(f"⚠️ 规范文件不存在: {SPEC_FILE}")
        return "no_spec"
    
    content = SPEC_FILE.read_text(encoding="utf-8")
    return hashlib.md5(content.encode()).hexdigest()[:8]


def get_spec_version() -> str:
    """从规范文件中提取版本号"""
    if not SPEC_FILE.exists():
        return "0.0.0"
    
    content = SPEC_FILE.read_text(encoding="utf-8")
    match = re.search(r'version:\s*(\d+\.\d+\.\d+)', content)
    if match:
        return match.group(1)
    
    match = re.search(r'-\s*version:\s*(\d+\.\d+\.\d+)', content)
    if match:
        return match.group(1)
    
    return "0.0.0"


def get_spec_last_updated() -> str:
    """获取规范最后更新时间"""
    if not SPEC_FILE.exists():
        return "unknown"
    
    content = SPEC_FILE.read_text(encoding="utf-8")
    match = re.search(r'last_updated:\s*(\d{4}-\d{2}-\d{2})', content)
    return match.group(1) if match else "unknown"


def extract_spec_info_from_file(file_path: Path) -> dict:
    """从测试文件中提取规范信息"""
    content = file_path.read_text(encoding="utf-8")
    
    info = {
        "spec_hash": None,
        "spec_version": None,
        "spec_last_updated": None,
        "has_spec_marker": False
    }
    
    # 检查 spec_hash
    match = re.search(r'spec_hash:\s*([a-f0-9]+)', content)
    if match:
        info["spec_hash"] = match.group(1)
        info["has_spec_marker"] = True
    
    # 检查 spec_version
    match = re.search(r'spec_version:\s*(\d+\.\d+\.\d+)', content)
    if match:
        info["spec_version"] = match.group(1)
    
    # 检查 spec_last_updated
    match = re.search(r'spec_last_updated:\s*(\d{4}-\d{2}-\d{2})', content)
    if match:
        info["spec_last_updated"] = match.group(1)
    
    return info


def remove_existing_markers(content: str) -> str:
    """移除文件中已有的规范标记"""
    marker_pattern = r'# ==================== 规范同步信息 ====================\n.*?# ===================================================\n\n'
    new_content = re.sub(marker_pattern, '', content, flags=re.DOTALL)
    new_content = re.sub(r'\n{3,}', '\n\n', new_content)
    return new_content


def add_spec_marker_to_file(file_path: Path, spec_hash: str, spec_version: str, spec_date: str, force: bool = False, dry_run: bool = False):
    """给测试文件添加规范标记"""
    content = file_path.read_text(encoding="utf-8")
    
    # 检查是否已有标记
    has_marker = re.search(r'spec_hash:', content) is not None
    
    if has_marker and not force:
        print(f"  ⏭️  {file_path.relative_to(PROJECT_ROOT)} 已有标记，跳过（使用 --force 强制覆盖）")
        return False
    
    if has_marker and force:
        content = remove_existing_markers(content)
        print(f"  🔄 移除旧标记: {file_path.relative_to(PROJECT_ROOT)}")
    
    marker = f'''# ==================== 规范同步信息 ====================
spec_file: test/cases/ui-testing-patterns.md
spec_version: {spec_version}
spec_hash: {spec_hash}
spec_last_updated: {spec_date}
# ===================================================

'''
    
    # 检查文件是否以 docstring 开头
    if content.strip().startswith('"""'):
        end_of_docstring = content.find('"""', 3)
        if end_of_docstring != -1:
            insert_pos = end_of_docstring + 3
            if content[insert_pos:insert_pos+1] == '\n':
                insert_pos += 1
            new_content = content[:insert_pos] + '\n' + marker + content[insert_pos:]
        else:
            new_content = marker + content
    else:
        new_content = marker + content
    
    if dry_run:
        print(f"  📝 将{'覆盖' if has_marker and force else '添加'}标记到: {file_path.relative_to(PROJECT_ROOT)}")
        return True
    
    file_path.write_text(new_content, encoding="utf-8")
    print(f"  ✅ 已{'覆盖' if has_marker and force else '添加'}标记: {file_path.relative_to(PROJECT_ROOT)}")
    return True


def find_test_files() -> list:
    """查找所有测试文件"""
    test_files = []
    
    for pattern in TEST_PATTERNS:
        for file_path in TEST_DIR.rglob(pattern):
            # 排除特定目录
            if any(exclude in file_path.parts for exclude in EXCLUDE_DIRS):
                continue
            test_files.append(file_path)
    
    return test_files


def check_sync_status():
    """检查所有测试文件的同步状态"""
    spec_hash = get_spec_hash()
    spec_version = get_spec_version()
    spec_date = get_spec_last_updated()
    
    print(f"\n📋 规范信息:")
    print(f"   - 文件: {SPEC_FILE.relative_to(PROJECT_ROOT) if SPEC_FILE.exists() else '不存在'}")
    print(f"   - 版本: {spec_version}")
    print(f"   - 哈希: {spec_hash}")
    print(f"   - 更新日期: {spec_date}")
    
    test_files = find_test_files()
    print(f"\n📁 找到 {len(test_files)} 个测试文件")
    
    missing_marker_files = []
    outdated_files = []
    synced_files = []
    
    for file_path in test_files:
        info = extract_spec_info_from_file(file_path)
        
        if not info["has_spec_marker"]:
            missing_marker_files.append(file_path)
        elif info["spec_hash"] != spec_hash:
            outdated_files.append((file_path, info["spec_hash"]))
        else:
            synced_files.append(file_path)
    
    print(f"\n📊 检查结果:")
    print(f"   ✅ 已同步: {len(synced_files)} 个文件")
    print(f"   ⚠️ 缺少标记: {len(missing_marker_files)} 个文件")
    print(f"   🔄 需要更新: {len(outdated_files)} 个文件")
    
    if missing_marker_files:
        print(f"\n⚠️ 缺少规范标记的文件:")
        for f in missing_marker_files:
            print(f"   - {f.relative_to(PROJECT_ROOT)}")
        print(f"\n💡 运行: python scripts/check_spec_sync.py --add-markers")
    
    if outdated_files:
        print(f"\n🔄 需要同步的文件:")
        for f, old_hash in outdated_files:
            print(f"   - {f.relative_to(PROJECT_ROOT)} (旧哈希: {old_hash})")
        print(f"\n💡 运行: python scripts/check_spec_sync.py --add-markers --force")
    
    return len(missing_marker_files) + len(outdated_files)


def add_markers_to_files(force: bool = False, dry_run: bool = False):
    """为缺少标记的文件添加标记"""
    spec_hash = get_spec_hash()
    spec_version = get_spec_version()
    spec_date = get_spec_last_updated()
    
    test_files = find_test_files()
    added_count = 0
    
    for file_path in test_files:
        info = extract_spec_info_from_file(file_path)
        
        if force or not info["has_spec_marker"]:
            if add_spec_marker_to_file(file_path, spec_hash, spec_version, spec_date, force=force, dry_run=dry_run):
                added_count += 1
    
    print(f"\n✅ 已{'覆盖' if force else '添加'} {added_count} 个文件的规范标记")
    return added_count


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="检查测试文件与规范的同步状态")
    parser.add_argument("--add-markers", action="store_true", help="为缺少标记的文件添加标记")
    parser.add_argument("--force", action="store_true", help="强制覆盖已有标记")
    parser.add_argument("--dry-run", action="store_true", help="预览将要执行的操作")
    
    args = parser.parse_args()
    
    if args.add_markers:
        add_markers_to_files(force=args.force, dry_run=args.dry_run)
    else:
        exit_code = check_sync_status()
        sys.exit(exit_code)


if __name__ == "__main__":
    main()