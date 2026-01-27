"""
Evaluation Metrics Extractor - Extract evaluation metrics from papers
"""
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from .llm_client import get_llm_client
from parsers.pdf_parser import ParsedPaper


@dataclass
class EvaluationMetric:
    """Represents an evaluation metric"""
    name: str
    full_name: str
    description: str
    formula: str
    higher_better: str
    evidence_location: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class MetricsExtractor:
    """Extract evaluation metrics from research papers"""
    
    SYSTEM_PROMPT = """You are an expert at extracting evaluation metrics from research papers.
Extract all metrics accurately. Always output valid JSON only."""
    
    USER_PROMPT_TEMPLATE = """Extract all evaluation metrics used in this paper.

For each metric, provide:
1. Name (abbreviation, e.g., "BLEU", "F1", "Accuracy")
2. Full name (e.g., "Bilingual Evaluation Understudy")
3. Description
4. Formula (if mentioned)
5. Higher is better (Yes/No/Unknown)
6. Location

Return in JSON format:
{{
  "metrics": [
    {{
      "name": "string",
      "full_name": "string",
      "description": "string",
      "formula": "string",
      "higher_better": "string",
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
    
    def extract(self, paper: ParsedPaper) -> List[EvaluationMetric]:
        """Extract metrics from a parsed paper"""
        prompt = self.USER_PROMPT_TEMPLATE.format(
            title=paper.title,
            content=paper.full_text[:25000]
        )
        
        print(f"📈 Extracting evaluation metrics from: {paper.title[:60]}...")
        response = self.llm.complete_json(prompt, self.SYSTEM_PROMPT)
        
        metrics = []
        if isinstance(response, dict):
            items = response.get("metrics", [])
        elif isinstance(response, list):
            items = response
        else:
            return []
        
        for item in items:
            try:
                metric = EvaluationMetric(
                    name=item.get("name", "Unknown"),
                    full_name=item.get("full_name", ""),
                    description=item.get("description", ""),
                    formula=item.get("formula", ""),
                    higher_better=item.get("higher_better", "Unknown"),
                    evidence_location=item.get("evidence_location", "")
                )
                metrics.append(metric)
            except Exception as e:
                print(f"⚠️  Failed to parse metric: {e}")
                continue
        
        print(f"✅ Found {len(metrics)} evaluation metrics")
        return metrics


