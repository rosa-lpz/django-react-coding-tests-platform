#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Stopping all development servers...${NC}\n"

# Kill processes on port 8000 (Django)
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}Stopping Django backend (port 8000)...${NC}"
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    echo -e "${GREEN}✓ Django stopped${NC}"
else
    echo -e "Django backend not running on port 8000"
fi

# Kill processes on port 5173 (Vite/React)
if lsof -Pi :5173 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}Stopping React frontend (port 5173)...${NC}"
    lsof -ti:5173 | xargs kill -9 2>/dev/null
    echo -e "${GREEN}✓ React stopped${NC}"
else
    echo -e "React frontend not running on port 5173"
fi

echo -e "\n${GREEN}All servers stopped!${NC}"
