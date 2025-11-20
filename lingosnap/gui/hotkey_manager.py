"""
Global hotkey manager with enhanced compatibility
"""

from PyQt6.QtCore import QObject, pyqtSignal, QThread
import time
import sys
import subprocess
import os


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
        self.method = None  # Will be set to 'pynput', 'xcape', or 'polling'
    
    def run(self):
        """Run the hotkey listener"""
        # Try pynput first
        if self._try_pynput():
            return
        
        # If pynput doesn't work, try alternative methods
        print("WARNING: pynput method failed, hotkeys may not be available", file=sys.stderr)
        print("RECOMMENDATION: Use the OCR button in the GUI instead of hotkeys", file=sys.stderr)
        
        # Keep thread alive but inactive
        while self.running:
            time.sleep(1)
    
    def _try_pynput(self):
        """Try to use pynput for hotkeys"""
        try:
            from pynput import keyboard
            self.method = 'pynput'
            
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
            print("Starting hotkey listener with pynput...", file=sys.stderr)
            self.listener = keyboard.Listener(
                on_press=on_press, 
                on_release=on_release,
                suppress=False  # Don't suppress keys to avoid interfering with system
            )
            self.listener.start()
            
            # Wait a bit to see if it starts successfully
            time.sleep(0.2)
            
            if not self.listener.is_alive():
                print("ERROR: pynput listener failed to start", file=sys.stderr)
                return False
            
            print("Hotkey listener started successfully with pynput", file=sys.stderr)
            
            # Keep the thread alive while running
            while self.running and self.listener.is_alive():
                time.sleep(0.1)
            
            # Stop listener when running becomes False
            if self.listener:
                self.listener.stop()
            print("Hotkey listener stopped.", file=sys.stderr)
            return True
            
        except ImportError as e:
            print(f"WARNING: pynput not available: {e}", file=sys.stderr)
            return False
        except Exception as e:
            error_msg = f"Failed to start pynput listener: {e}"
            print(f"ERROR: {error_msg}", file=sys.stderr)
            print(f"This may be due to:")
            print(f"  - Running on Wayland (switch to X11 for hotkey support)")
            print(f"  - Missing permissions (add user to 'input' group)")
            print(f"  - Desktop environment restrictions")
            print(f"WORKAROUND: Use the OCR button in the GUI", file=sys.stderr)
            self.error_occurred.emit(error_msg)
            return False
    
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
