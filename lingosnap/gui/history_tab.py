"""
History tab
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QScrollArea, QFrame,
                             QLabel, QPushButton, QHBoxLayout)
from PyQt6.QtCore import Qt
from datetime import datetime


class HistoryCard(QFrame):
    """Card widget for displaying a history entry"""
    
    def __init__(self, entry, parent=None):
        super().__init__(parent)
        self.entry = entry
        self.init_ui()
    
    def init_ui(self):
        """Initialize card UI"""
        layout = QVBoxLayout()
        
        # Timestamp and language pair
        header_layout = QHBoxLayout()
        
        # Parse timestamp
        try:
            dt = datetime.fromisoformat(self.entry['timestamp'])
            timestamp_str = dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            timestamp_str = self.entry['timestamp']
        
        timestamp_label = QLabel(timestamp_str)
        timestamp_label.setStyleSheet('color: gray; font-size: 10px;')
        header_layout.addWidget(timestamp_label)
        
        lang_pair = QLabel(f"{self.entry['source_lang']} → {self.entry['target_lang']}")
        lang_pair.setStyleSheet('color: gray; font-size: 10px;')
        header_layout.addWidget(lang_pair)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Source text preview
        source_preview = self.entry['source_text'][:100]
        if len(self.entry['source_text']) > 100:
            source_preview += '...'
        
        source_label = QLabel(source_preview)
        source_label.setWordWrap(True)
        source_label.setStyleSheet('font-weight: bold;')
        layout.addWidget(source_label)
        
        # Target text preview
        target_preview = self.entry['translated_text'][:100]
        if len(self.entry['translated_text']) > 100:
            target_preview += '...'
        
        target_label = QLabel(target_preview)
        target_label.setWordWrap(True)
        layout.addWidget(target_label)
        
        self.setLayout(layout)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Style
        self.setStyleSheet('''
            HistoryCard {
                background-color: #f0f0f0;
                border-radius: 5px;
                padding: 10px;
            }
            HistoryCard:hover {
                background-color: #e0e0e0;
            }
        ''')
    
    def mousePressEvent(self, event):
        """Handle mouse click"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Emit signal or call parent method
            parent = self.parent()
            while parent and not isinstance(parent, HistoryTab):
                parent = parent.parent()
            if parent:
                parent.on_card_clicked(self.entry)


class HistoryTab(QWidget):
    """History tab widget"""
    
    def __init__(self, history_db, text_translate_tab):
        super().__init__()
        self.history_db = history_db
        self.text_translate_tab = text_translate_tab
        self.init_ui()
        self.load_history()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        
        # Header with refresh button
        header_layout = QHBoxLayout()
        title_label = QLabel('Translation History')
        title_label.setStyleSheet('font-size: 16px; font-weight: bold;')
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        self.refresh_button = QPushButton('Refresh')
        self.refresh_button.clicked.connect(self.load_history)
        header_layout.addWidget(self.refresh_button)
        
        self.clear_button = QPushButton('Clear All')
        self.clear_button.clicked.connect(self.clear_history)
        header_layout.addWidget(self.clear_button)
        
        layout.addLayout(header_layout)
        
        # Scroll area for history cards
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_widget.setLayout(self.scroll_layout)
        
        scroll_area.setWidget(self.scroll_widget)
        layout.addWidget(scroll_area)
        
        self.setLayout(layout)
    
    def load_history(self):
        """Load history from database"""
        # Clear existing cards
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Get history from database
        history_limit = 100  # Could be configurable
        entries = self.history_db.get_history(history_limit)
        
        # Create cards
        for entry in entries:
            card = HistoryCard(entry)
            self.scroll_layout.addWidget(card)
        
        # Add empty state if no history
        if not entries:
            empty_label = QLabel('No translation history yet')
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setStyleSheet('color: gray; font-size: 14px; padding: 50px;')
            self.scroll_layout.addWidget(empty_label)
    
    def on_card_clicked(self, entry):
        """Handle card click - restore translation session"""
        # Switch to Text Translate tab
        main_window = self.window()
        if hasattr(main_window, 'tab_widget'):
            main_window.tab_widget.setCurrentIndex(0)
        
        # Set text in translate tab
        self.text_translate_tab.source_text.setPlainText(entry['source_text'])
        self.text_translate_tab.target_text.setPlainText(entry['translated_text'])
        
        # Set language selections
        source_lang = entry['source_lang']
        target_lang = entry['target_lang']
        
        # Find and set source language
        for i in range(self.text_translate_tab.source_lang_combo.count()):
            if self.text_translate_tab.source_lang_combo.itemData(i) == source_lang:
                self.text_translate_tab.source_lang_combo.setCurrentIndex(i)
                break
        
        # Find and set target language
        for i in range(self.text_translate_tab.target_lang_combo.count()):
            if self.text_translate_tab.target_lang_combo.itemData(i) == target_lang:
                self.text_translate_tab.target_lang_combo.setCurrentIndex(i)
                break
    
    def clear_history(self):
        """Clear all history"""
        self.history_db.clear_history()
        self.load_history()
    
    def apply_translations(self, lang: str):
        """Apply UI translations"""
        if lang == 'zh':
            self.refresh_button.setText('刷新')
            self.clear_button.setText('清空全部')
        else:
            self.refresh_button.setText('Refresh')
            self.clear_button.setText('Clear All')
