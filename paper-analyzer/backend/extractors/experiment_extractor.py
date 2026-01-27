"""
Experiment Extractor - Extract experimental details from papers
"""
from typing import List, Dict, Any
from dataclasses import dataclass, field, asdict
from .llm_client import BedrockLLMClient, get_llm_client
from parsers.pdf_parser import ParsedPaper


@dataclass
class Experiment:
    """Represents an experiment from a paper"""
    experiment_id: str
    name: str
    description: str
    task: str
    datasets: List[Dict[str, Any]] = field(default_factory=list)
    baselines: List[Dict[str, Any]] = field(default_factory=list)
    proposed_methods: List[Dict[str, Any]] = field(default_factory=list)
    evaluation_metrics: List[Dict[str, Any]] = field(default_factory=list)
    results: List[Dict[str, Any]] = field(default_factory=list)
    hyperparameters: Dict[str, Any] = field(default_factory=dict)
    evidence_location: str = ""
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ExperimentExtractor:
    """Extract experimental details from research papers"""
    
    SYSTEM_PROMPT = """You are an expert machine learning researcher analyzing experimental details in academic papers.
Extract ALL experimental information accurately. Always output valid JSON only."""
    
    USER_PROMPT_TEMPLATE = """Extract all experiments from this paper with comprehensive details for replication.

For each experiment, provide:
1. Experiment name and description
2. Task being evaluated
3. Datasets used (with train/val/test splits if mentioned)
4. Baseline methods compared against
5. Proposed method variants
6. Evaluation metrics
7. Complete results
8. Hyperparameters (if mentioned)
9. Evidence location (table/figure/section)

Return in JSON format following this structure:
{{
  "experiments": [
    {{
      "experiment_id": "exp_1",
      "name": "string",
      "description": "string",
      "task": "string",
      "datasets": [
        {{
          "name": "string",
          "splits": {{"train": "string", "val": "string", "test": "string"}},
          "preprocessing": "string"
        }}
      ],
      "baselines": [
        {{
          "name": "string",
          "type": "string",
          "description": "string"
        }}
      ],
      "proposed_methods": [
        {{
          "name": "string",
          "variant": "string",
          "description": "string"
        }}
      ],
      "evaluation_metrics": [
        {{
          "name": "string",
          "full_name": "string",
          "primary": true
        }}
      ],
      "results": [
        {{
          "method": "string",
          "metrics": {{}},
          "notes": "string"
        }}
      ],
      "hyperparameters": {{}},
      "evidence_location": "string",
      "notes": "string"
    }}
  ]
}}

Output ONLY the JSON. No explanations.

Paper Title: {title}

Paper Content:
{content}
"""
    
    def __init__(self, llm_client: BedrockLLMClient = None):
        self.llm = llm_client or get_llm_client()
    
    def extract(self, paper: ParsedPaper) -> List[Experiment]:
        """
        Extract experiments from a parsed paper
        
        Args:
            paper: ParsedPaper object
            
        Returns:
            List of Experiment objects
        """
        # Format prompt
        prompt = self.USER_PROMPT_TEMPLATE.format(
            title=paper.title,
            content=paper.full_text[:20000]  # More content for experiments
        )
        
        # Get LLM response
        print(f"🔬 Extracting experiments from: {paper.title[:60]}...")
        response = self.llm.complete_json(prompt, self.SYSTEM_PROMPT)
        
        # Parse response
        experiments = []
        
        if isinstance(response, dict):
            items = response.get("experiments", [])
        elif isinstance(response, list):
            items = response
        else:
            print(f"⚠️  Unexpected response type: {type(response)}")
            return []
        
        # Convert to Experiment objects
        for item in items:
            try:
                experiment = Experiment(
                    experiment_id=item.get("experiment_id", "exp_unknown"),
                    name=item.get("name", "Unknown Experiment"),
                    description=item.get("description", ""),
                    task=item.get("task", ""),
                    datasets=item.get("datasets", []),
                    baselines=item.get("baselines", []),
                    proposed_methods=item.get("proposed_methods", []),
                    evaluation_metrics=item.get("evaluation_metrics", []),
                    results=item.get("results", []),
                    hyperparameters=item.get("hyperparameters", {}),
                    evidence_location=item.get("evidence_location", ""),
                    notes=item.get("notes", "")
                )
                experiments.append(experiment)
            except Exception as e:
                print(f"⚠️  Failed to parse experiment: {e}")
                continue
        
        print(f"✅ Found {len(experiments)} experiments")
        return experiments


