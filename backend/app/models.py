# backend/app/models.py

# نستورد كائن db الذي أنشأناه في __init__.py
from . import db

# لم نعد بحاجة لـ declarative_base، لأن db.Model يقوم بالمهمة
# Base = declarative_base()

class InventoryItem(db.Model):
    __tablename__ = "inventory_items"

    item_id = db.Column(db.Integer, primary_key=True) # لا حاجة لـ index=True هنا
    rfid = db.Column(db.String(100), unique=True, nullable=True) #جديد
    product_type = db.Column(db.String(100), nullable=True) # جديد
    product_name = db.Column(db.String(100), nullable=False)
    unit_weight = db.Column(db.Float, nullable=False)
    container_weight = db.Column(db.Float, nullable=False)
    total_weight = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer)
    shelf_id = db.Column(db.Integer)
    last_update = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now())
    # status = db.Column(db.Enum('Normal', 'Low', 'Empty', 'Anomaly', name='status_enum'), default='Normal')
    # ملاحظة: Enum يتطلب معالجة خاصة، سنستخدم String مؤقتاً لتبسيط النشر
    status = db.Column(db.String(50), default='Normal')

    # دالة لتحويل الكائن إلى قاموس (dictionary) بسهولة
    def to_dict(self):
        return {
            "item_id": self.item_id,
            "rfid": self.rfid,#جديد
            "product_type": self.product_type,#جديد
            "product_name": self.product_name,
            "unit_weight": self.unit_weight,
            "container_weight": self.container_weight,
            "total_weight": self.total_weight,
            "quantity": self.quantity,
            "shelf_id": self.shelf_id,
            "last_update": self.last_update.isoformat() if self.last_update else None,
            "status": self.status
        }

