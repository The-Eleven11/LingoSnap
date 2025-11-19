"""
Global hotkey manager
"""

from PyQt6.QtCore import QObject, pyqtSignal, QThread
from pynput import keyboard
import time


class HotkeyListener(QThread):
    """Thread for listening to global hotkeys"""
    
    text_capture = pyqtSignal()
    ocr_capture = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.running = False
        self.ctrl_pressed = False
        self.c_press_count = 0
        self.last_c_press_time = 0
    
    def run(self):
        """Run the hotkey listener"""
        self.running = True
        
        def on_press(key):
            try:
                # Track Ctrl key
                if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                    self.ctrl_pressed = True
                
                # Check for Ctrl+C+C (double C press)
                if self.ctrl_pressed and hasattr(key, 'char') and key.char == 'c':
                    current_time = time.time()
                    if current_time - self.last_c_press_time < 0.5:  # 500ms window
                        self.c_press_count += 1
                        if self.c_press_count >= 2:
                            self.text_capture.emit()
                            self.c_press_count = 0
                    else:
                        self.c_press_count = 1
                    self.last_c_press_time = current_time
                
                # Check for Ctrl+F8
                if self.ctrl_pressed and key == keyboard.Key.f8:
                    self.ocr_capture.emit()
                
            except AttributeError:
                pass
        
        def on_release(key):
            try:
                if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                    self.ctrl_pressed = False
                    self.c_press_count = 0
            except AttributeError:
                pass
        
        # Start listener
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            while self.running:
                time.sleep(0.1)
            listener.stop()
    
    def stop(self):
        """Stop the listener"""
        self.running = False


class HotkeyManager(QObject):
    """Manager for global hotkeys"""
    
    text_capture_triggered = pyqtSignal()
    ocr_capture_triggered = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.listener = HotkeyListener()
        self.listener.text_capture.connect(self.text_capture_triggered.emit)
        self.listener.ocr_capture.connect(self.ocr_capture_triggered.emit)
    
    def start(self):
        """Start listening for hotkeys"""
        self.listener.start()
    
    def stop(self):
        """Stop listening for hotkeys"""
        self.listener.stop()
        self.listener.wait()
