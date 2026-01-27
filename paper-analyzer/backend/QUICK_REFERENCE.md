# Enhanced Visualization Engine - Quick Reference

## 🚀 Quick Start

```python
from visualization_engine import VisualizationEngine
from extractors import get_llm_client

# Initialize
llm = get_llm_client()
engine = VisualizationEngine(llm)

# Generate visualization
html, metadata = engine.generate_visualization(
    paper_ids=["paper_1", "paper_2"],
    query="Compare contributions",
    all_raw_data=your_paper_data
)
```

## 📊 Data Format Expected

```python
all_raw_data = {
    "paper_id_1": {
        "paper": {
            "title": str,
            "authors": List[str],
            "abstract": str
        },
        "contributions": List[dict],
        "experiments": List[dict],
        "architectures": List[dict],
        # ... any extractor data
    }
}
```

## 🎯 Query Analysis Intent Types

| Intent | Example Queries | Visualization Type |
|--------|----------------|-------------------|
| `compare` | "Compare X across papers", "Differences between..." | Table |
| `summarize` | "Show all X", "List of..." | Cards/Grid |
| `timeline` | "Evolution of X", "Over time..." | Timeline |
| `cluster` | "Group by X", "Categorize..." | Grouped Cards |
| `explore` | "Analyze X", "Understand..." | Mixed Layout |
| `filter` | "Papers with X", "Only Y..." | Filtered List |
| `detail` | "Deep dive into X", "Explain..." | Detailed View |

## 🎨 Design System

```python
COLORS = {
    "background": "#0a0e27",      # Dark blue-black
    "card": "#16213e",            # Navy blue
    "accent": "#e94560",          # Coral red
    "secondary": "#0f3460",       # Deep blue
    "text": "#eee",               # Light gray
    "muted": "#a8a8a8"           # Muted gray
}

CONTRIBUTION_COLORS = {
    "architecture": "#4A9FF5",    # Blue
    "training": "#48BB78",        # Green
    "data": "#F97316",            # Orange
    "loss_function": "#e94560"    # Coral
}
```

## 📋 Data Selection Limits

### Single Paper (1)
All extractors: No limits (show everything)

### Few Papers (2-3)
```python
contributions: 10
experiments: 15
architectures: 5
hyperparameters: 5
baselines: 15
datasets: 10
```

### Many Papers (4+)
```python
contributions: 5
experiments: 8
architectures: 3
hyperparameters: 3
baselines: 10
datasets: 8
```

## 🔗 Smart Extractor Relationships

```python
"experiments" → auto-includes ["baselines", "datasets", "metrics"]
"architectures" → auto-includes ["hyperparameters"]
"training" → auto-includes ["hyperparameters", "metrics"]
```

## 🛠️ Customization Points

### 1. Adjust Data Limits
Edit `create_data_selection_strategy()` in `visualization_engine.py`:
```python
max_items = {
    "contributions": 10,  # Change this
    "experiments": 15,    # And this
    # ...
}
```

### 2. Add Best Practices
Edit `_get_general_best_practices()`:
```python
if "your_extractor" in analysis.focus_areas:
    practices.extend([
        "Your specific practice here"
    ])
```

### 3. Modify Color Scheme
Edit `build_enhanced_visualization_prompt()`:
```python
<design_system>
Colors:
  - Background: #your-color
  - Accent: #your-accent
</design_system>
```

### 4. Add Intent Detection
Edit `_fallback_query_analysis()`:
```python
if any(w in query_lower for w in ["your", "keywords"]):
    intent = "your_intent"
```

## 📦 Metadata Structure

```python
metadata = {
    "original_query": str,
    "enhanced_query": str,
    "analysis": {
        "intent": str,
        "focus_areas": List[str],
        "visualization_type": str,
        "complexity": str
    },
    "best_practices_applied": List[str],
    "data_selection": {
        "extractors_used": List[str],
        "priority_order": List[str]
    },
    "paper_count": int
}
```

## ⚡ Performance Tips

1. **Use fast model for stages 1-3** (analysis, practices, enhancement)
2. **Use best model for stage 7** (HTML generation)
3. **Cache query analyses** for similar queries
4. **Skip enhancement for simple queries** (add auto-detect)

## 🐛 Common Issues

### Issue: "Too much data, LLM times out"
**Fix:** Reduce limits in `max_items_per_extractor`

### Issue: "HTML missing some papers"
**Fix:** Check data selection strategy - may be filtering too aggressively

### Issue: "Query analysis returns weird intent"
**Fix:** Falls back to keyword matching, check `_fallback_query_analysis()`

### Issue: "Generated HTML is generic"
**Fix:** Check that best practices and enhanced query are being used in prompt

## 🧪 Testing

```bash
# Run test suite
cd paper-analyzer/backend
python test_visualization_engine.py

# Check specific stage
python -c "
from visualization_engine import VisualizationEngine
from test_visualization_engine import MockLLM

llm = MockLLM()
engine = VisualizationEngine(llm)
analysis = engine.analyze_query('Your query', 3)
print(analysis)
"
```

## 📝 Examples

### Example 1: Simple Query
```python
query = "Show contributions"
# → Intent: summarize
# → Focus: [contributions]
# → Type: cards
```

### Example 2: Comparison Query
```python
query = "Compare training methods across papers"
# → Intent: compare
# → Focus: [training, hyperparameters, metrics]
# → Type: table
```

### Example 3: Timeline Query
```python
query = "Evolution of architectures over time"
# → Intent: timeline
# → Focus: [architectures]
# → Type: timeline
```

## 🔍 Debugging

### Print Analysis
```python
analysis = engine.analyze_query(query, paper_count)
print(f"Intent: {analysis.intent}")
print(f"Focus: {analysis.focus_areas}")
```

### Print Strategy
```python
strategy = engine.create_data_selection_strategy(analysis)
print(f"Extractors: {strategy.extractors}")
print(f"Limits: {strategy.max_items_per_extractor}")
```

### Save Prompt
```python
prompt = engine.build_enhanced_visualization_prompt(enhanced_query, data, analysis)
with open('/tmp/debug_prompt.txt', 'w') as f:
    f.write(prompt)
```

## 📚 Related Files

- `visualization_engine.py` - Main engine implementation
- `VISUALIZATION_ENGINE.md` - Detailed documentation
- `BEFORE_AFTER_COMPARISON.md` - Examples of improvements
- `test_visualization_engine.py` - Test suite
- `api/app.py` - API integration

## 🎯 Key Takeaways

1. **Multi-stage is better** - Each stage builds on the previous
2. **Smart data selection** - Only include what's needed
3. **Query-specific practices** - Not one-size-fits-all
4. **Transparent metadata** - Know what happened
5. **Graceful fallbacks** - Always have a plan B

## 💡 Pro Tips

- The more specific the query, the better the results
- For complex queries, break into multiple visualizations
- Use metadata to understand what was filtered
- Test with different paper counts to see limit behavior
- Cache analyses for repeated queries

## 🚦 Decision Tree

```
Query received
    ↓
Is it simple? (single extractor, few papers)
    Yes → Skip enhancement, use basic analysis
    No → Full pipeline
        ↓
    More than 5 papers?
        Yes → Aggressive filtering
        No → Generous limits
            ↓
        Comparison intent?
            Yes → Table layout, side-by-side
            No → Cards/grid layout
```

---

**Questions?** Check `VISUALIZATION_ENGINE.md` for detailed explanations.

**Issues?** Review `BEFORE_AFTER_COMPARISON.md` for examples.

**Testing?** Run `test_visualization_engine.py`.
