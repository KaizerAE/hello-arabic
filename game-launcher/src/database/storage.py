# src/database/storage.py
# إدارة التخزين باستخدام pickle
"""
Storage Module
يدير حفظ واسترجاع بيانات الألعاب باستخدام pickle
"""

import os
import pickle
from typing import List, Dict, Any


class DatabaseManager:
    """
    مدير قاعدة البيانات المبني على pickle
    - يحفظ البيانات في ملف ثنائي
    - يوفر عمليات التحميل والحفظ بأمان
    """

    def __init__(self, db_path: str = "games.db"):
        """تهيئة مدير قاعدة البيانات"""
        self.db_path = db_path
        # تأكد من وجود المجلد
        folder = os.path.dirname(self.db_path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

    def save_games(self, games_data: List[Dict[str, Any]]) -> None:
        """
        حفظ قائمة الألعاب إلى الملف
        Args:
            games_data: قائمة قواميس تمثل الألعاب
        """
        tmp_path = self.db_path + ".tmp"
        try:
            with open(tmp_path, "wb") as f:
                pickle.dump(games_data, f, protocol=pickle.HIGHEST_PROTOCOL)
            # استبدال آمن
            os.replace(tmp_path, self.db_path)
        finally:
            # تنظيف الملف المؤقت إذا بقي
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass

    def load_games(self) -> List[Dict[str, Any]]:
        """
        تحميل قائمة الألعاب من الملف. يعيد قائمة فارغة إذا لم يوجد الملف.
        """
        if not os.path.exists(self.db_path):
            return []
        try:
            with open(self.db_path, "rb") as f:
                data = pickle.load(f)
                # تأكد من أن البيانات قائمة
                if isinstance(data, list):
                    return data
                return []
        except Exception as e:
            print(f"خطأ في تحميل قاعدة البيانات: {e}")
            return []

    def clear(self) -> None:
        """حذف ملف قاعدة البيانات"""
        try:
            if os.path.exists(self.db_path):
                os.remove(self.db_path)
        except Exception as e:
            print(f"تعذر حذف قاعدة البيانات: {e}")
