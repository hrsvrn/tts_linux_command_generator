#!/bin/bash

# A script to create a Python virtual environment and install dependencies.

# Name of the virtual environment directory
VENV_DIR="venv"

echo "Starting environment setup."

# Check for requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found in the current directory."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment at './$VENV_DIR'."
    python3 -m venv $VENV_DIR
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment. Ensure python3 and the venv module are installed."
        exit 1
    fi
else
    echo "Virtual environment already exists."
fi

# Install dependencies using the virtual environment's pip
echo "Installing dependencies from requirements.txt."
./$VENV_DIR/bin/pip install -r requirements.txt

echo
echo "Setup complete."
echo "To activate the environment, run:"
echo "source $VENV_DIR/bin/activate"

# This block checks if the script was executed with 'source'.
# If so, it activates the environment in the current shell.
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
    source $VENV_DIR/bin/activate
fi
