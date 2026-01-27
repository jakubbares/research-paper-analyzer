"""
Hyperparameter Extractor - Extract training hyperparameters
"""
from typing import Dict, Any
from dataclasses import dataclass, asdict
from .llm_client import BedrockLLMClient, get_llm_client
from parsers import ParsedPaper


@dataclass
class HyperparameterSet:
    """Represents a set of hyperparameters"""
    experiment_name: str
    optimizer: str
    learning_rate: str
    batch_size: str
    num_epochs: str
    weight_decay: str = ""
    dropout: str = ""
    warmup_steps: str = ""
    lr_schedule: str = ""
    gradient_clipping: str = ""
    other_params: Dict[str, str] = None
    evidence_location: str = ""
    
    def __post_init__(self):
        if self.other_params is None:
            self.other_params = {}
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class HyperparameterExtractor:
    """Extract training hyperparameters from research papers"""
    
    PROMPT_TEMPLATE = """Extract all training hyperparameters from this paper.

Include:
- Optimizer (type and parameters: learning rate, momentum, betas, epsilon)
- Learning rate schedule (constant, decay, cosine, etc.)
- Batch size (per GPU and effective/global if mentioned)
- Number of epochs/steps
- Warmup strategy
- Weight decay
- Gradient clipping
- Dropout rates
- Regularization techniques
- Any other hyperparameters mentioned

Organize by experiment if different experiments use different settings.

If a hyperparameter is not specified, use "not specified".

Return in JSON format:
{{
  "hyperparameter_sets": [
    {{
      "experiment_name": "string",
      "optimizer": "string",
      "learning_rate": "string",
      "batch_size": "string",
      "num_epochs": "string",
      "weight_decay": "string",
      "dropout": "string",
      "warmup_steps": "string",
      "lr_schedule": "string",
      "gradient_clipping": "string",
      "other_params": {{}},
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
    
    def extract(self, paper: ParsedPaper) -> list[HyperparameterSet]:
        """
        Extract hyperparameters from a parsed paper
        
        Args:
            paper: ParsedPaper object
            
        Returns:
            List of HyperparameterSet objects
        """
        # Format prompt
        prompt = self.PROMPT_TEMPLATE.format(
            title=paper.title,
            content=paper.full_text[:15000]
        )
        
        # Get LLM response
        print("Extracting hyperparameters...")
        response = self.llm.complete_json(prompt)
        
        # Parse response
        hyperparameters = []
        items = response.get("hyperparameter_sets", [])
        
        for item in items:
            hyperparameters.append(HyperparameterSet(**item))
        
        return hyperparameters


