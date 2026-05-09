"""从 HTML 文件中提取所有 id 和 class，供 AI 参考"""

from bs4 import BeautifulSoup
import re

def extract_selectors(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    selectors = {
        'ids': [],
        'classes': [],
        'buttons': []
    }
    
    # 提取所有 id
    for tag in soup.find_all(id=True):
        selectors['ids'].append(tag['id'])
    
    # 提取所有 class
    for tag in soup.find_all(class_=True):
        for cls in tag['class']:
            if cls not in selectors['classes']:
                selectors['classes'].append(cls)
    
    # 提取按钮文本
    for btn in soup.find_all(['button', 'input']):
        if btn.get('type') in ['submit', 'button'] or btn.name == 'button':
            text = btn.get_text().strip() or btn.get('value', '')
            if text:
                selectors['buttons'].append(text)
    
    return selectors

# 使用
selectors = extract_selectors('activity_management.html')
print(f"页面中的 ID: {selectors['ids'][:20]}")
print(f"按钮文本: {selectors['buttons']}")