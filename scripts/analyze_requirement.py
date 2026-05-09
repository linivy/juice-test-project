#!/usr/bin/env python
"""需求阶段测试点生成器 - 不需要选择器"""

import sys
import os
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from test.ai.prompts_requirement import (
    REQUIREMENT_TEST_POINTS_PROMPT,
    REQUIREMENT_REVIEW_PROMPT,
    REQUIREMENT_CHECKLIST_PROMPT
)
from openai import OpenAI


class RequirementAnalyzer:
    """需求阶段分析器 - 不依赖开发环境"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("请设置 DEEPSEEK_API_KEY 环境变量")
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com/v1")
    
    def generate_test_points(self, requirement: str, module_name: str, feature_name: str) -> str:
        """生成测试点（用于产品/开发评审）"""
        prompt = REQUIREMENT_TEST_POINTS_PROMPT.format(
            module_name=module_name.upper(),
            feature_name=feature_name,
            requirement=requirement
        )
        
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=3000
        )
        return response.choices[0].message.content
    
    def check_completeness(self, requirement: str) -> str:
        """需求完整性检查"""
        prompt = REQUIREMENT_CHECKLIST_PROMPT.format(requirement=requirement)
        
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=2000
        )
        return response.choices[0].message.content

def main():
    parser = argparse.ArgumentParser(description="需求阶段测试点生成器")
    parser.add_argument("-r", "--requirement", required=True, help="需求描述")
    parser.add_argument("-m", "--module", required=True, help="模块名称")
    parser.add_argument("-f", "--feature", required=True, help="功能名称")
    parser.add_argument("--check", action="store_true", help="需求完整性检查")
    parser.add_argument("--output", "-o", type=str, help="输出文件路径")
    
    args = parser.parse_args()
    
    analyzer = RequirementAnalyzer()
    
    if args.check:
        result = analyzer.check_completeness(args.requirement)
        print("=" * 60)
        print("📋 需求完整性检查")
        print("=" * 60)
        print(result)
    else:
        result = analyzer.generate_test_points(args.requirement, args.module, args.feature)
        print("=" * 60)
        print("📋 测试点（用于需求评审）")
        print("=" * 60)
        print(result)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"\n✅ 已保存到 {args.output}")

if __name__ == "__main__":
    main()