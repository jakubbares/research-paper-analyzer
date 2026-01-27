# 🚀 DEPLOYMENT GUIDE - 100% COMPLETE SYSTEM

## Quick Start with Docker (Recommended)

### Prerequisites
- Docker & Docker Compose installed
- AWS Bedrock access (API keys)

### 1. Clone & Configure

```bash
cd /Users/jakubbares/Science/New/paper-analyzer

# Create .env file with AWS credentials
cat > .env << EOF
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=meta.llama3-3-70b-instruct-v1:0
ALLOWED_ORIGINS=http://localhost:3000
EOF
```

### 2. Build & Run

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 4. Stop Services

```bash
docker-compose down

# To remove volumes too
docker-compose down -v
```

---

## Manual Deployment (Development)

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your AWS credentials

# Run server
uvicorn api.app:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Run development server
npm run dev

# Or build for production
npm run build
npm start
```

---

## Production Deployment

### AWS / Cloud Deployment

1. **Build Docker images:**
```bash
docker-compose build
```

2. **Push to container registry:**
```bash
docker tag paper-analyzer-backend:latest your-registry/paper-analyzer-backend:latest
docker tag paper-analyzer-frontend:latest your-registry/paper-analyzer-frontend:latest

docker push your-registry/paper-analyzer-backend:latest
docker push your-registry/paper-analyzer-frontend:latest
```

3. **Deploy to cloud:**
   - AWS ECS/Fargate
   - Google Cloud Run
   - Azure Container Instances
   - Digital Ocean App Platform

### Environment Variables

**Backend:**
- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `AWS_REGION` - AWS region (default: us-east-1)
- `BEDROCK_MODEL_ID` - Model ID (default: meta.llama3-3-70b-instruct-v1:0)
- `ALLOWED_ORIGINS` - CORS origins (comma-separated)
- `API_PORT` - API port (default: 8000)

**Frontend:**
- `NEXT_PUBLIC_API_URL` - Backend URL

---

## Troubleshooting

### Backend won't start

**Check AWS credentials:**
```bash
# Test AWS Bedrock access
aws bedrock list-foundation-models --region us-east-1
```

**Check Python version:**
```bash
python --version  # Should be 3.10+
```

### Frontend won't connect

**Check API URL:**
```bash
# Make sure backend is running
curl http://localhost:8000/health
```

### Docker issues

**Clean rebuild:**
```bash
docker-compose down -v
docker system prune -a
docker-compose up --build
```

---

## System Requirements

### Minimum
- 2 CPU cores
- 4 GB RAM
- 10 GB disk space
- Python 3.10+
- Node.js 18+

### Recommended
- 4 CPU cores
- 8 GB RAM
- 50 GB disk space
- Docker 20+

---

## Features Included

✅ **5 AI Extractors** - Contributions, Experiments, Architecture, Hyperparameters, Ablations
✅ **Export System** - JSON, CSV, Markdown
✅ **Batch Upload** - Multiple papers at once
✅ **Multi-Paper Analysis** - Cross-paper insights
✅ **Dashboard** - Charts and visualizations
✅ **16 API Endpoints** - Complete REST API
✅ **Docker Ready** - One-command deployment
✅ **Production Ready** - Error handling, caching, validation

---

## API Documentation

Full API docs available at: http://localhost:8000/docs (when running)

---

## Support

Issues? Check:
1. Backend logs: `docker-compose logs backend`
2. Frontend logs: `docker-compose logs frontend`
3. AWS Bedrock status
4. Environment variables

---

**🎉 YOU'RE READY TO DEPLOY!**


