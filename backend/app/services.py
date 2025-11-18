# backend/app/services.py

# نستورد كائن db والموديل الخاص بنا
from . import db
from .models import InventoryItem

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
