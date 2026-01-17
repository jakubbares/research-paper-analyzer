"""
DeepSeek LLM Client - Works with payment issues!
"""
import json
import requests
from typing import Dict, Any, Optional


class DeepSeekClient:
    """LLM client using DeepSeek API"""
    
    def __init__(self, api_key: str):
        """Initialize DeepSeek client"""
        self.api_key = api_key
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.model = "deepseek-chat"
        self.mock_mode = False
        
        print(f"✅ DeepSeek client initialized!")
    
    def complete(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Get text completion from DeepSeek
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            
        Returns:
            LLM response as string
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = requests.post(
                self.api_url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": 4096,
                    "temperature": 0.1
                },
                timeout=60
            )
            
            response.raise_for_status()
            data = response.json()
            
            return data['choices'][0]['message']['content']
            
        except Exception as e:
            print(f"❌ DeepSeek API Error: {e}")
            raise
    
    def complete_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Get JSON completion from DeepSeek
        
        Args:
            prompt: User prompt (should instruct to output JSON)
            system_prompt: Optional system prompt
            
        Returns:
            Parsed JSON as dictionary
        """
        # Add JSON instruction
        json_instruction = """You MUST output ONLY valid JSON. 
No explanations, no markdown, no code blocks, just pure JSON.
Start directly with { or [ and end with } or ]."""
        
        if system_prompt:
            system_prompt = f"{system_prompt}\n\n{json_instruction}"
        else:
            system_prompt = json_instruction
        
        # Add JSON reminder to prompt
        if "output only" not in prompt.lower():
            prompt = f"{prompt}\n\nIMPORTANT: Output ONLY valid JSON. No markdown, no explanations."
        
        response_text = self.complete(prompt, system_prompt)
        
        # Clean response
        response_text = self._clean_json_response(response_text)
        
        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
            print(f"Response was: {response_text[:500]}")
            return self._extract_json(response_text)
    
    def _clean_json_response(self, text: str) -> str:
        """Remove markdown code blocks if present"""
        text = text.strip()
        
        # Remove markdown code blocks
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        
        if text.endswith("```"):
            text = text[:-3]
        
        return text.strip()
    
    def _extract_json(self, text: str) -> Dict[str, Any]:
        """Try to extract JSON from text that might contain other content"""
        import re
        
        # Try to find JSON object or array
        json_pattern = r'(\{(?:[^{}]|(?:\{[^{}]*\}))*\}|\[(?:[^\[\]]|(?:\[[^\[\]]*\]))*\])'
        matches = re.findall(json_pattern, text, re.DOTALL)
        
        if matches:
            for match in matches:
                try:
                    return json.loads(match)
                except:
                    continue
        
        # If still failed, return error
        return {
            "error": "Failed to parse JSON from LLM response",
            "raw_response": text[:500],
            "suggestion": "The model might not be outputting valid JSON. Check model configuration."
        }


# Global DeepSeek client instance
_deepseek_client = None


def get_deepseek_client(api_key: str) -> DeepSeekClient:
    """Get or create global DeepSeek client instance"""
    global _deepseek_client
    if _deepseek_client is None:
        _deepseek_client = DeepSeekClient(api_key)
    return _deepseek_client

