from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QGridLayout, QApplication
from PyQt5.QtCore import Qt

QSS_STYLE = """
QWidget { background-color: #23272f; color: #f0f0f0; }
"""

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("مكتبة الألعاب")
        self.setStyleSheet(QSS_STYLE)
        self.resize(800, 500)
        # هنا أكمل باقي الواجهة وتصميمك المتطور
