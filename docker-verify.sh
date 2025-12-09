#!/bin/bash

# Docker Setup Verification Script
# This script checks if your Docker setup is ready

set -e

echo "=================================="
echo "Docker Setup Verification"
echo "=================================="
echo

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
echo -n "Checking Docker installation... "
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓${NC}"
    docker --version
else
    echo -e "${RED}✗${NC}"
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

echo

# Check if Docker Compose is installed
echo -n "Checking Docker Compose installation... "
if command -v docker-compose &> /dev/null || docker compose version &> /dev/null; then
    echo -e "${GREEN}✓${NC}"
    docker compose version 2>/dev/null || docker-compose --version
else
    echo -e "${RED}✗${NC}"
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo

# Check if Docker daemon is running
echo -n "Checking Docker daemon... "
if docker info &> /dev/null; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    echo "Docker daemon is not running. Please start Docker."
    exit 1
fi

echo

# Check if .env.docker exists
echo -n "Checking .env.docker file... "
if [ -f .env.docker ]; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${YELLOW}⚠${NC}"
    echo "  .env.docker not found. Creating from template..."
    if [ -f .env.docker.example ]; then
        cp .env.docker.example .env.docker
        echo "  Created .env.docker from .env.docker.example"
        echo -e "  ${YELLOW}Please edit .env.docker and set your values${NC}"
    else
        echo -e "  ${RED}Error: .env.docker.example not found${NC}"
        exit 1
    fi
fi

echo

# Check if port 8000 is available
echo -n "Checking if port 8000 is available... "
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 || netstat -tuln 2>/dev/null | grep -q ':8000 '; then
    echo -e "${YELLOW}⚠${NC}"
    echo "  Port 8000 is already in use. You may need to stop the service using it."
    echo "  Run: lsof -i :8000 to see what's using the port"
else
    echo -e "${GREEN}✓${NC}"
fi

echo

# Check if port 5432 is available
echo -n "Checking if port 5432 is available... "
if lsof -Pi :5432 -sTCP:LISTEN -t >/dev/null 2>&1 || netstat -tuln 2>/dev/null | grep -q ':5432 '; then
    echo -e "${YELLOW}⚠${NC}"
    echo "  Port 5432 is already in use (PostgreSQL default port)."
    echo "  This is usually fine if you don't have a local PostgreSQL running."
else
    echo -e "${GREEN}✓${NC}"
fi

echo

# Check Docker Compose file
echo -n "Checking docker-compose.yml... "
if [ -f docker-compose.yml ]; then
    echo -e "${GREEN}✓${NC}"
    if docker compose config &> /dev/null || docker-compose config &> /dev/null; then
        echo "  docker-compose.yml is valid"
    else
        echo -e "  ${RED}docker-compose.yml has errors${NC}"
        exit 1
    fi
else
    echo -e "${RED}✗${NC}"
    echo "docker-compose.yml not found"
    exit 1
fi

echo

# Check Dockerfile
echo -n "Checking Dockerfile... "
if [ -f Dockerfile ]; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    echo "Dockerfile not found"
    exit 1
fi

echo

echo "=================================="
echo -e "${GREEN}All checks passed!${NC}"
echo "=================================="
echo
echo "You can now build and run the application:"
echo
echo "  docker-compose up --build"
echo
echo "Or run in detached mode:"
echo
echo "  docker-compose up -d --build"
echo
echo "To view logs:"
echo
echo "  docker-compose logs -f"
echo
echo "To stop:"
echo
echo "  docker-compose down"
echo
echo "=================================="
