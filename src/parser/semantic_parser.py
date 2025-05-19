from bs4 import BeautifulSoup
from typing import Dict, Any

class SemanticParser:
    def __init__(self):
        pass
        
    def parse_tags(self, tagged_text: str) -> Dict[str, str]:
        """从带标签的文本中提取字段和值"""
        soup = BeautifulSoup(tagged_text, "html.parser")
        fields = {tag.name: tag.text for tag in soup.find_all()}
        return fields
    
    def extract_fields(self, tagged_text: str) -> Dict[str, Any]:
        """提取所有字段信息，包括属性"""
        soup = BeautifulSoup(tagged_text, "html.parser")
        result = {}
        
        for tag in soup.find_all():
            # 获取标签名和文本内容
            prompt_key = tag.name
            prompt_value = tag.text
            
            # 获取属性
            attributes = dict(tag.attrs)
            
            result[prompt_key] = {
                'value': prompt_value,
                'attributes': attributes
            }
            
        return result 