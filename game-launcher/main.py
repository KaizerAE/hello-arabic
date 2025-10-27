#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Game Launcher - مشغل الألعاب
تطبيق حديث لإدارة مكتبة الألعاب
Author: KaizerAE
Version: 1.0.0
License: Open Source
"""

# تشغيل واجهة التطبيق مباشرة
from src.ui.main_window import run_application


def main():
    """نقطة دخول التطبيق"""
    print("=" * 50)
    print("🎮 Game Launcher v1.0.0")
    print("📝 مشروع مكتبة الألعاب الحديثة")
    print("🚀 Starting application...")
    print("بدء تشغيل التطبيق...")
    print("=" * 50)

    # تشغيل واجهة المستخدم PyQt5
    run_application()


if __name__ == "__main__":
    main()
