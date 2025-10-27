#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Game Launcher - مشغل الألعاب
A modern game library management application

Author: KaizerAE
Version: 1.0.0
License: Open Source
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QPushButton, QStackedWidget,
    QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.QtGui import QFont, QColor, QLinearGradient, QPalette


class WelcomeScreen(QWidget):
    """شاشة الترحيب الرئيسية / Main Welcome Screen"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)
        
        # Main title with gradient effect
        title_label = QLabel("🎮 Game Launcher")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Arial", 42, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("""
            QLabel {
                color: #2196F3;
                padding: 20px;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(33, 150, 243, 0.1),
                    stop:1 rgba(3, 169, 244, 0.1)
                );
                border-radius: 15px;
            }
        """)
        
        # Arabic subtitle
        subtitle_ar = QLabel("مكتبة ألعاب حديثة وشاملة")
        subtitle_ar.setAlignment(Qt.AlignCenter)
        subtitle_ar.setFont(QFont("Arial", 16))
        subtitle_ar.setStyleSheet("color: #757575; padding: 10px;")
        
        # English subtitle
        subtitle_en = QLabel("Modern & Comprehensive Game Library")
        subtitle_en.setAlignment(Qt.AlignCenter)
        subtitle_en.setFont(QFont("Arial", 14))
        subtitle_en.setStyleSheet("color: #9E9E9E; padding: 5px;")
        
        # Version info
        version_label = QLabel("Version 1.0.0 - Initial Release")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setFont(QFont("Arial", 10))
        version_label.setStyleSheet("color: #BDBDBD; padding: 10px;")
        
        # Feature cards container
        features_frame = QFrame()
        features_frame.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        features_layout = QVBoxLayout()
        
        # Features list
        features = [
            "📚 إدارة مكتبة الألعاب / Game Library Management",
            "🚀 تشغيل سريع / Quick Launch",
            "📊 تتبع الإحصائيات / Statistics Tracking",
            "🎨 واجهة عصرية / Modern Interface",
            "🔄 مزامنة سحابية / Cloud Sync (قريباً / Coming Soon)"
        ]
        
        for feature in features:
            feature_label = QLabel(feature)
            feature_label.setFont(QFont("Arial", 11))
            feature_label.setStyleSheet("""
                QLabel {
                    color: #424242;
                    padding: 8px;
                    background-color: white;
                    border-radius: 5px;
                    margin: 3px;
                }
            """)
            features_layout.addWidget(feature_label)
        
        features_frame.setLayout(features_layout)
        
        # Start button
        start_button = QPushButton("ابدأ الآن / Get Started")
        start_button.setFont(QFont("Arial", 14, QFont.Bold))
        start_button.setCursor(Qt.PointingHandCursor)
        start_button.setFixedHeight(50)
        start_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 25px;
                padding: 10px 40px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        start_button.clicked.connect(self.on_start_clicked)
        
        # Add shadow effect to start button
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 80))
        start_button.setGraphicsEffect(shadow)
        
        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addWidget(subtitle_ar)
        layout.addWidget(subtitle_en)
        layout.addWidget(version_label)
        layout.addSpacing(20)
        layout.addWidget(features_frame)
        layout.addSpacing(20)
        layout.addWidget(start_button, alignment=Qt.AlignCenter)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def on_start_clicked(self):
        """Handle start button click"""
        print("🎮 Starting Game Launcher...")
        print("📂 Loading game library...")
        # TODO: Transition to main application window
        # This will be implemented in future versions


class GameLauncherApp(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the main window"""
        # Window configuration
        self.setWindowTitle("Game Launcher - مشغل الألعاب")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(800, 600)
        
        # Set window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FAFAFA;
            }
        """)
        
        # Create central widget and stacked widget for multiple screens
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Stacked widget to manage different screens
        self.stacked_widget = QStackedWidget()
        
        # Add welcome screen
        welcome_screen = WelcomeScreen()
        self.stacked_widget.addWidget(welcome_screen)
        
        # TODO: Add more screens (library, settings, etc.)
        
        main_layout.addWidget(self.stacked_widget)
        
        # Show welcome animation
        self.show_welcome_animation()
    
    def show_welcome_animation(self):
        """Display welcome animation"""
        # This can be enhanced with fade-in or slide animations
        print("👋 Welcome to Game Launcher!")
        print("مرحباً بك في مشغل الألعاب!")


def main():
    """Main entry point of the application"""
    # Create application instance
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("Game Launcher")
    app.setOrganizationName("KaizerAE")
    app.setApplicationVersion("1.0.0")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = GameLauncherApp()
    window.show()
    
    # Print startup message
    print("="*50)
    print("🎮 Game Launcher v1.0.0")
    print("📝 مشروع مكتبة الألعاب الحديثة")
    print("🚀 Application started successfully!")
    print("="*50)
    
    # Start event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
