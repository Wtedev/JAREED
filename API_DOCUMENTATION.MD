# توثيق الواجهة الخلفية (Backend API) - مشروع جارد

مرحبا يا اقوى فريق 
هذا هو الدليل الرسمي لاستخدام API الخاص بالمشروع


project_URL --> https://catkzlbzcjlkngrjrmql.supabase.co

project_API_KEY --> eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNhdGt6bGJ6Y2psa25ncmpybXFsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMxNDQ4NjIsImV4cCI6MjA3ODcyMDg2Mn0.5lrVkY10_d1Q3fMuXQ2Mz1aIzUqvM84zhJJQdtypxq4


ما هو الرابط الأساسي (Base URL)؟
الرابط الأساسي (Base URL) هو نقطة البداية أو العنوان الرئيسي للخادم الذي يحتوي على كل الـ API. بدلاً من كتابة العنوان الكامل في كل مرة، نقوم بتعريف هذا الرابط مرة واحدة في كود الواجهة الأمامية، ثم نضيف إليه الروابط الفرعية (Endpoints) لكل طلب.
كيف ستستخدمينه في React؟
في كود React، عند استخدام مكتبات مثل axios أو fetch لإرسال طلبات إلى الواجهة الخلفية، ستقومين بتعريف هذا الرابط الأساسي في مكان مركزي واحد.