# 🎤 Kokoro TTS Frontend Applications

This package provides two user-friendly frontend applications for the Kokoro Text-to-Speech system:

1.  **Web Frontend** - Browser-based interface with modern UI
2.  **Desktop GUI** - Native desktop application with tkinter

## 🚀 Quick Start

For users who already have the prerequisites (like `pyenv`, Python 3.12+, and `espeak-ng`) installed, follow these steps to get the web application running quickly:

## 1. Prerequisites (One-Time Setup)

You only need to perform these steps once on your machine. This guide uses `pyenv` to manage Python versions, which is highly recommended to avoid conflicts with your system's default Python.

### Step 1: Install pyenv


Install `pyenv` using a package manager. If you are on macOS, Homebrew is the recommended method:

#### MACOS
```bash
brew install pyenv
```
#### cachyOS - No Dependencies
```bash
sudo pacman -S pyenv
```
#### cachyOS - with Dependencies
```bash
sudo pacman -S pyenv base-devel openssl zlib xz sqlite bzip2 readline tk ncurses libffi
```
### Install Python 3.12.4 in PYENV environment
```bash
pyenv install 3.12.4
```
### Add to pyenv to your shell with init

For Bash:
```bash
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
source ~/.bash_profile
```

For Zsh:
```bash
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc
```

For Fish:
```bash
echo 'pyenv init - | source' >> ~/.config/fish/config.fish
Restart terminal
```

```bash
# 1. Clone the repository and navigate to the frontend directory
git clone https://github.com/bobdavis84/kokoro.git
cd kokoro/frontend

# 2. Set up the Python environment
pyenv local 3.12.4
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Make script executable and run the web application
source .venv/bin/activate
sh ./start_web.sh
```

Once started, access the application in your browser at the local URL provided in the terminal (e.g., `http://127.0.0.1:53286`).

## 📋 Features

Both applications include a rich set of features:

-   ✅ **Voice Selection** - Choose from multiple available voices
-   ✅ **Playback Speed Control** - Adjust speech speed from 0.5x to 2.0x
-   ✅ **Text Input Box** - Enter text up to 5000 characters
-   ✅ **Generate Speech Button** - One-click speech generation
-   ✅ **Audio Playback** - Built-in audio player
-   ✅ **File Download/Save** - Save generated audio files
-   ✅ **Language Support** - Multiple language options
-   ✅ **Real-time Status** - Shows system status and progress

## 🔧 Detailed Installation and Setup

Follow these steps to get the frontend applications running on your local machine.

### 1. Prerequisites

Make sure you have the following installed on your system:

-   **Git**: To clone the repository.
-   **Python 3.12+**: We recommend using `pyenv` to manage Python versions.
-   **System Dependencies**: `espeak-ng` for text processing and `tk` (optional, for the Desktop GUI).

    **Dependency Installation Commands:**
    -   **Arch / CachyOS:** `sudo pacman -S espeak-ng tk`
    -   **Debian / Ubuntu:** `sudo apt-get install espeak-ng tk`

### 2. Set Up Python Environment (Recommended: `pyenv`)

Using `pyenv` helps manage multiple Python versions without conflicts.

1.  **Install `pyenv`**: Follow the official [pyenv installation guide](https://github.com/pyenv/pyenv#installation).

2.  **Configure your shell** to load `pyenv`. Add the correct command for your shell's startup file (`~/.bashrc`, `~/.zshrc`, or `~/.config/fish/config.fish`).

    -   For **bash**:
        ```bash
        echo 'eval "$(pyenv init -)"' >> ~/.bashrc
        ```
    -   For **zsh**:
        ```bash
        echo 'eval "$(pyenv init -)"' >> ~/.zshrc
        ```
    -   For **fish**:
        ```fish
        echo 'pyenv init - | source' >> ~/.config/fish/config.fish
        ```

3.  **Restart your shell** or run `source <your_shell_config_file>` for the changes to take effect.

4.  **Install Python 3.12.4** (or a newer 3.12+ version):
    ```bash
    pyenv install 3.12.4
    ```

### 3. Install Application Dependencies

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/bobdavis84/kokoro
    ```

2.  **Navigate to the frontend directory**:
    ```bash
    cd kokoro/frontend
    ```

3.  **Set the local Python version** (if you used `pyenv`):
    ```bash
    pyenv local 3.12.4
    ```

4.  **Create and activate a virtual environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
    *Note: To deactivate the virtual environment later, simply run `deactivate`.*

5.  **Install the required Python packages**:
    ```bash
    pip install -r requirements.txt
    ```

### 4. Running the Application

1.  **Make the startup scripts executable**:
    ```bash
    source .venv/bin/activate
    ```

2.  **Start the Web Frontend**:
    ```bash
    sh ./start_web.sh
    ```
    *Note: The first time you run this, it may take a few minutes to download the necessary TTS models.*

3.  **Access the application** in your web browser. The terminal will show you which URLs to use:
    -   Access from the same machine via: `http://127.0.0.1:53286`
    -   Access from other devices on your local network via: `http://<YOUR_LOCAL_IP_ADDRESS>:53286` (e.g., `http://192.168.1.100:53286`). Your local IP address will vary.

4.  **(Alternative) Start the Desktop GUI**:
    ```bash
    ./start_gui.sh
    ```
    
## 🌐 Web Frontend Details

### API Endpoints

The web frontend also provides a REST API:

```bash
# Generate speech
curl -X POST http://localhost:53286/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello world!",
    "voice": "af_heart",
    "language": "a",
    "speed": 1.0
  }'

# Check status
curl http://localhost:53286/status

# Health check
curl http://localhost:53286/health
```

## 🎨 Customization

### Web Frontend Styling
Edit `templates/index.html` to customize colors, layout, and add features.

### Desktop GUI Appearance
Modify `gui_app.py` to change the window size, layout, fonts, and colors.

### Adding New Voices
To add new voices, update the `voices` dictionary in both `app.py` (web) and `gui_app.py` (desktop).

## 🐛 Troubleshooting

1.  **"Kokoro TTS is not available" / "No module named 'kokoro'"**
    - Ensure your virtual environment is active (`source .venv/bin/activate`).
    - Re-run `pip install -r requirements.txt`.

2.  **"No module named 'tkinter'" (Desktop GUI)**
    - Install the `tk` package using your system's package manager (see prerequisites).

3.  **Port already in use (Web Frontend)**
    - Change the port in `app.py`: `app.run(host='0.0.0.0', port=YOUR_PORT)`
    - Or stop the existing process using that port.