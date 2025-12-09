#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Django + React Coding Tests Platform...${NC}"

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/codingtestsvenv" ]; then
    echo -e "${RED}Error: Virtual environment not found at $SCRIPT_DIR/codingtestsvenv${NC}"
    echo "Please create the virtual environment first."
    exit 1
fi

# Function to cleanup processes on exit
cleanup() {
    echo -e "\n${YELLOW}Stopping servers...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up trap to catch Ctrl+C and cleanup
trap cleanup SIGINT SIGTERM

# Start Django backend
echo -e "${GREEN}Starting Django backend server...${NC}"
cd "$SCRIPT_DIR/backend"
"$SCRIPT_DIR/codingtestsvenv/bin/python" manage.py runserver > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend server started (PID: $BACKEND_PID)${NC}"
echo -e "  Django running at: ${YELLOW}http://localhost:8000${NC}"

# Wait a moment for backend to start
sleep 2

# Start React frontend
echo -e "${GREEN}Starting React frontend server...${NC}"
cd "$SCRIPT_DIR/frontend"
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend server started (PID: $FRONTEND_PID)${NC}"
echo -e "  React running at: ${YELLOW}http://localhost:5173${NC}"

echo -e "\n${GREEN}Both servers are running!${NC}"
echo -e "Backend logs: ${YELLOW}logs/backend.log${NC}"
echo -e "Frontend logs: ${YELLOW}logs/frontend.log${NC}"
echo -e "\nPress ${RED}Ctrl+C${NC} to stop both servers\n"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
