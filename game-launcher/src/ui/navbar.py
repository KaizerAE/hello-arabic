"""
ui/navbar.py
Top navigation bar with brand, language switch (ar/en), category quick filters, and search relay.

Expansion guide:
- Add more actions (e.g., Settings, Downloads) by appending QAction buttons.
- i18n keys central; use translator callable t(key) for all user-visible strings.
- Emits signals that parent windows can connect to for filtering and language changes.
"""
from __future__ import annotations
from typing import Callable
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox

from PySide6.QtGui import QAction

class NavBar(QWidget):
    # Signals to communicate with main window
    search_changed = Signal(str)
    category_changed = Signal(str)
    language_changed = Signal(str)  # 'ar' or 'en'

    def __init__(self, t: Callable[[str], str]):
        super().__init__()
        self.t = t
        self._build()

    def _build(self):
        self.setObjectName("NavBar")
        self.setStyleSheet(
            """
            QWidget#NavBar { background:#0b0f14; }
            QLabel#Brand { color:#e6eaf0; font-weight:700; }
            QLineEdit { background:#141a22; border:1px solid #273142; border-radius:8px; padding:6px 10px; color:#e6eaf0; }
            QPushButton { background:#1a212b; color:#e6eaf0; border:1px solid #273142; border-radius:8px; padding:6px 10px; }
            QPushButton:hover { border-color:#4cc2ff; }
            QComboBox { background:#141a22; color:#e6eaf0; border:1px solid #273142; border-radius:8px; padding:6px 10px; }
            """
        )
        h = QHBoxLayout(self)
        h.setContentsMargins(12, 12, 12, 12)
        h.setSpacing(8)

        self.brand = QLabel(self.t("app_name"))
        self.brand.setObjectName("Brand")

        self.search = QLineEdit()
        self.search.setPlaceholderText(self.t("search_games"))
        self.search.textChanged.connect(self.search_changed)

        self.quick_category = QComboBox()
        self.quick_category.addItem(self.t("all_categories"), "All")
        self.quick_category.currentIndexChanged.connect(lambda: self.category_changed.emit(self.quick_category.currentData()))

        self.lang = QComboBox()
        self.lang.addItem("العربية", "ar")
        self.lang.addItem("English", "en")
        self.lang.currentIndexChanged.connect(lambda: self.language_changed.emit(self.lang.currentData()))

        btn_settings = QPushButton(self.t("settings"))

        h.addWidget(self.brand, 0)
        h.addWidget(self.search, 1)
        h.addWidget(self.quick_category, 0)
        h.addWidget(self.lang, 0)
        h.addWidget(btn_settings, 0)

    # Helper for parent to sync categories centrally
    def set_categories(self, cats: list[str]):
        current = self.quick_category.currentData()
        self.quick_category.blockSignals(True)
        self.quick_category.clear()
        self.quick_category.addItem(self.t("all_categories"), "All")
        for c in cats:
            if c == "All":
                continue
            self.quick_category.addItem(c, c)
        # restore
        if current in [self.quick_category.itemData(i) for i in range(self.quick_category.count())]:
            self.quick_category.setCurrentText(current)
        self.quick_category.blockSignals(False)
