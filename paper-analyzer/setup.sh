#!/bin/bash
# Setup Script for Research Paper Analyzer

echo "🔧 Setting up Research Paper Analyzer..."

# Backend setup
echo ""
echo "📦 Setting up Backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate and install
source venv/bin/activate
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env if doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Edit backend/.env with your AWS credentials!"
fi

# Create data directories
mkdir -p ../data/uploads
mkdir -p ../data/extracted

cd ..

# Frontend setup
echo ""
echo "📦 Setting up Frontend..."
cd frontend

# Install npm dependencies
echo "Installing Node dependencies..."
npm install

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env with your AWS credentials"
echo "2. Run './start-backend.sh' in one terminal"
echo "3. Run './start-frontend.sh' in another terminal"
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "🚀 Happy analyzing!"
