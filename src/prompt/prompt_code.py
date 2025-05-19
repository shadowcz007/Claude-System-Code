import requests
import yaml
import os
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import os

# 加载.env文件
load_dotenv()

class PromptEngine:

    def __init__(self, config_path: str = "config/config.yaml"):
        self.config = self._load_config(config_path)
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
            
    def _load_config(self, config_path: str) -> dict:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _call_openai_api(self, messages: list, **kwargs) -> Dict[str, Any]:
        """直接调用OpenAI API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.config['llm']['model'],
            "messages": messages,
            "temperature": kwargs.get('temperature', self.config['llm']['temperature']),
            "max_tokens": kwargs.get('max_tokens', self.config['llm']['max_tokens'])
        }
        
        response = requests.post(
            self.config['llm']['api_url'],
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            raise Exception(f"API调用失败: {response.text}")
            
        return response.json()
    
    def semantic_tagging(self, text: str) -> str:
        """将输入文本转换为语义标签结构"""
        template = self.config['prompt_templates']['semantic_tagging']
        prompt = template.format(text=text)
        
        messages = [{"role": "user", "content": prompt}]
        response = self._call_openai_api(messages)
        
        return response['choices'][0]['message']['content'] 