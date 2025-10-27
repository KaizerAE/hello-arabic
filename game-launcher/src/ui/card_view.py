"""
ui/card_view.py
Grid Card View for Game Launcher with images, Play button, tags, search hooks, and i18n-ready strings.

Expansion guide:
- Add new card fields by extending GameCardData and updating GameCardWidget.render.
- Hook data provider via set_data_provider(callable) to fetch games from DB/JSON/API.
- Styling centralized in THEME; tweak to match other launchers.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Dict

from PySide6.QtCore import Qt, QSize, Signal, QObject
from PySide6.QtGui import QPixmap, QIcon, QAction
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout,
    QScrollArea, QLineEdit, QComboBox, QSizePolicy, QFrame, QMenu
)

# Theming palette to resemble popular game launchers
THEME: Dict[str, str] = {
    "bg": "#0e141b",
    "panel": "#141a22",
    "accent": "#4cc2ff",
    "accent_hover": "#71d2ff",
    "text": "#e6eaf0",
    "muted": "#98a2b3",
    "card": "#1a212b",
    "danger": "#ff5d5d",
}

@dataclass
class GameCardData:
    id: str
    title: str
    image_path: str
    category: str = "All"
    tags: List[str] = field(default_factory=list)
    executable: Optional[str] = None  # path or URI
    store_url: Optional[str] = None
    homepage_url: Optional[str] = None

class CardSignals(QObject):
    play_clicked = Signal(str)
    card_open_menu = Signal(str)

class GameCardWidget(QFrame):
    def __init__(self, data: GameCardData, t: Callable[[str], str]):
        super().__init__()
        self.data = data
        self.t = t
        self.setObjectName("GameCard")
        self.setStyleSheet(
            f"""
            QFrame#GameCard {{ background:{THEME['card']}; border-radius:10px; }}
            QFrame#GameCard:hover {{ border:1px solid {THEME['accent']}; }}
            QLabel#Title {{ color:{THEME['text']}; font-weight:600; }}
            QLabel#Category {{ color:{THEME['muted']}; font-size:12px; }}
            QPushButton#Play {{ background:{THEME['accent']}; color:#0b0f14; border:0; border-radius:6px; padding:6px 10px; }}
            QPushButton#Play:hover {{ background:{THEME['accent_hover']}; }}
            """
        )
        self.signals = CardSignals()
        self._build()

    def _build(self):
        v = QVBoxLayout(self)
        v.setContentsMargins(8, 8, 8, 8)
        v.setSpacing(6)

        img = QLabel()
        img.setFixedSize(240, 135)  # 16:9 card image
        img.setStyleSheet("background:#0b0f14; border-radius:8px;")
        pix = QPixmap(self.data.image_path)
        if not pix.isNull():
            img.setPixmap(pix.scaled(img.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        img.setAlignment(Qt.AlignCenter)

        title = QLabel(self.data.title)
        title.setObjectName("Title")
        title.setWordWrap(True)

        category = QLabel(self.data.category)
        category.setObjectName("Category")

        play = QPushButton(self.t("play"))
        play.setObjectName("Play")
        play.setCursor(Qt.PointingHandCursor)
        play.clicked.connect(lambda: self.signals.play_clicked.emit(self.data.id))

        top = QHBoxLayout()
        top.addWidget(title, 1)
        top.addWidget(play, 0)

        v.addWidget(img)
        v.addLayout(top)
        v.addWidget(category)

        # Context menu for extra links
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._open_menu)

    def _open_menu(self, pos):
        menu = QMenu(self)
        if self.data.store_url:
            act_store = QAction(self.t("open_store"), self)
            act_store.triggered.connect(lambda: self.signals.card_open_menu.emit(self.data.store_url or ""))
            menu.addAction(act_store)
        if self.data.homepage_url:
            act_home = QAction(self.t("open_homepage"), self)
            act_home.triggered.connect(lambda: self.signals.card_open_menu.emit(self.data.homepage_url or ""))
            menu.addAction(act_home)
        if not menu.isEmpty():
            menu.exec(self.mapToGlobal(pos))

class CardGridView(QWidget):
    # High-level grid view with search/filter
    play_requested = Signal(str)          # emits game id
    open_link_requested = Signal(str)     # emits url

    def __init__(self, t: Callable[[str], str]):
        super().__init__()
        self.t = t
        self._data_provider: Optional[Callable[[], List[GameCardData]]] = None
        self._all_cards: List[GameCardData] = []
        self._build()

    # Public API to connect data
    def set_data_provider(self, provider: Callable[[], List[GameCardData]]):
        """Attach external data provider. Call refresh() after setting."""
        self._data_provider = provider

    def refresh(self):
        if self._data_provider:
            self._all_cards = self._data_provider() or []
        self._apply_filters()

    def _build(self):
        self.setStyleSheet(
            f"""
            QWidget {{ background:{THEME['bg']}; color:{THEME['text']}; }}
            QLineEdit {{ background:{THEME['panel']}; border:1px solid #273142; border-radius:8px; padding:8px; color:{THEME['text']}; }}
            QComboBox {{ background:{THEME['panel']}; border:1px solid #273142; border-radius:8px; padding:6px; color:{THEME['text']}; }}
            """
        )

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(10)

        controls = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText(self.t("search_games"))
        self.search.textChanged.connect(self._apply_filters)

        self.category = QComboBox()
        self.category.addItem(self.t("all_categories"), "All")
        self.category.currentIndexChanged.connect(self._apply_filters)

        controls.addWidget(self.search, 1)
        controls.addWidget(self.category, 0)
        root.addLayout(controls)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.container = QWidget()
        self.grid = QGridLayout(self.container)
        self.grid.setSpacing(14)
        self.grid.setContentsMargins(4, 4, 4, 4)
        self.scroll.setWidget(self.container)
        root.addWidget(self.scroll, 1)

    def _apply_filters(self):
        # Clear grid
        while self.grid.count():
            item = self.grid.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)
        # Build category list
        cats = ["All"] + sorted({c.category for c in self._all_cards if c.category})
        self._sync_categories(cats)
        # Filter
        q = (self.search.text() or "").strip().lower()
        cat = self.category.currentData() or "All"
        filtered = []
        for d in self._all_cards:
            if cat != "All" and d.category != cat:
                continue
            hay = " ".join([d.title] + d.tags)
            if q and q not in hay.lower():
                continue
            filtered.append(d)
        # Fill grid
        col_count = 4
        r = c = 0
        for d in filtered:
            w = GameCardWidget(d, self.t)
            w.signals.play_clicked.connect(self.play_requested.emit)
            w.signals.card_open_menu.connect(self.open_link_requested.emit)
            self.grid.addWidget(w, r, c)
            c += 1
            if c >= col_count:
                c = 0
                r += 1

    def _sync_categories(self, cats: List[str]):
        # keep current selection when possible
        current = self.category.currentData()
        self.category.blockSignals(True)
        self.category.clear()
        for c in cats:
            label = self.t("category_" + c.lower()) if c != "All" else self.t("all_categories")
            self.category.addItem(label, c)
        # restore
        if current in cats:
            idx = cats.index(current)
            self.category.setCurrentIndex(idx)
        self.category.blockSignals(False)

# Example i18n keys used in this file:
# play, search_games, all_categories, open_store, open_homepage, category_<name>
