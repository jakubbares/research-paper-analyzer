"""
Related Work Extractor - Extract related work citations from papers
"""
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from .llm_client import get_llm_client
from parsers.pdf_parser import ParsedPaper


@dataclass
class RelatedWork:
    """Represents a related work citation"""
    paper_name: str
    authors: str
    year: str
    contribution: str
    comparison: str
    evidence_location: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class RelatedWorkExtractor:
    """Extract related work from research papers"""
    
    SYSTEM_PROMPT = """You are an expert at extracting related work from research papers.
Extract key related papers accurately. Always output valid JSON only."""
    
    USER_PROMPT_TEMPLATE = """Extract key related work from this paper's related work section.

For each cited paper, provide:
1. Paper name/title
2. Authors (if mentioned)
3. Year
4. Main contribution
5. How it compares to this paper
6. Location

Return in JSON format:
{{
  "related_work": [
    {{
      "paper_name": "string",
      "authors": "string",
      "year": "string",
      "contribution": "string",
      "comparison": "string",
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
    
    def extract(self, paper: ParsedPaper) -> List[RelatedWork]:
        """Extract related work from a parsed paper"""
        prompt = self.USER_PROMPT_TEMPLATE.format(
            title=paper.title,
            content=paper.full_text[:25000]
        )
        
        print(f"📚 Extracting related work from: {paper.title[:60]}...")
        response = self.llm.complete_json(prompt, self.SYSTEM_PROMPT)
        
        related_works = []
        if isinstance(response, dict):
            items = response.get("related_work", [])
        elif isinstance(response, list):
            items = response
        else:
            return []
        
        for item in items:
            try:
                work = RelatedWork(
                    paper_name=item.get("paper_name", "Unknown"),
                    authors=item.get("authors", ""),
                    year=item.get("year", ""),
                    contribution=item.get("contribution", ""),
                    comparison=item.get("comparison", ""),
                    evidence_location=item.get("evidence_location", "")
                )
                related_works.append(work)
            except Exception as e:
                print(f"⚠️  Failed to parse related work: {e}")
                continue
        
        print(f"✅ Found {len(related_works)} related works")
        return related_works

