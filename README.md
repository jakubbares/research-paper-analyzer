# Research Paper Analyzer

AI-powered research paper analysis system that automatically extracts contributions, experiments, and insights from ML research papers.

## 🚀 Quick Start

```bash
cd paper-analyzer
```

See **[paper-analyzer/README.md](paper-analyzer/README.md)** for complete documentation.

## 🎯 Features

- **PDF Upload & Parsing**: Upload research papers and extract structured content
- **Contribution Extraction**: Automatically identify and categorize technical contributions
- **Experiment Extraction**: Extract experimental details (datasets, baselines, results, hyperparameters)
- **Multi-Paper Analysis**: Analyze multiple papers and compare across contributions
- **Custom Queries**: Ask questions about papers using natural language
- **Modern UI**: Beautiful, responsive interface built with Next.js and Tailwind CSS

## 🏗️ Architecture

```
Frontend (Next.js + React + Tailwind)
         ↓ HTTP/REST
Backend (FastAPI + Python)
         ↓ LangChain
AWS Bedrock (DeepSeek V3)
```

## 📋 Prerequisites

- Python 3.10+
- Node.js 18+
- AWS Account with Bedrock access
- AWS Credentials with Bedrock permissions

## 🔧 Installation

### 1. Backend Setup

```bash
cd paper-analyzer/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `.env` file with AWS credentials:
```bash
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=deepseek-ai.deepseek-v3
```

### 2. Frontend Setup

```bash
cd paper-analyzer/frontend
npm install
```

## 🚀 Running

### Start Backend (Terminal 1)

```bash
cd paper-analyzer/backend
source venv/bin/activate
uvicorn api.app:app --reload --port 8000
```

### Start Frontend (Terminal 2)

```bash
cd paper-analyzer/frontend
npm run dev
```

Open browser: `http://localhost:3000`

## 📖 Usage

1. **Upload Paper**: Drag and drop a PDF research paper
2. **Extract Contributions**: Click to analyze and categorize technical innovations
3. **Extract Experiments**: Analyze experimental setups, baselines, and results
4. **Multi-Paper Analysis**: Upload multiple papers and compare insights
5. **Custom Queries**: Ask natural language questions about the papers

## 🎯 API Endpoints

- `POST /api/papers` - Upload paper
- `GET /api/papers/{id}` - Get paper info
- `POST /api/papers/{id}/extract/contributions` - Extract contributions
- `POST /api/papers/{id}/extract/experiments` - Extract experiments
- `POST /api/papers/{id}/query` - Custom query
- `GET /api/papers` - List all papers

Full API docs: `http://localhost:8000/docs`

## 📁 Project Structure

```
paper-analyzer/
├── backend/
│   ├── api/              # FastAPI application
│   ├── parsers/          # PDF parsing
│   ├── extractors/       # LLM-based extraction
│   └── aggregation/      # Multi-paper analysis
├── frontend/
│   ├── app/              # Next.js pages
│   ├── components/       # React components
│   └── lib/              # API client & utils
└── data/
    ├── uploads/          # Uploaded PDFs
    └── extracted/        # Cached extractions
```

## 🔑 AWS Bedrock Setup

1. Enable Bedrock in AWS Console
2. Request access to DeepSeek models
3. Create IAM user with `AmazonBedrockFullAccess`
4. Add credentials to `.env` file

See [paper-analyzer/AWS_SETUP_GUIDE.md](paper-analyzer/AWS_SETUP_GUIDE.md) for details.

## 💰 Cost Estimates

AWS Bedrock DeepSeek pricing:
- ~$0.02 per paper analysis
- Cached results are free

## 📊 Performance

- PDF Parsing: ~1-3 seconds
- Contribution Extraction: ~30-60 seconds
- Experiment Extraction: ~30-60 seconds
- Caching: Subsequent requests are instant

## 🔒 Security

- Papers stored locally in `data/uploads/`
- Extractions cached in `data/extracted/`
- No data sent to third parties except AWS Bedrock
- AWS credentials in `.env` (gitignored)

## 🧪 Extractors Available

- **Contributions**: Novel architectures, loss functions, training procedures, datasets
- **Experiments**: Datasets, baselines, metrics, results, hyperparameters
- **Ablation Studies**: Component analysis and impact
- **Architecture**: Model structure and design choices
- **Training**: Optimization procedures and techniques
- **Algorithms**: Novel algorithmic contributions
- **Datasets**: New datasets introduced
- **Metrics**: Evaluation metrics used
- **Baselines**: Comparison methods
- **Code/Resources**: Available implementations
- **Claims**: Main claims and contributions
- **Equations**: Mathematical formulations
- **Future Work**: Proposed future directions
- **Limitations**: Acknowledged limitations
- **Related Work**: Literature context
- **Loss Functions**: Training objectives
- **Hyperparameters**: Training configurations

## 📝 Tech Stack

**Backend:**
- FastAPI
- LangChain
- AWS Bedrock (DeepSeek)
- PyMuPDF
- Python 3.10+

**Frontend:**
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- React Query
- shadcn/ui

## 📧 Support

For detailed documentation, see [paper-analyzer/README.md](paper-analyzer/README.md)

## 📝 License

MIT License

---

**Built with FastAPI, LangChain, AWS Bedrock, Next.js, and Tailwind CSS**

🚀 Happy Paper Analyzing! 📄🤖
