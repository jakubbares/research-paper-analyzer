"""
Limitations Extractor - Extract limitations from papers
"""
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from .llm_client import get_llm_client
from parsers.pdf_parser import ParsedPaper


@dataclass
class Limitation:
    """Represents a limitation"""
    limitation_type: str
    description: str
    severity: str
    proposed_solution: str
    evidence_location: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class LimitationsExtractor:
    """Extract limitations from research papers"""
    
    SYSTEM_PROMPT = """You are an expert at analyzing limitations in research papers.
Extract all limitations accurately. Always output valid JSON only."""
    
    USER_PROMPT_TEMPLATE = """Extract all limitations mentioned in this paper.

For each limitation, provide:
1. Type (e.g., "Computational", "Data", "Theoretical", "Methodological")
2. Description
3. Severity (High/Medium/Low if inferable, otherwise "Unknown")
4. Proposed solution (if mentioned)
5. Location

Return in JSON format:
{{
  "limitations": [
    {{
      "limitation_type": "string",
      "description": "string",
      "severity": "string",
      "proposed_solution": "string",
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
    
    def extract(self, paper: ParsedPaper) -> List[Limitation]:
        """Extract limitations from a parsed paper"""
        prompt = self.USER_PROMPT_TEMPLATE.format(
            title=paper.title,
            content=paper.full_text[:25000]
        )
        
        print(f"⚠️  Extracting limitations from: {paper.title[:60]}...")
        response = self.llm.complete_json(prompt, self.SYSTEM_PROMPT)
        
        limitations = []
        if isinstance(response, dict):
            items = response.get("limitations", [])
        elif isinstance(response, list):
            items = response
        else:
            return []
        
        for item in items:
            try:
                limitation = Limitation(
                    limitation_type=item.get("limitation_type", "Unknown"),
                    description=item.get("description", ""),
                    severity=item.get("severity", "Unknown"),
                    proposed_solution=item.get("proposed_solution", ""),
                    evidence_location=item.get("evidence_location", "")
                )
                limitations.append(limitation)
            except Exception as e:
                print(f"⚠️  Failed to parse limitation: {e}")
                continue
        
        print(f"✅ Found {len(limitations)} limitations")
        return limitations


