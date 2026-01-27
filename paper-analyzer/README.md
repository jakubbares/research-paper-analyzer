# Research Paper Analyzer

AI-powered research paper analysis using AWS Bedrock (DeepSeek), LangChain, FastAPI, and Next.js.

## 🚀 Features

- **PDF Upload & Parsing**: Upload research papers and extract structured content
- **Contribution Extraction**: Automatically identify and categorize technical contributions
- **Experiment Extraction**: Extract experimental details (datasets, baselines, results, hyperparameters)
- **Custom Queries**: Ask questions about papers using natural language
- **Modern UI**: Beautiful, responsive interface built with Next.js and Tailwind CSS
- **AWS Bedrock Integration**: Powered by DeepSeek model via AWS Bedrock
- **LangChain**: Structured LLM interactions
- **Caching**: Intelligent caching of extractions for fast repeat access

## 🏗️ Architecture

```
Frontend (Next.js + React)
         ↓ HTTP/REST
Backend (FastAPI)
         ↓ LangChain
AWS Bedrock (DeepSeek)
```

## 📋 Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **AWS Account** with Bedrock access
- **AWS Credentials** with Bedrock permissions

## 🔧 Installation

### 1. Clone Repository

```bash
cd /Users/jakubbares/Science/New/paper-analyzer
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your AWS credentials
nano .env  # or use any editor
```

**Important**: Update `.env` with your AWS credentials:
```bash
AWS_ACCESS_KEY_ID=your_actual_key_here
AWS_SECRET_ACCESS_KEY=your_actual_secret_here
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=deepseek-ai.deepseek-v3
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Environment is already configured in .env.local
```

## 🚀 Running the Application

### Start Backend (Terminal 1)

```bash
cd backend
source venv/bin/activate  # Activate virtual environment
uvicorn api.app:app --reload --port 8000
```

The backend will be available at: `http://localhost:8000`

API Docs: `http://localhost:8000/docs`

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

The frontend will be available at: `http://localhost:3000`

## 📖 Usage

1. **Open Browser**: Navigate to `http://localhost:3000`

2. **Upload Paper**: 
   - Click "Upload" tab
   - Drag and drop a PDF or click to select
   - Click "Upload and Analyze"

3. **View Paper Info**:
   - Switch to "Paper Info" tab
   - View title, abstract, authors

4. **Extract Contributions**:
   - Click "Extract Contributions" button
   - Wait for AI analysis (30-60 seconds)
   - View categorized contributions

5. **Extract Experiments**:
   - Click "Extract Experiments" button
   - Wait for AI analysis (30-60 seconds)
   - View datasets, baselines, results, hyperparameters

## 🎯 API Endpoints

### Health Check
```bash
GET /health
```

### Upload Paper
```bash
POST /api/papers
Content-Type: multipart/form-data
Body: file (PDF)
```

### Get Paper Info
```bash
GET /api/papers/{paper_id}
```

### Extract Contributions
```bash
POST /api/papers/{paper_id}/extract/contributions
```

### Extract Experiments
```bash
POST /api/papers/{paper_id}/extract/experiments
```

### Custom Query
```bash
POST /api/papers/{paper_id}/query
Body: {"query": "What datasets were used?"}
```

### List All Papers
```bash
GET /api/papers
```

## 📁 Project Structure

```
paper-analyzer/
├── backend/
│   ├── api/
│   │   └── app.py              # FastAPI application
│   ├── parsers/
│   │   └── pdf_parser.py       # PDF parsing logic
│   ├── extractors/
│   │   ├── llm_client.py       # AWS Bedrock + LangChain client
│   │   ├── contribution_extractor.py
│   │   └── experiment_extractor.py
│   ├── config.py               # Configuration management
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # Environment variables
│
├── frontend/
│   ├── app/
│   │   ├── layout.tsx          # Root layout
│   │   └── page.tsx            # Home page
│   ├── components/
│   │   ├── ui/                 # UI components
│   │   ├── PaperUpload.tsx
│   │   ├── ContributionGrid.tsx
│   │   ├── ExperimentViewer.tsx
│   │   └── Providers.tsx       # React Query provider
│   ├── lib/
│   │   ├── api.ts              # API client
│   │   └── utils.ts            # Utilities
│   └── .env.local              # Frontend env vars
│
└── data/
    ├── uploads/                # Uploaded PDFs
    └── extracted/              # Extracted JSON data
```

## 🔑 AWS Bedrock Setup

1. **Enable Bedrock**: Go to AWS Console → Bedrock → Enable service in your region

2. **Request Model Access**: 
   - Navigate to Bedrock → Model Access
   - Request access to DeepSeek models
   - Wait for approval (usually instant)

3. **Create IAM User**:
   - Create user with `AmazonBedrockFullAccess` policy
   - Generate access keys
   - Add keys to `.env` file

4. **Verify Access**:
```bash
aws bedrock list-foundation-models --region us-east-1
```

## 🧪 Testing

### Test Backend
```bash
cd backend
pytest
```

### Test API Manually
```bash
# Health check
curl http://localhost:8000/health

# Upload paper
curl -X POST http://localhost:8000/api/papers \
  -F "file=@/path/to/paper.pdf"
```

## 🐛 Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError`
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Issue**: `AWS Credentials not found`
```bash
# Check .env file
cat .env

# Or set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

**Issue**: `Bedrock model not found`
- Verify you have model access in AWS Console
- Check model ID is correct: `deepseek-ai.deepseek-v3`
- Try a different region if needed

### Frontend Issues

**Issue**: `Cannot connect to backend`
```bash
# Check backend is running
curl http://localhost:8000/health

# Check NEXT_PUBLIC_API_URL in .env.local
cat frontend/.env.local
```

**Issue**: `Module not found`
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 📊 Performance

- **PDF Parsing**: ~1-3 seconds per paper
- **Contribution Extraction**: ~30-60 seconds (depends on paper length)
- **Experiment Extraction**: ~30-60 seconds
- **Caching**: Subsequent requests are instant

## 💰 Cost Estimates

AWS Bedrock DeepSeek pricing (approximate):
- Input: $0.001 per 1K tokens
- Output: $0.003 per 1K tokens

Average per paper:
- ~15K input tokens + ~2K output tokens = ~$0.02 per analysis
- Cached results are free

## 🔒 Security

- Papers are stored locally in `data/uploads/`
- Extractions cached in `data/extracted/`
- No data sent to third parties except AWS Bedrock
- AWS credentials stored in `.env` (gitignored)

## 📝 License

MIT License

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📧 Support

For issues and questions, please open a GitHub issue.

## 🎉 Credits

Built with:
- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://www.langchain.com/)
- [AWS Bedrock](https://aws.amazon.com/bedrock/)
- [Next.js](https://nextjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [React Query](https://tanstack.com/query)
- [PyMuPDF](https://pymupdf.readthedocs.io/)

---

**Happy Paper Analyzing! 🚀📄🤖**


