# src/ui/main_window.py
# النافذة الرئيسية لتطبيق Game Launcher
"""
Main Window Module
يحتوي على النافذة الرئيسية للتطبيق
"""

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMenuBar, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    """
    النافذة الرئيسية للتطبيق
    
    سيحتوي لاحقاً على:
    - قائمة رئيسية (إعدادات، عرض)
    - شريط أدوات
    - منطقة عرض الألعاب
    - شريط الحالة
    """
    
    def __init__(self):
        """
        تهيئة النافذة الرئيسية
        """
        super().__init__()
        self.setWindowTitle("Game Launcher")
        self.setGeometry(100, 100, 1000, 700)
        
        # إعداد واجهة المستخدم
        self.setup_ui()
        
    def setup_ui(self):
        """
        إعداد عناصر واجهة المستخدم
        TODO: إضافة عناصر الواجهة
        """
        # إعداد القائمة الرئيسية
        self.setup_menu_bar()
        
        # إعداد الويدجت المركزي
        self.setup_central_widget()
        
    def setup_menu_bar(self):
        """
        إعداد القائمة الرئيسية
        TODO: إضافة عناصر القائمة
        """
        menubar = self.menuBar()
        
        # قائمة الملف
        file_menu = menubar.addMenu('ملف')
        # TODO: إضافة إجراءات الملف
        
        # قائمة العرض
        view_menu = menubar.addMenu('عرض')
        # TODO: إضافة إجراءات العرض
        
        # قائمة المساعدة
        help_menu = menubar.addMenu('مساعدة')
        # TODO: إضافة إجراءات المساعدة
        
    def setup_central_widget(self):
        """
        إعداد الويدجت المركزي
        TODO: إضافة عناصر الواجهة الرئيسية
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # عنوان مؤقت
        title_label = QLabel("مرحباً بك في Game Launcher")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("QLabel { font-size: 24px; margin: 20px; }")
        layout.addWidget(title_label)
        
        # TODO: إضافة قائمة الألعاب
        # TODO: إضافة أزرار التحكم
        
        central_widget.setLayout(layout)
        

def run_application():
    """
    تشغيل تطبيق Game Launcher
    """
    app = QApplication(sys.argv)
    
    # إعداد التطبيق ليدعم اللغة العربية
    app.setLayoutDirection(Qt.RightToLeft)  # دعم الكتابة من اليمين إلى اليسار
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

# للاختبار المباشر
if __name__ == "__main__":
    run_application()
