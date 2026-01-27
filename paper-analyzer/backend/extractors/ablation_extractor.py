"""
Ablation Extractor - Extract ablation studies
"""
from typing import List, Dict, Any
from dataclasses import dataclass, field, asdict
from .llm_client import BedrockLLMClient, get_llm_client
from parsers import ParsedPaper


@dataclass
class AblationStudy:
    """Represents an ablation study"""
    name: str
    description: str
    base_configuration: str
    variations: List[Dict[str, Any]] = field(default_factory=list)
    key_findings: str = ""
    evidence_location: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AblationExtractor:
    """Extract ablation studies from research papers"""
    
    PROMPT_TEMPLATE = """Extract all ablation studies from this paper.

An ablation study tests the importance of specific components by removing or modifying them.

For each ablation study, provide:
- Name/description of what's being ablated
- Base configuration (full model with all components)
- Variations tested (what was removed/changed and the results)
- Key findings/insights (what the ablation revealed)
- Evidence location (table/figure number, section name)

Return in JSON format:
{{
  "ablation_studies": [
    {{
      "name": "string",
      "description": "string",
      "base_configuration": "string",
      "variations": [
        {{
          "variant_name": "string",
          "what_changed": "string",
          "results": "string or dict"
        }}
      ],
      "key_findings": "string",
      "evidence_location": "string"
    }}
  ]
}}

Output only the JSON.

Paper Title: {title}

Paper Content (first 15000 chars):
{content}
"""
    
    def __init__(self, llm_client: BedrockLLMClient = None):
        self.llm = llm_client or get_llm_client()
    
    def extract(self, paper: ParsedPaper) -> List[AblationStudy]:
        """
        Extract ablation studies from a parsed paper
        
        Args:
            paper: ParsedPaper object
            
        Returns:
            List of AblationStudy objects
        """
        # Format prompt
        prompt = self.PROMPT_TEMPLATE.format(
            title=paper.title,
            content=paper.full_text[:15000]
        )
        
        # Get LLM response
        print("Extracting ablation studies...")
        response = self.llm.complete_json(prompt)
        
        # Parse response
        ablations = []
        items = response.get("ablation_studies", [])
        
        for item in items:
            ablations.append(AblationStudy(**item))
        
        return ablations


