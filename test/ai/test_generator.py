# test/ai/test_generator.py
"""AI 测试用例生成器 - 支持多项目、分批生成、长需求处理"""

import os
import re
from typing import Optional, Dict, Any, List
from openai import OpenAI

from .prompts import build_project_context, get_test_categories, TEST_POINTS_PROMPT, TEST_DATA_PROMPT, CODE_GENERATION_PROMPT
from .config import get_config
from concurrent.futures import ThreadPoolExecutor, as_completed


class AITestGenerator:
    """AI 测试用例生成器"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "deepseek-chat", project: str = "juice"):
        """
        初始化 AI 生成器
        
        Args:
            api_key: DeepSeek API Key
            model: 模型名称
            project: 项目名称（juice / activity）
        """
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("请设置 DEEPSEEK_API_KEY 环境变量")
        
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com/v1")
        self.model = model
        self.project = project
        self.config = get_config(project)
        self.html_selectors = self._parse_html_selectors() if project == "activity" else {}
    
    def _parse_html_selectors(self) -> dict:
        """解析 HTML 文件，提取实际的选择器"""
        html_path = self.config.get("html_file_path", "activity_management.html")
        if not os.path.exists(html_path):
            print(f"⚠️ HTML 文件不存在: {html_path}")
            return {}
        
        try:
            from bs4 import BeautifulSoup
            with open(html_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
            
            selectors = {
                "ids": [],
                "buttons": [],
                "modals": [],
            }
            
            for tag in soup.find_all(id=True):
                selectors["ids"].append(tag['id'])
            
            for btn in soup.find_all(['button', 'input']):
                if btn.get('type') in ['submit', 'button'] or btn.name == 'button':
                    text = btn.get_text().strip() or btn.get('value', '')
                    if text:
                        selectors["buttons"].append({"text": text, "id": btn.get('id', '')})
                    if btn.get('id'):
                        selectors["ids"].append(btn['id'])
            
            for modal in soup.find_all(class_=re.compile(r'modal', re.I)):
                if modal.get('id'):
                    selectors["modals"].append(modal['id'])
            
            print(f"📄 从 HTML 解析到 {len(selectors['ids'])} 个 ID, {len(selectors['buttons'])} 个按钮")
            return selectors
            
        except ImportError:
            print("⚠️ 未安装 beautifulsoup4，跳过 HTML 解析。安装: pip install beautifulsoup4")
            return {}
        except Exception as e:
            print(f"⚠️ HTML 解析失败: {e}")
            return {}
    
    def _extract_p0_points(self, test_points: str) -> List[str]:
        """从测试点中提取 P0 级别的测试点"""
        lines = test_points.split('\n')
        p0_points = []
        in_p0 = False
        
        for line in lines:
            if 'P0' in line or '### P0' in line:
                in_p0 = True
                continue
            if in_p0 and ('P1' in line or '### P1' in line or 'P2' in line):
                in_p0 = False
            if in_p0 and line.strip().startswith('-'):
                p0_points.append(line.strip())
        
        return p0_points
    
    def _extract_p1_points(self, test_points: str) -> List[str]:
        """从测试点中提取 P1 级别的测试点"""
        lines = test_points.split('\n')
        p1_points = []
        in_p1 = False
        
        for line in lines:
            if 'P1' in line or '### P1' in line:
                in_p1 = True
                continue
            if in_p1 and ('P2' in line or '### P2' in line):
                in_p1 = False
            if in_p1 and line.strip().startswith('-'):
                p1_points.append(line.strip())
        
        return p1_points
    
    def _extract_p2_points(self, test_points: str) -> List[str]:
        """从测试点中提取 P2 级别的测试点"""
        lines = test_points.split('\n')
        p2_points = []
        in_p2 = False
        
        for line in lines:
            if 'P2' in line or '### P2' in line:
                in_p2 = True
                continue
            if in_p2 and line.strip().startswith('-'):
                p2_points.append(line.strip())
        
        return p2_points
    
    def _chunk_list(self, lst: List, size: int) -> List[List]:
        """将列表分批"""
        for i in range(0, len(lst), size):
            yield lst[i:i+size]
    
    def _chunk_requirement(self, requirement: str, chunk_size: int = 3000) -> List[str]:
        """将长需求拆分为多个小块"""
        lines = requirement.split('\n')
        chunks = []
        current_chunk = []
        current_len = 0
        
        for line in lines:
            if current_len + len(line) > chunk_size and current_chunk:
                chunks.append('\n'.join(current_chunk))
                current_chunk = [line]
                current_len = len(line)
            else:
                current_chunk.append(line)
                current_len += len(line)
        
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
        
        return chunks
    
    def generate_test_points(self, requirement: str, module_name: str, feature_name: str) -> str:
        """生成功能测试点"""
        project_context = build_project_context(self.config)
        test_categories = get_test_categories("all")
        
        # 添加页面类型说明
        page_type = self.config.get("page_type", "multi_page")
        if page_type == "single_page_app":
            project_context += f"""
## 页面类型说明
- 这是一个单页面应用（SPA），所有功能在同一页面
- 不需要单独的登录步骤
- 直接访问 {self.config.get('base_url', '')} 即可
- 使用右上角角色切换下拉框来测试权限
"""
        
        prompt = TEST_POINTS_PROMPT.format(
            project_context=project_context,
            module_name=module_name.upper(),
            feature_name=feature_name,
            requirement=requirement,
            test_categories=test_categories
        )
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=4000
        )
        return response.choices[0].message.content
    
    def generate_test_data(self, test_points: str) -> str:
        """根据测试点生成参数化测试数据"""
        prompt = TEST_DATA_PROMPT.format(test_points=test_points)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=4000
        )
        return response.choices[0].message.content
    
    def generate_test_code(self, test_data: str, module_name: str, feature_name: str, page_path: str = None) -> str:
        """生成 pytest 测试代码"""
        if page_path is None:
            page_path = self.config.get("page_path", "/")
        
        project_context = build_project_context(self.config)
        
        # 添加实际选择器信息
        if self.html_selectors and self.html_selectors.get("ids"):
            selectors_info = "\n## 页面实际可用的选择器（从 HTML 解析，请优先使用这些）\n"
            selectors_info += f"- 页面中的 ID: {', '.join(self.html_selectors['ids'][:30])}\n"
            if self.html_selectors.get("buttons"):
                selectors_info += f"- 按钮文本: {', '.join([b['text'] for b in self.html_selectors['buttons'][:10]])}\n"
            project_context += selectors_info
        
        prompt = CODE_GENERATION_PROMPT.format(
            project_context=project_context,
            test_data=test_data,
            module_name=module_name.upper(),
            feature_name=feature_name,
            page_path=page_path
        )
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=3000
        )
        return response.choices[0].message.content
    
    def generate_batch_code(self, batch_points: List[str], module_name: str, feature_name: str) -> str:
        """为一批测试点生成代码"""
        batch_text = "\n".join(batch_points)
        return self.generate_test_code(batch_text, module_name, feature_name)
    
    def generate_complete_test_case(self, requirement: str, module_name: str, feature_name: str, page_path: str = None) -> Dict[str, Any]:
        """一次性生成完整的测试用例"""
        print(f"\n正在为 [{module_name}] 生成测试用例...")
        
        print("  步骤1: 生成功能测试点...")
        test_points = self.generate_test_points(requirement, module_name, feature_name)
        if "[COMPLETE]" not in test_points:
            print("  ⚠️ 测试点可能不完整，请检查输出")
        
        print("  步骤2: 生成参数化测试数据...")
        test_data = self.generate_test_data(test_points)
        if "[COMPLETE]" not in test_data:
            print("  ⚠️ 测试数据可能不完整，请检查输出")
        
        print("  步骤3: 生成 pytest 测试代码...")
        test_code = self.generate_test_code(test_data, module_name, feature_name, page_path)
        if "[COMPLETE]" not in test_code:
            print("  ⚠️ 测试代码可能不完整，请检查输出")
        
        print("  完成！\n")
        
        return {
            "test_points": test_points,
            "test_data": test_data,
            "test_code": test_code
        }
    
    def generate_in_batches(self, requirement: str, module_name: str, feature_name: str, batch_size: int = 5) -> Dict[str, Any]:
        """
        分批生成测试用例（解决输出截断问题）
        
        改进：如果需求太长，先对需求进行分块
        """
        print(f"\n📋 步骤1：分析需求...")
        print(f"  需求长度: {len(requirement)} 字符")
        
        # 如果需求太长（超过 3000 字符），先拆分需求
        if len(requirement) > 3000:
            print(f"  ⚠️ 需求较长，将拆分为多个部分...")
            requirement_chunks = self._chunk_requirement(requirement, 2500)
            print(f"  拆分为 {len(requirement_chunks)} 个部分")
            
            all_p0_points = []
            all_p1_points = []
            all_p2_points = []
            
            for i, chunk in enumerate(requirement_chunks, 1):
                print(f"\n  📝 处理需求部分 {i}/{len(requirement_chunks)}...")
                test_points = self.generate_test_points(chunk, module_name, feature_name)
                
                p0_points = self._extract_p0_points(test_points)
                p1_points = self._extract_p1_points(test_points)
                p2_points = self._extract_p2_points(test_points)
                
                all_p0_points.extend(p0_points)
                all_p1_points.extend(p1_points)
                all_p2_points.extend(p2_points)
                
                print(f"    本节 P0: {len(p0_points)} 个, P1: {len(p1_points)} 个, P2: {len(p2_points)} 个")
            
            # 去重
            all_p0_points = list(dict.fromkeys(all_p0_points))
            all_p1_points = list(dict.fromkeys(all_p1_points))
            all_p2_points = list(dict.fromkeys(all_p2_points))
            
            print(f"\n  📊 汇总结果:")
            print(f"    P0 测试点: {len(all_p0_points)} 个")
            print(f"    P1 测试点: {len(all_p1_points)} 个")
            print(f"    P2 测试点: {len(all_p2_points)} 个")
            
            # 合并为一个汇总测试点
            test_points = f"## P0\n" + "\n".join(all_p0_points)
            if all_p1_points:
                test_points += f"\n\n## P1\n" + "\n".join(all_p1_points)
            if all_p2_points:
                test_points += f"\n\n## P2\n" + "\n".join(all_p2_points)
            
            p0_points = all_p0_points
            p1_points = all_p1_points
        else:
            print(f"  需求在正常范围内，直接生成测试点...")
            test_points = self.generate_test_points(requirement, module_name, feature_name)
            p0_points = self._extract_p0_points(test_points)
            p1_points = self._extract_p1_points(test_points)
            p2_points = self._extract_p2_points(test_points)
            
            print(f"  P0: {len(p0_points)} 个, P1: {len(p1_points)} 个, P2: {len(p2_points)} 个")
        
        # 分批生成代码
        all_test_code = []
        
        # 分批生成 P0 代码
        if p0_points:
            print(f"\n🔧 分批生成 P0 测试代码 (每批 {batch_size} 个)...")
            batches = list(self._chunk_list(p0_points, batch_size))
            # 使用并行生成
            batch_codes = self.generate_batches_parallel(batches, module_name, feature_name, max_workers=3)
            for i, code in enumerate(batch_codes, 1):
                all_test_code.append(f"# ========== P0 批次 {i} ==========\n{code}")

        # 分批生成 P1 代码
        if p1_points:
            print(f"\n🔧 分批生成 P1 测试代码 (每批 {batch_size} 个)...")
            batches = list(self._chunk_list(p1_points, batch_size))
            for i, batch in enumerate(batches, 1):
                print(f"  批次 {i}/{len(batches)}: 生成 {len(batch)} 个测试点...")
                code = self.generate_batch_code(batch, module_name, feature_name)
                all_test_code.append(f"# ========== P1 批次 {i} ==========\n{code}")
        
        # 分批生成 P2 代码（可选，P2 可以少一些）
        if p2_points and len(p2_points) <= 50:
            print(f"\n🔧 生成 P2 测试代码...")
            code = self.generate_batch_code(p2_points[:10], module_name, feature_name)
            all_test_code.append(f"# ========== P2 ==========\n{code}")
        elif p2_points:
            print(f"\n⚠️ P2 测试点较多 ({len(p2_points)} 个)，已跳过，可按需单独生成")
        
        # 合并所有代码
        combined_code = "\n\n".join(all_test_code)
        
        print(f"\n✅ 完成！共生成 {len(all_test_code)} 批代码")
        
        return {
            "test_points": test_points,
            "test_data": "参数化数据已嵌入代码中",
            "test_code": combined_code
        }

    def generate_batches_parallel(self, point_batches: List[List[str]], module_name: str, feature_name: str, max_workers: int = 3):
        """并行生成多批测试代码"""
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        results = {}
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {}
            for i, batch in enumerate(point_batches):
                future = executor.submit(self.generate_batch_code, batch, module_name, feature_name)
                futures[future] = i
            
            for future in as_completed(futures):
                i = futures[future]
                results[i] = future.result()
                print(f"  批次 {i+1}/{len(point_batches)} 完成")
        
        return [results[i] for i in sorted(results.keys())]
    
    def save_to_file(self, result: Dict[str, Any], output_dir: str = "test/ai/generated"):
        """保存生成的结果到文件"""
        project_name = self.config.get("project_name", self.project).replace(" ", "_")
        project_dir = os.path.join(output_dir, project_name)
        os.makedirs(project_dir, exist_ok=True)
        
        with open(f"{project_dir}/test_points.md", "w", encoding="utf-8") as f:
            f.write(result["test_points"])
        
        with open(f"{project_dir}/generated_test.py", "w", encoding="utf-8") as f:
            f.write(result["test_code"])
        
        print(f"📁 文件已保存到 {project_dir}/")
    
    def run_and_save(self, requirement: str, module_name: str, feature_name: str, use_batch: bool = True):
        """运行生成并保存结果"""
        if use_batch:
            result = self.generate_in_batches(requirement, module_name, feature_name)
        else:
            result = self.generate_complete_test_case(requirement, module_name, feature_name)
        
        self.save_to_file(result)
        return result


def get_generator(project: str = "juice"):
    """获取项目对应的生成器"""
    return AITestGenerator(project=project)


# ==================== 命令行使用示例 ====================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI 测试用例生成器")
    parser.add_argument("-r", "--requirement", required=True, help="需求描述或文件路径")
    parser.add_argument("-m", "--module", required=True, help="模块名称")
    parser.add_argument("-f", "--feature", required=True, help="功能名称")
    parser.add_argument("-p", "--path", default=None, help="页面路径")
    parser.add_argument("--project", default="juice", help="项目名称")
    parser.add_argument("--batch", action="store_true", help="使用分批生成模式（推荐）")
    parser.add_argument("--batch-size", type=int, default=5, help="每批生成的测试点数量")
    
    args = parser.parse_args()
    
    # 读取文件内容（如果是文件路径）
    requirement = args.requirement
    if os.path.isfile(requirement):
        with open(requirement, 'r', encoding='utf-8') as f:
            requirement = f.read()
        print(f"📖 已读取需求文件: {args.requirement} ({len(requirement)} 字符)")
    
    generator = AITestGenerator(project=args.project)
    
    if args.batch:
        result = generator.generate_in_batches(
            requirement, args.module, args.feature, args.batch_size
        )
    else:
        result = generator.generate_complete_test_case(
            requirement, args.module, args.feature, args.path
        )
    
    generator.save_to_file(result)
    
    print("\n" + "=" * 60)
    print("📋 测试点预览")
    print("=" * 60)
    preview = result["test_points"][:800]
    print(preview + ("..." if len(result["test_points"]) > 800 else ""))