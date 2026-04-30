# test/rules/spec_parser.py
"""规范解析器 - 从 ui-testing-patterns.md 读取规范"""

import re
from pathlib import Path


class SpecParser:
    """解析 ui-testing-patterns.md 规范文件"""
    
    def __init__(self, spec_path: str = "test/cases/ui-testing-patterns.md"):
        self.spec_path = Path(spec_path)
        self.content = self.spec_path.read_text(encoding="utf-8") if self.spec_path.exists() else ""
    
    def get_form_test_points(self) -> list:
        """从规范中提取表单页测试点"""
        # 解析规范中的测试点定义
        pattern = r"### \d+\.\d+ (.*?)\n```python\n(.*?)```"
        matches = re.findall(pattern, self.content, re.DOTALL)
        return [{"name": m[0], "code": m[1]} for m in matches]
    
    def get_required_test_points(self, page_type: str) -> list:
        """获取指定页面类型必须包含的测试点"""
        # 根据规范内容返回必测点列表
        required = {
            "form": ["页面加载", "有效提交", "无效提交", "必填验证", "边界值", "重复提交", "重置功能", "安全测试"],
            "detail": ["字段显示", "空字段处理", "返回按钮", "状态显示", "数据一致性", "编辑按钮", "页面加载"],
            "list": ["页面加载", "字段验证", "导航访问", "空列表", "搜索", "排序", "分页", "CRUD刷新"],
        }
        return required.get(page_type, [])
    
    def get_last_updated(self) -> str:
        """获取规范最后更新时间"""
        match = re.search(r'last_updated: (.+?)\n', self.content)
        return match.group(1) if match else "unknown"


class SpecDrivenGenerator:
    """规范驱动的测试生成器"""
    
    def __init__(self):
        self.spec = SpecParser()
        self.last_spec_update = self.spec.get_last_updated()
    
    def check_sync_status(self, target_file: Path) -> dict:
        """检查目标文件是否与规范同步"""
        if not target_file.exists():
            return {"synced": False, "reason": "文件不存在"}
        
        content = target_file.read_text(encoding="utf-8")
        
        # 检查文件中记录的规范版本
        match = re.search(r'spec_version: (.+?)\n', content)
        file_version = match.group(1) if match else None
        
        return {
            "synced": file_version == self.last_spec_update,
            "file_version": file_version,
            "spec_version": self.last_spec_update
        }
    
    def generate_test_file(self, page_type: str, module_name: str) -> str:
        """根据规范生成测试文件"""
        required_points = self.spec.get_required_test_points(page_type)
        
        # 生成文件头
        header = f'''
"""
{module_name} - {page_type} 页面自动化测试

规范文件: test/cases/ui-testing-patterns.md
spec_version: {self.last_spec_update}
生成时间: auto-generated

根据规范自动生成的测试点:
{chr(10).join(f'- {p}' for p in required_points)}
"""
'''
        return header