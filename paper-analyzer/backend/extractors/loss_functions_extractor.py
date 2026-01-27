"""
Loss Functions Extractor - Extract loss functions from papers
"""
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from .llm_client import get_llm_client
from parsers.pdf_parser import ParsedPaper


@dataclass
class LossFunction:
    """Represents a loss function"""
    name: str
    formula: str
    purpose: str
    hyperparameters: str
    evidence_location: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class LossFunctionsExtractor:
    """Extract loss functions from research papers"""
    
    SYSTEM_PROMPT = """You are an expert at extracting loss functions from research papers.
Extract all loss functions accurately. Always output valid JSON only."""
    
    USER_PROMPT_TEMPLATE = """Extract all loss functions used in this paper.

For each loss function, provide:
1. Name (e.g., "Cross Entropy", "MSE", "Custom Loss")
2. Formula (LaTeX or description)
3. Purpose (what it optimizes for)
4. Hyperparameters (weights, coefficients)
5. Location

Return in JSON format:
{{
  "loss_functions": [
    {{
      "name": "string",
      "formula": "string",
      "purpose": "string",
      "hyperparameters": "string",
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
    
    def extract(self, paper: ParsedPaper) -> List[LossFunction]:
        """Extract loss functions from a parsed paper"""
        prompt = self.USER_PROMPT_TEMPLATE.format(
            title=paper.title,
            content=paper.full_text[:25000]
        )
        
        print(f"📉 Extracting loss functions from: {paper.title[:60]}...")
        response = self.llm.complete_json(prompt, self.SYSTEM_PROMPT)
        
        loss_functions = []
        if isinstance(response, dict):
            items = response.get("loss_functions", [])
        elif isinstance(response, list):
            items = response
        else:
            return []
        
        for item in items:
            try:
                loss = LossFunction(
                    name=item.get("name", "Unknown"),
                    formula=item.get("formula", ""),
                    purpose=item.get("purpose", ""),
                    hyperparameters=item.get("hyperparameters", ""),
                    evidence_location=item.get("evidence_location", "")
                )
                loss_functions.append(loss)
            except Exception as e:
                print(f"⚠️  Failed to parse loss function: {e}")
                continue
        
        print(f"✅ Found {len(loss_functions)} loss functions")
        return loss_functions


