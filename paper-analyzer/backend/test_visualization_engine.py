#!/usr/bin/env python3
"""
Test script for the Enhanced Visualization Engine

This demonstrates the multi-stage pipeline:
1. Query Analysis
2. Best Practices Generation
3. Query Enhancement
4. Smart Data Selection
5. Visualization Generation
"""

import json
from visualization_engine import VisualizationEngine, QueryAnalysis, DataSelectionStrategy, EnhancedQuery


class MockLLM:
    """Mock LLM client for testing"""
    
    def complete(self, prompt: str, system_prompt: str = None) -> str:
        """Mock HTML generation"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Test Visualization</title>
    <style>
        body { font-family: sans-serif; padding: 20px; background: #0a0e27; color: #eee; }
        .card { background: #16213e; padding: 20px; margin: 10px; border-radius: 8px; }
    </style>
</head>
<body>
    <h1>Test Visualization</h1>
    <div class="card">Mock generated content</div>
</body>
</html>"""
    
    def complete_json(self, prompt: str, system_prompt: str = None) -> dict:
        """Mock JSON responses based on prompt content"""
        
        if "Analyze this visualization query" in prompt:
            # Query analysis response
            return {
                "intent": "compare",
                "focus_areas": ["contributions", "experiments"],
                "visualization_type": "table",
                "complexity": "medium",
                "requires_cross_paper_analysis": True,
                "key_aspects": ["performance", "methods"]
            }
        
        elif "Generate specific best practices" in prompt:
            # Best practices response
            return {
                "best_practices": [
                    "Use a side-by-side comparison table with papers as columns",
                    "Highlight key differences with color coding",
                    "Include a summary section at the top",
                    "Show performance metrics prominently",
                    "Use collapsible sections for detailed information"
                ]
            }
        
        elif "Enhance this visualization query" in prompt:
            # Query enhancement response
            return {
                "enhanced_query": "Create a comprehensive comparison table showing contributions and experimental results across all papers. Use a side-by-side layout with papers as columns, highlighting key performance differences. Include collapsible sections for detailed experiment information and a summary header showing the most important findings.",
                "key_requirements": [
                    "Side-by-side comparison layout",
                    "Color-coded performance differences",
                    "Collapsible detail sections",
                    "Summary header with key findings"
                ],
                "style_guidelines": {
                    "layout": "Table-based with sticky headers and horizontal scrolling",
                    "colors": "Dark theme with green for improvements, red for regressions",
                    "typography": "Clear hierarchy with large headings and readable body text"
                }
            }
        
        return {}


def create_mock_paper_data(num_papers: int = 3) -> dict:
    """Create mock paper data for testing"""
    papers = {}
    
    for i in range(num_papers):
        paper_id = f"paper_{i+1}"
        papers[paper_id] = {
            "paper": {
                "title": f"Test Paper {i+1}: Novel Approach to Problem X",
                "authors": [f"Author {j+1}" for j in range(3)],
                "abstract": f"This paper presents a novel approach to solving problem X. We introduce method Y and achieve Z% improvement."
            },
            "contributions": [
                {
                    "contribution_type": "architecture",
                    "specific_innovation": f"Novel architecture component {i+1}",
                    "problem_addressed": "Improving computational efficiency",
                    "evidence_location": "Section 3.2"
                },
                {
                    "contribution_type": "training",
                    "specific_innovation": f"New training procedure {i+1}",
                    "problem_addressed": "Faster convergence",
                    "evidence_location": "Section 4.1"
                }
            ],
            "experiments": [
                {
                    "experiment_name": f"Main Benchmark Evaluation {i+1}",
                    "dataset": "CIFAR-10",
                    "metrics": ["Accuracy", "F1-Score"],
                    "results": {
                        "accuracy": 0.92 + i * 0.01,
                        "f1_score": 0.90 + i * 0.01
                    },
                    "baselines": ["ResNet-50", "VGG-16"]
                }
            ],
            "architectures": [
                {
                    "architecture_name": f"Model-{i+1}",
                    "components": ["Encoder", "Decoder", "Attention"],
                    "parameters": f"{10 + i}M parameters"
                }
            ],
            "datasets": [
                {"name": "CIFAR-10", "split": "train/test", "size": "60k"},
                {"name": "ImageNet", "split": "validation", "size": "50k"}
            ],
            "baselines": [
                {"name": "ResNet-50", "source": "Original paper"},
                {"name": "VGG-16", "source": "Baseline repository"}
            ]
        }
    
    return papers


def print_section(title: str, content: str = None):
    """Print a formatted section"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)
    if content:
        print(content)


def main():
    """Test the visualization engine"""
    
    print_section("ENHANCED VISUALIZATION ENGINE TEST")
    print("\nThis test demonstrates the multi-stage pipeline for generating visualizations.\n")
    
    # Initialize engine with mock LLM
    llm = MockLLM()
    engine = VisualizationEngine(llm)
    
    # Test query
    test_query = "Compare contributions and experiments across papers"
    paper_ids = ["paper_1", "paper_2", "paper_3"]
    
    print_section("INPUT")
    print(f"Query: {test_query}")
    print(f"Papers: {len(paper_ids)}")
    
    # Create mock data
    mock_data = create_mock_paper_data(len(paper_ids))
    
    # Stage 1: Query Analysis
    print_section("STAGE 1: Query Analysis")
    analysis = engine.analyze_query(test_query, len(paper_ids))
    print(f"Intent: {analysis.intent}")
    print(f"Focus Areas: {', '.join(analysis.focus_areas)}")
    print(f"Visualization Type: {analysis.visualization_type}")
    print(f"Complexity: {analysis.complexity}")
    print(f"Requires Cross-Paper Analysis: {analysis.requires_cross_paper_analysis}")
    
    # Stage 2: Best Practices Generation
    print_section("STAGE 2: Best Practices Generation")
    best_practices = engine.generate_best_practices(analysis)
    for i, practice in enumerate(best_practices, 1):
        print(f"{i}. {practice}")
    
    # Stage 3: Query Enhancement
    print_section("STAGE 3: Query Enhancement")
    enhanced_query = engine.enhance_query(test_query, analysis, best_practices)
    print(f"\nOriginal Query:\n  {enhanced_query.original_query}")
    print(f"\nEnhanced Query:\n  {enhanced_query.enhanced_query}")
    print(f"\nStyle Guidelines:")
    for key, value in enhanced_query.style_guidelines.items():
        print(f"  - {key}: {value}")
    
    # Stage 4: Data Selection Strategy
    print_section("STAGE 4: Data Selection Strategy")
    strategy = engine.create_data_selection_strategy(analysis)
    print(f"Selected Extractors: {', '.join(strategy.extractors)}")
    print(f"Priority Order: {', '.join(strategy.priority_order)}")
    print(f"Include Metadata: {strategy.include_metadata}")
    print(f"Include Cross-References: {strategy.include_cross_references}")
    print(f"\nItem Limits:")
    for extractor in strategy.extractors:
        limit = strategy.max_items_per_extractor.get(extractor, "N/A")
        print(f"  - {extractor}: {limit}")
    
    # Stage 5: Data Filtering
    print_section("STAGE 5: Data Filtering")
    filtered_data = engine.filter_and_prepare_data(mock_data, strategy, analysis)
    print(f"Papers processed: {len([k for k in filtered_data.keys() if not k.startswith('_')])}")
    
    for paper_id, paper_data in filtered_data.items():
        if paper_id.startswith("_"):
            continue
        print(f"\n{paper_id}:")
        for extractor in strategy.extractors:
            if extractor in paper_data:
                count = len(paper_data[extractor]) if isinstance(paper_data[extractor], list) else 1
                print(f"  - {extractor}: {count} items")
    
    if "_cross_paper_insights" in filtered_data:
        print("\nCross-Paper Insights:")
        insights = filtered_data["_cross_paper_insights"]
        for key, value in insights.items():
            print(f"  - {key}: {value}")
    
    # Stage 6: Prompt Building
    print_section("STAGE 6: Enhanced Prompt Building")
    prompt = engine.build_enhanced_visualization_prompt(enhanced_query, filtered_data, analysis)
    
    # Show a preview of the prompt
    prompt_lines = prompt.split('\n')
    print("Prompt Structure:")
    current_section = None
    for line in prompt_lines[:50]:  # Show first 50 lines
        if line.startswith("<") and ">" in line:
            section = line.split(">")[0][1:]
            if section != current_section and not section.startswith("/"):
                current_section = section
                print(f"  ✓ Section: {current_section}")
    
    print(f"\nTotal prompt length: {len(prompt)} characters")
    print(f"Total lines: {len(prompt_lines)}")
    
    # Stage 7: Full Pipeline Test
    print_section("STAGE 7: Full Pipeline Execution")
    print("Running complete pipeline...")
    
    html, metadata = engine.generate_visualization(paper_ids, test_query, mock_data)
    
    print("\n✓ Visualization generated successfully!")
    print(f"\nMetadata:")
    print(f"  Original Query: {metadata['original_query']}")
    print(f"  Enhanced Query: {metadata['enhanced_query'][:100]}...")
    print(f"  Intent: {metadata['analysis']['intent']}")
    print(f"  Focus Areas: {', '.join(metadata['analysis']['focus_areas'])}")
    print(f"  Extractors Used: {', '.join(metadata['data_selection']['extractors_used'])}")
    print(f"  Best Practices Applied: {len(metadata['best_practices_applied'])}")
    
    print(f"\nHTML Output:")
    print(f"  Length: {len(html)} characters")
    print(f"  Lines: {len(html.split(chr(10)))}")
    print(f"  Valid HTML: {html.strip().startswith('<!DOCTYPE')}")
    
    # Save output for inspection
    output_file = "/tmp/test_visualization.html"
    with open(output_file, 'w') as f:
        f.write(html)
    print(f"\n✓ HTML saved to: {output_file}")
    
    # Save metadata
    metadata_file = "/tmp/test_visualization_metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"✓ Metadata saved to: {metadata_file}")
    
    print_section("TEST COMPLETE")
    print("\nThe enhanced visualization engine is working correctly!")
    print("Key improvements:")
    print("  1. ✓ Multi-stage query analysis")
    print("  2. ✓ Automatic best practices generation")
    print("  3. ✓ Intelligent query enhancement")
    print("  4. ✓ Smart data selection and filtering")
    print("  5. ✓ Comprehensive prompt building")
    print("  6. ✓ Metadata tracking for transparency")
    print("\nNext steps:")
    print("  - Test with real LLM (DeepSeek/Claude)")
    print("  - Test with actual paper data")
    print("  - Compare output quality with old system")
    print("  - Fine-tune data selection limits")


if __name__ == "__main__":
    main()
