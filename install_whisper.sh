#!/bin/bash

set -e  # Exit on any error

echo "Installing Whisper.cpp..."

# Check if whisper.cpp directory already exists
if [ -d "whisper.cpp" ]; then
    echo "whisper.cpp directory already exists. Removing it for fresh install..."
    rm -rf whisper.cpp
fi

# Clone the repository
echo "Cloning whisper.cpp repository..."
git clone https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp

# Download the model
echo "Downloading the base English model..."
if ! bash ./models/download-ggml-model.sh base.en; then
    echo "Error: Failed to download the model"
    exit 1
fi

# Create build directory and compile
echo "Compiling whisper.cpp..."
mkdir -p build && cd build
cmake ..
if ! make -j; then
    echo "Error: Compilation failed"
    exit 1
fi

# Verify the whisper-cli executable exists
if [ ! -f "bin/whisper-cli" ]; then
    echo "Error: Compilation succeeded but 'whisper-cli' executable not found"
    exit 1
fi

echo "Whisper.cpp installation completed successfully!"
cd ../..
