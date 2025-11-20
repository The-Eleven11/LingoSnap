"""
Global hotkey manager
"""

from PyQt6.QtCore import QObject, pyqtSignal, QThread
from pynput import keyboard
import time
import sys


class HotkeyListener(QThread):
    """Thread for listening to global hotkeys"""
    
    text_capture = pyqtSignal()
    ocr_capture = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.running = True  # Start as True so listener runs
        self.ctrl_pressed = False
        self.c_press_count = 0
        self.last_c_press_time = 0
        self.listener = None
    
    def run(self):
        """Run the hotkey listener"""
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
                            print("DEBUG: Ctrl+C+C detected, triggering text capture", file=sys.stderr)
                            self.text_capture.emit()
                            self.c_press_count = 0
                    else:
                        self.c_press_count = 1
                    self.last_c_press_time = current_time
                
                # Check for Ctrl+F8
                if self.ctrl_pressed and key == keyboard.Key.f8:
                    print("DEBUG: Ctrl+F8 detected, triggering OCR capture", file=sys.stderr)
                    self.ocr_capture.emit()
                
            except AttributeError:
                pass
            except Exception as e:
                print(f"ERROR in hotkey listener on_press: {e}", file=sys.stderr)
                self.error_occurred.emit(str(e))
        
        def on_release(key):
            try:
                if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                    self.ctrl_pressed = False
                    self.c_press_count = 0
            except AttributeError:
                pass
            except Exception as e:
                print(f"ERROR in hotkey listener on_release: {e}", file=sys.stderr)
        
        # Start listener
        try:
            print("Starting hotkey listener...", file=sys.stderr)
            self.listener = keyboard.Listener(on_press=on_press, on_release=on_release)
            self.listener.start()
            print("Hotkey listener started successfully", file=sys.stderr)
            
            # Keep the thread alive while running
            while self.running:
                time.sleep(0.1)
            
            # Stop listener when running becomes False
            if self.listener:
                self.listener.stop()
            print("Hotkey listener stopped.", file=sys.stderr)
            
        except Exception as e:
            error_msg = f"Failed to start hotkey listener: {e}"
            print(f"ERROR: {error_msg}", file=sys.stderr)
            self.error_occurred.emit(error_msg)
    
    def stop(self):
        """Stop the listener"""
        self.running = False
        if self.listener:
            self.listener.stop()


class HotkeyManager(QObject):
    """Manager for global hotkeys"""
    
    text_capture_triggered = pyqtSignal()
    ocr_capture_triggered = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.listener = HotkeyListener()
        self.listener.text_capture.connect(self.text_capture_triggered.emit)
        self.listener.ocr_capture.connect(self.ocr_capture_triggered.emit)
        self.listener.error_occurred.connect(self.on_error)
    
    def on_error(self, error_msg):
        """Handle hotkey listener errors"""
        print(f"Hotkey manager error: {error_msg}", file=sys.stderr)
    
    def start(self):
        """Start listening for hotkeys"""
        try:
            self.listener.start()
            print("Hotkey manager started successfully", file=sys.stderr)
        except Exception as e:
            print(f"Failed to start hotkey manager: {e}", file=sys.stderr)
    
    def stop(self):
        """Stop listening for hotkeys"""
        self.listener.stop()
        self.listener.wait()
