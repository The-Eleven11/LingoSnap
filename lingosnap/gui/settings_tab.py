"""
Settings tab
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QComboBox, QLineEdit, QPushButton, QGroupBox,
                             QListWidget, QMessageBox, QFormLayout, QDialog,
                             QDialogButtonBox, QProgressDialog)
from PyQt6.QtCore import pyqtSignal, Qt, QTimer


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
        
        # Buttons layout
        argos_buttons_layout = QHBoxLayout()
        
        self.refresh_packages_button = QPushButton('Refresh Packages')
        self.refresh_packages_button.clicked.connect(self.refresh_argos_packages)
        argos_buttons_layout.addWidget(self.refresh_packages_button)
        
        self.install_package_button = QPushButton('Install Package')
        self.install_package_button.clicked.connect(self.show_install_package_dialog)
        argos_buttons_layout.addWidget(self.install_package_button)
        
        argos_layout.addLayout(argos_buttons_layout)
        
        # Installation instructions
        install_note = QLabel(
            'Note: Installing packages requires internet connection and may take a few minutes. '
            'Common packages: English↔Chinese, English↔Spanish, English↔French, etc.'
        )
        install_note.setWordWrap(True)
        install_note.setStyleSheet('color: gray; font-size: 10px;')
        argos_layout.addWidget(install_note)
        
        self.argos_group.setLayout(argos_layout)
        layout.addWidget(self.argos_group)
        
        # Hotkey settings
        hotkey_group = QGroupBox('Hotkey Settings')
        hotkey_layout = QFormLayout()
        
        self.text_capture_input = QLineEdit()
        self.text_capture_input.setReadOnly(True)
        hotkey_layout.addRow('Text Capture:', self.text_capture_input)
        
        self.ocr_capture_input = QLineEdit()
        self.ocr_capture_input.setReadOnly(True)
        hotkey_layout.addRow('OCR Capture:', self.ocr_capture_input)
        
        # Test button
        self.test_hotkey_button = QPushButton('Test Hotkeys')
        self.test_hotkey_button.clicked.connect(self.test_hotkeys)
        hotkey_layout.addRow('', self.test_hotkey_button)
        
        # Hotkey status
        self.hotkey_status_label = QLabel('Status: Waiting to test...')
        self.hotkey_status_label.setWordWrap(True)
        self.hotkey_status_label.setStyleSheet('color: gray; font-size: 10px;')
        hotkey_layout.addRow('', self.hotkey_status_label)
        
        hotkey_note = QLabel(
            'Note: Hotkeys may require appropriate permissions on Linux. '
            'If hotkeys don\'t work, try running the application with appropriate permissions.'
        )
        hotkey_note.setWordWrap(True)
        hotkey_note.setStyleSheet('color: gray; font-size: 10px;')
        hotkey_layout.addRow('', hotkey_note)
        
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
            if packages:
                for pkg in packages:
                    item_text = f"{pkg['from_name']} → {pkg['to_name']} (v{pkg['package_version']})"
                    self.package_list.addItem(item_text)
            else:
                self.package_list.addItem('No packages installed - Click "Install Package" to add')
        else:
            self.package_list.addItem('Argos Translate not available - install with: pip install argostranslate')
    
    def show_install_package_dialog(self):
        """Show dialog to install new language packages"""
        dialog = PackageInstallDialog(self.argos_engine, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Refresh package list after installation
            self.refresh_argos_packages()
            # Reload languages in translation tab
            if hasattr(self.main_window, 'text_translate_tab'):
                self.main_window.text_translate_tab.load_languages()
    
    def test_hotkeys(self):
        """Test hotkey functionality"""
        self.hotkey_status_label.setText(
            'Testing hotkeys...\n'
            '1. Try pressing Ctrl+C+C (hold Ctrl, press C twice quickly)\n'
            '2. Try pressing Ctrl+F8\n'
            'Check if the main window appears or screenshot tool activates.'
        )
        
        # Show info about hotkey status
        if hasattr(self.main_window, 'hotkey_manager'):
            if self.main_window.hotkey_manager.listener.isRunning():
                self.hotkey_status_label.setText(
                    self.hotkey_status_label.text() + '\n\n✓ Hotkey listener is running.'
                )
            else:
                self.hotkey_status_label.setText(
                    self.hotkey_status_label.text() + '\n\n✗ Hotkey listener is NOT running.'
                )
                QMessageBox.warning(
                    self,
                    'Hotkey Error',
                    'Hotkey listener is not running. The application may need to be restarted '
                    'or may require additional permissions.'
                )
        
        QMessageBox.information(
            self,
            'Test Hotkeys',
            'Hotkey monitoring is active.\n\n'
            'Try the following:\n'
            '1. Select some text anywhere on your screen\n'
            '2. Press Ctrl+C+C (hold Ctrl, quickly press C twice)\n'
            '3. The LingoSnap window should appear with the selected text\n\n'
            'Or:\n'
            '1. Press Ctrl+F8\n'
            '2. A screenshot overlay should appear\n\n'
            'Note: On Linux, hotkeys may require appropriate permissions. '
            'If they don\'t work, try running from terminal to see any error messages.'
        )
    
    def on_ui_language_changed(self):
        """Handle UI language change"""
        self.language_changed.emit()
    
    def apply_translations(self, lang: str):
        """Apply UI translations"""
        if lang == 'zh':
            self.refresh_packages_button.setText('刷新语言包')
            self.install_package_button.setText('安装语言包')
        else:
            self.refresh_packages_button.setText('Refresh Packages')
            self.install_package_button.setText('Install Package')


class PackageInstallDialog(QDialog):
    """Dialog for installing Argos Translate language packages"""
    
    def __init__(self, argos_engine, parent=None):
        super().__init__(parent)
        self.argos_engine = argos_engine
        self.setWindowTitle('Install Language Package')
        self.setMinimumWidth(500)
        self.init_ui()
        self.load_available_packages()
    
    def init_ui(self):
        """Initialize dialog UI"""
        layout = QVBoxLayout()
        
        # Instructions
        instructions = QLabel(
            'Select a language package to install. This will download and install '
            'the translation model for offline use.'
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Available packages list
        layout.addWidget(QLabel('Available Packages:'))
        self.available_list = QListWidget()
        self.available_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        layout.addWidget(self.available_list)
        
        # Status label
        self.status_label = QLabel('')
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.install_selected_package)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def load_available_packages(self):
        """Load available packages from Argos"""
        self.status_label.setText('Loading available packages...')
        QTimer.singleShot(100, self._load_packages_async)
    
    def _load_packages_async(self):
        """Load packages asynchronously"""
        try:
            packages = self.argos_engine.get_available_packages()
            
            if not packages:
                self.status_label.setText(
                    'No packages available. Please check your internet connection '
                    'or ensure Argos Translate is properly installed.'
                )
                return
            
            # Get installed packages to mark them
            installed = self.argos_engine.get_installed_packages()
            installed_pairs = {(p['from_code'], p['to_code']) for p in installed}
            
            # Add packages to list
            for pkg in packages:
                from_lang = pkg['from_name']
                to_lang = pkg['to_name']
                from_code = pkg['from_code']
                to_code = pkg['to_code']
                version = pkg['package_version']
                
                # Check if already installed
                is_installed = (from_code, to_code) in installed_pairs
                status = ' (Installed)' if is_installed else ''
                
                item_text = f"{from_lang} → {to_lang} (v{version}){status}"
                item = self.available_list.addItem(item_text)
                
                # Store package info in item data
                self.available_list.item(
                    self.available_list.count() - 1
                ).setData(Qt.ItemDataRole.UserRole, pkg)
            
            self.status_label.setText(
                f'Found {len(packages)} available packages. Select one to install.'
            )
            
        except Exception as e:
            self.status_label.setText(f'Error loading packages: {str(e)}')
    
    def install_selected_package(self):
        """Install the selected package"""
        selected_items = self.available_list.selectedItems()
        
        if not selected_items:
            QMessageBox.warning(
                self,
                'No Selection',
                'Please select a package to install.'
            )
            return
        
        # Get package info
        pkg = selected_items[0].data(Qt.ItemDataRole.UserRole)
        
        # Show progress dialog
        progress = QProgressDialog(
            f"Installing {pkg['from_name']} → {pkg['to_name']}...\n"
            "This may take a few minutes.",
            None,
            0,
            0,
            self
        )
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setWindowTitle('Installing Package')
        progress.setCancelButton(None)
        progress.show()
        
        # Install package
        QTimer.singleShot(100, lambda: self._install_package_async(pkg, progress))
    
    def _install_package_async(self, pkg, progress):
        """Install package asynchronously"""
        try:
            success = self.argos_engine.install_package(
                pkg['from_code'],
                pkg['to_code']
            )
            
            progress.close()
            
            if success:
                QMessageBox.information(
                    self,
                    'Installation Complete',
                    f"Successfully installed {pkg['from_name']} → {pkg['to_name']}\n\n"
                    "You can now use this language pair for offline translation."
                )
                self.accept()
            else:
                QMessageBox.critical(
                    self,
                    'Installation Failed',
                    f"Failed to install {pkg['from_name']} → {pkg['to_name']}\n\n"
                    "Please check your internet connection and try again."
                )
        except Exception as e:
            progress.close()
            QMessageBox.critical(
                self,
                'Installation Error',
                f"Error installing package: {str(e)}"
            )
