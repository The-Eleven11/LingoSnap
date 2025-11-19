"""
Screenshot capture tool
"""

from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QRect, QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen, QPixmap, QScreen
from PIL import Image
import io


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
        # Capture all screens
        screens = QApplication.screens()
        if not screens:
            return
        
        # Get primary screen
        screen = screens[0]
        self.screenshot = screen.grabWindow(0)
        
        # Show overlay
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
        
        # Convert QPixmap to PIL Image
        buffer = io.BytesIO()
        cropped.save(buffer, 'PNG')
        buffer.seek(0)
        pil_image = Image.open(buffer)
        
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
    
    def capture(self, callback):
        """
        Start screenshot capture
        
        Args:
            callback: Function to call with captured image
        """
        self.callback = callback
        
        if not self.widget:
            self.widget = ScreenshotWidget()
            self.widget.screenshot_taken.connect(self.on_screenshot_taken)
        
        self.widget.start_capture()
    
    def on_screenshot_taken(self, image):
        """Handle screenshot taken"""
        if self.callback:
            self.callback(image)
