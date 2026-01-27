"""
FastAPI Application - Main API Server
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import shutil
import uuid
from pathlib import Path
import json
from datetime import datetime

from config import settings
from parsers import PaperParser, ParsedPaper
from extractors import (
    get_llm_client,
    ContributionExtractor,
    ExperimentExtractor,
    ArchitectureExtractor,
    HyperparameterExtractor,
    AblationExtractor,
    BaselinesExtractor,
    EquationsExtractor,
    AlgorithmsExtractor,
    LimitationsExtractor,
    FutureWorkExtractor,
    CodeResourcesExtractor,
    DatasetsExtractor,
    LossFunctionsExtractor,
    MetricsExtractor,
    TrainingExtractor,
    RelatedWorkExtractor,
    ClaimsExtractor,
    Contribution,
    Experiment,
    Architecture,
    HyperparameterSet,
    AblationStudy,
    Baseline,
    Equation,
    Algorithm,
    Limitation,
    FutureWorkItem,
    CodeResource,
    Dataset,
    LossFunction,
    EvaluationMetric,
    TrainingProcedure,
    RelatedWork,
    KeyClaim
)
from aggregation import AggregationEngine

# Initialize FastAPI app
app = FastAPI(
    title="Research Paper Analyzer API",
    description="AI-powered paper analysis using AWS Bedrock + LangChain",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create data directories
UPLOAD_DIR = Path(settings.upload_dir)
EXTRACTED_DIR = Path(settings.extracted_dir)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)

# Initialize components (lazy loading)
_paper_parser = None
_contribution_extractor = None
_experiment_extractor = None
_architecture_extractor = None
_hyperparameter_extractor = None
_ablation_extractor = None
_baselines_extractor = None
_equations_extractor = None
_algorithms_extractor = None
_limitations_extractor = None
_future_work_extractor = None
_code_resources_extractor = None
_datasets_extractor = None
_loss_functions_extractor = None
_metrics_extractor = None
_training_extractor = None
_related_work_extractor = None
_claims_extractor = None


def get_paper_parser() -> PaperParser:
    """Get or create paper parser"""
    global _paper_parser
    if _paper_parser is None:
        _paper_parser = PaperParser()
    return _paper_parser


def get_contribution_extractor() -> ContributionExtractor:
    """Get or create contribution extractor"""
    global _contribution_extractor
    if _contribution_extractor is None:
        _contribution_extractor = ContributionExtractor()
    return _contribution_extractor


def get_experiment_extractor() -> ExperimentExtractor:
    """Get or create experiment extractor"""
    global _experiment_extractor
    if _experiment_extractor is None:
        _experiment_extractor = ExperimentExtractor()
    return _experiment_extractor


def get_architecture_extractor() -> ArchitectureExtractor:
    """Get or create architecture extractor"""
    global _architecture_extractor
    if _architecture_extractor is None:
        _architecture_extractor = ArchitectureExtractor()
    return _architecture_extractor


def get_hyperparameter_extractor() -> HyperparameterExtractor:
    """Get or create hyperparameter extractor"""
    global _hyperparameter_extractor
    if _hyperparameter_extractor is None:
        _hyperparameter_extractor = HyperparameterExtractor()
    return _hyperparameter_extractor


def get_ablation_extractor() -> AblationExtractor:
    """Get or create ablation extractor"""
    global _ablation_extractor
    if _ablation_extractor is None:
        _ablation_extractor = AblationExtractor()
    return _ablation_extractor


def get_baselines_extractor() -> BaselinesExtractor:
    """Get or create baselines extractor"""
    global _baselines_extractor
    if _baselines_extractor is None:
        _baselines_extractor = BaselinesExtractor()
    return _baselines_extractor


def get_equations_extractor() -> EquationsExtractor:
    """Get or create equations extractor"""
    global _equations_extractor
    if _equations_extractor is None:
        _equations_extractor = EquationsExtractor()
    return _equations_extractor


def get_algorithms_extractor() -> AlgorithmsExtractor:
    """Get or create algorithms extractor"""
    global _algorithms_extractor
    if _algorithms_extractor is None:
        _algorithms_extractor = AlgorithmsExtractor()
    return _algorithms_extractor


def get_limitations_extractor() -> LimitationsExtractor:
    """Get or create limitations extractor"""
    global _limitations_extractor
    if _limitations_extractor is None:
        _limitations_extractor = LimitationsExtractor()
    return _limitations_extractor


def get_future_work_extractor() -> FutureWorkExtractor:
    """Get or create future work extractor"""
    global _future_work_extractor
    if _future_work_extractor is None:
        _future_work_extractor = FutureWorkExtractor()
    return _future_work_extractor


def get_code_resources_extractor() -> CodeResourcesExtractor:
    """Get or create code resources extractor"""
    global _code_resources_extractor
    if _code_resources_extractor is None:
        _code_resources_extractor = CodeResourcesExtractor()
    return _code_resources_extractor


def get_datasets_extractor() -> DatasetsExtractor:
    """Get or create datasets extractor"""
    global _datasets_extractor
    if _datasets_extractor is None:
        _datasets_extractor = DatasetsExtractor()
    return _datasets_extractor


def get_loss_functions_extractor() -> LossFunctionsExtractor:
    """Get or create loss functions extractor"""
    global _loss_functions_extractor
    if _loss_functions_extractor is None:
        _loss_functions_extractor = LossFunctionsExtractor()
    return _loss_functions_extractor


def get_metrics_extractor() -> MetricsExtractor:
    """Get or create metrics extractor"""
    global _metrics_extractor
    if _metrics_extractor is None:
        _metrics_extractor = MetricsExtractor()
    return _metrics_extractor


def get_training_extractor() -> TrainingExtractor:
    """Get or create training extractor"""
    global _training_extractor
    if _training_extractor is None:
        _training_extractor = TrainingExtractor()
    return _training_extractor


def get_related_work_extractor() -> RelatedWorkExtractor:
    """Get or create related work extractor"""
    global _related_work_extractor
    if _related_work_extractor is None:
        _related_work_extractor = RelatedWorkExtractor()
    return _related_work_extractor


def get_claims_extractor() -> ClaimsExtractor:
    """Get or create claims extractor"""
    global _claims_extractor
    if _claims_extractor is None:
        _claims_extractor = ClaimsExtractor()
    return _claims_extractor


# ============================================================================
# Pydantic Models
# ============================================================================

class PaperResponse(BaseModel):
    """Response model for paper upload/retrieval"""
    paper_id: str
    title: str
    abstract: str
    authors: List[str]
    num_pages: int
    status: str = "processed"


class ContributionResponse(BaseModel):
    """Response model for contribution"""
    contribution_type: str
    specific_innovation: str
    problem_addressed: str
    evidence_location: str
    comment: str


class ExperimentResponse(BaseModel):
    """Response model for experiment"""
    experiment_id: str
    name: str
    description: str
    task: str
    datasets: List[Dict[str, Any]]
    baselines: List[Dict[str, Any]]
    proposed_methods: List[Dict[str, Any]]
    evaluation_metrics: List[Dict[str, Any]]
    results: List[Dict[str, Any]]
    hyperparameters: Dict[str, Any]
    evidence_location: str
    notes: str


class QueryRequest(BaseModel):
    """Request model for custom query"""
    query: str


class QueryResponse(BaseModel):
    """Response model for custom query"""
    paper_id: str
    query: str
    result: str


class VisualizeRequest(BaseModel):
    """Request model for dynamic visualization generation"""
    paper_ids: List[str]
    query: str
    extractors: Optional[List[str]] = None  # Auto-detect if not provided


# ============================================================================
# Helper Functions
# ============================================================================

def save_parsed_paper(paper: ParsedPaper) -> None:
    """Save parsed paper metadata to JSON"""
    paper_file = EXTRACTED_DIR / f"{paper.paper_id}_paper.json"
    with open(paper_file, 'w', encoding='utf-8') as f:
        json.dump({
            "paper_id": paper.paper_id,
            "title": paper.title,
            "authors": paper.authors,
            "abstract": paper.abstract,
            "num_pages": paper.num_pages,
            "metadata": paper.metadata
        }, f, indent=2, ensure_ascii=False)


def load_parsed_paper(paper_id: str) -> Optional[Dict]:
    """Load parsed paper metadata from JSON"""
    paper_file = EXTRACTED_DIR / f"{paper_id}_paper.json"
    if not paper_file.exists():
        return None
    with open(paper_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_contributions(paper_id: str, contributions: List[Contribution]) -> None:
    """Save contributions to JSON"""
    contrib_file = EXTRACTED_DIR / f"{paper_id}_contributions.json"
    with open(contrib_file, 'w', encoding='utf-8') as f:
        json.dump([c.to_dict() for c in contributions], f, indent=2, ensure_ascii=False)


def load_contributions(paper_id: str) -> Optional[List[Dict]]:
    """Load contributions from JSON"""
    contrib_file = EXTRACTED_DIR / f"{paper_id}_contributions.json"
    if not contrib_file.exists():
        return None
    with open(contrib_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_experiments(paper_id: str, experiments: List[Experiment]) -> None:
    """Save experiments to JSON"""
    exp_file = EXTRACTED_DIR / f"{paper_id}_experiments.json"
    with open(exp_file, 'w', encoding='utf-8') as f:
        json.dump([e.to_dict() for e in experiments], f, indent=2, ensure_ascii=False)


def load_experiments(paper_id: str) -> Optional[List[Dict]]:
    """Load experiments from JSON"""
    exp_file = EXTRACTED_DIR / f"{paper_id}_experiments.json"
    if not exp_file.exists():
        return None
    with open(exp_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_architectures(paper_id: str, architectures: List[Architecture]) -> None:
    """Save architectures to JSON"""
    arch_file = EXTRACTED_DIR / f"{paper_id}_architectures.json"
    with open(arch_file, 'w', encoding='utf-8') as f:
        json.dump([a.to_dict() for a in architectures], f, indent=2, ensure_ascii=False)


def load_architectures(paper_id: str) -> Optional[List[Architecture]]:
    """Load architectures from JSON"""
    arch_file = EXTRACTED_DIR / f"{paper_id}_architectures.json"
    if not arch_file.exists():
        return None
    with open(arch_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [Architecture(**item) for item in data]


def save_hyperparameters(paper_id: str, hyperparams: List[HyperparameterSet]) -> None:
    """Save hyperparameters to JSON"""
    hyper_file = EXTRACTED_DIR / f"{paper_id}_hyperparameters.json"
    with open(hyper_file, 'w', encoding='utf-8') as f:
        json.dump([h.to_dict() for h in hyperparams], f, indent=2, ensure_ascii=False)


def load_hyperparameters(paper_id: str) -> Optional[List[HyperparameterSet]]:
    """Load hyperparameters from JSON"""
    hyper_file = EXTRACTED_DIR / f"{paper_id}_hyperparameters.json"
    if not hyper_file.exists():
        return None
    with open(hyper_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [HyperparameterSet(**item) for item in data]


def save_ablations(paper_id: str, ablations: List[AblationStudy]) -> None:
    """Save ablation studies to JSON"""
    abl_file = EXTRACTED_DIR / f"{paper_id}_ablations.json"
    with open(abl_file, 'w', encoding='utf-8') as f:
        json.dump([a.to_dict() for a in ablations], f, indent=2, ensure_ascii=False)


def load_ablations(paper_id: str) -> Optional[List[AblationStudy]]:
    """Load ablation studies from JSON"""
    abl_file = EXTRACTED_DIR / f"{paper_id}_ablations.json"
    if not abl_file.exists():
        return None
    with open(abl_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [AblationStudy(**item) for item in data]


def save_baselines(paper_id: str, baselines: List[Baseline]) -> None:
    """Save baselines to JSON"""
    file_path = EXTRACTED_DIR / f"{paper_id}_baselines.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump([b.to_dict() for b in baselines], f, indent=2, ensure_ascii=False)


def load_baselines(paper_id: str) -> Optional[List[Baseline]]:
    """Load baselines from JSON"""
    file_path = EXTRACTED_DIR / f"{paper_id}_baselines.json"
    if not file_path.exists():
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [Baseline(**item) for item in data]


def save_equations(paper_id: str, equations: List[Equation]) -> None:
    """Save equations to JSON"""
    file_path = EXTRACTED_DIR / f"{paper_id}_equations.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump([e.to_dict() for e in equations], f, indent=2, ensure_ascii=False)


def load_equations(paper_id: str) -> Optional[List[Equation]]:
    """Load equations from JSON"""
    file_path = EXTRACTED_DIR / f"{paper_id}_equations.json"
    if not file_path.exists():
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [Equation(**item) for item in data]


def save_algorithms(paper_id: str, algorithms: List[Algorithm]) -> None:
    """Save algorithms to JSON"""
    file_path = EXTRACTED_DIR / f"{paper_id}_algorithms.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump([a.to_dict() for a in algorithms], f, indent=2, ensure_ascii=False)


def load_algorithms(paper_id: str) -> Optional[List[Algorithm]]:
    """Load algorithms from JSON"""
    file_path = EXTRACTED_DIR / f"{paper_id}_algorithms.json"
    if not file_path.exists():
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [Algorithm(**item) for item in data]


def save_limitations(paper_id: str, limitations: List[Limitation]) -> None:
    """Save limitations to JSON"""
    file_path = EXTRACTED_DIR / f"{paper_id}_limitations.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump([l.to_dict() for l in limitations], f, indent=2, ensure_ascii=False)


def load_limitations(paper_id: str) -> Optional[List[Limitation]]:
    """Load limitations from JSON"""
    file_path = EXTRACTED_DIR / f"{paper_id}_limitations.json"
    if not file_path.exists():
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [Limitation(**item) for item in data]


def save_future_work(paper_id: str, items: List[FutureWorkItem]) -> None:
    """Save future work to JSON"""
    file_path = EXTRACTED_DIR / f"{paper_id}_future_work.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump([i.to_dict() for i in items], f, indent=2, ensure_ascii=False)


def load_future_work(paper_id: str) -> Optional[List[FutureWorkItem]]:
    """Load future work from JSON"""
    file_path = EXTRACTED_DIR / f"{paper_id}_future_work.json"
    if not file_path.exists():
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [FutureWorkItem(**item) for item in data]


def save_code_resources(paper_id: str, resources: List[CodeResource]) -> None:
    """Save code resources to JSON"""
    file_path = EXTRACTED_DIR / f"{paper_id}_code_resources.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump([r.to_dict() for r in resources], f, indent=2, ensure_ascii=False)


def load_code_resources(paper_id: str) -> Optional[List[CodeResource]]:
    """Load code resources from JSON"""
    file_path = EXTRACTED_DIR / f"{paper_id}_code_resources.json"
    if not file_path.exists():
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [CodeResource(**item) for item in data]


def save_datasets(paper_id: str, datasets: List[Dataset]) -> None:
    """Save datasets to JSON"""
    file_path = EXTRACTED_DIR / f"{paper_id}_datasets.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump([d.to_dict() for d in datasets], f, indent=2, ensure_ascii=False)


def load_datasets(paper_id: str) -> Optional[List[Dataset]]:
    """Load datasets from JSON"""
    file_path = EXTRACTED_DIR / f"{paper_id}_datasets.json"
    if not file_path.exists():
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [Dataset(**item) for item in data]


def save_loss_functions(paper_id: str, losses: List[LossFunction]) -> None:
    """Save loss functions to JSON"""
    file_path = EXTRACTED_DIR / f"{paper_id}_loss_functions.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump([l.to_dict() for l in losses], f, indent=2, ensure_ascii=False)


def load_loss_functions(paper_id: str) -> Optional[List[LossFunction]]:
    """Load loss functions from JSON"""
    file_path = EXTRACTED_DIR / f"{paper_id}_loss_functions.json"
    if not file_path.exists():
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [LossFunction(**item) for item in data]


def save_metrics(paper_id: str, metrics: List[EvaluationMetric]) -> None:
    """Save evaluation metrics to JSON"""
    file_path = EXTRACTED_DIR / f"{paper_id}_metrics.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump([m.to_dict() for m in metrics], f, indent=2, ensure_ascii=False)


def load_metrics(paper_id: str) -> Optional[List[EvaluationMetric]]:
    """Load evaluation metrics from JSON"""
    file_path = EXTRACTED_DIR / f"{paper_id}_metrics.json"
    if not file_path.exists():
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [EvaluationMetric(**item) for item in data]


def save_training(paper_id: str, procedures: List[TrainingProcedure]) -> None:
    """Save training procedures to JSON"""
    file_path = EXTRACTED_DIR / f"{paper_id}_training.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump([p.to_dict() for p in procedures], f, indent=2, ensure_ascii=False)


def load_training(paper_id: str) -> Optional[List[TrainingProcedure]]:
    """Load training procedures from JSON"""
    file_path = EXTRACTED_DIR / f"{paper_id}_training.json"
    if not file_path.exists():
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [TrainingProcedure(**item) for item in data]


def save_related_work(paper_id: str, works: List[RelatedWork]) -> None:
    """Save related work to JSON"""
    file_path = EXTRACTED_DIR / f"{paper_id}_related_work.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump([w.to_dict() for w in works], f, indent=2, ensure_ascii=False)


def load_related_work(paper_id: str) -> Optional[List[RelatedWork]]:
    """Load related work from JSON"""
    file_path = EXTRACTED_DIR / f"{paper_id}_related_work.json"
    if not file_path.exists():
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [RelatedWork(**item) for item in data]


def save_claims(paper_id: str, claims: List[KeyClaim]) -> None:
    """Save key claims to JSON"""
    file_path = EXTRACTED_DIR / f"{paper_id}_claims.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump([c.to_dict() for c in claims], f, indent=2, ensure_ascii=False)


def load_claims(paper_id: str) -> Optional[List[KeyClaim]]:
    """Load key claims from JSON"""
    file_path = EXTRACTED_DIR / f"{paper_id}_claims.json"
    if not file_path.exists():
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [KeyClaim(**item) for item in data]


# ============================================================================
# API Routes
# ============================================================================

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Research Paper Analyzer API",
        "version": "1.0.0",
        "backend": "FastAPI + LangChain + AWS Bedrock (DeepSeek)",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    if settings.llm_provider.lower() == "deepseek":
        llm_info = f"DeepSeek - {settings.deepseek_model}"
    else:
        llm_info = f"AWS Bedrock - {settings.bedrock_model_id}"
    
    return {
        "status": "healthy",
        "llm": llm_info,
        "provider": settings.llm_provider
    }


@app.post("/api/papers", response_model=PaperResponse)
async def upload_paper(file: UploadFile = File(...)):
    """
    Upload a paper PDF and parse it
    
    Returns paper metadata
    """
    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported")
    
    # Generate paper ID
    paper_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{paper_id}.pdf"
    
    # Save uploaded file
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(500, f"Failed to save file: {str(e)}")
    
    # Parse PDF
    try:
        parser = get_paper_parser()
        paper = parser.parse_pdf(str(file_path), paper_id)
        save_parsed_paper(paper)
    except Exception as e:
        file_path.unlink()  # Clean up file
        raise HTTPException(500, f"Failed to parse PDF: {str(e)}")
    
    return PaperResponse(
        paper_id=paper.paper_id,
        title=paper.title,
        abstract=paper.abstract,
        authors=paper.authors,
        num_pages=paper.num_pages,
        status="processed"
    )


@app.get("/api/papers/{paper_id}", response_model=PaperResponse)
def get_paper(paper_id: str):
    """Get paper metadata"""
    paper_data = load_parsed_paper(paper_id)
    if not paper_data:
        raise HTTPException(404, "Paper not found")
    
    return PaperResponse(**paper_data, status="processed")


@app.post("/api/papers/{paper_id}/extract/contributions")
async def extract_contributions(paper_id: str) -> Dict[str, Any]:
    """Extract contributions from a paper"""
    # Check if already extracted
    cached = load_contributions(paper_id)
    if cached:
        return {
            "paper_id": paper_id,
            "contributions": cached,
            "cached": True
        }
    
    # Load paper
    paper_data = load_parsed_paper(paper_id)
    if not paper_data:
        raise HTTPException(404, "Paper not found")
    
    # Get PDF path
    pdf_path = UPLOAD_DIR / f"{paper_id}.pdf"
    if not pdf_path.exists():
        raise HTTPException(404, "Paper PDF not found")
    
    try:
        # Parse paper (to get full content)
        parser = get_paper_parser()
        paper = parser.parse_pdf(str(pdf_path), paper_id)
        
        # Extract contributions
        extractor = get_contribution_extractor()
        contributions = extractor.extract(paper)
        
        # Save results
        save_contributions(paper_id, contributions)
        
        return {
            "paper_id": paper_id,
            "contributions": [c.to_dict() for c in contributions],
            "cached": False
        }
    except Exception as e:
        raise HTTPException(500, f"Extraction failed: {str(e)}")


@app.post("/api/papers/{paper_id}/extract/experiments")
async def extract_experiments(paper_id: str) -> Dict[str, Any]:
    """Extract experiments from a paper"""
    # Check if already extracted
    cached = load_experiments(paper_id)
    if cached:
        return {
            "paper_id": paper_id,
            "experiments": cached,
            "cached": True
        }
    
    # Load paper
    paper_data = load_parsed_paper(paper_id)
    if not paper_data:
        raise HTTPException(404, "Paper not found")
    
    # Get PDF path
    pdf_path = UPLOAD_DIR / f"{paper_id}.pdf"
    if not pdf_path.exists():
        raise HTTPException(404, "Paper PDF not found")
    
    try:
        # Parse paper
        parser = get_paper_parser()
        paper = parser.parse_pdf(str(pdf_path), paper_id)
        
        # Extract experiments
        extractor = get_experiment_extractor()
        experiments = extractor.extract(paper)
        
        # Save results
        save_experiments(paper_id, experiments)
        
        return {
            "paper_id": paper_id,
            "experiments": [e.to_dict() for e in experiments],
            "cached": False
        }
    except Exception as e:
        raise HTTPException(500, f"Extraction failed: {str(e)}")


@app.post("/api/papers/{paper_id}/query")
async def query_paper(paper_id: str, request: QueryRequest) -> QueryResponse:
    """Ask a custom question about a paper"""
    # Get PDF path
    pdf_path = UPLOAD_DIR / f"{paper_id}.pdf"
    if not pdf_path.exists():
        raise HTTPException(404, "Paper not found")
    
    try:
        # Parse paper
        parser = get_paper_parser()
        paper = parser.parse_pdf(str(pdf_path), paper_id)
        
        # Query LLM
        llm = get_llm_client()
        prompt = f"""Answer the following question about this research paper.

Paper Title: {paper.title}
Paper Abstract: {paper.abstract}

Paper Content (first 15000 chars):
{paper.full_text[:15000]}

Question: {request.query}

Provide a clear, concise answer based on the paper content."""
        
        response = llm.complete(prompt)
        
        return QueryResponse(
            paper_id=paper_id,
            query=request.query,
            result=response
        )
    except Exception as e:
        raise HTTPException(500, f"Query failed: {str(e)}")


@app.post("/api/papers/{paper_id}/extract/architecture")
async def extract_architecture(paper_id: str) -> Dict[str, Any]:
    """Extract architecture details from a paper"""
    cached = load_architectures(paper_id)
    if cached:
        return {
            "paper_id": paper_id,
            "architectures": [a.to_dict() for a in cached],
            "cached": True
        }
    
    pdf_path = UPLOAD_DIR / f"{paper_id}.pdf"
    if not pdf_path.exists():
        raise HTTPException(404, "Paper PDF not found")
    
    try:
        parser = get_paper_parser()
        paper = parser.parse_pdf(str(pdf_path), paper_id)
        extractor = get_architecture_extractor()
        architectures = extractor.extract(paper)
        save_architectures(paper_id, architectures)
        
        return {
            "paper_id": paper_id,
            "architectures": [a.to_dict() for a in architectures],
            "cached": False
        }
    except Exception as e:
        raise HTTPException(500, f"Extraction failed: {str(e)}")


@app.post("/api/papers/{paper_id}/extract/hyperparameters")
async def extract_hyperparameters(paper_id: str) -> Dict[str, Any]:
    """Extract training hyperparameters from a paper"""
    cached = load_hyperparameters(paper_id)
    if cached:
        return {
            "paper_id": paper_id,
            "hyperparameters": [h.to_dict() for h in cached],
            "cached": True
        }
    
    pdf_path = UPLOAD_DIR / f"{paper_id}.pdf"
    if not pdf_path.exists():
        raise HTTPException(404, "Paper PDF not found")
    
    try:
        parser = get_paper_parser()
        paper = parser.parse_pdf(str(pdf_path), paper_id)
        extractor = get_hyperparameter_extractor()
        hyperparams = extractor.extract(paper)
        save_hyperparameters(paper_id, hyperparams)
        
        return {
            "paper_id": paper_id,
            "hyperparameters": [h.to_dict() for h in hyperparams],
            "cached": False
        }
    except Exception as e:
        raise HTTPException(500, f"Extraction failed: {str(e)}")


@app.post("/api/papers/{paper_id}/extract/ablations")
async def extract_ablations(paper_id: str) -> Dict[str, Any]:
    """Extract ablation studies from a paper"""
    cached = load_ablations(paper_id)
    if cached:
        return {
            "paper_id": paper_id,
            "ablations": [a.to_dict() for a in cached],
            "cached": True
        }
    
    pdf_path = UPLOAD_DIR / f"{paper_id}.pdf"
    if not pdf_path.exists():
        raise HTTPException(404, "Paper PDF not found")
    
    try:
        parser = get_paper_parser()
        paper = parser.parse_pdf(str(pdf_path), paper_id)
        extractor = get_ablation_extractor()
        ablations = extractor.extract(paper)
        save_ablations(paper_id, ablations)
        
        return {
            "paper_id": paper_id,
            "ablations": [a.to_dict() for a in ablations],
            "cached": False
        }
    except Exception as e:
        raise HTTPException(500, f"Extraction failed: {str(e)}")


@app.post("/api/papers/{paper_id}/extract/baselines")
async def extract_baselines(paper_id: str) -> Dict[str, Any]:
    """Extract baseline methods from a paper"""
    cached = load_baselines(paper_id)
    if cached:
        return {"paper_id": paper_id, "baselines": [b.to_dict() for b in cached], "cached": True}
    
    pdf_path = UPLOAD_DIR / f"{paper_id}.pdf"
    if not pdf_path.exists():
        raise HTTPException(404, "Paper PDF not found")
    
    try:
        parser = get_paper_parser()
        paper = parser.parse_pdf(str(pdf_path), paper_id)
        extractor = get_baselines_extractor()
        baselines = extractor.extract(paper)
        save_baselines(paper_id, baselines)
        return {"paper_id": paper_id, "baselines": [b.to_dict() for b in baselines], "cached": False}
    except Exception as e:
        raise HTTPException(500, f"Extraction failed: {str(e)}")


@app.post("/api/papers/{paper_id}/extract/equations")
async def extract_equations(paper_id: str) -> Dict[str, Any]:
    """Extract equations from a paper"""
    cached = load_equations(paper_id)
    if cached:
        return {"paper_id": paper_id, "equations": [e.to_dict() for e in cached], "cached": True}
    
    pdf_path = UPLOAD_DIR / f"{paper_id}.pdf"
    if not pdf_path.exists():
        raise HTTPException(404, "Paper PDF not found")
    
    try:
        parser = get_paper_parser()
        paper = parser.parse_pdf(str(pdf_path), paper_id)
        extractor = get_equations_extractor()
        equations = extractor.extract(paper)
        save_equations(paper_id, equations)
        return {"paper_id": paper_id, "equations": [e.to_dict() for e in equations], "cached": False}
    except Exception as e:
        raise HTTPException(500, f"Extraction failed: {str(e)}")


@app.post("/api/papers/{paper_id}/extract/algorithms")
async def extract_algorithms(paper_id: str) -> Dict[str, Any]:
    """Extract algorithms from a paper"""
    cached = load_algorithms(paper_id)
    if cached:
        return {"paper_id": paper_id, "algorithms": [a.to_dict() for a in cached], "cached": True}
    
    pdf_path = UPLOAD_DIR / f"{paper_id}.pdf"
    if not pdf_path.exists():
        raise HTTPException(404, "Paper PDF not found")
    
    try:
        parser = get_paper_parser()
        paper = parser.parse_pdf(str(pdf_path), paper_id)
        extractor = get_algorithms_extractor()
        algorithms = extractor.extract(paper)
        save_algorithms(paper_id, algorithms)
        return {"paper_id": paper_id, "algorithms": [a.to_dict() for a in algorithms], "cached": False}
    except Exception as e:
        raise HTTPException(500, f"Extraction failed: {str(e)}")


@app.post("/api/papers/{paper_id}/extract/limitations")
async def extract_limitations(paper_id: str) -> Dict[str, Any]:
    """Extract limitations from a paper"""
    cached = load_limitations(paper_id)
    if cached:
        return {"paper_id": paper_id, "limitations": [l.to_dict() for l in cached], "cached": True}
    
    pdf_path = UPLOAD_DIR / f"{paper_id}.pdf"
    if not pdf_path.exists():
        raise HTTPException(404, "Paper PDF not found")
    
    try:
        parser = get_paper_parser()
        paper = parser.parse_pdf(str(pdf_path), paper_id)
        extractor = get_limitations_extractor()
        limitations = extractor.extract(paper)
        save_limitations(paper_id, limitations)
        return {"paper_id": paper_id, "limitations": [l.to_dict() for l in limitations], "cached": False}
    except Exception as e:
        raise HTTPException(500, f"Extraction failed: {str(e)}")


@app.post("/api/papers/{paper_id}/extract/future_work")
async def extract_future_work(paper_id: str) -> Dict[str, Any]:
    """Extract future work from a paper"""
    cached = load_future_work(paper_id)
    if cached:
        return {"paper_id": paper_id, "future_work": [f.to_dict() for f in cached], "cached": True}
    
    pdf_path = UPLOAD_DIR / f"{paper_id}.pdf"
    if not pdf_path.exists():
        raise HTTPException(404, "Paper PDF not found")
    
    try:
        parser = get_paper_parser()
        paper = parser.parse_pdf(str(pdf_path), paper_id)
        extractor = get_future_work_extractor()
        items = extractor.extract(paper)
        save_future_work(paper_id, items)
        return {"paper_id": paper_id, "future_work": [f.to_dict() for f in items], "cached": False}
    except Exception as e:
        raise HTTPException(500, f"Extraction failed: {str(e)}")


@app.post("/api/papers/{paper_id}/extract/code_resources")
async def extract_code_resources(paper_id: str) -> Dict[str, Any]:
    """Extract code and resource URLs from a paper"""
    cached = load_code_resources(paper_id)
    if cached:
        return {"paper_id": paper_id, "code_resources": [r.to_dict() for r in cached], "cached": True}
    
    pdf_path = UPLOAD_DIR / f"{paper_id}.pdf"
    if not pdf_path.exists():
        raise HTTPException(404, "Paper PDF not found")
    
    try:
        parser = get_paper_parser()
        paper = parser.parse_pdf(str(pdf_path), paper_id)
        extractor = get_code_resources_extractor()
        resources = extractor.extract(paper)
        save_code_resources(paper_id, resources)
        return {"paper_id": paper_id, "code_resources": [r.to_dict() for r in resources], "cached": False}
    except Exception as e:
        raise HTTPException(500, f"Extraction failed: {str(e)}")


@app.post("/api/papers/{paper_id}/extract/datasets")
async def extract_datasets(paper_id: str) -> Dict[str, Any]:
    """Extract datasets from a paper"""
    cached = load_datasets(paper_id)
    if cached:
        return {"paper_id": paper_id, "datasets": [d.to_dict() for d in cached], "cached": True}
    
    pdf_path = UPLOAD_DIR / f"{paper_id}.pdf"
    if not pdf_path.exists():
        raise HTTPException(404, "Paper PDF not found")
    
    try:
        parser = get_paper_parser()
        paper = parser.parse_pdf(str(pdf_path), paper_id)
        extractor = get_datasets_extractor()
        datasets = extractor.extract(paper)
        save_datasets(paper_id, datasets)
        return {"paper_id": paper_id, "datasets": [d.to_dict() for d in datasets], "cached": False}
    except Exception as e:
        raise HTTPException(500, f"Extraction failed: {str(e)}")


@app.post("/api/papers/{paper_id}/extract/loss_functions")
async def extract_loss_functions(paper_id: str) -> Dict[str, Any]:
    """Extract loss functions from a paper"""
    cached = load_loss_functions(paper_id)
    if cached:
        return {"paper_id": paper_id, "loss_functions": [l.to_dict() for l in cached], "cached": True}
    
    pdf_path = UPLOAD_DIR / f"{paper_id}.pdf"
    if not pdf_path.exists():
        raise HTTPException(404, "Paper PDF not found")
    
    try:
        parser = get_paper_parser()
        paper = parser.parse_pdf(str(pdf_path), paper_id)
        extractor = get_loss_functions_extractor()
        losses = extractor.extract(paper)
        save_loss_functions(paper_id, losses)
        return {"paper_id": paper_id, "loss_functions": [l.to_dict() for l in losses], "cached": False}
    except Exception as e:
        raise HTTPException(500, f"Extraction failed: {str(e)}")


@app.post("/api/papers/{paper_id}/extract/metrics")
async def extract_metrics(paper_id: str) -> Dict[str, Any]:
    """Extract evaluation metrics from a paper"""
    cached = load_metrics(paper_id)
    if cached:
        return {"paper_id": paper_id, "metrics": [m.to_dict() for m in cached], "cached": True}
    
    pdf_path = UPLOAD_DIR / f"{paper_id}.pdf"
    if not pdf_path.exists():
        raise HTTPException(404, "Paper PDF not found")
    
    try:
        parser = get_paper_parser()
        paper = parser.parse_pdf(str(pdf_path), paper_id)
        extractor = get_metrics_extractor()
        metrics = extractor.extract(paper)
        save_metrics(paper_id, metrics)
        return {"paper_id": paper_id, "metrics": [m.to_dict() for m in metrics], "cached": False}
    except Exception as e:
        raise HTTPException(500, f"Extraction failed: {str(e)}")


@app.post("/api/papers/{paper_id}/extract/training")
async def extract_training(paper_id: str) -> Dict[str, Any]:
    """Extract training procedures from a paper"""
    cached = load_training(paper_id)
    if cached:
        return {"paper_id": paper_id, "training": [t.to_dict() for t in cached], "cached": True}
    
    pdf_path = UPLOAD_DIR / f"{paper_id}.pdf"
    if not pdf_path.exists():
        raise HTTPException(404, "Paper PDF not found")
    
    try:
        parser = get_paper_parser()
        paper = parser.parse_pdf(str(pdf_path), paper_id)
        extractor = get_training_extractor()
        procedures = extractor.extract(paper)
        save_training(paper_id, procedures)
        return {"paper_id": paper_id, "training": [t.to_dict() for t in procedures], "cached": False}
    except Exception as e:
        raise HTTPException(500, f"Extraction failed: {str(e)}")


@app.post("/api/papers/{paper_id}/extract/related_work")
async def extract_related_work(paper_id: str) -> Dict[str, Any]:
    """Extract related work from a paper"""
    cached = load_related_work(paper_id)
    if cached:
        return {"paper_id": paper_id, "related_work": [w.to_dict() for w in cached], "cached": True}
    
    pdf_path = UPLOAD_DIR / f"{paper_id}.pdf"
    if not pdf_path.exists():
        raise HTTPException(404, "Paper PDF not found")
    
    try:
        parser = get_paper_parser()
        paper = parser.parse_pdf(str(pdf_path), paper_id)
        extractor = get_related_work_extractor()
        works = extractor.extract(paper)
        save_related_work(paper_id, works)
        return {"paper_id": paper_id, "related_work": [w.to_dict() for w in works], "cached": False}
    except Exception as e:
        raise HTTPException(500, f"Extraction failed: {str(e)}")


@app.post("/api/papers/{paper_id}/extract/claims")
async def extract_claims(paper_id: str) -> Dict[str, Any]:
    """Extract key claims from a paper"""
    cached = load_claims(paper_id)
    if cached:
        return {"paper_id": paper_id, "claims": [c.to_dict() for c in cached], "cached": True}
    
    pdf_path = UPLOAD_DIR / f"{paper_id}.pdf"
    if not pdf_path.exists():
        raise HTTPException(404, "Paper PDF not found")
    
    try:
        parser = get_paper_parser()
        paper = parser.parse_pdf(str(pdf_path), paper_id)
        extractor = get_claims_extractor()
        claims = extractor.extract(paper)
        save_claims(paper_id, claims)
        return {"paper_id": paper_id, "claims": [c.to_dict() for c in claims], "cached": False}
    except Exception as e:
        raise HTTPException(500, f"Extraction failed: {str(e)}")


# ============================================================================
# Dynamic Visualization Generation
# ============================================================================

@app.post("/api/visualize")
async def generate_visualization(request: VisualizeRequest) -> Dict[str, Any]:
    """
    Generate dynamic HTML visualization based on user query.
    
    Takes multiple paper IDs, collects their extracted data,
    and asks the LLM to generate a custom HTML visualization.
    """
    # 1. Collect extracted data from all papers
    all_data = {}
    for paper_id in request.paper_ids:
        paper_data = load_parsed_paper(paper_id)
        if not paper_data:
            continue
        
        # Load all available extractions
        contributions = load_contributions(paper_id)
        experiments = load_experiments(paper_id)
        architectures = load_architectures(paper_id)
        hyperparameters = load_hyperparameters(paper_id)
        ablations = load_ablations(paper_id)
        baselines = load_baselines(paper_id)
        datasets = load_datasets(paper_id)
        limitations = load_limitations(paper_id)
        future_work = load_future_work(paper_id)
        
        all_data[paper_id] = {
            "paper": {
                "title": paper_data.get("title", "Unknown"),
                "authors": paper_data.get("authors", []),
                "abstract": paper_data.get("abstract", "")[:500]  # Truncate for context
            },
            "contributions": [c.to_dict() if hasattr(c, 'to_dict') else c for c in (contributions or [])],
            "experiments": [e.to_dict() if hasattr(e, 'to_dict') else e for e in (experiments or [])],
            "architectures": [a.to_dict() if hasattr(a, 'to_dict') else a for a in (architectures or [])],
            "hyperparameters": [h.to_dict() if hasattr(h, 'to_dict') else h for h in (hyperparameters or [])],
            "ablations": [a.to_dict() if hasattr(a, 'to_dict') else a for a in (ablations or [])],
            "baselines": [b.to_dict() if hasattr(b, 'to_dict') else b for b in (baselines or [])],
            "datasets": [d.to_dict() if hasattr(d, 'to_dict') else d for d in (datasets or [])],
            "limitations": [l.to_dict() if hasattr(l, 'to_dict') else l for l in (limitations or [])],
            "future_work": [f.to_dict() if hasattr(f, 'to_dict') else f for f in (future_work or [])]
        }
    
    if not all_data:
        raise HTTPException(404, "No papers found with the provided IDs")
    
    # 2. Generate HTML via LLM
    llm = get_llm_client()
    
    # Serialize data, truncating if too long
    data_json = json.dumps(all_data, indent=2, ensure_ascii=False, default=str)
    if len(data_json) > 50000:
        data_json = data_json[:50000] + "\n... [truncated]"
    
    prompt = f"""You are a data visualization expert. Generate an HTML page that visualizes the following research paper data according to the user's query.

USER QUERY: {request.query}

DATA (from {len(all_data)} papers):
{data_json}

REQUIREMENTS:
- Output ONLY valid HTML (no markdown, no explanation, no code fences)
- Start with <!DOCTYPE html> and include complete HTML structure
- Include inline CSS in a <style> tag in the <head>
- Include inline JavaScript in a <script> tag at the end of <body> if needed
- Make it visually clean and professional with a modern design
- Use a cohesive color scheme (prefer dark theme with accent colors)
- Include interactive elements where useful (collapsible sections, hover effects, click to expand)
- The HTML must be completely self-contained with no external dependencies
- For tables: use alternating row colors, proper headers, and good padding
- For lists: use cards or grid layouts when showing multiple items
- Include a title/header that reflects the query
- If comparing papers, show paper titles prominently

OUTPUT THE HTML NOW:"""

    try:
        html = llm.complete(prompt)
    except Exception as e:
        raise HTTPException(500, f"LLM generation failed: {str(e)}")
    
    # Clean up response (remove markdown code fences if present)
    html = html.strip()
    if html.startswith("```html"):
        html = html[7:]
    elif html.startswith("```"):
        html = html[3:]
    if html.endswith("```"):
        html = html[:-3]
    html = html.strip()
    
    # Ensure it starts with DOCTYPE or html tag
    if not html.lower().startswith("<!doctype") and not html.lower().startswith("<html"):
        # Wrap in basic HTML structure
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualization</title>
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; padding: 20px; background: #1a1a2e; color: #eee; }}
    </style>
</head>
<body>
{html}
</body>
</html>"""
    
    return {
        "html": html,
        "paper_count": len(all_data),
        "query": request.query
    }


@app.get("/api/papers/{paper_id}/export/contributions")
def export_contributions(paper_id: str, format: str = "json"):
    """Export contributions as JSON or CSV"""
    contributions = load_contributions(paper_id)
    if not contributions:
        raise HTTPException(404, "No contributions found for this paper")
    
    if format == "csv":
        import csv
        from io import StringIO
        
        output = StringIO()
        fieldnames = ["contribution_type", "specific_innovation", "problem_addressed", "evidence_location", "comment"]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows([c.to_dict() for c in contributions])
        
        from fastapi.responses import Response
        return Response(
            content=output.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={paper_id}_contributions.csv"}
        )
    
    # JSON format
    return {
        "paper_id": paper_id,
        "contributions": [c.to_dict() for c in contributions],
        "exported_at": str(datetime.now())
    }


@app.get("/api/papers/{paper_id}/export/experiments")
def export_experiments(paper_id: str, format: str = "json"):
    """Export experiments as JSON or CSV"""
    experiments = load_experiments(paper_id)
    if not experiments:
        raise HTTPException(404, "No experiments found for this paper")
    
    if format == "csv":
        import csv
        from io import StringIO
        
        output = StringIO()
        fieldnames = ["experiment_id", "name", "description", "task", "evidence_location"]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        for exp in experiments:
            writer.writerow({
                "experiment_id": exp.experiment_id,
                "name": exp.name,
                "description": exp.description,
                "task": exp.task,
                "evidence_location": exp.evidence_location
            })
        
        from fastapi.responses import Response
        return Response(
            content=output.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={paper_id}_experiments.csv"}
        )
    
    # JSON format
    return {
        "paper_id": paper_id,
        "experiments": [e.to_dict() for e in experiments],
        "exported_at": str(datetime.now())
    }


@app.get("/api/papers/{paper_id}/export/all")
def export_all(paper_id: str, format: str = "json"):
    """Export everything (paper, contributions, experiments) as JSON"""
    paper_data = load_parsed_paper(paper_id)
    if not paper_data:
        raise HTTPException(404, "Paper not found")
    
    contributions = load_contributions(paper_id) or []
    experiments = load_experiments(paper_id) or []
    
    result = {
        "paper": paper_data,
        "contributions": [c.to_dict() for c in contributions],
        "experiments": [e.to_dict() for e in experiments],
        "exported_at": str(datetime.now())
    }
    
    if format == "markdown":
        # Generate markdown report
        md = f"""# {paper_data.get('title', 'Research Paper Analysis')}

## Paper Information
- **Authors**: {', '.join(paper_data.get('authors', []))}
- **Pages**: {paper_data.get('num_pages', 'N/A')}

## Abstract
{paper_data.get('abstract', 'N/A')}

## Contributions ({len(contributions)})
"""
        for i, c in enumerate(contributions, 1):
            md += f"\n### {i}. {c.contribution_type}\n"
            md += f"**Innovation**: {c.specific_innovation}\n\n"
            md += f"**Problem**: {c.problem_addressed}\n\n"
            md += f"**Location**: {c.evidence_location}\n\n"
        
        md += f"\n## Experiments ({len(experiments)})\n"
        for i, e in enumerate(experiments, 1):
            md += f"\n### {i}. {e.name}\n"
            md += f"**Task**: {e.task}\n\n"
            md += f"**Description**: {e.description}\n\n"
            md += f"**Datasets**: {', '.join([d.get('name', 'Unknown') for d in e.datasets])}\n\n"
        
        from fastapi.responses import Response
        return Response(
            content=md,
            media_type="text/markdown",
            headers={"Content-Disposition": f"attachment; filename={paper_id}_report.md"}
        )
    
    return result


@app.get("/api/papers")
def list_papers() -> Dict[str, Any]:
    """List all uploaded papers"""
    papers = []
    for paper_file in EXTRACTED_DIR.glob("*_paper.json"):
        with open(paper_file, 'r') as f:
            paper_data = json.load(f)
            papers.append({
                "paper_id": paper_data["paper_id"],
                "title": paper_data["title"],
                "authors": paper_data.get("authors", []),
                "num_pages": paper_data.get("num_pages", 0)
            })
    
    return {
        "papers": papers,
        "total": len(papers)
    }


@app.get("/api/analysis/contributions")
def analyze_contributions(paper_ids: str) -> Dict[str, Any]:
    """Aggregate contributions across multiple papers"""
    ids = paper_ids.split(",")
    engine = AggregationEngine(EXTRACTED_DIR)
    return engine.aggregate_contributions(ids)


@app.get("/api/analysis/experiments")
def analyze_experiments(paper_ids: str) -> Dict[str, Any]:
    """Aggregate experiments across multiple papers"""
    ids = paper_ids.split(",")
    engine = AggregationEngine(EXTRACTED_DIR)
    return engine.aggregate_experiments(ids)


@app.get("/api/analysis/patterns")
def analyze_patterns(paper_ids: str) -> Dict[str, Any]:
    """Detect patterns across multiple papers"""
    ids = paper_ids.split(",")
    engine = AggregationEngine(EXTRACTED_DIR)
    return engine.find_patterns(ids)


@app.get("/api/analysis/gaps")
def analyze_gaps(paper_ids: str) -> Dict[str, Any]:
    """Identify research gaps across papers"""
    ids = paper_ids.split(",")
    engine = AggregationEngine(EXTRACTED_DIR)
    return engine.find_gaps(ids)


# ============================================================================
# Run Server
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.api_port)

