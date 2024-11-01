# src/tools/claude_api.py
from typing import Dict, Any
import os
import anthropic

class ClaudeAPI:
    """Anthropic's Claude API implementation"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        
    def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze text using Claude"""
        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": text}]
            )
            return {
                "status": "success",
                "analysis": response.content
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }