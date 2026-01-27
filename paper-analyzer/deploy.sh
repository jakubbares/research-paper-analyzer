#!/bin/bash

# 🚀 ONE-COMMAND DEPLOYMENT SCRIPT
# Paper Analyzer - Complete System

set -e  # Exit on error

echo "🚀 Starting Paper Analyzer Deployment..."
echo "========================================"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}❌ Error: docker-compose.yml not found!${NC}"
    echo "Please run this script from the paper-analyzer directory"
    exit 1
fi

echo ""
echo -e "${BLUE}📋 Pre-flight checks...${NC}"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    echo "Install from: https://www.docker.com/get-started"
    exit 1
fi
echo -e "${GREEN}✅ Docker installed${NC}"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker Compose installed${NC}"

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo -e "${RED}❌ backend/.env not found!${NC}"
    echo ""
    echo "Creating from .env.example..."
    cp backend/.env.example backend/.env 2>/dev/null || true
    echo ""
    echo -e "${RED}⚠️  Please edit backend/.env with your AWS credentials:${NC}"
    echo "   nano backend/.env"
    exit 1
fi
echo -e "${GREEN}✅ Environment configured${NC}"

# Check AWS credentials
if grep -q "your_access_key_here" backend/.env 2>/dev/null; then
    echo -e "${RED}❌ AWS credentials not configured in backend/.env${NC}"
    echo "Please edit backend/.env with real AWS credentials"
    exit 1
fi
echo -e "${GREEN}✅ AWS credentials configured${NC}"

echo ""
echo -e "${BLUE}🔨 Building Docker images...${NC}"
docker-compose build

echo ""
echo -e "${BLUE}🚀 Starting services...${NC}"
docker-compose up -d

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "========================================"
echo "🎉 Paper Analyzer is now running!"
echo "========================================"
echo ""
echo "Access the application:"
echo -e "  ${BLUE}Frontend:${NC}  http://localhost:3000"
echo -e "  ${BLUE}Backend:${NC}   http://localhost:8000"
echo -e "  ${BLUE}API Docs:${NC}  http://localhost:8000/docs"
echo ""
echo "View logs:"
echo "  docker-compose logs -f"
echo ""
echo "Stop services:"
echo "  docker-compose down"
echo ""
echo "========================================"


