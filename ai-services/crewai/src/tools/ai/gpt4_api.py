# src/tools/gpt4_api.py
from typing import Dict, Any
import os
import openai

class GPT4API:
    """OpenAI's GPT-4 API implementation"""
    
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
    def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze text using GPT-4"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": text}]
            )
            return {
                "status": "success",
                "analysis": response.choices[0].message.content
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }