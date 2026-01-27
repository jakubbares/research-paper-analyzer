# Before & After: Visualization Prompt Comparison

This document shows concrete examples of how the Enhanced Visualization Engine improves prompts and data handling.

---

## Example 1: "Show me all contributions"

### ❌ OLD SYSTEM

**Query Processing:**
- No analysis
- No enhancement
- Just passes through as-is

**Data Handling:**
```python
# Loads ALL extractors for ALL papers
all_data[paper_id] = {
    "contributions": [...],  # All contributions
    "experiments": [...],     # All experiments (not needed!)
    "architectures": [...],   # All architectures (not needed!)
    "hyperparameters": [...], # All hyperparameters (not needed!)
    # ... 9+ extractors loaded unnecessarily
}

# Dumps everything, truncates at 50k chars
data_json = json.dumps(all_data)[:50000]
```

**Prompt:**
```
You are a data visualization expert. Generate an HTML page that visualizes 
the following research paper data according to the user's query.

USER QUERY: Show me all contributions

DATA (from 3 papers):
{
  "paper_1": {
    "contributions": [...],
    "experiments": [...],
    "architectures": [...],
    // ... lots of irrelevant data ...
  },
  "paper_2": { ... },
  "paper_3": { ... }
}

REQUIREMENTS:
- Output ONLY valid HTML
- Include inline CSS
- Make it visually clean
- Use dark theme
- Include interactive elements
- Self-contained

OUTPUT THE HTML NOW:
```

**Issues:**
1. 🚫 Query is unchanged - no specifics added
2. 🚫 Includes irrelevant data (experiments, architectures, etc.)
3. 🚫 Generic requirements - not query-specific
4. 🚫 No guidance on how to organize contributions
5. 🚫 May hit 50k limit with many papers

---

### ✅ NEW SYSTEM

**Query Analysis:**
```json
{
  "intent": "summarize",
  "focus_areas": ["contributions"],
  "visualization_type": "cards",
  "complexity": "simple",
  "requires_cross_paper_analysis": true
}
```

**Best Practices Generated:**
1. Group contributions by type (architecture, training, data, loss function)
2. Use a card-based grid layout for easy scanning
3. Color-code contribution types with consistent badges
4. Show paper title prominently on each card
5. Include evidence locations as clickable links
6. Add a summary header showing contribution type distribution

**Enhanced Query:**
```
Create a comprehensive grid of contribution cards showing all contributions 
across papers. Organize contributions by type using color-coded badges 
(architecture: blue, training: green, data: orange, loss function: red). 
Each card should display the paper title, specific innovation, problem 
addressed, and evidence location. Include a summary section at the top 
showing the distribution of contribution types across all papers.
```

**Data Selection:**
```python
# Only loads contributions + paper metadata
strategy = {
    "extractors": ["contributions"],
    "max_items_per_extractor": {"contributions": 999},  # No limit for single extractor
    "include_cross_references": True
}

filtered_data = {
    "paper_1": {
        "paper": {...},
        "contributions": [...]  # ONLY contributions
    },
    "_cross_paper_insights": {
        "contribution_distribution": {
            "architecture": 5,
            "training": 3,
            "data": 2,
            "loss_function": 1
        }
    }
}
```

**Enhanced Prompt:**
```xml
<role>Senior data visualization designer specializing in research papers</role>

<task>Generate complete HTML visualization of research paper data</task>

<original_user_query>Show me all contributions</original_user_query>

<enhanced_visualization_requirements>
Create a comprehensive grid of contribution cards showing all contributions 
across papers. Organize contributions by type using color-coded badges 
(architecture: blue, training: green, data: orange, loss function: red). 
Each card should display the paper title, specific innovation, problem 
addressed, and evidence location. Include a summary section at the top 
showing the distribution of contribution types across all papers.
</enhanced_visualization_requirements>

<query_analysis>
- Intent: summarize
- Focus: contributions
- Visualization type: cards
- Complexity: simple
</query_analysis>

<best_practices>
1. Group contributions by type (architecture, training, data, loss function)
2. Use a card-based grid layout for easy scanning
3. Color-code contribution types with consistent badges
4. Show paper title prominently on each card
5. Include evidence locations as clickable links
6. Add a summary header showing contribution type distribution
</best_practices>

<data>
{
  "paper_1": {
    "paper": {"title": "...", "authors": [...]},
    "contributions": [...]
  },
  "_cross_paper_insights": {
    "contribution_distribution": {
      "architecture": 5,
      "training": 3,
      "data": 2
    }
  }
}
</data>

<design_system>
Colors:
  - Architecture badge: #4A9FF5 (blue)
  - Training badge: #48BB78 (green)
  - Data badge: #F97316 (orange)
  - Loss function badge: #e94560 (coral)
  
Layout:
  - CSS Grid with 3 columns on desktop
  - Card spacing: 1.5rem gap
  - Max width: 1400px
</design_system>

<mandatory_constraints>
❌ NEVER use external CDNs
✓ ALWAYS group by contribution type
✓ ALWAYS show distribution summary first
✓ ALWAYS use color-coded badges
</mandatory_constraints>

<output_instruction>
Generate complete HTML following the enhanced requirements and best practices
</output_instruction>
```

**Improvements:**
1. ✅ Specific layout guidance (grid with 3 columns)
2. ✅ Only relevant data (contributions only)
3. ✅ Query-specific best practices
4. ✅ Detailed color scheme for contribution types
5. ✅ Cross-paper insights included
6. ✅ No risk of hitting limits (only needed data)

---

## Example 2: "Compare training procedures"

### ❌ OLD SYSTEM

**Data:**
```python
# Loads everything, including irrelevant extractors
all_data[paper_id] = {
    "contributions": [...],  # Not needed for comparison
    "experiments": [...],    # Somewhat relevant
    "architectures": [...],  # Not needed
    "training": [...],       # NEEDED
    "hyperparameters": [...], # Related, but not loaded!
    # Missing: metrics, which are needed for comparison!
}
```

**Prompt:**
```
USER QUERY: Compare training procedures

DATA: {... all 9 extractors dumped ...}

REQUIREMENTS:
- Make it clean
- Use dark theme
- Self-contained
```

**Issues:**
1. 🚫 Includes contributions (not relevant)
2. 🚫 Includes architectures (not relevant)
3. 🚫 Missing hyperparameters (needed for comparison!)
4. 🚫 Missing metrics (needed to show results!)
5. 🚫 No guidance on comparison format

---

### ✅ NEW SYSTEM

**Query Analysis:**
```json
{
  "intent": "compare",
  "focus_areas": ["training"],
  "visualization_type": "table",
  "complexity": "medium",
  "requires_cross_paper_analysis": true
}
```

**Smart Data Selection:**
```python
# Automatically includes related extractors!
strategy = {
    "extractors": [
        "training",         # Primary focus
        "hyperparameters",  # Auto-added (related to training)
        "metrics"          # Auto-added (shows results)
    ]
}
```

**Best Practices:**
```
1. Use a side-by-side comparison table with papers as columns
2. Align training attributes in rows for easy comparison
3. Highlight differences with color coding
4. Include hyperparameters inline with training procedures
5. Show convergence metrics for each approach
6. Use sticky headers for scrollable tables
```

**Enhanced Query:**
```
Create a detailed comparison table showing training procedures across all papers. 
Use papers as columns and training attributes as rows (optimizer, learning rate, 
batch size, epochs, etc.). Highlight significant differences with color coding 
(red for unusual choices, green for best practices). Include a summary row at 
the top showing which paper achieved fastest convergence. Make headers sticky 
for easy scrolling.
```

**Result:** Far more actionable, includes all relevant data, clear structure.

---

## Example 3: "Show experiments from 10 papers"

### ❌ OLD SYSTEM

**Data Handling:**
```python
# Tries to load ALL experiments from ALL 10 papers
all_data = {}
for paper_id in paper_ids:  # 10 papers
    all_data[paper_id] = {
        "experiments": [...],  # Could be 15+ per paper = 150 experiments
        "baselines": [...],    # 20+ per paper = 200 baselines
        "datasets": [...],
        # ... etc
    }

# Dumps to JSON
data_json = json.dumps(all_data)  # Easily exceeds 50k chars
# Truncates: data_json = data_json[:50000] + "... [truncated]"
```

**Problem:** Data gets truncated mid-JSON, breaking structure. Some papers completely missing.

---

### ✅ NEW SYSTEM

**Data Selection:**
```python
# Recognizes 10 papers = many, so be selective
strategy = {
    "extractors": ["experiments", "baselines", "datasets", "metrics"],
    "max_items_per_extractor": {
        "experiments": 5,   # Top 5 per paper = 50 total
        "baselines": 10,    # Top 10 per paper
        "datasets": 8,      # Top 8 per paper
        "metrics": 10       # Top 10 per paper
    }
}

# Result: Well within limits, no truncation
```

**Filtered Data:**
```python
filtered_data = {
    "paper_1": {
        "experiments": [...5 items...],
        "_metadata": {
            "note": "Showing 5 of 15 total experiments"
        }
    },
    # All 10 papers included properly
}
```

**Benefit:** 
- ✅ All 10 papers represented
- ✅ No truncation
- ✅ Quality over quantity
- ✅ User knows what's hidden

---

## Token Usage Comparison

### Old System:
```
Prompt: ~800 tokens
Data: ~4,000 tokens (often truncated)
Total: ~4,800 tokens per request
```

### New System:
```
Stage 1 (Analysis): ~500 tokens
Stage 2 (Best Practices): ~800 tokens
Stage 3 (Enhancement): ~1,000 tokens
Stage 6 (Generation): ~3,000 tokens (filtered data) + ~1,500 tokens (prompt)
Total: ~6,800 tokens per request
```

**Cost Difference:** ~40% more tokens, but FAR better results

---

## Quality Improvements Summary

| Aspect | Old System | New System |
|--------|-----------|------------|
| **Query Understanding** | None | Deep analysis with fallbacks |
| **Data Relevance** | All or nothing | Smart selection based on query |
| **Data Amount** | Arbitrary 50k limit | Context-aware limits per paper count |
| **Best Practices** | Generic list | Query-specific, generated per request |
| **Prompt Specificity** | Vague | Detailed with examples and constraints |
| **Layout Guidance** | "Make it clean" | Specific grid/table/card specs |
| **Color Schemes** | "Dark theme" | Exact hex codes per element |
| **Cross-Paper Insights** | None | Common datasets, distributions, patterns |
| **Metadata** | None | Full transparency on selections |
| **Fallback Handling** | Fails on LLM error | Graceful fallbacks at each stage |

---

## Real-World Impact

### Scenario: User with 5 papers asks "What datasets are used?"

**Old System:**
- Loads all 9 extractors × 5 papers
- Dumps 40,000 chars of JSON
- Generic prompt: "show datasets"
- LLM gets overwhelmed with irrelevant data
- Result: ⭐⭐ Generic list

**New System:**
- Analyzes: intent=summarize, focus=datasets
- Generates practices: "Group by frequency", "Show which papers use each"
- Enhances: "Create frequency table with paper names"
- Loads ONLY datasets (+ paper metadata)
- Smart prompt with table structure
- Result: ⭐⭐⭐⭐⭐ Beautiful frequency table with cross-references

---

## Conclusion

The Enhanced Visualization Engine doesn't just generate HTML—it understands, plans, selects, and optimizes before generating. This results in:

1. **Better data efficiency** - Only include what's needed
2. **Better prompts** - Specific, actionable, context-aware
3. **Better results** - Query-specific best practices applied
4. **Better scalability** - Smart limits based on paper count
5. **Better transparency** - Metadata shows what happened

**Philosophy:** Garbage in → Garbage out. By enhancing the input (query + data + prompt), we dramatically improve the output.
