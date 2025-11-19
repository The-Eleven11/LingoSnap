# LingoSnap Usage Guide

## Overview

LingoSnap provides three main ways to translate text:
1. **Text Capture** - Capture selected text with a hotkey
2. **OCR Capture** - Screenshot and OCR text from images
3. **Terminal Integration** - Translate terminal output

## Getting Started

### Launching LingoSnap

Start the application:
```bash
lingosnap
```

The application will:
- Open the main window
- Minimize to system tray
- Start listening for global hotkeys

### System Tray

LingoSnap runs in the system tray:
- **Click tray icon:** Show/hide main window
- **Right-click tray icon:** Open context menu
  - Show: Display main window
  - Quit: Exit application

## Main Window Interface

The main window has three tabs:

### 1. Text Translate Tab

This is the main translation interface.

**Components:**
- **Language Selection**
  - Source Language dropdown (includes "Auto Detect")
  - Swap button (↔) to exchange languages
  - Target Language dropdown
- **Text Areas**
  - Left: Source text input
  - Right: Translated text output
- **Status Bar**
  - Shows translation status and messages

**How to Use:**
1. Select source and target languages
2. Type or paste text in the left box
3. Translation happens automatically after 2 seconds of inactivity
4. Edit the source text to retranslate
5. Both text areas are scrollable and synchronized

**Features:**
- Auto-detection of source language
- Manual typing with debounced translation
- Instant translation for hotkey-captured text
- Editable source and target text
- Synchronized scrolling

### 2. History Tab

View and manage translation history.

**Features:**
- **History Cards:** Each translation saved as a card showing:
  - Timestamp
  - Language pair (e.g., EN → ZH)
  - Source text preview
  - Translated text preview
- **Click a card:** Restore that translation in the Text Translate tab
- **Refresh button:** Reload history from database
- **Clear All button:** Delete all history entries

**Storage:**
- History is automatically saved for every translation
- Stored in `~/.lingosnap/history.db`
- Configurable limit (default: 100 entries)

### 3. Settings Tab

Configure LingoSnap preferences.

**Translation Engine:**
- **Google Translate:** Online translation, all languages supported
  - API Key field (optional for unofficial API)
  - Character usage counter
  - Reset counter button
- **Argos Translate:** Offline translation, requires language packages
  - View installed language packages
  - Refresh packages button
  - Install new packages (if available)

**Hotkey Settings:**
- **Text Capture Hotkey:** Default `ctrl+c+c`
- **OCR Capture Hotkey:** Default `ctrl+f8`
- Custom hotkeys can be configured

**UI Language:**
- English
- 中文 (Chinese)

**Terminal Default Target Language:**
- Set default language for `lingo` command
- Only shows languages available in selected engine

**About:**
- Version information
- GitHub repository link

**Save Settings Button:**
- Click to save all configuration changes

## Using Hotkeys

### Text Capture (Ctrl+C+C)

Capture and translate selected text:

1. Select text anywhere in your system
2. Press Ctrl+C+C (hold Ctrl, press C twice quickly)
3. LingoSnap window appears with the text
4. Translation happens automatically

**Use Cases:**
- Translate text from web pages
- Translate text from PDF documents
- Translate text from any application

### OCR Capture (Ctrl+F8)

Capture and translate text from images:

1. Press Ctrl+F8
2. Screen darkens with crosshair cursor
3. Click and drag to select an area
4. Release to capture
5. LingoSnap extracts text using OCR
6. Translation happens automatically

**Use Cases:**
- Translate text in images
- Translate text in videos/games
- Translate text that can't be selected

**Tips:**
- Select clear, readable text for best OCR results
- Press ESC to cancel screenshot
- Works with multiple monitors

## Terminal Integration

### Command: `lingo`

Translate terminal output directly from command line.

**Basic Syntax:**
```bash
lingo -t <line_number> [-l <language>]
```

**Options:**
- `-t, --target-line N`: Translate the Nth previous line of output (default: 1)
- `-l, --language CODE`: Target language code (e.g., zh, fr, es)

**Examples:**

1. **Translate last command output:**
```bash
$ echo "Hello, World!"
Hello, World!
$ lingo -t 1
你好，世界！
```

2. **Translate to French:**
```bash
$ echo "The quick brown fox"
The quick brown fox
$ lingo -t 1 -l fr
Le renard brun rapide
```

3. **Translate 2nd to last output:**
```bash
$ echo "First line"
First line
$ echo "Second line"
Second line
$ lingo -t 2
第一行
```

**Requirements:**
- Works best with `tmux` for automatic capture
- Without tmux, will prompt to paste text manually

**Tmux Setup:**
```bash
# Install tmux
sudo apt install tmux

# Start tmux session
tmux

# Run commands and use lingo as normal
```

## Language Support

### Google Translate Engine

Supports 100+ languages including:
- English (en)
- Chinese Simplified (zh-cn)
- Chinese Traditional (zh-tw)
- Spanish (es)
- French (fr)
- German (de)
- Japanese (ja)
- Korean (ko)
- Russian (ru)
- Arabic (ar)
- And many more...

### Argos Translate Engine

Requires manual installation of language packages:
1. Select "Argos Translate" in Settings
2. Click "Refresh Packages"
3. View available packages in the list
4. Download and install needed packages

**Common Packages:**
- English ↔ Chinese
- English ↔ Spanish
- English ↔ French
- English ↔ German

## Tips and Best Practices

### For Best Translation Quality:

1. **Use complete sentences** rather than fragments
2. **Check both source and target** language selections
3. **Use Auto Detect** when unsure of source language
4. **Review translations** as they may not be perfect
5. **Keep text clear** for OCR capture

### For Better Performance:

1. **Close unused tabs** to save memory
2. **Clear history periodically** if it gets too large
3. **Use Argos Translate** for offline/private translations
4. **Keep software updated** for bug fixes

### Keyboard Shortcuts:

- `Ctrl+C+C`: Capture selected text
- `Ctrl+F8`: OCR screenshot
- `ESC`: Cancel screenshot
- Window close: Minimize to tray

## Troubleshooting

### Translation is slow
- Check internet connection (Google Translate)
- Check if source text is very long
- Consider using Argos Translate for offline speed

### OCR not recognizing text
- Ensure text is clear and readable
- Select a larger area around the text
- Check if correct language data is installed for Tesseract

### Hotkeys not working
- Check if LingoSnap is running (system tray)
- Check for hotkey conflicts with other apps
- Verify hotkey settings in Settings tab

### History not saving
- Check disk space
- Verify permissions: `ls -la ~/.lingosnap/`
- Check database file exists: `~/.lingosnap/history.db`

## Configuration Files

LingoSnap stores configuration and data in `~/.lingosnap/`:

- `config.json`: Application settings
- `history.db`: Translation history database
- `argos-packages/`: Argos language packages (if installed)

**Backup Configuration:**
```bash
cp -r ~/.lingosnap/ ~/lingosnap-backup/
```

**Reset Configuration:**
```bash
rm -rf ~/.lingosnap/
# Restart LingoSnap to create fresh config
```

## Advanced Usage

### Custom Hotkeys

You can customize hotkeys in the Settings tab. Format examples:
- `ctrl+shift+t`
- `ctrl+alt+o`
- `ctrl+f9`

### Multiple Language Pairs

Quickly switch between language pairs:
1. Use the swap button (↔) to reverse languages
2. Or manually select from dropdowns
3. Settings are remembered between sessions

### Batch Translation

For translating multiple items:
1. Use History tab to keep track
2. Each translation is automatically saved
3. Click history cards to review

## Integration with Other Tools

### Browser Integration
- Select text in browser
- Use Ctrl+C+C hotkey
- Translation appears instantly

### IDE Integration
- Works with any text editor/IDE
- Select code comments
- Use hotkeys for translation

### Document Translation
- PDF readers
- Office applications
- Any application with selectable text

## Privacy and Data

- **Google Translate:** Data sent to Google servers
- **Argos Translate:** All processing done locally
- **History:** Stored only on local machine
- **Hotkeys:** Monitored only while app is running

For maximum privacy, use Argos Translate engine.

## Getting Help

- **GitHub Issues:** https://github.com/The-Eleven11/LingoSnap/issues
- **Documentation:** Check README.md and INSTALLATION.md
- **Logs:** Check `~/.lingosnap/` for any log files

## Contributing

To contribute to LingoSnap:
1. Fork the repository
2. Make your changes
3. Submit a pull request

See DEVELOPER.md for development guidelines.
