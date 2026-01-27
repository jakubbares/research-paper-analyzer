#!/usr/bin/env python3
"""
Generate MASSIVE HTML visualization using the actual Enhanced Visualization Engine with DeepSeek
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from visualization_engine import VisualizationEngine
from extractors import get_llm_client


def create_massive_paper_data():
    """Create data for 10 papers with tons of content"""
    papers = {}
    
    paper_titles = [
        "NeuroSAT: Learning a SAT Solver from Single-Bit Supervision",
        "G4SATBench: Benchmarking and Advancing SAT Solving with Graph Neural Networks",
        "GraSS: Combining Graph Neural Networks with Expert Knowledge for SAT Solving",
        "Circuit-Aware SAT Solving: Guiding CDCL via Conditional Graph Models",
        "HyperSAT: Unsupervised Hypergraph Neural Networks for SAT Solving",
        "Addressing Variable Dependency in GNN-based SAT Solving",
        "Learning from Algorithm Feedback: One-Shot SAT Solving",
        "Learning Branching Heuristics from Graph Neural Networks",
        "STRCMP: Integrating Graph Structural Priors with Large Language Models",
        "Understanding GNNs for Boolean Satisfiability through Lens Theory"
    ]
    
    contribution_types = ["architecture", "training", "data", "loss_function", "method"]
    
    for i, title in enumerate(paper_titles):
        paper_id = f"paper_{i+1}"
        
        # Create 5-7 contributions per paper
        contributions = []
        for j in range(5 + i % 3):
            contrib_type = contribution_types[j % len(contribution_types)]
            contributions.append({
                "contribution_type": contrib_type,
                "specific_innovation": f"Novel {contrib_type} approach: {['Message-passing GNN', 'Attention mechanism', 'Curriculum learning', 'Multi-task loss', 'Hybrid architecture'][j % 5]}",
                "problem_addressed": f"Addresses {['computational efficiency', 'generalization', 'data scarcity', 'interpretability', 'scalability'][j % 5]} in SAT solving",
                "evidence_location": f"Section {3 + j}, Figure {j+1}, Table {j+2}",
                "comment": f"Achieves {85 + i*2 + j}% improvement on benchmark tasks"
            })
        
        # Create 10-15 experiments per paper
        experiments = []
        datasets = ["SAT Competition 2020", "Random 3-SAT", "Industrial Hardware", "Crafted Instances", "Graph Coloring"]
        for j in range(10 + i):
            experiments.append({
                "experiment_name": f"Experiment {j+1}: {datasets[j % len(datasets)]}",
                "dataset": datasets[j % len(datasets)],
                "benchmarks": ["MiniSat", "Glucose", "Lingeling"],
                "baselines": [
                    {"name": "MiniSat", "performance": f"{70 + j*2}%"},
                    {"name": "Glucose", "performance": f"{75 + j*2}%"},
                    {"name": "Lingeling", "performance": f"{78 + j*2}%"}
                ],
                "metrics": ["Accuracy", "Solve Time", "Memory Usage"],
                "results": {
                    "accuracy": f"{85 + i + j}%",
                    "solve_time": f"{1000 - i*50 - j*10}ms",
                    "memory": f"{500 + i*50 + j*20}MB"
                },
                "conclusion": f"Outperforms baselines by {10 + i + j}% on average",
                "ablations": [
                    {"component": "Message passing", "impact": "+12%"},
                    {"component": "Attention", "impact": "+8%"},
                    {"component": "Pre-training", "impact": "+5%"}
                ]
            })
        
        # Create architectures
        architectures = []
        for j in range(3):
            architectures.append({
                "architecture_name": f"Model-{i+1}-V{j+1}",
                "components": ["Encoder", "Message Passing Layers", "Decoder", "Attention"],
                "layers": 20 + i*2 + j*5,
                "parameters": f"{2 + i + j*2}.{i}M",
                "hidden_dim": 128 * (2 ** j),
                "description": f"Graph neural network with {20 + i*2 + j*5} layers and attention mechanism"
            })
        
        # Create datasets used
        datasets_used = [
            {"name": "SAT Competition 2020", "split": "train/test", "size": "10k instances", "difficulty": "mixed"},
            {"name": "Random 3-SAT", "split": "generated", "size": "100k instances", "difficulty": "medium"},
            {"name": "Industrial", "split": "real-world", "size": "500 instances", "difficulty": "hard"},
            {"name": "Crafted", "split": "hand-made", "size": "200 instances", "difficulty": "very hard"}
        ]
        
        # Create baselines
        baselines = [
            {"name": "MiniSat", "version": "2.2.0", "performance": f"{70 + i}%", "type": "CDCL"},
            {"name": "Glucose", "version": "4.0", "performance": f"{75 + i}%", "type": "Modern CDCL"},
            {"name": "Lingeling", "version": "latest", "performance": f"{78 + i}%", "type": "Competition winner"},
            {"name": "CryptoMiniSat", "version": "5.8", "performance": f"{72 + i}%", "type": "Specialized"}
        ]
        
        # Create training details
        training = [{
            "method": ["Adam optimizer", "Learning rate scheduling", "Curriculum learning"][i % 3],
            "learning_rate": 0.001 / (i + 1),
            "batch_size": 32 * (2 ** (i % 3)),
            "epochs": 50 + i*10,
            "training_time": f"{10 + i*3} hours",
            "hardware": "8x NVIDIA A100"
        }]
        
        # Create metrics
        metrics = [
            {"name": "Accuracy", "value": f"{85 + i*2}%", "description": "Classification accuracy"},
            {"name": "Precision", "value": f"{83 + i*2}%", "description": "Positive prediction accuracy"},
            {"name": "Recall", "value": f"{87 + i*2}%", "description": "True positive rate"},
            {"name": "F1 Score", "value": f"{85 + i*2}%", "description": "Harmonic mean"},
            {"name": "Solve Time", "value": f"{1000 - i*100}ms", "description": "Average solving time"}
        ]
        
        papers[paper_id] = {
            "paper": {
                "title": title,
                "authors": [f"Author {j+1} {chr(65+i)}" for j in range(3 + i % 3)],
                "abstract": f"This paper presents a novel approach to SAT solving using graph neural networks. We achieve state-of-the-art results on multiple benchmarks."
            },
            "contributions": contributions,
            "experiments": experiments,
            "architectures": architectures,
            "datasets": datasets_used,
            "baselines": baselines,
            "training": training,
            "metrics": metrics,
            "hyperparameters": [{"param": "hidden_dim", "value": 256 + i*64}],
            "ablations": [{"study": f"Ablation {j+1}", "result": f"+{5+j}%"} for j in range(3)],
            "limitations": [{"limitation": f"Limited generalization to {['large', 'complex', 'novel'][j % 3]} instances"} for j in range(2)],
            "future_work": [{"direction": f"Explore {['meta-learning', 'multi-objective', 'explainable'][j % 3]} approaches"} for j in range(2)]
        }
    
    return papers


def main():
    print("="*80)
    print("  GENERATING MASSIVE VISUALIZATION WITH DEEPSEEK")
    print("="*80)
    
    # Get real LLM client (DeepSeek)
    print("\n1. Initializing DeepSeek LLM client...")
    llm = get_llm_client()
    
    # Create visualization engine
    print("2. Creating VisualizationEngine...")
    engine = VisualizationEngine(llm)
    
    # Create massive dataset
    print("3. Creating massive paper dataset (10 papers with tons of data)...")
    paper_ids = [f"paper_{i+1}" for i in range(10)]
    all_data = create_massive_paper_data()
    
    print(f"   - Papers: {len(paper_ids)}")
    print(f"   - Contributions: {sum(len(p['contributions']) for p in all_data.values())}")
    print(f"   - Experiments: {sum(len(p['experiments']) for p in all_data.values())}")
    
    # User query asking for COMPREHENSIVE visualization
    query = """Show me a comprehensive analysis comparing ALL contributions, experiments, 
    architectures, training methods, and results across ALL papers. I want detailed tables, 
    performance comparisons, dataset usage, baseline comparisons, and key insights. 
    Make it information-dense with lots of data, metrics, and detailed breakdowns. 
    Include collapsible sections for detailed experiment results. This should be 
    at least 3 screens worth of information."""
    
    print(f"\n4. Query: {query[:100]}...")
    
    # RUN THE FULL 7-STAGE PIPELINE WITH DEEPSEEK
    print("\n" + "="*80)
    print("  RUNNING 7-STAGE PIPELINE")
    print("="*80)
    
    try:
        html, metadata = engine.generate_visualization(
            paper_ids=paper_ids,
            query=query,
            all_raw_data=all_data
        )
        
        print("\n✅ PIPELINE COMPLETE!")
        
        # Save the generated HTML
        output_file = "/tmp/deepseek_generated_viz.html"
        with open(output_file, 'w') as f:
            f.write(html)
        
        print(f"\n📊 RESULTS:")
        print(f"  - HTML generated: {len(html):,} characters")
        print(f"  - Lines: {len(html.split(chr(10))):,}")
        print(f"  - Saved to: {output_file}")
        
        print(f"\n📈 METADATA:")
        print(f"  - Original query: {metadata['original_query'][:80]}...")
        print(f"  - Enhanced query: {metadata['enhanced_query'][:100]}...")
        print(f"  - Intent: {metadata['analysis']['intent']}")
        print(f"  - Focus areas: {', '.join(metadata['analysis']['focus_areas'][:5])}")
        print(f"  - Visualization type: {metadata['analysis']['visualization_type']}")
        print(f"  - Extractors used: {', '.join(metadata['data_selection']['extractors_used'])}")
        print(f"  - Best practices: {len(metadata['best_practices_applied'])}")
        
        print("\n" + "="*80)
        print("  ✅ SUCCESS! DeepSeek generated the HTML!")
        print("="*80)
        print(f"\nOpen in browser: file://{output_file}")
        
        # Save metadata
        import json
        with open("/tmp/deepseek_generated_metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print("Metadata saved to: /tmp/deepseek_generated_metadata.json")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
