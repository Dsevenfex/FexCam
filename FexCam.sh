#!/bin/bash

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color 

echo -e "${GREEN}[*] FexCam Is Starting ...${NC}"

if [ ! -f "requirements.txt" ]; then
    echo "[-] Error: requirements.txt Not Found!"
    exit 1
fi

if [ ! -d "venv" ]; then
    echo -e "${BLUE}[*] Venv Is Not Found . Creating New ...${NC}"
    python3 -m venv venv
    
    if [ $? -ne 0 ]; then
        echo "[-] Error: Problem creating venv. Make sure python3-venv is installed."
        exit 1
    fi
fi

echo -e "${BLUE}[*] Venv Activate ...${NC}"
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    echo "[-] Error: Not Found Venv Activate Script!"
    exit 1
fi

echo -e "${BLUE}[*] Dependencies Check and Install ...${NC}"
pip install -r requirements.txt 

if [ -f "FexCam.py" ]; then
    echo -e "${GREEN}[+] FexCam Activating ...${NC}"
    python3 FexCam.py
else
    echo "[-] Error: Main Python Folder (FexCam.py) Not Found!"
    deactivate
    exit 1
fi

 deactivate
