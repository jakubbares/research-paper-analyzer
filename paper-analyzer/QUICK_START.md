# 🚀 Quick Start Guide

This guide will get you up and running with the Research Paper Analyzer in **5 minutes**.

---

## ⚡ Prerequisites Check

Before starting, ensure you have:

- [ ] **Python 3.10+** installed (`python3 --version`)
- [ ] **Node.js 18+** installed (`node --version`)
- [ ] **AWS Account** with Bedrock access
- [ ] **AWS Access Keys** ready

---

## 🎯 Step-by-Step Setup

### Step 1: Run Setup Script

```bash
cd /Users/jakubbares/Science/New/paper-analyzer
./setup.sh
```

This will:
- Create Python virtual environment
- Install all Python dependencies
- Install all Node.js dependencies
- Create data directories
- Copy .env template

**Time:** ~2-3 minutes

---

### Step 2: Configure AWS Credentials

Edit the backend `.env` file with your AWS credentials:

```bash
nano backend/.env
```

Update these lines:
```bash
AWS_ACCESS_KEY_ID=your_actual_access_key_here
AWS_SECRET_ACCESS_KEY=your_actual_secret_key_here
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=deepseek-ai.deepseek-v3
```

**Important:** Make sure you have:
1. Enabled AWS Bedrock in your AWS account
2. Requested access to DeepSeek models
3. Created IAM user with Bedrock permissions

---

### Step 3: Start Backend Server

Open **Terminal 1**:

```bash
cd /Users/jakubbares/Science/New/paper-analyzer
./start-backend.sh
```

You should see:
```
✅ Starting FastAPI server on http://localhost:8000
📖 API docs will be available at http://localhost:8000/docs
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal running!**

---

### Step 4: Start Frontend Server

Open **Terminal 2**:

```bash
cd /Users/jakubbares/Science/New/paper-analyzer
./start-frontend.sh
```

You should see:
```
✅ Starting Next.js dev server on http://localhost:3000
- Local:        http://localhost:3000
```

**Keep this terminal running!**

---

### Step 5: Open in Browser

Open your browser and navigate to:

```
http://localhost:3000
```

You should see the **Research Paper Analyzer** interface! 🎉

---

## 📖 First Analysis

### 1. Upload a Paper

- Click on the **"Upload"** tab (default)
- Drag and drop a PDF research paper OR click "Select PDF File"
- Click **"Upload and Analyze"**
- Wait ~3 seconds for parsing

### 2. View Paper Info

- Automatically switches to **"Paper Info"** tab
- See the paper's title, authors, abstract
- Paper is now ready for AI analysis

### 3. Extract Contributions

- Click **"Extract Contributions"** button
- Wait ~30-60 seconds (AI is analyzing)
- View categorized contributions in beautiful cards
- Results are cached for instant future access

### 4. Extract Experiments

- Click **"Extract Experiments"** button
- Wait ~30-60 seconds (AI is analyzing)
- View datasets, baselines, results, hyperparameters
- Results are cached

---

## 🧪 Testing the API

### Test Health Endpoint

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "llm": "AWS Bedrock - deepseek-ai.deepseek-v3"
}
```

### Test Paper Upload

```bash
curl -X POST http://localhost:8000/api/papers \
  -F "file=@/path/to/your/paper.pdf"
```

### View API Documentation

Open in browser:
```
http://localhost:8000/docs
```

Interactive Swagger UI with all endpoints!

---

## 🎨 What You Can Do

### Upload & Analyze Papers
- Drag and drop PDF files
- Automatic text extraction
- Parse title, abstract, authors

### Extract Contributions
- **Novel Architectures**: New model designs
- **Loss Functions**: Custom training objectives
- **Algorithms**: Novel procedures
- **Datasets**: New benchmarks
- **Metrics**: Evaluation methods
- **+40 more categories!**

### Extract Experiments
- **Datasets**: Training/validation/test splits
- **Baselines**: Compared methods
- **Results**: Performance metrics
- **Hyperparameters**: Training settings
- **Evidence**: Citations to paper sections

### Custom Queries (Coming Soon)
- Ask natural language questions
- "What datasets were used?"
- "How was the model trained?"

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────┐
│   Browser (http://localhost:3000)  │
│   Next.js + React + Tailwind        │
└─────────────┬───────────────────────┘
              │ HTTP REST API
              ↓
┌─────────────────────────────────────┐
│   Backend (http://localhost:8000)  │
│   FastAPI + LangChain               │
└─────────────┬───────────────────────┘
              │ LangChain
              ↓
┌─────────────────────────────────────┐
│   AWS Bedrock                       │
│   DeepSeek v3 Model                 │
└─────────────────────────────────────┘
```

---

## 🐛 Common Issues

### Issue: "AWS Credentials not found"

**Solution:**
```bash
# Check .env file exists
cat backend/.env

# Verify credentials are set
grep AWS_ACCESS_KEY_ID backend/.env
```

Make sure you've replaced `your_actual_access_key_here` with your real AWS access key.

---

### Issue: "Bedrock model not accessible"

**Solution:**
1. Go to AWS Console → Bedrock
2. Click "Model Access" in left sidebar
3. Find DeepSeek and click "Request Access"
4. Wait for approval (usually instant)

---

### Issue: "Port 8000 already in use"

**Solution:**
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or change port in backend/.env
nano backend/.env
# Change API_PORT=8001
```

---

### Issue: "Module not found" (Python)

**Solution:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

---

### Issue: "Module not found" (Node.js)

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 🔄 Stopping the Servers

### Stop Backend
In Terminal 1, press: `Ctrl+C`

### Stop Frontend
In Terminal 2, press: `Ctrl+C`

---

## 🎓 Next Steps

Now that you're set up, explore:

1. **Test with Different Papers**
   - Try papers from different ML domains
   - Compare extraction quality

2. **Customize Prompts**
   - Edit `backend/extractors/contribution_extractor.py`
   - Modify `USER_PROMPT_TEMPLATE` for your needs

3. **Add New Features**
   - Custom query interface
   - Batch processing
   - Export to CSV/JSON

4. **Deploy to Production**
   - Add database (PostgreSQL)
   - Add authentication
   - Deploy to AWS/Vercel

---

## 📚 Documentation

- **Main README**: `README.md` - Complete documentation
- **API Docs**: `http://localhost:8000/docs` - Interactive API documentation
- **Code Comments**: Every file is well-documented

---

## 💡 Pro Tips

1. **Use Chrome DevTools** - Network tab shows API calls in real-time
2. **Check Backend Logs** - See detailed processing in Terminal 1
3. **Caching is Smart** - Re-extractions are instant (cached)
4. **API First** - Test API endpoints before UI debugging
5. **Watch Costs** - Monitor AWS Bedrock usage in AWS Console

---

## 🎉 You're Ready!

You now have a fully functional AI-powered research paper analyzer!

**Start analyzing papers and extracting insights! 🚀📄🤖**

---

## 📞 Need Help?

- Check `README.md` for detailed documentation
- Review backend logs in Terminal 1
- Check browser console for frontend errors
- Open AWS Console to verify Bedrock access

---

**Happy Analyzing! 🎓✨**


