import subprocess
import os
import numpy as np 
import time
from scipy.io.wavfile import write
import sounddevice as sd 
import sys

# Environment Variables
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
WHISPER_CPP_PATH = os.path.join(SCRIPT_DIR, "whisper.cpp")
WHISPER_EXECUTABLE = os.path.join(WHISPER_CPP_PATH, "build", "bin", "whisper-cli")

CONFIG = {
    "RECORD_SECONDS": 5,
    "SAMPLE_RATE": 16000,
    "WAV_FILE": "temp_audio.wav",
    "WHISPER_MODEL": "models/ggml-base.en.bin",
    "OLLAMA_MODEL": "hf.co/hrsvrn/linux-command-generator-llama3.2-1b:Q4_K_M"
}

def check_dependencies():
    """Check if all required components are installed and accessible"""
    # Check whisper.cpp
    if not os.path.exists(WHISPER_EXECUTABLE):
        print("Error: whisper.cpp executable not found. Please run install_whisper.sh first.")
        return False

    # Check whisper model
    model_path = os.path.join(WHISPER_CPP_PATH, CONFIG["WHISPER_MODEL"])
    if not os.path.exists(model_path):
        print("Error: Whisper model not found. Please run install_whisper.sh to download it.")
        return False

    # Check Ollama
    try:
        subprocess.run(["ollama", "list"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: Ollama not found or not running. Please install and start Ollama first.")
        print("Visit https://ollama.ai for installation instructions.")
        return False

    # Check audio device
    try:
        devices = sd.query_devices()
        if sd.default.device[0] is None:
            print("Error: No default input (microphone) device found.")
            return False
    except sd.PortAudioError as e:
        print(f"Error: Audio system not properly configured: {e}")
        return False

    return True

def record_audio(filename, duration, samplerate):
    """Record audio with better error handling"""
    try:
        print("Starting Recording in 3 seconds")
        time.sleep(3)
        print("Started Recording !!!")
        print(f"Please finish recording under {duration} seconds")
        
        recording = sd.rec(int(duration * samplerate), 
                         samplerate=samplerate, 
                         channels=1, 
                         dtype='int16',
                         blocking=True)
        
        # Normalize audio data
        recording = np.clip(recording, -32768, 32767)
        write(filename, samplerate, recording)
        
        if not os.path.exists(filename):
            raise Exception("Failed to save audio file")
            
        return True
        
    except Exception as e:
        print(f"Error during audio recording: {e}")
        return False

def transcribe_audio(wav_file):
    """Transcribe audio with improved error handling"""
    model_path = os.path.join(WHISPER_CPP_PATH, CONFIG["WHISPER_MODEL"])
    output_file_txt = f"{wav_file}.txt"

    command = [
        WHISPER_EXECUTABLE,
        "-m", model_path,
        "-f", wav_file,
        "-nt",          # No timestamps
        "-otxt",         # Output as a .txt file
        "--no-prints"
    ]

    try:
        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )
            
        if os.path.exists(output_file_txt):
            with open(output_file_txt, 'r') as f:
                transcribed_text = f.read().strip()
            os.remove(output_file_txt)
            if not transcribed_text:
                print("Warning: Transcription produced empty text")
            return transcribed_text
        else:
            raise FileNotFoundError("Whisper.cpp did not produce an output file")
            
    except subprocess.CalledProcessError as e:
        print(f"Error during transcription: {e.stderr}")
        return None
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error during transcription: {e}")
        return None

def generate_command_from_text(text):
    """Generate command using Ollama with improved error handling"""
    if not text:
        return "No text provided"
        
    command = [
        "ollama",
        "run",
        CONFIG["OLLAMA_MODEL"],
        text
    ]
    
    try:
        # Run Ollama
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            timeout=30  # Add timeout to prevent hanging
        )
        
        generated_command = result.stdout.strip()
        if not generated_command:
            return "# No command was generated"
            
        return generated_command

    except subprocess.TimeoutExpired:
        return "# Ollama process timed out"
    except subprocess.CalledProcessError as e:
        print(f"Error during Ollama execution: {e.stderr}")
        return "# Ollama process failed"
    except FileNotFoundError:
        return "# 'ollama' command not found. Is Ollama installed and in your PATH?"
    except Exception as e:
        print(f"Unexpected error during command generation: {e}")
        return "# An unexpected error occurred"

def main():
    """Main function with improved flow and cleanup"""
    if not check_dependencies():
        sys.exit(1)
        
    wav_file = CONFIG["WAV_FILE"]
    try:
        # Record audio
        if not record_audio(wav_file, CONFIG["RECORD_SECONDS"], CONFIG["SAMPLE_RATE"]):
            print("Failed to record audio")
            return

        # Transcribe audio
        transcribed_text = transcribe_audio(wav_file)
        if not transcribed_text:
            print("Failed to transcribe audio")
            return

        # Generate command
        print(f"\nTranscribed text: {transcribed_text}")
        final_command = generate_command_from_text(transcribed_text)
        print(f"\nGenerated command: {final_command}")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Cleanup
        if os.path.exists(wav_file):
            try:
                os.remove(wav_file)
            except Exception as e:
                print(f"Warning: Could not remove temporary file {wav_file}: {e}")

if __name__ == "__main__":
    main()
