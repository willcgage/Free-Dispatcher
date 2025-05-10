#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 could not be found. Please install Python3 to proceed."
    exit
fi

# Check if pip is installed
if ! command -v pip &> /dev/null
then
    echo "pip could not be found. Please install pip to proceed."
    exit
fi

# Install dependencies from requirements.txt
pip install -r requirements.txt

echo "Dependencies installed successfully."
