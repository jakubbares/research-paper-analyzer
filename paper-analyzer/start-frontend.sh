#!/bin/bash
# Start Frontend Development Server

echo "🚀 Starting Research Paper Analyzer Frontend..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Start development server
echo "✅ Starting Next.js dev server on http://localhost:3000"
npm run dev
