"""
Settings tab
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QComboBox, QLineEdit, QPushButton, QGroupBox,
                             QListWidget, QMessageBox, QFormLayout)
from PyQt6.QtCore import pyqtSignal


class SettingsTab(QWidget):
    """Settings tab widget"""
    
    engine_changed = pyqtSignal(str)
    language_changed = pyqtSignal()
    
    def __init__(self, config, google_engine, argos_engine, main_window):
        super().__init__()
        self.config = config
        self.google_engine = google_engine
        self.argos_engine = argos_engine
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        
        # Engine selection
        engine_group = QGroupBox('Translation Engine')
        engine_layout = QVBoxLayout()
        
        self.engine_combo = QComboBox()
        self.engine_combo.addItem('Google Translate', 'google')
        self.engine_combo.addItem('Argos Translate (Offline)', 'argos')
        self.engine_combo.currentIndexChanged.connect(self.on_engine_changed)
        engine_layout.addWidget(self.engine_combo)
        
        engine_group.setLayout(engine_layout)
        layout.addWidget(engine_group)
        
        # Google Translate settings
        self.google_group = QGroupBox('Google Translate Settings')
        google_layout = QFormLayout()
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText('Enter API Key (optional)')
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        google_layout.addRow('API Key:', self.api_key_input)
        
        self.char_count_label = QLabel('0 characters')
        google_layout.addRow('Usage:', self.char_count_label)
        
        self.reset_count_button = QPushButton('Reset Counter')
        self.reset_count_button.clicked.connect(self.reset_google_counter)
        google_layout.addRow('', self.reset_count_button)
        
        self.google_group.setLayout(google_layout)
        layout.addWidget(self.google_group)
        
        # Argos Translate settings
        self.argos_group = QGroupBox('Argos Translate Settings')
        argos_layout = QVBoxLayout()
        
        argos_layout.addWidget(QLabel('Installed Language Packages:'))
        self.package_list = QListWidget()
        argos_layout.addWidget(self.package_list)
        
        self.refresh_packages_button = QPushButton('Refresh Packages')
        self.refresh_packages_button.clicked.connect(self.refresh_argos_packages)
        argos_layout.addWidget(self.refresh_packages_button)
        
        self.argos_group.setLayout(argos_layout)
        layout.addWidget(self.argos_group)
        
        # Hotkey settings
        hotkey_group = QGroupBox('Hotkey Settings')
        hotkey_layout = QFormLayout()
        
        self.text_capture_input = QLineEdit()
        hotkey_layout.addRow('Text Capture:', self.text_capture_input)
        
        self.ocr_capture_input = QLineEdit()
        hotkey_layout.addRow('OCR Capture:', self.ocr_capture_input)
        
        hotkey_group.setLayout(hotkey_layout)
        layout.addWidget(hotkey_group)
        
        # UI Language
        ui_group = QGroupBox('UI Language')
        ui_layout = QHBoxLayout()
        
        self.ui_lang_combo = QComboBox()
        self.ui_lang_combo.addItem('English', 'en')
        self.ui_lang_combo.addItem('中文', 'zh')
        self.ui_lang_combo.currentIndexChanged.connect(self.on_ui_language_changed)
        ui_layout.addWidget(self.ui_lang_combo)
        
        ui_group.setLayout(ui_layout)
        layout.addWidget(ui_group)
        
        # Terminal default language
        terminal_group = QGroupBox('Terminal Default Target Language')
        terminal_layout = QHBoxLayout()
        
        self.terminal_lang_combo = QComboBox()
        terminal_layout.addWidget(self.terminal_lang_combo)
        
        terminal_group.setLayout(terminal_layout)
        layout.addWidget(terminal_group)
        
        # Save button
        save_button = QPushButton('Save Settings')
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)
        
        # About section
        about_group = QGroupBox('About')
        about_layout = QVBoxLayout()
        about_layout.addWidget(QLabel('LingoSnap - Instant translation at your fingertips'))
        about_layout.addWidget(QLabel('Version: 0.1.0'))
        
        github_link = QLabel('<a href="https://github.com/The-Eleven11/LingoSnap">GitHub Repository</a>')
        github_link.setOpenExternalLinks(True)
        about_layout.addWidget(github_link)
        
        about_group.setLayout(about_layout)
        layout.addWidget(about_group)
        
        layout.addStretch()
        self.setLayout(layout)
        
        # Load current settings
        self.load_settings()
    
    def load_settings(self):
        """Load settings from config"""
        # Engine
        engine = self.config.get('engine', 'google')
        index = self.engine_combo.findData(engine)
        if index >= 0:
            self.engine_combo.setCurrentIndex(index)
        
        # API Key
        api_key = self.config.get('google_api_key', '')
        self.api_key_input.setText(api_key)
        
        # Character count
        char_count = self.google_engine.get_character_count()
        self.char_count_label.setText(f'{char_count} characters')
        
        # Hotkeys
        text_hotkey = self.config.get('text_capture_hotkey', 'ctrl+c+c')
        self.text_capture_input.setText(text_hotkey)
        
        ocr_hotkey = self.config.get('ocr_capture_hotkey', 'ctrl+f8')
        self.ocr_capture_input.setText(ocr_hotkey)
        
        # UI Language
        ui_lang = self.config.get('ui_language', 'en')
        index = self.ui_lang_combo.findData(ui_lang)
        if index >= 0:
            self.ui_lang_combo.setCurrentIndex(index)
        
        # Terminal default language
        self.load_terminal_languages()
        terminal_lang = self.config.get('terminal_default_target', 'zh')
        for i in range(self.terminal_lang_combo.count()):
            if self.terminal_lang_combo.itemData(i) == terminal_lang:
                self.terminal_lang_combo.setCurrentIndex(i)
                break
        
        # Refresh Argos packages
        self.refresh_argos_packages()
        
        # Update engine-specific groups
        self.update_engine_groups()
    
    def load_terminal_languages(self):
        """Load languages for terminal default"""
        self.terminal_lang_combo.clear()
        
        # Get current engine
        engine = self.google_engine if self.config.get('engine') == 'google' else self.argos_engine
        languages = engine.get_supported_languages()
        
        for code, name in languages:
            if code != 'auto':
                self.terminal_lang_combo.addItem(name, code)
    
    def save_settings(self):
        """Save settings to config"""
        # Engine
        engine = self.engine_combo.currentData()
        self.config.set('engine', engine)
        
        # API Key
        api_key = self.api_key_input.text()
        self.config.set('google_api_key', api_key)
        
        # Hotkeys
        text_hotkey = self.text_capture_input.text()
        self.config.set('text_capture_hotkey', text_hotkey)
        
        ocr_hotkey = self.ocr_capture_input.text()
        self.config.set('ocr_capture_hotkey', ocr_hotkey)
        
        # UI Language
        ui_lang = self.ui_lang_combo.currentData()
        self.config.set('ui_language', ui_lang)
        
        # Terminal default language
        terminal_lang = self.terminal_lang_combo.currentData()
        if terminal_lang:
            self.config.set('terminal_default_target', terminal_lang)
        
        QMessageBox.information(self, 'Settings Saved', 
                               'Settings have been saved successfully.')
    
    def on_engine_changed(self):
        """Handle engine change"""
        engine_type = self.engine_combo.currentData()
        self.update_engine_groups()
        self.load_terminal_languages()
        self.engine_changed.emit(engine_type)
    
    def update_engine_groups(self):
        """Update engine-specific group enabled states"""
        engine = self.engine_combo.currentData()
        
        # Enable/disable based on selected engine
        self.google_group.setEnabled(engine == 'google')
        self.argos_group.setEnabled(engine == 'argos')
    
    def reset_google_counter(self):
        """Reset Google Translate character counter"""
        self.google_engine.reset_character_count()
        self.char_count_label.setText('0 characters')
        QMessageBox.information(self, 'Counter Reset', 
                               'Character counter has been reset.')
    
    def refresh_argos_packages(self):
        """Refresh Argos package list"""
        self.package_list.clear()
        
        if self.argos_engine.is_available():
            packages = self.argos_engine.get_installed_packages()
            for pkg in packages:
                item_text = f"{pkg['from_name']} → {pkg['to_name']} (v{pkg['package_version']})"
                self.package_list.addItem(item_text)
        else:
            self.package_list.addItem('No packages installed')
    
    def on_ui_language_changed(self):
        """Handle UI language change"""
        self.language_changed.emit()
    
    def apply_translations(self, lang: str):
        """Apply UI translations"""
        if lang == 'zh':
            self.refresh_packages_button.setText('刷新语言包')
        else:
            self.refresh_packages_button.setText('Refresh Packages')
