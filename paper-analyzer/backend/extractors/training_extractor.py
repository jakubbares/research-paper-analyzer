"""
Training Procedures Extractor - Extract training procedures from papers
"""
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from .llm_client import get_llm_client
from parsers.pdf_parser import ParsedPaper


@dataclass
class TrainingProcedure:
    """Represents a training procedure"""
    phase: str
    description: str
    hyperparameters: str
    duration: str
    evidence_location: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TrainingExtractor:
    """Extract training procedures from research papers"""
    
    SYSTEM_PROMPT = """You are an expert at extracting training procedures from research papers.
Extract all training details accurately. Always output valid JSON only."""
    
    USER_PROMPT_TEMPLATE = """Extract training procedures from this paper.

For each training phase/procedure, provide:
1. Phase (e.g., "Pretraining", "Fine-tuning", "Main Training")
2. Description
3. Key hyperparameters
4. Duration (epochs/steps/time if mentioned)
5. Location

Return in JSON format:
{{
  "training_procedures": [
    {{
      "phase": "string",
      "description": "string",
      "hyperparameters": "string",
      "duration": "string",
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
    
    def extract(self, paper: ParsedPaper) -> List[TrainingProcedure]:
        """Extract training procedures from a parsed paper"""
        prompt = self.USER_PROMPT_TEMPLATE.format(
            title=paper.title,
            content=paper.full_text[:25000]
        )
        
        print(f"🏋️  Extracting training procedures from: {paper.title[:60]}...")
        response = self.llm.complete_json(prompt, self.SYSTEM_PROMPT)
        
        procedures = []
        if isinstance(response, dict):
            items = response.get("training_procedures", [])
        elif isinstance(response, list):
            items = response
        else:
            return []
        
        for item in items:
            try:
                procedure = TrainingProcedure(
                    phase=item.get("phase", "Unknown"),
                    description=item.get("description", ""),
                    hyperparameters=item.get("hyperparameters", ""),
                    duration=item.get("duration", ""),
                    evidence_location=item.get("evidence_location", "")
                )
                procedures.append(procedure)
            except Exception as e:
                print(f"⚠️  Failed to parse training procedure: {e}")
                continue
        
        print(f"✅ Found {len(procedures)} training procedures")
        return procedures

