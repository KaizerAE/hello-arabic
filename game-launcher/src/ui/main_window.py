            color: #AAB0B6; font-size: 12px; }
        QLineEdit, QComboBox, QTextEdit { background-color: #1A1F24; border: 1px solid #2A3138; padding: 6px; border-radius: 6px; }
        QPushButton { background-color: #2B323A; border: 1px solid #39424C; padding: 6px 10px; border-radius: 6px; }
        QPushButton:hover { background-color: #36404A; }
        QPushButton:pressed { background-color: #3E4954; }
        QFrame#GameCard { background-color: #14181D; border: 1px solid #242A31; border-radius: 10px; padding: 8px; }
        QScrollArea { border: none; }
        QStatusBar { color: #C9CED3; }
        """
        self.setStyleSheet(qss)

# نقطة تشغيل التطبيق (للتطوير المحلي)
def run_application():
    app = QApplication(sys.argv)
    # احترام اتجاه الواجهة مع العربية
    app.setLayoutDirection(Qt.RightToLeft)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_application()
