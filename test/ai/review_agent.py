#!/usr/bin/env python
"""AI 测试 Review Agent - 自动审查测试点和测试代码"""

import os
import re
from typing import Dict, Any, List, Optional
from openai import OpenAI


class TestReviewAgent:
    """测试审查智能体 - 通用版"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "deepseek-chat"):
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("请设置 DEEPSEEK_API_KEY 环境变量")
        
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com/v1")
        self.model = model
    
    def review_test_points(self, requirement: str, test_points: str) -> Dict[str, Any]:
        """审查功能测试点"""
        prompt = f"""
你是一位资深的测试架构师，请审查以下测试点是否完整覆盖了需求。

## 原始需求
{requirement}

## 生成的测试点
{test_points}

## 审查要求
请从以下维度进行分析：

### 1. 覆盖度分析
- 需求中的每个功能点是否都有对应的测试点？
- 哪些功能点没有被覆盖？

### 2. 测试类型完整性
- 正向流程是否覆盖？
- 异常流程是否覆盖？
- 边界值是否覆盖？
- 安全测试是否覆盖？

### 3. 优先级合理性
- P0/P1/P2 分级是否合理？
- 是否有重要的功能被标记为低优先级？

### 4. 遗漏检测
- 列出所有遗漏的测试场景
- 列出需求中隐含但未明确的测试点

### 5. 改进建议
- 哪些测试点需要补充？
- 哪些测试点描述不够清晰？

## 输出格式
请按以下格式输出：

### 一、覆盖度评估
- 覆盖率：X%
- 已覆盖功能点：[列表]
- 未覆盖功能点：[列表]

### 二、测试类型完整性
| 测试类型 | 是否覆盖 | 数量 | 评价 |
|---------|---------|------|------|

### 三、优先级评估
- 分级合理：是/否
- 建议调整：[列表]

### 四、遗漏清单
- [遗漏场景1]
- [遗漏场景2]

### 五、改进建议
- [建议1]
- [建议2]

### 六、整体评分
- 覆盖度：⭐️⭐️⭐️⭐️⭐️
- 质量：⭐️⭐️⭐️⭐️⭐️
- 综合评分：X/10
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=3000
        )
        
        content = response.choices[0].message.content
        score = self._extract_score(content)
        
        return {
            "review": content,
            "score": score,
            "type": "test_points"
        }
    def review_test_code(self, requirement: str, test_code: str, test_points: str = None) -> Dict[str, Any]:
        """审查自动化测试代码"""
        test_points_section = f"\n## 对应的测试点\n{test_points}" if test_points else ""
        
        prompt = f"""
你是一位资深的测试开发工程师，请审查以下自动化测试代码的质量。

## 原始需求
{requirement}
{test_points_section}

## 生成的测试代码
```python
{test_code}
```

## 审查要求
请从以下维度进行分析：

### 1. 代码结构
- 类和方法命名是否规范？
- 是否有重复代码？
- 代码是否易于维护？

### 2. 断言质量
- 断言是否充分？
- 断言消息是否有意义？
- 是否验证了关键的成功/失败条件？

### 3. 元素定位
- 选择器是否稳定（优先使用 ID）？
- 是否考虑了元素等待？

### 4. 测试数据
- 测试数据是否合理？
- 是否使用了参数化？

### 5. 错误处理
- 是否有适当的异常处理？
- 失败时是否有截图/日志？

### 6. 与需求的对齐
- 测试代码是否覆盖了所有测试点？
- 是否有遗漏的测试场景？
"""
        prompt += """
## 输出格式
### 一、整体评价
- 代码质量：优秀/良好/一般/需改进
- 可维护性：优秀/良好/一般/需改进

### 二、问题清单
| 问题类型 | 问题描述 | 严重程度 | 建议修复 |
|---------|---------|---------|---------|

### 三、改进建议
- [建议1]
- [建议2]

### 四、代码质量评分
- 结构：X/10
- 断言：X/10
- 元素定位：X/10
- 数据：X/10
- 错误处理：X/10
- **综合：X/10**
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=4000
        )
        
        content = response.choices[0].message.content
        score = self._extract_score(content)
        
        return {
            "review": content,
            "score": score,
            "type": "test_code"
        }
    def review_all(self, requirement: str, test_points: str, test_code: str) -> Dict[str, Any]:
        """全面审查（测试点 + 代码）"""
        print("\n🔍 开始审查测试点...")
        points_result = self.review_test_points(requirement, test_points)
        
        print("\n🔍 开始审查测试代码...")
        code_result = self.review_test_code(requirement, test_code, test_points)
        
        summary = self._generate_summary(points_result, code_result)
        
        return {
            "test_points_review": points_result,
            "test_code_review": code_result,
            "summary": summary
        }