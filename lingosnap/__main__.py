"""
LingoSnap main entry point
"""

import sys
import os
import setproctitle
from PyQt6.QtWidgets import QApplication
from lingosnap.gui.main_window import MainWindow


def main():
    """Main entry point for LingoSnap application"""
    # Set process title for easier identification
    setproctitle.setproctitle('lingosnap')
    
    # Set QT_QPA_PLATFORM environment variable for better compatibility
    # This helps with X11/Wayland detection and fallback
    if 'QT_QPA_PLATFORM' not in os.environ:
        # Try to auto-detect and prefer xcb (X11) for better compatibility
        # If xcb fails, Qt will automatically fallback to wayland
        session_type = os.environ.get('XDG_SESSION_TYPE', '').lower()
        
        if session_type == 'x11':
            os.environ['QT_QPA_PLATFORM'] = 'xcb'
        elif session_type == 'wayland':
            os.environ['QT_QPA_PLATFORM'] = 'wayland'
        # Otherwise let Qt auto-detect
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName('LingoSnap')
    app.setOrganizationName('LingoSnap')
    app.setQuitOnLastWindowClosed(False)  # Keep running in system tray
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
