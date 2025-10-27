# Game Launcher - مشغل الألعاب

## نظرة عامة / Overview

مشروع Game Launcher هو مكتبة ألعاب حديثة وشاملة مصممة لإدارة وتنظيم مجموعتك من الألعاب في مكان واحد. يوفر المشروع واجهة رسومية سهلة الاستخدام مبنية على PyQt5 لتجربة مستخدم سلسة واحترافية.

Game Launcher is a modern, comprehensive game library designed to manage and organize your game collection in one place. The project provides an easy-to-use graphical interface built with PyQt5 for a smooth and professional user experience.

## الوظائف الرئيسية / Main Features

### 🎮 إدارة المكتبة / Library Management
- إضافة وحذف الألعاب من المكتبة
- تصنيف الألعاب حسب النوع، المنصة، والناشر
- البحث السريع عن الألعاب في المكتبة
- عرض معلومات تفصيلية عن كل لعبة

### 🚀 التشغيل والإطلاق / Launch & Play
- تشغيل الألعاب مباشرة من الواجهة
- إدارة ملفات الحفظ والإعدادات
- تتبع وقت اللعب والإحصائيات
- دعم منصات متعددة (Steam, Epic Games, GOG, وغيرها)

### 📊 التتبع والإحصائيات / Tracking & Statistics
- تتبع الوقت المستغرق في كل لعبة
- إحصائيات شاملة عن عادات اللعب
- نظام الإنجازات والتقدم
- تقييم الألعاب والمراجعات الشخصية

### 🎨 الواجهة والتخصيص / Interface & Customization
- واجهة رسومية عصرية وسهلة الاستخدام
- دعم الثيمات الداكنة والفاتحة
- تخصيص العرض والترتيب
- دعم اللغة العربية والإنجليزية

### 🔄 المزامنة والنسخ الاحتياطي / Sync & Backup
- مزامنة المكتبة عبر الأجهزة المختلفة
- نسخ احتياطي تلقائي للبيانات
- استيراد وتصدير قوائم الألعاب
- دعم السحابة (Cloud Storage)

## البنية التقنية / Technical Architecture

### التقنيات المستخدمة / Technologies Used
- **Python 3.8+**: لغة البرمجة الأساسية
- **PyQt5**: بناء الواجهة الرسومية
- **SQLite**: قاعدة بيانات محلية لتخزين البيانات
- **JSON**: تخزين الإعدادات والتكوينات

### الهيكل المعماري / Architectural Structure
```
game-launcher/
├── main.py              # نقطة الدخول الرئيسية
├── requirements.txt     # المكتبات المطلوبة
├── README.md           # توثيق المشروع
├── src/                # الكود المصدري
│   ├── ui/            # واجهات المستخدم
│   ├── core/          # المنطق الأساسي
│   ├── database/      # إدارة قواعد البيانات
│   └── utils/         # أدوات مساعدة
├── assets/            # الموارد (صور، أيقونات)
├── config/            # ملفات الإعدادات
└── tests/             # الاختبارات
```

## التثبيت والتشغيل / Installation & Running

### المتطلبات / Requirements
```bash
pip install -r requirements.txt
```

### التشغيل / Run
```bash
python main.py
```

## خارطة الطريق / Roadmap

### المرحلة 1 (الحالية) - الأساسيات / Phase 1 (Current) - Basics
- [x] إنشاء الهيكل الأساسي للمشروع
- [x] واجهة الترحيب الأولية
- [ ] نظام إضافة الألعاب اليدوي
- [ ] قاعدة البيانات الأساسية

### المرحلة 2 - الوظائف المتقدمة / Phase 2 - Advanced Features
- [ ] تكامل مع منصات الألعاب
- [ ] نظام البحث والفلترة المتقدم
- [ ] تتبع الوقت والإحصائيات
- [ ] نظام الثيمات والتخصيص

### المرحلة 3 - الميزات الاجتماعية / Phase 3 - Social Features
- [ ] مشاركة المكتبة مع الأصدقاء
- [ ] التوصيات الذكية
- [ ] نظام التقييمات والمراجعات
- [ ] المزامنة السحابية

## المساهمة / Contributing

نرحب بجميع المساهمات! إذا كنت ترغب في المساهمة في المشروع:
1. Fork المشروع
2. أنشئ فرع للميزة الجديدة (`git checkout -b feature/AmazingFeature`)
3. قم بعمل Commit للتغييرات (`git commit -m 'Add some AmazingFeature'`)
4. قم بعمل Push للفرع (`git push origin feature/AmazingFeature`)
5. افتح Pull Request

## الترخيص / License

هذا المشروع مفتوح المصدر ومتاح للاستخدام والتعديل.

## الاتصال / Contact

لأي استفسارات أو اقتراحات، يرجى فتح Issue في المستودع.

---

**ملاحظة**: هذا المشروع قيد التطوير النشط ويتم إضافة ميزات جديدة بانتظام.

**Note**: This project is under active development and new features are being added regularly.
