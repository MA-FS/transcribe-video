#!/bin/bash

echo "==== Video Transcription Tool Setup ===="
echo "This script will install all requirements for the Video Transcription Tool."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Step 1: Check and install ffmpeg if needed
echo "Checking for ffmpeg..."
if command_exists ffmpeg; then
    echo "✅ ffmpeg is already installed."
else
    echo "❌ ffmpeg not found. Attempting to install..."
    
    # Detect OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command_exists brew; then
            echo "Installing ffmpeg using Homebrew..."
            brew install ffmpeg
        else
            echo "❌ Homebrew not found. Please install Homebrew first:"
            echo "    /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            echo "Then run this setup script again."
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command_exists apt; then
            echo "Installing ffmpeg using apt..."
            sudo apt update
            sudo apt install -y ffmpeg
        elif command_exists yum; then
            echo "Installing ffmpeg using yum..."
            sudo yum install -y ffmpeg
        else
            echo "❌ Unable to determine package manager. Please install ffmpeg manually."
            exit 1
        fi
    else
        echo "❌ Unsupported operating system. Please install ffmpeg manually."
        exit 1
    fi
    
    # Verify installation
    if command_exists ffmpeg; then
        echo "✅ ffmpeg installed successfully."
    else
        echo "❌ Failed to install ffmpeg. Please install it manually."
        exit 1
    fi
fi

# Step 2: Create virtual environment
echo "Creating Python virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists."
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment. Please make sure Python 3.8+ is installed."
        exit 1
    fi
    echo "✅ Virtual environment created."
fi

# Step 3: Activate virtual environment and install packages
echo "Activating virtual environment and installing Python packages..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment."
    exit 1
fi

echo "Installing Python packages..."
pip install --upgrade pip
pip install openai-whisper faster-whisper

# Step 4: Create ToDo directory if it doesn't exist
echo "Creating ToDo directory for video files..."
if [ ! -d "ToDo" ]; then
    mkdir ToDo
    echo "✅ ToDo directory created."
else
    echo "ToDo directory already exists."
fi

echo ""
echo "==== Setup Complete ===="
echo "To use the Video Transcription Tool:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo "2. Place your video files in the 'ToDo' folder"
echo "3. Run the script:"
echo "   python process_todo_files.py"
echo ""
echo "For more details, please refer to the README.md file." 