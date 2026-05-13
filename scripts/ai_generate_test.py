#!/usr/bin/env python
"""AI 测试用例生成器命令行工具"""

import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test.ai.test_generator import AITestGenerator


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="AI 测试用例生成器")
    parser.add_argument("-r", "--requirement", required=True, help="需求描述或文件路径")
    parser.add_argument("-m", "--module", required=True, help="模块名称（如 ACTIVITY）")
    parser.add_argument("-f", "--feature", required=True, help="功能名称（如 创建活动）")
    parser.add_argument("--project", default="juice", help="项目名称（juice/activity）")
    parser.add_argument("-o", "--output-name", default=None, help="输出文件名标识（用于区分不同需求）")
    parser.add_argument("--save", action="store_true", default=True, help="保存到文件")
    parser.add_argument("--no-save", action="store_true", help="不保存到文件")
    
    args = parser.parse_args()
    
    # 读取需求文件
    requirement_path = args.requirement
    if os.path.isfile(requirement_path):
        with open(requirement_path, 'r', encoding='utf-8') as f:
            requirement = f.read()
        print(f"📖 需求长度: {len(requirement)} 字符")
    else:
        requirement = requirement_path
        print(f"📖 需求长度: {len(requirement)} 字符")
    
    # 创建生成器
    generator = AITestGenerator(project=args.project)
    
    # 确定输出标识
    output_name = args.output_name
    if output_name is None and os.path.isfile(args.requirement):
        output_name = args.requirement
    
    print(f"🚀 使用逐个生成模式...")
    
    # 生成测试用例
    result = generator.generate_in_batches(
        requirement, 
        args.module, 
        args.feature,
        batch_size=5
    )
    
    # 保存结果 - 传递需求标识
    if not args.no_save and result.get("test_code"):
        # 使用带需求标识的保存方法
        generator.save_to_file(result, requirement_info=output_name)
    
    # 打印预览
    if result.get("test_points"):
        print("\n" + "=" * 60)
        print("📋 测试点预览")
        print("=" * 60)
        preview = result["test_points"][:800]
        print(preview)
        if len(result["test_points"]) > 800:
            print("\n... (完整内容请查看生成的 test_points.md 文件)")
    else:
        print("\n⚠️ 没有生成测试点")
    
    return result


if __name__ == "__main__":
    main()