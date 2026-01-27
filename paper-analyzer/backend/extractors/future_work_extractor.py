"""
Future Work Extractor - Extract future work directions from papers
"""
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from .llm_client import get_llm_client
from parsers.pdf_parser import ParsedPaper


@dataclass
class FutureWorkItem:
    """Represents a future work item"""
    category: str
    description: str
    priority: str
    evidence_location: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class FutureWorkExtractor:
    """Extract future work directions from research papers"""
    
    SYSTEM_PROMPT = """You are an expert at extracting future work from research papers.
Extract all future directions accurately. Always output valid JSON only."""
    
    USER_PROMPT_TEMPLATE = """Extract future work directions from this paper.

For each item, provide:
1. Category (e.g., "Extension", "New Application", "Improvement")
2. Description
3. Priority (High/Medium/Low if inferable, otherwise "Unknown")
4. Location

Return in JSON format:
{{
  "future_work": [
    {{
      "category": "string",
      "description": "string",
      "priority": "string",
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
    
    def extract(self, paper: ParsedPaper) -> List[FutureWorkItem]:
        """Extract future work from a parsed paper"""
        prompt = self.USER_PROMPT_TEMPLATE.format(
            title=paper.title,
            content=paper.full_text[:25000]
        )
        
        print(f"🔮 Extracting future work from: {paper.title[:60]}...")
        response = self.llm.complete_json(prompt, self.SYSTEM_PROMPT)
        
        items_list = []
        if isinstance(response, dict):
            items = response.get("future_work", [])
        elif isinstance(response, list):
            items = response
        else:
            return []
        
        for item in items:
            try:
                future_item = FutureWorkItem(
                    category=item.get("category", "Unknown"),
                    description=item.get("description", ""),
                    priority=item.get("priority", "Unknown"),
                    evidence_location=item.get("evidence_location", "")
                )
                items_list.append(future_item)
            except Exception as e:
                print(f"⚠️  Failed to parse future work item: {e}")
                continue
        
        print(f"✅ Found {len(items_list)} future work items")
        return items_list


