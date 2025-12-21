# backend/app/services.py

# نستورد كائن db والموديل الخاص بنا
from . import db
from .models import InventoryItem
from datetime import datetime, timedelta
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# يجب أن تتأكدي من أن لديك دالة to_dict() في models.py
# لغرض التبسيط، سنفترض أن لديك دالة to_dict() في models.py
# ... (بقية الدوال الموجودة مثل get_all_products_service, get_product_by_id_service, etc.) ...

def get_all_products_service():
    try:
        items = InventoryItem.query.all()
        # نحول قائمة الكائنات إلى قائمة قواميس
        return [item.to_dict() for item in items]
    except Exception as e:
        return {"error": str(e)}

def get_product_by_id_service(item_id):
    try:
        item = InventoryItem.query.get(item_id)
        return item.to_dict() if item else None
    except Exception as e:
        return {"error": str(e)}

def create_product_service(data):
    try:
        new_item = InventoryItem(
            product_name=data.get('product_name'),
            rfid=data.get("rfid"),
            product_type=data.get("product_type"),
            unit_weight=data.get('unit_weight'),
            container_weight=data.get('container_weight'),
            total_weight=data.get('total_weight'),
            quantity=data.get('quantity'),
            shelf_id=data.get('shelf_id'),
            status=data.get('status', 'Normal')
        )
        db.session.add(new_item)
        db.session.commit()
        return new_item.to_dict()
    except Exception as e:
        db.session.rollback() # مهم للتراجع عن التغييرات عند حدوث خطأ
        return {"error": str(e)}

def update_product_weight_service(item_id, new_total_weight):
    try:
        item = InventoryItem.query.get(item_id)
        if not item:
            return None
        
        item.total_weight = new_total_weight
        # هنا إضافة منطق حساب الكمية لاخقا 
        # item.quantity = ...
        
        db.session.commit()
        return item.to_dict()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}

def delete_product_service(item_id):
    try:
        item = InventoryItem.query.get(item_id)
        if not item:
            return {"message": "Product not found"}
            
        db.session.delete(item)
        db.session.commit()
        return {"message": f"Product with id {item_id} deleted successfully."}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}

# ------------------------------------------------------------------
# دالة الذكاء الاصطناعي الجديدة (Predictive Analytics)
# ------------------------------------------------------------------

def predict_stock_needs(item_id: int, days_ahead: int = 7):
    """
    تستخدم نموذج الانحدار الخطي للتنبؤ بالكمية المطلوبة لمنتج معين في الأيام القادمة.
    """
    try:
        # 1. جلب البيانات التاريخية (يجب استبدال هذا بجلب بيانات المبيعات الحقيقية من قاعدة البيانات)
        # لغرض العرض الأكاديمي، نستخدم بيانات وهمية بسيطة:
        
        # إنشاء بيانات وهمية للتدريب (الزمن مقابل الكمية المستهلكة)
        data = {
            'day_index': np.arange(1, 31), # 30 يوم من البيانات
            'quantity_sold': np.array([10, 12, 15, 11, 14, 16, 18, 15, 17, 20, 
                                       22, 25, 21, 24, 26, 28, 25, 27, 30, 32,
                                       35, 31, 34, 36, 38, 35, 37, 40, 42, 45])
        }
        df = pd.DataFrame(data)
        
        # 2. تجهيز البيانات للنموذج
        X = df[['day_index']] # المتغير المستقل (الزمن)
        y = df['quantity_sold'] # المتغير التابع (الكمية)
        
        # 3. تدريب نموذج الانحدار الخطي
        model = LinearRegression()
        model.fit(X, y)
        
        # 4. التنبؤ للأيام القادمة
        last_day = df['day_index'].max()
        future_days = np.arange(last_day + 1, last_day + 1 + days_ahead).reshape(-1, 1)
        
        predictions = model.predict(future_days)
        
        # 5. تنسيق النتائج
        results = []
        for i, pred in enumerate(predictions):
            results.append({
                "date": (datetime.now() + timedelta(days=i+1)).strftime("%Y-%m-%d"),
                "predicted_demand": max(0, round(pred)) # لا يمكن أن يكون الطلب سالباً
            })
            
        return results

    except Exception as e:
        print(f"Error in prediction service: {e}")
        return {"error": str(e)}
