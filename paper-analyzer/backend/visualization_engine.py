"""
Enhanced Visualization Engine with Query Enhancement and Smart Data Selection

This module implements a multi-stage pipeline:
1. Query Analysis - Understand intent and requirements
2. Best Practices Generation - Create query-specific guidelines
3. Query Enhancement - Rewrite query for optimal results
4. Smart Data Selection - Choose relevant extractors and data
5. Visualization Generation - Create HTML with enhanced context
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import json
import re


@dataclass
class QueryAnalysis:
    """Analysis of user's visualization query"""
    intent: str  # "compare", "summarize", "explore", "timeline", etc.
    focus_areas: List[str]  # ["contributions", "experiments", etc.]
    visualization_type: str  # "table", "cards", "timeline", etc.
    complexity: str  # "simple", "medium", "complex"
    paper_count: int
    requires_cross_paper_analysis: bool


@dataclass
class DataSelectionStrategy:
    """Strategy for selecting and filtering data"""
    extractors: List[str]  # Which extractors to use
    max_items_per_extractor: Dict[str, int]  # Limits per extractor
    include_metadata: bool
    include_cross_references: bool
    priority_order: List[str]  # Order of importance


@dataclass
class EnhancedQuery:
    """Enhanced version of user query with best practices"""
    original_query: str
    enhanced_query: str
    best_practices: List[str]
    constraints: List[str]
    style_guidelines: Dict[str, str]


class VisualizationEngine:
    """Main engine for enhanced visualization generation"""
    
    def __init__(self, llm_client):
        self.llm = llm_client
        
    def analyze_query(self, query: str, paper_count: int) -> QueryAnalysis:
        """
        Stage 1: Analyze the user's query to understand intent and requirements
        """
        analysis_prompt = f"""Analyze this visualization query and extract structured information.

USER QUERY: "{query}"
PAPER COUNT: {paper_count}

Analyze the query and output JSON with:
{{
  "intent": "<compare|summarize|explore|timeline|cluster|filter|detail>",
  "focus_areas": ["<list of relevant data types: contributions, experiments, architectures, hyperparameters, ablations, baselines, datasets, limitations, future_work, algorithms, equations, training, metrics, loss_functions, related_work, claims>"],
  "visualization_type": "<table|cards|timeline|graph|matrix|list|detail_view>",
  "complexity": "<simple|medium|complex>",
  "requires_cross_paper_analysis": <true|false>,
  "key_aspects": ["<specific things to highlight>"]
}}

Examples:
- "Show me all contributions" → intent: summarize, focus: [contributions], viz: cards
- "Compare training procedures across papers" → intent: compare, focus: [training], viz: table
- "Timeline of architectural improvements" → intent: timeline, focus: [architectures], viz: timeline

Output ONLY the JSON:"""

        try:
            response = self.llm.complete_json(analysis_prompt)
            
            return QueryAnalysis(
                intent=response.get("intent", "summarize"),
                focus_areas=response.get("focus_areas", []),
                visualization_type=response.get("visualization_type", "cards"),
                complexity=response.get("complexity", "medium"),
                paper_count=paper_count,
                requires_cross_paper_analysis=response.get("requires_cross_paper_analysis", False)
            )
        except Exception as e:
            # Fallback to basic analysis
            return self._fallback_query_analysis(query, paper_count)
    
    def _fallback_query_analysis(self, query: str, paper_count: int) -> QueryAnalysis:
        """Fallback query analysis using keyword matching"""
        query_lower = query.lower()
        
        # Detect intent
        if any(w in query_lower for w in ["compare", "versus", "vs", "difference"]):
            intent = "compare"
        elif any(w in query_lower for w in ["timeline", "evolution", "over time"]):
            intent = "timeline"
        elif any(w in query_lower for w in ["cluster", "group", "categorize"]):
            intent = "cluster"
        elif any(w in query_lower for w in ["all", "show", "list"]):
            intent = "summarize"
        else:
            intent = "explore"
        
        # Detect focus areas
        extractor_keywords = {
            "contributions": ["contribution", "innovation", "novelty", "propose"],
            "experiments": ["experiment", "result", "performance", "evaluation"],
            "architectures": ["architecture", "model", "network", "structure"],
            "training": ["training", "optimization", "learning"],
            "hyperparameters": ["hyperparameter", "learning rate", "batch size"],
            "baselines": ["baseline", "comparison", "prior work"],
            "datasets": ["dataset", "benchmark", "data"],
            "limitations": ["limitation", "weakness", "drawback"],
        }
        
        focus_areas = []
        for extractor, keywords in extractor_keywords.items():
            if any(kw in query_lower for kw in keywords):
                focus_areas.append(extractor)
        
        # If no specific focus, include key extractors
        if not focus_areas:
            focus_areas = ["contributions", "experiments", "architectures"]
        
        return QueryAnalysis(
            intent=intent,
            focus_areas=focus_areas,
            visualization_type="table" if intent == "compare" else "cards",
            complexity="medium",
            paper_count=paper_count,
            requires_cross_paper_analysis=paper_count > 1
        )
    
    def generate_best_practices(self, analysis: QueryAnalysis) -> List[str]:
        """
        Stage 2: Generate query-specific best practices
        """
        best_practices_prompt = f"""Generate specific best practices for creating a visualization based on this analysis:

INTENT: {analysis.intent}
FOCUS AREAS: {', '.join(analysis.focus_areas)}
VISUALIZATION TYPE: {analysis.visualization_type}
PAPER COUNT: {analysis.paper_count}
COMPLEXITY: {analysis.complexity}

Generate 5-10 specific, actionable best practices for this visualization. Consider:
- Layout and organization
- Information hierarchy
- Interactive elements
- Visual design
- Data presentation
- User experience

Output as JSON:
{{
  "best_practices": [
    "Specific practice 1...",
    "Specific practice 2...",
    ...
  ]
}}"""

        try:
            response = self.llm.complete_json(best_practices_prompt)
            return response.get("best_practices", [])
        except:
            # Fallback to general best practices
            return self._get_general_best_practices(analysis)
    
    def _get_general_best_practices(self, analysis: QueryAnalysis) -> List[str]:
        """Fallback best practices based on query analysis"""
        practices = []
        
        if analysis.intent == "compare":
            practices.extend([
                "Use a side-by-side comparison layout with aligned attributes",
                "Highlight differences with color coding (red for worse, green for better)",
                "Include a summary section at the top showing key differences",
                "Use consistent ordering across all papers"
            ])
        
        if analysis.paper_count > 5:
            practices.append("Implement collapsible sections to manage information density")
            practices.append("Add a table of contents or navigation for quick access")
        
        if "experiments" in analysis.focus_areas:
            practices.extend([
                "Show baseline comparisons with clear performance deltas",
                "Group experiments by type (main vs ablation)",
                "Include dataset and metric information prominently"
            ])
        
        if analysis.visualization_type == "table":
            practices.extend([
                "Use sticky headers for scrollable tables",
                "Add alternating row colors for readability",
                "Make columns sortable if possible"
            ])
        
        # Always include these
        practices.extend([
            "Use a clear visual hierarchy with proper heading levels",
            "Implement hover effects for interactive elements",
            "Ensure responsive design that works at different viewport sizes"
        ])
        
        return practices
    
    def enhance_query(self, original_query: str, analysis: QueryAnalysis, 
                     best_practices: List[str]) -> EnhancedQuery:
        """
        Stage 3: Enhance the query based on analysis and best practices
        """
        enhancement_prompt = f"""Enhance this visualization query to be more specific and actionable.

ORIGINAL QUERY: "{original_query}"

CONTEXT:
- Intent: {analysis.intent}
- Focus: {', '.join(analysis.focus_areas)}
- Visualization type: {analysis.visualization_type}
- Number of papers: {analysis.paper_count}

BEST PRACTICES TO INCORPORATE:
{chr(10).join(f'- {bp}' for bp in best_practices)}

Create an enhanced query that:
1. Is more specific about what to show
2. Includes layout/structure guidance
3. Specifies interaction patterns
4. Mentions key visual elements

Output JSON:
{{
  "enhanced_query": "Enhanced detailed query here...",
  "key_requirements": ["req1", "req2", ...],
  "style_guidelines": {{
    "layout": "description",
    "colors": "description",
    "typography": "description"
  }}
}}

The enhanced query should be 2-4 sentences that a designer could follow."""

        try:
            response = self.llm.complete_json(enhancement_prompt)
            
            return EnhancedQuery(
                original_query=original_query,
                enhanced_query=response.get("enhanced_query", original_query),
                best_practices=best_practices,
                constraints=response.get("key_requirements", []),
                style_guidelines=response.get("style_guidelines", {})
            )
        except:
            # Fallback enhancement
            return self._fallback_query_enhancement(original_query, analysis, best_practices)
    
    def _fallback_query_enhancement(self, original_query: str, analysis: QueryAnalysis,
                                    best_practices: List[str]) -> EnhancedQuery:
        """Fallback query enhancement"""
        
        # Build enhanced query
        enhanced_parts = [original_query]
        
        if analysis.visualization_type == "table":
            enhanced_parts.append(f"Present as a comparison table with papers as columns and {', '.join(analysis.focus_areas)} as rows.")
        elif analysis.visualization_type == "cards":
            enhanced_parts.append(f"Display using a card-based grid layout with one card per paper.")
        
        if analysis.paper_count > 3:
            enhanced_parts.append("Include filtering and search capabilities.")
        
        enhanced_parts.append("Use a modern dark theme with clear visual hierarchy.")
        
        return EnhancedQuery(
            original_query=original_query,
            enhanced_query=" ".join(enhanced_parts),
            best_practices=best_practices,
            constraints=[
                "Must be self-contained HTML",
                "No external dependencies",
                "Mobile responsive"
            ],
            style_guidelines={
                "layout": "grid-based with proper spacing",
                "colors": "dark theme with accent colors",
                "typography": "system fonts, clear hierarchy"
            }
        )
    
    def create_data_selection_strategy(self, analysis: QueryAnalysis) -> DataSelectionStrategy:
        """
        Stage 4: Determine which data to include and how much
        """
        
        # Determine extractors based on focus areas
        extractors = list(set(analysis.focus_areas))  # Remove duplicates
        
        # Add related extractors
        if "experiments" in extractors:
            if "baselines" not in extractors:
                extractors.append("baselines")
            if "datasets" not in extractors:
                extractors.append("datasets")
            if "metrics" not in extractors:
                extractors.append("metrics")
        
        if "architectures" in extractors:
            if "hyperparameters" not in extractors:
                extractors.append("hyperparameters")
        
        # If no specific extractors, use all key ones
        if not extractors:
            extractors = ["contributions", "experiments", "architectures", "datasets", "baselines"]
        
        # Determine limits based on paper count and complexity
        if analysis.paper_count == 1:
            # Single paper: show everything
            max_items = {
                "contributions": 999,
                "experiments": 999,
                "architectures": 999,
                "hyperparameters": 999,
                "ablations": 999,
                "baselines": 999,
                "datasets": 999,
                "algorithms": 999,
                "equations": 50,
                "training": 999,
                "metrics": 999,
                "loss_functions": 999,
                "limitations": 999,
                "future_work": 999,
                "related_work": 20,
                "claims": 20,
                "code_resources": 999
            }
        elif analysis.paper_count <= 3:
            # Few papers: be generous
            max_items = {
                "contributions": 10,
                "experiments": 15,
                "architectures": 5,
                "hyperparameters": 5,
                "ablations": 10,
                "baselines": 15,
                "datasets": 10,
                "algorithms": 5,
                "equations": 20,
                "training": 5,
                "metrics": 15,
                "loss_functions": 10,
                "limitations": 10,
                "future_work": 10,
                "related_work": 10,
                "claims": 10,
                "code_resources": 10
            }
        else:
            # Many papers: be selective
            max_items = {
                "contributions": 5,
                "experiments": 8,
                "architectures": 3,
                "hyperparameters": 3,
                "ablations": 5,
                "baselines": 10,
                "datasets": 8,
                "algorithms": 3,
                "equations": 10,
                "training": 3,
                "metrics": 10,
                "loss_functions": 5,
                "limitations": 5,
                "future_work": 5,
                "related_work": 5,
                "claims": 5,
                "code_resources": 5
            }
        
        # Priority order
        priority_order = extractors.copy()
        
        # Ensure primary focus areas are first
        for focus in analysis.focus_areas:
            if focus in priority_order:
                priority_order.remove(focus)
                priority_order.insert(0, focus)
        
        return DataSelectionStrategy(
            extractors=extractors,
            max_items_per_extractor=max_items,
            include_metadata=True,
            include_cross_references=analysis.requires_cross_paper_analysis,
            priority_order=priority_order
        )
    
    def filter_and_prepare_data(self, all_raw_data: Dict[str, Any], 
                                strategy: DataSelectionStrategy,
                                query_analysis: QueryAnalysis) -> Dict[str, Any]:
        """
        Stage 5: Apply data selection strategy and prepare data for visualization
        """
        filtered_data = {}
        
        for paper_id, paper_data in all_raw_data.items():
            filtered_paper = {
                "paper": paper_data.get("paper", {}),
                "_metadata": {
                    "paper_id": paper_id,
                    "selected_extractors": strategy.extractors
                }
            }
            
            # Filter each extractor's data
            for extractor in strategy.extractors:
                if extractor not in paper_data:
                    continue
                
                data = paper_data[extractor]
                if not data:
                    continue
                
                # Apply limits
                max_items = strategy.max_items_per_extractor.get(extractor, 999)
                
                if isinstance(data, list):
                    # Truncate list if too long
                    filtered_paper[extractor] = data[:max_items]
                    
                    # Add count metadata
                    if len(data) > max_items:
                        filtered_paper[extractor].append({
                            "_note": f"Showing {max_items} of {len(data)} total items"
                        })
                else:
                    filtered_paper[extractor] = data
            
            filtered_data[paper_id] = filtered_paper
        
        # Add cross-paper analysis if needed
        if strategy.include_cross_references and len(filtered_data) > 1:
            filtered_data["_cross_paper_insights"] = self._generate_cross_paper_insights(
                filtered_data, query_analysis
            )
        
        return filtered_data
    
    def _generate_cross_paper_insights(self, data: Dict[str, Any], 
                                      analysis: QueryAnalysis) -> Dict[str, Any]:
        """Generate insights across multiple papers"""
        insights = {}
        
        # Find common datasets
        all_datasets = []
        for paper_id, paper_data in data.items():
            if paper_id.startswith("_"):
                continue
            datasets = paper_data.get("datasets", [])
            all_datasets.extend([d.get("name") if isinstance(d, dict) else str(d) 
                               for d in datasets])
        
        if all_datasets:
            from collections import Counter
            dataset_counts = Counter(all_datasets)
            insights["common_datasets"] = [
                {"name": name, "paper_count": count}
                for name, count in dataset_counts.most_common(10)
                if count > 1
            ]
        
        # Count paper contributions by type
        if "contributions" in analysis.focus_areas:
            contribution_types = []
            for paper_id, paper_data in data.items():
                if paper_id.startswith("_"):
                    continue
                contribs = paper_data.get("contributions", [])
                for c in contribs:
                    if isinstance(c, dict):
                        contribution_types.append(c.get("contribution_type", "unknown"))
            
            if contribution_types:
                from collections import Counter
                type_counts = Counter(contribution_types)
                insights["contribution_distribution"] = dict(type_counts)
        
        return insights
    
    def build_enhanced_visualization_prompt(self, enhanced_query: EnhancedQuery,
                                           filtered_data: Dict[str, Any],
                                           analysis: QueryAnalysis) -> str:
        """
        Stage 6: Build the final prompt for HTML generation
        """
        
        # Serialize data
        data_json = json.dumps(filtered_data, indent=2, ensure_ascii=False, default=str)
        
        # Build comprehensive prompt
        prompt = f"""<role>You are a senior data visualization designer specializing in scientific research papers.</role>

<task>Generate a complete, professional HTML visualization of research paper data.</task>

<original_user_query>{enhanced_query.original_query}</original_user_query>

<enhanced_visualization_requirements>
{enhanced_query.enhanced_query}
</enhanced_visualization_requirements>

<query_analysis>
- Intent: {analysis.intent}
- Focus: {', '.join(analysis.focus_areas)}
- Visualization type: {analysis.visualization_type}
- Paper count: {analysis.paper_count}
- Complexity: {analysis.complexity}
</query_analysis>

<best_practices>
{chr(10).join(f'{i+1}. {bp}' for i, bp in enumerate(enhanced_query.best_practices))}
</best_practices>

<data>
{data_json}
</data>

<technical_requirements>
- Output ONLY valid HTML - no markdown, no explanations, no code fences
- Start with <!DOCTYPE html> and include complete HTML structure
- Use inline CSS in <style> tag in <head>
- Use inline JavaScript in <script> tag at end of <body> if needed
- Completely self-contained - NO external dependencies (no CDNs, no external fonts)
- Modern, clean design with proper spacing and typography
</technical_requirements>

<design_system>
Colors:
- Background: #0a0e27 (dark blue-black)
- Cards/Panels: #16213e (navy blue)
- Accent: #e94560 (coral red)
- Secondary: #0f3460 (deep blue)
- Text: #eee (light gray)
- Muted text: #a8a8a8

Typography:
- Font family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif
- Base size: 16px
- Headings: 1.5rem to 2.5rem with bold weight
- Body: 1rem with line-height 1.6

Layout:
- {enhanced_query.style_guidelines.get('layout', 'Grid-based with proper spacing')}
- Max width: 1400px, centered
- Padding: 2rem
- Card spacing: 1.5rem gap

Interactive Elements:
- Smooth transitions (0.3s ease)
- Hover effects: transform: translateY(-4px) and shadow
- Collapsible sections: Use <details> and <summary> tags
- Click indicators: cursor: pointer, subtle color changes
</design_system>

CRITICAL - CREATE MASSIVE, INFORMATION-DENSE VISUALIZATION:
- This MUST be AT LEAST 3 full screens of scrollable content (3000+ pixels minimum height)
- Include EVERY piece of data available - do NOT summarize or truncate
- Create 5-10 major sections with detailed subsections
- Use <details> tags extensively to pack more information densely
- Include comprehensive tables showing ALL data points
- Show specific numbers, metrics, percentages, and evidence
- Add summary boxes with statistics
- Create comparison matrices
- Include ALL experiments, ALL contributions, ALL results
- Make it INFORMATION-DENSE but well-organized
- Use grid layouts to fit more content
- The more information, the better!

<mandatory_constraints>
❌ NEVER use external CDNs (cdnjs, unpkg, googleapis, etc.)
❌ NEVER use placeholder/Lorem Ipsum text - use actual data
❌ NEVER output markdown code fences
❌ NEVER use alert() or console.log() for user-facing messages
❌ NEVER create horizontal scroll (use overflow-x: auto on containers if needed)
✓ ALWAYS use semantic HTML (header, main, section, article, nav)
✓ ALWAYS include proper heading hierarchy (h1 → h2 → h3)
✓ ALWAYS make interactive elements keyboard-accessible
✓ ALWAYS use the actual data provided
</mandatory_constraints>

<output_instruction>
Generate the complete HTML now. Remember:
1. Use the enhanced query requirements as your guide
2. Follow all best practices listed above
3. Incorporate the data naturally and comprehensively
4. Create a polished, professional result
5. Start directly with <!DOCTYPE html>
</output_instruction>"""

        return prompt
    
    def generate_visualization(self, paper_ids: List[str], query: str,
                              all_raw_data: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Main pipeline: orchestrate all stages to generate visualization
        
        Returns: (html_string, metadata_dict)
        """
        
        # Stage 1: Analyze query
        analysis = self.analyze_query(query, len(paper_ids))
        
        # Stage 2: Generate best practices
        best_practices = self.generate_best_practices(analysis)
        
        # Stage 3: Enhance query
        enhanced_query = self.enhance_query(query, analysis, best_practices)
        
        # Stage 4: Create data selection strategy
        strategy = self.create_data_selection_strategy(analysis)
        
        # Stage 5: Filter and prepare data
        filtered_data = self.filter_and_prepare_data(all_raw_data, strategy, analysis)
        
        # Stage 6: Build enhanced prompt
        prompt = self.build_enhanced_visualization_prompt(enhanced_query, filtered_data, analysis)
        
        # Stage 7: Generate HTML using STREAMING for longer output!
        print("🚀 Generating MASSIVE HTML using streaming...")
        html = self._generate_html_streaming(prompt)
        
        # Post-process HTML
        html = self._clean_html(html)
        
        # Prepare metadata
        metadata = {
            "original_query": query,
            "enhanced_query": enhanced_query.enhanced_query,
            "analysis": {
                "intent": analysis.intent,
                "focus_areas": analysis.focus_areas,
                "visualization_type": analysis.visualization_type,
                "complexity": analysis.complexity
            },
            "best_practices_applied": best_practices,
            "data_selection": {
                "extractors_used": strategy.extractors,
                "priority_order": strategy.priority_order
            },
            "paper_count": len(paper_ids),
            "html_length": len(html)
        }
        
        return html, metadata
    
    def _generate_html_streaming(self, prompt: str) -> str:
        """
        Generate HTML using streaming for LONG outputs
        """
        # Check if LLM supports streaming
        if hasattr(self.llm, 'complete_streaming'):
            try:
                chunks = []
                chunk_count = 0
                for chunk in self.llm.complete_streaming(prompt, max_tokens=16384):
                    chunks.append(chunk)
                    chunk_count += 1
                    if chunk_count % 50 == 0:
                        print(f"  📦 Received {chunk_count} chunks, {len(''.join(chunks))} chars so far...")
                
                html = ''.join(chunks)
                print(f"✅ Streaming complete! Generated {len(html)} characters ({chunk_count} chunks)")
                return html
            except Exception as e:
                print(f"⚠️  Streaming failed ({e}), falling back to regular generation...")
                return self.llm.complete(prompt, max_tokens=8192)
        else:
            # Fallback to regular completion with increased tokens
            print("⚠️  Streaming not supported, using regular completion with max tokens...")
            return self.llm.complete(prompt, max_tokens=8192)
    
    def _clean_html(self, html: str) -> str:
        """Clean up generated HTML"""
        html = html.strip()
        
        # Remove markdown code fences
        if html.startswith("```html"):
            html = html[7:]
        elif html.startswith("```"):
            html = html[3:]
        if html.endswith("```"):
            html = html[:-3]
        
        html = html.strip()
        
        # Ensure proper HTML structure
        if not html.lower().startswith("<!doctype") and not html.lower().startswith("<html"):
            html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Paper Visualization</title>
    <style>
        body {{ 
            font-family: system-ui, -apple-system, sans-serif; 
            padding: 20px; 
            background: #0a0e27; 
            color: #eee;
            margin: 0;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
    </style>
</head>
<body>
    <div class="container">
        {html}
    </div>
</body>
</html>"""
        
        return html
