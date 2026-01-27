"""
Datasets Extractor - Extract dataset information from papers
"""
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from .llm_client import get_llm_client
from parsers.pdf_parser import ParsedPaper


@dataclass
class Dataset:
    """Represents a dataset"""
    name: str
    description: str
    size: str
    splits: str
    url: str
    evidence_location: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class DatasetsExtractor:
    """Extract dataset information from research papers"""
    
    SYSTEM_PROMPT = """You are an expert at extracting dataset information from research papers.
Extract all datasets accurately. Always output valid JSON only."""
    
    USER_PROMPT_TEMPLATE = """Extract all datasets used in this paper.

For each dataset, provide:
1. Name
2. Description
3. Size (number of examples, if mentioned)
4. Splits (train/val/test split info)
5. URL (if mentioned)
6. Location

Return in JSON format:
{{
  "datasets": [
    {{
      "name": "string",
      "description": "string",
      "size": "string",
      "splits": "string",
      "url": "string",
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
    
    def extract(self, paper: ParsedPaper) -> List[Dataset]:
        """Extract datasets from a parsed paper"""
        prompt = self.USER_PROMPT_TEMPLATE.format(
            title=paper.title,
            content=paper.full_text[:25000]
        )
        
        print(f"📊 Extracting datasets from: {paper.title[:60]}...")
        response = self.llm.complete_json(prompt, self.SYSTEM_PROMPT)
        
        datasets = []
        if isinstance(response, dict):
            items = response.get("datasets", [])
        elif isinstance(response, list):
            items = response
        else:
            return []
        
        for item in items:
            try:
                dataset = Dataset(
                    name=item.get("name", "Unknown"),
                    description=item.get("description", ""),
                    size=item.get("size", ""),
                    splits=item.get("splits", ""),
                    url=item.get("url", ""),
                    evidence_location=item.get("evidence_location", "")
                )
                datasets.append(dataset)
            except Exception as e:
                print(f"⚠️  Failed to parse dataset: {e}")
                continue
        
        print(f"✅ Found {len(datasets)} datasets")
        return datasets


