# Enhanced Visualization Engine

## Overview

The Enhanced Visualization Engine is a sophisticated multi-stage pipeline that transforms simple user queries into optimized, data-driven HTML visualizations. Unlike the previous single-prompt approach, this system analyzes, enhances, and intelligently prepares everything before generation.

## Architecture

### 🔄 Multi-Stage Pipeline

```
User Query → Analyze → Generate Best Practices → Enhance Query → Select Data → Build Prompt → Generate HTML
```

Each stage builds upon the previous one, creating a comprehensive context for optimal visualization generation.

---

## Detailed Pipeline Stages

### Stage 1: Query Analysis 🔍

**Purpose:** Understand the user's intent and requirements

**Process:**
- LLM analyzes the natural language query
- Extracts structured information about intent, focus areas, and complexity
- Determines the optimal visualization type
- Fallback to keyword matching if LLM fails

**Output:** `QueryAnalysis` object containing:
- `intent`: compare, summarize, explore, timeline, cluster, filter, detail
- `focus_areas`: List of relevant extractors (contributions, experiments, etc.)
- `visualization_type`: table, cards, timeline, graph, matrix, list, detail_view
- `complexity`: simple, medium, complex
- `requires_cross_paper_analysis`: boolean

**Example:**
```python
Query: "Compare training procedures across papers"
→ Analysis: {
    intent: "compare",
    focus_areas: ["training", "hyperparameters", "metrics"],
    visualization_type: "table",
    complexity: "medium",
    requires_cross_paper_analysis: True
}
```

---

### Stage 2: Best Practices Generation 📋

**Purpose:** Create query-specific guidelines for visualization

**Process:**
- Based on query analysis, LLM generates 5-10 specific best practices
- Practices cover layout, hierarchy, interactivity, design, and UX
- Fallback to general best practices based on intent patterns

**Output:** List of actionable best practices

**Examples:**
For comparison queries:
- "Use a side-by-side comparison layout with aligned attributes"
- "Highlight differences with color coding (red for worse, green for better)"
- "Include a summary section at the top showing key differences"

For many papers (>5):
- "Implement collapsible sections to manage information density"
- "Add a table of contents or navigation for quick access"

For experiment-focused queries:
- "Show baseline comparisons with clear performance deltas"
- "Group experiments by type (main vs ablation)"

---

### Stage 3: Query Enhancement 🚀

**Purpose:** Transform vague query into specific, actionable instructions

**Process:**
- Takes original query + analysis + best practices
- LLM rewrites query with specific details about layout, structure, and visuals
- Includes style guidelines (layout, colors, typography)
- Fallback to template-based enhancement

**Output:** `EnhancedQuery` object containing:
- `original_query`: User's original text
- `enhanced_query`: 2-4 sentence detailed specification
- `best_practices`: List of practices to apply
- `constraints`: Key requirements
- `style_guidelines`: Dict with layout/colors/typography specs

**Example:**
```python
Original: "Show me all contributions"

Enhanced: "Create a comprehensive grid of contribution cards, one per paper, 
organized by contribution type (architecture, training, data, loss function). 
Each card should display the innovation, problem addressed, and evidence location. 
Use a dark theme with color-coded badges for contribution types. Include hover 
effects and expandable sections for detailed information."
```

---

### Stage 4: Data Selection Strategy 🎯

**Purpose:** Intelligently choose which data to include and how much

**Process:**
- Determines relevant extractors from focus areas
- Adds related extractors (e.g., experiments → baselines + datasets + metrics)
- Sets limits based on paper count and complexity
- Establishes priority order
- Decides on metadata and cross-reference inclusion

**Smart Limits:**
| Paper Count | Contributions | Experiments | Architectures | Notes |
|-------------|---------------|-------------|---------------|-------|
| 1 paper     | No limit      | No limit    | No limit      | Show everything |
| 2-3 papers  | 10 per paper  | 15 per paper| 5 per paper   | Be generous |
| 4+ papers   | 5 per paper   | 8 per paper | 3 per paper   | Be selective |

**Output:** `DataSelectionStrategy` object containing:
- `extractors`: List of extractors to use
- `max_items_per_extractor`: Dict mapping extractor → limit
- `include_metadata`: boolean
- `include_cross_references`: boolean
- `priority_order`: Ordered list of extractors by importance

**Smart Relationships:**
- `experiments` → automatically includes `baselines`, `datasets`, `metrics`
- `architectures` → automatically includes `hyperparameters`
- If no extractors specified → includes `contributions`, `experiments`, `architectures`, `datasets`, `baselines`

---

### Stage 5: Data Filtering & Preparation 📊

**Purpose:** Apply strategy and prepare optimized dataset

**Process:**
1. For each paper, filter data by selected extractors
2. Apply item limits per extractor
3. Add metadata (counts, flags, relevance scores)
4. Generate cross-paper insights (common datasets, contribution distribution)
5. Add truncation notices when limits are applied

**Output:** Filtered data dictionary with:
- Per-paper data (only selected extractors, within limits)
- `_metadata`: Information about selections
- `_cross_paper_insights`: Common patterns, shared resources, clusters

**Cross-Paper Insights:**
- Common datasets and their usage count
- Contribution type distribution
- Shared baselines
- Performance comparison opportunities

---

### Stage 6: Enhanced Prompt Building 📝

**Purpose:** Create comprehensive prompt with all context

**Prompt Structure:**
```xml
<role>Data visualization designer specializing in research papers</role>

<task>Generate complete HTML visualization</task>

<original_user_query>User's original text</original_user_query>

<enhanced_visualization_requirements>
Enhanced query with specifics
</enhanced_visualization_requirements>

<query_analysis>
- Intent
- Focus areas
- Visualization type
- Complexity
</query_analysis>

<best_practices>
Numbered list of practices to apply
</best_practices>

<data>
Filtered JSON data
</data>

<technical_requirements>
- HTML structure requirements
- Self-contained, no external deps
- Inline CSS/JS
</technical_requirements>

<design_system>
Colors:
  - Background: #0a0e27
  - Cards: #16213e
  - Accent: #e94560
  - Text: #eee

Typography:
  - System fonts
  - Base: 16px
  - Headings: 1.5-2.5rem

Layout:
  - Max width: 1400px
  - Grid-based
  - Proper spacing
</design_system>

<mandatory_constraints>
❌ NEVER use external CDNs
❌ NEVER use placeholder text
❌ NEVER output markdown
✓ ALWAYS use semantic HTML
✓ ALWAYS follow best practices
✓ ALWAYS use actual data
</mandatory_constraints>

<output_instruction>
Generate complete HTML now
</output_instruction>
```

---

### Stage 7: HTML Generation & Post-Processing ✨

**Purpose:** Generate and clean final HTML

**Process:**
1. LLM generates HTML using enhanced prompt
2. Remove markdown code fences if present
3. Validate HTML structure
4. Wrap in basic template if needed
5. Return HTML + metadata

**Metadata Returned:**
- Original query
- Enhanced query
- Analysis details (intent, focus, type, complexity)
- Best practices applied
- Data selection strategy used
- Paper count

---

## Key Improvements Over Old System

### Before (Single-Stage):
```python
prompt = f"Generate HTML for: {query}\nData: {json_dump}"
html = llm.complete(prompt)
return html
```

**Problems:**
- ❌ No query understanding
- ❌ Generic, not query-specific
- ❌ Dumps all data (50k char limit)
- ❌ No best practices
- ❌ No data intelligence

### After (Multi-Stage):
```python
analysis = analyze_query(query)
best_practices = generate_best_practices(analysis)
enhanced_query = enhance_query(query, analysis, best_practices)
strategy = create_data_selection_strategy(analysis)
filtered_data = filter_and_prepare_data(all_data, strategy)
prompt = build_enhanced_prompt(enhanced_query, filtered_data, analysis)
html = llm.complete(prompt)
return html, metadata
```

**Benefits:**
- ✅ Deep query understanding
- ✅ Query-specific best practices
- ✅ Smart data selection (no arbitrary limits)
- ✅ Context-aware prompting
- ✅ Transparent metadata
- ✅ Fallback mechanisms at each stage

---

## Usage Example

```python
from visualization_engine import VisualizationEngine
from extractors import get_llm_client

# Initialize
llm = get_llm_client()
engine = VisualizationEngine(llm)

# Prepare paper data
paper_ids = ["paper_1", "paper_2", "paper_3"]
all_raw_data = load_all_paper_data(paper_ids)

# Generate visualization
html, metadata = engine.generate_visualization(
    paper_ids=paper_ids,
    query="Compare training procedures and show performance improvements",
    all_raw_data=all_raw_data
)

# Use results
print(f"Enhanced Query: {metadata['enhanced_query']}")
print(f"Focus Areas: {metadata['analysis']['focus_areas']}")
print(f"Extractors Used: {metadata['data_selection']['extractors_used']}")

# Save HTML
with open("output.html", "w") as f:
    f.write(html)
```

---

## API Integration

The `/api/visualize` endpoint now uses this engine:

```python
@app.post("/api/visualize")
async def generate_visualization(request: VisualizeRequest):
    # Load all extractor data for all papers
    all_data = load_all_paper_data(request.paper_ids)
    
    # Use enhanced engine
    llm = get_llm_client()
    engine = VisualizationEngine(llm)
    
    html, metadata = engine.generate_visualization(
        paper_ids=request.paper_ids,
        query=request.query,
        all_raw_data=all_data
    )
    
    return {
        "html": html,
        "metadata": metadata
    }
```

---

## Testing

Run the test script to see the pipeline in action:

```bash
cd paper-analyzer/backend
python test_visualization_engine.py
```

**Test Output:**
- Shows each stage's processing
- Displays query analysis results
- Lists generated best practices
- Shows enhanced query
- Details data selection strategy
- Saves HTML and metadata to `/tmp/`

---

## Configuration & Tuning

### Data Limits

Adjust limits in `create_data_selection_strategy()`:

```python
if analysis.paper_count > 5:
    max_items = {
        "contributions": 3,  # Fewer for many papers
        "experiments": 5,
        # ...
    }
```

### Best Practices

Add domain-specific practices in `_get_general_best_practices()`:

```python
if "architecture" in analysis.focus_areas:
    practices.extend([
        "Show layer-by-layer breakdown",
        "Include parameter counts",
        "Visualize network topology"
    ])
```

### Fallback Behavior

Each stage has intelligent fallbacks:
- Query analysis → keyword matching
- Best practices → template-based rules
- Query enhancement → structured templates

---

## Future Enhancements

1. **Quality Validation**: Add HTML validation and regeneration loop
2. **Template Library**: Pre-built component templates for common patterns
3. **Caching**: Cache analyses and strategies for similar queries
4. **A/B Testing**: Compare old vs new system outputs
5. **User Feedback**: Learn from user ratings of visualizations
6. **Dynamic Limits**: Adjust limits based on LLM context window
7. **Multi-Modal**: Support images/diagrams in visualizations
8. **Interactive Refinement**: Allow users to refine the analysis

---

## Performance Considerations

**Token Usage:**
- Old system: ~1,000-5,000 tokens per generation
- New system: ~3,000-10,000 tokens per generation (includes analysis stages)

**Latency:**
- Old system: 1 LLM call (~2-5s)
- New system: 3-4 LLM calls (~8-15s total)

**Trade-off:** Higher cost/latency for significantly better results

**Optimization Options:**
1. Use faster model for analysis stages (cheap + fast)
2. Use best model for final HTML generation (expensive + high quality)
3. Cache analyses for similar queries
4. Skip enhancement for simple queries (auto-detect)

---

## Troubleshooting

### Issue: LLM returns invalid JSON in analysis
**Solution:** Falls back to keyword-based analysis automatically

### Issue: Too much data even after filtering
**Solution:** Adjust limits in `DataSelectionStrategy` or truncate JSON string

### Issue: Enhanced query too specific/restrictive
**Solution:** Adjust enhancement prompt to be more flexible

### Issue: Generated HTML missing data
**Solution:** Check data selection strategy - may be filtering too aggressively

### Issue: Slow generation time
**Solution:** Use faster model for stages 1-3, reserve best model for stage 7

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      User Request                                │
│              "Compare training across papers"                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  Load All Data  │ (All extractors, all papers)
                    └────────┬────────┘
                             │
         ┌───────────────────┴───────────────────┐
         │      VisualizationEngine              │
         │                                       │
         │  ┌─────────────────────────────────┐ │
         │  │ Stage 1: Query Analysis         │ │ → QueryAnalysis
         │  └──────────────┬──────────────────┘ │
         │                 │                     │
         │  ┌──────────────▼──────────────────┐ │
         │  │ Stage 2: Best Practices Gen     │ │ → List[str]
         │  └──────────────┬──────────────────┘ │
         │                 │                     │
         │  ┌──────────────▼──────────────────┐ │
         │  │ Stage 3: Query Enhancement      │ │ → EnhancedQuery
         │  └──────────────┬──────────────────┘ │
         │                 │                     │
         │  ┌──────────────▼──────────────────┐ │
         │  │ Stage 4: Data Selection         │ │ → DataSelectionStrategy
         │  └──────────────┬──────────────────┘ │
         │                 │                     │
         │  ┌──────────────▼──────────────────┐ │
         │  │ Stage 5: Data Filtering         │ │ → Filtered Data Dict
         │  └──────────────┬──────────────────┘ │
         │                 │                     │
         │  ┌──────────────▼──────────────────┐ │
         │  │ Stage 6: Prompt Building        │ │ → Enhanced Prompt
         │  └──────────────┬──────────────────┘ │
         │                 │                     │
         │  ┌──────────────▼──────────────────┐ │
         │  │ Stage 7: HTML Generation        │ │ → HTML + Metadata
         │  └─────────────────────────────────┘ │
         │                                       │
         └───────────────────┬───────────────────┘
                             │
                    ┌────────▼────────┐
                    │  Return Results │
                    └─────────────────┘
```

---

## Summary

The Enhanced Visualization Engine transforms simple queries into optimized visualizations through intelligent analysis, enhancement, and data selection. It's smarter about what to include, how to present it, and how to guide the LLM to produce high-quality results.

**Key Philosophy:** Don't just dump data and hope for the best. Understand, enhance, select, then generate.
