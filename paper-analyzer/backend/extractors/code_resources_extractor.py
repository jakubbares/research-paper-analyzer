"""
Code and Resources Extractor - Extract URLs and resources from papers
"""
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from .llm_client import get_llm_client
from parsers.pdf_parser import ParsedPaper


@dataclass
class CodeResource:
    """Represents a code or data resource"""
    resource_type: str
    name: str
    url: str
    description: str
    license: str
    evidence_location: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CodeResourcesExtractor:
    """Extract code, datasets, and resource URLs from research papers"""
    
    SYSTEM_PROMPT = """You are an expert at extracting code and data resources from research papers.
Extract all URLs and resources accurately. Always output valid JSON only."""
    
    USER_PROMPT_TEMPLATE = """Extract code, datasets, and resource URLs from this paper.

For each resource, provide:
1. Type (Code/Dataset/Model/Benchmark/Other)
2. Name
3. URL (if mentioned)
4. Description
5. License (if mentioned)
6. Location

Return in JSON format:
{{
  "resources": [
    {{
      "resource_type": "string",
      "name": "string",
      "url": "string",
      "description": "string",
      "license": "string",
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
    
    def extract(self, paper: ParsedPaper) -> List[CodeResource]:
        """Extract code resources from a parsed paper"""
        prompt = self.USER_PROMPT_TEMPLATE.format(
            title=paper.title,
            content=paper.full_text[:25000]
        )
        
        print(f"💾 Extracting code/resources from: {paper.title[:60]}...")
        response = self.llm.complete_json(prompt, self.SYSTEM_PROMPT)
        
        resources = []
        if isinstance(response, dict):
            items = response.get("resources", [])
        elif isinstance(response, list):
            items = response
        else:
            return []
        
        for item in items:
            try:
                resource = CodeResource(
                    resource_type=item.get("resource_type", "Unknown"),
                    name=item.get("name", ""),
                    url=item.get("url", ""),
                    description=item.get("description", ""),
                    license=item.get("license", ""),
                    evidence_location=item.get("evidence_location", "")
                )
                resources.append(resource)
            except Exception as e:
                print(f"⚠️  Failed to parse resource: {e}")
                continue
        
        print(f"✅ Found {len(resources)} code/resources")
        return resources

