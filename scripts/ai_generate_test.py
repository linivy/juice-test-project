#!/usr/bin/env python
"""AI 测试用例生成命令行工具"""

import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test.ai.test_generator import AITestGenerator


def read_requirement(input_arg: str) -> str:
    """如果输入是文件路径，读取文件内容；否则直接返回字符串"""
    if os.path.isfile(input_arg):
        with open(input_arg, 'r', encoding='utf-8') as f:
            return f.read()
    return input_arg


def main():
    parser = argparse.ArgumentParser(description="AI 测试用例生成器")
    parser.add_argument("-r", "--requirement", required=True, help="需求描述或文件路径")
    parser.add_argument("-m", "--module", required=True, help="模块名称")
    parser.add_argument("-f", "--feature", required=True, help="功能名称")
    parser.add_argument("-p", "--path", default=None, help="页面路径")
    parser.add_argument("--save", action="store_true", help="保存到文件")
    parser.add_argument("--api-key", type=str, help="DeepSeek API Key")
    parser.add_argument("--project", type=str, default="juice", help="项目名称: juice, activity")
    parser.add_argument("--batch", action="store_true", help="使用分批生成模式（推荐，避免截断）")
    parser.add_argument("--batch-size", type=int, default=5, help="每批生成的测试点数量（默认5）")
    
    args = parser.parse_args()
    
    # 支持从文件读取需求
    requirement = read_requirement(args.requirement)
    print(f"📖 需求长度: {len(requirement)} 字符")
    
    generator = AITestGenerator(api_key=args.api_key, project=args.project)
    
    if args.batch:
        print("🚀 使用分批生成模式...")
        result = generator.generate_in_batches(
            requirement=requirement,
            module_name=args.module,
            feature_name=args.feature,
            batch_size=args.batch_size
        )
    else:
        print("🚀 使用一次性生成模式...")
        result = generator.generate_complete_test_case(
            requirement=requirement,
            module_name=args.module,
            feature_name=args.feature,
            page_path=args.path
        )
    
    print("=" * 60)
    print("📋 测试点预览")
    print("=" * 60)
    preview = result["test_points"][:800]
    print(preview + ("..." if len(result["test_points"]) > 800 else ""))
    
    if args.save:
        generator.save_to_file(result)
        print("\n✅ 已保存到文件")


if __name__ == "__main__":
    main()