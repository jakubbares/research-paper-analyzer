"""
Equations Extractor - Extract mathematical equations from papers
"""
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from .llm_client import get_llm_client
from parsers.pdf_parser import ParsedPaper


@dataclass
class Equation:
    """Represents an equation"""
    equation_id: str
    latex: str
    description: str
    context: str
    evidence_location: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class EquationsExtractor:
    """Extract equations from research papers"""
    
    SYSTEM_PROMPT = """You are an expert at extracting mathematical equations from papers.
Extract all significant equations. Always output valid JSON only."""
    
    USER_PROMPT_TEMPLATE = """Extract all significant equations from this paper.

For each equation, provide:
1. Unique ID (eq_1, eq_2, etc.)
2. LaTeX representation (if possible, otherwise description)
3. Description of what it represents
4. Context/purpose
5. Location (section/equation number)

Return in JSON format:
{{
  "equations": [
    {{
      "equation_id": "string",
      "latex": "string",
      "description": "string",
      "context": "string",
      "evidence_location": "string"
    }}
  ]
}}

Output ONLY the JSON. No explanations.

Paper Title: {title}

Paper Content:
{content}
"""
    
    def __init__(self):
        """Initialize with LLM client"""
        self.llm = get_llm_client()
    
    def extract(self, paper: ParsedPaper) -> List[Equation]:
        """Extract equations from a parsed paper"""
        prompt = self.USER_PROMPT_TEMPLATE.format(
            title=paper.title,
            content=paper.full_text[:25000]
        )
        
        print(f"🔢 Extracting equations from: {paper.title[:60]}...")
        response = self.llm.complete_json(prompt, self.SYSTEM_PROMPT)
        
        equations = []
        if isinstance(response, dict):
            items = response.get("equations", [])
        elif isinstance(response, list):
            items = response
        else:
            return []
        
        for item in items:
            try:
                equation = Equation(
                    equation_id=item.get("equation_id", "eq_unknown"),
                    latex=item.get("latex", ""),
                    description=item.get("description", ""),
                    context=item.get("context", ""),
                    evidence_location=item.get("evidence_location", "")
                )
                equations.append(equation)
            except Exception as e:
                print(f"⚠️  Failed to parse equation: {e}")
                continue
        
        print(f"✅ Found {len(equations)} equations")
        return equations


