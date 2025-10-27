# src/core/library.py
# مكتبة الألعاب - إدارة ألعاب المستخدم
"""
Game Library Module
يدير مكتبة الألعاب الخاصة بالمستخدم
"""

import os
from datetime import datetime

class Game:
    """فئة تمثل لعبة واحدة"""
    
    def __init__(self, name, path, genre="غير محدد", description=""):
        self.id = self._generate_id()
        self.name = name
        self.path = path
        self.genre = genre
        self.description = description
        self.added_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_played = None
        self.play_time = 0  # بالدقائق
        self.play_count = 0
    
    def _generate_id(self):
        """توليد معرف فريد للعبة"""
        from random import randint
        return f"game_{datetime.now().strftime('%Y%m%d%H%M%S')}_{randint(1000, 9999)}"
    
    def update_play_stats(self, duration_minutes=0):
        """تحديث إحصائيات اللعب"""
        self.last_played = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.play_count += 1
        self.play_time += duration_minutes
    
    def to_dict(self):
        """تحويل اللعبة إلى قاموس"""
        return {
            'id': self.id,
            'name': self.name,
            'path': self.path,
            'genre': self.genre,
            'description': self.description,
            'added_date': self.added_date,
            'last_played': self.last_played,
            'play_time': self.play_time,
            'play_count': self.play_count
        }
    
    @classmethod
    def from_dict(cls, data):
        """إنشاء لعبة من قاموس"""
        game = cls(
            name=data['name'],
            path=data['path'],
            genre=data.get('genre', 'غير محدد'),
            description=data.get('description', '')
        )
        game.id = data['id']
        game.added_date = data.get('added_date', game.added_date)
        game.last_played = data.get('last_played')
        game.play_time = data.get('play_time', 0)
        game.play_count = data.get('play_count', 0)
        return game


class GameLibrary:
    """
    Class لإدارة مكتبة الألعاب
    
    يوفر وظائف:
    - إضافة وحذف الألعاب
    - تحديث معلومات الألعاب
    - البحث والفلترة
    - إحصائيات اللعب
    """
    
    def __init__(self, storage_manager=None):
        """
        تهيئة مكتبة الألعاب
        
        Args:
            storage_manager: مدير قاعدة البيانات لحفظ واسترجاع البيانات
        """
        self.games = {}  # dictionary: {game_id: Game}
        self.storage = storage_manager
        
        # تحميل الألعاب من قاعدة البيانات إن وجدت
        if self.storage:
            self._load_games()
    
    def _load_games(self):
        """تحميل الألعاب من قاعدة البيانات"""
        try:
            games_data = self.storage.load_games()
            for game_dict in games_data:
                game = Game.from_dict(game_dict)
                self.games[game.id] = game
        except Exception as e:
            print(f"خطأ في تحميل الألعاب: {e}")
    
    def _save_games(self):
        """حفظ الألعاب في قاعدة البيانات"""
        if self.storage:
            try:
                games_data = [game.to_dict() for game in self.games.values()]
                self.storage.save_games(games_data)
            except Exception as e:
                print(f"خطأ في حفظ الألعاب: {e}")
    
    def add_game(self, name, path, genre="غير محدد", description=""):
        """
        إضافة لعبة جديدة للمكتبة
        
        Args:
            name: اسم اللعبة
            path: مسار ملف اللعبة التنفيذي
            genre: نوع اللعبة (اختياري)
            description: وصف اللعبة (اختياري)
        
        Returns:
            Game: كائن اللعبة المضافة أو None في حالة الفشل
        """
        # التحقق من صحة المدخلات
        if not name or not name.strip():
            print("خطأ: اسم اللعبة فارغ")
            return None
        
        if not path or not path.strip():
            print("خطأ: مسار اللعبة فارغ")
            return None
        
        # التحقق من وجود المسار
        if not os.path.exists(path):
            print(f"تحذير: المسار غير موجود: {path}")
            # يمكن الاستمرار لكن يجب إعلام المستخدم
        
        # التحقق من عدم تكرار اللعبة
        for game in self.games.values():
            if game.name == name and game.path == path:
                print(f"اللعبة '{name}' موجودة بالفعل")
                return None
        
        # إنشاء اللعبة الجديدة
        new_game = Game(name, path, genre, description)
        self.games[new_game.id] = new_game
        
        # حفظ التغييرات
        self._save_games()
        
        print(f"تمت إضافة اللعبة: {name}")
        return new_game
    
    def remove_game(self, game_id):
        """
        حذف لعبة من المكتبة
        
        Args:
            game_id: معرف اللعبة المراد حذفها
        
        Returns:
            bool: True إذا تم الحذف بنجاح، False خلاف ذلك
        """
        if game_id in self.games:
            game_name = self.games[game_id].name
            del self.games[game_id]
            self._save_games()
            print(f"تم حذف اللعبة: {game_name}")
            return True
        else:
            print(f"خطأ: اللعبة غير موجودة (ID: {game_id})")
            return False
    
    def get_game(self, game_id):
        """
        الحصول على لعبة معينة
        
        Args:
            game_id: معرف اللعبة
        
        Returns:
            Game: كائن اللعبة أو None إذا لم يتم العثور عليها
        """
        return self.games.get(game_id)
    
    def get_all_games(self):
        """
        الحصول على جميع الألعاب
        
        Returns:
            list: قائمة بجميع الألعاب
        """
        return list(self.games.values())
    
    def search_games(self, keyword):
        """
        البحث عن ألعاب باستخدام كلمة مفتاحية
        
        Args:
            keyword: الكلمة المفتاحية للبحث
        
        Returns:
            list: قائمة الألعاب المطابقة
        """
        keyword = keyword.lower()
        results = []
        
        for game in self.games.values():
            if (keyword in game.name.lower() or 
                keyword in game.genre.lower() or 
                keyword in game.description.lower()):
                results.append(game)
        
        return results
    
    def filter_by_genre(self, genre):
        """
        فلترة الألعاب حسب النوع
        
        Args:
            genre: نوع اللعبة
        
        Returns:
            list: قائمة الألعاب من النوع المحدد
        """
        return [game for game in self.games.values() if game.genre == genre]
    
    def update_game(self, game_id, **kwargs):
        """
        تحديث معلومات لعبة
        
        Args:
            game_id: معرف اللعبة
            **kwargs: الحقول المراد تحديثها
        
        Returns:
            bool: True إذا تم التحديث بنجاح
        """
        if game_id not in self.games:
            print(f"خطأ: اللعبة غير موجودة (ID: {game_id})")
            return False
        
        game = self.games[game_id]
        
        # تحديث الحقول المسموح بها
        allowed_fields = ['name', 'path', 'genre', 'description']
        for field, value in kwargs.items():
            if field in allowed_fields:
                setattr(game, field, value)
        
        self._save_games()
        print(f"تم تحديث اللعبة: {game.name}")
        return True
    
    def launch_game(self, game_id):
        """
        تشغيل لعبة وتحديث إحصائياتها
        
        Args:
            game_id: معرف اللعبة
        
        Returns:
            bool: True إذا تم التشغيل بنجاح
        """
        game = self.get_game(game_id)
        if not game:
            print(f"خطأ: اللعبة غير موجودة (ID: {game_id})")
            return False
        
        if not os.path.exists(game.path):
            print(f"خطأ: ملف اللعبة غير موجود: {game.path}")
            return False
        
        try:
            # تحديث إحصائيات اللعب
            game.update_play_stats()
            self._save_games()
            
            # تشغيل اللعبة
            import subprocess
            if os.name == 'nt':  # Windows
                os.startfile(game.path)
            else:  # Linux/Mac
                subprocess.Popen([game.path])
            
            print(f"تم تشغيل اللعبة: {game.name}")
            return True
        except Exception as e:
            print(f"خطأ في تشغيل اللعبة: {e}")
            return False
    
    def get_statistics(self):
        """
        الحصول على إحصائيات المكتبة
        
        Returns:
            dict: قاموس يحتوي على الإحصائيات
        """
        total_games = len(self.games)
        total_play_time = sum(game.play_time for game in self.games.values())
        total_plays = sum(game.play_count for game in self.games.values())
        
        most_played = None
        if self.games:
            most_played = max(self.games.values(), key=lambda g: g.play_count)
        
        return {
            'total_games': total_games,
            'total_play_time': total_play_time,
            'total_plays': total_plays,
            'most_played': most_played.name if most_played else "لا يوجد"
        }
