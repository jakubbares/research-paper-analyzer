"""
Algorithms Extractor - Extract algorithms from papers
"""
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from .llm_client import get_llm_client
from parsers.pdf_parser import ParsedPaper


@dataclass
class Algorithm:
    """Represents an algorithm"""
    algorithm_id: str
    name: str
    description: str
    pseudocode: str
    complexity: str
    evidence_location: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AlgorithmsExtractor:
    """Extract algorithms from research papers"""
    
    SYSTEM_PROMPT = """You are an expert at extracting algorithms from papers.
Extract all algorithms with their details. Always output valid JSON only."""
    
    USER_PROMPT_TEMPLATE = """Extract all algorithms from this paper.

For each algorithm, provide:
1. Algorithm ID and name
2. Description  
3. Pseudocode (if available)
4. Time/space complexity (if mentioned)
5. Location

Return in JSON format:
{{
  "algorithms": [
    {{
      "algorithm_id": "string",
      "name": "string",
      "description": "string",
      "pseudocode": "string",
      "complexity": "string",
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
    
    def extract(self, paper: ParsedPaper) -> List[Algorithm]:
        """Extract algorithms from a parsed paper"""
        prompt = self.USER_PROMPT_TEMPLATE.format(
            title=paper.title,
            content=paper.full_text[:25000]
        )
        
        print(f"⚙️  Extracting algorithms from: {paper.title[:60]}...")
        response = self.llm.complete_json(prompt, self.SYSTEM_PROMPT)
        
        algorithms = []
        if isinstance(response, dict):
            items = response.get("algorithms", [])
        elif isinstance(response, list):
            items = response
        else:
            return []
        
        for item in items:
            try:
                algorithm = Algorithm(
                    algorithm_id=item.get("algorithm_id", "alg_unknown"),
                    name=item.get("name", "Unknown Algorithm"),
                    description=item.get("description", ""),
                    pseudocode=item.get("pseudocode", ""),
                    complexity=item.get("complexity", ""),
                    evidence_location=item.get("evidence_location", "")
                )
                algorithms.append(algorithm)
            except Exception as e:
                print(f"⚠️  Failed to parse algorithm: {e}")
                continue
        
        print(f"✅ Found {len(algorithms)} algorithms")
        return algorithms


