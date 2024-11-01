# src/tools/gemini_api.py
from typing import Dict, Any
import os
import google.generativeai as genai

class GeminiAPI:
    """Google's Gemini API implementation"""
    
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-pro')
        
    def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze text using Gemini"""
        try:
            response = self.model.generate_content(text)
            return {
                "status": "success",
                "analysis": response.text
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }