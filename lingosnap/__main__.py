"""
LingoSnap main entry point
"""

import sys
import setproctitle
from PyQt6.QtWidgets import QApplication
from lingosnap.gui.main_window import MainWindow


def main():
    """Main entry point for LingoSnap application"""
    # Set process title for easier identification
    setproctitle.setproctitle('lingosnap')
    
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
