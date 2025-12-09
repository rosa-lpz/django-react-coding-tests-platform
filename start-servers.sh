#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║      Django + React Coding Tests Platform (Dev Mode)      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}\n"

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create logs directory if it doesn't exist
mkdir -p "$SCRIPT_DIR/logs"

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/codingtestsvenv" ]; then
    echo -e "${RED}✗ Error: Virtual environment not found${NC}"
    echo "  Location: $SCRIPT_DIR/codingtestsvenv"
    echo "  Please create the virtual environment first."
    exit 1
fi

# Function to cleanup processes on exit
cleanup() {
    echo -e "\n${YELLOW}Shutting down servers...${NC}"
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo -e "${GREEN}✓${NC} Backend server stopped"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo -e "${GREEN}✓${NC} Frontend server stopped"
    fi
    echo -e "${GREEN}Goodbye!${NC}"
    exit 0
}

# Set up trap to catch Ctrl+C and cleanup
trap cleanup SIGINT SIGTERM

# Start Django backend
echo -e "${YELLOW}[1/2]${NC} Starting Django backend..."
cd "$SCRIPT_DIR/backend"
"$SCRIPT_DIR/codingtestsvenv/bin/python" manage.py runserver 2>&1 | while IFS= read -r line; do
    echo -e "${GREEN}[Backend]${NC} $line"
done &
BACKEND_PID=$!
sleep 3
echo -e "${GREEN}✓ Backend ready${NC} at ${BLUE}http://localhost:8000${NC}\n"

# Start React frontend  
echo -e "${YELLOW}[2/2]${NC} Starting React frontend..."
cd "$SCRIPT_DIR/frontend"
npm run dev 2>&1 | while IFS= read -r line; do
    echo -e "${BLUE}[Frontend]${NC} $line"
done &
FRONTEND_PID=$!
sleep 3
echo -e "${GREEN}✓ Frontend ready${NC} at ${BLUE}http://localhost:5173${NC}\n"

echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                    🚀 Servers Running!                     ║${NC}"
echo -e "${GREEN}╠════════════════════════════════════════════════════════════╣${NC}"
echo -e "${GREEN}║${NC}  Backend (Django):  http://localhost:8000                 ${GREEN}║${NC}"
echo -e "${GREEN}║${NC}  Frontend (React):  http://localhost:5173                 ${GREEN}║${NC}"
echo -e "${GREEN}║${NC}  Admin Panel:       http://localhost:8000/admin           ${GREEN}║${NC}"
echo -e "${GREEN}╠════════════════════════════════════════════════════════════╣${NC}"
echo -e "${GREEN}║${NC}  Test User: ${YELLOW}testuser${NC} / ${YELLOW}testpass123${NC}                      ${GREEN}║${NC}"
echo -e "${GREEN}╠════════════════════════════════════════════════════════════╣${NC}"
echo -e "${GREEN}║${NC}  Press ${RED}Ctrl+C${NC} to stop both servers                       ${GREEN}║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}\n"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
