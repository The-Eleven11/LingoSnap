"""
Text translation tab
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox,
                             QPushButton, QTextEdit, QLabel)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont


class TextTranslateTab(QWidget):
    """Text translation tab widget"""
    
    translation_completed = pyqtSignal()
    
    def __init__(self, engine, config, history_db):
        super().__init__()
        self.engine = engine
        self.config = config
        self.history_db = history_db
        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.on_typing_timeout)
        self.typing_timer.setSingleShot(True)
        self.is_translating = False
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        
        # Language selection layout
        lang_layout = QHBoxLayout()
        
        # Source language
        self.source_lang_combo = QComboBox()
        lang_layout.addWidget(QLabel('Source:'))
        lang_layout.addWidget(self.source_lang_combo)
        
        # Swap button
        self.swap_button = QPushButton('↔')
        self.swap_button.setMaximumWidth(50)
        self.swap_button.clicked.connect(self.swap_languages)
        lang_layout.addWidget(self.swap_button)
        
        # Target language
        self.target_lang_combo = QComboBox()
        lang_layout.addWidget(QLabel('Target:'))
        lang_layout.addWidget(self.target_lang_combo)
        
        layout.addLayout(lang_layout)
        
        # Text boxes layout with OCR button
        text_layout = QHBoxLayout()
        
        # Source text box container with OCR button
        source_container = QWidget()
        source_layout = QVBoxLayout()
        source_layout.setContentsMargins(0, 0, 0, 0)
        
        self.source_text = QTextEdit()
        self.source_text.setPlaceholderText('Enter text to translate...')
        self.source_text.setFont(QFont('Arial', 12))
        self.source_text.textChanged.connect(self.on_source_text_changed)
        source_layout.addWidget(self.source_text)
        
        # OCR button at bottom right
        ocr_button_layout = QHBoxLayout()
        ocr_button_layout.addStretch()
        self.ocr_button = QPushButton('📷 OCR Screenshot')
        self.ocr_button.setToolTip('Click to capture text from screen (or press Ctrl+F8)')
        self.ocr_button.clicked.connect(self.on_ocr_button_clicked)
        self.ocr_button.setMaximumWidth(150)
        ocr_button_layout.addWidget(self.ocr_button)
        source_layout.addLayout(ocr_button_layout)
        
        source_container.setLayout(source_layout)
        text_layout.addWidget(source_container)
        
        # Target text box
        self.target_text = QTextEdit()
        self.target_text.setPlaceholderText('Translation will appear here...')
        self.target_text.setFont(QFont('Arial', 12))
        self.target_text.setReadOnly(False)
        text_layout.addWidget(self.target_text)
        
        layout.addLayout(text_layout)
        
        # Status label
        self.status_label = QLabel('')
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
        # Load languages
        self.load_languages()
        
        # Sync scrolling
        self.source_text.verticalScrollBar().valueChanged.connect(
            lambda v: self.target_text.verticalScrollBar().setValue(v)
        )
        self.target_text.verticalScrollBar().valueChanged.connect(
            lambda v: self.source_text.verticalScrollBar().setValue(v)
        )
    
    def load_languages(self):
        """Load available languages into combo boxes"""
        self.source_lang_combo.clear()
        self.target_lang_combo.clear()
        
        # Get supported languages from engine
        languages = self.engine.get_supported_languages()
        
        # Add auto-detect option for source
        self.source_lang_combo.addItem('Auto Detect', 'auto')
        
        # Add languages
        for code, name in languages:
            self.source_lang_combo.addItem(name, code)
            self.target_lang_combo.addItem(name, code)
        
        # Set default selections
        default_source = self.config.get('default_source_lang', 'auto')
        default_target = self.config.get('default_target_lang', 'zh-cn')
        
        # Find and set source language
        for i in range(self.source_lang_combo.count()):
            if self.source_lang_combo.itemData(i) == default_source:
                self.source_lang_combo.setCurrentIndex(i)
                break
        
        # Find and set target language
        for i in range(self.target_lang_combo.count()):
            if self.target_lang_combo.itemData(i) == default_target:
                self.target_lang_combo.setCurrentIndex(i)
                break
    
    def on_source_text_changed(self):
        """Handle source text changes"""
        if not self.is_translating:
            # Restart typing timer (2 second delay)
            self.typing_timer.stop()
            self.typing_timer.start(2000)
            self.status_label.setText('Waiting for input...')
    
    def on_typing_timeout(self):
        """Handle typing timeout - trigger translation"""
        self.translate()
    
    def set_source_text(self, text: str, translate_immediately: bool = True):
        """
        Set source text and optionally translate immediately
        
        Args:
            text: Text to set
            translate_immediately: Whether to translate immediately
        """
        self.source_text.setPlainText(text)
        if translate_immediately:
            self.translate()
    
    def translate(self):
        """Perform translation"""
        source_text = self.source_text.toPlainText().strip()
        
        if not source_text:
            self.target_text.clear()
            self.status_label.setText('')
            return
        
        source_lang = self.source_lang_combo.currentData()
        target_lang = self.target_lang_combo.currentData()
        
        if not target_lang:
            self.status_label.setText('Please select a target language')
            return
        
        try:
            self.is_translating = True
            self.status_label.setText('Translating...')
            
            # Perform translation
            translated_text = self.engine.translate(source_text, source_lang, target_lang)
            
            # Update target text
            self.target_text.setPlainText(translated_text)
            self.status_label.setText('Translation complete')
            
            # Save to history
            self.history_db.add_entry(source_lang, target_lang, 
                                     source_text, translated_text)
            
            self.translation_completed.emit()
            
        except Exception as e:
            self.status_label.setText(f'Translation failed: {str(e)}')
        finally:
            self.is_translating = False
    
    def swap_languages(self):
        """Swap source and target languages"""
        source_index = self.source_lang_combo.currentIndex()
        target_index = self.target_lang_combo.currentIndex()
        
        # Don't swap if source is auto-detect
        if self.source_lang_combo.currentData() == 'auto':
            return
        
        self.source_lang_combo.setCurrentIndex(target_index)
        self.target_lang_combo.setCurrentIndex(source_index)
        
        # Also swap text
        source_text = self.source_text.toPlainText()
        target_text = self.target_text.toPlainText()
        
        self.source_text.setPlainText(target_text)
        self.target_text.setPlainText(source_text)
    
    def set_engine(self, engine):
        """
        Set translation engine
        
        Args:
            engine: Translation engine instance
        """
        self.engine = engine
        self.load_languages()
    
    def on_ocr_button_clicked(self):
        """Handle OCR button click"""
        # Trigger the same action as Ctrl+F8 hotkey
        # Get the main window to trigger screenshot
        main_window = self.window()
        if hasattr(main_window, 'on_ocr_capture'):
            main_window.on_ocr_capture()
    
    def apply_translations(self, lang: str):
        """Apply UI translations"""
        if lang == 'zh':
            self.source_text.setPlaceholderText('输入要翻译的文本...')
            self.target_text.setPlaceholderText('翻译结果将显示在这里...')
            self.ocr_button.setText('📷 OCR截图')
            self.ocr_button.setToolTip('点击从屏幕捕获文本（或按 Ctrl+F8）')
        else:
            self.source_text.setPlaceholderText('Enter text to translate...')
            self.target_text.setPlaceholderText('Translation will appear here...')
            self.ocr_button.setText('📷 OCR Screenshot')
            self.ocr_button.setToolTip('Click to capture text from screen (or press Ctrl+F8)')
