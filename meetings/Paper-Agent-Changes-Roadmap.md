# Paper Analyzer Agent — Planned Changes

**Document Created:** 21st January, 2026  
**Based on Meeting:** 19th January, 2026 (Jakub Bares & Jan Hůla)

---

## Overview

This document outlines the architectural and feature changes planned for the Paper Analyzer agent. The core vision is to transform the agent from a static extraction tool into a **dynamic, query-driven research assistant** that generates custom visualizations on-the-fly.

---

## 1. Dynamic UI Generation

### Current State
- Fixed set of extractors with predefined output formats
- Static visualization components

### Planned Changes
- **Query-Driven Visualization**: User provides a natural language query (e.g., "Show me all contributions related to training algorithms across these papers")
- **On-the-fly HTML Generation**: System generates custom HTML/JavaScript visualizations tailored to the specific query
- **Canvas-Based Dashboard**: Main app remains as-is, but includes a canvas/container where dynamically generated visualizations are rendered

### Implementation Notes
- Output will be static HTML with embedded JavaScript (not React components)
- Visualization templates should include constraint instructions (things to avoid, patterns to follow)
- Start simple — a single `<div>` container for the generated visualization

---

## 2. Combined/Smart Extractor System

### Current Extractors
- Contributions
- Experiments  
- Architectures
- Hyperparameters
- Ablations
- Baselines
- Algorithms
- Limitations
- Future Work
- Equations
- Training
- Metrics
- Datasets
- Claims
- Related Work
- Loss Functions
- Code Resources

### Planned Changes

#### a) Intent-Based Extractor Selection
- User describes their **intent** in natural language (e.g., "I want to write a new paper about GNN architectures and need to understand current approaches")
- System determines which extractors are relevant
- Only relevant extractors run, merged into a single extraction pass

#### b) Merged Extractor Execution
- Combine multiple extractor prompts into a single LLM call
- Reduces processing time from sequential to parallel
- All extracted data fits in context/response

#### c) Extractor Metadata
- Define precisely what each extractor can extract
- Document available attributes per extractor
- Allow the system to reason about which extractors to use

---

## 3. Multi-Paper Analysis

### Current State
- Papers analyzed individually
- No cross-paper comparison

### Planned Changes

#### a) Batch Processing
- Upload and process multiple papers simultaneously
- Run extractors in parallel across papers

#### b) Comparative Dashboards
- Side-by-side comparison of extracted attributes
- **Table View**: Papers as columns, attributes as rows (scrollable grid)
- Identify patterns across papers

#### c) Contribution Clustering
- Group contributions by category:
  - Architecture contributions
  - Training/learning algorithm contributions
  - Data-related contributions
  - Loss function contributions
- Enable filtering by contribution type

---

## 4. Smart Prioritization & Filtering

### Problem
- Loading 20 papers creates information overload
- Not everything is relevant to the user's task

### Solution
- **Context-Aware Filtering**: Based on user's stated task/goal, prioritize relevant papers and sections
- **Replication Guidance**: When task is "replicate experiments," system recommends:
  - Which baselines to replicate
  - Which benchmarks are essential
  - What can be skipped
- **Relevance Scoring**: Rank extracted information by relevance to the query

---

## 5. New Views & Components

### Table/Matrix View
- Large dashboard with horizontal scrolling
- Papers on one axis, attributes on the other
- Quick overview of all extracted data

### Clustered Contributions View
- Group by contribution type
- Show which papers contain each type
- Click-through to paper details

### Experiment Drilldown
- Select a paper → see all experiments
- For each experiment: benchmarks, baselines, metrics, results
- Main experiments vs. ablation studies separation

---

## 6. Technical Implementation — How Dynamic UI Works

### The Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     EXISTING NEXT.JS APP                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Header / Navigation / Tabs (stays the same)              │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  NEW: "Dynamic View" Tab                                   │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │  Query Input (natural language)                      │  │ │
│  │  │  "Show me all contributions about training..."       │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │  CANVAS / IFRAME                                     │  │ │
│  │  │                                                      │  │ │
│  │  │   ← LLM-generated HTML is rendered here →            │  │ │
│  │  │                                                      │  │ │
│  │  │   The backend returns raw HTML + JS                  │  │ │
│  │  │   This container displays it via:                    │  │ │
│  │  │   - dangerouslySetInnerHTML (simple)                 │  │ │
│  │  │   - iframe with srcdoc (sandboxed, safer)            │  │ │
│  │  │                                                      │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
1. User Types Query
   ↓
2. Frontend sends: POST /api/visualize
   {
     "paper_ids": ["uuid1", "uuid2", ...],
     "query": "Show all contributions related to training"
   }
   ↓
3. Backend (Python):
   a) Determines which extractors are needed based on query
   b) Runs extractions (parallel, uses cache if available)
   c) Combines extracted data into context
   d) Calls LLM with prompt:
      "Given this data: {...}
       And this query: '...'
       Generate an HTML visualization.
       Follow these rules: [constraints]"
   e) Returns: { "html": "<div>...</div><script>...</script>" }
   ↓
4. Frontend renders HTML in the canvas container
```

### Frontend Component: `DynamicViewer.tsx`

```tsx
// New component to add to frontend/components/

'use client';
import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';

interface DynamicViewerProps {
  paperIds: string[];
}

export function DynamicViewer({ paperIds }: DynamicViewerProps) {
  const [query, setQuery] = useState('');
  const [generatedHtml, setGeneratedHtml] = useState<string | null>(null);

  const generateMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch('/api/visualize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ paper_ids: paperIds, query })
      });
      return res.json();
    },
    onSuccess: (data) => setGeneratedHtml(data.html)
  });

  return (
    <div className="space-y-4">
      {/* Query Input */}
      <div className="flex gap-2">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="What do you want to see? e.g., 'Show all training contributions'"
          className="flex-1 border rounded px-4 py-2"
        />
        <button 
          onClick={() => generateMutation.mutate()}
          disabled={generateMutation.isPending}
          className="bg-blue-600 text-white px-6 py-2 rounded"
        >
          {generateMutation.isPending ? 'Generating...' : 'Generate View'}
        </button>
      </div>

      {/* Canvas: Render Generated HTML */}
      {generatedHtml && (
        <div className="border rounded-lg bg-white min-h-[600px]">
          {/* Option A: Direct injection (simpler, less safe) */}
          <div dangerouslySetInnerHTML={{ __html: generatedHtml }} />
          
          {/* Option B: Sandboxed iframe (safer for untrusted HTML) */}
          {/* 
          <iframe 
            srcDoc={generatedHtml}
            className="w-full h-[800px] border-0"
            sandbox="allow-scripts"
          />
          */}
        </div>
      )}
    </div>
  );
}
```

### Backend Endpoint: `/api/visualize`

```python
# Add to backend/api/app.py

class VisualizeRequest(BaseModel):
    paper_ids: List[str]
    query: str
    extractors: Optional[List[str]] = None  # Auto-detect if not provided

@app.post("/api/visualize")
async def generate_visualization(request: VisualizeRequest) -> Dict[str, Any]:
    """
    Generate dynamic HTML visualization based on query
    """
    # 1. Collect extracted data from all papers
    all_data = {}
    for paper_id in request.paper_ids:
        paper_data = load_parsed_paper(paper_id)
        if not paper_data:
            continue
            
        all_data[paper_id] = {
            "paper": paper_data,
            "contributions": load_contributions(paper_id) or [],
            "experiments": load_experiments(paper_id) or [],
            # ... load other extractors as needed
        }
    
    # 2. Generate HTML via LLM
    llm = get_llm_client()
    
    prompt = f"""You are a data visualization expert. Generate an HTML page 
that visualizes the following research paper data according to the user's query.

USER QUERY: {request.query}

DATA:
{json.dumps(all_data, indent=2, default=str)[:50000]}

REQUIREMENTS:
- Output ONLY valid HTML (no markdown, no explanation)
- Include inline CSS in a <style> tag
- Include inline JavaScript in a <script> tag if needed
- Make it visually clean and professional
- Use a modern, minimal design
- Include interactive elements where useful (collapsible sections, hover effects)
- The HTML should be self-contained and work in isolation

OUTPUT:"""

    html = llm.complete(prompt)
    
    # Clean up response (remove markdown code fences if present)
    html = html.strip()
    if html.startswith("```html"):
        html = html[7:]
    if html.startswith("```"):
        html = html[3:]
    if html.endswith("```"):
        html = html[:-3]
    
    return {
        "html": html.strip(),
        "paper_count": len(request.paper_ids),
        "query": request.query
    }
```

### Key Considerations

1. **No React Generation** — We don't ask the LLM to write React components. That's complex, error-prone, and requires build steps. Instead, we generate plain HTML + vanilla JS.

2. **Iframe for Safety** — If you're worried about XSS or broken HTML crashing the app, use an iframe with `sandbox="allow-scripts"`. This isolates the generated content.

3. **Constraints Prompt** — Include rules in the prompt like:
   - "Never use external CDN links"
   - "Always include responsive styles"
   - "Maximum 3 colors in the design"
   - "Use table-based layouts for comparisons"

4. **Caching** — Consider caching generated visualizations by hashing (paper_ids + query). Same query = same result.

5. **Fallback** — If generation fails or output is invalid, show a basic JSON view of the data.

---

## 7. Priority Order

1. **Dynamic HTML Generation** — Core feature, enables everything else
2. **Combined Extractor Execution** — Performance optimization
3. **Multi-Paper Comparative View** — High-value feature
4. **Intent-Based Extractor Selection** — UX improvement
5. **Contribution Clustering** — Analysis feature
6. **Smart Prioritization** — Advanced feature

---

## 8. Related Work / Inspiration

- **Prompt End** (startup): Generates metadata that populates pre-built components, enables data editing in context
- **Jan's Prototype**: Demonstrated query → clustered contributions → auto-generated HTML views

---

## 9. Open Questions

- [ ] Should equations be a standalone extractor? (Possibly low value on its own)
- [ ] How to handle very long papers that don't fit in context?
- [ ] Cache extraction results for re-use in different visualizations?
- [ ] Version control for generated visualizations?

---

## Next Steps

1. Create custom extractor that combines multiple existing extractors
2. Implement basic HTML generation canvas in the frontend
3. Build the prompt pipeline: intent → extractor selection → merged extraction → HTML generation
4. Test with multi-paper workflows

---

*This document will be updated as implementation progresses.*

