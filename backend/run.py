# backend/run.py

from app import create_app

# نقوم بإنشاء التطبيق باستخدام الـ Factory
app = create_app()

if __name__ == '__main__':
    # هذا الجزء للتشغيل المحلي فقط، Render لن يستخدمه
    app.run(debug=True)
