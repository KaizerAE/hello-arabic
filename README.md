# game-launcher

<p align="center">
  <img src="https://raw.githubusercontent.com/KaizerAE/hello-arabic/main/assets/hero.png" alt="hello-arabic banner" width="820"/>
</p>

<p align="center">
  <a href="#-features">⚡ الميزات</a> •
  <a href="#-get-started">🚀 البدء</a> •
  <a href="#-tutorial">📘 مثال تعليمي</a> •
  <a href="#-components">🧩 جدول المكونات</a> •
  <a href="#-screenshots">🖼️ لقطات</a> •
  <a href="#-resources">🔗 مصادر</a>
</p>

> مشروع hello-arabic يقدم أمثلة عربية واضحة للتعامل مع النصوص العربية وبرمجة واجهات بسيطة، بأسلوب نظيف ومنظم شبيه بمشاريع الأجهزة (كمثال: محطة الطقس) لكن مخصص للبرمجيات والنص العربي.

---

## ⚡ الميزات
- واجهات مبسطة تدعم الاتجاه من اليمين لليسار RTL.
- أمثلة كود بايثون وجافاسكريبت لمعالجة النص العربي (تشكيل، إزالة تشكيل، قلب الاتجاه).
- قوالب جاهزة لواجهات HTML/CSS عربية مع أيقونات.
- تعليمات خطوة بخطوة للمبتدئين مع صور توضيحية.
- هيكل مشروع واضح وموحد مع صور منتجات افتراضية.

## 🚀 البدء
- المتطلبات:
  - Python 3.10+
  - Node.js (اختياري لواجهة الويب)
- التثبيت:
```bash
# استنساخ المستودع
git clone https://github.com/KaizerAE/hello-arabic
cd hello-arabic

# تفعيل بيئة افتراضية (اختياري)
python -m venv .venv
source .venv/bin/activate  # على ويندوز: .venv\\Scripts\\activate

# تثبيت التبعيات
pip install -r requirements.txt  # إن وجدت
```

## 📘 مثال تعليمي: عداد كلمات عربي بسيط
يوضح هذا المثال كيفية حساب تكرارات الكلمات العربية مع دعم إزالة التشكيل.

```python
# examples/word_counter.py
from collections import Counter
import re

ARABIC_DIACRITICS = re.compile(r"[\u0617-\u061A\u064B-\u0652]")

def normalize(text: str) -> str:
    # إزالة التشكيل وتوحيد المسافات
    text = ARABIC_DIACRITICS.sub("", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

if __name__ == "__main__":
    sample = """
    السَّلامُ عَلَيْكُم ورحمةُ اللهِ وبركاتهُ
    السلام عليكم ورحمة الله وبركاته
    """
    clean = normalize(sample)
    words = re.findall(r"[\u0621-\u064A]+", clean)
    counts = Counter(words)
    for w, c in counts.most_common():
        print(f"{w}: {c}")
```

تشغيل المثال:
```bash
python examples/word_counter.py
```

## 🧩 جدول المكونات (لمشروع واجهة تعليمية)
بالرغم من أن المشروع برمجي، إلا أن تنظيمه يستلهم من أسلوب مشاريع الأجهزة مع جدول مكونات لتسهيل الفهم:

| المكوّن | الوصف | مثال استخدام |
|---|---|---|
| Python | لغة برمجة للمعالجة النصية | سكربت word_counter |
| Regex | مطابقة نصوص عربية | استخراج الكلمات العربية |
| HTML/CSS | واجهة عربية RTL | صفحة index.html لعرض النتائج |
| Icons | أيقونات واجهة | Hero/ميزات/روابط |

> ملاحظة: في حال ربط المشروع بأجهزة (مثل Arduino لعرض النص على شاشة OLED)، يمكن إضافة مكونات مثل Arduino UNO + شاشة SSD1306 + أسلاك.

## 🖼️ لقطات وصور منتجات

<p align="center">
  <img src="https://raw.githubusercontent.com/KaizerAE/hello-arabic/main/assets/product-arduino.png" alt="Arduino board (افتراضي)" width="360"/>
  <img src="https://raw.githubusercontent.com/KaizerAE/hello-arabic/main/assets/product-python.png" alt="Python code screenshot" width="360"/>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/KaizerAE/hello-arabic/main/assets/ui-sample.png" alt="UI RTL sample" width="760"/>
</p>

إذا لم تظهر الصور، أنشئ مجلد assets وأضف صورك بنفس أسماء الملفات أعلاه، أو حدث الروابط لمسارك الخاص.

## 🧭 بنية المشروع المقترحة
```
hello-arabic/
├─ assets/
│  ├─ hero.png
│  ├─ product-arduino.png
│  ├─ product-python.png
│  └─ ui-sample.png
├─ examples/
│  └─ word_counter.py
├─ web/
│  ├─ index.html
│  └─ styles.css
├─ requirements.txt
└─ README.md
```

## 🔗 مصادر للمبتدئين
- مقدمة Python بالعربية: https://python.org/doc/
- تعلم التعابير النمطية (Regex): https://regexone.com
- RTL في الويب: https://developer.mozilla.org/en-US/docs/Web/CSS/direction
- Unicode العربية: https://unicode.org/charts/PDF/U0600.pdf

## 💬 دعم ومساهمة
- افتح Issue لأي خطأ أو اقتراح.
- مرحب بالمساهمات عبر Pull Requests.
- إن كنت مبتدئاً، ابدأ بوسم good first issue.

---

<p align="center">
  صنع بحب للعربية ✨
</p>
