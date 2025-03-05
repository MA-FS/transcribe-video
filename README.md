# Video Transcription Tool

This tool automates the process of extracting audio from video files and transcribing the audio content using OpenAI's Whisper speech recognition models.

## Overview

The `process_todo_files.py` script performs two main functions:
1. Extracts audio (MP3 format) from video files in a designated folder
2. Transcribes the extracted audio files using either the original Whisper or faster-whisper library

## Requirements

- Python 3.8+
- ffmpeg (for audio extraction)
- OpenAI's Whisper or faster-whisper library
- Sufficient disk space for audio files and model downloads

## Setup

### Automatic Setup (Recommended)

We provide setup scripts to automatically install all requirements:

#### For macOS/Linux:
```bash
# Make the script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

#### For Windows:
```batch
# Run the setup script
setup.bat
```

The setup script will:
1. Check for and install ffmpeg (or guide you through installation)
2. Create a Python virtual environment
3. Install all required Python packages
4. Create the necessary directories

### Manual Setup

If the automatic setup doesn't work for you, you can follow these manual steps:

#### 1. Install ffmpeg

#### macOS (using Homebrew):
```bash
brew install ffmpeg
```

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg
```

#### Windows:
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

#### 2. Create a Virtual Environment

```bash
# Create the virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

#### 3. Install Required Python Packages

```bash
# Install the original Whisper implementation
pip install openai-whisper

# For better performance (recommended if your system supports it)
pip install faster-whisper
```

## Usage

1. Activate the virtual environment (if not already activated):
   ```bash
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   # venv\Scripts\activate
   ```

2. Place your video files in the `ToDo` folder

3. Run the script:
   ```bash
   python process_todo_files.py
   ```

4. The script will:
   - Extract audio from all video files in the `ToDo` folder
   - Transcribe each audio file using the Whisper model
   - Save transcriptions as text files in the same folder

## Configuration Options

You can modify these parameters in the script:

```python
# Change model size for different accuracy/speed trade-offs:
# - "tiny": Fastest, least accurate
# - "base": Fast, reasonable accuracy
# - "small": Balanced speed/accuracy
# - "medium": Slower, more accurate
# - "large-v2": Slowest, most accurate
transcribe_audio_files(todo_folder_path, model_size="tiny", use_cpu=True)

# Set use_cpu=False to use GPU acceleration (if CUDA is available)
```

## Expected Output

1. Audio extraction:
   - For each video file (e.g., `video.mp4`), an MP3 file (`video.mp3`) will be created
   - The script skips files that have already been processed

2. Transcription:
   - For each audio file (e.g., `video.mp3`), a text file (`video_transcription.txt`) will be created
   - The script skips transcription for files that already have transcription files

3. Console output:
   - Progress indicators showing which files are being processed
   - Notifications when files are skipped (already processed)
   - Time taken for transcription of each file
   - Error messages if any issues occur

## Performance Notes

- Transcription speed depends on:
  - The chosen model size
  - Whether CPU or GPU is used
  - The length of the audio file
  - Your computer's specifications
- The first run will download the Whisper model, which might take time depending on your internet connection
- Models are cached in the `./models` directory for future use

## Troubleshooting

If you encounter errors:

1. Make sure ffmpeg is properly installed and accessible in your PATH
2. Check that you have the required Python libraries installed
3. For GPU acceleration, ensure you have CUDA properly set up
4. For memory issues, try using a smaller model size