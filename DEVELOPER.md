# LingoSnap Developer Guide

## Project Overview

LingoSnap is a desktop translation application built with Python and PyQt6, designed to run primarily on Ubuntu Linux with architecture for cross-platform compatibility.

## Project Structure

```
LingoSnap/
├── lingosnap/                  # Main package
│   ├── __init__.py
│   ├── __main__.py            # Application entry point
│   ├── engines/               # Translation engines
│   │   ├── __init__.py
│   │   ├── base.py           # Abstract base class
│   │   ├── google_engine.py  # Google Translate implementation
│   │   └── argos_engine.py   # Argos Translate implementation
│   ├── gui/                   # GUI components
│   │   ├── __init__.py
│   │   ├── main_window.py    # Main window with system tray
│   │   ├── text_translate_tab.py
│   │   ├── history_tab.py
│   │   ├── settings_tab.py
│   │   ├── hotkey_manager.py # Global hotkey handling
│   │   └── screenshot_tool.py # OCR screenshot capture
│   ├── utils/                 # Utility modules
│   │   ├── __init__.py
│   │   ├── config.py         # Configuration management
│   │   ├── history.py        # History database
│   │   └── ocr.py            # OCR functionality
│   └── cli/                   # Terminal integration
│       ├── __init__.py
│       └── terminal.py        # CLI tool
├── tests/                     # Unit tests
├── debian/                    # Debian packaging files
│   ├── control
│   ├── rules
│   ├── changelog
│   ├── compat
│   └── lingosnap.desktop
├── requirements.txt           # Python dependencies
├── setup.py                   # Package setup
├── README.md                  # Project overview
├── INSTALLATION.md            # Installation guide
├── USAGE.md                   # Usage documentation
└── DEVELOPER.md              # This file

```

## Architecture

### Design Patterns

1. **Strategy Pattern**: Translation engines implement a common interface
2. **Observer Pattern**: Qt signals/slots for event handling
3. **Singleton Pattern**: Configuration and database managers
4. **MVC Pattern**: Separation of GUI, logic, and data

### Key Components

#### Translation Engines

All engines inherit from `TranslationEngine` base class:

```python
class TranslationEngine(ABC):
    @abstractmethod
    def translate(text, source_lang, target_lang) -> str
    
    @abstractmethod
    def get_supported_languages() -> List[Tuple[str, str]]
    
    @abstractmethod
    def detect_language(text) -> Optional[str]
    
    @abstractmethod
    def is_available() -> bool
```

**Implementations:**
- `GoogleTranslateEngine`: Online translation via googletrans library
- `ArgosTranslateEngine`: Offline translation with Argos Translate

#### GUI Architecture

Built with PyQt6:
- `MainWindow`: Central window with tab widget and system tray
- `TextTranslateTab`: Main translation interface
- `HistoryTab`: Translation history viewer
- `SettingsTab`: Configuration interface

**Key Features:**
- System tray integration
- Global hotkey monitoring
- Screenshot capture overlay
- Synchronized text scrolling

#### Data Management

- **Config**: JSON-based configuration in `~/.lingosnap/config.json`
- **History**: SQLite database in `~/.lingosnap/history.db`

## Development Setup

### Prerequisites

- Python 3.10+
- Ubuntu 20.04+ (or similar Linux distribution)
- Git

### Setup Development Environment

1. **Clone repository:**
```bash
git clone https://github.com/The-Eleven11/LingoSnap.git
cd LingoSnap
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
pip install -e .  # Install in editable mode
```

4. **Install system dependencies:**
```bash
sudo apt install tesseract-ocr tesseract-ocr-eng
```

5. **Run application:**
```bash
python -m lingosnap
```

### Development Tools

#### Linting and Formatting

```bash
# Install dev tools
pip install flake8 black pylint mypy

# Run linting
flake8 lingosnap/
pylint lingosnap/

# Format code
black lingosnap/
```

#### Type Checking

```bash
mypy lingosnap/
```

#### Testing

```bash
# Install pytest
pip install pytest pytest-qt pytest-cov

# Run tests
pytest tests/

# With coverage
pytest --cov=lingosnap tests/
```

## Adding New Features

### Adding a New Translation Engine

1. Create new engine file in `lingosnap/engines/`:

```python
from lingosnap.engines.base import TranslationEngine

class NewEngine(TranslationEngine):
    def translate(self, text, source_lang, target_lang):
        # Implementation
        pass
    
    # Implement other required methods...
```

2. Register in `MainWindow.__init__()`:

```python
self.new_engine = NewEngine()
```

3. Add to Settings tab dropdown

### Adding UI Translations

1. Add translations to tab's `apply_translations()` method:

```python
def apply_translations(self, lang: str):
    if lang == 'zh':
        self.label.setText('中文文本')
    else:
        self.label.setText('English text')
```

2. Connect to language change signal in parent

### Adding Configuration Options

1. Add default in `Config.DEFAULT_CONFIG`:

```python
DEFAULT_CONFIG = {
    'new_option': 'default_value',
    # ...
}
```

2. Add UI controls in Settings tab
3. Save/load in settings methods

## Code Style Guidelines

### Python Style

Follow PEP 8 with these specifics:

- **Indentation**: 4 spaces
- **Line length**: 88 characters (Black default)
- **Imports**: Grouped (stdlib, third-party, local)
- **Quotes**: Single quotes for strings, double for docstrings
- **Naming**:
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `UPPER_CASE` for constants

### Documentation

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Short description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: Description of when this is raised
    """
    pass
```

### Commit Messages

Format: `<type>: <description>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/config changes

Example:
```
feat: Add support for French language in OCR
fix: Resolve hotkey conflict issue
docs: Update installation instructions
```

## Testing

### Unit Tests

Create tests in `tests/` directory:

```python
import pytest
from lingosnap.engines.google_engine import GoogleTranslateEngine

def test_google_engine_translate():
    engine = GoogleTranslateEngine()
    result = engine.translate("Hello", "en", "es")
    assert result == "Hola"
```

### GUI Tests

Use pytest-qt for GUI testing:

```python
from pytestqt import qtbot
from lingosnap.gui.main_window import MainWindow

def test_main_window(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.isVisible()
```

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_engines.py

# With coverage
pytest --cov=lingosnap --cov-report=html
```

## Building and Packaging

### Python Package

```bash
# Build wheel
python setup.py bdist_wheel

# Install locally
pip install dist/lingosnap-0.1.0-py3-none-any.whl
```

### Debian Package

```bash
# Install build dependencies
sudo apt install debhelper dh-python python3-all python3-setuptools

# Build package
dpkg-buildpackage -us -uc

# Result: ../lingosnap_0.1.0_all.deb
```

### AppImage (Future)

For portable Linux distribution:

```bash
# Install appimage-builder
pip install appimage-builder

# Create AppImage
appimage-builder --recipe appimage.yml
```

## Debugging

### Enable Debug Mode

Add to main.py:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Qt Debug Output

```bash
export QT_DEBUG_PLUGINS=1
python -m lingosnap
```

### Common Issues

**Hotkeys not working:**
- Check permissions
- Verify pynput installation
- Test with sudo (temporary)

**OCR failing:**
- Verify Tesseract: `tesseract --version`
- Check language data: `tesseract --list-langs`

**Translation errors:**
- Check internet connection
- Verify engine availability
- Check console for error messages

## Performance Optimization

### Translation Caching

Consider implementing translation cache:

```python
class CachedEngine(TranslationEngine):
    def __init__(self, engine):
        self.engine = engine
        self.cache = {}
    
    def translate(self, text, source, target):
        key = (text, source, target)
        if key not in self.cache:
            self.cache[key] = self.engine.translate(text, source, target)
        return self.cache[key]
```

### Database Optimization

Add indexes to history table:

```sql
CREATE INDEX idx_timestamp ON history(timestamp DESC);
CREATE INDEX idx_languages ON history(source_lang, target_lang);
```

### Memory Management

- Clear history regularly
- Limit cache size
- Use weak references for large objects

## Contributing

### Workflow

1. Fork the repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Make changes with tests
4. Run linting and tests
5. Commit with clear messages
6. Push and create pull request

### Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] Tests added for new features
- [ ] All tests pass
- [ ] Documentation updated
- [ ] No linting errors
- [ ] Commit messages are clear

### Code Review

Pull requests require:
- Passing CI/CD tests
- Code review approval
- Documentation review
- No merge conflicts

## Release Process

1. Update version in:
   - `setup.py`
   - `lingosnap/__init__.py`
   - `debian/changelog`

2. Update CHANGELOG.md

3. Create git tag:
```bash
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

4. Build packages:
```bash
python setup.py sdist bdist_wheel
dpkg-buildpackage -us -uc
```

5. Create GitHub release with:
   - Release notes
   - Wheel package
   - Debian package
   - Source tarball

## Future Development

### Planned Features

1. **Windows/macOS Support**
   - Platform-specific hotkey handlers
   - Native system tray integration
   - Installers for each platform

2. **Additional Engines**
   - DeepL API integration
   - OpenAI GPT translation
   - Custom API endpoints

3. **Enhanced OCR**
   - Multiple OCR engines
   - Better language detection
   - Handwriting recognition

4. **Cloud Sync**
   - Sync history across devices
   - Cloud configuration backup
   - Multi-device hotkeys

5. **Plugin System**
   - Custom translation engines
   - UI themes
   - Hotkey actions

### Architecture Improvements

- Modular plugin architecture
- Better separation of concerns
- Improved error handling
- Comprehensive logging
- Performance profiling

## Resources

### Documentation

- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [Argos Translate](https://github.com/argosopentech/argos-translate)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

### Tools

- [Qt Designer](https://doc.qt.io/qt-6/qtdesigner-manual.html) - GUI design
- [PyInstaller](https://pyinstaller.org/) - Executable packaging
- [AppImage](https://appimage.org/) - Linux packaging

### Community

- GitHub Issues for bug reports
- GitHub Discussions for questions
- Pull requests welcome

## License

MIT License - see LICENSE file for details

## Contact

- GitHub: https://github.com/The-Eleven11/LingoSnap
- Issues: https://github.com/The-Eleven11/LingoSnap/issues
