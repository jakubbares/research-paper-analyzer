# 🚀 How to Get MASSIVE HTML Visualizations

## Quick Start

Your visualization HTML is now **4x longer** thanks to DeepSeek streaming!

### What Changed?

1. ✅ **DeepSeek Streaming** - Up to 16,384 tokens (was 4,096)
2. ✅ **Auto-Used** - Visualization engine uses it automatically
3. ✅ **No Config Needed** - Just use the app normally
4. ✅ **Progress Tracking** - See generation progress in terminal

---

## How to Use

### Option 1: Use the Web App (Recommended)

```bash
# 1. Start backend
cd paper-analyzer/backend
uvicorn api.app:app --reload

# 2. Start frontend (in new terminal)
cd paper-analyzer/frontend
npm run dev

# 3. Open browser
open http://localhost:3000
```

**In the app:**
1. Upload 2-5 papers
2. Enter a comprehensive query:
   ```
   Show me a comprehensive analysis comparing ALL contributions, 
   experiments, architectures, training methods, results, datasets, 
   baselines, and limitations. Include detailed tables, metrics, 
   and breakdowns for every paper. Make it information-dense with 
   lots of data and at least 3 screens of content.
   ```
3. Click "Generate Visualization"
4. **Watch the backend terminal** - you'll see streaming progress!
5. The massive HTML appears in the app (no separate window!)

### Option 2: Test Streaming Directly

```bash
cd paper-analyzer/backend
python test_streaming.py
```

Output:
```
================================================================================
  TESTING DEEPSEEK STREAMING
================================================================================
✅ LLM client supports streaming: DeepSeekClient

🚀 Testing streaming generation...
   Prompt: Generate a long HTML document with at least 10 sections...
  📦 Received 50 chunks, 1,234 chars so far...
  📦 Received 100 chunks, 2,891 chars so far...
  📦 Received 150 chunks, 4,567 chars so far...
  
✅ Streaming complete!
   Total chunks: 378
   Total characters: 12,567
   Estimated tokens: ~3,141
```

---

## What You'll See

### In the Backend Terminal:

```
🔧 Using DeepSeek LLM (provider=deepseek)
✅ DeepSeek client initialized!

Stage 1: Analyzing query...
Stage 2: Generating best practices...
Stage 3: Enhancing query...
Stage 4: Creating data selection strategy...
Stage 5: Filtering and preparing data...
Stage 6: Building enhanced visualization prompt...

🚀 Generating MASSIVE HTML using streaming...
  📦 Received 50 chunks, 1,456 chars so far...
  📦 Received 100 chunks, 3,123 chars so far...
  📦 Received 150 chunks, 4,789 chars so far...
  📦 Received 200 chunks, 6,456 chars so far...
  📦 Received 250 chunks, 8,123 chars so far...
  📦 Received 300 chunks, 9,789 chars so far...
  📦 Received 350 chunks, 11,456 chars so far...
  📦 Received 400 chunks, 13,123 chars so far...
✅ Streaming complete! Generated 14,567 characters (423 chunks)

Stage 7: Post-processing HTML...
✅ Visualization generation complete!
```

### In the Frontend:

You'll see a **MASSIVE** HTML visualization with:
- 🎯 10+ major sections
- 📊 Comprehensive tables with ALL data
- 📈 Detailed metrics and comparisons
- 🔍 Collapsible sections for deep dives
- 📝 Summary statistics
- 🗂️ Cross-paper insights
- **3-5+ screens of scrollable content!**

---

## Configuration

### Check Your Settings

**File:** `paper-analyzer/backend/.env`

```bash
# Make sure you're using DeepSeek
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-your-key-here
```

If `LLM_PROVIDER=bedrock`, you'll use Bedrock (also works, but no streaming - falls back to 8192 tokens).

### Max Tokens Settings

| Setting | Value | When Used |
|---------|-------|-----------|
| **Streaming** | 16,384 tokens | Default for HTML generation |
| **Fallback** | 8,192 tokens | If streaming fails |
| **JSON** | 4,096 tokens | Query analysis, best practices |

These are automatic - no config needed!

---

## Troubleshooting

### "Streaming not supported"

**Cause:** Using Bedrock instead of DeepSeek

**Fix:**
```bash
# In backend/.env
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-your-actual-key
```

Then restart backend:
```bash
uvicorn api.app:app --reload
```

### "HTML still seems short"

**Check:**
1. Is your query specific enough? (try the example query above)
2. Are you analyzing multiple papers? (more data = longer HTML)
3. Did you select data-rich papers? (papers with lots of experiments/results)

**Verify in terminal:**
- Look for: `✅ Streaming complete! Generated XXXXX characters`
- If < 5000 chars, the LLM might be cutting short
- If > 10000 chars, it's working perfectly!

### "DeepSeek API Error"

**Cause:** API key issue or quota exceeded

**Check:**
```bash
# Test your API key
curl https://api.deepseek.com/v1/models \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY"
```

**Fix:**
- Verify API key is correct in `.env`
- Check your DeepSeek account balance
- Ensure you have quota remaining

---

## How Long Can It Get?

### Token Limits:
- **DeepSeek Max:** 32,768 tokens total (input + output)
- **Our Prompt:** ~4,000-8,000 tokens (data + instructions)
- **Available for Output:** ~16,000-24,000 tokens
- **We Request:** 16,384 tokens (safe margin)

### Character Estimates:
- **1 token ≈ 4 characters** (English text)
- **16,384 tokens ≈ 65,536 characters**
- **Typical output:** 10,000-20,000 characters
- **That's:** 3-5 screens of dense content!

### Real Examples:

| Papers | Query Complexity | Output Length | Screens |
|--------|-----------------|---------------|---------|
| 1 paper | Simple | 3,000 chars | 1 screen |
| 3 papers | Medium | 8,000 chars | 2 screens |
| 5 papers | Comprehensive | 15,000 chars | 3-4 screens |
| 10 papers | Full analysis | 20,000+ chars | 5+ screens |

---

## Tips for MAXIMUM Length

### 1. Upload Multiple Papers
More papers = more data = longer HTML

### 2. Use Comprehensive Queries
Instead of:
```
Show contributions
```

Use:
```
Show me a comprehensive analysis comparing ALL contributions, 
experiments, architectures, training methods, results, datasets, 
baselines, limitations, and future work across ALL papers. 
Include detailed tables, metrics, percentages, and breakdowns. 
Make it information-dense with everything you can find.
```

### 3. Select Data-Rich Papers
Papers with:
- ✅ Many experiments (5+ experiments)
- ✅ Lots of baselines (10+ comparisons)
- ✅ Multiple datasets
- ✅ Detailed architectures
- ✅ Ablation studies

Generate longer visualizations than:
- ❌ Theoretical papers
- ❌ Survey papers
- ❌ Position papers

### 4. Ask for Details
Add to your query:
- "Include ALL data points"
- "Show specific numbers and percentages"
- "Add detailed breakdowns for each paper"
- "Create comprehensive comparison tables"
- "Don't summarize - show everything"

---

## Monitoring Progress

### Real-Time Monitoring:

**Terminal output tells you everything:**
```
📦 Received 50 chunks, 1,234 chars so far...
```

This means:
- ✅ Streaming is working
- ✅ HTML is being generated
- ✅ 1,234 characters received (growing!)

**If you see:**
- Many updates (50, 100, 150, ...) = MASSIVE HTML ✅
- Few updates (50, then done) = Short HTML ❌

### Post-Generation Check:

```
✅ Streaming complete! Generated 14,567 characters (423 chunks)
```

**Good outputs:**
- 10,000+ characters = Excellent! 🎉
- 5,000-10,000 = Good ✅
- < 5,000 = Short (try a more comprehensive query)

---

## Summary

✅ **Streaming is automatically enabled** for DeepSeek  
✅ **16,384 tokens max** (4x the default)  
✅ **Progress tracking** in terminal  
✅ **No configuration needed** - just use the app!  
✅ **Fallback to 8192 tokens** if streaming fails  
✅ **Works in the app** - HTML renders directly on page  

**Result:** MASSIVE, information-dense visualizations with ALL your data! 🚀

---

## Quick Reference

| Task | Command |
|------|---------|
| **Start App** | `uvicorn api.app:app --reload` (backend)<br>`npm run dev` (frontend) |
| **Test Streaming** | `python test_streaming.py` |
| **Check Config** | `cat backend/.env \| grep LLM` |
| **View Logs** | Watch backend terminal during generation |
| **Verify Length** | Look for "Generated XXXXX characters" |

**Need help?** Check `STREAMING_IMPLEMENTATION.md` for technical details!
