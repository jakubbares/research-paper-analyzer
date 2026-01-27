"""
Baselines Extractor - Extract baseline methods from papers
"""
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from .llm_client import get_llm_client
from parsers.pdf_parser import ParsedPaper


@dataclass
class Baseline:
    """Represents a baseline method"""
    name: str
    description: str
    paper_reference: str
    year: str
    category: str
    evidence_location: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class BaselinesExtractor:
    """Extract baseline comparison methods from research papers"""
    
    SYSTEM_PROMPT = """You are an expert machine learning researcher analyzing baseline methods in academic papers.
Extract ALL baseline methods accurately. Always output valid JSON only."""
    
    USER_PROMPT_TEMPLATE = """Extract all baseline methods that this paper compares against.

For each baseline, provide:
1. Name of the method
2. Brief description
3. Paper reference (if mentioned)
4. Year (if mentioned)
5. Category (e.g., "Transformer", "CNN", "Prior SOTA", "Human baseline")
6. Where it's mentioned (section/table/figure)

Return in JSON format:
{{
  "baselines": [
    {{
      "name": "string",
      "description": "string",
      "paper_reference": "string",
      "year": "string",
      "category": "string",
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
    
    def extract(self, paper: ParsedPaper) -> List[Baseline]:
        """Extract baselines from a parsed paper"""
        prompt = self.USER_PROMPT_TEMPLATE.format(
            title=paper.title,
            content=paper.full_text[:25000]
        )
        
        print(f"📊 Extracting baselines from: {paper.title[:60]}...")
        response = self.llm.complete_json(prompt, self.SYSTEM_PROMPT)
        
        baselines = []
        if isinstance(response, dict):
            items = response.get("baselines", [])
        elif isinstance(response, list):
            items = response
        else:
            print(f"⚠️  Unexpected response type: {type(response)}")
            return []
        
        for item in items:
            try:
                baseline = Baseline(
                    name=item.get("name", "Unknown"),
                    description=item.get("description", ""),
                    paper_reference=item.get("paper_reference", ""),
                    year=item.get("year", ""),
                    category=item.get("category", ""),
                    evidence_location=item.get("evidence_location", "")
                )
                baselines.append(baseline)
            except Exception as e:
                print(f"⚠️  Failed to parse baseline: {e}")
                continue
        
        print(f"✅ Found {len(baselines)} baselines")
        return baselines


