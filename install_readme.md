# Installation Guide

This guide will help you set up the Mario Kart 64 World Model project environment.

## Prerequisites

- **Python 3.12** (required - Python 3.13 is not compatible with some packages)
- **Ubuntu/Debian** system (for system dependencies)
- **Git** (to clone the repository)

## System Dependencies

First, install the required system packages:

```bash
# Update package list
sudo apt update

# Install Python 3.12 and venv support
sudo apt install python3.12 python3.12-venv python3.12-dev

# Install SDL2 libraries for pygame
sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev

# Install other build dependencies
sudo apt install build-essential pkg-config
```

## Python Environment Setup

1. **Navigate to the project directory:**
   ```bash
   cd /path/to/wm_mariokart64
   ```

2. **Remove any existing virtual environment:**
   ```bash
   rm -rf .venv
   ```

3. **Create a new virtual environment with Python 3.12:**
   ```bash
   python3.12 -m venv .venv
   ```

4. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

5. **Verify Python version:**
   ```bash
   python --version
   # Should output: Python 3.12.x
   ```

## Install Python Dependencies

1. **Navigate to the diamond directory:**
   ```bash
   cd diamond
   ```

2. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   pip list
   ```

## Optional: Atari Support

If you need Atari environment support, install it separately:

```bash
pip install "gymnasium[atari,accept-rom-license]"
```

## Additional Dependencies

The project also requires PyTorch and Jupyter/IPython support. These are included in the requirements.txt:

- **PyTorch**: For deep learning models
- **IPython/Jupyter**: For interactive development and display functions

## Troubleshooting

### Common Issues

1. **"python3.12: command not found"**
   - Install Python 3.12: `sudo apt install python3.12`

2. **"ensurepip is not available"**
   - Install venv support: `sudo apt install python3.12-venv`

3. **"sdl2-config: not found"**
   - Install SDL2 libraries: `sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev`

4. **Package installation fails**
   - Make sure you're using Python 3.12, not 3.13
   - Check that the virtual environment is activated
   - Try installing packages one by one if there are conflicts

### Why Python 3.12?

- **Compatibility**: All required packages (numpy 1.26.0, pillow 10.3.0, etc.) are fully compatible with Python 3.12
- **Stability**: Python 3.12 is mature and widely adopted in the ML/DL community
- **Avoid dependency hell**: Python 3.13 is too new and many packages don't support it yet

## Usage

After installation, you can run the project:

```bash
# Activate the environment
source .venv/bin/activate
cd diamond

# Run your scripts
python src/main.py
```

## Environment Management

- **Activate environment**: `source .venv/bin/activate`
- **Deactivate environment**: `deactivate`
- **Check installed packages**: `pip list`
- **Update packages**: `pip install --upgrade package_name`

## Project Structure

```
wm_mariokart64/
├── .venv/                 # Virtual environment (created during setup)
├── diamond/               # Main project directory
│   ├── requirements.txt   # Python dependencies
│   ├── src/              # Source code
│   └── config/           # Configuration files
├── dataset/              # Dataset utilities
└── colab/                # Jupyter notebooks
```

---

**Note**: This setup has been tested on Ubuntu 24.04 with Python 3.12.3. If you encounter issues on other systems, please check the specific package documentation for your platform.
