#!/bin/bash
# Start Backend Server

echo "🚀 Starting Research Paper Analyzer Backend..."
cd backend

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Run setup.sh first."
    exit 1
fi

source venv/bin/activate

# Check .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your AWS credentials before continuing."
    exit 1
fi

# Start server
echo "✅ Starting FastAPI server on http://localhost:8000"
echo "📖 API docs will be available at http://localhost:8000/docs"
uvicorn api.app:app --reload --port 8000
