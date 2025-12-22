# backend/app/services.py

# نستورد كائن db والموديل الخاص بنا
from . import db
from .models import InventoryItem, InventoryReading
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
            rfid_uid=data.get('rfid_uid'),
            min_threshold=data.get('min_threshold', 3),  
            product_name=data.get('product_name'),
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
from datetime import datetime

# def process_sensor_reading(rfid: str, weight: float, timestamp: str | None = None):
#     try:
#         item = InventoryItem.query.filter_by(rfid_uid=rfid).first()
#         if not item:
#             return {"error": f"Unknown RFID: {rfid}. Please assign it to a product first."}, 404

#         # حساب الكمية: (الوزن الكلي - وزن الحاوية) / وزن الوحدة
#         net_weight = float(weight) - float(item.container_weight)
#         if net_weight < 0:
#             net_weight = 0

#         qty = int(round(net_weight / float(item.unit_weight))) if item.unit_weight else 0
#         if qty < 0:
#             qty = 0

#         item.total_weight = float(weight)
#         item.quantity = qty
#         item.last_update = datetime.utcnow()

#         # تحديد الحالة بناءً على threshold
#         if qty <= item.min_threshold:
#             item.status = "Low"
#         else:
#             item.status = "Normal"

#         db.session.commit()
#         return item.to_dict(), 200

#     except Exception as e:
#         db.session.rollback()
#         return {"error": str(e)}, 500

def process_sensor_reading(rfid: str, weight: float, timestamp: str | None = None):
    try:
        # 1) جلب المنتج حسب RFID
        item = InventoryItem.query.filter_by(rfid_uid=str(rfid)).first()
        if not item:
            return {
                "message": "Unknown RFID. Please assign it to a product first.",
                "rfid_uid": str(rfid)
            }, 404

        # 2) تحويل القيم بأمان
        w = float(weight)

        container_w = float(item.container_weight or 0.0)
        unit_w = float(item.unit_weight or 0.0)
        min_th = int(item.min_threshold if item.min_threshold is not None else 3)

        # 3) حساب الوزن الصافي والكمية
        net_weight = w - container_w
        if net_weight < 0:
            net_weight = 0.0

        if unit_w > 0:
            qty = int(round(net_weight / unit_w))
        else:
            qty = 0

        if qty < 0:
            qty = 0

        # 4) تحديث الحقول
        item.total_weight = w
        item.quantity = qty
        item.last_update = datetime.utcnow()

        # 5) تحديد الحالة
        item.status = "Low" if qty <= min_th else "Normal"

        # ✅ Parse timestamp safely
        ts = None
        if timestamp:
            try:
                ts = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            except Exception:
                ts = datetime.utcnow()
        else:
            ts = datetime.utcnow()

        reading = InventoryReading(
            item_id=item.item_id,
            rfid_uid=str(rfid),
            weight=float(weight),
            quantity=int(qty),
            timestamp=ts
        )
        db.session.add(reading)
        db.session.commit()

        # 6) Response مرتب للعرض + للفرونت
        return {
            "message": "Sensor reading processed successfully",
            "sensor_payload": {
                "rfid": str(rfid),
                "weight": w,
                "timestamp": ts.isoformat()
            },
            "updated_item": item.to_dict()
        }, 200

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
# ------------------------------------------------------------------
# دالة الذكاء الاصطناعي الجديدة (Predictive Analytics)
# ------------------------------------------------------------------
def predict_stock_needs(item_id: int, days_ahead: int = 7):
    try:
        # 1) نجلب آخر 30 يوم قراءات (حسب توفر البيانات)
        cutoff = datetime.utcnow() - timedelta(days=30)
        readings = (InventoryReading.query
                    .filter(InventoryReading.item_id == item_id,
                            InventoryReading.timestamp >= cutoff)
                    .order_by(InventoryReading.timestamp.asc())
                    .all())

        if len(readings) < 5:
            return {"error": "Not enough historical sensor readings to forecast (need at least 5)."}, 400

        # 2) نحولها DataFrame
        df = pd.DataFrame([r.to_dict() for r in readings])
        df["ts"] = pd.to_datetime(
            df["timestamp"],
            utc=True,
            errors="coerce",
            format="mixed"   # مهم جداً عشان اختلاف الصيغ + microseconds
        )
        # نحذف أي صف فشل تحويله
        df = df.dropna(subset=["ts"])
        df["date"] = df["ts"].dt.date
        # 3) نحسب الاستهلاك اليومي = (أول كمية - آخر كمية) أو فرق الكميات خلال اليوم
        # هنا نستخدم: max(qty) - min(qty) لكل يوم (مناسب للرف/المخزون)
        daily = df.groupby("date")["quantity"].agg(["max", "min"]).reset_index()
        daily["consumption"] = (daily["max"] - daily["min"]).clip(lower=0)

        # إذا طلع استهلاك كله أصفار -> ما يقدر يتعلم
        if daily["consumption"].sum() == 0:
            return {"error": "Consumption appears constant (no changes). Cannot build a forecasting trend."}, 400

        # 4) تجهيز X و y
        daily["day_index"] = np.arange(len(daily)) + 1
        X = daily[["day_index"]].values
        y = daily["consumption"].values

        # 5) تدريب Linear Regression
        model = LinearRegression()
        model.fit(X, y)

        # 6) توقع للأيام القادمة
        last_day = int(daily["day_index"].max())
        future_days = np.arange(last_day + 1, last_day + 1 + days_ahead).reshape(-1, 1)
        preds = model.predict(future_days)

        results = []
        for i, p in enumerate(preds):
            results.append({
                "date": (datetime.utcnow() + timedelta(days=i+1)).strftime("%Y-%m-%d"),
                "predicted_consumption": max(0, round(float(p)))
            })

        return {
            "item_id": item_id,
            "days_ahead": days_ahead,
            "based_on_days": int(len(daily)),
            "forecast": results
        }, 200

    except Exception as e:
        return {"error": str(e)}, 500