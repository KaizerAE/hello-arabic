# src/ui/main_window.py
# واجهة المستخدم: عرض تلقائي للألعاب + أزرار إضافة وحذف
"""
Main Window Module
واجهة PyQt5 لإدارة مكتبة الألعاب
- عرض تلقائي لقائمة الألعاب من GameLibrary
- زر إضافة لعبة (اسم + مسار + نوع + وصف)
- زر حذف لعبة (حسب التحديد)
"""

import sys
from typing import Optional
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QLineEdit, QFileDialog,
    QComboBox, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt

# ربط الطبقات الأساسية
from src.core.library import GameLibrary
from src.database.storage import DatabaseManager


class MainWindow(QMainWindow):
    def __init__(self, library: Optional[GameLibrary] = None):
        super().__init__()
        self.setWindowTitle("Game Launcher")
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(800, 500)

        # مدير التخزين والمكتبة
        self.storage = DatabaseManager(db_path="game-launcher-data/games.db")
        self.library = library or GameLibrary(storage_manager=self.storage)

        self._setup_ui()
        self._load_games_into_list()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout()
        central.setLayout(root)

        # عنوان
        title = QLabel("مكتبة الألعاب")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("QLabel { font-size: 20px; font-weight: 600; margin: 8px 0; }")
        root.addWidget(title)

        # منطقة تحكم أعلى لإضافة لعبة
        ctrl = QHBoxLayout()
        self.name_edit = QLineEdit(); self.name_edit.setPlaceholderText("اسم اللعبة")
        self.path_edit = QLineEdit(); self.path_edit.setPlaceholderText("مسار ملف التشغيل (.exe أو ملف) ...")
        browse_btn = QPushButton("استعراض…")
        self.genre_combo = QComboBox(); self.genre_combo.addItems([
            "غير محدد", "أكشن", "مغامرات", "أر بي جي", "سباقات", "رياضة", "استراتيجية", "ألغاز"
        ])
        self.desc_edit = QLineEdit(); self.desc_edit.setPlaceholderText("وصف مختصر (اختياري)")
        add_btn = QPushButton("إضافة")

        browse_btn.clicked.connect(self._browse_path)
        add_btn.clicked.connect(self._add_game)

        ctrl.addWidget(self.name_edit, 2)
        ctrl.addWidget(self.path_edit, 3)
        ctrl.addWidget(browse_btn)
        ctrl.addWidget(self.genre_combo)
        ctrl.addWidget(self.desc_edit, 2)
        ctrl.addWidget(add_btn)
        root.addLayout(ctrl)

        # قائمة الألعاب + أزرار جانبية
        mid = QHBoxLayout()
        self.games_list = QListWidget()
        self.games_list.itemSelectionChanged.connect(self._on_selection_changed)
        mid.addWidget(self.games_list, 3)

        side = QVBoxLayout()
        self.details = QTextEdit(); self.details.setReadOnly(True)
        self.details.setPlaceholderText("تفاصيل اللعبة…")
        side.addWidget(self.details, 1)

        btn_row = QHBoxLayout()
        self.delete_btn = QPushButton("حذف")
        self.delete_btn.setEnabled(False)
        self.launch_btn = QPushButton("تشغيل")
        self.launch_btn.setEnabled(False)
        btn_row.addWidget(self.delete_btn)
        btn_row.addWidget(self.launch_btn)
        side.addLayout(btn_row)

        self.delete_btn.clicked.connect(self._delete_selected)
        self.launch_btn.clicked.connect(self._launch_selected)

        mid.addLayout(side, 2)
        root.addLayout(mid)

        # حالة سفلية
        self.statusBar().showMessage("جاهز")

    def _browse_path(self):
        path, _ = QFileDialog.getOpenFileName(self, "اختر ملف اللعبة")
        if path:
            self.path_edit.setText(path)

    def _add_game(self):
        name = self.name_edit.text().strip()
        path = self.path_edit.text().strip()
        genre = self.genre_combo.currentText()
        desc = self.desc_edit.text().strip()

        game = self.library.add_game(name=name, path=path, genre=genre, description=desc)
        if game:
            self._append_game_item(game.id, game.name, game.genre)
            self.name_edit.clear(); self.path_edit.clear(); self.desc_edit.clear()
            self.genre_combo.setCurrentIndex(0)
            self.statusBar().showMessage("تمت الإضافة", 3000)
        else:
            QMessageBox.warning(self, "تعذرت الإضافة", "تحقق من المدخلات أو تكرار اللعبة.")

    def _append_game_item(self, game_id: str, name: str, genre: str):
        item = QListWidgetItem(f"{name} — {genre}")
        item.setData(Qt.UserRole, game_id)
        self.games_list.addItem(item)

    def _load_games_into_list(self):
        self.games_list.clear()
        for game in self.library.get_all_games():
            self._append_game_item(game.id, game.name, game.genre)

    def _on_selection_changed(self):
        items = self.games_list.selectedItems()
        has_sel = bool(items)
        self.delete_btn.setEnabled(has_sel)
        self.launch_btn.setEnabled(has_sel)
        if has_sel:
            game_id = items[0].data(Qt.UserRole)
            game = self.library.get_game(game_id)
            if game:
                info = (
                    f"الاسم: {game.name}\n"
                    f"المسار: {game.path}\n"
                    f"النوع: {game.genre}\n"
                    f"الوصف: {game.description}\n"
                    f"عدد مرات التشغيل: {game.play_count}\n"
                    f"إجمالي وقت اللعب (دقائق): {game.play_time}\n"
                    f"آخر تشغيل: {game.last_played or '—'}\n"
                )
                self.details.setText(info)
        else:
            self.details.clear()

    def _delete_selected(self):
        items = self.games_list.selectedItems()
        if not items:
            return
        item = items[0]
        game_id = item.data(Qt.UserRole)
        game = self.library.get_game(game_id)
        if not game:
            return
        reply = QMessageBox.question(
            self, "تأكيد الحذف", f"هل تريد حذف '{game.name}'؟",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            if self.library.remove_game(game_id):
                row = self.games_list.row(item)
                self.games_list.takeItem(row)
                self.statusBar().showMessage("تم الحذف", 3000)

    def _launch_selected(self):
        items = self.games_list.selectedItems()
        if not items:
            return
        game_id = items[0].data(Qt.UserRole)
        ok = self.library.launch_game(game_id)
        if not ok:
            QMessageBox.warning(self, "فشل التشغيل", "تعذر تشغيل اللعبة. تحقق من المسار.")
        else:
            self._on_selection_changed()


def run_application():
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.RightToLeft)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_application()
