"""
Main application window with system tray
"""

from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QSystemTrayIcon, 
                             QMenu, QApplication, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QAction, QCloseEvent
from lingosnap.gui.text_translate_tab import TextTranslateTab
from lingosnap.gui.history_tab import HistoryTab
from lingosnap.gui.settings_tab import SettingsTab
from lingosnap.utils.config import Config
from lingosnap.utils.history import HistoryDatabase
from lingosnap.engines.google_engine import GoogleTranslateEngine
from lingosnap.engines.argos_engine import ArgosTranslateEngine
from lingosnap.gui.hotkey_manager import HotkeyManager
from lingosnap.gui.screenshot_tool import ScreenshotTool
from lingosnap.utils.ocr import OCREngine


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize configuration and database
        self.config = Config()
        self.history_db = HistoryDatabase()
        
        # Initialize engines
        self.google_engine = GoogleTranslateEngine()
        self.argos_engine = ArgosTranslateEngine()
        self.ocr_engine = OCREngine()
        
        # Get current engine
        engine_type = self.config.get('engine', 'google')
        self.current_engine = (self.google_engine if engine_type == 'google' 
                              else self.argos_engine)
        
        # Initialize UI
        self.init_ui()
        
        # Initialize system tray
        self.init_tray()
        
        # Initialize hotkey manager
        self.init_hotkeys()
        
        # Apply translations
        self.apply_translations()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle('LingoSnap')
        self.setGeometry(100, 100, 900, 600)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
        # Create tabs
        self.text_translate_tab = TextTranslateTab(
            self.current_engine, 
            self.config, 
            self.history_db
        )
        self.history_tab = HistoryTab(self.history_db, self.text_translate_tab)
        self.settings_tab = SettingsTab(
            self.config,
            self.google_engine,
            self.argos_engine,
            self
        )
        
        # Add tabs
        self.tab_widget.addTab(self.text_translate_tab, 'Text Translate')
        self.tab_widget.addTab(self.history_tab, 'History')
        self.tab_widget.addTab(self.settings_tab, 'Settings')
        
        # Connect signals
        self.settings_tab.engine_changed.connect(self.on_engine_changed)
        self.settings_tab.language_changed.connect(self.apply_translations)
    
    def init_tray(self):
        """Initialize system tray icon"""
        self.tray_icon = QSystemTrayIcon(self)
        
        # Create tray icon (use default icon for now)
        self.tray_icon.setIcon(self.style().standardIcon(
            self.style().StandardPixmap.SP_ComputerIcon
        ))
        
        # Create tray menu
        tray_menu = QMenu()
        
        show_action = QAction('Show', self)
        show_action.triggered.connect(self.show_window)
        tray_menu.addAction(show_action)
        
        quit_action = QAction('Quit', self)
        quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        
        # Show tray icon
        self.tray_icon.show()
    
    def init_hotkeys(self):
        """Initialize global hotkeys"""
        self.hotkey_manager = HotkeyManager(self)
        self.screenshot_tool = ScreenshotTool(self)
        
        # Connect hotkey callbacks
        self.hotkey_manager.text_capture_triggered.connect(self.on_text_capture)
        self.hotkey_manager.ocr_capture_triggered.connect(self.on_ocr_capture)
        
        # Start hotkey monitoring
        self.hotkey_manager.start()
    
    def on_text_capture(self):
        """Handle text capture hotkey"""
        # Get text from clipboard
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        
        if text:
            # Show window and populate text
            self.show_window()
            self.tab_widget.setCurrentIndex(0)  # Switch to Text Translate tab
            self.text_translate_tab.set_source_text(text)
    
    def on_ocr_capture(self):
        """Handle OCR capture hotkey"""
        # Show screenshot tool
        self.screenshot_tool.capture(self.on_screenshot_captured)
    
    def on_screenshot_captured(self, image):
        """Handle screenshot captured"""
        if image:
            try:
                # Perform OCR
                text = self.ocr_engine.extract_text(image)
                
                if text:
                    # Show window and populate text
                    self.show_window()
                    self.tab_widget.setCurrentIndex(0)
                    self.text_translate_tab.set_source_text(text)
                else:
                    QMessageBox.warning(self, 'OCR Failed', 
                                       'No text found in the captured image.')
            except Exception as e:
                QMessageBox.critical(self, 'OCR Error', 
                                    f'Failed to extract text: {str(e)}')
    
    def on_engine_changed(self, engine_type: str):
        """Handle engine change"""
        self.current_engine = (self.google_engine if engine_type == 'google' 
                              else self.argos_engine)
        self.text_translate_tab.set_engine(self.current_engine)
    
    def apply_translations(self):
        """Apply UI language translations"""
        ui_lang = self.config.get('ui_language', 'en')
        
        if ui_lang == 'zh':
            # Chinese translations
            self.setWindowTitle('LingoSnap')
            self.tab_widget.setTabText(0, '文本翻译')
            self.tab_widget.setTabText(1, '历史记录')
            self.tab_widget.setTabText(2, '设置')
        else:
            # English translations
            self.setWindowTitle('LingoSnap')
            self.tab_widget.setTabText(0, 'Text Translate')
            self.tab_widget.setTabText(1, 'History')
            self.tab_widget.setTabText(2, 'Settings')
        
        # Update tab translations
        self.text_translate_tab.apply_translations(ui_lang)
        self.history_tab.apply_translations(ui_lang)
        self.settings_tab.apply_translations(ui_lang)
    
    def show_window(self):
        """Show and raise the main window"""
        self.show()
        self.raise_()
        self.activateWindow()
    
    def on_tray_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.show_window()
    
    def closeEvent(self, event: QCloseEvent):
        """Handle window close event"""
        # Hide window instead of closing
        event.ignore()
        self.hide()
        
        # Show notification
        self.tray_icon.showMessage(
            'LingoSnap',
            'Application minimized to system tray',
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )
    
    def quit_application(self):
        """Quit the application"""
        # Stop hotkey manager
        self.hotkey_manager.stop()
        
        # Quit application
        QApplication.quit()
