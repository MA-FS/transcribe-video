import os
import subprocess
import time

# Try to use faster-whisper, but fall back to original whisper if needed
try:
    from faster_whisper import WhisperModel
    USING_FASTER_WHISPER = True
    print("Using faster-whisper library")
except ImportError:
    import whisper
    USING_FASTER_WHISPER = False
    print("Using original whisper library")

def extract_audio_from_files(folder_path):
    """Extract audio from video files in the specified folder"""
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")
        
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if not os.path.isfile(filepath):
            continue  # Skip directories
            
        name, ext = os.path.splitext(filename)
        # Skip files that don't have extensions or are already mp3
        if not ext or ext.lower() == '.mp3' or ext.lower() == '.ds_store':
            continue
            
        mp3_filename = f"{name}.mp3"
        output_filepath = os.path.join(folder_path, mp3_filename)
        
        # Check if MP3 already exists, skip if it does
        if os.path.exists(output_filepath):
            print(f"MP3 already exists for {filename}, skipping extraction")
            continue
            
        # Use ffmpeg to extract audio
        try:
            print(f"Extracting audio from {filename}...")
            result = subprocess.run(
                ['ffmpeg', '-i', filepath, '-q:a', '0', '-map', 'a', output_filepath],
                stderr=subprocess.PIPE,  # Capture error output
                text=True
            )
            
            if result.returncode == 0:
                print(f"✅ Extracted audio from {filename} to {mp3_filename}")
            else:
                print(f"❌ Failed to extract audio from {filename}: {result.stderr}")
        except Exception as e:
            print(f"❌ Error extracting audio from {filename}: {str(e)}")

def transcribe_audio_files(audio_folder, model_size="tiny", use_cpu=True):
    """
    Transcribe audio files using Whisper
    
    Parameters:
    - audio_folder: folder containing audio files
    - model_size: size of Whisper model ('tiny', 'base', 'small', 'medium', 'large-v2')
    - use_cpu: whether to use CPU (True) or GPU (False) for transcription
    """
    print(f"Loading {model_size} Whisper model on {'CPU' if use_cpu else 'GPU'}...")
    
    # Get all mp3 files in the folder
    audio_files = [f for f in os.listdir(audio_folder) 
                  if f.lower().endswith('.mp3') and not f.startswith('.')]
    total_files = len(audio_files)
    
    if total_files == 0:
        print("No MP3 files found for transcription")
        return
        
    print(f"Found {total_files} MP3 files to transcribe")
    
    # Initialize the appropriate model
    try:
        if USING_FASTER_WHISPER:
            # Set device based on parameters
            device = "cpu" if use_cpu else "cuda"
            compute_type = "int8" if use_cpu else "float16"
            model = WhisperModel(model_size, device=device, compute_type=compute_type, download_root="./models")
            print("Faster-Whisper model loaded successfully")
        else:
            # Original whisper library
            device = "cpu" if use_cpu else "cuda"
            model = whisper.load_model(model_size, device=device)
            print("Original Whisper model loaded successfully")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        print("Please try installing the required libraries:")
        print("pip install -U openai-whisper faster-whisper")
        return
    
    for i, audio_file in enumerate(audio_files, 1):
        audio_path = os.path.join(audio_folder, audio_file)
        transcription_filename = f"{os.path.splitext(audio_file)[0]}_transcription.txt"
        output_path = os.path.join(audio_folder, transcription_filename)
        
        # Skip if transcription already exists
        if os.path.exists(output_path):
            print(f"[{i}/{total_files}] Transcription already exists for {audio_file}, skipping")
            continue
        
        print(f"[{i}/{total_files}] Transcribing {audio_file}... (this may take several minutes)")
        start_time = time.time()
        
        try:
            # Transcribe using the appropriate library
            if USING_FASTER_WHISPER:
                try:
                    # Try with faster-whisper
                    segments, info = model.transcribe(
                        audio_path, 
                        beam_size=5,
                        language="en",  # Specify language to avoid detection errors
                        vad_filter=True,
                        vad_parameters=dict(min_silence_duration_ms=500)
                    )
                    
                    # Collect all transcribed text segments
                    transcription_parts = []
                    for segment in segments:
                        transcription_parts.append(segment.text)
                        if len(transcription_parts) % 5 == 0:
                            print(f"  - Processed {len(transcription_parts)} segments so far...")
                    
                    transcription = "\n".join(transcription_parts)
                    
                except Exception as e:
                    # If faster-whisper fails, try to import original whisper
                    print(f"  - Faster-whisper failed, falling back to original whisper: {e}")
                    import whisper
                    model = whisper.load_model(model_size, device=device)
                    result = model.transcribe(audio_path, language="en")
                    transcription = result["text"]
            else:
                # Use original whisper directly
                result = model.transcribe(audio_path, language="en")
                transcription = result["text"]
                print("  - Transcription complete")
            
            # Create a full transcription document
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(transcription)
            
            elapsed = time.time() - start_time
            print(f"✅ Processed {audio_file} in {elapsed:.1f} seconds:")
            print(f"  - Full transcription saved as {transcription_filename}")
            
        except Exception as e:
            print(f"❌ Error processing {audio_file}: {str(e)}")
            continue

if __name__ == "__main__":
    todo_folder_path = 'ToDo'
    
    # Step 1: Extract audio from files
    extract_audio_from_files(todo_folder_path)
    
    # Step 2: Transcribe audio files - using a smaller model for faster processing
    # Change to 'tiny' or 'base' for much faster but less accurate transcription
    # Change to 'medium' or 'large-v2' for slower but more accurate transcription
    transcribe_audio_files(todo_folder_path, model_size="tiny", use_cpu=True)
    
    print("Processing complete!")