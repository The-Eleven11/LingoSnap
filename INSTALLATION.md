# LingoSnap Installation Guide

## Prerequisites

### System Requirements
- Ubuntu 20.04 or later (primary support)
- Python 3.10 or higher
- At least 500MB free disk space

### Dependencies
The following system packages are required:
- `python3` (>= 3.10)
- `python3-pip`
- `tesseract-ocr` (for OCR functionality)
- `tesseract-ocr-eng` (English OCR data)
- `tesseract-ocr-chi-sim` (Simplified Chinese OCR data - optional)

## Installation Methods

### Method 1: From Source (Development)

1. **Clone the repository:**
```bash
git clone https://github.com/The-Eleven11/LingoSnap.git
cd LingoSnap
```

2. **Install system dependencies:**
```bash
sudo apt update
sudo apt install python3 python3-pip tesseract-ocr tesseract-ocr-eng tesseract-ocr-chi-sim
```

3. **Install Python dependencies:**
```bash
pip3 install -r requirements.txt
```

4. **Install LingoSnap:**
```bash
pip3 install -e .
```

5. **Run LingoSnap:**
```bash
lingosnap
```

### Method 2: Using pip

```bash
# Install from PyPI (when published)
pip3 install lingosnap

# Run
lingosnap
```

### Method 3: Debian Package (.deb)

1. **Build the package:**
```bash
# Install build dependencies
sudo apt install debhelper python3-all dh-python python3-setuptools

# Build the package
dpkg-buildpackage -us -uc

# The .deb file will be created in the parent directory
```

2. **Install the package:**
```bash
sudo dpkg -i ../lingosnap_0.1.0_all.deb
sudo apt-get install -f  # Fix any missing dependencies
```

3. **Launch from applications menu or terminal:**
```bash
lingosnap
```

## Post-Installation Setup

### 1. Configure Translation Engine

LingoSnap supports two translation engines:

#### Google Translate (Default)
- Works out of the box
- Requires internet connection
- No API key needed for basic use (uses unofficial API)

#### Argos Translate (Offline)
- Download and install language packages:
```bash
# Start LingoSnap
lingosnap

# Go to Settings tab
# Select "Argos Translate" as engine
# Click "Refresh Packages" to see available language packs
# Install desired language packs through the UI
```

### 2. Verify OCR Installation

Test Tesseract OCR:
```bash
tesseract --version
tesseract --list-langs
```

You should see at least `eng` in the list of languages.

### 3. Configure Hotkeys

Default hotkeys:
- **Text Capture:** Ctrl+C+C (press C twice while holding Ctrl)
- **OCR Capture:** Ctrl+F8

To customize:
1. Open LingoSnap
2. Go to Settings tab
3. Modify hotkey values
4. Click "Save Settings"

### 4. Enable Autostart (Optional)

To start LingoSnap automatically on login:

```bash
# Copy desktop file to autostart
mkdir -p ~/.config/autostart
cp /usr/share/applications/lingosnap.desktop ~/.config/autostart/
```

## Terminal Integration

The `lingo` command provides terminal translation:

### Basic Usage
```bash
# Translate the last terminal output line
lingo -t 1

# Translate the 2nd to last output line
lingo -t 2

# Translate to French
lingo -t 1 -l fr

# Translate to Chinese (default if not specified)
lingo -t 1 -l zh
```

### Terminal Setup for Output Capture

For automatic terminal output capture, LingoSnap works best with `tmux`:

1. **Install tmux:**
```bash
sudo apt install tmux
```

2. **Use tmux:**
```bash
# Start a tmux session
tmux

# Run your commands as normal
# Use lingo to translate output
```

Without tmux, lingo will prompt you to paste the text manually.

## Troubleshooting

### Issue: Hotkeys not working
- **Solution:** Ensure LingoSnap is running (check system tray)
- **Solution:** Check if hotkeys conflict with other applications
- **Solution:** Try running with `sudo` to test permissions

### Issue: OCR not working
- **Solution:** Verify Tesseract is installed: `tesseract --version`
- **Solution:** Install language data: `sudo apt install tesseract-ocr-eng`
- **Solution:** Check screenshot permissions

### Issue: Translation fails
- **Solution:** Check internet connection (for Google Translate)
- **Solution:** Install language packages (for Argos Translate)
- **Solution:** Check error message in status bar

### Issue: Application won't start
- **Solution:** Check Python version: `python3 --version` (should be >= 3.10)
- **Solution:** Reinstall dependencies: `pip3 install -r requirements.txt`
- **Solution:** Check logs: `~/.lingosnap/`

## Uninstallation

### From pip:
```bash
pip3 uninstall lingosnap
```

### From .deb:
```bash
sudo apt remove lingosnap
```

### Clean configuration:
```bash
rm -rf ~/.lingosnap/
```

## Next Steps

- Read [USAGE.md](USAGE.md) for detailed usage instructions
- Check [README.md](README.md) for project overview
- Report issues on [GitHub](https://github.com/The-Eleven11/LingoSnap/issues)
