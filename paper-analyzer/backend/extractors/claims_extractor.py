"""
Key Claims Extractor - Extract key claims from papers
"""
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from .llm_client import get_llm_client
from parsers.pdf_parser import ParsedPaper


@dataclass
class KeyClaim:
    """Represents a key claim"""
    claim: str
    evidence: str
    confidence: str
    evidence_location: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ClaimsExtractor:
    """Extract key claims from research papers"""
    
    SYSTEM_PROMPT = """You are an expert at extracting key claims from research papers.
Extract all major claims accurately. Always output valid JSON only."""
    
    USER_PROMPT_TEMPLATE = """Extract key claims made in this paper.

For each claim, provide:
1. The claim statement
2. Evidence provided (experimental results, theory, etc.)
3. Confidence level (Strong/Moderate/Weak if inferable)
4. Location

Return in JSON format:
{{
  "claims": [
    {{
      "claim": "string",
      "evidence": "string",
      "confidence": "string",
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
    
    def extract(self, paper: ParsedPaper) -> List[KeyClaim]:
        """Extract claims from a parsed paper"""
        prompt = self.USER_PROMPT_TEMPLATE.format(
            title=paper.title,
            content=paper.full_text[:25000]
        )
        
        print(f"💡 Extracting key claims from: {paper.title[:60]}...")
        response = self.llm.complete_json(prompt, self.SYSTEM_PROMPT)
        
        claims = []
        if isinstance(response, dict):
            items = response.get("claims", [])
        elif isinstance(response, list):
            items = response
        else:
            return []
        
        for item in items:
            try:
                claim = KeyClaim(
                    claim=item.get("claim", ""),
                    evidence=item.get("evidence", ""),
                    confidence=item.get("confidence", "Unknown"),
                    evidence_location=item.get("evidence_location", "")
                )
                claims.append(claim)
            except Exception as e:
                print(f"⚠️  Failed to parse claim: {e}")
                continue
        
        print(f"✅ Found {len(claims)} key claims")
        return claims


