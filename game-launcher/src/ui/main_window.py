from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QGridLayout, QApplication,
    QLabel, QLineEdit, QPushButton, QFrame, QMessageBox, QInputDialog
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

QSS_STYLE = """
/* Global dark theme */
* { font-family: 'Segoe UI', 'Cairo', sans-serif; }
QWidget { background-color: #1f2330; color: #e6e6e6; }
QLineEdit { background: #2a2f3b; border: 1px solid #3a4252; border-radius: 8px; padding: 8px 12px; color: #e6e6e6; }
QLineEdit:focus { border: 1px solid #4f93ff; }
QPushButton { background: #2d3443; border: 1px solid #3a4252; border-radius: 8px; padding: 8px 12px; color: #e6e6e6; }
QPushButton:hover { background: #344055; }
QPushButton:pressed { background: #2a3344; }
QScrollArea { border: none; }
#Toolbar { background: #1c2030; border-bottom: 1px solid #2b3244; }
#GameCard { background: #242a39; border: 1px solid #353e51; border-radius: 12px; }
#GameCard:hover { border: 1px solid #4f93ff; }
#Header { color: #f4f7ff; font-size: 18px; font-weight: 600; }
#Subtle { color: #b9c0cf; }
"""

class GameCard(QFrame):
    """بطاقة لعبة فردية تعرض الاسم والإجراءات."""
    def __init__(self, game: dict, on_launch, on_delete, parent=None):
        super().__init__(parent)
        self.setObjectName("GameCard")
        self.setMinimumSize(220, 120)
        self.setMaximumHeight(140)
        self.game = game

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # الاسم
        name_row = QHBoxLayout()
        title = QLabel(game.get("name", "لعبة بدون اسم"))
        title.setObjectName("Header")
        title.setWordWrap(True)
        name_row.addWidget(title, 1)

        # زر تشغيل
        launch_btn = QPushButton("تشغيل")
        launch_btn.setToolTip("تشغيل اللعبة")
        launch_btn.clicked.connect(lambda: on_launch(self.game))
        name_row.addWidget(launch_btn)
        layout.addLayout(name_row)

        # سطر معلومات/مسار
        info = QLabel(game.get("path", ""))
        info.setObjectName("Subtle")
        info.setWordWrap(True)
        layout.addWidget(info)

        # أزرار أسفل البطاقة
        actions = QHBoxLayout()
        actions.addStretch(1)
        delete_btn = QPushButton("حذف")
        delete_btn.setToolTip("حذف اللعبة من المكتبة")
        delete_btn.clicked.connect(lambda: on_delete(self.game))
        actions.addWidget(delete_btn)
        layout.addLayout(actions)


class MainWindow(QWidget):
    """
    نافذة مكتبة الألعاب (واجهة رئيسية)

    الميزات:
    - وضع داكن عبر QSS_STYLE
    - شريط علوي: حقل بحث، إضافة لعبة، إعادة تعيين
    - عرض كبطاقات شبكة مع تمرير
    - وظائف: بحث، إضافة، حذف (على مستوى الواجهة)

    ملاحظات التكامل مع المشروع:
    - يفترض أن هناك مدير ألعاب خارجي يمكن ربطه لاحقاً.
      حالياً نخزن قائمة الألعاب محلياً self.games.
    - دوال on_add_game, on_delete_game, on_launch_game قابلة للتوصيل مع backend.
    """

    def __init__(self, games=None):
        super().__init__()
        self.setWindowTitle("مكتبة الألعاب")
        self.setStyleSheet(QSS_STYLE)
        self.resize(980, 640)

        # بيانات أولية
        self.games = list(games) if games else []  # [{"name": ..., "path": ...}]
        self.filtered = list(self.games)

        # تخطيط رئيسي عمودي
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(10)

        # شريط أدوات علوي
        toolbar = QFrame()
        toolbar.setObjectName("Toolbar")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(12, 12, 12, 12)
        toolbar_layout.setSpacing(8)

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("ابحث عن لعبة بالاسم…")
        self.search_edit.textChanged.connect(self.apply_search)

        add_btn = QPushButton("إضافة لعبة")
        add_btn.setToolTip("إضافة لعبة جديدة إلى المكتبة")
        add_btn.clicked.connect(self.prompt_add_game)

        reset_btn = QPushButton("إعادة تعيين")
        reset_btn.setToolTip("مسح البحث وتحديث القائمة")
        reset_btn.clicked.connect(self.reset_filters)

        toolbar_layout.addWidget(QLabel("المكتبة:"))
        toolbar_layout.addWidget(self.search_edit, 1)
        toolbar_layout.addWidget(add_btn)
        toolbar_layout.addWidget(reset_btn)
        root.addWidget(toolbar)

        # منطقة التمرير لبطاقات الألعاب
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.cards_container = QWidget()
        self.grid = QGridLayout(self.cards_container)
        self.grid.setContentsMargins(4, 4, 4, 4)
        self.grid.setHorizontalSpacing(12)
        self.grid.setVerticalSpacing(12)
        self.scroll.setWidget(self.cards_container)
        root.addWidget(self.scroll, 1)

        # أول عرض
        self.refresh_cards()

    # ========== وظائف البيانات ==========
    def apply_search(self):
        term = self.search_edit.text().strip().lower()
        if not term:
            self.filtered = list(self.games)
        else:
            self.filtered = [g for g in self.games if term in g.get("name", "").lower()]
        self.refresh_cards()

    def reset_filters(self):
        self.search_edit.clear()
        self.filtered = list(self.games)
        self.refresh_cards()

    def prompt_add_game(self):
        """حوار بسيط لإدخال اسم اللعبة ومسارها (بدون حوارات ملفات لإبقاء الاعتماديات بسيطة)."""
        name, ok = QInputDialog.getText(self, "إضافة لعبة", "اسم اللعبة:")
        if not ok or not name.strip():
            return
        path, ok2 = QInputDialog.getText(self, "إضافة لعبة", "المسار/الأمر للتشغيل:")
        if not ok2 or not path.strip():
            return
        self.on_add_game({"name": name.strip(), "path": path.strip()})

    # Hooks قابلة للتخصيص/الربط مع منظومة المشروع
    def on_add_game(self, game: dict):
        """إضافة لعبة للقائمة وتحديث العرض. استبدل المنطق هنا بحفظ دائم إذا لزم."""
        # منع تكرار الاسم البسيط
        if any(g.get("name", "").strip().lower() == game.get("name", "").strip().lower() for g in self.games):
            QMessageBox.warning(self, "تحذير", "هناك لعبة بنفس الاسم موجودة بالفعل.")
            return
        self.games.append(game)
        self.apply_search()  # سيعيد بناء البطاقات بناءً على البحث الحالي

    def on_delete_game(self, game: dict):
        reply = QMessageBox.question(self, "تأكيد الحذف", f"هل تريد حذف '{game.get('name','')}'؟")
        if reply != QMessageBox.Yes:
            return
        try:
            self.games.remove(game)
        except ValueError:
            pass
        self.apply_search()

    def on_launch_game(self, game: dict):
        """تشغيل اللعبة. حالياً يعرض رسالة، ويمكن ربطه لاحقاً بتنفيذ فعلي."""
        name = game.get("name", "لعبة")
        path = game.get("path", "")
        QMessageBox.information(self, "تشغيل", f"سيتم تشغيل: {name}\nأمر التشغيل: {path}")
        # مثال للتشغيل الحقيقي لاحقاً:
        # import subprocess, shlex
        # try:
        #     subprocess.Popen(shlex.split(path))
        # except Exception as e:
        #     QMessageBox.critical(self, "خطأ", str(e))

    # ========== بناء الواجهة ==========
    def refresh_cards(self):
        # تنظيف الشبكة
        for i in reversed(range(self.grid.count())):
            w = self.grid.itemAt(i).widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()

        # إنشاء بطاقات جديدة
        if not self.filtered:
            empty = QLabel("لا توجد ألعاب مطابقة.")
            empty.setObjectName("Subtle")
            empty.setAlignment(Qt.AlignCenter)
            self.grid.addWidget(empty, 0, 0)
            return

        cols = 3  # أعمدة البطاقة
        row = col = 0
        for game in self.filtered:
            card = GameCard(game, self.on_launch_game, self.on_delete_game)
            self.grid.addWidget(card, row, col)
            col += 1
            if col >= cols:
                col = 0
                row += 1


# اختباري محلي فقط
if __name__ == "__main__":
    import sys
    sample = [
        {"name": "Chess", "path": "chess.exe"},
        {"name": "Sudoku", "path": "sudoku.exe"},
        {"name": "Tetris", "path": "tetris.exe"},
        {"name": "Pacman", "path": "pacman.exe"},
    ]
    app = QApplication(sys.argv)
    w = MainWindow(sample)
    w.show()
    sys.exit(app.exec_())
