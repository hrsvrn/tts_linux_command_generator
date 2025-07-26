# Linux Command Generator

This project uses speech-to-text and a large language model to generate Linux commands from spoken English. You can say something like "create a new directory called my_folder" and the script will output the corresponding command: `mkdir my_folder`.

## How it Works

1.  **Audio Recording:** The script records 5 seconds of audio from your microphone.
2.  **Transcription:** The recorded audio is converted to text using a local `whisper.cpp` model.
3.  **Command Generation:** The transcribed text is then sent to a local `Ollama` model, which generates the corresponding Linux command.

## Prerequisites

*   **Linux Environment:** This script is designed for Linux.
*   **Python 3:** The main script is written in Python.
*   **Ollama:** You need to have Ollama installed and running. You can find installation instructions at [https://ollama.ai](https://ollama.ai).
*   **PortAudio:** This is required for audio recording. You can typically install it using your system's package manager (e.g., `sudo apt-get install portaudio19-dev` on Debian/Ubuntu).

## Installation

1.  **Create Virtual Environment and Install Dependencies:**
    This script will create a Python virtual environment and install the necessary dependencies.
    ```bash
    ./create_venv.sh
    ```

2.  **Install whisper.cpp:**
    This script will clone the `whisper.cpp` repository, download the required model, and compile the code.
    ```bash
    ./install_whisper.sh
    ```

## Usage

1.  **Activate the virtual environment:**
    ```bash
    source venv/bin/activate
    ```

2.  **Run the command generator:**
    ```bash
    python3 command_generator.py
    ```

3.  **Speak a command:** After the script starts, you will have 5 seconds to speak a command. For example, you could say:
    *   "list all the files in the current directory"
    *   "create a new text file called hello_world.txt"
    *   "show me the running processes"

4.  **View the output:** The script will print the transcribed text and the generated Linux command to the console.

## Configuration

The script's behavior can be configured by editing the `CONFIG` dictionary in `command_generator.py`:

*   `RECORD_SECONDS`: The duration of the audio recording in seconds.
*   `SAMPLE_RATE`: The sample rate for the audio recording.
*   `WAV_FILE`: The name of the temporary audio file.
*   `WHISPER_MODEL`: The `whisper.cpp` model to use for transcription.
*   `OLLAMA_MODEL`: The `Ollama` model to use for command generation.
