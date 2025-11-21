"""
Screenshot capture tool
"""

import sys
import subprocess
import tempfile
import os
import time
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QRect, QPoint, pyqtSignal, QTimer
from PyQt6.QtGui import QPainter, QColor, QPen, QPixmap, QScreen
from PIL import Image


class ScreenshotWidget(QWidget):
    """Widget for capturing screenshots"""
    
    screenshot_taken = pyqtSignal(object)  # Emits PIL Image
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        
        self.start_point = None
        self.end_point = None
        self.screenshot = None
    
    def start_capture(self):
        """Start screenshot capture"""
        # First, capture the screen BEFORE showing the overlay
        # This is crucial because the overlay will be captured otherwise
        
        screen = QApplication.primaryScreen()
        if not screen:
            print("Error: No screen found", file=sys.stderr)
            return
        
        # Capture the entire screen
        # Use the screen's geometry for accurate capture
        geometry = screen.geometry()
        self.screenshot = screen.grabWindow(
            0,  # Window ID (0 for entire screen)
            geometry.x(),
            geometry.y(),
            geometry.width(),
            geometry.height()
        )
        
        # Verify screenshot was captured
        if self.screenshot.isNull():
            print("Warning: Screenshot may be empty. This can happen on Wayland.", file=sys.stderr)
            print("Tip: Try running on X11 (select 'Ubuntu on Xorg' at login)", file=sys.stderr)
        
        # Show overlay AFTER capturing
        self.showFullScreen()
        self.setCursor(Qt.CursorShape.CrossCursor)
    
    def paintEvent(self, event):
        """Paint the overlay"""
        painter = QPainter(self)
        
        # Draw semi-transparent overlay
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))
        
        # Draw selection rectangle
        if self.start_point and self.end_point:
            rect = QRect(self.start_point, self.end_point).normalized()
            
            # Clear the selection area
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
            painter.fillRect(rect, QColor(0, 0, 0, 0))
            
            # Draw border
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
            pen = QPen(QColor(0, 120, 215), 2)
            painter.setPen(pen)
            painter.drawRect(rect)
    
    def mousePressEvent(self, event):
        """Handle mouse press"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_point = event.pos()
            self.end_point = event.pos()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move"""
        if self.start_point:
            self.end_point = event.pos()
            self.update()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if event.button() == Qt.MouseButton.LeftButton and self.start_point:
            self.end_point = event.pos()
            self.capture_region()
    
    def keyPressEvent(self, event):
        """Handle key press"""
        if event.key() == Qt.Key.Key_Escape:
            self.cancel_capture()
    
    def capture_region(self):
        """Capture the selected region"""
        if not self.start_point or not self.end_point or not self.screenshot:
            self.cancel_capture()
            return
        
        rect = QRect(self.start_point, self.end_point).normalized()
        
        if rect.width() < 5 or rect.height() < 5:
            self.cancel_capture()
            return
        
        # Crop the screenshot
        cropped = self.screenshot.copy(rect)
        
        # Check if cropped pixmap is valid
        if cropped.isNull():
            print("Error: Failed to crop screenshot", file=sys.stderr)
            self.cancel_capture()
            return
        
        # Convert QPixmap to PIL Image
        # PyQt6 doesn't support saving to BytesIO directly, so convert via QImage
        qimage = cropped.toImage()
        
        # Check if conversion was successful
        if qimage.isNull():
            print("Error: Failed to convert pixmap to image", file=sys.stderr)
            self.cancel_capture()
            return
        
        # Get image bits
        bits = qimage.bits()
        if bits is None:
            print("Error: Failed to get image bits", file=sys.stderr)
            self.cancel_capture()
            return
        
        # Convert QImage to bytes
        try:
            byte_array = bits.asarray(qimage.sizeInBytes())
        except Exception as e:
            print(f"Error: Failed to convert image to byte array: {e}", file=sys.stderr)
            self.cancel_capture()
            return
        
        # Create PIL Image from raw data
        width = qimage.width()
        height = qimage.height()
        
        try:
            # QImage format is typically ARGB32 or RGB32
            if qimage.format() == qimage.Format.Format_RGB32 or qimage.format() == qimage.Format.Format_ARGB32:
                # Convert to RGB
                pil_image = Image.frombytes('RGBA', (width, height), byte_array, 'raw', 'BGRA')
                pil_image = pil_image.convert('RGB')
            else:
                # Fallback: convert to RGB888 first
                qimage = qimage.convertToFormat(qimage.Format.Format_RGB888)
                bits = qimage.bits()
                if bits is None:
                    raise ValueError("Failed to get bits after format conversion")
                byte_array = bits.asarray(qimage.sizeInBytes())
                pil_image = Image.frombytes('RGB', (width, height), byte_array, 'raw', 'RGB')
        except Exception as e:
            print(f"Error: Failed to create PIL image: {e}", file=sys.stderr)
            self.cancel_capture()
            return
        
        # Clean up
        self.hide()
        self.start_point = None
        self.end_point = None
        
        # Emit signal
        self.screenshot_taken.emit(pil_image)
    
    def cancel_capture(self):
        """Cancel screenshot capture"""
        self.hide()
        self.start_point = None
        self.end_point = None
        self.screenshot_taken.emit(None)


class ScreenshotTool:
    """Tool for capturing screenshots with OCR"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.widget = None
        self.callback = None
        self.temp_file = None
        self.use_system_tool = True  # Default to system tool for better compatibility
    
    def capture(self, callback):
        """
        Start screenshot capture
        
        Args:
            callback: Function to call with captured image
        """
        self.callback = callback
        
        # Try system screenshot tool first for better compatibility
        if self.use_system_tool:
            self.capture_with_system_tool()
        else:
            # Fallback to built-in method
            if not self.widget:
                self.widget = ScreenshotWidget()
                self.widget.screenshot_taken.connect(self.on_screenshot_taken)
            
            self.widget.start_capture()
    
    def capture_with_system_tool(self):
        """
        Use system screenshot tool for better compatibility
        
        This method:
        1. Hides the main window
        2. Calls system screenshot tool (gnome-screenshot, spectacle, flameshot, etc.)
        3. Waits for user to save the screenshot
        4. Loads the screenshot for OCR
        5. Restores the main window
        """
        # Hide the main window temporarily
        if self.parent:
            self.parent.hide()
        
        # Create a temporary file for the screenshot
        self.temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        temp_path = self.temp_file.name
        self.temp_file.close()
        
        # Try different screenshot tools in order of preference
        screenshot_tools = [
            # GNOME Screenshot (most common on Ubuntu) - most reliable
            ['gnome-screenshot', '-a', '-f', temp_path],
            # KDE Spectacle
            ['spectacle', '-b', '-r', '-n', '-o', temp_path],
            # ImageMagick import - simple and reliable
            ['import', temp_path],
            # Scrot - lightweight and reliable
            ['scrot', '-s', temp_path],
            # Flameshot - captures to stdout in raw mode, we'll handle separately
            # Note: flameshot gui mode doesn't support direct file output
        ]
        
        success = False
        
        # First, try flameshot with special handling (captures to stdout)
        try:
            result = subprocess.run(['which', 'flameshot'], capture_output=True, timeout=1)
            if result.returncode == 0:
                print("Using screenshot tool: flameshot", file=sys.stderr)
                
                # Flameshot gui mode with raw output to stdout
                process = subprocess.Popen(
                    ['flameshot', 'gui', '--raw'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                
                # Wait for the screenshot to be captured to stdout
                QTimer.singleShot(500, lambda: self.check_flameshot_stdout(temp_path, process, 0))
                success = True
        except:
            pass
        
        # If flameshot didn't work, try other tools
        if not success:
            for tool_cmd in screenshot_tools:
                try:
                    # Check if tool exists
                    tool_name = tool_cmd[0]
                    check_cmd = ['which', tool_name]
                    result = subprocess.run(check_cmd, capture_output=True, timeout=1)
                    
                    if result.returncode == 0:
                        print(f"Using screenshot tool: {tool_name}", file=sys.stderr)
                        
                        # Run the screenshot tool
                        # Use subprocess.Popen to run asynchronously
                        process = subprocess.Popen(
                            tool_cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                        
                        # Wait for the screenshot to be saved
                        # Check periodically if file exists and has content
                        QTimer.singleShot(500, lambda: self.check_screenshot_file(temp_path, process, 0))
                        success = True
                        break
                        
                except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
                    continue
        
        if not success:
            print("Error: No system screenshot tool found", file=sys.stderr)
            print("Tried: gnome-screenshot, spectacle, flameshot, import, scrot", file=sys.stderr)
            print("Falling back to built-in screenshot method", file=sys.stderr)
            
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except:
                pass
            
            # Restore window
            if self.parent:
                self.parent.show()
            
            # Fallback to built-in method
            self.use_system_tool = False
            if not self.widget:
                self.widget = ScreenshotWidget()
                self.widget.screenshot_taken.connect(self.on_screenshot_taken)
            
            self.widget.start_capture()
    
    def check_flameshot_stdout(self, temp_path, process, retry_count):
        """
        Check if flameshot has output screenshot data to stdout
        
        Args:
            temp_path: Path to temporary screenshot file
            process: The subprocess running flameshot
            retry_count: Number of times we've checked
        """
        max_retries = 60  # Check for up to 30 seconds (60 * 0.5s)
        
        # Check if process has finished
        poll_result = process.poll()
        
        if poll_result is not None:
            # Process finished
            if poll_result == 0:
                # Success - read from stdout
                try:
                    stdout_data = process.stdout.read()
                    
                    if stdout_data and len(stdout_data) > 0:
                        # Save the image data to temp file
                        with open(temp_path, 'wb') as f:
                            f.write(stdout_data)
                        
                        print(f"Screenshot captured from flameshot ({len(stdout_data)} bytes)", file=sys.stderr)
                        
                        # Load the image
                        image = Image.open(temp_path)
                        
                        # Clean up temp file
                        try:
                            os.unlink(temp_path)
                        except:
                            pass
                        
                        # Restore window
                        if self.parent:
                            self.parent.show()
                        
                        # Call callback
                        if self.callback:
                            self.callback(image)
                        return
                    else:
                        # No data - user cancelled
                        print("Flameshot: No screenshot captured (cancelled or ESC pressed)", file=sys.stderr)
                        
                except Exception as e:
                    print(f"Error reading flameshot output: {e}", file=sys.stderr)
            else:
                # Process finished with error
                print(f"Flameshot exited with code {poll_result}", file=sys.stderr)
            
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except:
                pass
            
            # Restore window
            if self.parent:
                self.parent.show()
            
            # Call callback with None
            if self.callback:
                self.callback(None)
        
        elif retry_count >= max_retries:
            # Timeout
            print("Timeout waiting for screenshot (30 seconds)", file=sys.stderr)
            print("Flameshot process still running but no output received", file=sys.stderr)
            print("This may indicate:", file=sys.stderr)
            print("  1. Screenshot was cancelled (pressed ESC)", file=sys.stderr)
            print("  2. Flameshot GUI still open - click checkmark (✓) or press Enter", file=sys.stderr)
            print("  3. System issue preventing capture", file=sys.stderr)
            
            # Try to terminate the process
            try:
                process.terminate()
                process.wait(timeout=2)
            except:
                try:
                    process.kill()
                except:
                    pass
            
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except:
                pass
            
            # Restore window
            if self.parent:
                self.parent.show()
            
            # Call callback with None
            if self.callback:
                self.callback(None)
        
        else:
            # Still waiting, check again
            # Print progress every 5 seconds to let user know we're waiting
            if retry_count > 0 and retry_count % 10 == 0:
                elapsed = retry_count * 0.5
                print(f"Still waiting for screenshot... ({elapsed:.0f}s elapsed)", file=sys.stderr)
                print("After selecting region, click the checkmark (✓) or press Enter", file=sys.stderr)
            
            QTimer.singleShot(500, lambda: self.check_flameshot_stdout(temp_path, process, retry_count + 1))
    
    def check_screenshot_file(self, temp_path, process, retry_count):
        """
        Check if screenshot file has been created and has content
        
        Args:
            temp_path: Path to temporary screenshot file
            process: The subprocess running the screenshot tool
            retry_count: Number of times we've checked
        """
        max_retries = 60  # Check for up to 30 seconds (60 * 0.5s)
        
        # Check if process has finished
        poll_result = process.poll()
        
        # Check if file exists and has content
        if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
            # File is ready, load it
            print(f"Screenshot saved to {temp_path}", file=sys.stderr)
            
            try:
                # Load the image
                image = Image.open(temp_path)
                
                # Clean up temp file
                try:
                    os.unlink(temp_path)
                except:
                    pass
                
                # Restore window
                if self.parent:
                    self.parent.show()
                
                # Call callback
                if self.callback:
                    self.callback(image)
                    
            except Exception as e:
                print(f"Error loading screenshot: {e}", file=sys.stderr)
                
                # Clean up temp file
                try:
                    os.unlink(temp_path)
                except:
                    pass
                
                # Restore window
                if self.parent:
                    self.parent.show()
                
                # Call callback with None
                if self.callback:
                    self.callback(None)
        
        elif poll_result is not None and poll_result != 0:
            # Process finished with error
            print(f"Screenshot tool exited with code {poll_result}", file=sys.stderr)
            
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except:
                pass
            
            # Restore window
            if self.parent:
                self.parent.show()
            
            # Call callback with None (user cancelled)
            if self.callback:
                self.callback(None)
        
        elif poll_result is not None:
            # Process finished successfully but file doesn't exist yet
            # This might mean user cancelled
            if retry_count < 5:
                # Wait a bit longer in case file is being written
                QTimer.singleShot(200, lambda: self.check_screenshot_file(temp_path, process, retry_count + 1))
            else:
                print("Screenshot tool finished but no file created (user may have cancelled)", file=sys.stderr)
                
                # Clean up temp file
                try:
                    os.unlink(temp_path)
                except:
                    pass
                
                # Restore window
                if self.parent:
                    self.parent.show()
                
                # Call callback with None
                if self.callback:
                    self.callback(None)
        
        elif retry_count >= max_retries:
            # Timeout
            print("Timeout waiting for screenshot (30 seconds)", file=sys.stderr)
            print("Screenshot tool may still be waiting for your selection or cancelled", file=sys.stderr)
            
            # Try to terminate the process
            try:
                process.terminate()
                process.wait(timeout=2)
            except:
                try:
                    process.kill()
                except:
                    pass
            
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except:
                pass
            
            # Restore window
            if self.parent:
                self.parent.show()
            
            # Call callback with None
            if self.callback:
                self.callback(None)
        
        else:
            # Still waiting, check again
            # Print progress every 10 seconds to let user know we're waiting
            if retry_count > 0 and retry_count % 20 == 0:
                elapsed = retry_count * 0.5
                print(f"Still waiting for screenshot... ({elapsed:.0f}s elapsed)", file=sys.stderr)
            
            QTimer.singleShot(500, lambda: self.check_screenshot_file(temp_path, process, retry_count + 1))
    
    def on_screenshot_taken(self, image):
        """Handle screenshot taken"""
        if self.callback:
            self.callback(image)
